/* 트리즈엔 관리자 체험판 — 브라우저 안의 가상 서버
   server/api.php 와 같은 요청(bootstrap, login, write, upload, users …)을 같은 규칙으로 처리합니다.
   데이터는 이 브라우저의 localStorage 에만 저장되는 시험용입니다. */
(function () {
  "use strict";
  var KEY = "trizn-demo-v5", SKEY = "trizn-demo-session-v3";
  var SECTIONS = ["site","menus","slides","popups","business","products","models","works","posts","inquiries","pillars","facts","history","partners","clients"];
  var COLS = ["menus","slides","popups","business","products","models","works","posts","partners","clients","history","pillars","facts","site"];
  var MAX = 512 * 1048576;
  var mem = null, sess = null;

  function now() { return new Date().toISOString(); }
  function load() {
    if (mem) return mem;
    try { var raw = localStorage.getItem(KEY); if (raw) mem = JSON.parse(raw); } catch (e) {}
    if (!mem || !mem.docs) mem = null;
    return mem;
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch (e) {} }
  function session() {
    if (sess) return sess;
    try { sess = JSON.parse(sessionStorage.getItem(SKEY) || "null"); } catch (e) {}
    if (!sess) sess = { csrf: rand(16), uid: null };
    return sess;
  }
  function saveSess() { try { sessionStorage.setItem(SKEY, JSON.stringify(sess)); } catch (e) {} }
  function rand(n) { var a = new Uint8Array(n); crypto.getRandomValues(a); return Array.from(a, function (b) { return b.toString(16).padStart(2, "0"); }).join(""); }
  async function hash(pw, salt) {
    var d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(salt + ":" + pw));
    return salt + "$" + Array.from(new Uint8Array(d), function (b) { return b.toString(16).padStart(2, "0"); }).join("");
  }
  async function verify(pw, stored) { var salt = String(stored).split("$")[0]; return (await hash(pw, salt)) === stored; }
  function validPw(pw) {
    if (pw.length < 8) return "비밀번호는 8자 이상이어야 합니다.";
    if (!/[A-Za-z]/.test(pw) || !/\d/.test(pw)) return "비밀번호에 영문과 숫자를 함께 넣어 주세요.";
    return null;
  }
  async function init() {
    if (load()) return mem;
    var seed = window.TRIZN_DEMO_SEED || [];
    mem = { docs: {}, users: [], inquiries: [], attempts: [] };
    seed.forEach(function (d) { var p = d.path.split("/"); (mem.docs[p[0]] = mem.docs[p[0]] || {})[p[1]] = d.data; });
    mem.users.push({ id: 1, login: "admin", name: "최고관리자", pass: await hash("Trizn2026x", rand(8)), role: "super", perms: [], active: true, created: now(), last: null });
    mem.users.push({ id: 2, login: "editor1", name: "홍보담당", pass: await hash("Editor2026", rand(8)), role: "sub", perms: ["posts", "popups"], active: true, created: now(), last: null });
    save();
    return mem;
  }
  function me() { var s = session(); return s.uid ? mem.users.find(function (u) { return u.id === s.uid && u.active; }) || null : null; }
  function permsOf(u) { return u.role === "super" ? ["*"] : u.perms || []; }
  function can(u, sec) { if (!u) return false; var p = permsOf(u); return p.indexOf("*") >= 0 || p.indexOf(sec) >= 0; }
  function pub(u) { return { id: u.login, name: u.name, role: u.role, perms: permsOf(u), active: !!u.active, lastLogin: u.last, createdAt: u.created }; }
  function isList(v) { return Array.isArray(v); }
  function isObj(v) { return v && typeof v === "object" && !Array.isArray(v); }
  function merge(a, b) { var o = Object.assign({}, a); Object.keys(b).forEach(function (k) { o[k] = isObj(b[k]) && isObj(a[k]) ? merge(a[k], b[k]) : b[k]; }); return o; }
  function Fail(code, msg, http) { this.code = code; this.msg = msg; this.http = http || 400; }
  function fail(code, msg, http) { throw new Fail(code, msg, http); }
  var supers = function (exceptId) { return mem.users.filter(function (u) { return u.role === "super" && u.active && u.id !== exceptId; }).length; };

  async function handle(action, method, body, form, headers) {
    await init();
    var s = session(), u = me(), isPost = method === "POST";
    if (isPost && headers["X-CSRF"] !== s.csrf) fail("csrf", "페이지를 새로고침한 뒤 다시 시도하세요.", 403);
    var need = function (sec) { if (!u) fail("auth", "로그인이 필요합니다.", 401); if (sec && !can(u, sec)) fail("forbidden", "이 메뉴를 수정할 권한이 없습니다.", 403); };
    var superOnly = function () { if (!u || u.role !== "super") fail("forbidden", "최고관리자만 할 수 있습니다.", 403); };
    switch (action) {
    case "bootstrap": {
      var data = {};
      COLS.forEach(function (c) { data[c] = Object.keys(mem.docs[c] || {}).map(function (id) { return { id: id, data: mem.docs[c][id] }; }); });
      if (u) data.drafts = Object.keys(mem.docs.drafts || {}).filter(function (id) { return can(u, id.split("__")[0]); }).map(function (id) { return { id: id, data: mem.docs.drafts[id] }; });
      if (can(u, "inquiries")) data.inquiries = [{ id: "all", data: { items: mem.inquiries.slice().reverse() } }];
      return { ok: true, data: data, me: u ? pub(u) : null, csrf: s.csrf, maxUpload: MAX };
    }
    case "login": {
      var t = Date.now() - 900000;
      mem.attempts = mem.attempts.filter(function (a) { return a.at > t; });
      if (mem.attempts.filter(function (a) { return a.login === body.id; }).length >= 5) fail("too_many", "로그인 시도가 많습니다. 15분 뒤 다시 시도하세요.", 429);
      var x = mem.users.find(function (v) { return v.login === String(body.id || "").trim(); });
      if (!x || !x.active || !(await verify(String(body.pw || ""), x.pass))) { mem.attempts.push({ login: body.id, at: Date.now() }); save(); fail("invalid", "아이디 또는 비밀번호가 맞지 않습니다.", 401); }
      s.uid = x.id; s.csrf = rand(16); saveSess(); x.last = now(); mem.attempts = mem.attempts.filter(function (a) { return a.login !== x.login; }); save();
      return { ok: true };
    }
    case "logout": sess = { csrf: rand(16), uid: null }; saveSess(); return { ok: true };
    case "write": {
      var col = String(body.col || ""), id = String(body.id || ""), op = body.op;
      if (!/^[A-Za-z0-9_-]{1,80}$/.test(id)) fail("invalid_argument", "잘못된 문서 번호입니다.");
      if (col === "drafts") { var tg = id.split("__")[0]; if (COLS.indexOf(tg) < 0) fail("invalid_argument", "잘못된 반영 대기 항목입니다."); need(tg); }
      else { if (COLS.indexOf(col) < 0) fail("invalid_argument", "알 수 없는 항목입니다."); need(col); }
      var bag = mem.docs[col] = mem.docs[col] || {};
      if (op === "delete") { delete bag[id]; save(); return { ok: true }; }
      var d = body.data; if (!isObj(d)) fail("invalid_argument", "저장할 내용이 올바르지 않습니다.");
      if (op === "update") { if (!bag[id]) fail("invalid_argument", "이미 삭제된 항목입니다."); d = merge(bag[id], d); }
      else if (op !== "set") fail("invalid_argument", "잘못된 요청입니다.");
      bag[id] = d; save();
      return { ok: true, data: d };
    }
    case "upload": {
      need(null);
      if (!SECTIONS.some(function (sec) { return can(u, sec); })) fail("forbidden", "업로드 권한이 없습니다.", 403);
      var f = form && form.get("file");
      if (!f) fail("invalid_argument", "파일을 받지 못했습니다.");
      var ext = (String(f.name).split(".").pop() || "").toLowerCase();
      if (["jpg","jpeg","png","gif","webp","mp4","webm","mov","m4v","pdf","csv","txt"].indexOf(ext) < 0) fail("invalid_argument", "올릴 수 없는 파일 형식입니다. (이미지, MP4/WEBM 영상, PDF만 가능)");
      if (f.size > MAX) fail("quota_exceeded", "파일이 업로드 한도보다 큽니다.", 413);
      var url = URL.createObjectURL(f);
      return { ok: true, id: url, url: url, size: f.size, type: f.type };
    }
    case "inquiry": {
      if (String(body.website || "").trim()) return { ok: true };
      var item = {};
      [["name",60],["contact",80],["type",30],["body",2000]].forEach(function (p) { var v = String(body[p[0]] || "").trim(); if (!v && p[0] !== "type") fail("invalid_argument", "필수 항목을 모두 입력해 주세요."); item[p[0]] = v.slice(0, p[1]); });
      item.id = "q" + Date.now(); item.at = now(); mem.inquiries.push(item); save();
      return { ok: true };
    }
    case "users": superOnly(); return { ok: true, users: mem.users.map(pub) };
    case "user_save": {
      superOnly();
      var login = String(body.id || "").trim(), name = String(body.name || "").trim().slice(0, 40), role = body.role === "super" ? "super" : "sub";
      var perms = (body.perms || []).filter(function (p) { return SECTIONS.indexOf(p) >= 0; }), active = !!body.active, pw = String(body.password || "");
      if (!name) fail("invalid_argument", "이름을 입력하세요.");
      if (body.isNew) {
        if (!/^[A-Za-z0-9_.-]{3,30}$/.test(login)) fail("invalid_argument", "아이디는 영문·숫자 3~30자로 입력하세요.");
        if (mem.users.some(function (v) { return v.login === login; })) fail("invalid_argument", "이미 있는 아이디입니다.");
        var e1 = validPw(pw); if (e1) fail("invalid_argument", e1);
        mem.users.push({ id: Math.max.apply(null, mem.users.map(function (v) { return v.id; })) + 1, login: login, name: name, pass: await hash(pw, rand(8)), role: role, perms: perms, active: active, created: now(), last: null });
      } else {
        var t2 = mem.users.find(function (v) { return v.login === login; }); if (!t2) fail("invalid_argument", "계정을 찾을 수 없습니다.");
        if (t2.id === u.id && (!active || role !== "super")) fail("invalid_argument", "내 계정의 최고관리자 권한이나 사용 상태는 바꿀 수 없습니다.");
        if (t2.role === "super" && (role !== "super" || !active) && supers(t2.id) < 1) fail("invalid_argument", "최고관리자가 최소 한 명은 있어야 합니다.");
        if (pw) { var e2 = validPw(pw); if (e2) fail("invalid_argument", e2); t2.pass = await hash(pw, rand(8)); }
        t2.name = name; t2.role = role; t2.perms = perms; t2.active = active;
      }
      save(); return { ok: true };
    }
    case "user_delete": {
      superOnly();
      var t3 = mem.users.find(function (v) { return v.login === body.id; }); if (!t3) fail("invalid_argument", "계정을 찾을 수 없습니다.");
      if (t3.id === u.id) fail("invalid_argument", "내 계정은 삭제할 수 없습니다.");
      if (t3.role === "super" && supers(t3.id) < 1) fail("invalid_argument", "최고관리자가 최소 한 명은 있어야 합니다.");
      mem.users = mem.users.filter(function (v) { return v !== t3; }); save(); return { ok: true };
    }
    case "password": {
      need(null);
      if (!(await verify(String(body.cur || ""), u.pass))) fail("invalid_argument", "현재 비밀번호가 맞지 않습니다.");
      var e3 = validPw(String(body.nw || "")); if (e3) fail("invalid_argument", e3);
      u.pass = await hash(String(body.nw), rand(8)); save(); return { ok: true };
    }
    default: fail("unknown_action", "알 수 없는 요청입니다.", 404);
    }
  }

  var realFetch = window.fetch.bind(window);
  window.fetch = function (input, opt) {
    var url = typeof input === "string" ? input : input.url;
    if (!/^api\.php\?/.test(url)) return realFetch(input, opt);
    opt = opt || {};
    var action = decodeURIComponent((url.match(/action=([^&]+)/) || [])[1] || "");
    var form = opt.body instanceof FormData ? opt.body : null, body = {};
    if (opt.body && !form) { try { body = JSON.parse(opt.body); } catch (e) {} }
    return handle(action, opt.method || "GET", body, form, opt.headers || {}).then(function (r) { return r; }, function (e) {
      if (e instanceof Fail) return { ok: false, code: e.code, error: e.msg, __http: e.http };
      console.error(e); return { ok: false, code: "unavailable", error: "체험판 오류가 발생했습니다.", __http: 500 };
    }).then(function (j) {
      var http = j.__http || 200; delete j.__http;
      return new Response(JSON.stringify(j), { status: http, headers: { "Content-Type": "application/json" } });
    });
  };

  window.TRIZN_DEMO_RESET = function () { try { localStorage.removeItem(KEY); sessionStorage.removeItem(SKEY); } catch (e) {} location.hash = "#admin"; location.reload(); };
  document.addEventListener("DOMContentLoaded", function () {
    var bar = document.createElement("div");
    bar.className = "demo-bar";
    bar.innerHTML = '<b>체험판</b><span>테스트 계정 — 최고관리자 <code>admin</code> / <code>Trizn2026x</code> · 서브관리자(게시판·팝업) <code>editor1</code> / <code>Editor2026</code></span><span class="demo-note">바꾼 내용은 이 브라우저에만 저장되고, 올린 파일은 새로고침하면 사라집니다.</span><button type="button" id="demoReset">처음 상태로</button>';
    document.body.appendChild(bar);
    document.getElementById("demoReset").addEventListener("click", window.TRIZN_DEMO_RESET);
  });
})();
