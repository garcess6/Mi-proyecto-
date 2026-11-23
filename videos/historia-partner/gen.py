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
        "tag": "PARTNER · <b>AQUACORE</b>",
        "title": "Partner With Us",
        "locale": "en-US",
        "key": "partner|aquacore|safe|scale|ngos|governments|investors|volume|world|tablets|distribution|training|follow|restock|labs|cameroon|niger|coli|salmonella|cholera|pilot|country|communities",
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

      /* S0 · title */
      add("s0", center("t0r", 40, `<svg viewBox="0 0 160 160" width="340" height="340"><circle id="ra" cx="58" cy="80" r="44" fill="none" stroke="${INK}" stroke-width="10"/><circle id="rb" cx="102" cy="80" r="44" fill="none" stroke="${BLUE}" stroke-width="10"/></svg>`) + center("t0t", 420, `<div style="font-family:Cap;font-weight:900;font-size:104px;line-height:1">PARTNER<br>WITH <span style="color:${BLUE}">US</span></div>`) + chipAt("t0c", 720, "SAFE WATER, AT SCALE", 64));
      tl.set(["#t0t", "#t0c"], { opacity: 0 }, 0);
      tl.fromTo("#ra", { x: -200 }, { x: 0, duration: 0.6, ease: "back.out(1.6)" }, 0.05);
      tl.fromTo("#rb", { x: 200 }, { x: 0, duration: 0.6, ease: "back.out(1.6)" }, 0.05);
      pop("#t0t", at(0, 0.2)); pop("#t0c", at(0, 0.6), { rotation: -2 });
      /* S1 · who we work with */
      add("s1", card("c1a", 40, 30, 310, iNgo, "NGOs") + card("c1b", 385, 30, 310, iGov, "governments") + card("c1c", 730, 30, 310, iInv, "private investors", 170, 40) + chipAt("v1", 420, "VOLUME PROGRAMS", 64) + center("g1", 560, svgI(iGlobe, 300)) + `<div id="w1" class="abs label" style="left:0;top:880px;width:1080px;font-size:58px">all around the world</div>`);
      tl.set(["#c1a", "#c1b", "#c1c", "#v1", "#g1", "#w1"], { opacity: 0 }, T[1]);
      pop("#c1a", at(1, 0.08)); pop("#c1b", at(1, 0.18)); pop("#c1c", at(1, 0.3));
      pop("#v1", at(1, 0.5), { rotation: -2 }); pop("#g1", at(1, 0.7)); tl.fromTo("#g1 svg", { rotation: -25 }, { rotation: 25, duration: 1.6, ease: "sine.inOut", transformOrigin: "50% 50%" }, at(1, 0.7)); pop("#w1", at(1, 0.78));
      /* S2 · what we bring */
      const row = (id, top, n, ic, l) => `<div id="${id}" class="abs" style="left:60px;top:${top}px;width:960px;height:200px;display:flex;align-items:center;gap:30px"><div style="width:90px;height:90px;border-radius:45px;background:${BLUE};color:#fff;font-family:Cap;font-weight:900;font-size:48px;display:flex;align-items:center;justify-content:center;flex:none">${n}</div>${svgI(ic, 170)}<div class="label" style="text-align:left;font-size:60px">${l}</div></div>`;
      add("s2", row("w2a", 20, 1, iTab, "tablets at volume") + row("w2b", 260, 2, iTruck, "local distribution") + row("w2c", 500, 3, iPeople, "training for families") + row("w2d", 740, 4, iCycle, "monitor &amp; restock"));
      tl.set(["#w2a", "#w2b", "#w2c", "#w2d"], { opacity: 0 }, T[2]);
      [["#w2a", 0.12], ["#w2b", 0.32], ["#w2c", 0.55], ["#w2d", 0.78]].forEach(([r, f]) => tl.fromTo(r, { x: -150, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, at(2, f) - 0.15));
      /* S3 · lab tested */
      add("s3", chipAt("nl3", 20, "NATIONAL HEALTH LABS ✓", 56));
      const lab = (id, left, c, l) => `<div id="${id}" class="abs card" style="left:${left}px;top:150px;width:440px;padding:18px 10px">${svgI(iFlask, 120)}<div style="font-family:Cap;font-weight:900;font-size:50px">${c}</div><div class="small" style="font-size:34px;color:${MUTED}">${l}</div></div>`;
      add("s3", lab("lb3a", 60, "CAMEROON", "Centre Pasteur · 2012") + lab("lb3b", 580, "NIGER", "LANSPEX · 2017"));
      const vib = `<g><path d="M-30 10 C-30 -20 10 -30 30 -10" stroke="${INK}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-30 10 C-30 -20 10 -30 30 -10" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g>`;
      const gc = (id, left, art, name) => `<div id="${id}" class="abs" style="left:${left}px;top:560px;width:300px;text-align:center"><svg viewBox="-60 -50 120 100" width="220" height="180">${art}<g class="gx3" stroke="${BLUE}" stroke-width="10" stroke-linecap="round"><line x1="-45" y1="-40" x2="45" y2="40"/><line x1="45" y1="-40" x2="-45" y2="40"/></g></svg><div class="label" style="font-size:52px">${name}</div></div>`;
      add("s3", gc("g3a", 50, bacterium(0, 0, 1.4, ""), "E. coli") + gc("g3b", 390, bacterium(0, 0, 1.2, "").replace(/#1e7fd8/g, DIRT), "Salmonella") + gc("g3c", 730, vib, "cholera"));
      tl.set(["#nl3", "#lb3a", "#lb3b", "#g3a", "#g3b", "#g3c", ".gx3"], { opacity: 0 }, T[3]);
      pop("#nl3", T[3] + 0.05); pop("#lb3a", at(3, 0.25)); pop("#lb3b", at(3, 0.4));
      [["#g3a", 0.62], ["#g3b", 0.75], ["#g3c", 0.88]].forEach(([g, f]) => { pop(g, at(3, f) - 0.15); tl.fromTo(`${g} .gx3`, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.2, ease: "back.out(3)" }, at(3, f) + 0.1); });
      /* S4 · starts with a pilot */
      add("s4", center("pin4", 40, svgI(`<path d="M80 150 C80 150 30 96 30 64 a50 50 0 0 1 100 0 C130 96 80 150 80 150 Z" fill="${SKY}" stroke="${INK}" stroke-width="9"/><circle cx="80" cy="64" r="18" fill="${BLUE}"/>`, 300)) + chipAt("c4", 400, "IT STARTS WITH A PILOT", 64) + `<div id="s4b" class="abs" style="left:0;top:560px;width:1080px;text-align:center">${svgI(iBox, 200)}<span class="label" style="font-size:110px;vertical-align:top;line-height:200px;color:${BLUE}"> → </span>${svgI(iFlask, 200)}</div><div id="s4c" class="abs label" style="left:0;top:800px;width:1080px;font-size:56px">lab-tested in your own country</div>`);
      tl.set(["#c4", "#s4b", "#s4c"], { opacity: 0 }, T[4]);
      tl.fromTo("#pin4", { y: -400 }, { y: 0, duration: 0.5, ease: "bounce.out" }, T[4] + 0.05);
      pop("#c4", at(4, 0.2), { rotation: -2 }); pop("#s4b", at(4, 0.5)); pop("#s4c", at(4, 0.7));
      /* S5 · CTA */
      add("s5", center("cb5", 40, svgI(iChat, 300)) + `<div id="q5" class="abs" style="left:0;top:380px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:76px;line-height:1.05">Bring safe water<br>to your communities</div>` + chipAt("c5", 640, "DM US: PARTNER", 84, BLUE, -2) + `<div id="u5" class="abs" style="left:0;top:830px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:56px">aquacoreglobal.com</div>`);
      tl.set(["#q5", "#c5", "#u5"], { opacity: 0 }, T[5]);
      pop("#cb5", T[5] + 0.05); pop("#q5", at(5, 0.1)); pop("#c5", at(5, 0.5), { rotation: -2 }); pop("#u5", at(5, 0.8));

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
        json.dump({"id": f"historia-partner-{lang}-{fmt}", "name": f"historia-partner-{lang}-{fmt}"}, open(os.path.join(d, "meta.json"), "w"))
        link = os.path.join(d, "assets")
        if not os.path.islink(link):
            os.symlink("../assets", link)
    print(lang, "total", total, "T", T)


if __name__ == "__main__":
    for lang in ("en",):
        build(lang)
