<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
header('Content-Type: text/html; charset=utf-8');
header('X-Frame-Options: DENY');

$msg = ''; $done = false;
$already = installed();
if (!$already && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $key = (string)cfg('install_key');
    $login = trim((string)($_POST['login'] ?? '')); $name = trim((string)($_POST['name'] ?? ''));
    $pw = (string)($_POST['pw'] ?? ''); $pw2 = (string)($_POST['pw2'] ?? '');
    if ($key !== '' && !hash_equals($key, (string)($_POST['key'] ?? ''))) $msg = '설치 키가 맞지 않습니다.';
    elseif (!preg_match('/^[A-Za-z0-9_.-]{3,30}$/', $login)) $msg = '아이디는 영문·숫자 3~30자로 입력하세요.';
    elseif ($name === '') $msg = '이름을 입력하세요.';
    elseif ($pw !== $pw2) $msg = '비밀번호 확인이 다릅니다.';
    elseif ($e = valid_password($pw)) $msg = $e;
    else {
        try {
            if (db_driver() === 'sqlite' && !is_dir(__DIR__ . '/data')) mkdir(__DIR__ . '/data', 0755, true);
            create_schema();
            db()->beginTransaction();
            q('INSERT INTO users (login, name, pass_hash, role, perms, active, created_at) VALUES (?,?,?,?,?,?,?)', [$login, mb_substr($name, 0, 40), password_hash($pw, PASSWORD_DEFAULT), 'super', '[]', 1, now()]);
            $count = (int)q('SELECT COUNT(*) c FROM docs')->fetch()['c'];
            $seedFile = __DIR__ . '/data/seed.json';
            $imported = 0;
            if ($count === 0 && is_file($seedFile)) {
                foreach (json_decode((string)file_get_contents($seedFile), true) ?: [] as $d) {
                    [$col, $id] = explode('/', $d['path'], 2) + [1 => ''];
                    if (in_array($col, TZ_COLS, true) && preg_match('/^[A-Za-z0-9_-]{1,80}$/', $id)) { upsert_doc($col, $id, $d['data']); $imported++; }
                }
            }
            db()->commit();
            $done = true; $msg = "설치를 마쳤습니다. 기본 콘텐츠 {$imported}건을 넣었습니다.";
        } catch (Throwable $e) {
            if (db()->inTransaction()) db()->rollBack();
            $msg = '설치하지 못했습니다: ' . $e->getMessage();
        }
    }
}
$ok = [
    'PHP 8.0 이상' => version_compare(PHP_VERSION, '8.0.0', '>='),
    'PDO ' . strtoupper(db_driver()) . ' 드라이버' => in_array(db_driver(), PDO::getAvailableDrivers(), true),
    'data 폴더 쓰기 권한' => db_driver() !== 'sqlite' || is_writable(__DIR__ . '/data'),
    'uploads 폴더 쓰기 권한' => is_writable(__DIR__ . '/uploads'),
];
$h = fn($s) => htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');
?><!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>트리즈엔 홈페이지 설치</title>
<style>body{margin:0;font-family:"Noto Sans KR",system-ui,sans-serif;background:#0B0A45;color:#fff;display:grid;place-items:center;min-height:100vh;padding:24px;box-sizing:border-box}
.box{background:#fff;color:#17162E;width:min(460px,100%);padding:36px;border-radius:12px;display:grid;gap:16px}h1{margin:0;font-size:22px}label{display:grid;gap:6px;font-size:14px;font-weight:500}
input{border:1px solid #D3D0E3;border-radius:6px;padding:11px 12px;font-size:15px}button,.btn{background:#5230C2;color:#fff;border:0;border-radius:6px;padding:13px;font-size:15px;font-weight:500;cursor:pointer;text-align:center;text-decoration:none}
.msg{padding:12px 14px;border-radius:6px;background:#FDECEC;color:#A12B2B;font-size:14px}.ok{background:#E8F5EE;color:#1E6B47}ul{margin:0;padding-left:18px;font-size:14px;line-height:1.9}.no{color:#C93B3B}p{margin:0;font-size:14px;color:#6C6A86}</style></head><body>
<div class="box">
<?php if ($already && !$done): ?>
  <h1>이미 설치되었습니다</h1><p>관리자 계정이 있어서 설치 화면은 잠겨 있습니다. 보안을 위해 이 파일(install.php)은 서버에서 지워도 됩니다.</p><a class="btn" href="./#admin">관리자 로그인으로</a>
<?php elseif ($done): ?>
  <h1>설치 완료</h1><div class="msg ok"><?= $h($msg) ?></div><p>보안을 위해 install.php 파일은 서버에서 지워 주세요.</p><a class="btn" href="./#admin">관리자 로그인하기</a>
<?php else: ?>
  <h1>트리즈엔 홈페이지 설치</h1><p>최고관리자 계정을 만들면 기본 콘텐츠가 함께 들어갑니다.</p>
  <ul><?php foreach ($ok as $k => $v): ?><li class="<?= $v ? '' : 'no' ?>"><?= $h($k) ?> — <?= $v ? '확인' : '필요' ?></li><?php endforeach; ?></ul>
  <?php if ($msg): ?><div class="msg"><?= $h($msg) ?></div><?php endif; ?>
  <form method="post" style="display:grid;gap:14px" autocomplete="off">
    <?php if ((string)cfg('install_key') !== ''): ?><label>설치 키<input name="key" required></label><?php endif; ?>
    <label>최고관리자 아이디<input name="login" required pattern="[A-Za-z0-9_.\-]{3,30}" value="<?= $h($_POST['login'] ?? '') ?>"></label>
    <label>이름<input name="name" required maxlength="40" value="<?= $h($_POST['name'] ?? '') ?>"></label>
    <label>비밀번호 (8자 이상, 영문+숫자)<input type="password" name="pw" required minlength="8" autocomplete="new-password"></label>
    <label>비밀번호 확인<input type="password" name="pw2" required minlength="8" autocomplete="new-password"></label>
    <button type="submit">설치하기</button>
  </form>
<?php endif; ?>
</div></body></html>
