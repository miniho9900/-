<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

try {
    if (!installed()) fail('not_installed', '아직 설치되지 않았습니다. install.php를 먼저 실행하세요.', 503);
    start_session();
    $action = (string)($_GET['action'] ?? '');
    $isPost = ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST';
    if ($isPost && !hash_equals($_SESSION['csrf'], (string)($_SERVER['HTTP_X_CSRF'] ?? ''))) fail('csrf', '페이지를 새로고침한 뒤 다시 시도하세요.', 403);
    $body = [];
    if ($isPost && $action !== 'upload') {
        $raw = file_get_contents('php://input') ?: '';
        if (strlen($raw) > 2 * 1048576) fail('invalid_argument', '보내는 내용이 너무 큽니다.', 413);
        $body = json_decode($raw, true);
        if (!is_array($body)) fail('invalid_argument', '잘못된 요청입니다.');
    }
    $me = current_user();
    $need = function (?string $sec = null) use ($me) {
        if (!$me) fail('auth', '로그인이 필요합니다.', 401);
        if ($sec !== null && !can($me, $sec)) fail('forbidden', '이 메뉴를 수정할 권한이 없습니다.', 403);
    };
    $super = function () use ($me) { if (!$me || $me['role'] !== 'super') fail('forbidden', '최고관리자만 할 수 있습니다.', 403); };

    switch ($action) {
    case 'bootstrap':
        $data = array_fill_keys(TZ_COLS, []);
        foreach (q('SELECT col, id, data FROM docs')->fetchAll() as $r) {
            if (!isset($data[$r['col']])) continue;
            $data[$r['col']][] = ['id' => $r['id'], 'data' => json_decode($r['data'], true) ?: []];
        }
        if ($me && can($me, 'inquiries')) {
            $items = array_map(fn($r) => (json_decode($r['data'], true) ?: []) + ['id' => 'q' . $r['id'], 'at' => $r['created_at']], q('SELECT * FROM inquiries ORDER BY id DESC LIMIT 500')->fetchAll());
            $data['inquiries'] = [['id' => 'all', 'data' => ['items' => $items]]];
        }
        json_out(['ok' => true, 'data' => $data, 'me' => $me ? public_user($me) : null, 'csrf' => $_SESSION['csrf'], 'maxUpload' => max_upload_bytes()]);

    case 'login':
        if (!$isPost) fail('method', 'POST만 됩니다.', 405);
        $login = substr(trim((string)($body['id'] ?? '')), 0, 40); $pw = (string)($body['pw'] ?? '');
        $since = time() - 900;
        q('DELETE FROM attempts WHERE at < ?', [time() - 86400]);
        $n = (int)q('SELECT COUNT(*) c FROM attempts WHERE ip = ? AND at > ?', [client_ip(), $since])->fetch()['c'];
        $nl = (int)q('SELECT COUNT(*) c FROM attempts WHERE login = ? AND at > ?', [$login, $since])->fetch()['c'];
        if ($n >= 10 || $nl >= 5) fail('too_many', '로그인 시도가 많습니다. 15분 뒤 다시 시도하세요.', 429);
        $u = q1('SELECT * FROM users WHERE login = ?', [$login]);
        if (!$u || !(int)$u['active'] || !password_verify($pw, $u['pass_hash'])) {
            q('INSERT INTO attempts (ip, login, at) VALUES (?,?,?)', [client_ip(), $login, time()]);
            usleep(400000);
            fail('invalid', '아이디 또는 비밀번호가 맞지 않습니다.', 401);
        }
        session_regenerate_id(true);
        $_SESSION['uid'] = (int)$u['id']; $_SESSION['seen'] = time();
        if (password_needs_rehash($u['pass_hash'], PASSWORD_DEFAULT)) q('UPDATE users SET pass_hash = ? WHERE id = ?', [password_hash($pw, PASSWORD_DEFAULT), $u['id']]);
        q('UPDATE users SET last_login = ? WHERE id = ?', [now(), $u['id']]);
        q('DELETE FROM attempts WHERE login = ?', [$login]);
        json_out(['ok' => true]);

    case 'logout':
        $_SESSION = []; session_regenerate_id(true); $_SESSION['csrf'] = bin2hex(random_bytes(16));
        json_out(['ok' => true]);

    case 'write':
        if (!$isPost) fail('method', 'POST만 됩니다.', 405);
        $col = (string)($body['col'] ?? ''); $id = (string)($body['id'] ?? ''); $op = (string)($body['op'] ?? '');
        if (!in_array($col, TZ_COLS, true)) fail('invalid_argument', '알 수 없는 항목입니다.');
        if (!preg_match('/^[A-Za-z0-9_-]{1,80}$/', $id)) fail('invalid_argument', '잘못된 문서 번호입니다.');
        $need($col);
        $cur = q1('SELECT data FROM docs WHERE col = ? AND id = ?', [$col, $id]);
        if ($op === 'delete') { q('DELETE FROM docs WHERE col = ? AND id = ?', [$col, $id]); json_out(['ok' => true]); }
        $data = $body['data'] ?? null;
        if (!is_array($data) || ($data && array_is_list($data))) fail('invalid_argument', '저장할 내용이 올바르지 않습니다.');
        if ($op === 'update') { if (!$cur) fail('invalid_argument', '이미 삭제된 항목입니다.'); $data = merge_obj(json_decode($cur['data'], true) ?: [], $data); }
        elseif ($op !== 'set') fail('invalid_argument', '잘못된 요청입니다.');
        if (strlen(json_encode($data)) > 1048576) fail('quota_exceeded', '내용이 너무 깁니다.', 413);
        upsert_doc($col, $id, $data);
        json_out(['ok' => true, 'data' => $data]);

    case 'upload':
        if (!$isPost) fail('method', 'POST만 됩니다.', 405);
        $need();
        if (!array_filter(TZ_SECTIONS, fn($s) => can($me, $s))) fail('forbidden', '업로드 권한이 없습니다.', 403);
        $f = $_FILES['file'] ?? null;
        if (!$f || ($f['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
            $err = $f['error'] ?? UPLOAD_ERR_NO_FILE;
            fail('invalid_argument', in_array($err, [UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE], true) ? '파일이 서버 업로드 한도보다 큽니다.' : '파일을 받지 못했습니다.', 400);
        }
        if ($f['size'] > max_upload_bytes()) fail('quota_exceeded', '파일이 업로드 한도보다 큽니다.', 413);
        $ext = strtolower(pathinfo((string)$f['name'], PATHINFO_EXTENSION));
        if (!isset(TZ_UPLOAD_EXT[$ext])) fail('invalid_argument', '올릴 수 없는 파일 형식입니다. (이미지, MP4/WEBM 영상, PDF만 가능)');
        $mime = function_exists('finfo_open') ? (string)finfo_file(finfo_open(FILEINFO_MIME_TYPE), $f['tmp_name']) : '';
        if ($mime !== '' && !str_starts_with($mime, TZ_UPLOAD_EXT[$ext]) && !($ext === 'webm' && $mime === 'audio/webm')) fail('invalid_argument', '파일 내용이 확장자와 맞지 않습니다.');
        $name = bin2hex(random_bytes(12)) . '.' . $ext;
        $dir = __DIR__ . '/uploads';
        if (!is_dir($dir)) mkdir($dir, 0755, true);
        if (!move_uploaded_file($f['tmp_name'], "$dir/$name")) fail('unavailable', '파일을 저장하지 못했습니다. uploads 폴더 쓰기 권한을 확인하세요.', 500);
        @chmod("$dir/$name", 0644);
        json_out(['ok' => true, 'id' => $name, 'url' => 'uploads/' . $name, 'size' => (int)$f['size'], 'type' => $mime]);

    case 'inquiry':
        if (!$isPost) fail('method', 'POST만 됩니다.', 405);
        if (trim((string)($body['website'] ?? '')) !== '') json_out(['ok' => true]); // honeypot
        $item = [];
        foreach (['name' => 60, 'contact' => 80, 'type' => 30, 'body' => 2000] as $k => $max) {
            $v = trim((string)($body[$k] ?? ''));
            if ($v === '' && $k !== 'type') fail('invalid_argument', '필수 항목을 모두 입력해 주세요.');
            $item[$k] = mb_substr($v, 0, $max);
        }
        $n = (int)q('SELECT COUNT(*) c FROM inquiries WHERE ip = ? AND created_at > ?', [client_ip(), date('c', time() - 3600)])->fetch()['c'];
        if ($n >= 5) fail('resource_exhausted', '짧은 시간에 문의가 많이 접수되었습니다. 잠시 뒤 다시 시도하거나 전화로 문의해 주세요.', 429);
        q('INSERT INTO inquiries (data, ip, created_at) VALUES (?,?,?)', [json_encode($item, JSON_UNESCAPED_UNICODE), client_ip(), now()]);
        json_out(['ok' => true]);

    case 'users':
        $super();
        json_out(['ok' => true, 'users' => array_map('public_user', q('SELECT * FROM users ORDER BY role DESC, id')->fetchAll())]);

    case 'user_save':
        if (!$isPost) fail('method', 'POST만 됩니다.', 405);
        $super();
        $login = trim((string)($body['id'] ?? '')); $isNew = !empty($body['isNew']);
        $name = mb_substr(trim((string)($body['name'] ?? '')), 0, 40);
        $role = ($body['role'] ?? 'sub') === 'super' ? 'super' : 'sub';
        $perms = array_values(array_intersect(TZ_SECTIONS, array_map('strval', (array)($body['perms'] ?? []))));
        $active = !empty($body['active']) ? 1 : 0;
        $pw = (string)($body['password'] ?? '');
        if ($name === '') fail('invalid_argument', '이름을 입력하세요.');
        if ($isNew) {
            if (!preg_match('/^[A-Za-z0-9_.-]{3,30}$/', $login)) fail('invalid_argument', '아이디는 영문·숫자 3~30자로 입력하세요.');
            if (q1('SELECT id FROM users WHERE login = ?', [$login])) fail('invalid_argument', '이미 있는 아이디입니다.');
            if ($e = valid_password($pw)) fail('invalid_argument', $e);
            q('INSERT INTO users (login, name, pass_hash, role, perms, active, created_at) VALUES (?,?,?,?,?,?,?)', [$login, $name, password_hash($pw, PASSWORD_DEFAULT), $role, json_encode($perms), $active, now()]);
        } else {
            $u = q1('SELECT * FROM users WHERE login = ?', [$login]);
            if (!$u) fail('invalid_argument', '계정을 찾을 수 없습니다.');
            if ((int)$u['id'] === (int)$me['id'] && (!$active || $role !== 'super')) fail('invalid_argument', '내 계정의 최고관리자 권한이나 사용 상태는 바꿀 수 없습니다.');
            if ($u['role'] === 'super' && ($role !== 'super' || !$active)) {
                $others = (int)q("SELECT COUNT(*) c FROM users WHERE role = 'super' AND active = 1 AND id <> ?", [$u['id']])->fetch()['c'];
                if ($others < 1) fail('invalid_argument', '최고관리자가 최소 한 명은 있어야 합니다.');
            }
            if ($pw !== '') { if ($e = valid_password($pw)) fail('invalid_argument', $e); q('UPDATE users SET pass_hash = ? WHERE id = ?', [password_hash($pw, PASSWORD_DEFAULT), $u['id']]); }
            q('UPDATE users SET name = ?, role = ?, perms = ?, active = ? WHERE id = ?', [$name, $role, json_encode($perms), $active, $u['id']]);
        }
        json_out(['ok' => true]);

    case 'user_delete':
        if (!$isPost) fail('method', 'POST만 됩니다.', 405);
        $super();
        $u = q1('SELECT * FROM users WHERE login = ?', [(string)($body['id'] ?? '')]);
        if (!$u) fail('invalid_argument', '계정을 찾을 수 없습니다.');
        if ((int)$u['id'] === (int)$me['id']) fail('invalid_argument', '내 계정은 삭제할 수 없습니다.');
        if ($u['role'] === 'super' && (int)q("SELECT COUNT(*) c FROM users WHERE role = 'super' AND active = 1 AND id <> ?", [$u['id']])->fetch()['c'] < 1) fail('invalid_argument', '최고관리자가 최소 한 명은 있어야 합니다.');
        q('DELETE FROM users WHERE id = ?', [$u['id']]);
        json_out(['ok' => true]);

    case 'password':
        if (!$isPost) fail('method', 'POST만 됩니다.', 405);
        $need();
        if (!password_verify((string)($body['cur'] ?? ''), $me['pass_hash'])) fail('invalid_argument', '현재 비밀번호가 맞지 않습니다.');
        if ($e = valid_password((string)($body['nw'] ?? ''))) fail('invalid_argument', $e);
        q('UPDATE users SET pass_hash = ? WHERE id = ?', [password_hash((string)$body['nw'], PASSWORD_DEFAULT), $me['id']]);
        json_out(['ok' => true]);

    default:
        fail('unknown_action', '알 수 없는 요청입니다.', 404);
    }
} catch (Throwable $e) {
    error_log('[trizn api] ' . $e->getMessage());
    fail('unavailable', '서버 오류가 발생했습니다. 잠시 후 다시 시도하세요.', 500);
}
