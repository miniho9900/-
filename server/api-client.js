/* 트리즈엔 홈페이지 — PHP 서버 연결 (화면 코드가 쓰는 저장소·업로드·로그인 기능을 서버 API로 연결합니다) */
(function () {
  "use strict";
  var API = window.TRIZN_API || "api.php";
  var csrf = "", me = null, cache = null, subs = [], loading = null;

  function call(action, body, isForm) {
    var opt = { method: body === undefined ? "GET" : "POST", credentials: "same-origin", headers: { "X-CSRF": csrf } };
    if (body !== undefined) { if (isForm) opt.body = body; else { opt.headers["Content-Type"] = "application/json"; opt.body = JSON.stringify(body); } }
    return fetch(API + "?action=" + encodeURIComponent(action), opt).then(function (r) {
      return r.json().catch(function () { return { ok: false, code: "unavailable", error: "서버 응답을 읽지 못했습니다." }; }).then(function (j) {
        if (!r.ok || j.ok === false) { var e = new Error(j.error || "요청을 처리하지 못했습니다."); e.code = j.code || "unavailable"; throw e; }
        return j;
      });
    });
  }
  function apply(j) { cache = j.data || {}; me = j.me || null; csrf = j.csrf || csrf; window.TRIZN_MAX_UPLOAD = j.maxUpload || window.TRIZN_MAX_UPLOAD; }
  function ready() { return loading || (loading = call("bootstrap").then(apply)); }
  function emit() { subs.slice().forEach(function (f) { try { f(); } catch (e) { console.error(e); } }); }
  function refresh() { return call("bootstrap").then(function (j) { apply(j); emit(); }); }
  setInterval(function () { if (!document.hidden && !document.getElementById("edForm")) refresh().catch(function () {}); }, 60000);

  function find(c, id) { return (cache[c] || []).find(function (d) { return d.id === id; }); }
  function putLocal(c, id, data) { var list = cache[c] || (cache[c] = []); var d = find(c, id); if (d) d.data = data; else list.push({ id: id, data: data }); }
  function snapDoc(c, id) { var d = find(c, id); return { id: id, exists: !!d, data: function () { return d ? d.data : undefined; }, metadata: { fromCache: false, hasPendingWrites: false } }; }
  function listen(fn, err) { subs.push(fn); ready().then(fn).catch(function (e) { if (err) err({ code: e.code || "unavailable", message: e.message }); }); return function () { subs = subs.filter(function (x) { return x !== fn; }); }; }
  function docRef(path) {
    var p = path.split("/"), c = p[0], id = p[1];
    return {
      id: id, path: path,
      get: function () { return ready().then(function () { return snapDoc(c, id); }); },
      onSnapshot: function (next, err) { return listen(function () { next(snapDoc(c, id)); }, err); },
      set: function (data) { return call("write", { op: "set", col: c, id: id, data: data }).then(function (j) { putLocal(c, id, j.data); emit(); }); },
      update: function (data) { return call("write", { op: "update", col: c, id: id, data: data }).then(function (j) { putLocal(c, id, j.data); emit(); }); },
      delete: function () { return call("write", { op: "delete", col: c, id: id }).then(function () { cache[c] = (cache[c] || []).filter(function (d) { return d.id !== id; }); emit(); }); }
    };
  }
  var db = {
    doc: docRef,
    collection: function (c) {
      return {
        doc: function (id) { return docRef(c + "/" + id); },
        onSnapshot: function (next, err) {
          return listen(function () {
            var docs = (cache[c] || []).map(function (d) { return { id: d.id, exists: true, data: function () { return d.data; }, metadata: { fromCache: false, hasPendingWrites: false } }; });
            next({ docs: docs, size: docs.length, empty: !docs.length, metadata: { fromCache: false, hasPendingWrites: false }, docChanges: function () { return []; } });
          }, err);
        }
      };
    }
  };
  var assets = {
    upload: function (file) { var fd = new FormData(); fd.append("file", file, file.name || "upload"); return call("upload", fd, true).then(function (j) { return { id: j.id, url: j.url, sizeBytes: j.size, contentType: j.type }; }); }
  };
  var user = {
    canEdit: function () { return ready().then(function () { return !!me; }); },
    isOwner: function () { return ready().then(function () { return !!me && me.role === "super"; }); },
    id: function () { return ready().then(function () { return me ? "u_" + me.id : "public"; }); },
    me: function () { return ready().then(function () { return me; }); },
    can: function () { return ready().then(function () { return !!me; }); }
  };
  window.claude = { use: function (name) {
    if (name === "db") return ready().then(function () { return db; }, function () { return null; });
    if (name === "user") return ready().then(function () { return user; }, function () { return null; });
    if (name === "assets") return ready().then(function () { return me ? assets : null; }, function () { return null; });
    return Promise.resolve(null);
  } };
  window.TRIZN = {
    login: function (id, pw) { return ready().catch(function () {}).then(function () { return call("login", { id: id, pw: pw }); }); },
    logout: function () { return call("logout", {}); },
    inquiry: function (item) { return ready().then(function () { return call("inquiry", item); }); },
    users: function () { return call("users"); },
    saveUser: function (u) { return call("user_save", u); },
    deleteUser: function (id) { return call("user_delete", { id: id }); },
    changePw: function (cur, nw) { return call("password", { cur: cur, nw: nw }); }
  };
})();
