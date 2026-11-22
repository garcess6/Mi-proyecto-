const {chromium}=require('playwright');const m=require('./_meta.json');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:2000},deviceScaleFactor:1});
await p.goto('file://'+__dirname+'/_build.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
const s=async(id,path,o={})=>(await p.$('#'+id)).screenshot({path,...o});
await s('stack','logo/aquacore-logo-cuadrado.png',{omitBackground:true});await s('avatar','logo/aquacore-perfil-instagram.png');await s('icon-tr','logo/aquacore-icono.png',{omitBackground:true});
await s('lockup','logo/aquacore-logo-horizontal.png');await s('lockup-tr','logo/aquacore-logo-horizontal-transparente.png',{omitBackground:true});await s('lockup-neg','logo/aquacore-logo-horizontal-fondo-azul.png');
for(let i=1;i<=m.about;i++)await s('about'+i,`historias/about-us-${i}.png`);
for(let i=1;i<=m.partner;i++)await s('partner'+i,`historias/partner-${i}.png`);
for(let i=1;i<=m.how;i++)await s('how'+i,`historias/how-it-works-${i}.png`);
for(let i=1;i<=m.pilot;i++)await s('pilot'+i,`historias/pilot-${i}.png`);
for(const c of m.covers)await s('cov-'+c,`destacadas/destacada-${c}.png`);
await b.close()})()
