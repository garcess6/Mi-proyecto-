#!/usr/bin/env python3
"""Make a ~45 s cut of a country video from its gen_hook.py.

Usage: python3 make_short.py <country> <lang>
Writes videos/pais-<c>/gen_short_<lang>.py and runs it -> short-<lang>-9x16 / short-<lang>-16x9
"""
import json, os, re, subprocess, sys

C, LANG = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "videos", f"pais-{C}")

CFG = {
    # kept original story scenes, in order (last one = end card)
    "cod": dict(keep=[0, 1, 2, 4, 5, 7, 8], hook_wav="vo_{lang}/h0.wav", hook=None, hk=None),
    "eth": dict(keep=[1, 2, 3, 4, 5, 7, 8], hook_wav="vo_short_{lang}/h0.wav",
                hook="Imagine all of Spain without basic drinking water. In Ethiopia, that's the reality for fifty-nine million people.",
                hk=dict(num=59000000, suf="", label="people without basic drinking water", chip="MORE THAN ALL OF SPAIN", chip2="THAT'S ETHIOPIA TODAY",
                        src="Source: WHO/UNICEF JMP 2025 (2024 data)", wChip="spain", wWater="reality", key="imagine|spain|basic|drinking|water|ethiopia|reality|fiftynine|million")),
    "nga": dict(keep=[0, 1, 2, 5, 6, 8], hook_wav="vo_short_{lang}/h0.wav",
                hook="Three in every hundred. That's how many people who caught cholera in Nigeria in 2024 died. And it often starts with water that looks perfectly clean.",
                hk=dict(num=3, suf=" in 100", label="people who caught cholera died", chip="NIGERIA · 2024", chip2="WATER THAT LOOKS CLEAN",
                        src="Source: WHO WER 2025 (2024 data)", wChip="nigeria", wWater="clean", key="three|hundred|cholera|nigeria|2024|died|water|clean")),
}[C]

s = open(os.path.join(D, "gen_hook.py")).read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:100], s.count(a))
    s = s.replace(a, b)


# ---- renumber scenes
a = s.index("SCENES = r'''"); b = s.index("\n'''\n", a)
sc = s[a:b]
hook_at = sc.index("      /* ================= HOOK scene")
marks = [(m.start(), int(m.group(1)) if m.group(1) else 99) for m in re.finditer(r"      /\* (?:================= )?(?:S(\d) ·|end card)", sc[:hook_at])]
head = sc[:marks[0][0]]
blocks = {}
for i, (pos, k) in enumerate(marks):
    end = marks[i + 1][0] if i + 1 < len(marks) else hook_at
    blocks[k] = sc[pos:end]
tail = sc[hook_at:]
MAP = {k: n for n, k in enumerate(CFG["keep"])}
out = head
for k in sorted(blocks):
    blk = blocks[k]
    if k == 99:
        out += blk; continue
    if k not in MAP:
        continue
    n = MAP[k]
    blk = re.sub(r'(["#])s%d\b' % k, r'\g<1>s%d' % n, blk)
    blk = re.sub(r'T\[%d\]' % k, 'T[%d]' % n, blk)
    blk = re.sub(r'\bat\(%d,' % k, 'at(%d,' % n, blk)
    out += blk
g0 = tail.index("const GCFG = "); g1 = tail.index(";", g0)
G = json.loads(tail[g0 + len("const GCFG = "):g1])
G = [G[k] for k in CFG["keep"] if k < len(G)]
tail = tail[:g0] + "const GCFG = " + json.dumps(G) + tail[g1:]
s = s[:a] + out + tail + s[b:]

# ---- hook text / visuals
if CFG["hook"]:
    s = re.sub(r"^HOOKS = .*$", "HOOKS = " + json.dumps({LANG: CFG["hook"]}, ensure_ascii=False).replace("\\", "\\\\"), s, count=1, flags=re.M)
    s = re.sub(r"^HK = .*$", "HK = " + json.dumps({LANG: CFG["hk"]}, ensure_ascii=False).replace("\\", "\\\\"), s, count=1, flags=re.M)

# ---- short script, voice, timing, output
rep('[l.strip() for l in open(os.path.join(HERE, "assets", f"lines_{lang}.txt")) if l.strip()]', '[l.strip() for l in open(os.path.join(HERE, "assets", f"lines_short_{lang}.txt")) if l.strip()]')
hw = CFG["hook_wav"].replace("{lang}", "{lang}")
rep('return os.path.join(HERE, "assets", f"vo_{lang}", "h0.wav" if i == 0 else f"l{i}.wav")',
    'return os.path.join(HERE, "assets", f"' + hw + '") if i == 0 else os.path.join(HERE, "assets", f"vo_short_{lang}", f"l{i}.wav")')
rep('t += d + 0.45', 't += d + 0.35')
s = re.sub(r"total = round\(end_card \+ 3\.\d, 2\)", "total = round(end_card + 3.0, 2)", s)
s = s.replace('end_card = round(starts[-1] + durs[-1] + 0.5, 2)', 'end_card = round(starts[-1] + durs[-1] + 0.4, 2)')
rep('"voiceh_{lang}.wav")], check=True)', '"voiceshort_{lang}.wav")], check=True)')
rep("src=\"assets/voiceh_{lang}.wav\"')", "src=\"assets/voiceshort_{lang}.wav\"')")
rep('d = os.path.join(HERE, f"hook-{lang}-{fmt}")', 'd = os.path.join(HERE, f"short-{lang}-{fmt}")')
rep('''        if not os.path.islink(link):
            os.symlink("../assets", link)''', '''        import shutil
        if os.path.islink(link): os.remove(link)
        shutil.rmtree(link, ignore_errors=True)
        shutil.copytree(os.path.join(HERE, "assets"), link, ignore=shutil.ignore_patterns("vo_*", "voice_*", "voiceh_*"))''')
s = re.sub(r'    for lang in \(.*?\):', f'    for lang in ("{LANG}",):', s)
fn = os.path.join(D, f"gen_short_{LANG}.py")
open(fn, "w").write(s)
subprocess.run([sys.executable, fn], check=True, cwd=D)
for fmt in ("9x16", "16x9"):
    f = os.path.join(D, f"short-{LANG}-{fmt}", "index.html")
    h = open(f).read().replace('<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>', '<script src="assets/vendor/gsap.min.js"></script>')
    open(f, "w").write(h)
print("done", C, LANG)
