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
        "tag": "COUNTRY FOCUS · <b>NIGERIA</b>",
        "title": "Nigeria Water",
        "locale": "en-US",
        "key": "amina|sunrise|water|million|nigerians|safe|seven|well|clean|clear|germs|cholera|thousand|deaths|hundred|died|control|testing|vaccination|fuel|filters|aquacore|tablet|litre|minutes|children|labs|coli|salmonella|pilot|scale",
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

      const MAP = __MAP__;
      const mapSvg = (id, w, extra = "") => `<svg id="${id}" viewBox="0 0 ${MAP.w} ${MAP.h}" width="${w}" height="${w}"><path d="${MAP.d}" fill="${SKY}" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>${extra}</svg>`;
      const fmt = (v) => Math.round(v).toLocaleString("en-US");
      const counter = (id, to, t, dur, suffix = "") => { const o = { v: 0 }; tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { document.getElementById(id).textContent = fmt(o.v) + suffix; } }, t); };
      const srcLine = (id, text) => `<div id="${id}" class="abs" style="left:0;top:950px;width:1080px;text-align:center;font-family:Cap;font-weight:800;font-size:28px;color:${MUTED}">${text}</div>`;
      const ORANGE = "#f2994a";
      // Amina = stick figure + headwrap + skirt overlay (same 200x360 viewBox as figure())
      const amina = (id, left, top, w, face = "smile", prop = "") => figure(id, { left, top, w, face, prop }) +
        `<svg id="${id}_o" class="abs" style="left:${left}px;top:${top}px" viewBox="0 0 200 360" width="${w}" height="${w * 1.8}"><path d="M54 66 Q100 4 146 66 Q100 44 54 66 Z" fill="${ORANGE}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><path d="M100 196 L56 286 L144 286 Z" fill="${ORANGE}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/></svg>`;
      const iCanS = `<g stroke="${INK}" stroke-width="8" stroke-linejoin="round"><path d="M34 50 L126 50 L126 146 L34 146 Z" fill="${SKY}"/><path d="M62 50 L62 30 L98 30 L98 50" fill="#fff"/></g>`;
      const iWell = `<g stroke="${INK}" stroke-width="7" fill="#fff" stroke-linejoin="round"><rect x="30" y="90" width="100" height="56"/><path d="M40 90 L40 40 M120 90 L120 40 M24 40 L136 40"/><path d="M80 40 L80 70"/><rect x="68" y="70" width="24" height="18" fill="${SKY}"/></g>`;
      const iPlan = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round"><rect x="34" y="24" width="92" height="120" rx="8"/><rect x="58" y="14" width="44" height="22" rx="6" fill="${SKY}"/></g><path d="M52 64 H108 M52 88 H108 M52 112 H88" stroke="${BLUE}" stroke-width="8" stroke-linecap="round"/>`;
      const iSyr = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linecap="round" stroke-linejoin="round"><rect x="40" y="56" width="80" height="34" rx="6" transform="rotate(-35 80 73)"/><path d="M114 40 L138 22 M126 32 L136 44 M44 104 L22 128"/></g><rect x="52" y="62" width="40" height="22" fill="${BLUE}" transform="rotate(-35 80 73)"/>`;
      const iPot = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round" stroke-linecap="round"><path d="M20 70 L140 70 L130 140 L30 140 Z"/><path d="M8 70 L152 70"/></g>`;
      const iFilter = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round"><path d="M20 30 L140 30 L100 90 L100 140 L60 140 L60 90 Z"/><path d="M36 54 L124 54" stroke="#8a7660" stroke-width="12"/></g>`;
      const cross = `<g stroke="${RED}" stroke-width="14" stroke-linecap="round"><line x1="24" y1="24" x2="136" y2="136"/><line x1="136" y1="24" x2="24" y2="136"/></g>`;

      /* S0 · sunrise walk */
      add("s0", `<svg class="abs" style="left:0;top:0" width="1080" height="1080"><circle id="sun0" cx="820" cy="560" r="90" fill="#ffd34d" stroke="${INK}" stroke-width="7"/><rect x="0" y="560" width="1080" height="520" fill="#fff"/><path d="M0 560 H1080" stroke="${INK}" stroke-width="8"/><path d="M0 700 Q300 670 540 700 T1080 690" stroke="#8a7660" stroke-width="10" stroke-dasharray="26 16" fill="none"/></svg>`);
      add("s0", `<div id="am0w" class="abs" style="left:0;top:0;width:1080px;height:1080px">${amina("am0", 120, 360, 200, "smile")}<div class="abs" style="left:290px;top:560px">${svgI(iCanS, 110)}</div></div>`);
      add("s0", `<div id="tm0" class="abs" style="left:60px;top:40px"><span class="chip" style="font-size:44px">5:30 AM</span></div><div id="il0" class="abs" style="left:640px;top:50px;font-family:Hand;font-size:34px;color:${MUTED}">illustrative story</div>`);
      add("s0", `<div id="nm0" class="abs" style="left:0;top:860px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:90px">MEET <span style="color:${ORANGE}">AMINA</span></div>`);
      tl.set(["#nm0"], { opacity: 0 }, 0);
      tl.fromTo("#sun0", { y: 160 }, { y: -180, duration: 4.5, ease: "power1.out" }, 0);
      tl.fromTo("#am0w", { x: -260 }, { x: 420, duration: 5.2, ease: "none" }, 0.1);
      tl.fromTo("#am0w", { y: 0 }, { y: -8, duration: 0.25, yoyo: true, repeat: 19, ease: "sine.inOut" }, 0.1);
      pop("#tm0", 0.1); pop("#nm0", at(0, 0.05));

      /* S1 · 163 million, 7 in 10 */
      let d1 = ""; MAP.pts.forEach((p, i) => { if (i % 2 === 0) d1 += `<circle class="d1" cx="${p[0]}" cy="${p[1]}" r="8" fill="${INK}"/>`; });
      add("s1", `<div id="m1" class="abs" style="left:260px;top:20px">${mapSvg("map1", 560, d1 + `<circle id="me1" cx="${MAP.pts[120][0]}" cy="${MAP.pts[120][1]}" r="18" fill="${ORANGE}" stroke="${INK}" stroke-width="5"/>`)}</div>`);
      add("s1", `<div id="n1" class="abs" style="left:0;top:600px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:140px;line-height:1">0</div><div id="l1" class="abs label" style="left:0;top:760px;width:1080px;font-size:52px">Nigerians without safe water at home</div>` + chipAt("s1c", 860, "7 IN 10 PEOPLE", 64) + srcLine("sr1", "Source: WHO/UNICEF JMP 2025 (2024 data)"));
      tl.set([".d1", "#l1", "#s1c"], { opacity: 0 }, T[1]);
      tl.fromTo("#s1 .cam", focus(540 - 260 + MAP.pts[120][0] * 560 / MAP.w, 20 + MAP.pts[120][1] * 560 / MAP.h, 3.2), { ...focus(540, 500, 1.0), duration: 1.6, ease: "power2.inOut" }, T[1]);
      tl.to(".d1", { opacity: 1, duration: 0.05, stagger: { each: 0.01, from: "random" } }, T[1] + 0.6);
      counter("n1", 163000000, at(1, 0.1), 1.6); pop("#l1", at(1, 0.2)); pop("#s1c", at(1, 0.72), { rotation: -2 });

      /* S2 · the well */
      add("s2", `<div id="wl2" class="abs" style="left:80px;top:300px">${svgI(iWell, 380)}</div>` + amina("am2", 470, 330, 200, "smile") + glass("g2", { left: 760, top: 360, w: 240, extra: `<g id="gm2">${bacterium(60, 130, 0.6, "")}${virus(100, 175, 0.5, "")}</g>` }) + `<div id="ln2" class="abs" style="left:740px;top:400px;width:280px;height:280px"><svg viewBox="0 0 300 300" width="280" height="280"><circle cx="140" cy="140" r="110" fill="none" stroke="${INK}" stroke-width="14"/><line x1="220" y1="220" x2="290" y2="290" stroke="${INK}" stroke-width="22" stroke-linecap="round"/></svg></div>`);
      add("s2", `<div id="c2a" class="abs" style="left:60px;top:60px"><span class="chip" style="font-size:44px">LOOKS CLEAN ✓</span></div><div id="c2b" class="abs" style="left:560px;top:60px"><span class="chip" style="font-size:44px">LOOKS CLEAR ✓</span></div>` + chipAt("c2c", 840, "BUT GERMS HIDE INSIDE ✗", 54, RED, -2));
      tl.set(["#gm2", "#ln2", "#c2a", "#c2b", "#c2c"], { opacity: 0 }, T[2]);
      pop("#wl2", T[2] + 0.05); pop("#am2", T[2] + 0.1); tl.set("#am2_o", { opacity: 0 }, T[2]); tl.to("#am2_o", { opacity: 1, duration: 0.2 }, T[2] + 0.2);
      pop("#c2a", at(2, 0.05)); pop("#g2", at(2, 0.25)); pop("#c2b", at(2, 0.3));
      tl.fromTo("#ln2", { x: 300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4 }, at(2, 0.6)); tl.to("#gm2", { opacity: 1, duration: 0.2 }, at(2, 0.72)); wiggle("#gm2 .wig", at(2, 0.72), 1.0);
      pop("#c2c", at(2, 0.75), { rotation: -2 }); setFace(tl, "am2", "worry", at(2, 0.75));

      /* S3 · cholera 2024 */
      let ppl = ""; for (let r = 0; r < 10; r++) for (let c = 0; c < 10; c++) { const k = r * 10 + c; ppl += `<circle class="pp3 ${[23, 57, 81].includes(k) ? "rd3" : ""}" cx="${60 + c * 44}" cy="${60 + r * 44}" r="15" fill="#fff" stroke="${INK}" stroke-width="4"/>`; }
      add("s3", `<svg id="pg3" class="abs" style="left:40px;top:300px" width="520" height="520">${ppl}</svg>`);
      add("s3", `<div id="k3" class="abs" style="left:590px;top:300px;width:470px"><div id="k3a"><div id="n3a" style="font-family:Cap;font-weight:900;font-size:96px">0</div><div class="label" style="font-size:42px;text-align:left">cholera cases in 2024</div></div><div id="k3b" style="margin-top:26px"><div id="n3b" style="font-family:Cap;font-weight:900;font-size:96px;color:${RED}">0</div><div class="label" style="font-size:42px;text-align:left">deaths</div></div></div>` + chipAt("c3", 40, "3 IN 100 WHO GOT SICK DIED", 50, RED) + srcLine("sr3", "Source: WHO global cholera report 2024 (WER, Sep 2025)"));
      tl.set(["#k3a", "#k3b", "#c3", ".pp3"], { opacity: 0 }, T[3]);
      tl.set("#k3a", { opacity: 1 }, at(3, 0.08)); counter("n3a", 24841, at(3, 0.08), 1.4);
      tl.set("#k3b", { opacity: 1 }, at(3, 0.4)); counter("n3b", 734, at(3, 0.4), 1.0);
      tl.to(".pp3", { opacity: 1, duration: 0.05, stagger: 0.012 }, at(3, 0.55));
      tl.to(".rd3", { attr: { fill: RED }, duration: 0.2, stagger: 0.15 }, at(3, 0.8)); pop("#c3", at(3, 0.78));

      /* S4 · response */
      add("s4", chipAt("c4", 40, "NIGERIA CDC + WHO", 60) + card("c4a", 40, 220, 310, iPlan, "contingency plans") + card("c4b", 385, 220, 310, iFlask, "more lab testing") + card("c4c", 730, 220, 310, iSyr, "emergency vaccination") + srcLine("sr4", "Source: WHO Joint External Evaluation, Nigeria 2024 · WHO WER 2025"));
      tl.set(["#c4", "#c4a", "#c4b", "#c4c"], { opacity: 0 }, T[4]);
      tl.fromTo("#s4 .cam", focus(540, 400, 1.06), { ...focus(540, 480, 1.0), duration: 4, ease: "none" }, T[4]);
      pop("#c4", T[4] + 0.05); pop("#c4a", at(4, 0.4)); pop("#c4b", at(4, 0.55)); pop("#c4c", at(4, 0.72));

      /* S5 · at home: no fuel, filter upkeep */
      add("s5", amina("am5", 440, 40, 200, "worry") + `<div id="p5" class="abs" style="left:80px;top:520px;width:380px;text-align:center"><svg viewBox="0 0 160 160" width="230" height="230">${iPot}${cross}</svg><div class="label" style="font-size:52px">no fuel to spare</div></div><div id="f5" class="abs" style="left:620px;top:520px;width:380px;text-align:center"><svg viewBox="0 0 160 160" width="230" height="230">${iFilter}${cross}</svg><div class="label" style="font-size:52px">filter upkeep</div></div>`);
      tl.set(["#p5", "#f5"], { opacity: 0 }, T[5]);
      pop("#am5", T[5] + 0.05); pop("#p5", at(5, 0.5)); pop("#f5", at(5, 0.8));

      /* S6 · AquaCore */
      add("s6", `<div id="br6" class="abs" style="left:0;top:10px;width:1080px;text-align:center"><svg viewBox="0 0 160 160" width="110" height="110">${iAqua}</svg><span style="font-family:Cap;font-weight:900;font-size:70px;vertical-align:top;line-height:110px"> AQUA<span style="color:${BLUE}">CORE</span></span></div>`);
      add("s6", `<div id="cn6" class="abs" style="left:80px;top:220px">${svgI(iCanS + `<text x="80" y="112" text-anchor="middle" font-family="Cap" font-weight="900" font-size="30" fill="${INK}">25 L</text>`, 260)}</div><div id="tb6" class="abs" style="left:140px;top:-120px">${svgI(iTab, 140)}</div><div id="ck6" class="abs" style="left:380px;top:240px;width:260px;text-align:center"><svg viewBox="0 0 160 160" width="200" height="200">${iClock}<line id="hd6" x1="80" y1="80" x2="80" y2="30" stroke="${BLUE}" stroke-width="10" stroke-linecap="round"/></svg><div class="chip" style="display:inline-block;font-size:40px">30 MIN</div></div>`);
      add("s6", `<div id="kd6" class="abs" style="left:0;top:0;width:1080px;height:1080px">${figure("kd6a", { left: 720, top: 230, w: 140, prop: "glass", face: "smile" })}${figure("kd6b", { left: 880, top: 250, w: 130, prop: "glass", face: "smile" })}</div>`);
      add("s6", chipAt("lb6", 640, "TESTED BY NATIONAL LABS ✓", 48) + `<div id="lb6c" class="abs label" style="left:0;top:750px;width:1080px;font-size:52px">E. coli · Salmonella · cholera <span style="color:${BLUE}">eliminated</span></div><div id="lb6b" class="abs" style="left:0;top:860px;width:1080px;text-align:center;font-family:Cap;font-weight:800;font-size:30px;color:${MUTED}">Centre Pasteur du Cameroun 2012 · LANSPEX Niger 2017</div>`);
      tl.set(["#br6", "#ck6", "#kd6", "#lb6", "#lb6b", "#lb6c", "#tb6"], { opacity: 0 }, T[6]);
      pop("#br6", T[6] + 0.05); pop("#cn6", T[6] + 0.1);
      tl.set("#tb6", { opacity: 1 }, at(6, 0.08)); tl.fromTo("#tb6", { y: 0 }, { y: 420, duration: 0.45, ease: "power2.in" }, at(6, 0.08)); tl.to("#tb6", { opacity: 0, duration: 0.1 }, at(6, 0.08) + 0.45);
      pop("#ck6", at(6, 0.25)); tl.fromTo("#hd6", { rotation: 0 }, { rotation: 360, svgOrigin: "80 80", duration: 1.2 }, at(6, 0.27));
      tl.to("#kd6", { opacity: 1, duration: 0.3 }, at(6, 0.38)); tl.fromTo("#kd6a .armR, #kd6b .armR", { rotation: 0 }, { rotation: -60, svgOrigin: "100 150", duration: 0.4, yoyo: true, repeat: 1 }, at(6, 0.45));
      pop("#lb6", at(6, 0.58)); pop("#lb6c", at(6, 0.72)); pop("#lb6b", at(6, 0.8));

      /* S7 · pilot */
      const PS = [[iBox, "we send 100 tablets", 0.2], [iFlask, "your local lab tests before &amp; after", 0.38], [iChart, "we size the program", 0.62], [iTruck, "we deploy", 0.78], [iScale, "and scale", 0.9]];
      add("s7", chipAt("pt7", 10, "IT STARTS WITH A PILOT", 52) + PS.map(([ic, lab], k) => `<div id="ps7_${k}" class="abs" style="left:60px;top:${130 + k * 165}px;width:960px;height:150px;display:flex;align-items:center;gap:26px"><div style="width:84px;height:84px;border-radius:42px;background:${BLUE};color:#fff;font-family:Cap;font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:center;flex:none">${k + 1}</div>${svgI(ic, 140)}<div class="label" style="text-align:left;font-size:54px;line-height:1.05">${lab}</div></div>`).join(""));
      tl.set(["#pt7", ...PS.map((x, k) => `#ps7_${k}`)], { opacity: 0 }, T[7]);
      pop("#pt7", T[7] + 0.05);
      PS.forEach((x, k) => tl.fromTo(`#ps7_${k}`, { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power2.out" }, at(7, x[2]) - 0.2));

      /* S8 · CTA */
      add("s8", `<div id="m8" class="abs" style="left:340px;top:20px">${mapSvg("map8", 400)}</div><div id="w8" class="abs label" style="left:40px;top:470px;width:1000px;font-size:64px">Working on water in Nigeria?</div>` + chipAt("p8", 620, "START A PILOT", 96, BLUE, -2) + `<div id="u8" class="abs" style="left:0;top:800px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:50px">aquacoreglobal.com</div>`);
      tl.set(["#w8", "#p8", "#u8"], { opacity: 0 }, T[8]);
      pop("#m8", T[8] + 0.05); pop("#w8", at(8, 0.05)); pop("#p8", at(8, 0.5), { rotation: -2 }); pop("#u8", at(8, 0.7));

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
    total = round(end_card + 3.0, 2)
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
        json.dump({"id": f"pais-nga-{lang}-{fmt}", "name": f"pais-nga-{lang}-{fmt}"}, open(os.path.join(d, "meta.json"), "w"))
        link = os.path.join(d, "assets")
        if not os.path.islink(link):
            os.symlink("../assets", link)
    print(lang, "total", total, "T", T)


if __name__ == "__main__":
    for lang in ("en",):
        build(lang)
