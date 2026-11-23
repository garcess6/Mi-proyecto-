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
        "tag": "COUNTRY FOCUS · <b>ETHIOPIA</b>",
        "title": "Ethiopia Water",
        "noBasic": "people without basic drinking water",
        "france": "more than the population of Spain",
        "nineTen": "8 in 10",
        "noSafe": "have no safe water at home",
        "rivers": "of rural people lack even basic water",
        "cholera": "cholera", "typhoid": "typhoid", "diarrhoea": "diarrhoea",
        "since": "OUTBREAK SINCE 2023",
        "cases": "cholera cases in 2024", "deaths": "deaths in 2024",
        "vacc": "vaccination", "surv": "surveillance", "wash": "water &amp; hygiene",
        "goal": "GOAL 2028", "goalSub": "national plan to eliminate cholera",
        "today": "What can families do today?",
        "boil": "boiling", "boilX": "needs fuel",
        "filt": "filters", "filtX": "need upkeep",
        "chl": "chlorine", "chlX": "weak in cloudy water",
        "perL": "1 tablet = 25 L", "min": "30 MIN", "cloudyOK": "works in cloudy water",
        "cost": "€0.50", "costSub": "per person / month", "labs": "Tested by national labs: Cameroon · Niger",
        "working": "Working on water in Ethiopia?", "pilot": "START A PILOT",
        "question": "Could this work in <span style=\"color:#1e7fd8\">your</span> region? 💬",
        "src1": "Source: WHO/UNICEF JMP 2025 (2024 data)",
        "src2": "Source: WHO global cholera report 2024 (WER, Sep 2025)",
        "src3": "Source: WHO Joint External Evaluation, Ethiopia 2025",
        "srcEnd": "Sources: WHO/UNICEF JMP 2025 · WHO 2025",
        "locale": "en-US",
        "key": "fiftynine|million|ethiopia|spain|eight|safe|rural|thirty|cholera|typhoid|diarrhoea|thousand|deaths|2023|2028|vaccination|surveillance|boiling|fuel|filters|chlorine|cloudy|aquacore|dioxide|litres|minutes|fifty|cents|labs|pilot",
    },
}

SCENES = r'''
      const TX = __TX__;
      const MAP = __MAP__;
      const T = __T__;
      const RED = "#d64545";
      const at = (li, f) => LINES[li][0] + LINES[li][1] * f;
      const fmt = (v) => Math.round(v).toLocaleString(TX.locale);
      const counter = (id, to, t, dur, suffix = "") => { const o = { v: 0 }; tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { document.getElementById(id).textContent = fmt(o.v) + suffix; } }, t); };
      const mapSvg = (id, w, extra = "") => `<svg id="${id}" viewBox="0 0 ${MAP.w} ${MAP.h}" width="${w}" height="${w}"><path class="mp" d="${MAP.d}" fill="${SKY}" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>${extra}</svg>`;
      const src = (id, text) => `<div id="${id}" class="abs" style="left:0;top:985px;width:1080px;text-align:center;font-family:Cap;font-weight:800;font-size:28px;color:${MUTED}">${text}</div>`;
      const iAqua = `<g stroke="${INK}" stroke-width="9" fill="none" stroke-linejoin="round"><path d="M80 14 C80 14 38 66 38 96 a42 42 0 0 0 84 0 C122 66 80 14 80 14 Z"/></g><circle cx="80" cy="96" r="18" fill="${BLUE}"/>`;
      const iClock = `<circle cx="80" cy="80" r="64" fill="#fff" stroke="${INK}" stroke-width="9"/><circle cx="80" cy="80" r="7" fill="${INK}"/><line x1="80" y1="80" x2="80" y2="34" stroke="${BLUE}" stroke-width="9" stroke-linecap="round"/><line x1="80" y1="80" x2="110" y2="80" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>`;
      const iVib = `<path d="M30 100 C30 50 100 30 130 70" stroke="${INK}" stroke-width="24" fill="none" stroke-linecap="round"/><path d="M30 100 C30 50 100 30 130 70" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M130 70 q14 10 26 2" stroke="${INK}" stroke-width="5" fill="none"/>`;
      const iBact = `<g transform="translate(80 80) scale(2.2)"><rect x="-26" y="-13" width="52" height="26" rx="13" fill="#fff" stroke="${INK}" stroke-width="4.5"/><circle cx="-8" cy="-2" r="3" fill="${INK}"/><circle cx="8" cy="3" r="3" fill="${BLUE}"/></g>`;
      const iDrop = `<path d="M80 14 C80 14 34 70 34 100 a46 46 0 0 0 92 0 C126 70 80 14 80 14 Z" fill="#fff" stroke="${INK}" stroke-width="8"/><path d="M38 112 Q80 100 122 112 a46 42 0 0 1 -84 0 Z" fill="${SKY}"/>`;
      const iSyr = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linecap="round" stroke-linejoin="round"><rect x="40" y="56" width="80" height="34" rx="6" transform="rotate(-35 80 73)"/><path d="M114 40 L138 22 M126 32 L136 44 M44 104 L22 128" /></g><rect x="52" y="62" width="40" height="22" fill="${BLUE}" transform="rotate(-35 80 73)"/>`;
      const iHosp = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round"><rect x="24" y="44" width="112" height="96"/><path d="M14 44 L80 14 L146 44"/></g><path d="M80 66 V114 M56 90 H104" stroke="${RED}" stroke-width="14" stroke-linecap="round"/>`;
      const iCan = `<g stroke="${INK}" stroke-width="8" stroke-linejoin="round"><path d="M34 50 L126 50 L126 146 L34 146 Z" fill="${SKY}"/><path d="M62 50 L62 30 L98 30 L98 50" fill="#fff"/></g><circle cx="80" cy="100" r="22" fill="#fff" stroke="${INK}" stroke-width="6"/><line x1="64" y1="100" x2="96" y2="100" stroke="${INK}" stroke-width="6"/>`;
      const card = (id, left, top, w, icon, label, sub = "", isz = 170) => `<div id="${id}" class="abs card" style="left:${left}px;top:${top}px;width:${w}px;padding:18px 10px"><svg viewBox="0 0 160 160" width="${isz}" height="${isz}">${icon}</svg><div class="label" style="font-size:48px">${label}</div>${sub ? `<div class="small" style="font-size:34px;color:${MUTED};margin-top:4px">${sub}</div>` : ""}</div>`;
      const big = (id, top, html, size = 150, color = INK) => `<div id="${id}" class="abs" style="left:0;top:${top}px;width:1080px;text-align:center;font-family:Cap;font-weight:900;font-size:${size}px;line-height:1;color:${color}">${html}</div>`;
      const sub = (id, top, html, size = 52, color = INK) => `<div id="${id}" class="abs label" style="left:40px;top:${top}px;width:1000px;font-size:${size}px;color:${color}">${html}</div>`;

      /* ================= S0 · hook: 70 million ================= */
      let d0 = "";
      MAP.pts.forEach((p, i) => { if (i % 3 === 0) d0 += `<circle class="d0" cx="${p[0]}" cy="${p[1]}" r="9" fill="${INK}"/>`; });
      add("s0", `<div id="m0" class="abs" style="left:250px;top:10px">${mapSvg("map0", 580, d0)}</div>`);
      add("s0", big("n0", 630, "0") + sub("l0", 790, TX.noBasic) + `<div id="fr0" class="abs" style="left:0;top:880px;width:1080px;text-align:center"><span class="chip" style="font-size:46px">${TX.france}</span></div>` + src("sr0", TX.src1));
      tl.set([".d0", "#l0", "#fr0"], { opacity: 0 }, 0);
      tl.fromTo("#s0 .cam", focus(540, 320, 1.25), { ...focus(540, 520, 1.0), duration: 2.2, ease: "power2.inOut" }, 0);
      tl.fromTo("#map0 .mp", { opacity: 0, scale: 0.6, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }, 0.1);
      tl.to(".d0", { opacity: 1, duration: 0.05, stagger: { each: 0.012, from: "random" } }, 0.6);
      counter("n0", 59000000, at(0, 0.05), 1.6);
      pop("#l0", at(0, 0.2));
      pop("#fr0", at(0, 0.62));

      /* ================= S1 · 9 in 10, rivers ================= */
      let figs = "";
      for (let i = 0; i < 10; i++) figs += `<div class="f1" id="f1_${i}" style="position:absolute;left:${30 + i * 102}px;top:60px">${figure("p1_" + i, { left: 0, top: 0, w: 90, face: i < 8 ? "worry" : "smile" })}</div>`;
      add("s1", figs);
      add("s1", big("n1", 300, TX.nineTen, 130, BLUE) + sub("l1", 430, TX.noSafe));
      add("s1", `<svg class="abs" style="left:0;top:0" width="1080" height="1080"><path id="riv" d="M0 830 L1080 830" stroke="${DIRT}" stroke-width="10" stroke-dasharray="30 18"/></svg>`);
      add("s1", `<div id="w1" class="abs" style="left:300px;top:560px">${figure("p1w", { left: 0, top: 0, w: 140, face: "hmm" })}</div><div id="jc1" class="abs" style="left:430px;top:600px;text-align:center"><svg viewBox="0 0 160 160" width="150" height="150">${iClock}</svg><div class="chip" style="font-size:36px">30+ MIN</div></div>`);
      add("s1", `<div id="n1b" class="abs" style="left:620px;top:580px;width:440px;text-align:center"><div style="font-family:Cap;font-weight:900;font-size:96px;color:${BLUE}" id="n1bv">0</div><div class="label" style="font-size:44px">${TX.rivers}</div></div>` + src("sr1", TX.src1));
      tl.set([".f1", "#n1", "#l1", "#w1", "#jc1", "#n1b", "#riv"], { opacity: 0 }, T[1]);
      tl.fromTo("#s1 .cam", focus(540, 300, 1.1), { ...focus(540, 520, 1.0), duration: 2.0, ease: "power1.inOut" }, T[1] + 0.2);
      tl.to(".f1", { opacity: 1, duration: 0.1, stagger: 0.06 }, T[1] + 0.05);
      for (let i = 0; i < 8; i++) tl.to(`#f1_${i}`, { opacity: 0.35, duration: 0.15 }, at(1, 0.12) + i * 0.08);
      pop("#n1", at(1, 0.1)); pop("#l1", at(1, 0.2));
      tl.to("#riv", { opacity: 1, duration: 0.3 }, at(1, 0.5));
      pop("#w1", at(1, 0.55)); pop("#jc1", at(1, 0.75));
      tl.fromTo("#w1", { x: -40 }, { x: 40, duration: 2.5, ease: "none" }, at(1, 0.55));
      tl.set("#n1b", { opacity: 1 }, at(1, 0.6)); counter("n1bv", 53, at(1, 0.6), 1.0, "%");

      /* ================= S2 · diseases + cholera 2025 ================= */
      add("s2", card("c2a", 40, 20, 310, iVib, TX.cholera) + card("c2b", 385, 20, 310, iBact, TX.typhoid) + card("c2c", 730, 20, 310, iDrop, TX.diarrhoea));
      const step = Math.floor(MAP.pts.length / 26);
      let prov = "";
      for (let i = 0; i < 26; i++) { const p = MAP.pts[(i * step + Math.floor(step / 2)) % MAP.pts.length]; if (false) prov += `<circle class="pv" data-i="${i}" cx="${p[0]}" cy="${p[1]}" r="20" fill="#fff" stroke="${INK}" stroke-width="6"/>`; }
      add("s2", `<div id="m2" class="abs" style="left:20px;top:330px">${mapSvg("map2", 520, prov)}</div>`);
      add("s2", `<div id="k2" class="abs" style="left:560px;top:340px;width:500px">
        <div id="k2a"><span class="chip" style="font-size:34px;white-space:nowrap;background:${RED}">${TX.since}</span></div>
        <div id="k2b" style="margin-top:22px"><span id="n2b" style="font-family:Cap;font-weight:900;font-size:86px">0</span><div class="label" style="font-size:40px;text-align:left">${TX.cases}</div></div>
        <div id="k2c" style="margin-top:22px"><span id="n2c" style="font-family:Cap;font-weight:900;font-size:86px;color:${RED}">0</span><div class="label" style="font-size:40px;text-align:left">${TX.deaths}</div></div></div>` + src("sr2", TX.src2));
      tl.set(["#c2a", "#c2b", "#c2c", "#m2", "#k2a", "#k2b", "#k2c"], { opacity: 0 }, T[2]);
      tl.fromTo("#s2 .cam", focus(540, 260, 1.06), { ...focus(540, 280, 1.03), duration: 1.0, ease: "none" }, T[2]);
      pop("#c2a", at(2, 0.04)); pop("#c2b", at(2, 0.1)); pop("#c2c", at(2, 0.16));
      tl.to("#s2 .cam", { ...focus(540, 560, 1.0), duration: 0.7, ease: "power2.inOut" }, at(2, 0.24));
      tl.to("#m2", { opacity: 1, duration: 0.3 }, at(2, 0.26));
      $$("#map2 .pv").forEach((c) => { const i = +c.dataset.i; if (i % 13 < 8) tl.to(c, { attr: { fill: RED }, duration: 0.12 }, at(2, 0.34) + (i % 13) * 0.09 + (i >= 13 ? 0.05 : 0)); });
      pop("#k2a", at(2, 0.86));
      tl.set("#k2b", { opacity: 1 }, at(2, 0.5)); counter("n2b", 27152, at(2, 0.5), 1.3, "");
      tl.set("#k2c", { opacity: 1 }, at(2, 0.66)); counter("n2c", 271, at(2, 0.66), 1.0, "");

      /* ================= S3 · response ================= */
      const iLens = `<g stroke="${INK}" stroke-width="10" fill="${SKY}" stroke-linecap="round"><circle cx="68" cy="68" r="44"/><line x1="100" y1="100" x2="142" y2="142" stroke-width="16"/></g>`;
      add("s3", card("c3a", 40, 30, 310, iLens, TX.surv) + card("c3b", 385, 30, 310, iSyr, TX.vacc) + card("c3c", 730, 30, 310, iCan, TX.wash));
      add("s3", `<div id="g3" class="abs" style="left:0;top:560px;width:1080px;text-align:center"><span class="chip" style="font-size:86px;padding:14px 40px">${TX.goal}</span><div class="label" style="font-size:52px;margin-top:24px">${TX.goalSub}</div></div>` + src("sr3", TX.src3));
      tl.set(["#c3a", "#c3b", "#c3c", "#g3"], { opacity: 0 }, T[3]);
      tl.fromTo("#s3 .cam", focus(540, 300, 1.1), { ...focus(540, 480, 1.0), duration: 3, ease: "power1.inOut" }, T[3]);
      pop("#g3", at(3, 0.1), { rotation: -2 });
      tl.to("#g3", { y: 60, duration: 0.4 }, at(3, 0.42));
      pop("#c3a", at(3, 0.42)); pop("#c3b", at(3, 0.52)); pop("#c3c", at(3, 0.64));

      /* ================= S4 · alternatives ================= */
      const iPot = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round" stroke-linecap="round"><path d="M20 70 L140 70 L130 140 L30 140 Z"/><path d="M8 70 L152 70"/><path d="M50 50 q-8 -14 0 -28 M80 50 q-8 -14 0 -28 M110 50 q-8 -14 0 -28" stroke="${MUTED}" fill="none"/></g>`;
      const iFilter = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round"><path d="M20 30 L140 30 L100 90 L100 140 L60 140 L60 90 Z"/><path d="M36 54 L124 54" stroke="${BLUE}"/></g>`;
      const iChlor = `<g stroke="${INK}" stroke-width="8" fill="#fff" stroke-linejoin="round" stroke-linecap="round"><rect x="50" y="60" width="60" height="84" rx="10" fill="${SKY}"/><path d="M64 60 L64 40 L96 40 L96 60"/><path d="M70 40 L70 20 L90 20 L90 40"/></g>`;
      const row = (id, top, icon, name, x) => `<div id="${id}" class="abs" style="left:40px;top:${top}px;width:1000px;height:200px;border-bottom:5px solid ${SKY}"><svg class="abs" style="left:0;top:20px" viewBox="0 0 160 160" width="160" height="160">${icon}</svg><div class="abs label" style="left:180px;top:60px;text-align:left;font-size:64px">${name}</div><div class="abs label" style="left:500px;top:60px;width:500px;text-align:right;font-size:56px">${x} <span style="font-size:80px">✗</span></div></div>`;
      add("s4", sub("t4", 40, TX.today, 62) + row("r4a", 170, iPot, TX.boil, TX.boilX) + row("r4b", 400, iFilter, TX.filt, TX.filtX) + row("r4c", 630, iChlor, TX.chl, TX.chlX));
      tl.set(["#t4", "#r4a", "#r4b", "#r4c"], { opacity: 0 }, T[4]);
      tl.fromTo("#s4 .cam", focus(540, 480, 1.04), { ...focus(540, 500, 1.0), duration: 4, ease: "none" }, T[4]);
      pop("#t4", T[4] + 0.05);
      [["#r4a", 0.3], ["#r4b", 0.55], ["#r4c", 0.75]].forEach(([r, f]) => tl.fromTo(r, { x: -100, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power2.out" }, at(4, f) - 0.2));

      /* ================= S5 · AquaCore ================= */
      add("s5", `<div id="br5" class="abs" style="left:0;top:10px;width:1080px;text-align:center"><svg viewBox="0 0 160 160" width="140" height="140">${iAqua}</svg><div style="font-family:Cap;font-weight:900;font-size:72px;letter-spacing:0.04em;margin-top:-6px">AQUA<span style="color:${BLUE}">CORE</span></div><div class="chip" style="display:inline-block;font-size:40px;margin-top:8px">ClO₂</div></div>`);
      const badge = (id, left, top, html) => `<div id="${id}" class="abs card" style="left:${left}px;top:${top}px;width:470px;height:200px;display:flex;align-items:center;justify-content:center;flex-direction:column">${html}</div>`;
      add("s5", badge("b5a", 50, 330, `<div style="font-family:Cap;font-weight:900;font-size:44px">${TX.perL}</div>`) + badge("b5b", 560, 330, `<svg viewBox="0 0 160 160" width="110" height="110">${iClock}</svg><div class="chip" style="font-size:40px">${TX.min}</div>`) + badge("b5c", 50, 560, `<div style="font-size:80px;color:${BLUE};line-height:1">✓</div><div class="label" style="font-size:48px">${TX.cloudyOK}</div>`) + badge("b5d", 560, 560, `<div style="font-family:Cap;font-weight:900;font-size:88px;color:${BLUE};line-height:1">${TX.cost}</div><div class="label" style="font-size:42px">${TX.costSub}</div>`));
      add("s5", `<div id="lb5" class="abs" style="left:0;top:820px;width:1080px;text-align:center"><span class="chip" style="font-size:40px">${TX.labs} ✓</span></div>`);
      tl.set(["#br5", "#b5a", "#b5b", "#b5c", "#b5d", "#lb5"], { opacity: 0 }, T[5]);
      tl.fromTo("#s5 .cam", focus(540, 330, 1.08), { ...focus(540, 500, 1.0), duration: 1.6, ease: "power2.inOut" }, T[5] + 0.6);
      pop("#br5", T[5] + 0.05);
      pop("#b5a", at(5, 0.2)); pop("#b5b", at(5, 0.36)); pop("#b5c", at(5, 0.5)); pop("#b5d", at(5, 0.66)); pop("#lb5", at(5, 0.84));

      /* ================= S6 · CTA ================= */
      add("s6", `<div id="m6" class="abs" style="left:340px;top:20px">${mapSvg("map6", 400)}</div>` + sub("w6", 470, TX.working, 64) + `<div id="p6" class="abs" style="left:0;top:620px;width:1080px;text-align:center"><span class="chip" style="font-size:96px;padding:16px 50px">${TX.pilot}</span><div style="font-family:Cap;font-weight:900;font-size:50px;margin-top:30px">aquacoreglobal.com</div></div>`);
      tl.set(["#m6", "#w6", "#p6"], { opacity: 0 }, T[6]);
      pop("#m6", T[6] + 0.05); pop("#w6", at(6, 0.05)); pop("#p6", at(6, 0.55), { rotation: -2 });

      /* ================= S7 · end card ================= */
      add("s7", `<div class="abs" style="left:0;top:60px;width:1080px;text-align:center">
        <img id="logo" src="assets/logo.png" style="width:380px;height:380px" />
        <div id="e2" style="font-family:Cap;font-weight:900;font-size:56px;margin-top:10px">aquacoreglobal.com</div>
        <div id="e3" style="display:inline-block;margin-top:40px;padding:22px 40px;border:7px solid ${INK};border-radius:40px;font-family:Hand;font-size:54px">${TX.question}</div>
      </div>` + src("sr7", TX.srcEnd));
      pop("#logo", T[7] + 0.05);
      tl.fromTo("#e2", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35 }, T[7] + 0.3);
      pop("#e3", T[7] + 0.6);
      tl.fromTo("#logo", { scale: 1 }, { scale: 1.06, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }, T[7] + 1.0);

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
    total = round(end_card + 3.5, 2)
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
        json.dump({"id": f"pais-eth-{lang}-{fmt}", "name": f"pais-eth-{lang}-{fmt}"}, open(os.path.join(d, "meta.json"), "w"))
        link = os.path.join(d, "assets")
        if not os.path.islink(link):
            os.symlink("../assets", link)
    print(lang, "total", total, "T", T)


if __name__ == "__main__":
    for lang in ("en",):
        build(lang)
