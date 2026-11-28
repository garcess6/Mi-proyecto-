#!/usr/bin/env python3
"""Reality Check: 'Is it milk?' (German tap water). Dynamic template + the creators' own voices + SFX."""
import json, os, re, subprocess
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "proj")
CHOL = os.path.join(HERE, "..", "colera", "sp01-colera", "index.html")
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
LINES = [l.strip() for l in open(os.path.join(HERE, "lines.txt")) if l.strip()]
VD = [dur(os.path.join(P, "assets", "vo", f"v{i}.wav")) for i in range(len(LINES))]
GREEN, ORANGE, RED, BLUE = "#2e9e5b", "#e08a1e", "#d64545", "#1e7fd8"
CREDIT = "@inthemixnetwork · TikTok · Aug 2026 (Adin Ross stream)"

SECTIONS = [
    dict(title=["1 ·", "$40M", "raised?"], quote="you have millions for water", who="ADIN ROSS, ON STREAM",
         segs=[(5.65, 7.05, "fr_7.0.jpg")],
         stick=["<b>$40M+</b> in one month", "via <b>WaterAid</b>", "goal: <b>2M</b> people"],
         verdict="✓ TRUE", col=GREEN, src="TeamWater · TikTok Newsroom, Aug 2025", glass=False),
    dict(title=["2 ·", "WATER", "park?"], quote="I'm expecting a water park", who="ADIN ROSS, ON STREAM",
         segs=[(9.68, 11.05, "fr_11.0.jpg")],
         stick=["$1 = <b>1 year</b> of water", "goal: <b>2M</b> people", "for <b>decades</b>"],
         verdict="↻ NOT A PARK", col=ORANGE, src="TeamWater donation page", glass=False),
    dict(title=["3 ·", "HOW MANY", "so far?"], quote="How was the $40M allocated?", who="THE QUESTION",
         segs=[(23.49, 24.95, "fr_24.9.jpg")],
         stick=["<b>~225,000</b> people", "goal: <b>2,000,000</b>", "<b>≈ 11 %</b> after 1 year"],
         verdict="⏳ IN PROGRESS", col=BLUE, src="MrBeast one-year update, via UNILAD Tech (Aug 2026)", glass=False),
    dict(title=["4 ·", "WHAT", "got built?"], quote="Show me what was built.", who="THE QUESTION",
         segs=[(31.2, 32.65, "fr_32.6.jpg")],
         stick=["🇹🇿 <b>75,000 L</b>/day", "🇧🇷 water <b>filters</b>", "🇷🇼 pipes <b>in progress</b>"],
         verdict="✓ REAL PROJECTS", col=GREEN, src="MrBeast one-year update, via UNILAD Tech / Dexerto", glass=False),
]

# ---------- schedule
VO_AT, CLIPS = [], []          # VO start times; (t, a, b) clip audio placements
t = 0.1
CLIPS.append((t, 0.0, 2.47)); HOOK_SEG = (t, 0.0, 2.47)
VO_AT.append(round(t + 2.47 + 0.15, 2))
SHRINK = round(VO_AT[0] + 1.2, 2)
SPLASH = round(VO_AT[0] + VD[0] - 1.3, 2)
T = [0.0]
t = round(VO_AT[0] + VD[0] + 0.35, 2)
SEC = []
for k, s in enumerate(SECTIONS):
    T.append(t); st = t
    a, b, fr = s["segs"][0]
    CLIPS.append((t, a, b)); segs = [(t, a, b, fr)]
    t = round(t + (b - a) + 0.1, 2)
    VO_AT.append(t); vo_t = t
    t = round(t + VD[k + 1] + 0.15, 2)
    for (a2, b2, fr2) in s["segs"][1:]:
        CLIPS.append((t, a2, b2)); segs.append((t, a2, b2, fr2)); t = round(t + (b2 - a2) + 0.1, 2)
    t = round(t + 0.55, 2)
    SEC.append(dict(start=st, end=t, vo=vo_t, segs=segs))
T.append(t); VO_AT.append(round(t + 0.15, 2)); t = round(t + 0.15 + VD[5] + 0.9, 2)
T.append(t); END = round(t + 3.2, 2); T.append(END)

chol = open(CHOL).read()
helpers = chol[chol.index("      function figure("):chol.index("      // cholera bacterium")]
guide = chol[chol.index("      /* ================= GUIDE"):chol.index("      // S0 hook")]
guide = guide.replace("G.fx = nx; G.fy = ny; G.fo = 1;", 'G.fx = nx; G.fy = ny; G.fo = 1; sfx("click", t + 0.36);')
guide = guide.replace("const GW = 130,", "const GW = 140,").replace("const nx = tx - 33, ny = ty + 4;", "const nx = tx - 33, ny = ty + 30;")
caps = chol[chol.index("      /* ================= captions"):chol.index("      if (document.documentElement.dataset.format")]
caps = re.sub(r"      const KEY = .*\n", "", caps)

CW, CH = 400, 722
media = ""
for k, sec in enumerate(SEC, 1):
    media += f'      <div id="card{k}" class="abs cardw" style="opacity:0">\n'
    for j, (ts, a, b, fr) in enumerate(sec["segs"]):
        nxt = sec["segs"][j + 1][0] if j + 1 < len(sec["segs"]) else sec["end"]
        media += f'        <video id="vid{k}_{j}" class="clip fv" src="assets/clip.mp4" data-start="{ts}" data-duration="{round(b - a, 2)}" data-media-start="{a}" muted playsinline></video>\n'
        media += f'        <img id="frz{k}_{j}" class="clip fv" src="assets/{fr}" data-start="{round(ts + b - a, 2)}" data-duration="{round(nxt - ts - (b - a), 2)}" />\n'
    media += '        <div class="cred">' + CREDIT + '</div>\n      </div>\n'

# the lines the creators say, shown as their own captions (white, on dark) during clip playback
THEIR = []
def their_caps(ts, a, b):
    src = [(9.9, 10.9, "no it's just hot"), (10.9, 11.4, "and there's minerals inside"), (11.4, 12.9, "but it's safe to drink"),
           (13.9, 15.4, "see it's clear again, you can try it"), (6.4, 8.0, "I've never drunk tap water before")]
    return []
THEIR_ALL = THEIR + [c for sec in SEC for (ts, a, b, fr) in sec["segs"] for c in their_caps(ts, a, b)]

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait" data-format="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Team Water Audit</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Hand"; src: url("assets/fonts/patrick-hand-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
      @font-face {{ font-family: "Cap"; src: url("assets/fonts/nunito-latin-900-normal.woff2") format("woff2"); font-weight: 900; }}
      @font-face {{ font-family: "Cap"; src: url("assets/fonts/nunito-latin-800-normal.woff2") format("woff2"); font-weight: 800; }}
      :root {{ --ink: #111418; --blue: #1e7fd8; --sky: #dff2fc; --muted: #8b96a3; --red: #d64545; --yel: #ffd34d; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #f6fafe; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Hand", sans-serif; color: var(--ink);
        background-color: #f6fafe; background-image: linear-gradient(#e3eef8 2px, transparent 2px), linear-gradient(90deg, #e3eef8 2px, transparent 2px); background-size: 54px 54px; }}
      .abs {{ position: absolute; }}
      svg {{ overflow: visible; }}
      .fv {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
      .cardw {{ left: 80px; top: 430px; width: {CW}px; height: {CH}px; border: 8px solid var(--ink); border-radius: 26px; overflow: hidden; background: #000; box-shadow: 14px 14px 0 rgba(17,20,24,0.18); }}
      .cred {{ position: absolute; left: 10px; bottom: 10px; font-family: Cap; font-weight: 800; font-size: 20px; color: #fff; background: rgba(0,0,0,0.55); padding: 4px 10px; border-radius: 8px; }}
      .pill {{ white-space: nowrap; display: inline-flex; align-items: center; gap: 14px; padding: 10px 28px; border: 5px solid var(--ink); border-radius: 999px; font-family: "Cap"; font-weight: 900; font-size: 34px; letter-spacing: 0.04em; background: #fff; }}
      .pill b {{ color: var(--blue); }}
      .ttl {{ position: absolute; left: 0; width: 1080px; top: 215px; text-align: center; font-family: Cap; font-weight: 900; font-size: 74px; line-height: 1; white-space: nowrap; }}
      .ttl .hl {{ display: inline-block; background: var(--blue); color: #fff; padding: 2px 18px 8px; border-radius: 14px; border: 5px solid var(--ink); margin: 0 10px; transform: rotate(-2deg); }}
      .ttl span.w {{ display: inline-block; }}
      .sticker {{ display: inline-block; font-family: Cap; font-weight: 800; font-size: 34px; background: #fff; border: 5px solid var(--ink); border-radius: 16px; padding: 10px 18px; box-shadow: 6px 6px 0 rgba(17,20,24,0.15); white-space: nowrap; }}
      .sticker b {{ color: var(--blue); }}
      .quote {{ position: absolute; left: 520px; top: 430px; width: 500px; background: #fff; border: 6px solid var(--ink); border-radius: 22px; padding: 18px 22px; box-shadow: 8px 8px 0 rgba(17,20,24,0.15); }}
      .quote .who {{ font-family: Cap; font-weight: 900; font-size: 22px; color: var(--muted); letter-spacing: 0.06em; }}
      .quote .q {{ font-family: Cap; font-weight: 800; font-size: 36px; line-height: 1.15; margin-top: 6px; }}
      .verdict {{ display: inline-block; font-family: Cap; font-weight: 900; font-size: 54px; color: #fff; border: 7px solid var(--ink); border-radius: 20px; padding: 10px 30px; white-space: nowrap; }}
      .src {{ font-family: Cap; font-weight: 800; font-size: 24px; color: var(--muted); }}
      .their {{ position: absolute; left: 60px; width: 960px; top: 1460px; text-align: center; opacity: 0; }}
      .their span {{ display: inline-block; font-family: Cap; font-weight: 900; font-size: 56px; color: #fff; background: rgba(17,20,24,0.85); padding: 8px 26px; border-radius: 16px; }}
      #caps {{ position: absolute; left: 60px; width: 960px; top: 1440px; height: 200px; }}
      .cap {{ position: absolute; left: 0; right: 0; top: 50%; transform: translateY(-50%); text-align: center; font-family: "Cap"; font-weight: 900; font-size: 68px; line-height: 1.1; color: var(--ink); opacity: 0; }}
      .cap span {{ display: inline-block; margin: 0 0.06em; }}
      .cap span.k {{ color: var(--blue); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" src="assets/mix.wav" data-start="0" data-duration="{END}"></audio>
      <div id="tag" class="abs" style="left:0;top:95px;width:1080px;text-align:center;z-index:3"><div class="pill"><img src="assets/logo-drop.png" style="height:46px;width:auto" />REALITY CHECK · <b>#TEAMWATER</b></div></div>
      <div id="hk" class="abs" style="left:0;top:0;width:1080px;height:1920px;overflow:hidden;z-index:2">
        <video id="hv0" class="clip fv" src="assets/clip.mp4" data-start="{HOOK_SEG[0]}" data-duration="{round(HOOK_SEG[2] - HOOK_SEG[1], 2)}" data-media-start="{HOOK_SEG[1]}" muted playsinline></video>
        <img id="hfz" class="clip fv" src="assets/fr_3.4.jpg" data-start="{round(HOOK_SEG[0] + HOOK_SEG[2] - HOOK_SEG[1], 2)}" data-duration="{round(T[1] - HOOK_SEG[0] - (HOOK_SEG[2] - HOOK_SEG[1]), 2)}" />
        <div id="hkb" style="position:absolute;inset:0;border:22px solid #111418;border-radius:70px;opacity:0"></div>
        <div class="cred" style="font-size:24px;bottom:auto;top:200px;left:30px">Video: {CREDIT}</div>
      </div>
      <div id="hov" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:4"></div>
      <div id="splash" class="clip abs" data-start="{SPLASH}" data-duration="{round(T[1] - SPLASH, 2)}" style="left:0;top:0;width:1080px;height:1920px;z-index:6"></div>
{media}      <div id="ov" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:3"></div>
      <div id="concl" class="clip abs" data-start="{T[5]}" data-duration="{round(T[6] - T[5], 2)}" style="left:0;top:0;width:1080px;height:1920px;z-index:3"></div>
      <div id="endc" class="clip abs" data-start="{T[6]}" data-duration="{round(END - T[6], 2)}" style="left:0;top:0;width:1080px;height:1920px;background:#fff;z-index:7"></div>
      <div id="guideLayer" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:8"></div>
      <div id="theirs" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:9"></div>
      <div id="capbg" class="abs" style="left:40px;top:1440px;width:1000px;height:200px;background:rgba(255,255,255,0.92);border:5px solid #111418;border-radius:28px;z-index:8;opacity:0"></div>
      <div id="caps" style="z-index:9"></div>
    </div>
    <script>
      const INK = "#111418", BLUE = "#1e7fd8", SKY = "#dff2fc", MUTED = "#8b96a3", RED = "{RED}", YEL = "#ffd34d", GREEN = "{GREEN}", ORANGE = "{ORANGE}";
      const LINES = {json.dumps([[s, round(d, 2), l] for s, d, l in zip(VO_AT, VD, LINES)])};
      const T = {json.dumps(T)};
      const SEC = {json.dumps(SEC)};
      const TIMED = LINES.map(([start, dur, text]) => {{
        const words = text.split(" ");
        const wts = words.map((w) => w.replace(/[^\\w']/g, "").length + 3 + (/\\d/.test(w) ? 6 : 0) + (/[.?!…]$/.test(w) ? 7 : /[,:]$/.test(w) ? 4 : 0));
        const total = wts.reduce((a, b) => a + b, 0);
        let t = start + 0.1; const span = dur - 0.25;
        return words.map((w, i) => {{ const d = (wts[i] / total) * span; const o = {{ w, t, d }}; t += d; return o; }});
      }});
      const W = (li, word, nth = 0) => {{ const m = TIMED[li].filter((x) => x.w.toLowerCase().replace(/[^\\w']/g, "") === word.toLowerCase()); return (m[nth] || m[0]).t; }};
{helpers}
      const tl = gsap.timeline({{ paused: true }});
      const SFX = []; window.__sfx = SFX; const sfx = (k, t) => SFX.push([k, Math.max(0, +(+t).toFixed(3))]);
      const pop = (sel, t, extra = {{}}) => sfx("pop", t) && tl.fromTo(sel, {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.32, ease: "back.out(2.4)", ...extra }}, t);
      const slam = (sel, t, rot = -4) => sfx("thud", t + 0.12) && tl.fromTo(sel, {{ scale: 2.2, opacity: 0, rotation: rot }}, {{ scale: 1, opacity: 1, rotation: rot, duration: 0.26, ease: "back.out(2.2)" }}, t);
      const add = (id, html) => document.getElementById(id).insertAdjacentHTML("beforeend", html);
      const out = (sel, t) => tl.to(sel, {{ opacity: 0, scale: 0.9, duration: 0.14 }}, t);
      const title = (id, [a, h, b], top = 215) => `<div id="${{id}}" class="ttl" style="top:${{top}}px"><span class="w">${{a}}</span><span class="hl">${{h}}</span><span class="w">${{b}}</span></div>`;
      const titleIn = (id, t) => {{ sfx("whoosh", t - 0.05); tl.fromTo(`#${{id}} .w, #${{id}} .hl`, {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.22, stagger: 0.08, ease: "back.out(2)" }}, t); tl.fromTo(`#${{id}} .hl`, {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.25, ease: "power3.out" }}, t + 0.08); }};
      const CL = {json.dumps([[s["title"], s["quote"], s["stick"], s["verdict"], s["col"], s["src"], s["glass"], s["who"]] for s in SECTIONS], ensure_ascii=False)};

      /* their own words, as captions while their clip plays */
      {json.dumps(THEIR_ALL)}.forEach(([a, b, txt], n) => {{
        add("theirs", `<div id="th${{n}}" class="their"><span>“${{txt}}”</span></div>`);
        tl.fromTo(`#th${{n}}`, {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.1 }}, a); tl.set(`#th${{n}}`, {{ opacity: 0 }}, b);
      }});

      /* ================= HOOK ================= */
      add("hov", `<div id="hs" class="abs" style="left:0;top:820px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{RED}};font-size:96px">AUDIT? 🧐</span></div>`);
      add("hov", title("ht", ["", "$40M", "where did it go?"]));
      add("hov", `<div id="hl" class="abs" style="left:540px;top:520px;opacity:0"><span class="sticker" style="font-size:44px">💧 <b id="hvn">$0</b></span></div>
        <div id="hv" class="abs" style="left:540px;top:640px;opacity:0"><span class="sticker" style="font-size:40px;background:${{YEL}}">🎯 <b>2M</b> people goal</span></div>
        <div id="hq" class="abs" style="left:540px;top:780px;width:470px;opacity:0"><div class="quote" style="position:relative;left:0;top:0;width:470px"><div class="who">ADIN ROSS, ON STREAM</div><div class="q">“I'm expecting a water park, you have millions for water.”</div></div></div>`);
      tl.set("#ht .w, #ht .hl", {{ opacity: 0 }}, 0);
      tl.fromTo("#hk", {{ scale: 1.0 }}, {{ scale: 1.06, duration: 1.4, ease: "none", transformOrigin: "50% 40%" }}, 0);
      slam("#hs", 0.7, -4);
      tl.to("#hs", {{ opacity: 0, scale: 0.6, duration: 0.2 }}, {SHRINK} - 0.1);
      sfx("whoosh", {SHRINK});
      tl.fromTo("#hk", {{ x: 0, y: 0, scaleX: 1.06, scaleY: 1.06, rotation: 0, borderRadius: 0, transformOrigin: "0% 0%" }}, {{ x: 80, y: 430, scaleX: {CW} / 1080, scaleY: {CH} / 1920, rotation: -4, borderRadius: 70, duration: 0.55, ease: "power3.inOut" }}, {SHRINK});
      tl.fromTo("#hkb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {SHRINK} + 0.2);
      titleIn("ht", {SHRINK} + 0.3);
      const tLikes = W(0, "forty") - 0.2;
      sfx("pop", tLikes); sfx("pop", tLikes + 0.9);
      tl.fromTo("#hl", {{ x: 300, opacity: 0, rotation: 6 }}, {{ x: 0, opacity: 1, rotation: 3, duration: 0.3, ease: "back.out(2)" }}, tLikes);
      tl.fromTo("#hv", {{ x: 300, opacity: 0, rotation: -6 }}, {{ x: 0, opacity: 1, rotation: -3, duration: 0.3, ease: "back.out(2)" }}, tLikes + 0.9);
      {{ const o = {{ v: 0 }}; tl.to(o, {{ v: 40, duration: 0.9, ease: "power2.out", onUpdate: () => {{ document.getElementById("hvn").textContent = "$" + Math.round(o.v) + ",000,000"; }} }}, tLikes); }}
      pop("#hq", tLikes + 1.0, {{ rotation: 2 }});
      tl.set("#hk", {{ opacity: 1 }}, 0); tl.set("#hk", {{ opacity: 0 }}, {SPLASH});
      tl.set("#capbg", {{ opacity: 1 }}, {VO_AT[0]} - 0.05); tl.to("#capbg", {{ opacity: 0, duration: 0.2 }}, {SHRINK} + 0.4); tl.set("#hov", {{ opacity: 1 }}, 0); tl.set("#hov", {{ opacity: 0 }}, {SPLASH} + 0.2);

      /* ================= SPLASH ================= */
      let rays = ""; for (let k = 0; k < 16; k++) rays += `<path d="M540 900 L${{540 + Math.cos((k * 2 * Math.PI) / 16 - 0.1) * 1400}} ${{900 + Math.sin((k * 2 * Math.PI) / 16 - 0.1) * 1400}} L${{540 + Math.cos((k * 2 * Math.PI) / 16 + 0.1) * 1400}} ${{900 + Math.sin((k * 2 * Math.PI) / 16 + 0.1) * 1400}} Z" fill="${{k % 2 ? "#cfe6fa" : "#e9f4fd"}}"/>`;
      add("splash", `<div class="abs" style="left:0;top:0;width:1080px;height:1920px;background:#f6fafe"></div><svg id="rays" class="abs" style="left:0;top:0" width="1080" height="1920">${{rays}}</svg>
        <div id="sp1" class="abs" style="left:290px;top:650px;width:500px;height:500px;border-radius:250px;background:#fff;border:12px solid ${{INK}};display:flex;flex-direction:column;align-items:center;justify-content:center">
          <img src="assets/logo-drop.png" style="height:150px;width:auto" />
          <div style="font-family:Cap;font-weight:900;font-size:64px;line-height:1;margin-top:10px">REALITY</div>
          <div style="font-family:Cap;font-weight:900;font-size:64px;line-height:1;color:#fff;background:${{BLUE}};padding:4px 22px;border-radius:14px;border:5px solid ${{INK}};margin-top:6px;transform:rotate(-3deg)">CHECK</div></div>
        <div id="sp2" class="abs" style="left:0;top:1200px;width:1080px;text-align:center"><span class="sticker" style="font-size:46px">4 questions · <b>the data decides</b></span></div>`);
      sfx("whoosh", {SPLASH} - 0.1); sfx("ding", {SPLASH} + 0.12);
      tl.fromTo("#rays", {{ rotation: 0, opacity: 0 }}, {{ rotation: 25, opacity: 1, duration: T[1] - {SPLASH}, ease: "none", svgOrigin: "540 900" }}, {SPLASH});
      tl.fromTo("#sp1", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.2)" }}, {SPLASH} + 0.05);
      tl.fromTo("#sp2", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25 }}, {SPLASH} + 0.35);

      /* ================= SECTIONS ================= */
      CL.forEach(([ttl, quote, stick, verdict, vcol, srcT, hasGlass, who], k) => {{
        const i = k + 1, S = SEC[k], ts = S.start, te = S.end, vo = S.vo, voEnd = vo + LINES[i][1];
        add("ov", title("tt" + i, ttl));
        add("ov", `<div id="q${{i}}" class="quote" style="opacity:0"><div class="who">${{who}}</div><div class="q">“${{quote}}”</div></div>`);
        const top0 = hasGlass ? 900 : 720;
        add("ov", stick.map((s, j) => `<div id="s${{i}}_${{j}}" class="abs" style="left:${{530 + (j % 2) * 20}}px;top:${{top0 + j * 104}}px;opacity:0"><span class="sticker">${{s}}</span></div>`).join(""));
        if (hasGlass) {{
          let bub = ""; for (let b = 0; b < 14; b++) bub += `<circle class="bb${{i}}" cx="${{40 + ((b * 37) % 80)}}" cy="${{200 - ((b * 53) % 120)}}" r="${{3 + (b % 3)}}" fill="#fff" stroke="${{MUTED}}" stroke-width="1.5"/>`;
          add("ov", `<svg id="gl${{i}}" class="abs" style="left:640px;top:600px;opacity:0" width="200" height="275" viewBox="0 0 160 220"><path d="M26 30 L134 30 L124 206 L36 206 Z" fill="${{SKY}}"/><rect id="milk${{i}}" x="20" y="30" width="120" height="178" fill="#ffffff" opacity="0.92"/>${{bub}}<path d="M18 10 L142 10 L126 210 L34 210 Z" fill="none" stroke="${{INK}}" stroke-width="8" stroke-linejoin="round"/></svg>`);
        }}
        add("ov", `<div id="v${{i}}" class="abs" style="left:0;top:1215px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{vcol}}">${{verdict}}</span></div>`);
        if (srcT) add("ov", `<div id="src${{i}}" class="abs src" style="left:0;top:1338px;width:1080px;text-align:center;opacity:0">Source: ${{srcT}}</div>`);
        tl.set(`#tt${{i}} .w, #tt${{i}} .hl`, {{ opacity: 0 }}, 0);
        titleIn("tt" + i, ts + 0.02);
        tl.set(`#card${{i}}`, {{ opacity: 0 }}, 0); tl.set(`#card${{i}}`, {{ opacity: 1 }}, ts); tl.set(`#card${{i}}`, {{ opacity: 0 }}, te);
        sfx("whoosh", ts); sfx("whoosh", te - 0.25);
        tl.fromTo(`#card${{i}}`, {{ x: -560, rotation: -14 }}, {{ x: 0, rotation: k % 2 ? 3 : -3, duration: 0.42, ease: "back.out(1.6)" }}, ts);
        pop(`#q${{i}}`, ts + 0.3, {{ rotation: k % 2 ? -2 : 2 }});
        const span = Math.max(1.4, voEnd - vo - 1.2);
        stick.forEach((s, j) => sfx("pop", vo + 0.9 + (j * span) / stick.length));
        stick.forEach((s, j) => tl.fromTo(`#s${{i}}_${{j}}`, {{ x: 220, opacity: 0, rotation: 8 }}, {{ x: 0, opacity: 1, rotation: j % 2 ? 2 : -2, duration: 0.28, ease: "back.out(2.2)" }}, vo + 0.9 + (j * span) / stick.length));
        if (hasGlass) {{
          pop(`#gl${{i}}`, vo + 0.6);
          tl.fromTo(`#milk${{i}}`, {{ attr: {{ height: 178 }} }}, {{ attr: {{ height: 0 }}, duration: 2.6, ease: "power1.inOut" }}, vo + 1.5);
          tl.fromTo(`.bb${{i}}`, {{ y: 0, opacity: 1 }}, {{ y: -170, opacity: 0, duration: 1.6, stagger: 0.08, ease: "power1.in" }}, vo + 1.2);
        }}
        tl.to(`#card${{i}}`, {{ scale: 0.92, y: -10, duration: 0.3, ease: "power2.out" }}, vo);
        tl.to(`#card${{i}}`, {{ scale: 1, y: 0, duration: 0.3, ease: "power2.out" }}, voEnd + 0.1);
        slam(`#v${{i}}`, Math.min(te - 1.0, voEnd - 0.6), k % 2 ? 3 : -3);
        if (srcT) tl.to(`#src${{i}}`, {{ opacity: 1, duration: 0.2 }}, Math.min(te - 0.8, voEnd - 0.4));
        out([`#tt${{i}}`, `#q${{i}}`, ...stick.map((s, j) => `#s${{i}}_${{j}}`), `#v${{i}}`, ...(srcT ? [`#src${{i}}`] : []), ...(hasGlass ? [`#gl${{i}}`] : [])], te - 0.14);
        tl.to(`#card${{i}}`, {{ x: 900, rotation: 16, duration: 0.2, ease: "power2.in" }}, te - 0.2);
      }});

      /* ================= SCORE ================= */
      add("concl", title("tc", ["THE", "SCORE", ""]));
      const SC = [["Money raised", "✓", GREEN], ["Water park", "↻", ORANGE], ["2M people reached", "⏳", BLUE], ["Projects built", "✓", GREEN], ["Independent audit", "?", RED]];
      add("concl", SC.map(([n, ic, c], j) => `<div id="sc${{j}}" class="abs" style="left:110px;top:${{380 + j * 120}}px;width:860px;height:100px;background:#fff;border:6px solid ${{INK}};border-radius:20px;display:flex;align-items:center;gap:24px;padding:0 24px;opacity:0">
        <div style="width:60px;height:60px;border-radius:30px;background:${{c}};color:#fff;font-family:Cap;font-weight:900;font-size:38px;display:flex;align-items:center;justify-content:center;border:4px solid ${{INK}}">${{ic}}</div>
        <div style="font-family:Cap;font-weight:800;font-size:40px">${{n}}</div></div>`).join(""));
      add("concl", `<div id="ca" class="abs" style="left:0;top:1020px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{GREEN}};font-size:44px">REAL MONEY ✓ REAL PROJECTS ✓</span></div>
        <div id="cw" class="abs" style="left:0;top:1150px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{BLUE}};font-size:42px">MOST IMPACT: STILL TO COME ⏳</span></div>
        <div id="ctip" class="abs" style="left:0;top:1280px;width:1080px;text-align:center;opacity:0"><span class="sticker" style="font-size:36px">📄 Public audit = <b>debate over</b></span></div>`);
      tl.set("#tc .w, #tc .hl", {{ opacity: 0 }}, 0);
      titleIn("tc", T[5] + 0.02);
      SC.forEach((x, j) => sfx("pop", T[5] + 0.15 + j * 0.18));
      SC.forEach((x, j) => tl.fromTo(`#sc${{j}}`, {{ x: -700, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.26, ease: "back.out(1.8)" }}, T[5] + 0.15 + j * 0.18));
      slam("#ca", W(5, "real") - 0.1, -3);
      slam("#cw", W(5, "impact") - 0.1, 2);
      pop("#ctip", W(5, "audit") - 0.1, {{ rotation: -2 }});

      /* ================= END CARD ================= */
      add("endc", `<div class="abs" style="left:0;top:330px;width:1080px;text-align:center">
        <img id="logo" src="assets/logo-horizontal.png" style="width:760px;height:auto" />
        <div id="e1" style="font-family:Cap;font-weight:900;font-size:56px;margin-top:40px">REALITY CHECK: <span style="color:${{BLUE}}">#TEAMWATER</span></div>
        <div id="e2" style="font-family:Cap;font-weight:800;font-size:40px;color:${{MUTED}};margin-top:8px">aquacoreglobal.com</div>
        <div id="e3" style="display:inline-block;margin-top:46px;padding:22px 42px;border:7px solid ${{INK}};border-radius:40px;font-family:Hand;font-size:56px">Should <span style="color:${{BLUE}}">#TeamWater</span> publish a full audit? 💬</div>
        <div id="e4" style="font-family:Cap;font-weight:800;font-size:23px;color:${{MUTED}};margin-top:40px;padding:0 40px">Original video: {CREDIT} · Sources: TeamWater · TikTok Newsroom (Aug 2025) · MrBeast one-year update via UNILAD Tech &amp; Dexerto (Aug 2026)</div></div>`);
      pop("#logo", T[6] + 0.05); sfx("ding", T[6] + 0.1);
      tl.fromTo("#e1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, T[6] + 0.25);
      tl.fromTo("#e2", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, T[6] + 0.4);
      pop("#e3", T[6] + 0.6);

{guide}
      const GX = 910, GY = 1130;
      gAt(GX, GY, 0, "o"); gTalk(0);
      gPoint(540, 960, 0.75);
      gPoint(760, 600, W(0, "forty"));
      CL.forEach((c, k) => {{
        const i = k + 1, S = SEC[k], voEnd = S.vo + LINES[i][1];
        gAt(GX, GY, S.start, k === 1 ? "smile" : "hmm"); gTalk(i);
        gPoint(280, 1150, S.start + 0.3);
        if (c[6]) gPoint(740, 900, S.vo + 1.6);
        gPoint(540, 1300, Math.min(S.end - 1.0, voEnd - 0.6) + 0.2);
      }});
      gAt(GX, GY, T[5], "smile"); gTalk(5);
      gPoint(420, 1110, W(5, "real"));
      gPoint(420, 1235, W(5, "impact"));
      gHideFinger(T[6] - 0.15);
      gAt(470, 1450, T[6], "smile");
      tl.fromTo("#guide .armR", {{ rotation: 0 }}, {{ rotation: -150, svgOrigin: "100 150", duration: 0.3 }}, T[6] + 0.2);
      tl.fromTo("#guide .armR", {{ rotation: -150 }}, {{ rotation: -110, svgOrigin: "100 150", duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, T[6] + 0.5);
      tl.set("#caps", {{ opacity: 1 }}, 0); tl.set("#caps", {{ opacity: 0 }}, T[6]);
      tl.set("#guideLayer", {{ opacity: 1 }}, 0); tl.set("#guideLayer", {{ opacity: 0 }}, {SPLASH}); tl.set("#guideLayer", {{ opacity: 1 }}, T[1]);

      const KEY = /^(audit|forty|million|dollars|numbers|true|wateraid|park|two|decades|twentyfive|thousand|eleven|percent|tanzania|brazil|rwanda|construction|real|projects|impact|independent|debate)$/i;
{caps}
      tl.set({{}}, {{}}, {END});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(os.path.join(P, "index.html"), "w").write(html)
json.dump({"id": "reality-teamwater-1", "name": "reality-teamwater-1"}, open(os.path.join(P, "meta.json"), "w"))

# ---------- audio: our VO + their clip audio + SFX
js = os.path.join(HERE, "sfx_events.js")
open(js, "w").write("""const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + process.argv[2]); await p.waitForTimeout(800);
console.log(JSON.stringify(await p.evaluate(() => window.__sfx))); await b.close(); })();""")
ev = json.loads(subprocess.check_output(["node", js, os.path.join(P, "index.html")], cwd=HERE).decode().strip().splitlines()[-1])
ev.sort(key=lambda e: e[1])
keep, last = [], {}
for k, tt in ev:
    if tt - last.get(k, -9) >= 0.09 and tt < END - 0.2:
        keep.append((k, tt)); last[k] = tt
VOL = {"click": 0.5, "pop": 0.3, "whoosh": 0.26, "thud": 0.5, "ding": 0.32}
inp, flt, mix, n = [], "", "", 0
for i, s in enumerate(VO_AT):
    inp += ["-i", os.path.join(P, "assets", "vo", f"v{i}.wav")]; ms = int(s * 1000)
    flt += f"[{n}:a]aresample=44100,adelay={ms}|{ms}[a{n}];"; mix += f"[a{n}]"; n += 1
for (tt, a, b) in CLIPS:
    inp += ["-i", os.path.join(P, "assets", "clipaudio.wav")]; ms = int(tt * 1000)
    flt += f"[{n}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={round(b - a - 0.08, 2)}:d=0.08,volume=1.0,adelay={ms}|{ms}[a{n}];"; mix += f"[a{n}]"; n += 1
for (k, tt) in keep:
    inp += ["-i", os.path.join(P, "assets", "sfx", f"{k}.wav")]; ms = int(tt * 1000)
    flt += f"[{n}:a]aresample=44100,volume={VOL[k]},adelay={ms}|{ms}[a{n}];"; mix += f"[a{n}]"; n += 1
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", f"{flt}{mix}amix=inputs={n}:normalize=0,alimiter=limit=0.95,apad=whole_dur={END}[o]",
                "-map", "[o]", "-ar", "44100", "-ac", "1", os.path.join(P, "assets", "mix.wav")], check=True)
print("END", END, "T", T, "SPLASH", SPLASH, "sfx", dict(Counter(k for k, _ in keep)))
