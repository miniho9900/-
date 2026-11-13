<?php
// 트리즈엔 홈페이지 서버 설정 — 호스팅에 맞게 이 파일만 고치면 됩니다.
return [
    // 데이터베이스
    //  · SQLite(기본): 별도 DB 없이 data/ 폴더에 파일로 저장합니다.
    //  · MySQL: 'mysql:host=localhost;dbname=trizn;charset=utf8mb4' 로 바꾸고 아래 계정을 채우세요.
    'db_dsn'  => 'sqlite:' . __DIR__ . '/data/trizn.sqlite',
    'db_user' => null,
    'db_pass' => null,

    // 업로드 한 파일 최대 크기(MB). 호스팅의 PHP 업로드 한도(upload_max_filesize, post_max_size)보다 클 수 없습니다.
    'max_upload_mb' => 512,

    // 로그인 유지 시간(분). 이 시간 동안 아무 작업이 없으면 자동 로그아웃됩니다.
    'session_idle_minutes' => 120,
    'session_name' => 'TRIZN_ADMIN',

    // 설치 키: 값을 넣으면 install.php에서 이 키를 입력해야 설치됩니다. (서버에 올린 직후 남이 먼저 설치하는 것을 막습니다)
    'install_key' => '',
];
