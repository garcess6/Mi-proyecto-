#!/usr/bin/env python3
"""Generate the DR Congo country video (EN / FR, 9:16 / 16:9) from the episode template.

Usage: python3 gen.py   (run inside videos/pais-cod)
"""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "ep05-analisis", "index.html")

TX = {
    "en": {
        "voice": "af_heart",
        "tag": "PILOT PROGRAM · <b>AQUACORE</b>",
        "title": "Pilot Program",
        "locale": "en-US",
        "key": "pilot|five|steps|one|two|three|four|five|hundred|tablets|lab|before|after|review|results|size|people|deploy|distribution|training|scale|region",
    },
}

SCENES = r'''
      const TX = __TX__;
      const T = __T__;
      const RED = "#d64545";
      const at = (li, f) => LINES[li][0] + LINES[li][1] * f;
      const iAqua = `<g stroke="${INK}" stroke-width="9" fill="none" stroke-linejoin="round"><path d="M80 14 C80 14 38 66 38 96 a42 42 0 0 0 84 0 C122 66 80 14 80 14 Z"/></g><circle cx="80" cy="96" r="18" fill="${BLUE}"/>`;
      const iClock = `<circle cx="80" cy="80" r="64" fill="#fff" stroke="${INK}" stroke-width="9"/><circle cx="80" cy="80" r="7" fill="${INK}"/>`;
      const iFlask = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round" stroke-linecap="round"><path d="M60 14 L100 14 M66 14 L66 64 L22 142 L138 142 L94 64 L94 14"/></g><path d="M42 108 L118 108 L132 138 L28 138 Z" fill="${SKY}"/>`;
      const iTab = `<path d="M18 70 V92 A62 24 0 0 0 142 92 V70" fill="${SKY}" stroke="${INK}" stroke-width="8"/><ellipse cx="80" cy="70" rx="62" ry="24" fill="#fff" stroke="${INK}" stroke-width="8"/><line x1="46" y1="70" x2="114" y2="70" stroke="${BLUE}" stroke-width="7" stroke-linecap="round"/>`;
      const iBox = `<path d="M20 50 L80 22 L140 50 L140 124 L80 150 L20 124 Z" fill="#fff" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/><path d="M20 50 L80 78 L140 50 M80 78 L80 150" fill="none" stroke="${BLUE}" stroke-width="7"/><text x="112" y="116" text-anchor="middle" font-family="Cap" font-weight="900" font-size="26" fill="${INK}" transform="rotate(-22 112 116)">100</text>`;
      const iChart = `<g stroke="${INK}" stroke-width="7" fill="#fff"><path d="M14 146 H146" stroke-linecap="round"/><rect class="br" x="30" y="96" width="24" height="44" stroke="${BLUE}"/><rect class="br" x="68" y="66" width="24" height="74"/><rect class="br" x="106" y="36" width="24" height="104" stroke="${BLUE}"/></g>`;
      const iPeople = `<g stroke="${INK}" stroke-width="7" fill="#fff" stroke-linecap="round"><circle cx="58" cy="50" r="20"/><path d="M22 140 C22 106 38 92 58 92 S94 106 94 140"/><circle cx="110" cy="58" r="16" stroke="${BLUE}"/><path d="M88 140 C90 116 98 106 110 106 S132 116 136 140" stroke="${BLUE}"/></g>`;
      const iTruck = `<g stroke="${INK}" stroke-width="6" fill="#fff" stroke-linejoin="round"><rect x="10" y="50" width="86" height="56" rx="6"/><path d="M96 66 H124 L146 88 V106 H96 Z"/><circle cx="38" cy="114" r="13"/><circle cx="118" cy="114" r="13"/><rect x="24" y="64" width="22" height="26" fill="${SKY}"/><rect x="54" y="64" width="22" height="26" fill="${SKY}"/></g>`;
      const iCycle = `<g stroke="${BLUE}" stroke-width="9" fill="none" stroke-linecap="round"><path d="M126 70 A50 50 0 0 0 38 54"/><path d="M34 90 A50 50 0 0 0 122 106"/><path d="M38 30 L38 56 L64 56"/><path d="M122 130 L122 104 L96 104"/></g><path d="M62 82 L76 96 L100 70" stroke="${INK}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      const iNgo = `<path d="M80 140 C80 140 20 106 20 64 a30 30 0 0 1 60 -10 a30 30 0 0 1 60 10 C140 106 80 140 80 140Z" fill="#fff" stroke="${INK}" stroke-width="8"/>`;
      const iGov = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round"><path d="M16 56 L80 22 L144 56 Z"/><path d="M14 140 H146"/></g><path d="M34 66 V126 M64 66 V126 M96 66 V126 M126 66 V126" stroke="${BLUE}" stroke-width="8"/>`;
      const iInv = `<g stroke="${INK}" stroke-width="8" fill="none" stroke-linecap="round"><path d="M14 140 H146"/></g><path d="M22 116 L58 80 L82 100 L134 46 M106 46 H134 V74" stroke="${BLUE}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      const iGlobe = `<circle cx="80" cy="80" r="62" fill="${SKY}" stroke="${INK}" stroke-width="8"/><ellipse cx="80" cy="80" rx="26" ry="62" fill="none" stroke="${BLUE}" stroke-width="6"/><path d="M18 80 H142 M28 46 H132 M28 114 H132" stroke="${BLUE}" stroke-width="6" fill="none"/>`;
      const iChat = `<path d="M16 24 H144 V108 H70 L40 134 V108 H16 Z" fill="#fff" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/><path d="M40 56 H120 M40 80 H96" stroke="${BLUE}" stroke-width="8" stroke-linecap="round"/>`;
      const iScale = `<g stroke="${INK}" stroke-width="5">${[[40, 50], [80, 40], [120, 52], [52, 92], [96, 88], [72, 128], [118, 120]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="16" fill="${SKY}"/><circle cx="${x}" cy="${y}" r="6" fill="${BLUE}" stroke="none"/>`).join("")}</g>`;
      const svgI = (icon, w) => `<svg viewBox="0 0 160 160" width="${w}" height="${w}">${icon}</svg>`;
      const card = (id, left, top, w, icon, label, isz = 170, fs = 46) => `<div id="${id}" class="abs card" style="left:${left}px;top:${top}px;width:${w}px;padding:16px 10px">${svgI(icon, isz)}<div class="label" style="font-size:${fs}px;line-height:1.05">${label}</div></div>`;
      const chipAt = (id, top, html, size = 60, bg = BLUE, rot = 0) => `<div id="${id}" class="abs" style="left:0;top:${top}px;width:1080px;text-align:center"><span class="chip" style="font-size:${size}px;background:${bg};display:inline-block;transform:rotate(${rot}deg)">${html}</span></div>`;
      const center = (id, top, html) => `<div id="${id}" class="abs" style="left:0;top:${top}px;width:1080px;text-align:center">${html}</div>`;
      const tracker = (sid, labels, cur) => `<div class="abs" style="left:60px;top:10px;width:960px;display:flex;gap:12px">${labels.map((l, k) => `<div style="flex:1"><div style="height:16px;border-radius:8px;background:${k < cur ? BLUE : "#d5dee8"}" id="${sid}s${k}"></div><div style="font-family:Cap;font-weight:900;font-size:${labels.length > 4 ? 24 : 30}px;margin-top:8px;color:${k <= cur ? INK : "#9aa8b8"}">${l}</div></div>`).join("")}</div>`;
      const trackOn = (sid, k, t) => tl.to(`#${sid}s${k}`, { backgroundColor: BLUE, duration: 0.25 }, t);
      const stepNum = (id, n) => `<div id="${id}" class="abs" style="left:60px;top:120px;width:140px;height:140px;border-radius:70px;background:${BLUE};color:#fff;font-family:Cap;font-weight:900;font-size:90px;display:flex;align-items:center;justify-content:center;border:7px solid ${INK}">${n}</div>`;
      const endCard = (sid) => { add(sid, `<div class="abs" style="left:0;top:120px;width:1080px;text-align:center"><img id="logo" src="assets/logo.png" style="width:420px;height:420px" /><div id="e2" style="font-family:Cap;font-weight:900;font-size:60px;margin-top:20px">aquacoreglobal.com</div></div>`); };

      const P5 = ["SEND", "TEST", "REVIEW", "SIZE", "DEPLOY"];
      /* S0 · title */
      add("s0", center("p0", 40, svgI(`<path d="M80 150 C80 150 30 96 30 64 a50 50 0 0 1 100 0 C130 96 80 150 80 150 Z" fill="${SKY}" stroke="${INK}" stroke-width="9"/><circle cx="80" cy="64" r="18" fill="${BLUE}"/>`, 320)) + center("p0t", 400, `<div style="font-family:Cap;font-weight:900;font-size:104px;line-height:1">HOW A PILOT<br><span style="color:${BLUE}">WORKS</span></div>`) + chipAt("p0c", 700, "5 STEPS", 70));
      tl.set(["#p0t", "#p0c"], { opacity: 0 }, 0);
      tl.fromTo("#p0", { y: -400, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "bounce.out" }, 0.05);
      pop("#p0t", at(0, 0.15)); pop("#p0c", at(0, 0.5), { rotation: -2 });
      /* S1 · send 100 tablets */
      add("s1", tracker("k1", P5, 0) + stepNum("n1", 1) + `<div id="bx1" class="abs" style="left:300px;top:200px">${svgI(iBox, 480)}</div>` + `<svg class="abs" style="left:0;top:0" width="1080" height="1080"><path id="pl1" d="M120 900 Q540 660 960 900" fill="none" stroke="${BLUE}" stroke-width="8" stroke-dasharray="20 16"/></svg>` + chipAt("c1", 960, "100 TABLETS", 60));
      tl.set(["#c1", "#pl1"], { opacity: 0 }, T[1]);
      trackOn("k1", 0, T[1] + 0.05); pop("#n1", T[1] + 0.05);
      tl.fromTo("#bx1", { x: -700, rotation: -20 }, { x: 0, rotation: 0, duration: 0.6, ease: "back.out(1.4)" }, T[1] + 0.1);
      tl.to("#pl1", { opacity: 1, duration: 0.3 }, at(1, 0.5)); pop("#c1", at(1, 0.4));
      /* S2 · local lab tests before/after */
      const dish = (id, n) => { let c = ""; for (let i = 0; i < n; i++) c += `<circle cx="${-80 + rnd() * 160}" cy="${-46 + rnd() * 92}" r="${5 + rnd() * 7}" fill="${BLUE}" stroke="${INK}" stroke-width="3"/>`; return `<svg id="${id}" viewBox="-130 -90 260 180" width="380" height="262"><ellipse rx="120" ry="78" fill="#fff" stroke="${INK}" stroke-width="9"/><ellipse rx="102" ry="62" fill="${SKY}" stroke="${INK}" stroke-width="4"/>${c}</svg>`; };
      add("s2", tracker("k2", P5, 1) + stepNum("n2", 2) + center("fl2", 110, svgI(iFlask, 240)) + `<div id="b2" class="abs" style="left:40px;top:430px;width:400px;text-align:center">${dish("d2a", 24)}<div class="chip" style="display:inline-block">BEFORE</div></div><div id="a2" class="abs" style="left:640px;top:430px;width:400px;text-align:center">${dish("d2b", 0)}<div class="chip" style="display:inline-block">AFTER ✓</div></div>` + `<div id="ar2" class="abs label" style="left:470px;top:470px;font-size:120px;color:${BLUE}">→</div>` + `<div id="ll2" class="abs label" style="left:0;top:830px;width:1080px;font-size:56px">your local lab</div>`);
      tl.set(["#b2", "#a2", "#ar2", "#ll2"], { opacity: 0 }, T[2]);
      trackOn("k2", 1, T[2] + 0.05); pop("#n2", T[2] + 0.05); pop("#fl2", T[2] + 0.1); pop("#ll2", at(2, 0.2));
      pop("#b2", at(2, 0.55)); pop("#ar2", at(2, 0.7)); pop("#a2", at(2, 0.82));
      /* S3 · review results */
      add("s3", tracker("k3", P5, 2) + stepNum("n3", 3) + center("ch3", 160, svgI(iChart, 420)) + chipAt("c3", 640, "REVIEW TOGETHER", 64));
      tl.set("#c3", { opacity: 0 }, T[3]);
      trackOn("k3", 2, T[3] + 0.05); pop("#n3", T[3] + 0.05); pop("#ch3", T[3] + 0.1);
      tl.fromTo("#ch3 .br", { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.4, stagger: 0.15, ease: "back.out(1.6)" }, T[3] + 0.2);
      pop("#c3", at(3, 0.5), { rotation: -2 });
      /* S4 · size the program */
      add("s4", tracker("k4", P5, 3) + stepNum("n4", 4) + `<div id="pp4" class="abs" style="left:120px;top:250px;width:380px;text-align:center">${svgI(iPeople, 260)}<div class="label" style="font-size:56px">how many people?</div></div><div id="tt4" class="abs" style="left:580px;top:250px;width:380px;text-align:center">${svgI(iTab, 260)}<div class="label" style="font-size:56px">how many tablets?</div></div>` + chipAt("c4", 760, "SIZE THE PROGRAM", 64));
      tl.set(["#pp4", "#tt4", "#c4"], { opacity: 0 }, T[4]);
      trackOn("k4", 3, T[4] + 0.05); pop("#n4", T[4] + 0.05); pop("#c4", T[4] + 0.15, { rotation: -2 });
      pop("#pp4", at(4, 0.45)); pop("#tt4", at(4, 0.75));
      /* S5 · deploy & scale */
      let dots = ""; for (let r = 0; r < 4; r++) for (let c = 0; c < 7; c++) { const x = 150 + c * 130 + (r % 2) * 40, y = 640 + r * 95; dots += `<g class="rg5" data-o="${c + r}"><circle cx="${x}" cy="${y}" r="32" fill="#fff" stroke="${INK}" stroke-width="5"/><circle class="rd5" cx="${x}" cy="${y}" r="14" fill="${BLUE}" opacity="0"/></g>`; }
      add("s5", tracker("k5", P5, 4) + stepNum("n5", 5) + `<div id="tr5" class="abs" style="left:260px;top:130px">${svgI(iTruck, 280)}</div><div id="tn5" class="abs" style="left:600px;top:150px;width:300px;text-align:center">${svgI(iPeople, 200)}<div class="label" style="font-size:44px">training</div></div>` + `<svg class="abs" style="left:0;top:0" width="1080" height="1080">${dots}</svg>` + chipAt("c5", 1000, "REGION BY REGION", 52));
      tl.set(["#tn5", "#c5"], { opacity: 0 }, T[5]);
      trackOn("k5", 4, T[5] + 0.05); pop("#n5", T[5] + 0.05);
      tl.fromTo("#tr5", { x: -700 }, { x: 0, duration: 0.6, ease: "power2.out" }, T[5] + 0.1);
      pop("#tn5", at(5, 0.4));
      $$("#s5 .rg5").forEach((g) => { const o = +g.dataset.o; tl.to(g.querySelector(".rd5"), { opacity: 1, duration: 0.12 }, at(5, 0.65) + o * 0.1); });
      pop("#c5", at(5, 0.75));
      /* S6 · CTA */
      add("s6", center("cb6", 40, svgI(iChat, 320)) + `<div id="q6" class="abs" style="left:0;top:400px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:84px;line-height:1.05">Ready for a pilot<br>in your region?</div>` + chipAt("c6", 700, "DM US: PILOT", 90, BLUE, -2));
      tl.set(["#q6", "#c6"], { opacity: 0 }, T[6]);
      pop("#cb6", T[6] + 0.05); pop("#q6", at(6, 0.1)); pop("#c6", at(6, 0.6), { rotation: -2 });

      /* end card */
      endCard("s" + (T.length - 2));
      pop("#logo", T[T.length - 2] + 0.05);
      tl.fromTo("#e2", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35 }, T[T.length - 2] + 0.3);
'''


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


def build(lang):
    tx = TX[lang]
    lines = [l.strip() for l in open(os.path.join(HERE, "assets", f"lines_{lang}.txt")) if l.strip()]
    durs = [dur(os.path.join(HERE, "assets", f"vo_{lang}", f"l{i+1}.wav")) for i in range(len(lines))]
    starts, t = [], 0.3
    for d in durs:
        starts.append(round(t, 2))
        t += d + 0.45
    end_card = round(starts[-1] + durs[-1] + 0.5, 2)
    total = round(end_card + 2.5, 2)
    T = [0] + starts[1:] + [end_card, total]

    # voice track
    inputs, filt, mix = [], "", ""
    for i, s in enumerate(starts):
        inputs += ["-i", os.path.join(HERE, "assets", f"vo_{lang}", f"l{i+1}.wav")]
        ms = int(s * 1000)
        filt += f"[{i}:a]adelay={ms}|{ms}[a{i}];"
        mix += f"[a{i}]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
                    f"{filt}{mix}amix=inputs={len(starts)}:normalize=0,apad=whole_dur={total}[out]",
                    "-map", "[out]", "-ar", "24000", "-ac", "1", os.path.join(HERE, "assets", f"voice_{lang}.wav")], check=True)

    s = open(TEMPLATE).read()
    a = s.index("      const iAqua =")
    b = s.index("      /* ================= captions")
    mapdata = json.load(open(os.path.join(HERE, "assets", "map.json")))
    js_tx = {k: v for k, v in tx.items() if k not in ("voice", "key")}
    scenes = SCENES.replace("__TX__", json.dumps(js_tx, ensure_ascii=False)).replace("__MAP__", json.dumps(mapdata)).replace("__T__", json.dumps(T))
    s = s[:a] + scenes + s[b:]
    la = s.index("      const LINES = [")
    lb = s.index("      ];", la) + len("      ];")
    s = s[:la] + "      const LINES = [\n" + "".join(f"        [{st}, {d:.2f}, {json.dumps(l, ensure_ascii=False)}],\n" for st, d, l in zip(starts, durs, lines)) + "      ];" + s[lb:]
    s = re.sub(r'data-duration="64\.5"', f'data-duration="{total}"', s)
    s = s.replace('src="assets/voice.wav"', f'src="assets/voice_{lang}.wav"')
    s = s.replace('<div id="tag" class="clip" data-start="0" data-duration="61.0"', f'<div id="tag" class="clip" data-start="0" data-duration="{end_card}"')
    s = re.sub(r'<div class="pill">.*?</div>', f'<div class="pill">{tx["tag"]}</div>', s, count=1)
    sa = s.index('        <div id="s0"')
    sb = s.index('      </div>\n      <div id="caps">')
    s = s[:sa] + "".join(f'        <div id="s{k}" class="scene clip" data-start="{T[k]}" data-duration="{round(T[k+1]-T[k],2)}" data-track-index="1"><div class="cam"></div></div>\n' for k in range(len(T) - 1)) + s[sb:]
    s = re.sub(r"const KEY = /\^\(.*?\)\$/i;", f"const KEY = /^({tx['key']})$/i;", s)
    s = s.replace('tl.to("#stage", { x: 393, duration: 0.5, ease: "power2.inOut" }, 61.0);', f'tl.to("#stage", {{ x: 393, duration: 0.5, ease: "power2.inOut" }}, {end_card});')
    s = s.replace("tl.set({}, {}, 64.5);", f"tl.set({{}}, {{}}, {total});")
    s = re.sub(r"<title>.*?</title>", f"<title>{tx['title']}</title>", s)
    s = s.replace('<html lang="en"', f'<html lang="{lang}"')
    assert 'data-duration="64.5"' not in s and "}, 61.0);" not in s and "tl.set({}, {}, 64.5)" not in s

    for fmt in ("9x16", "16x9"):
        d = os.path.join(HERE, f"{lang}-{fmt}")
        os.makedirs(d, exist_ok=True)
        out = s
        if fmt == "16x9":
            out = out.replace('data-resolution="portrait" data-format="portrait"', 'data-resolution="landscape" data-format="landscape"')
            out = out.replace("width=1080, height=1920", "width=1920, height=1080")
            out = out.replace('data-width="1080" data-height="1920"', 'data-width="1920" data-height="1080"')
        open(os.path.join(d, "index.html"), "w").write(out)
        for f in ("hyperframes.json", "package.json"):
            open(os.path.join(d, f), "w").write(open(os.path.join(HERE, f)).read())
        json.dump({"id": f"historia-pilot-{lang}-{fmt}", "name": f"historia-pilot-{lang}-{fmt}"}, open(os.path.join(d, "meta.json"), "w"))
        link = os.path.join(d, "assets")
        if not os.path.islink(link):
            os.symlink("../assets", link)
    print(lang, "total", total, "T", T)


if __name__ == "__main__":
    for lang in ("en",):
        build(lang)
