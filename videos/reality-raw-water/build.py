#!/usr/bin/env python3
"""Reality Check: raw water. Builds proj/index.html + voice track from the clip, freeze frames and VO lines."""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "proj")
CHOL = os.path.join(HERE, "..", "colera", "sp01-colera", "index.html")
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
LINES = [l.strip() for l in open(os.path.join(HERE, "lines.txt")) if l.strip()]
VD = [dur(os.path.join(P, "assets", "vo", f"v{i}.wav")) for i in range(len(LINES))]

CLAIMS = [  # clip in/out (s), freeze frame, claim label, stamp, reality text, source
    (0.45, 2.2, "fr_2.15.jpg", "CLAIM #1", "NO EVIDENCE", "No study shows that treated tap water “ages” you.", ""),
    (2.2, 3.4, "fr_3.35.jpg", "CLAIM #2", "TINY &amp; REGULATED", "Legal limits: chlorine ≤ 4 mg/L · fluoride ≤ 4 mg/L. Chlorine kills germs in the pipes.", "Source: US EPA drinking-water standards"),
    (3.4, 6.7, "fr_6.6.jpg", "CLAIM #3", "RISKY", "Montana, 2022: 19 people sick (Campylobacter) after drinking untreated water from a spot used for decades.", "Source: CDC MMWR, April 2023"),
    (8.9, 11.4, "fr_11.35.jpg", "CLAIM #4", "TASTE ≠ SAFE", "Germs have no taste, no smell and no colour. Only a lab test can tell.", ""),
    (11.4, 13.4, "fr_13.35.jpg", "PLAN B", "PLOT TWIST", "His backup: bottled mineral water. Tested and regulated. Not raw.", ""),
]

# ---------- timeline
T, starts = [], []
t = 0.0
T.append(t); starts.append(0.2); t = round(0.2 + VD[0] + 0.35, 2)              # hook
for i, (a, b, *_r) in enumerate(CLAIMS, 1):
    T.append(t); starts.append(round(t + 0.15, 2))
    t = round(t + max(b - a + 0.3, VD[i] + 0.55), 2)
T.append(t); starts.append(round(t + 0.15, 2)); t = round(t + VD[6] + 0.6, 2)  # conclusion
T.append(t); END = round(t + 3.2, 2); T.append(END)                            # end card

# voice track
inp, flt, mix = [], "", ""
for i, s in enumerate(starts):
    inp += ["-i", os.path.join(P, "assets", "vo", f"v{i}.wav")]
    ms = int(s * 1000); flt += f"[{i}:a]adelay={ms}|{ms}[a{i}];"; mix += f"[a{i}]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", f"{flt}{mix}amix=inputs={len(starts)}:normalize=0,apad=whole_dur={END}[o]",
                "-map", "[o]", "-ar", "24000", "-ac", "1", os.path.join(P, "assets", "voice.wav")], check=True)

chol = open(CHOL).read()
helpers = chol[chol.index("      function figure("):chol.index("      // cholera bacterium")]
guide = chol[chol.index("      /* ================= GUIDE"):chol.index("      // S0 hook")]
guide = guide.replace("const GW = 130,", "const GW = 150,").replace("const nx = tx - 33, ny = ty + 4;", "const nx = tx - 33, ny = ty + 30;")
guide = guide.replace('document.getElementById("guideLayer")', 'document.getElementById("guideLayer")')
caps = chol[chol.index("      /* ================= captions"):chol.index("      if (document.documentElement.dataset.format")]
import re as _re
caps = _re.sub(r"      const KEY = .*\n", "", caps)

FX, FY, FW, FH = 208, 200, 664, 1200  # video frame

clips_html = ""
for i, (a, b, fr, *_r) in enumerate(CLAIMS, 1):
    ts, d = T[i], round(b - a, 2)
    clips_html += f'      <video id="vid{i}" class="clip fv" src="assets/clip.mp4" data-start="{ts}" data-duration="{d}" data-media-start="{a}" muted playsinline></video>\n'
    clips_html += f'      <img id="frz{i}" class="clip fv" src="assets/{fr}" data-start="{round(ts + d, 2)}" data-duration="{round(T[i + 1] - ts - d, 2)}" />\n'

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
      :root {{ --ink: #111418; --blue: #1e7fd8; --sky: #dff2fc; --muted: #8b96a3; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #fff; }}
      #root {{ position: relative; width: 1080px; height: 1920px; background: #fff; font-family: "Hand", sans-serif; color: var(--ink); overflow: hidden; }}
      .abs {{ position: absolute; }}
      svg {{ overflow: visible; }}
      #frame {{ position: absolute; left: {FX}px; top: {FY}px; width: {FW}px; height: {FH}px; border: 9px solid var(--ink); border-radius: 34px; overflow: hidden; background: #000; }}
      .fv {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
      #dim {{ position: absolute; inset: 0; background: rgba(10,14,20,0.42); opacity: 0; }}
      .pill {{ white-space: nowrap; display: inline-flex; align-items: center; gap: 14px; padding: 10px 28px; border: 5px solid var(--ink); border-radius: 999px; font-family: "Cap"; font-weight: 900; font-size: 34px; letter-spacing: 0.04em; background: #fff; }}
      .pill b {{ color: var(--blue); }}
      .chip {{ font-family: "Cap"; font-weight: 900; letter-spacing: 0.05em; padding: 8px 26px; border-radius: 16px; background: var(--blue); color: #fff; border: 5px solid var(--ink); white-space: nowrap; display: inline-block; }}
      .claim {{ background: #ffd34d; color: var(--ink); }}
      .stamp {{ font-family: "Cap"; font-weight: 900; font-size: 70px; color: #d64545; border: 9px solid #d64545; border-radius: 18px; padding: 6px 26px; background: rgba(255,255,255,0.92); white-space: nowrap; display: inline-block; letter-spacing: 0.03em; }}
      .card {{ background: #fff; border: 7px solid var(--ink); border-radius: 26px; }}
      .rc {{ position: absolute; left: {FX + 24}px; width: {FW - 48}px; top: {FY + FH - 330}px; padding: 18px 26px 20px; }}
      .rc .h {{ font-family: "Cap"; font-weight: 900; font-size: 30px; color: #fff; background: var(--blue); display: inline-block; padding: 4px 18px; border-radius: 10px; letter-spacing: 0.08em; }}
      .rc .t {{ font-family: "Cap"; font-weight: 800; font-size: 40px; line-height: 1.15; margin-top: 12px; }}
      .rc .s {{ font-family: "Cap"; font-weight: 800; font-size: 22px; color: var(--muted); margin-top: 10px; }}
      #caps {{ position: absolute; left: 60px; width: 960px; top: 1410px; height: 210px; }}
      .cap {{ position: absolute; left: 0; right: 0; top: 50%; transform: translateY(-50%); text-align: center; font-family: "Cap"; font-weight: 900; font-size: 68px; line-height: 1.1; color: var(--ink); opacity: 0; }}
      .cap span {{ display: inline-block; margin: 0 0.06em; }}
      .cap span.k {{ color: var(--blue); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{END}"></audio>
      <div id="tag" class="abs" style="left:0;top:95px;width:1080px;text-align:center"><div class="pill"><img src="assets/logo-drop.png" style="height:46px;width:auto" />REALITY CHECK · <b>RAW WATER</b></div></div>
      <div id="frame">
      <img id="hk" class="clip fv" src="assets/fr_14.0.jpg" data-start="0" data-duration="{T[1]}" />
{clips_html}        <div id="concl" class="clip abs" data-start="{T[6]}" data-duration="{round(T[7] - T[6], 2)}" style="inset:0;background:#fff"></div>
        <div id="dim"></div>
        <div id="cred" class="abs" style="left:18px;top:18px;font-family:Cap;font-weight:800;font-size:22px;color:#fff;background:rgba(0,0,0,0.55);padding:6px 14px;border-radius:10px">Video: @erikharding.health · TikTok · Jul 2026</div>
      </div>
      <div id="ov" class="abs" style="left:0;top:0;width:1080px;height:1920px"></div>
      <div id="endc" class="clip abs" data-start="{T[7]}" data-duration="{round(END - T[7], 2)}" style="left:0;top:0;width:1080px;height:1920px;background:#fff"></div>
      <div id="guideLayer" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:5"></div>
      <div id="caps"></div>
    </div>
    <script>
      const INK = "#111418", BLUE = "#1e7fd8", SKY = "#dff2fc", MUTED = "#8b96a3", RED = "#d64545";
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
      const pop = (sel, t, extra = {{}}) => tl.fromTo(sel, {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)", ...extra }}, t);
      const slam = (sel, t, rot = -6) => tl.fromTo(sel, {{ scale: 2.2, opacity: 0, rotation: rot }}, {{ scale: 1, opacity: 1, rotation: rot, duration: 0.28, ease: "back.out(2.2)" }}, t);
      const ov = (html) => document.getElementById("ov").insertAdjacentHTML("beforeend", html);
      const hide = (sel, t) => tl.to(sel, {{ opacity: 0, duration: 0.15 }}, t);
      const CL = {json.dumps([[c[3], c[4], c[5], c[6]] for c in CLAIMS], ensure_ascii=False)};

      /* ---------- HOOK ---------- */
      ov(`<div id="hq" class="abs" style="left:0;top:{FY + 120}px;width:1080px;text-align:center;opacity:0"><span class="chip claim" style="font-size:44px">CLAIM: “LIVE LONGER”</span></div>`);
      ov(`<div id="hs" class="abs" style="left:0;top:{FY + 760}px;width:1080px;text-align:center;opacity:0"><span class="stamp" style="font-size:84px">LIVE LONGER?</span></div>`);
      ov(`<div id="hl" class="abs" style="left:{FX + 40}px;top:{FY + 980}px;opacity:0"><span class="chip" style="font-size:38px;background:${{INK}}">♥ 20.6K</span></div><div id="hv" class="abs" style="left:{FX + 330}px;top:{FY + 980}px;opacity:0"><span class="chip" style="font-size:38px">🔖 <span id="hvn">0</span> saves</span></div>`);
      tl.fromTo("#frame", {{ scale: 0.9, opacity: 0, transformOrigin: "50% 40%" }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, 0);
      tl.fromTo("#hk", {{ scale: 1.0 }}, {{ scale: 1.12, duration: T[1], ease: "none", transformOrigin: "50% 35%" }}, 0);
      slam("#hq", 0.25, -3);
      slam("#hs", W(0, "longer") - 0.1, -6);
      pop("#hl", W(0, "three") - 0.2); pop("#hv", W(0, "saved") - 0.4);
      {{ const o = {{ v: 0 }}; tl.to(o, {{ v: 3194, duration: 1.0, ease: "power2.out", onUpdate: () => {{ document.getElementById("hvn").textContent = Math.round(o.v).toLocaleString("en-US"); }} }}, W(0, "saved") - 0.3); }}
      tl.to("#dim", {{ opacity: 1, duration: 0.2 }}, W(0, "check") - 0.2);
      hide(["#hq", "#hs", "#hl", "#hv"], T[1] - 0.15);
      tl.set("#dim", {{ opacity: 0 }}, T[1]);

      /* ---------- CLAIMS ---------- */
      CL.forEach(([lab, stamp, txt, srcT], k) => {{
        const i = k + 1, ts = T[i], te = T[i + 1];
        ov(`<div id="cl${{i}}" class="abs" style="left:{FX + 24}px;top:{FY + 70}px;opacity:0"><span class="chip claim" style="font-size:40px">${{lab}}</span></div>`);
        ov(`<div id="st${{i}}" class="abs" style="left:0;top:{FY + 560}px;width:1080px;text-align:center;opacity:0"><span class="stamp">${{stamp}}</span></div>`);
        ov(`<div id="rc${{i}}" class="rc card" style="opacity:0"><span class="h">REALITY</span><div class="t">${{txt}}</div>${{srcT ? `<div class="s">${{srcT}}</div>` : ""}}</div>`);
        pop(`#cl${{i}}`, ts + 0.05);
        const fz = ts + (+document.getElementById("vid" + i).dataset.duration);
        tl.fromTo(`#frz${{i}}`, {{ scale: 1 }}, {{ scale: 1.08, duration: Math.max(0.5, te - fz), ease: "none", transformOrigin: "50% 40%" }}, fz);
        // the rebuttal lands on the second sentence of the line
        const tr = TIMED[i].find((x, j) => j > 0 && /[?]$/.test(TIMED[i][j - 1].w)) || TIMED[i][Math.floor(TIMED[i].length / 3)];
        tl.to("#dim", {{ opacity: 1, duration: 0.2 }}, Math.max(fz, tr.t - 0.1));
        slam(`#st${{i}}`, tr.t - 0.05, k % 2 ? 5 : -6);
        tl.fromTo(`#rc${{i}}`, {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power2.out" }}, tr.t + 0.35);
        hide([`#cl${{i}}`, `#st${{i}}`, `#rc${{i}}`], te - 0.12);
        tl.set("#dim", {{ opacity: 0 }}, te);
      }});

      /* ---------- CONCLUSION ---------- */
      document.getElementById("concl").insertAdjacentHTML("beforeend", `
        <div class="abs" style="left:0;top:120px;width:646px;text-align:center"><span id="c1" class="chip" style="font-size:46px;background:${{RED}};text-decoration:line-through">RAW</span></div>
        <div id="cg" class="abs" style="left:180px;top:260px">${{glass("cgl", {{ left: 0, top: 0, w: 270 }})}}</div>
        <div id="c2" class="abs" style="left:0;top:700px;width:646px;text-align:center"><span class="chip" style="font-size:54px">TESTED ✓</span></div>
        <div id="c3" class="abs" style="left:0;top:820px;width:646px;text-align:center"><span class="chip" style="font-size:54px">TREATED ✓</span></div>
        <div id="c4" class="abs" style="left:30px;top:960px;width:586px;text-align:center;font-family:Hand;font-size:50px;line-height:1.1">the water that helps you live longer</div>`);
      tl.set(["#c1", "#cg", "#c2", "#c3", "#c4"], {{ opacity: 0 }}, T[6]);
      pop("#c1", W(6, "raw") - 0.15); pop("#cg", T[6] + 0.1);
      slam("#c2", W(6, "tested") - 0.1, -3); slam("#c3", W(6, "treated") - 0.1, 3);
      tl.to("#c4", {{ opacity: 1, duration: 0.3 }}, W(6, "longer"));
      tl.set("#cred", {{ opacity: 0 }}, T[6]);

      /* ---------- END CARD ---------- */
      document.getElementById("endc").insertAdjacentHTML("beforeend", `<div class="abs" style="left:0;top:330px;width:1080px;text-align:center">
        <img id="logo" src="assets/logo-horizontal.png" style="width:760px;height:auto" />
        <div id="e1" style="font-family:Cap;font-weight:900;font-size:56px;margin-top:40px">REALITY CHECK: <span style="color:${{BLUE}}">RAW WATER</span></div>
        <div id="e2" style="font-family:Cap;font-weight:800;font-size:40px;color:${{MUTED}};margin-top:8px">aquacoreglobal.com</div>
        <div id="e3" style="display:inline-block;margin-top:46px;padding:22px 42px;border:7px solid ${{INK}};border-radius:40px;font-family:Hand;font-size:58px">Would <span style="color:${{BLUE}}">you</span> drink raw water? 💬</div>
        <div id="e4" style="font-family:Cap;font-weight:800;font-size:24px;color:${{MUTED}};margin-top:40px">Original video: @erikharding.health (TikTok, Jul 2026) · Sources: CDC MMWR 2023 · US EPA</div></div>`);
      pop("#logo", T[7] + 0.05);
      tl.fromTo("#e1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, T[7] + 0.25);
      tl.fromTo("#e2", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, T[7] + 0.4);
      pop("#e3", T[7] + 0.6); tl.to("#e4", {{ opacity: 1, duration: 0.3 }}, T[7] + 0.9); tl.set("#e4", {{ opacity: 0 }}, 0);
      tl.set(["#tag", "#caps"], {{ opacity: 1 }}, 0); tl.set("#tag", {{ opacity: 0 }}, T[7]);

{guide}
      // presenter beside the frame, bottom right
      const GX = 905, GY = 1110;
      gAt(GX, GY, 0, "hmm"); gTalk(0);
      gPoint(540, {FY + 150}, 0.3);
      gPoint(540, {FY + 860}, W(0, "longer"));
      gPoint({FX + 470}, {FY + 1010}, W(0, "saved") - 0.2);
      CL.forEach((c, k) => {{
        const i = k + 1;
        gAt(GX, GY, T[i], k === 4 ? "o" : "hmm"); gTalk(i);
        const tr = TIMED[i].find((x, j) => j > 0 && /[?]$/.test(TIMED[i][j - 1].w)) || TIMED[i][Math.floor(TIMED[i].length / 3)];
        gPoint(540, {FY + 650}, tr.t);
      }});
      gAt(GX, GY, T[6], "smile"); gTalk(6);
      gPoint({FX + 323}, {FY + 760}, W(6, "tested") - 0.1);
      gPoint({FX + 323}, {FY + 880}, W(6, "treated") - 0.1);
      gHideFinger(T[7] - 0.15);
      gAt(470, 1450, T[7], "smile");
      tl.fromTo("#guide .armR", {{ rotation: 0 }}, {{ rotation: -150, svgOrigin: "100 150", duration: 0.3 }}, T[7] + 0.2);
      tl.fromTo("#guide .armR", {{ rotation: -150 }}, {{ rotation: -110, svgOrigin: "100 150", duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, T[7] + 0.5);
      tl.set("#caps", {{ opacity: 0 }}, T[7]);

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
json.dump({"id": "reality-raw-water", "name": "reality-raw-water"}, open(os.path.join(P, "meta.json"), "w"))
print("END", END, "T", T)
