#!/usr/bin/env python3
"""관리자 체험판(claude.ai 페이지)을 만듭니다: demo/index.html + demo/uploads/*

    python3 tools/build_server.py && python3 tools/build_demo.py

서버 버전과 같은 화면 코드(site/index.html)와 연결 코드(server/api-client.js)에
브라우저 안 가상 서버(demo/demo-server.js)를 붙입니다.
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE, SRV, OUT = ROOT / "site", ROOT / "server", ROOT / "demo"
seed = json.loads((SRV / "data" / "seed.json").read_text(encoding="utf-8"))
txt = json.dumps(seed, ensure_ascii=False).replace("be7ab1de59d800edbc546b6ede166574.mp4", "hero-video-small.mp4")
(OUT / "uploads").mkdir(parents=True, exist_ok=True)
for f in (OUT / "uploads").iterdir():
    if f.name != "hero-video-small.mp4": f.unlink()
for f in (SRV / "uploads").iterdir():
    if f.suffix in (".jpg", ".png", ".webp") and f.name in txt: shutil.copy2(f, OUT / "uploads" / f.name)
shutil.copy2(OUT / "hero-video-small.mp4", OUT / "uploads" / "hero-video-small.mp4")
for f in ["logo.png", "logo-white.png", "trizro.png", "trizro-white.png"]: shutil.copy2(SITE / f, OUT / f)

body = (SITE / "index.html").read_text(encoding="utf-8")
body = re.sub(r"<title>.*?</title>", "", body, count=1, flags=re.S)
safe = lambda s: s.replace("</script", "<\\/script")
page = f"""<title>트리즈엔 관리자 체험판</title>
<style>
.demo-bar{{position:fixed;left:0;right:0;bottom:0;z-index:200;display:flex;flex-wrap:wrap;align-items:center;gap:6px 16px;background:#5230C2;color:#fff;font:13px/1.5 "Noto Sans KR",system-ui,sans-serif;padding:10px max(16px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));box-shadow:0 -8px 24px -12px rgba(0,0,0,.4)}}
.demo-bar b{{background:#fff;color:#5230C2;padding:2px 10px;border-radius:999px;font-size:12px}}
.demo-bar code{{background:rgba(255,255,255,.18);padding:1px 6px;border-radius:4px;font-family:ui-monospace,Menlo,Consolas,monospace}}
.demo-bar .demo-note{{opacity:.8}}
.demo-bar button{{margin-left:auto;border:1px solid rgba(255,255,255,.6);background:none;color:#fff;border-radius:999px;padding:5px 14px;font-size:12px;cursor:pointer}}
.demo-bar button:hover{{background:#fff;color:#5230C2}}
body{{padding-bottom:64px}}
.edit-fab{{bottom:calc(76px + env(safe-area-inset-bottom,0px))!important}}
@media (max-width:760px){{.demo-bar .demo-note{{display:none}}body{{padding-bottom:96px}}}}
</style>
<script>window.TRIZN_API = "api.php"; window.TRIZN_MEDIA_BASE = "uploads/"; window.TRIZN_DEMO_SEED = {safe(txt)};</script>
<script>
{safe((OUT / "demo-server.js").read_text(encoding="utf-8"))}
</script>
<script>
{safe((SRV / "api-client.js").read_text(encoding="utf-8"))}
</script>
"""
(OUT / "index.html").write_text(page + body, encoding="utf-8")
print("demo/index.html", len(page + body) // 1024, "KB;", len(list((OUT / "uploads").iterdir())), "media files")
