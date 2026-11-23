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
        "tag": "HOW IT WORKS · <b>AQUACORE</b>",
        "title": "How It Works",
        "locale": "en-US",
        "key": "work|safe|four|steps|one|two|three|four|fill|container|well|river|rain|tablet|wait|thirty|minutes|ready|drinking|cooking|litres|instructions",
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

      const L4 = ["FILL", "ADD", "WAIT", "READY"];
      /* S0 · title */
      add("s0", center("h0", 60, svgI(iTab, 320)) + center("h0t", 420, `<div style="font-family:Cap;font-weight:900;font-size:110px;line-height:1">HOW IT<br><span style="color:${BLUE}">WORKS</span></div>`) + chipAt("h0c", 720, "4 SIMPLE STEPS", 70));
      tl.set(["#h0t", "#h0c"], { opacity: 0 }, 0);
      tl.fromTo("#h0", { y: -400, rotation: -120, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.5)" }, 0.05);
      pop("#h0t", at(0, 0.2)); pop("#h0c", at(0, 0.6), { rotation: -2 });
      /* S1 · fill */
      const can = `<svg viewBox="0 0 200 230" width="380" height="437"><defs><clipPath id="cc1"><path d="M34 64 L166 64 L166 214 L34 214 Z"/></clipPath></defs><g clip-path="url(#cc1)"><rect id="wf1" x="30" y="214" width="140" height="160" fill="${SKY}"/><path id="wv1" d="M30 214 Q65 204 100 214 T170 214" stroke="${BLUE}" stroke-width="6" fill="none"/></g><path d="M30 60 L170 60 L170 215 Q170 225 160 225 L40 225 Q30 225 30 215 Z" fill="none" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/><path d="M70 60 L70 30 L130 30 L130 60" fill="#fff" stroke="${INK}" stroke-width="8"/><text x="100" y="170" text-anchor="middle" font-family="Cap" font-weight="900" font-size="40" fill="${INK}">25 L</text></svg>`;
      const src = (id, left, ic, l) => `<div id="${id}" class="abs" style="left:${left}px;top:760px;width:300px;text-align:center">${svgI(ic, 140)}<div class="label" style="font-size:44px">${l}</div></div>`;
      const iRiver = `<path d="M10 120 Q50 100 80 120 T150 120 L150 150 L10 150 Z" fill="${SKY}" stroke="${BLUE}" stroke-width="7"/><path d="M20 90 L50 50 L80 90 Z M70 90 L105 40 L140 90 Z" fill="#fff" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>`;
      const iWell = `<g stroke="${INK}" stroke-width="7" fill="#fff" stroke-linejoin="round"><rect x="30" y="90" width="100" height="56"/><path d="M40 90 L40 40 M120 90 L120 40 M24 40 L136 40"/><path d="M80 40 L80 70"/><rect x="68" y="70" width="24" height="18" fill="${SKY}"/></g>`;
      const iRain = `<g stroke="${INK}" stroke-width="7" fill="#fff" stroke-linejoin="round"><path d="M40 90 a26 26 0 0 1 8 -50 a36 36 0 0 1 68 -6 a30 30 0 0 1 24 56 Z"/></g><g stroke="${BLUE}" stroke-width="7" stroke-linecap="round"><line x1="56" y1="108" x2="46" y2="134"/><line x1="86" y1="108" x2="76" y2="134"/></g>`;
      add("s1", tracker("k1", L4, 0) + stepNum("n1", 1) + `<div id="cn1" class="abs" style="left:350px;top:130px">${can}</div>` + src("r1", 40, iRiver, "river") + src("r2", 390, iWell, "well") + src("r3", 740, iRain, "rain tank"));
      tl.set(["#r1", "#r2", "#r3"], { opacity: 0 }, T[1]);
      trackOn("k1", 0, T[1] + 0.05); pop("#n1", T[1] + 0.05); pop("#cn1", T[1] + 0.15);
      tl.fromTo("#wf1", { attr: { y: 214 } }, { attr: { y: 96 }, duration: 1.6, ease: "power1.out" }, at(1, 0.2));
      tl.fromTo("#wv1", { y: 0 }, { y: -118, duration: 1.6, ease: "power1.out" }, at(1, 0.2));
      pop("#r1", at(1, 0.66)); pop("#r2", at(1, 0.74)); pop("#r3", at(1, 0.84));
      /* S2 · add tablet */
      let fz = ""; for (let i = 0; i < 9; i++) fz += `<circle class="fz2" cx="${400 + rnd() * 280}" cy="760" r="${8 + rnd() * 8}" fill="#fff" stroke="${BLUE}" stroke-width="4"/>`;
      add("s2", tracker("k2", L4, 1) + stepNum("n2", 2) + `<div class="abs" style="left:350px;top:390px">${can.replace(/cc1/g, "cc2").replace('id="wf1" x="30" y="214"', 'x="30" y="96"').replace('id="wv1" d="M30 214 Q65 204 100 214 T170 214"', 'd="M30 96 Q65 86 100 96 T170 96"')}</div>` + `<div id="tb2" class="abs" style="left:440px;top:60px">${svgI(iTab, 200)}</div><svg class="abs" style="left:0;top:0" width="1080" height="1080">${fz}</svg>` + chipAt("c2", 120, "1 TABLET", 64));
      tl.set([".fz2"], { opacity: 0 }, T[2]);
      trackOn("k2", 1, T[2] + 0.05); pop("#n2", T[2] + 0.05); pop("#c2", T[2] + 0.1, { rotation: -3 });
      tl.fromTo("#tb2", { y: -200, rotation: -60 }, { y: 360, rotation: 20, duration: 0.55, ease: "power2.in" }, T[2] + 0.2);
      tl.to("#tb2", { opacity: 0, duration: 0.1 }, T[2] + 0.75);
      tl.fromTo(".fz2", { y: 0, opacity: 0 }, { y: -140, opacity: 1, duration: 0.5, stagger: { each: 0.07, repeat: 3 } }, T[2] + 0.75);
      /* S3 · wait 30 min */
      add("s3", tracker("k3", L4, 2) + stepNum("n3", 3) + center("ck3", 200, `<svg viewBox="0 0 160 160" width="460" height="460">${iClock}<path id="arc3" d="M80 24 A56 56 0 1 1 79.9 24" fill="none" stroke="${SKY}" stroke-width="14" stroke-dasharray="352" stroke-dashoffset="352"/><line id="hd3" x1="80" y1="80" x2="80" y2="30" stroke="${BLUE}" stroke-width="10" stroke-linecap="round"/><circle cx="80" cy="80" r="8" fill="${INK}"/></svg>`) + chipAt("c3", 720, "30 MINUTES", 84));
      tl.set("#c3", { opacity: 0 }, T[3]);
      trackOn("k3", 2, T[3] + 0.05); pop("#n3", T[3] + 0.05); pop("#ck3", T[3] + 0.1);
      tl.to("#hd3", { rotation: 360, svgOrigin: "80 80", duration: 2.2, ease: "power1.inOut" }, T[3] + 0.3);
      tl.to("#arc3", { attr: { "stroke-dashoffset": 0 }, duration: 2.2, ease: "power1.inOut" }, T[3] + 0.3);
      pop("#c3", at(3, 0.3), { rotation: -2 });
      /* S4 · ready */
      add("s4", tracker("k4", L4, 3) + stepNum("n4", 4) + figure("f4", { left: 420, top: 160, w: 260, prop: "glass", face: "smile" }) + chipAt("c4", 700, "READY ✓", 90) + `<div id="dc4" class="abs label" style="left:0;top:860px;width:1080px;font-size:56px">for drinking &amp; cooking</div>`);
      tl.set(["#c4", "#dc4"], { opacity: 0 }, T[4]);
      trackOn("k4", 3, T[4] + 0.05); pop("#n4", T[4] + 0.05); pop("#f4", T[4] + 0.1);
      tl.fromTo("#f4 .armR", { rotation: 0 }, { rotation: -60, svgOrigin: "100 150", duration: 0.4, yoyo: true, repeat: 1 }, T[4] + 0.5);
      pop("#c4", at(4, 0.25)); pop("#dc4", at(4, 0.5));
      /* S5 · summary + disclaimer */
      add("s5", center("s5a", 60, `<span style="display:inline-block;vertical-align:middle">${svgI(iTab, 200)}</span><span style="font-family:Cap;font-weight:900;font-size:120px;vertical-align:middle"> = 25 L</span>`) + `<div id="s5b" class="abs label" style="left:60px;top:420px;width:960px;font-size:52px;color:${MUTED}">Results depend on the source water and correct use.</div>` + chipAt("s5c", 640, "FOLLOW THE INSTRUCTIONS", 56));
      tl.set(["#s5b", "#s5c"], { opacity: 0 }, T[5]);
      pop("#s5a", T[5] + 0.05); pop("#s5b", at(5, 0.35)); pop("#s5c", at(5, 0.75));

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
        json.dump({"id": f"historia-how-{lang}-{fmt}", "name": f"historia-how-{lang}-{fmt}"}, open(os.path.join(d, "meta.json"), "w"))
        link = os.path.join(d, "assets")
        if not os.path.islink(link):
            os.symlink("../assets", link)
    print(lang, "total", total, "T", T)


if __name__ == "__main__":
    for lang in ("en",):
        build(lang)
