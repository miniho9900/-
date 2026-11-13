<?php
declare(strict_types=1);

$GLOBALS['TZ_CFG'] = require __DIR__ . '/config.php';
date_default_timezone_set('Asia/Seoul');

const TZ_COLS = ['menus','slides','popups','business','products','works','posts','partners','history','pillars','facts','site'];
const TZ_SECTIONS = ['site','menus','slides','popups','business','products','works','posts','inquiries','pillars','facts','history','partners'];
const TZ_UPLOAD_EXT = [
    'jpg'=>'image/', 'jpeg'=>'image/', 'png'=>'image/', 'gif'=>'image/', 'webp'=>'image/',
    'mp4'=>'video/', 'webm'=>'video/', 'mov'=>'video/', 'm4v'=>'video/',
    'pdf'=>'application/pdf', 'csv'=>'text/', 'txt'=>'text/',
];

function cfg(string $k) { return $GLOBALS['TZ_CFG'][$k] ?? null; }
function db_driver(): string { return strtolower(explode(':', (string)cfg('db_dsn'), 2)[0]); }

function db(): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    $pdo = new PDO((string)cfg('db_dsn'), cfg('db_user'), cfg('db_pass'), [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    if (db_driver() === 'sqlite') { $pdo->exec('PRAGMA journal_mode=WAL'); $pdo->exec('PRAGMA busy_timeout=5000'); }
    else { $pdo->exec('SET NAMES utf8mb4'); }
    return $pdo;
}
function q(string $sql, array $p = []): PDOStatement { $st = db()->prepare($sql); $st->execute($p); return $st; }
function q1(string $sql, array $p = []): ?array { $r = q($sql, $p)->fetch(); return $r ?: null; }

function create_schema(): void {
    if (db_driver() === 'sqlite') {
        $s = [
            "CREATE TABLE IF NOT EXISTS docs (col TEXT NOT NULL, id TEXT NOT NULL, data TEXT NOT NULL, updated_at TEXT NOT NULL, PRIMARY KEY (col, id))",
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL UNIQUE, name TEXT NOT NULL, pass_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'sub', perms TEXT NOT NULL DEFAULT '[]', active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, last_login TEXT)",
            "CREATE TABLE IF NOT EXISTS inquiries (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL, ip TEXT, created_at TEXT NOT NULL)",
            "CREATE TABLE IF NOT EXISTS attempts (ip TEXT NOT NULL, login TEXT, at INTEGER NOT NULL)",
        ];
    } else {
        $s = [
            "CREATE TABLE IF NOT EXISTS docs (col VARCHAR(40) NOT NULL, id VARCHAR(80) NOT NULL, data MEDIUMTEXT NOT NULL, updated_at VARCHAR(32) NOT NULL, PRIMARY KEY (col, id)) DEFAULT CHARSET=utf8mb4",
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, login VARCHAR(40) NOT NULL UNIQUE, name VARCHAR(80) NOT NULL, pass_hash VARCHAR(255) NOT NULL, role VARCHAR(10) NOT NULL DEFAULT 'sub', perms TEXT NOT NULL, active TINYINT NOT NULL DEFAULT 1, created_at VARCHAR(32) NOT NULL, last_login VARCHAR(32) NULL) DEFAULT CHARSET=utf8mb4",
            "CREATE TABLE IF NOT EXISTS inquiries (id INT AUTO_INCREMENT PRIMARY KEY, data MEDIUMTEXT NOT NULL, ip VARCHAR(64), created_at VARCHAR(32) NOT NULL) DEFAULT CHARSET=utf8mb4",
            "CREATE TABLE IF NOT EXISTS attempts (ip VARCHAR(64) NOT NULL, login VARCHAR(40), at INT NOT NULL, INDEX (ip, at)) DEFAULT CHARSET=utf8mb4",
        ];
    }
    foreach ($s as $sql) db()->exec($sql);
}
function installed(): bool {
    try { return (int)q('SELECT COUNT(*) c FROM users')->fetch()['c'] > 0; } catch (Throwable $e) { return false; }
}
function now(): string { return date('c'); }
function client_ip(): string { return substr($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0', 0, 64); }
function is_https(): bool { return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https'); }

function start_session(): void {
    session_name((string)cfg('session_name'));
    session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => is_https(), 'httponly' => true, 'samesite' => 'Lax']);
    session_start();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));
}
function current_user(): ?array {
    if (empty($_SESSION['uid'])) return null;
    $idle = (int)cfg('session_idle_minutes') * 60;
    if ($idle > 0 && time() - (int)($_SESSION['seen'] ?? 0) > $idle) { unset($_SESSION['uid']); return null; }
    $u = q1('SELECT * FROM users WHERE id = ? AND active = 1', [$_SESSION['uid']]);
    if (!$u) { unset($_SESSION['uid']); return null; }
    $_SESSION['seen'] = time();
    return $u;
}
function perms_of(array $u): array { return $u['role'] === 'super' ? ['*'] : (json_decode($u['perms'] ?: '[]', true) ?: []); }
function can(?array $u, string $sec): bool { if (!$u) return false; $p = perms_of($u); return in_array('*', $p, true) || in_array($sec, $p, true); }
function public_user(array $u): array {
    return ['id' => $u['login'], 'name' => $u['name'], 'role' => $u['role'], 'perms' => perms_of($u), 'active' => (bool)$u['active'], 'lastLogin' => $u['last_login'], 'createdAt' => $u['created_at']];
}
function valid_password(string $pw): ?string {
    if (strlen($pw) < 8) return '비밀번호는 8자 이상이어야 합니다.';
    if (!preg_match('/[A-Za-z]/', $pw) || !preg_match('/\d/', $pw)) return '비밀번호에 영문과 숫자를 함께 넣어 주세요.';
    if (strlen($pw) > 128) return '비밀번호가 너무 깁니다.';
    return null;
}
function ini_bytes(string $v): int {
    $v = trim($v); if ($v === '') return PHP_INT_MAX; $n = (int)$v; $u = strtolower(substr($v, -1));
    return $u === 'g' ? $n * 1073741824 : ($u === 'm' ? $n * 1048576 : ($u === 'k' ? $n * 1024 : $n));
}
function max_upload_bytes(): int {
    return min((int)cfg('max_upload_mb') * 1048576, ini_bytes((string)ini_get('upload_max_filesize')), ini_bytes((string)ini_get('post_max_size')));
}
// merge like the client store: nested objects merge, everything else (lists included) replaces
function merge_obj(array $a, array $b): array {
    foreach ($b as $k => $v) {
        if (is_array($v) && isset($a[$k]) && is_array($a[$k]) && !array_is_list($v) && !array_is_list($a[$k])) $a[$k] = merge_obj($a[$k], $v);
        else $a[$k] = $v;
    }
    return $a;
}
function upsert_doc(string $col, string $id, array $data): void {
    $json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    if (db_driver() === 'sqlite') q('INSERT INTO docs (col,id,data,updated_at) VALUES (?,?,?,?) ON CONFLICT(col,id) DO UPDATE SET data=excluded.data, updated_at=excluded.updated_at', [$col, $id, $json, now()]);
    else q('INSERT INTO docs (col,id,data,updated_at) VALUES (?,?,?,?) ON DUPLICATE KEY UPDATE data=VALUES(data), updated_at=VALUES(updated_at)', [$col, $id, $json, now()]);
}
function json_out(array $a, int $http = 200): void {
    http_response_code($http);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($a, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function fail(string $code, string $msg, int $http = 400): void { json_out(['ok' => false, 'code' => $code, 'error' => $msg], $http); }
