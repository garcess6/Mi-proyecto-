DROP='<path d="M45 4 C45 4 8 50 8 70 a37 37 0 0 0 74 0 C82 50 45 4 45 4Z" fill="none" stroke="{s}" stroke-width="{w}" stroke-linejoin="round"/><circle cx="45" cy="70" r="16" fill="{c}"/>'
def drop(h,s="#0B2545",c="#1E7FD8",w=7): return f'<svg height="{h}" viewBox="-5 -2 100 116">{DROP.format(s=s,c=c,w=w)}</svg>'
NAVY="#0B2545";BLUE="#1E7FD8";LIGHT="#EAF4FD";GREY="#5B6B7E"
# --- icons (line art, 100x100) ---
def ic(body,size=200,col=NAVY): return f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
I={
"play":'<rect x="10" y="20" width="80" height="60" rx="10"/><path d="M42 36 L62 50 L42 64 Z" fill="#1E7FD8" stroke="#1E7FD8"/>',
"tablet":'<circle cx="50" cy="50" r="36"/><path d="M50 14 V86" stroke="#1E7FD8"/><path d="M22 54 C32 46 40 46 50 52 S68 58 78 50" stroke="#1E7FD8"/>',
"pilot":'<path d="M50 88 C50 88 22 58 22 40 a28 28 0 0 1 56 0 C78 58 50 88 50 88Z"/><circle cx="50" cy="40" r="10" fill="#1E7FD8" stroke="#1E7FD8"/>',
"partner":'<circle cx="38" cy="50" r="24"/><circle cx="62" cy="50" r="24" stroke="#1E7FD8"/>',
"glass":'<path d="M28 18 H72 L66 86 H34 Z"/><path d="M31 40 H69" stroke="#1E7FD8"/><circle cx="44" cy="56" r="4" fill="#1E7FD8" stroke="none"/><circle cx="57" cy="66" r="3" fill="#1E7FD8" stroke="none"/><circle cx="52" cy="50" r="2.5" fill="#1E7FD8" stroke="none"/>',
"can":'<rect x="24" y="26" width="52" height="62" rx="8"/><path d="M40 26 V16 H60 V26"/><path d="M24 50 C36 44 46 44 56 50 S70 54 76 50" stroke="#1E7FD8"/>',
"clock":'<circle cx="50" cy="52" r="34"/><path d="M50 32 V52 L64 60" stroke="#1E7FD8"/>',
"check":'<circle cx="50" cy="50" r="36"/><path d="M34 51 L46 63 L68 39" stroke="#1E7FD8"/>',
"ngo":'<path d="M50 82 C50 82 16 62 16 38 a17 17 0 0 1 34 -6 a17 17 0 0 1 34 6 C84 62 50 82 50 82Z"/>',
"gov":'<path d="M14 36 L50 16 L86 36 Z"/><path d="M24 42 V74 M42 42 V74 M58 42 V74 M76 42 V74" stroke="#1E7FD8"/><path d="M14 84 H86"/>',
"inv":'<path d="M14 80 H86"/><path d="M20 66 L40 46 L54 58 L82 28" stroke="#1E7FD8"/><path d="M66 28 H82 V44" stroke="#1E7FD8"/>',
"truck":'<rect x="10" y="32" width="50" height="34" rx="4"/><path d="M60 42 H76 L88 54 V66 H60 Z"/><circle cx="28" cy="72" r="7"/><circle cx="72" cy="72" r="7"/>',
"people":'<circle cx="35" cy="34" r="11"/><path d="M15 80 C15 62 25 54 35 54 S55 62 55 80"/><circle cx="66" cy="38" r="9" stroke="#1E7FD8"/><path d="M52 80 C54 66 60 60 66 60 S82 66 84 80" stroke="#1E7FD8"/>',
"book":'<path d="M50 26 C40 18 24 18 14 22 V80 C24 76 40 76 50 84 C60 76 76 76 86 80 V22 C76 18 60 18 50 26 Z"/><path d="M50 26 V84" stroke="#1E7FD8"/>',
"globe":'<circle cx="50" cy="50" r="36"/><ellipse cx="50" cy="50" rx="15" ry="36" stroke="#1E7FD8"/><path d="M14 50 H86" stroke="#1E7FD8"/>',
"chat":'<path d="M16 24 H84 V68 H44 L28 82 V68 H16 Z"/><path d="M32 44 H68 M32 54 H56" stroke="#1E7FD8"/>',
}
CSS=f"""@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');
*{{box-sizing:border-box}}body{{margin:0;font-family:Montserrat,sans-serif;color:{NAVY}}}
.f{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#fff;margin-bottom:20px}}
.in{{position:absolute;left:90px;right:90px;top:250px;bottom:300px;display:flex;flex-direction:column;justify-content:center}}
.kick{{font-size:36px;font-weight:700;letter-spacing:6px;color:{BLUE}}}
h1{{font-size:132px;line-height:1.02;font-weight:800;margin:24px 0 0}}
h2{{font-size:92px;line-height:1.08;font-weight:800;margin:22px 0 0}}
p{{font-size:50px;line-height:1.4;font-weight:500;color:{GREY};margin:34px 0 0}}
b.bl{{color:{BLUE}}}
.foot{{position:absolute;left:90px;right:90px;bottom:170px;display:flex;align-items:center;justify-content:space-between;font-size:26px;font-weight:600;color:{GREY}}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:800;color:{NAVY};letter-spacing:2px;font-size:28px}}
.dots{{display:flex;gap:10px}}.dots i{{width:14px;height:14px;border-radius:7px;background:#D5DEE8}}.dots i.on{{background:{BLUE};width:40px}}
.step{{display:flex;align-items:center;gap:36px;margin-top:56px}}
.num{{width:92px;height:92px;border-radius:46px;background:{BLUE};color:#fff;font-weight:800;font-size:38px;display:flex;align-items:center;justify-content:center;flex:none}}
.st{{font-size:54px;font-weight:700;line-height:1.2}}.st small{{display:block;font-size:36px;font-weight:500;color:{GREY};margin-top:6px}}
.card{{display:flex;gap:34px;align-items:center;background:{LIGHT};border-radius:32px;padding:34px 38px;margin-top:30px}}
.card .t{{font-size:54px;font-weight:800}}.card .d{{font-size:36px;font-weight:500;color:{GREY};margin-top:6px;line-height:1.35}}
.note{{font-size:30px;color:{GREY};margin-top:70px;line-height:1.4}}
.cta{{display:inline-block;background:{NAVY};color:#fff;font-weight:700;font-size:48px;padding:30px 52px;border-radius:60px;margin-top:50px}}
.dark{{background:{NAVY};color:#fff}}.dark p{{color:#B9C7D8}}.dark .kick{{color:#5DB8FF}}
"""
def foot(i,n,dark=False):
    s="#fff" if dark else NAVY
    return f'<div class="foot"><div class="brand" style="color:{s}">{drop(46,s,"#3FA9F5" if dark else BLUE,9)}AQUACORE</div><div class="dots">'+"".join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n))+'</div></div>'
about=[
 ('dark',f'<div>{drop(260,"#fff","#3FA9F5",7)}</div><div class="kick" style="margin-top:80px">ABOUT US</div><h1>Who we are</h1><p>Safe water starts with what you can\'t see.</p>'),
 ('',f'<div class="kick">THE PROBLEM</div>{ic(I["glass"],340)}<h2>Water can look clear and still make people sick.</h2><p>Millions of families drink from <b class="bl">rivers, wells and rainwater</b> that are never tested or treated.</p>'),
 ('',f'<div class="kick">WHAT WE DO</div>{ic(I["tablet"],340)}<h2>We make water treatment <b class="bl">simple.</b></h2><p>AquaCore develops water-treatment tablets and the local network to deliver them. <b class="bl">1 tablet treats up to 25 L</b> of water for drinking and cooking.</p>'),
 ('',f'<div class="kick">HOW IT WORKS</div><h2>4 easy steps</h2>'+"".join(f'<div class="step"><div class="num">{n}</div>{ic(I[k],130)}<div class="st">{t}<small>{d}</small></div></div>' for n,k,t,d in [(1,"can","Fill a 25 L container","Clean, covered container"),(2,"tablet","Add 1 tablet","One per 25 litres"),(3,"clock","Wait","Respect the contact time"),(4,"check","Ready to use","For drinking & cooking")])+'<div class="note">Results depend on the source water and correct use. Always follow the instructions.</div>'),
 ('',f'<div class="kick">WHY THIS ACCOUNT</div>{ic(I["book"],340)}<h2>We\'re here to <b class="bl">educate.</b></h2><p>Short, simple videos about the water we drink and why <b class="bl">prevention</b> matters: test, treat, check.</p><div><span class="cta">▶ Watch the series</span></div>'),
]
partner=[
 ('dark',f'<div>{ic(I["partner"].replace(NAVY,"#fff"),300,"#fff")}</div><div class="kick" style="margin-top:70px">PARTNER WITH US</div><h1>Safe water, at scale.</h1><p>For NGOs, governments and private investors. Worldwide.</p>'),
 ('',f'<div class="kick">WHO WE WORK WITH</div><h2>Volume programs only</h2>'+"".join(f'<div class="card">{ic(I[k],150)}<div><div class="t">{t}</div><div class="d">{d}</div></div></div>' for k,t,d in [("ngo","NGOs","Humanitarian & community water programs"),("gov","Governments","Public health & rural water supply"),("inv","Private investors","Scalable, impact-driven deployment")])+f'<p style="font-size:42px">We do not sell to individuals. <b class="bl">We work worldwide.</b></p>'),
 ('',f'<div class="kick">WHAT WE BRING</div><h2>From lab to community</h2>'+"".join(f'<div class="step"><div class="num">{n}</div>{ic(I[k],130)}<div class="st">{t}<small>{d}</small></div></div>' for n,k,t,d in [(1,"tablet","Tablets at volume","Supply sized to your program"),(2,"truck","Local distribution","Receive, verify, store, deliver"),(3,"people","Training","Families learn correct use"),(4,"check","Follow-up","Supervise and restock")])+f'<div class="card" style="margin-top:50px">{ic(I["pilot"],110)}<div><div class="t">Pilot model</div><div class="d">10,000 people · 90 days</div></div></div>'),
 ('dark',f'<div class="kick">LET\'S TALK</div>{ic(I["chat"],320,"#fff")}<h1 style="font-size:112px">Bring safe water to your communities.</h1><p>Send us a DM with the word <b style="color:#5DB8FF">PARTNER</b> or visit</p><div><span class="cta" style="background:#1E7FD8">aquacoreglobal.com</span></div>'),
]
def frames(name,sl):
    out=""
    for i,(cls,body) in enumerate(sl):
        out+=f'<div class="f {cls}" id="{name}{i+1}"><div class="in">{body}</div>{foot(i,len(sl),cls=="dark")}</div>'
    return out
covers=[("serie","play","SERIES"),("como-funciona","tablet","HOW IT WORKS"),("piloto","pilot","PILOT"),("about-us","drop","ABOUT US"),("partner","partner","PARTNER")]
cov=""
for n,k,_ in covers:
    icon=drop(560,"#fff","#3FA9F5",7) if k=="drop" else ic(I[k].replace(f'stroke="{BLUE}"','stroke="#3FA9F5"').replace(f'fill="{BLUE}"','fill="#3FA9F5"'),560,"#fff")
    cov+=f'<div class="f" id="cov-{n}" style="background:{NAVY};display:flex;align-items:center;justify-content:center">{icon}</div>'
logo=f'''<div id="avatar" style="width:1080px;height:1080px;background:{NAVY};display:flex;align-items:center;justify-content:center">{drop(560,"#fff","#3FA9F5",8)}</div>
<div id="icon-tr" style="width:1000px;height:1200px;display:flex;align-items:center;justify-content:center">{drop(1100)}</div>
<div id="lockup" style="display:inline-flex;align-items:center;gap:60px;padding:80px 100px;background:#fff">{drop(300)}<div><div style="font-size:130px;font-weight:800;letter-spacing:3px;line-height:1">AQUACORE</div><div style="font-size:38px;font-weight:500;letter-spacing:21px;white-space:nowrap;color:{GREY};margin-top:18px">GLOBAL TECHNOLOGIES</div></div></div>
<div id="lockup-tr" style="display:inline-flex;align-items:center;gap:60px;padding:80px 100px">{drop(300)}<div><div style="font-size:130px;font-weight:800;letter-spacing:3px;line-height:1">AQUACORE</div><div style="font-size:38px;font-weight:500;letter-spacing:21px;white-space:nowrap;color:{GREY};margin-top:18px">GLOBAL TECHNOLOGIES</div></div></div>
<div id="lockup-neg" style="display:inline-flex;align-items:center;gap:60px;padding:80px 100px;background:{NAVY};color:#fff">{drop(300,"#fff","#3FA9F5")}<div><div style="font-size:130px;font-weight:800;letter-spacing:3px;line-height:1">AQUACORE</div><div style="font-size:38px;font-weight:500;letter-spacing:21px;white-space:nowrap;color:#B9C7D8;margin-top:18px">GLOBAL TECHNOLOGIES</div></div></div>'''
open("_build.html","w").write(f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body style='background:transparent'>{logo}{frames('about',about)}{frames('partner',partner)}{cov}</body></html>")
open("logo/aquacore-icono.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -2 100 116">{DROP.format(s=NAVY,c=BLUE,w=7)}</svg>')
open("logo/aquacore-icono-blanco.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -2 100 116">{DROP.format(s="#fff",c="#3FA9F5",w=7)}</svg>')
import json;json.dump({"about":len(about),"partner":len(partner),"covers":[c[0] for c in covers]},open("_meta.json","w"))
