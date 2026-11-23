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
        "tag": "ABOUT US · <b>AQUACORE</b>",
        "title": "About AquaCore",
        "locale": "en-US",
        "key": "aquacore|safe|see|clear|sick|millions|rivers|wells|rain|never|tested|simple|chlorine|dioxide|tablets|network|litre|tablet|thirty|minutes|ready|labs|coli|salmonella|cholera|ngos|governments|investors|worldwide|follow|prevention",
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
      const iRiver = `<path d="M10 120 Q50 100 80 120 T150 120 L150 150 L10 150 Z" fill="${SKY}" stroke="${BLUE}" stroke-width="7"/><path d="M20 90 L50 50 L80 90 Z M70 90 L105 40 L140 90 Z" fill="#fff" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>`;
      const iWell = `<g stroke="${INK}" stroke-width="7" fill="#fff" stroke-linejoin="round"><rect x="30" y="90" width="100" height="56"/><path d="M40 90 L40 40 M120 90 L120 40 M24 40 L136 40"/><path d="M80 40 L80 70"/><rect x="68" y="70" width="24" height="18" fill="${SKY}"/></g>`;
      const iRain = `<g stroke="${INK}" stroke-width="7" fill="#fff" stroke-linejoin="round"><path d="M40 90 a26 26 0 0 1 8 -50 a36 36 0 0 1 68 -6 a30 30 0 0 1 24 56 Z"/></g><g stroke="${BLUE}" stroke-width="7" stroke-linecap="round"><line x1="56" y1="108" x2="46" y2="134"/><line x1="86" y1="108" x2="76" y2="134"/><line x1="116" y1="108" x2="106" y2="134"/></g>`;
      const iNgo = `<path d="M80 140 C80 140 20 106 20 64 a30 30 0 0 1 60 -10 a30 30 0 0 1 60 10 C140 106 80 140 80 140Z" fill="#fff" stroke="${INK}" stroke-width="8"/>`;
      const iGov = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round"><path d="M16 56 L80 22 L144 56 Z"/><path d="M14 140 H146"/></g><path d="M34 66 V126 M64 66 V126 M96 66 V126 M126 66 V126" stroke="${BLUE}" stroke-width="8"/>`;
      const iInv = `<g stroke="${INK}" stroke-width="8" fill="none" stroke-linecap="round"><path d="M14 140 H146"/></g><path d="M22 116 L58 80 L82 100 L134 46 M106 46 H134 V74" stroke="${BLUE}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      const iGlobe = `<circle cx="80" cy="80" r="62" fill="${SKY}" stroke="${INK}" stroke-width="8"/><ellipse cx="80" cy="80" rx="26" ry="62" fill="none" stroke="${BLUE}" stroke-width="6"/><path d="M18 80 H142 M28 46 H132 M28 114 H132" stroke="${BLUE}" stroke-width="6" fill="none"/>`;
      const iBook = `<path d="M80 38 C64 26 38 26 18 32 V130 C38 124 64 124 80 136 C96 124 122 124 142 130 V32 C122 26 96 26 80 38 Z" fill="#fff" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/><path d="M80 38 V136" stroke="${BLUE}" stroke-width="7"/>`;
      const card = (id, left, top, w, icon, label, isz = 170, fs = 46) => `<div id="${id}" class="abs card" style="left:${left}px;top:${top}px;width:${w}px;padding:16px 10px"><svg viewBox="0 0 160 160" width="${isz}" height="${isz}">${icon}</svg><div class="label" style="font-size:${fs}px;line-height:1.05">${label}</div></div>`;
      const chipAt = (id, top, html, size = 60, bg = BLUE, rot = 0) => `<div id="${id}" class="abs" style="left:0;top:${top}px;width:1080px;text-align:center"><span class="chip" style="font-size:${size}px;background:${bg};display:inline-block;transform:rotate(${rot}deg)">${html}</span></div>`;

      /* ================= S0 · we're AquaCore ================= */
      add("s0", `<div id="lg0" class="abs" style="left:0;top:10px;width:1080px;text-align:center"><svg viewBox="0 0 160 160" width="210" height="210">${iAqua}</svg><div style="font-family:Cap;font-weight:900;font-size:104px;letter-spacing:0.04em;margin-top:-8px">AQUA<span style="color:${BLUE}">CORE</span></div></div>`);
      add("s0", glass("g0", { left: 390, top: 420, w: 300, extra: `<g id="gm0">${bacterium(60, 120, 0.7, "")}${virus(105, 160, 0.6, "")}${parasite(80, 190, 0.5, "")}</g>` }));
      add("s0", `<div id="ln0" class="abs" style="left:380px;top:470px;width:320px;height:320px"><svg viewBox="0 0 300 300" width="320" height="320"><circle cx="140" cy="140" r="115" fill="none" stroke="${INK}" stroke-width="14"/><line x1="222" y1="222" x2="290" y2="290" stroke="${INK}" stroke-width="22" stroke-linecap="round"/></svg></div>`);
      tl.set(["#g0", "#gm0", "#ln0"], { opacity: 0 }, 0);
      tl.fromTo("#lg0", { scale: 2.2, opacity: 0, transformOrigin: "50% 30%" }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 0.05);
      tl.fromTo("#s0 .cam", focus(540, 200, 1.3), { ...focus(540, 480, 1.0), duration: 1.2, ease: "power2.inOut" }, at(0, 0.3));
      pop("#g0", at(0, 0.35));
      tl.fromTo("#ln0", { x: -420, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "power2.out" }, at(0, 0.6));
      tl.to("#gm0", { opacity: 1, duration: 0.15 }, at(0, 0.75));
      wiggle("#gm0 .wig", at(0, 0.75), 1.0);

      /* ================= S1 · clear but unsafe; never tested ================= */
      add("s1", glass("g1", { left: 170, top: 40, w: 260, extra: `<g id="gm1">${bacterium(60, 130, 0.6, "")}${virus(100, 175, 0.5, "")}</g>` }));
      add("s1", `<div id="cl1" class="abs" style="left:120px;top:420px;width:360px;text-align:center"><span class="chip" style="font-size:44px">CLEAR ✓</span></div>`);
      add("s1", figure("f1", { left: 620, top: 40, w: 220, face: "smile" }));
      add("s1", `<div id="sk1" class="abs" style="left:560px;top:430px;width:360px;text-align:center"><span class="chip" style="font-size:44px;background:${RED}">SICK ✗</span></div>`);
      add("s1", card("c1a", 40, 560, 310, iRiver, "rivers") + card("c1b", 385, 560, 310, iWell, "wells") + card("c1c", 730, 560, 310, iRain, "rain tanks"));
      add("s1", chipAt("nt1", 900, "NEVER TESTED OR TREATED", 54, RED, -3));
      tl.set(["#g1", "#cl1", "#f1", "#sk1", "#c1a", "#c1b", "#c1c", "#nt1", "#gm1"], { opacity: 0 }, T[1]);
      tl.fromTo("#s1 .cam", focus(540, 280, 1.25), { ...focus(540, 300, 1.2), duration: 1.4, ease: "none" }, T[1]);
      pop("#g1", T[1] + 0.05); pop("#cl1", at(1, 0.12));
      tl.to("#gm1", { opacity: 1, duration: 0.2 }, at(1, 0.2)); wiggle("#gm1 .wig", at(1, 0.2), 1.5);
      pop("#f1", at(1, 0.18)); setFace(tl, "f1", "sick", at(1, 0.28)); pop("#sk1", at(1, 0.28));
      tl.to("#s1 .cam", { ...focus(540, 560, 1.0), duration: 0.6, ease: "power2.inOut" }, at(1, 0.4));
      pop("#c1a", at(1, 0.6)); pop("#c1b", at(1, 0.68)); pop("#c1c", at(1, 0.76));
      tl.fromTo("#nt1", { scale: 2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, at(1, 0.86));

      /* ================= S2 · tablets + local network ================= */
      add("s2", `<div id="tb2" class="abs" style="left:0;top:20px;width:1080px;text-align:center"><svg viewBox="0 0 160 160" width="300" height="300"><path d="M18 70 V92 A62 24 0 0 0 142 92 V70" fill="${SKY}" stroke="${INK}" stroke-width="8"/><ellipse cx="80" cy="70" rx="62" ry="24" fill="#fff" stroke="${INK}" stroke-width="8"/><line x1="46" y1="70" x2="114" y2="70" stroke="${BLUE}" stroke-width="7" stroke-linecap="round"/></svg></div>`);
      add("s2", chipAt("cl2", 300, "ClO₂ · chlorine dioxide", 54));
      const house = (x) => `<g class="hs2" transform="translate(${x} 0)"><path d="M0 60 L50 20 L100 60 L100 130 L0 130 Z" fill="#fff" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/><rect x="38" y="88" width="24" height="42" fill="${SKY}" stroke="${INK}" stroke-width="5"/></g>`;
      add("s2", `<svg class="abs" style="left:0;top:0" width="1080" height="1080"><g transform="translate(30 820)">${[0, 210, 420, 630, 840].map(house).join("")}</g>
        <g id="tr2"><g transform="translate(60 560) scale(3)" fill="#fff" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"><rect x="10" y="32" width="50" height="34" rx="4"/><path d="M60 42 H76 L88 54 V66 H60 Z"/><circle cx="28" cy="72" r="7"/><circle cx="72" cy="72" r="7"/><circle cx="28" cy="48" r="7" fill="${SKY}"/><circle cx="44" cy="48" r="7" fill="${SKY}"/></g></g></svg>`);
      add("s2", `<div id="ln2" class="abs label" style="left:560px;top:600px;width:480px;opacity:0;color:${BLUE}">local network</div>`);
      tl.set(["#cl2", ".hs2", "#tr2"], { opacity: 0 }, T[2]);
      tl.fromTo("#tb2", { y: -300, rotation: -90, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }, T[2] + 0.05);
      tl.fromTo("#s2 .cam", focus(540, 200, 1.3), { ...focus(540, 520, 1.0), duration: 1.4, ease: "power2.inOut" }, at(2, 0.35));
      pop("#cl2", at(2, 0.25));
      tl.to(".hs2", { opacity: 1, duration: 0.1, stagger: 0.08 }, at(2, 0.55));
      tl.set("#tr2", { opacity: 1 }, at(2, 0.6));
      tl.fromTo("#tr2", { x: -700 }, { x: 0, duration: 0.8, ease: "power2.out" }, at(2, 0.6));
      pop("#ln2", at(2, 0.8));

      /* ================= S3 · 4 steps ================= */
      const can = `<svg viewBox="0 0 200 230" width="300" height="345"><defs><clipPath id="cc3"><path d="M34 64 L166 64 L166 214 L34 214 Z"/></clipPath></defs><g clip-path="url(#cc3)"><rect id="wf3" x="30" y="214" width="140" height="160" fill="${SKY}"/></g><path d="M30 60 L170 60 L170 215 Q170 225 160 225 L40 225 Q30 225 30 215 Z" fill="none" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/><path d="M70 60 L70 30 L130 30 L130 60" fill="#fff" stroke="${INK}" stroke-width="8"/><text x="100" y="170" text-anchor="middle" font-family="Cap" font-weight="900" font-size="40" fill="${INK}">25 L</text></svg>`;
      let fz = ""; for (let i = 0; i < 7; i++) fz += `<circle class="fz3" cx="${150 + rnd() * 160}" cy="560" r="${7 + rnd() * 6}" fill="#fff" stroke="${BLUE}" stroke-width="4"/>`;
      add("s3", `<div class="abs" style="left:60px;top:40px;width:960px;display:flex;gap:12px">${["FILL", "ADD", "WAIT", "READY"].map((l, k) => `<div style="flex:1"><div id="sg3_${k}" style="height:16px;border-radius:8px;background:#d5dee8"></div><div style="font-family:Cap;font-weight:900;font-size:30px;margin-top:8px">${l}</div></div>`).join("")}</div>`);
      add("s3", `<div id="cn3" class="abs" style="left:90px;top:300px">${can}</div>`);
      add("s3", `<svg class="abs" style="left:0;top:0" width="1080" height="1080"><g id="tb3"><circle cx="240" cy="150" r="34" fill="#fff" stroke="${INK}" stroke-width="7"/><line x1="216" y1="150" x2="264" y2="150" stroke="${INK}" stroke-width="7"/></g>${fz}</svg>`);
      add("s3", `<div id="ck3" class="abs" style="left:560px;top:260px;width:380px;text-align:center"><svg viewBox="0 0 160 160" width="240" height="240">${iClock}<line id="hd3" x1="80" y1="80" x2="80" y2="34" stroke="${BLUE}" stroke-width="9" stroke-linecap="round"/></svg><div class="chip" style="display:inline-block;font-size:50px">30 MIN</div></div>`);
      add("s3", figure("f3", { left: 660, top: 250, w: 200, prop: "glass", face: "smile" }));
      add("s3", `<div id="rd3" class="abs" style="left:520px;top:640px;width:480px;text-align:center"><span class="chip" style="font-size:48px">READY ✓</span></div>`);
      tl.set(["#tb3", ".fz3", "#ck3", "#f3", "#rd3"], { opacity: 0 }, T[3]);
      tl.fromTo("#s3 .cam", focus(540, 540, 1.04), { ...focus(540, 540, 1.0), duration: 4, ease: "none" }, T[3]);
      const seg = (k, t) => tl.to(`#sg3_${k}`, { backgroundColor: BLUE, duration: 0.2 }, t);
      seg(0, T[3] + 0.1); tl.fromTo("#wf3", { attr: { y: 214 } }, { attr: { y: 90 }, duration: 0.9, ease: "power1.out" }, T[3] + 0.1);
      seg(1, at(3, 0.3)); tl.set("#tb3", { opacity: 1 }, at(3, 0.3)); tl.fromTo("#tb3", { y: 0 }, { y: 300, duration: 0.45, ease: "power2.in" }, at(3, 0.3)); tl.to("#tb3", { opacity: 0, duration: 0.1 }, at(3, 0.3) + 0.45);
      tl.fromTo(".fz3", { y: 0, opacity: 0 }, { y: -110, opacity: 1, duration: 0.5, stagger: { each: 0.08, repeat: 3 } }, at(3, 0.3) + 0.45);
      seg(2, at(3, 0.5)); pop("#ck3", at(3, 0.5)); tl.fromTo("#hd3", { rotation: 0 }, { rotation: 360, svgOrigin: "80 80", duration: 1.0, ease: "none" }, at(3, 0.52));
      seg(3, at(3, 0.75)); tl.to("#ck3", { opacity: 0, scale: 0.6, duration: 0.2 }, at(3, 0.72)); pop("#f3", at(3, 0.75)); pop("#rd3", at(3, 0.82));

      /* ================= S4 · lab tested ================= */
      add("s4", chipAt("nl4", 20, "NATIONAL HEALTH LABS ✓", 56));
      const lab = (id, left, c, l) => `<div id="${id}" class="abs card" style="left:${left}px;top:150px;width:440px;padding:18px 10px"><svg viewBox="0 0 160 160" width="120" height="120">${iFlask}</svg><div style="font-family:Cap;font-weight:900;font-size:50px">${c}</div><div class="small" style="font-size:34px;color:${MUTED}">${l}</div></div>`;
      add("s4", lab("lb4a", 60, "CAMEROON", "Centre Pasteur · 2012") + lab("lb4b", 580, "NIGER", "LANSPEX · 2017"));
      const vib = `<g><path d="M-30 10 C-30 -20 10 -30 30 -10" stroke="${INK}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-30 10 C-30 -20 10 -30 30 -10" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g>`;
      const gc = (id, left, art, name) => `<div id="${id}" class="abs" style="left:${left}px;top:560px;width:300px;text-align:center"><svg viewBox="-60 -50 120 100" width="220" height="180">${art}<g class="gx4" stroke="${BLUE}" stroke-width="10" stroke-linecap="round"><line x1="-45" y1="-40" x2="45" y2="40"/><line x1="45" y1="-40" x2="-45" y2="40"/></g></svg><div class="label" style="font-size:52px">${name}</div></div>`;
      add("s4", gc("g4a", 50, bacterium(0, 0, 1.4, ""), "E. coli") + gc("g4b", 390, bacterium(0, 0, 1.2, "").replace(/#1e7fd8/g, DIRT), "Salmonella") + gc("g4c", 730, vib, "cholera"));
      tl.set(["#nl4", "#lb4a", "#lb4b", "#g4a", "#g4b", "#g4c", ".gx4"], { opacity: 0 }, T[4]);
      tl.fromTo("#s4 .cam", focus(540, 480, 1.05), { ...focus(540, 500, 1.0), duration: 3, ease: "none" }, T[4]);
      pop("#nl4", T[4] + 0.05); pop("#lb4a", at(4, 0.15)); pop("#lb4b", at(4, 0.3));
      [["#g4a", 0.6], ["#g4b", 0.72], ["#g4c", 0.86]].forEach(([g, f]) => { pop(g, at(4, f) - 0.15); tl.fromTo(`${g} .gx4`, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.2, ease: "back.out(3)" }, at(4, f) + 0.1); });

      /* ================= S5 · who we work with ================= */
      add("s5", card("c5a", 40, 40, 310, iNgo, "NGOs") + card("c5b", 385, 40, 310, iGov, "governments") + card("c5c", 730, 40, 310, iInv, "investors"));
      add("s5", `<div id="gl5" class="abs" style="left:0;top:420px;width:1080px;text-align:center"><svg viewBox="0 0 160 160" width="330" height="330">${iGlobe}</svg></div>` + chipAt("ww5", 790, "WORLDWIDE", 70));
      tl.set(["#c5a", "#c5b", "#c5c", "#gl5", "#ww5"], { opacity: 0 }, T[5]);
      pop("#c5a", at(5, 0.15)); pop("#c5b", at(5, 0.3)); pop("#c5c", at(5, 0.55));
      pop("#gl5", at(5, 0.7)); tl.fromTo("#gl5 svg", { rotation: -20 }, { rotation: 20, duration: 1.5, ease: "sine.inOut", transformOrigin: "50% 50%" }, at(5, 0.7)); pop("#ww5", at(5, 0.8));

      /* ================= S6 · follow ================= */
      add("s6", `<div id="bk6" class="abs" style="left:0;top:40px;width:1080px;text-align:center"><svg viewBox="0 0 160 160" width="300" height="300">${iBook}</svg></div>`);
      add("s6", `<div id="pv6" class="abs label" style="left:40px;top:380px;width:1000px;font-size:64px">the water we drink · why <span style="color:${BLUE}">prevention</span> matters</div>`);
      add("s6", chipAt("fw6", 620, "FOLLOW FOR MORE", 90, BLUE, -2) + `<div id="hd6" class="abs" style="left:0;top:800px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:60px">@aquacoreglobal</div>`);
      tl.set(["#bk6", "#pv6", "#fw6", "#hd6"], { opacity: 0 }, T[6]);
      pop("#bk6", T[6] + 0.05); pop("#pv6", at(6, 0.3)); pop("#fw6", at(6, 0.05) + 0.1, { rotation: -2 }); pop("#hd6", at(6, 0.5));

      /* ================= S7 · end card ================= */
      add("s7", `<div class="abs" style="left:0;top:120px;width:1080px;text-align:center"><img id="logo" src="assets/logo.png" style="width:420px;height:420px" /><div id="e2" style="font-family:Cap;font-weight:900;font-size:60px;margin-top:20px">aquacoreglobal.com</div></div>`);
      pop("#logo", T[7] + 0.05);
      tl.fromTo("#e2", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35 }, T[7] + 0.3);

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
        json.dump({"id": f"historia-about-{lang}-{fmt}", "name": f"historia-about-{lang}-{fmt}"}, open(os.path.join(d, "meta.json"), "w"))
        link = os.path.join(d, "assets")
        if not os.path.islink(link):
            os.symlink("../assets", link)
    print(lang, "total", total, "T", T)


if __name__ == "__main__":
    for lang in ("en",):
        build(lang)
