#!/usr/bin/env python3
"""site/ 의 홈페이지 화면과 콘텐츠를 server/ (PHP 서버 버전)로 묶습니다.

    python3 tools/build_server.py

- site/index.html          → server/index.html (PHP API 연결 코드를 붙여서)
- site/live/<col>/<id>.json → server/data/seed.json (설치할 때 들어가는 기본 콘텐츠)
- site/images/*             → server/uploads/ (콘텐츠가 쓰는 이미지·영상)
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE, OUT = ROOT / "site", ROOT / "server"

# claude.ai 에 올라간 파일 id → 이 저장소의 원본 파일
ASSETS = {
    "07910d1245f365f300978abef5987c92": "biz1.jpg",
    "16ed5483b021c7b2c47ec193ffa36c42": "biz2.jpg",
    "573de8004fd61a36a1df81de91c0ff9b": "biz3.jpg",
    "537eac2d90b7e7d65aea2ff9dbbc4109": "biz4.jpg",
    "74e9271fc9ffa7ebe2ed7219b22c3e73": "biz5.jpg",
    "d6cf3b9f417aef72f41b7530aee89745": "lease_dia.png",
    "af7f54517916e04f333fb96350135912": "control_solution.png",
    "d918a263d2517ab2ffabf65b9cb57dca": "consulting1.jpg",
    "4a31dbaa7e89a4c39a06803bab4af91b": "control1.jpg",
    "be7ab1de59d800edbc546b6ede166574": "hero-video.mp4",
}
new_name = {aid: f"{aid}{Path(src).suffix}" for aid, src in ASSETS.items()}

def remap(v):
    if isinstance(v, str):
        if v in new_name: return new_name[v]
        return re.sub(r"/_blob/([0-9a-f]{32})", lambda m: "uploads/" + new_name.get(m.group(1), m.group(1)), v)
    if isinstance(v, list): return [remap(x) for x in v]
    if isinstance(v, dict): return {k: remap(x) for k, x in v.items()}
    return v

# 1. index.html
body = (SITE / "index.html").read_text(encoding="utf-8")
title = re.search(r"<title>.*?</title>", body, re.S).group(0)
body = body.replace(title, "", 1).replace('<meta name="claude:viewport-fit-sides" content="cover">', "")
head = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{title}
<meta name="description" content="트리즈엔(TrizN) | 네트워크망을 보유하고 있지 않는 세계 최대 네트워크 서비스 플랫폼을 목표로 합니다.">
<meta property="og:title" content="트리즈엔">
<meta property="og:description" content="토탈 네트워크 서비스 · 지능형 SDN 네트워크 솔루션">
<link rel="canonical" href="https://www.trizn.kr/">
<style>[hidden]{{display:none!important}}body{{margin:0}}img{{max-width:100%}}</style>
<script>window.TRIZN_API = "api.php"; window.TRIZN_MEDIA_BASE = "uploads/";</script>
<script src="api-client.js"></script>
</head>
<body>
"""
(OUT / "index.html").write_text(head + body + "\n</body>\n</html>\n", encoding="utf-8")

# 2. static files
for f in ["logo.png", "logo-white.png", "trizro.png", "trizro-white.png"]:
    shutil.copy2(SITE / f, OUT / f)

# 3. media
(OUT / "uploads").mkdir(exist_ok=True)
for aid, src in ASSETS.items():
    p = SITE / "images" / src
    if p.exists(): shutil.copy2(p, OUT / "uploads" / new_name[aid])
    else: print("missing media:", src)

# 4. seed content
docs = []
for f in sorted((SITE / "live").glob("*/*.json")):
    col, did = f.parent.name, f.stem
    if col == "inquiries": continue
    docs.append({"path": f"{col}/{did}", "data": remap(json.loads(f.read_text(encoding="utf-8")))})
(OUT / "data").mkdir(exist_ok=True)
(OUT / "data" / "seed.json").write_text(json.dumps(docs, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"server/index.html, {len(docs)} seed documents, {len(ASSETS)} media files")
