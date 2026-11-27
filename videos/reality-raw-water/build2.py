#!/usr/bin/env python3
"""Reality Check: raw water, dynamic version.
The clip opens full screen, shrinks into a moving card, a branded splash, numbered sections with
quote cards, data stickers and verdicts, a scoreboard and the end card. Output: proj2/index.html."""
import json, os, re, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "proj")
P = os.path.join(HERE, "proj2")
os.makedirs(P, exist_ok=True)
for f in ("hyperframes.json", "package.json"):
    shutil.copy(os.path.join(SRC, f), P)
if not os.path.isdir(os.path.join(P, "assets")):
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(P, "assets"))
CHOL = os.path.join(HERE, "..", "colera", "sp01-colera", "index.html")
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
LINES = [l.strip() for l in open(os.path.join(HERE, "lines.txt")) if l.strip()]
VD = [dur(os.path.join(P, "assets", "vo", f"v{i}.wav")) for i in range(len(LINES))]

# clip in/out, freeze, title [pre, highlight, post], quote, stickers, verdict, verdict colour, source
CLAIMS = [
    (0.45, 2.2, "fr_2.15.jpg", ["1 ·", "“AGING”", "water"], "Most water is aging you.",
     ["Source he gives: <b>none</b>", "Scientific evidence: <b>none</b>"], "✗ NO EVIDENCE", "#d64545", ""),
    (2.2, 3.4, "fr_3.35.jpg", ["2 ·", "CHLORINE", "&amp; fluoride"], "Tap water has chlorine and fluoride.",
     ["Chlorine limit: <b>≤ 4 mg/L</b>", "Fluoride limit: <b>≤ 4 mg/L</b>", "Chlorine kills germs in the pipes <b>✓</b>"], "⚖ TINY &amp; REGULATED", "#e08a1e", "US EPA drinking-water standards"),
    (3.4, 6.7, "fr_6.6.jpg", ["3 ·", "“JUST A", "spring”"], "No treatment plant, just a spring.",
     ["Montana · <b>2022</b>", "<b>19</b> people sick", "Bug: <b>Campylobacter</b>", "Spot used for <b>decades</b>"], "⚠ RISKY", "#d64545", "CDC MMWR, April 2023"),
    (8.9, 11.4, "fr_11.35.jpg", ["4 ·", "“TASTE”", "test"], "You can taste the difference.",
     ["👅 taste <b>✗</b>", "👃 smell <b>✗</b>", "👁 colour <b>✗</b>", "🧪 lab test <b>✓</b>"], "✗ TASTE ≠ SAFE", "#d64545", ""),
    (11.4, 13.4, "fr_13.35.jpg", ["5 ·", "PLAN", "B"], "If it doesn't deliver near you, get Icelandic or Gerolsteiner.",
     ["Bottled mineral water", "tested <b>✓</b>", "regulated <b>✓</b>", "raw <b>✗</b>"], "↻ PLOT TWIST", "#1e7fd8", ""),
]

# ---------- timeline (same voice lines as v1)
T, starts = [], []
t = 0.0
T.append(t); starts.append(0.2); t = round(0.2 + VD[0] + 0.35, 2)
SPLASH = (round(0.2 + VD[0] - 1.25, 2))                                       # splash on "Let's check the facts"
for i, (a, b, *_r) in enumerate(CLAIMS, 1):
    T.append(t); starts.append(round(t + 0.15, 2))
    t = round(t + max(b - a + 0.3, VD[i] + 0.55), 2)
T.append(t); starts.append(round(t + 0.15, 2)); t = round(t + VD[6] + 0.9, 2)
T.append(t); END = round(t + 3.2, 2); T.append(END)

inp, flt, mix = [], "", ""
for i, s in enumerate(starts):
    inp += ["-i", os.path.join(P, "assets", "vo", f"v{i}.wav")]
    ms = int(s * 1000); flt += f"[{i}:a]adelay={ms}|{ms}[a{i}];"; mix += f"[a{i}]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", f"{flt}{mix}amix=inputs={len(starts)}:normalize=0,apad=whole_dur={END}[o]",
                "-map", "[o]", "-ar", "24000", "-ac", "1", os.path.join(P, "assets", "voice.wav")], check=True)

chol = open(CHOL).read()
helpers = chol[chol.index("      function figure("):chol.index("      // cholera bacterium")]
guide = chol[chol.index("      /* ================= GUIDE"):chol.index("      // S0 hook")]
guide = guide.replace("const GW = 130,", "const GW = 140,").replace("const nx = tx - 33, ny = ty + 4;", "const nx = tx - 33, ny = ty + 30;")
caps = chol[chol.index("      /* ================= captions"):chol.index("      if (document.documentElement.dataset.format")]
caps = re.sub(r"      const KEY = .*\n", "", caps)

CW, CH = 400, 722  # clip card size

media = ""
for i, (a, b, fr, *_r) in enumerate(CLAIMS, 1):
    ts, d = T[i], round(b - a, 2)
    media += f'''      <div id="card{i}" class="abs cardw" style="opacity:0">
        <video id="vid{i}" class="clip fv" src="assets/clip.mp4" data-start="{ts}" data-duration="{d}" data-media-start="{a}" muted playsinline></video>
        <img id="frz{i}" class="clip fv" src="assets/{fr}" data-start="{round(ts + d, 2)}" data-duration="{round(T[i + 1] - ts - d, 2)}" />
        <div class="cred">@erikharding.health</div>
      </div>
'''

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait" data-format="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Raw Water Check</title>
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
      .verdict {{ display: inline-block; font-family: Cap; font-weight: 900; font-size: 64px; color: #fff; border: 7px solid var(--ink); border-radius: 20px; padding: 10px 34px; white-space: nowrap; }}
      .src {{ font-family: Cap; font-weight: 800; font-size: 24px; color: var(--muted); }}
      #caps {{ position: absolute; left: 60px; width: 960px; top: 1440px; height: 200px; }}
      .cap {{ position: absolute; left: 0; right: 0; top: 50%; transform: translateY(-50%); text-align: center; font-family: "Cap"; font-weight: 900; font-size: 68px; line-height: 1.1; color: var(--ink); opacity: 0; }}
      .cap span {{ display: inline-block; margin: 0 0.06em; }}
      .cap span.k {{ color: var(--blue); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{END}"></audio>
      <div id="tag" class="abs" style="left:0;top:95px;width:1080px;text-align:center;z-index:3"><div class="pill"><img src="assets/logo-drop.png" style="height:46px;width:auto" />REALITY CHECK · <b>RAW WATER</b></div></div>
      <div id="hk" class="clip abs" data-start="0" data-duration="{T[1]}" style="left:0;top:0;width:1080px;height:1920px;overflow:hidden;border:0 solid #111418;border-radius:0;z-index:2">
        <img class="fv" src="assets/fr_14.0.jpg" />
        <div id="hkb" style="position:absolute;inset:0;border:22px solid #111418;border-radius:70px;opacity:0"></div>
        <div class="cred" style="font-size:24px;bottom:auto;top:200px;left:30px">Video: @erikharding.health · TikTok · Jul 2026</div>
      </div>
      <div id="hov" class="clip abs" data-start="0" data-duration="{T[1]}" style="left:0;top:0;width:1080px;height:1920px;z-index:4"></div>
      <div id="splash" class="clip abs" data-start="{SPLASH}" data-duration="{round(T[1] - SPLASH, 2)}" style="left:0;top:0;width:1080px;height:1920px;z-index:6"></div>
{media}      <div id="ov" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:3"></div>
      <div id="concl" class="clip abs" data-start="{T[6]}" data-duration="{round(T[7] - T[6], 2)}" style="left:0;top:0;width:1080px;height:1920px;z-index:3"></div>
      <div id="endc" class="clip abs" data-start="{T[7]}" data-duration="{round(END - T[7], 2)}" style="left:0;top:0;width:1080px;height:1920px;background:#fff;z-index:7"></div>
      <div id="guideLayer" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:8"></div>
      <div id="caps" style="z-index:9"></div>
    </div>
    <script>
      const INK = "#111418", BLUE = "#1e7fd8", SKY = "#dff2fc", MUTED = "#8b96a3", RED = "#d64545", YEL = "#ffd34d";
      const LINES = {json.dumps([[s, round(d, 2), l] for s, d, l in zip(starts, VD, LINES)])};
      const T = {json.dumps(T)};
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
      const pop = (sel, t, extra = {{}}) => tl.fromTo(sel, {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.32, ease: "back.out(2.4)", ...extra }}, t);
      const slam = (sel, t, rot = -4) => tl.fromTo(sel, {{ scale: 2.2, opacity: 0, rotation: rot }}, {{ scale: 1, opacity: 1, rotation: rot, duration: 0.26, ease: "back.out(2.2)" }}, t);
      const add = (id, html) => document.getElementById(id).insertAdjacentHTML("beforeend", html);
      const out = (sel, t) => tl.to(sel, {{ opacity: 0, scale: 0.9, duration: 0.14 }}, t);
      const title = (id, [a, h, b], top = 215) => `<div id="${{id}}" class="ttl" style="top:${{top}}px"><span class="w">${{a}}</span><span class="hl">${{h}}</span><span class="w">${{b}}</span></div>`;
      const titleIn = (id, t) => {{ tl.fromTo(`#${{id}} .w, #${{id}} .hl`, {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.22, stagger: 0.08, ease: "back.out(2)" }}, t); tl.fromTo(`#${{id}} .hl`, {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.25, ease: "power3.out" }}, t + 0.08); }};
      const CL = {json.dumps([[c[3], c[4], c[5], c[6], c[7], c[8]] for c in CLAIMS], ensure_ascii=False)};

      /* ================= HOOK: full-screen clip -> card ================= */
      add("hov", `<div id="hs" class="abs" style="left:0;top:820px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{RED}};font-size:96px">LIVE LONGER?</span></div>`);
      add("hov", title("ht", ["", "LIVE", "longer? 🤔"]));
      add("hov", `<div id="hl" class="abs" style="left:540px;top:520px;opacity:0"><span class="sticker" style="font-size:44px">♥ <b>20.6K</b> likes</span></div>
        <div id="hv" class="abs" style="left:540px;top:640px;opacity:0"><span class="sticker" style="font-size:44px;background:${{YEL}}">🔖 <b id="hvn">0</b> saves</span></div>
        <div id="hq" class="abs" style="left:540px;top:780px;width:470px;opacity:0" ><div class="quote" style="position:relative;left:0;top:0;width:470px"><div class="who">@ERIKHARDING.HEALTH SAYS</div><div class="q">“what I drink to live longer than you”</div></div></div>`);
      tl.set("#ht .w, #ht .hl", {{ opacity: 0 }}, 0);
      tl.fromTo("#hk img", {{ scale: 1.0 }}, {{ scale: 1.15, duration: 2.6, ease: "none", transformOrigin: "50% 30%" }}, 0);
      slam("#hs", W(0, "longer") - 0.12, -4);
      const shrink = W(0, "over") - 0.35;
      tl.to("#hs", {{ opacity: 0, scale: 0.6, duration: 0.2 }}, shrink - 0.1);
      tl.fromTo("#hk", {{ x: 0, y: 0, scaleX: 1, scaleY: 1, rotation: 0, borderRadius: 0, transformOrigin: "0% 0%" }}, {{ x: 80, y: 430, scaleX: {CW} / 1080, scaleY: {CH} / 1920, rotation: -4, borderRadius: 70, duration: 0.55, ease: "power3.inOut" }}, shrink);
      tl.fromTo("#hkb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, shrink + 0.2);
      titleIn("ht", shrink + 0.3);
      tl.fromTo("#hl", {{ x: 300, opacity: 0, rotation: 6 }}, {{ x: 0, opacity: 1, rotation: 3, duration: 0.3, ease: "back.out(2)" }}, W(0, "three") - 0.25);
      tl.fromTo("#hv", {{ x: 300, opacity: 0, rotation: -6 }}, {{ x: 0, opacity: 1, rotation: -3, duration: 0.3, ease: "back.out(2)" }}, W(0, "saved") - 0.45);
      {{ const o = {{ v: 0 }}; tl.to(o, {{ v: 3194, duration: 0.9, ease: "power2.out", onUpdate: () => {{ document.getElementById("hvn").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, W(0, "saved") - 0.3); }}
      pop("#hq", W(0, "saved") + 0.15, {{ rotation: 2 }});

      /* ================= SPLASH: branded interstitial ================= */
      let rays = ""; for (let k = 0; k < 16; k++) rays += `<path d="M540 900 L${{540 + Math.cos((k * 2 * Math.PI) / 16 - 0.1) * 1400}} ${{900 + Math.sin((k * 2 * Math.PI) / 16 - 0.1) * 1400}} L${{540 + Math.cos((k * 2 * Math.PI) / 16 + 0.1) * 1400}} ${{900 + Math.sin((k * 2 * Math.PI) / 16 + 0.1) * 1400}} Z" fill="${{k % 2 ? "#cfe6fa" : "#e9f4fd"}}"/>`;
      add("splash", `<div class="abs" style="left:0;top:0;width:1080px;height:1920px;background:#f6fafe"></div><svg id="rays" class="abs" style="left:0;top:0" width="1080" height="1920">${{rays}}</svg>
        <div id="sp1" class="abs" style="left:290px;top:650px;width:500px;height:500px;border-radius:250px;background:#fff;border:12px solid ${{INK}};display:flex;flex-direction:column;align-items:center;justify-content:center">
          <img src="assets/logo-drop.png" style="height:150px;width:auto" />
          <div style="font-family:Cap;font-weight:900;font-size:64px;line-height:1;margin-top:10px">REALITY</div>
          <div style="font-family:Cap;font-weight:900;font-size:64px;line-height:1;color:#fff;background:${{BLUE}};padding:4px 22px;border-radius:14px;border:5px solid ${{INK}};margin-top:6px;transform:rotate(-3deg)">CHECK</div></div>
        <div id="sp2" class="abs" style="left:0;top:1200px;width:1080px;text-align:center"><span class="sticker" style="font-size:46px">5 claims · <b>the data decides</b></span></div>`);
      tl.fromTo("#rays", {{ rotation: 0, opacity: 0 }}, {{ rotation: 25, opacity: 1, duration: T[1] - {SPLASH}, ease: "none", svgOrigin: "540 900" }}, {SPLASH});
      tl.fromTo("#sp1", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.2)" }}, {SPLASH} + 0.05);
      tl.fromTo("#sp2", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25 }}, {SPLASH} + 0.35);

      /* ================= CLAIMS ================= */
      CL.forEach(([ttl, quote, stick, verdict, vcol, srcT], k) => {{
        const i = k + 1, ts = T[i], te = T[i + 1];
        add("ov", title("tt" + i, ttl));
        add("ov", `<div id="q${{i}}" class="quote" style="opacity:0"><div class="who">@ERIKHARDING.HEALTH SAYS</div><div class="q">“${{quote}}”</div></div>`);
        add("ov", stick.map((s, j) => `<div id="s${{i}}_${{j}}" class="abs" style="left:${{530 + (j % 2) * 20}}px;top:${{720 + j * 104}}px;opacity:0"><span class="sticker">${{s}}</span></div>`).join(""));
        add("ov", `<div id="v${{i}}" class="abs" style="left:0;top:1215px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{vcol}}">${{verdict}}</span></div>`);
        if (srcT) add("ov", `<div id="src${{i}}" class="abs src" style="left:0;top:1338px;width:1080px;text-align:center;opacity:0">Source: ${{srcT}}</div>`);
        tl.set(`#tt${{i}} .w, #tt${{i}} .hl`, {{ opacity: 0 }}, 0);
        titleIn("tt" + i, ts + 0.02);
        tl.set(`#card${{i}}`, {{ opacity: 0 }}, 0); tl.set(`#card${{i}}`, {{ opacity: 1 }}, ts); tl.set(`#card${{i}}`, {{ opacity: 0 }}, te);
        // clip card flies in from the left, tilts, plays; then nudges aside when the data lands
        tl.fromTo(`#card${{i}}`, {{ x: -560, rotation: -14 }}, {{ x: 0, rotation: k % 2 ? 3 : -3, duration: 0.42, ease: "back.out(1.6)" }}, ts);
        pop(`#q${{i}}`, ts + 0.3, {{ rotation: k % 2 ? -2 : 2 }});
        const tr = TIMED[i].find((x, j) => j > 0 && /[?]$/.test(TIMED[i][j - 1].w)) || TIMED[i][Math.floor(TIMED[i].length / 3)];
        const span = Math.max(1.2, te - tr.t - 1.3);
        stick.forEach((s, j) => tl.fromTo(`#s${{i}}_${{j}}`, {{ x: 220, opacity: 0, rotation: 8 }}, {{ x: 0, opacity: 1, rotation: j % 2 ? 2 : -2, duration: 0.28, ease: "back.out(2.2)" }}, tr.t + (j * span) / stick.length));
        tl.to(`#card${{i}}`, {{ scale: 0.92, y: -10, duration: 0.3, ease: "power2.out" }}, tr.t);
        slam(`#v${{i}}`, te - 1.15, k % 2 ? 3 : -3);
        if (srcT) tl.to(`#src${{i}}`, {{ opacity: 1, duration: 0.2 }}, te - 0.95);
        out([`#tt${{i}}`, `#q${{i}}`, ...stick.map((s, j) => `#s${{i}}_${{j}}`), `#v${{i}}`, ...(srcT ? [`#src${{i}}`] : [])], te - 0.14);
        tl.to(`#card${{i}}`, {{ x: 900, rotation: 16, duration: 0.2, ease: "power2.in" }}, te - 0.2);
      }});

      /* ================= SCOREBOARD + CONCLUSION ================= */
      add("concl", title("tc", ["THE", "SCORE", ""]));
      const SC = [["“Aging” water", "✗", RED], ["Chlorine &amp; fluoride", "⚖", "#e08a1e"], ["“Just a spring”", "⚠", RED], ["Taste the difference", "✗", RED], ["Plan B: bottled", "↻", BLUE]];
      add("concl", SC.map(([n, ic, c], j) => `<div id="sc${{j}}" class="abs" style="left:110px;top:${{380 + j * 120}}px;width:860px;height:100px;background:#fff;border:6px solid ${{INK}};border-radius:20px;display:flex;align-items:center;gap:24px;padding:0 24px;opacity:0">
        <div style="width:60px;height:60px;border-radius:30px;background:${{c}};color:#fff;font-family:Cap;font-weight:900;font-size:38px;display:flex;align-items:center;justify-content:center;border:4px solid ${{INK}}">${{ic}}</div>
        <div style="font-family:Cap;font-weight:800;font-size:40px">${{n}}</div></div>`).join(""));
      add("concl", `<div id="cr" class="abs" style="left:0;top:1015px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{RED}};text-decoration:line-through">RAW</span></div>
        <div id="ct" class="abs" style="left:0;top:1150px;width:1080px;text-align:center;opacity:0"><span class="verdict" style="background:${{BLUE}}">TESTED ✓ TREATED ✓</span></div>`);
      tl.set("#tc .w, #tc .hl", {{ opacity: 0 }}, 0);
      titleIn("tc", T[6] + 0.02);
      SC.forEach((x, j) => tl.fromTo(`#sc${{j}}`, {{ x: -700, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.26, ease: "back.out(1.8)" }}, T[6] + 0.15 + j * 0.16));
      slam("#cr", W(6, "raw") - 0.1, -4);
      slam("#ct", W(6, "tested") - 0.1, 2);

      /* ================= END CARD ================= */
      add("endc", `<div class="abs" style="left:0;top:330px;width:1080px;text-align:center">
        <img id="logo" src="assets/logo-horizontal.png" style="width:760px;height:auto" />
        <div id="e1" style="font-family:Cap;font-weight:900;font-size:56px;margin-top:40px">REALITY CHECK: <span style="color:${{BLUE}}">RAW WATER</span></div>
        <div id="e2" style="font-family:Cap;font-weight:800;font-size:40px;color:${{MUTED}};margin-top:8px">aquacoreglobal.com</div>
        <div id="e3" style="display:inline-block;margin-top:46px;padding:22px 42px;border:7px solid ${{INK}};border-radius:40px;font-family:Hand;font-size:58px">Would <span style="color:${{BLUE}}">you</span> drink raw water? 💬</div>
        <div id="e4" style="font-family:Cap;font-weight:800;font-size:24px;color:${{MUTED}};margin-top:40px">Original video: @erikharding.health (TikTok, Jul 2026) · Sources: CDC MMWR 2023 · US EPA</div></div>`);
      pop("#logo", T[7] + 0.05);
      tl.fromTo("#e1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, T[7] + 0.25);
      tl.fromTo("#e2", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, T[7] + 0.4);
      pop("#e3", T[7] + 0.6);

{guide}
      // presenter: bottom-right, talks and points at the verdicts
      const GX = 910, GY = 1130;
      gAt(GX, GY, 0, "hmm"); gTalk(0);
      gPoint(540, 960, W(0, "longer") + 0.1);
      gPoint(760, 735, W(0, "saved") - 0.2);
      CL.forEach((c, k) => {{
        const i = k + 1, te = T[i + 1];
        gAt(GX, GY, T[i], k === 4 ? "o" : "hmm"); gTalk(i);
        const tr = TIMED[i].find((x, j) => j > 0 && /[?]$/.test(TIMED[i][j - 1].w)) || TIMED[i][Math.floor(TIMED[i].length / 3)];
        gPoint(280, 1150, tr.t + 0.05);
        gPoint(540, 1300, te - 1.0);
      }});
      gAt(GX, GY, T[6], "smile"); gTalk(6);
      gPoint(540, 1235, W(6, "tested") + 0.1);
      gHideFinger(T[7] - 0.15);
      gAt(470, 1450, T[7], "smile");
      tl.fromTo("#guide .armR", {{ rotation: 0 }}, {{ rotation: -150, svgOrigin: "100 150", duration: 0.3 }}, T[7] + 0.2);
      tl.fromTo("#guide .armR", {{ rotation: -150 }}, {{ rotation: -110, svgOrigin: "100 150", duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, T[7] + 0.5);
      tl.set("#caps", {{ opacity: 0 }}, T[7]); tl.set("#caps", {{ opacity: 1 }}, 0);
      tl.set("#guideLayer", {{ opacity: 0 }}, {SPLASH}); tl.set("#guideLayer", {{ opacity: 1 }}, T[1]); tl.set("#guideLayer", {{ opacity: 1 }}, 0);

      const KEY = /^(live|longer|three|thousand|saved|facts|aging|evidence|chlorine|fluoride|tiny|regulated|germs|pipes|treatment|spring|montana|nineteen|sick|untreated|decades|taste|smell|colour|lab|test|bottled|mineral|tested|raw|treated)$/i;
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
json.dump({"id": "reality-raw-water-v2", "name": "reality-raw-water-v2"}, open(os.path.join(P, "meta.json"), "w"))
print("END", END, "T", T, "SPLASH", SPLASH)
