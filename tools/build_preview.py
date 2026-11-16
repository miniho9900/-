#!/usr/bin/env python3
"""메인 시안(미리보기) 페이지: demo/index.html 에 새 메인 효과(TZ_FX)를 켜서 preview/index.html 로 만듭니다.

    python3 tools/build_server.py && python3 tools/build_demo.py && python3 tools/build_preview.py
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
page = (ROOT / "demo" / "index.html").read_text(encoding="utf-8")
page = page.replace("<title>트리즈엔 관리자 체험판</title>", "<title>트리즈엔 메인 시안</title>", 1)
inj = """<script>window.TZ_FX = true;</script>
<style>.demo-bar{display:none!important}body{padding-bottom:0!important}.pv-badge{position:fixed;left:max(16px,env(safe-area-inset-left,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:300;background:#14131F;color:#fff;font:600 12px/1.4 "Noto Sans KR",system-ui,sans-serif;padding:9px 14px;border-radius:999px;box-shadow:0 10px 24px -10px rgba(0,0,0,.5)}.pv-badge b{color:#B9A8FF;margin-right:6px}</style>
<div class="pv-badge"><b>메인 시안</b>실제 사이트에는 아직 반영되지 않았습니다</div>
"""
(ROOT / "preview").mkdir(exist_ok=True)
(ROOT / "preview" / "index.html").write_text(inj + page, encoding="utf-8")
print("preview/index.html", len(inj + page) // 1024, "KB")
