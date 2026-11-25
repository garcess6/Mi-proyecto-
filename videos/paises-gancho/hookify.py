#!/usr/bin/env python3
"""Turn a country gen.py into gen_hook.py: spoken hook first + guide presenter with pointing finger.

Usage: python3 hookify.py <country>   (cod | eth | nga)
"""
import json, os, re, sys

C = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "videos", f"pais-{C}")
CHOL = os.path.join(HERE, "..", "colera", "sp01-colera", "index.html")
src = open(os.path.join(D, "gen.py")).read()
HOOKS = json.load(open(os.path.join(HERE, "hooks.json")))[C]

# ---------- hook visuals per country (text per language) ----------
HK = {
    "cod": {
        "en": dict(num=1300, suf="+", label="cholera deaths", chip="IN JUST 7 MONTHS", chip2="IT STARTS WITH WATER", src="Source: WHO Disease Outbreak News, Aug 2025", wChip="months", wWater="water", key="thirteen|hundred|deaths|seven|months|cholera|congo|2025|water"),
        "fr": dict(num=1300, suf="+", label="décès dus au choléra", chip="EN SEULEMENT 7 MOIS", chip2="TOUT COMMENCE PAR L'EAU", src="Source : OMS, Disease Outbreak News, août 2025", wChip="mois", wWater="boit", key="mille|trois|cents|morts|sept|mois|cholra|congo|eau|boit"),
    },
    "eth": {
        "en": dict(num=27000, suf="+", label="cholera cases in one year", chip="OUTBREAK SINCE 2023", chip2="IT STARTS WITH WATER", src="Source: WHO, 2024 data", wChip="since", wWater="water", key="twentyseven|thousand|cholera|cases|year|ethiopia|outbreak|2023|water"),
    },
    "nga": {
        "en": dict(num=3, suf=" in 100", label="people who caught cholera died", chip="NIGERIA · 2024", chip2="WATER THAT LOOKS CLEAN", src="Source: WHO WER 2025 (2024 data)", wChip="nigeria", wWater="clean", key="2024|three|hundred|cholera|nigeria|died|water|clean"),
    },
}[C]

# ---------- guide positions per scene: [x, y, base face, [[tx, ty, frac], ...]] ----------
GCFG = {
    "cod": [
        [40, 330, "worry", [[540, 700, 0.08], [540, 910, 0.62]]],
        [40, 560, "worry", [[540, 360, 0.12], [520, 680, 0.6], [840, 640, 0.68]]],
        [930, 830, "worry", [[195, 160, 0.06], [280, 590, 0.3], [700, 560, 0.56], [700, 700, 0.74]]],
        [40, 790, "hmm", [[195, 180, 0.16], [540, 180, 0.3], [885, 180, 0.42], [540, 610, 0.66]]],
        [930, 840, "hmm", [[120, 270, 0.3], [120, 500, 0.55], [120, 730, 0.75]]],
        [60, 40, "smile", [[285, 430, 0.2], [795, 430, 0.36], [285, 660, 0.5], [795, 660, 0.66]]],
        [930, 10, "smile", [[100, 205, 0.2], [100, 370, 0.36], [100, 535, 0.58], [100, 700, 0.78], [100, 865, 0.9]]],
        [60, 160, "smile", [[540, 220, 0.05], [540, 700, 0.55]]],
    ],
    "eth": [
        [40, 330, "worry", [[540, 700, 0.08], [540, 910, 0.62]]],
        [40, 560, "worry", [[540, 360, 0.12], [520, 680, 0.75], [840, 640, 0.68]]],
        [930, 830, "worry", [[195, 160, 0.06], [700, 470, 0.5], [700, 620, 0.66], [700, 380, 0.86]]],
        [40, 790, "hmm", [[540, 610, 0.1], [195, 180, 0.42], [540, 180, 0.52], [885, 180, 0.64]]],
        [930, 840, "hmm", [[120, 270, 0.3], [120, 500, 0.55], [120, 730, 0.75]]],
        [60, 40, "smile", [[285, 430, 0.2], [795, 430, 0.36], [285, 660, 0.5], [795, 660, 0.66]]],
        [930, 10, "smile", [[100, 205, 0.2], [100, 370, 0.36], [100, 535, 0.58], [100, 700, 0.78], [100, 865, 0.9]]],
        [60, 160, "smile", [[540, 220, 0.05], [540, 700, 0.55]]],
    ],
    "nga": [
        [930, 600, "smile", [[540, 900, 0.05]]],
        [40, 300, "worry", [[540, 670, 0.12], [540, 890, 0.72]]],
        [950, 720, "hmm", [[250, 95, 0.05], [880, 500, 0.3], [540, 875, 0.75]]],
        [920, 640, "worry", [[700, 350, 0.1], [700, 500, 0.42], [300, 560, 0.8]]],
        [475, 640, "hmm", [[195, 370, 0.4], [540, 370, 0.55], [885, 370, 0.72]]],
        [60, 120, "worry", [[270, 640, 0.5], [810, 640, 0.8]]],
        [40, 520, "smile", [[210, 350, 0.08], [860, 360, 0.4], [540, 670, 0.6]]],
        [930, 10, "smile", [[100, 205, 0.2], [100, 370, 0.38], [100, 535, 0.62], [100, 700, 0.78], [100, 865, 0.9]]],
        [60, 40, "smile", [[540, 360, 0.08], [540, 600, 0.55]]],
    ],
}[C]

chol = open(CHOL).read()
ga = chol.index("      /* ================= GUIDE"); gb = chol.index("      // S0 hook", ga)
GUIDE_FNS = chol[ga:gb].replace("const nx = tx - 33, ny = ty + 4;", "const nx = tx - 33, ny = ty + 58;")

HOOK_JS = r'''
      /* ================= HOOK scene (sh): the most striking fact first ================= */
      const HK = __HK__;
      const GCFG = __GCFG__;
      add("sh", `<div id="hn" class="abs" style="left:0;top:40px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:190px;line-height:1;color:${RED}">0</div>`);
      add("sh", `<div id="hl" class="abs label" style="left:40px;top:250px;width:1000px;font-size:58px">${HK.label}</div>`);
      add("sh", `<div id="hc" class="abs" style="left:0;top:340px;width:1080px;text-align:center"><span class="chip" style="font-size:56px;background:${INK}">${HK.chip}</span></div>`);
      let hdots = ""; MAP.pts.forEach((p, i) => { if (i % 4 === 0) hdots += `<circle class="hd" cx="${p[0]}" cy="${p[1]}" r="11" fill="${RED}" stroke="${INK}" stroke-width="3"/>`; });
      add("sh", `<div id="hm" class="abs" style="left:300px;top:450px">${mapSvg("hmap", 480, hdots)}</div>`);
      add("sh", glass("hg", { left: 420, top: 470, w: 240, extra: `<g id="hgm">${bacterium(60, 120, 0.7, "")}${virus(100, 170, 0.55, "")}${bacterium(110, 100, 0.5, "")}</g>` }));
      add("sh", `<div id="hc2" class="abs" style="left:0;top:830px;width:1080px;text-align:center"><span class="chip" style="font-size:60px">${HK.chip2}</span></div>`);
      add("sh", `<div id="hsrc" class="abs" style="left:0;top:985px;width:1080px;text-align:center;font-family:Cap;font-weight:800;font-size:28px;color:${MUTED}">${HK.src}</div>`);
      tl.set(["#hl", "#hc", "#hm", ".hd", "#hg", "#hc2", "#hsrc"], { opacity: 0 }, 0);
      tl.fromTo("#sh .cam", focus(540, 300, 1.15), { ...focus(540, 520, 1.0), duration: 2.4, ease: "power2.inOut" }, 0);
      tl.fromTo("#hn", { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.5)" }, 0.05);
      { const o = { v: 0 }; tl.to(o, { v: HK.num, duration: 1.3, ease: "power2.out", onUpdate: () => { document.getElementById("hn").textContent = Math.round(o.v).toLocaleString(TX.locale || "en-US") + HK.suf; } }, 0.1); }
      tl.fromTo("#hn", { x: 0 }, { x: 8, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }, 1.4);
      pop("#hl", 0.6); tl.to("#hsrc", { opacity: 1, duration: 0.3 }, 0.8);
      tl.fromTo("#hc", { scale: 1.7, opacity: 0, rotation: -3 }, { scale: 1, opacity: 1, rotation: -3, duration: 0.3, ease: "back.out(2.5)" }, W(0, HK.wChip) - 0.15);
      pop("#hm", W(0, HK.wChip) + 0.2);
      tl.to(".hd", { opacity: 1, duration: 0.05, stagger: { each: 0.025, from: "random" } }, W(0, HK.wChip) + 0.4);
      tl.to("#hm", { opacity: 0, duration: 0.25 }, W(0, HK.wWater) - 0.5);
      pop("#hg", W(0, HK.wWater) - 0.3); wiggle("#hgm .wig", W(0, HK.wWater), 1.2);
      tl.fromTo("#hc2", { scale: 1.7, opacity: 0, rotation: 2 }, { scale: 1, opacity: 1, rotation: 2, duration: 0.3, ease: "back.out(2.5)" }, W(0, HK.wWater) - 0.1);

''' + GUIDE_FNS + r'''
      // hook scene guide
      gAt(900, 600, 0, "worry"); gTalk(0);
      gPoint(540, 170, 0.3);
      gPoint(540, 380, W(0, HK.wChip));
      gPoint(540, 640, W(0, HK.wWater) - 0.2);
      // story scenes
      GCFG.forEach(([x, y, base, pts], k) => {
        if (k + 1 >= LINES.length) return;
        gAt(x, y, T[k], base); gTalk(k + 1);
        pts.forEach(([tx, ty, f]) => gPoint(tx, ty, at(k, f) - 0.15));
      });
      // end card: hide finger, wave
      { const te = T[T.length - 2];
        gHideFinger(te - 0.15);
        gAt(475, 745, te, "smile");
        tl.fromTo("#guide .armR", { rotation: 0 }, { rotation: -150, svgOrigin: "100 150", duration: 0.3 }, te + 0.2);
        tl.fromTo("#guide .armR", { rotation: -150 }, { rotation: -110, svgOrigin: "100 150", duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }, te + 0.5); }
'''


def rep(a, b, s, cnt=1):
    assert s.count(a) == cnt, (a[:100], s.count(a))
    return s.replace(a, b)


s = src
# hook + guide go at the end of SCENES
end = s.index("\n'''\n", s.index("SCENES = r'''"))
s = s[:end] + "\n" + HOOK_JS.replace("__GCFG__", json.dumps(GCFG)) + s[end:]
# at() now skips the hook line
s = rep("const at = (li, f) => LINES[li][0] + LINES[li][1] * f;", "const at = (li, f) => LINES[li + 1][0] + LINES[li + 1][1] * f;", s)
# S0 literal times -> T[0]
a = s.index("S0 ·"); b = s.index("S1 ·", a)
blk = s[a:b]
blk = re.sub(r"\}, 0\);", "}, T[0]);", blk)
blk = re.sub(r"\}, 0\.(\d)\);", r"}, T[0] + 0.\1);", blk)
blk = blk.replace('pop("#tm0", 0.1)', 'pop("#tm0", T[0] + 0.1)')
s = s[:a] + blk + s[b:]

# build(): prepend hook line + wav
s = rep("    lines = [l.strip() for l in open(os.path.join(HERE, \"assets\", f\"lines_{lang}.txt\")) if l.strip()]\n",
        "    lines = [HOOKS[lang]] + [l.strip() for l in open(os.path.join(HERE, \"assets\", f\"lines_{lang}.txt\")) if l.strip()]\n", s)
s = rep("    durs = [dur(os.path.join(HERE, \"assets\", f\"vo_{lang}\", f\"l{i+1}.wav\")) for i in range(len(lines))]\n",
        "    durs = [dur(VOF(lang, i)) for i in range(len(lines))]\n", s)
s = rep("        inputs += [\"-i\", os.path.join(HERE, \"assets\", f\"vo_{lang}\", f\"l{i+1}.wav\")]\n",
        "        inputs += [\"-i\", VOF(lang, i)]\n", s)
s = rep("os.path.join(HERE, \"assets\", f\"voice_{lang}.wav\")], check=True)", "os.path.join(HERE, \"assets\", f\"voiceh_{lang}.wav\")], check=True)", s)
s = rep("s = s.replace('src=\"assets/voice.wav\"', f'src=\"assets/voice_{lang}.wav\"')", "s = s.replace('src=\"assets/voice.wav\"', f'src=\"assets/voiceh_{lang}.wav\"')", s)
s = rep('.replace("__T__", json.dumps(T))', '.replace("__T__", json.dumps(T[1:])).replace("__HK__", json.dumps(HK[lang], ensure_ascii=False))', s)
# scene divs: hook scene + shifted story scenes + guide layer
old_div = """    s = s[:sa] + "".join(f'        <div id="s{k}" class="scene clip" data-start="{T[k]}" data-duration="{round(T[k+1]-T[k],2)}" data-track-index="1"><div class="cam"></div></div>\\n' for k in range(len(T) - 1)) + s[sb:]"""
new_div = """    s = s[:sa] + f'        <div id="sh" class="scene clip" data-start="0" data-duration="{T[1]}" data-track-index="1"><div class="cam"></div></div>\\n' + "".join(f'        <div id="s{k}" class="scene clip" data-start="{T[k+1]}" data-duration="{round(T[k+2]-T[k+1],2)}" data-track-index="1"><div class="cam"></div></div>\\n' for k in range(len(T) - 2)) + '        <div id="guideLayer" class="abs" style="left:0;top:0;width:1080px;height:1080px;z-index:5"></div>\\n' + s[sb:]"""
s = rep(old_div, new_div, s)
s = rep("s = re.sub(r\"const KEY = /\\^\\(.*?\\)\\$/i;\", f\"const KEY = /^({tx['key']})$/i;\", s)",
        "s = re.sub(r\"const KEY = /\\^\\(.*?\\)\\$/i;\", f\"const KEY = /^({HK[lang]['key']}|{tx['key']})$/i;\", s)", s)
# output into new folders so the originals stay untouched
s = s.replace('d = os.path.join(HERE, f"{lang}-{fmt}")', 'd = os.path.join(HERE, f"hook-{lang}-{fmt}")')
# helpers
helpers = f'''
HOOKS = {json.dumps(HOOKS, ensure_ascii=False)}
HK = {json.dumps(HK, ensure_ascii=False)}


def VOF(lang, i):
    return os.path.join(HERE, "assets", f"vo_{{lang}}", "h0.wav" if i == 0 else f"l{{i}}.wav")

'''
s = s.replace("\ndef dur(f):", helpers + "\ndef dur(f):", 1)
open(os.path.join(D, "gen_hook.py"), "w").write(s)
print("wrote", os.path.join(D, "gen_hook.py"))
