"""Render cover images (1080x1920) for the country videos."""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
F = "../ep04-metodos/assets/fonts"
COVERS = [
    ("AquaCore_DRCongo_EN_portada.png", "../pais-cod/assets/map.json", "COUNTRY FOCUS · <b>DR CONGO</b>", "70 MILLION", "people without basic drinking water", "What can be done? ▶"),
    ("AquaCore_DRCongo_FR_portada.png", "../pais-cod/assets/map.json", "FOCUS PAYS · <b>RD CONGO</b>", "70 MILLIONS", "de personnes sans eau potable de base", "Quelles solutions ? ▶"),
    ("AquaCore_Nigeria_EN_portada.png", "../pais-nga/assets/map.json", "COUNTRY FOCUS · <b>NIGERIA</b>", "163 MILLION", "Nigerians without safe water at home", "Meet Amina ▶"),
    ("AquaCore_Ethiopia_EN_portada.png", "../pais-eth/assets/map.json", "COUNTRY FOCUS · <b>ETHIOPIA</b>", "59 MILLION", "people without basic drinking water", "What can be done? ▶"),
]
CSS = f"""@font-face{{font-family:Hand;src:url("{F}/patrick-hand-latin-400-normal.woff2")}}
@font-face{{font-family:Cap;src:url("{F}/nunito-latin-900-normal.woff2");font-weight:900}}
@font-face{{font-family:Cap;src:url("{F}/nunito-latin-800-normal.woff2");font-weight:800}}
body{{margin:0}}.c{{width:1080px;height:1920px;background:#fff;position:relative;overflow:hidden;color:#111418;margin-bottom:10px}}
.pill{{position:absolute;left:0;right:0;top:300px;text-align:center}}.pill span{{display:inline-block;padding:12px 32px;border:5px solid #111418;border-radius:999px;font-family:Cap;font-weight:900;font-size:38px;letter-spacing:.04em}}
.pill b{{color:#1e7fd8}}
.map{{position:absolute;left:0;right:0;top:400px;text-align:center}}
.num{{position:absolute;left:0;right:0;top:1040px;text-align:center;font-family:Cap;font-weight:900;font-size:150px;line-height:1}}
.sub{{position:absolute;left:60px;right:60px;top:1210px;text-align:center;font-family:Hand;font-size:64px;line-height:1.05}}
.cta{{position:absolute;left:0;right:0;top:1360px;text-align:center}}.cta span{{display:inline-block;padding:14px 40px;border:6px solid #111418;border-radius:22px;background:#1e7fd8;color:#fff;font-family:Cap;font-weight:900;font-size:52px}}"""
html = ""
for i, (out, mp, tag, num, sub, cta) in enumerate(COVERS):
    m = json.load(open(os.path.join(HERE, mp)))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#111418"/>' for k, (x, y) in enumerate(m["pts"]) if k % 3 == 0)
    svg = f'<svg viewBox="0 0 {m["w"]} {m["h"]}" width="600" height="600"><path d="{m["d"]}" fill="#dff2fc" stroke="#111418" stroke-width="7" stroke-linejoin="round"/>{dots}</svg>'
    html += f'<div class="c" id="c{i}"><div class="pill"><span>{tag}</span></div><div class="map">{svg}</div><div class="num">{num}</div><div class="sub">{sub}</div><div class="cta"><span>{cta}</span></div></div>'
open(os.path.join(HERE, "_country.html"), "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{html}</body></html>")
js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://" + HERE + "/_country.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);" + "".join(f"await (await p.$('#c{i}')).screenshot({{path:'{os.path.join(HERE, c[0])}'}});" for i, c in enumerate(COVERS)) + "await b.close()})()"
subprocess.run(["node", "-e", js], check=True, cwd=HERE)
os.remove(os.path.join(HERE, "_country.html"))
print("ok")
