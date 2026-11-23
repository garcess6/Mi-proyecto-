"""Render bold cover images (1080x1920) for the About us / How it works / Pilot / Partner videos."""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
F = "../ep04-metodos/assets/fonts"
INK, BLUE, SKY = "#111418", "#1e7fd8", "#dff2fc"

def svg(body, w):
    return f'<svg viewBox="0 0 160 160" width="{w}" height="{w}">{body}</svg>'

TAB = f'<path d="M18 70 V92 A62 24 0 0 0 142 92 V70" fill="{SKY}" stroke="{INK}" stroke-width="8"/><ellipse cx="80" cy="70" rx="62" ry="24" fill="#fff" stroke="{INK}" stroke-width="8"/><line x1="46" y1="70" x2="114" y2="70" stroke="{BLUE}" stroke-width="7" stroke-linecap="round"/>'
CAN = f'<g stroke="{INK}" stroke-width="8" stroke-linejoin="round"><path d="M30 52 L130 52 L130 148 L30 148 Z" fill="{SKY}"/><path d="M58 52 L58 30 L102 30 L102 52" fill="#fff"/></g><text x="80" y="118" text-anchor="middle" font-family="Cap" font-weight="900" font-size="30" fill="{INK}">25 L</text>'
CLOCK = f'<circle cx="80" cy="80" r="62" fill="#fff" stroke="{INK}" stroke-width="9"/><path d="M80 80 V32 M80 80 L112 96" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/><circle cx="80" cy="80" r="7" fill="{INK}"/>'
CHECK = f'<circle cx="80" cy="80" r="62" fill="{BLUE}" stroke="{INK}" stroke-width="8"/><path d="M50 82 L72 104 L112 58" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
BOX = f'<path d="M20 50 L80 22 L140 50 L140 124 L80 150 L20 124 Z" fill="#fff" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/><path d="M20 50 L80 78 L140 50 M80 78 L80 150" fill="none" stroke="{BLUE}" stroke-width="7"/>'
FLASK = f'<g stroke="{INK}" stroke-width="8" fill="#fff" stroke-linejoin="round" stroke-linecap="round"><path d="M60 14 L100 14 M66 14 L66 64 L22 142 L138 142 L94 64 L94 14"/></g><path d="M42 108 L118 108 L132 138 L28 138 Z" fill="{SKY}"/>'
CHART = f'<g stroke="{INK}" stroke-width="7" fill="#fff"><path d="M14 146 H146" stroke-linecap="round"/><rect x="30" y="96" width="24" height="44" stroke="{BLUE}"/><rect x="68" y="66" width="24" height="74"/><rect x="106" y="36" width="24" height="104" stroke="{BLUE}"/></g>'
TRUCK = f'<g stroke="{INK}" stroke-width="6" fill="#fff" stroke-linejoin="round"><rect x="10" y="50" width="86" height="56" rx="6"/><path d="M96 66 H124 L146 88 V106 H96 Z"/><circle cx="38" cy="114" r="13"/><circle cx="118" cy="114" r="13"/></g>'
NGO = f'<path d="M80 140 C80 140 20 106 20 64 a30 30 0 0 1 60 -10 a30 30 0 0 1 60 10 C140 106 80 140 80 140Z" fill="#fff" stroke="{INK}" stroke-width="8"/>'
GOV = f'<g stroke="{INK}" stroke-width="8" fill="#fff" stroke-linejoin="round"><path d="M16 56 L80 22 L144 56 Z"/><path d="M14 140 H146"/></g><path d="M34 66 V126 M64 66 V126 M96 66 V126 M126 66 V126" stroke="{BLUE}" stroke-width="8"/>'
INV = f'<g stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"><path d="M14 140 H146"/></g><path d="M22 116 L58 80 L82 100 L134 46 M106 46 H134 V74" stroke="{BLUE}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
DROP = f'<path d="M80 14 C80 14 38 66 38 96 a42 42 0 0 0 84 0 C122 66 80 14 80 14 Z" fill="#fff" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/><circle cx="80" cy="96" r="18" fill="{BLUE}"/>'
GLASS = (f'<svg viewBox="0 0 160 220" width="300" height="412"><path d="M26 66 L134 66 L124 206 L36 206 Z" fill="{SKY}"/><path d="M26 66 Q53 56 80 66 T134 66" stroke="{BLUE}" stroke-width="6" fill="none"/>'
         f'<g transform="translate(64 130) scale(0.7)"><rect x="-26" y="-13" width="52" height="26" rx="13" fill="#fff" stroke="{INK}" stroke-width="4.5"/><circle cx="-8" cy="-2" r="3" fill="{INK}"/><circle cx="8" cy="3" r="3" fill="{BLUE}"/></g>'
         f'<g transform="translate(100 172) scale(0.6)" stroke="{INK}" stroke-width="4"><circle r="18" fill="#fff"/><circle cx="0" cy="-26" r="5" fill="{BLUE}"/><circle cx="26" cy="0" r="5" fill="{BLUE}"/><circle cx="0" cy="26" r="5" fill="{BLUE}"/><circle cx="-26" cy="0" r="5" fill="{BLUE}"/></g>'
         f'<path d="M18 10 L142 10 L126 210 L34 210 Z" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/></svg>')
LENS = f'<svg viewBox="0 0 300 300" width="300" height="300" style="position:absolute;left:520px;top:1080px"><circle cx="140" cy="140" r="110" fill="{SKY}" fill-opacity="0.35" stroke="{INK}" stroke-width="16"/><line x1="220" y1="220" x2="290" y2="290" stroke="{INK}" stroke-width="24" stroke-linecap="round"/></svg>'

def steps(icons, size=180, arrow=True):
    out = ""
    for k, ic in enumerate(icons):
        out += f'<div style="display:inline-block;text-align:center;vertical-align:top"><div style="font-family:Cap;font-weight:900;font-size:40px;color:#fff;background:{BLUE};width:64px;height:64px;border-radius:32px;line-height:64px;margin:0 auto 10px;border:5px solid {INK}">{k + 1}</div>{svg(ic, size)}</div>'
        if arrow and k < len(icons) - 1:
            out += f'<span style="font-family:Cap;font-weight:900;font-size:60px;color:{BLUE};vertical-align:top;line-height:{size + 150}px;margin:0 4px">›</span>'
    return out

COVERS = [
    ("AquaCore_AboutUs_portada.png", "ABOUT US", "WHO", "WE ARE",
     f'<div style="position:absolute;left:0;right:0;top:1020px;text-align:center">{GLASS}</div>{LENS}',
     "Safe water starts with what you can't see"),
    ("AquaCore_HowItWorks_portada.png", "HOW IT WORKS", "SAFE WATER", "IN 4 STEPS",
     f'<div style="position:absolute;left:0;right:0;top:1060px;text-align:center">{steps([CAN, TAB, CLOCK, CHECK], 170)}</div>',
     "1 tablet · 25 litres · 30 minutes"),
    ("AquaCore_Pilot_portada.png", "PILOT PROGRAM", "HOW A PILOT", "WORKS",
     f'<div style="position:absolute;left:0;right:0;top:1060px;text-align:center">{steps([BOX, FLASK, CHART, TRUCK], 170)}</div>',
     "From a first test to full deployment"),
    ("AquaCore_Partner_portada.png", "PARTNER", "PARTNER", "WITH US",
     f'<div style="position:absolute;left:0;right:0;top:1080px;text-align:center">' + "".join(f'<div style="display:inline-block;margin:0 22px;text-align:center">{svg(ic, 200)}<div style="font-family:Cap;font-weight:900;font-size:36px">{l}</div></div>' for ic, l in [(NGO, "NGOs"), (GOV, "GOVERNMENTS"), (INV, "INVESTORS")]) + '</div>',
     "Safe water, at scale · worldwide"),
]

CSS = f"""@font-face{{font-family:Hand;src:url("{F}/patrick-hand-latin-400-normal.woff2")}}
@font-face{{font-family:Cap;src:url("{F}/nunito-latin-900-normal.woff2");font-weight:900}}
@font-face{{font-family:Cap;src:url("{F}/nunito-latin-800-normal.woff2");font-weight:800}}
body{{margin:0}}.c{{width:1080px;height:1920px;background:#fff;position:relative;overflow:hidden;color:{INK};margin-bottom:10px}}
.top{{position:absolute;left:0;top:0;width:1080px;height:980px;background:{BLUE};border-bottom:10px solid {INK}}}
.pill{{position:absolute;left:0;right:0;top:300px;text-align:center}}.pill span{{display:inline-block;padding:12px 34px;background:#fff;border:6px solid {INK};border-radius:999px;font-family:Cap;font-weight:900;font-size:40px;letter-spacing:.05em}}
.pill b{{color:{BLUE}}}
.t1{{position:absolute;left:0;right:0;top:420px;text-align:center;font-family:Cap;font-weight:900;font-size:150px;line-height:1;color:#fff;-webkit-text-stroke:10px {INK};paint-order:stroke fill}}
.t2{{position:absolute;left:0;right:0;top:610px;text-align:center}}.t2 span{{display:inline-block;transform:rotate(-3deg);background:#fff;border:9px solid {INK};border-radius:28px;padding:10px 44px;font-family:Cap;font-weight:900;font-size:136px;line-height:1.05;color:{BLUE}}}
.sub{{position:absolute;left:40px;right:40px;top:1560px;text-align:center;font-family:Hand;font-size:60px}}
.logo{{position:absolute;left:0;right:0;top:820px;text-align:center}}"""

html = ""
for i, (out, tag, t1, t2, art, sub) in enumerate(COVERS):
    html += (f'<div class="c" id="c{i}"><div class="top"></div><div class="pill"><span>AQUACORE · <b>{tag}</b></span></div>'
             f'<div class="t1" style="font-size:{150 if len(t1) <= 8 else 124}px;top:{420 if len(t1) <= 8 else 440}px">{t1}</div><div class="t2"><span>{t2}</span></div>{art}<div class="sub">{sub}</div></div>')
open(os.path.join(HERE, "_story.html"), "w").write(f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{html}</body></html>")
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});"
      f"await p.goto('file://{HERE}/_story.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);"
      + "".join(f"await (await p.$('#c{i}')).screenshot({{path:'{os.path.join(HERE, c[0])}'}});" for i, c in enumerate(COVERS)) + "await b.close()})()")
subprocess.run(["node", "-e", js], check=True, cwd=HERE)
os.remove(os.path.join(HERE, "_story.html"))
print("ok")
