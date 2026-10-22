# Forge 0.18.1: a living sky behind the app that follows the real time of day, with a Sky choice in Settings.
# Applies count-asserted replacements to base18.html (0.18.0) and writes work.html.
src = open('base18.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep('/* Nav */', '''#skyCv{position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:-1;image-rendering:pixelated;image-rendering:crisp-edges;image-rendering:pixelated;pointer-events:none}
/* Nav */''')
rep('<div class="app">', '<canvas id="skyCv" aria-hidden="true"></canvas>\n<div class="app">')

SKY_JS = r'''
/* ---- The living sky: the app's background follows the real time of day, drawn at pixel-art resolution ---- */
/* s = sky top and horizon, h = far and near hills, st = star colour (none by day), orb = sun or moon */
const SKY={
  light:{dawn:{s:['#F5E2EC','#FCEBDD'],h:['#EBCBD9','#DDB7CC'],st:null,orb:null},
         day:{s:['#DCEFFA','#EFF8EA'],h:['#CDE6C3','#B8DBAE'],st:null,orb:'#FFF3BF'},
         dusk:{s:['#E6DCF6','#F9DDE6'],h:['#D8C4E8','#C5B0DC'],st:'#FFFFFF',orb:null},
         night:{s:['#D8D9F1','#EAE6F8'],h:['#CBC5E8','#B8B1DD'],st:'#FFFFFF',orb:'#FFFFFF'}},
  dark:{dawn:{s:['#1C1630','#4E2944'],h:['#33213D','#271A32'],st:'#A9849F',orb:null},
        day:{s:['#122039','#1E3447'],h:['#1B2D3B','#15243A'],st:null,orb:'#E9E2B8'},
        dusk:{s:['#191533','#4A2252'],h:['#2C1C42','#211736'],st:'#A897C9',orb:null},
        night:{s:['#0B0E26','#1B1A45'],h:['#17173C','#101030'],st:'#A7A4DA',orb:'#FFF4C9'}}};
function skyPhase(){const m=state&&state.settings&&state.settings.sky;if(m==='day'||m==='night')return m;const h=new Date().getHours();return h>=5&&h<7?'dawn':h>=7&&h<17?'day':h>=17&&h<20?'dusk':'night';}
function skyDark(){const t=document.documentElement.getAttribute('data-theme');return t==='dark'||(t!=='light'&&!!(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches));}
let skyKey='';
function drawSky(force){
  const cv=document.getElementById('skyCv');if(!cv)return;
  if(state&&state.settings&&state.settings.sky==='plain'){cv.hidden=true;skyKey='';return;}cv.hidden=false;
  const asp=Math.max(1,innerHeight)/Math.max(1,innerWidth);let W=96,H=Math.round(96*asp);if(H<140){H=140;W=Math.min(400,Math.round(140/asp));}const ph=skyPhase(),dk=skyDark(),k=ph+(dk?1:0)+'/'+W+'x'+H;
  if(!force&&k===skyKey)return;skyKey=k;
  cv.width=W;cv.height=H;
  const P=SKY[dk?'dark':'light'][ph],ctx=cv.getContext('2d'),img=ctx.createImageData(W,H),d=img.data;
  const put=(x,y,c)=>{x=Math.floor(x);y=Math.floor(y);if(x<0||y<0||x>=W||y>=H)return;const q=hexRGB(c),o=(y*W+x)*4;d[o]=q[0];d[o+1]=q[1];d[o+2]=q[2];d[o+3]=255;};
  const s0=hexRGB(P.s[0]),s1=hexRGB(P.s[1]),NB=8;
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const f=y/H*NB;let bi=Math.floor(f);if(f-bi>(BAY[(y&3)*4+(x&3)]+.5)/16)bi++;const t=Math.min(1,bi/NB),o=(y*W+x)*4;d[o]=lerp(s0[0],s1[0],t);d[o+1]=lerp(s0[1],s1[1],t);d[o+2]=lerp(s0[2],s1[2],t);d[o+3]=255;}
  const r=mulberry32(4242);
  if(P.st)for(let i=0,n=Math.round(W*H/300);i<n;i++){const x=r()*W,y=r()*H*.62;if(y<H*.11&&x<W*.62)continue;put(x,y,P.st);if(x>W*.62&&r()<.18){put(x+1,y,P.st);put(x-1,y,P.st);put(x,y+1,P.st);put(x,y-1,P.st);}}
  if(P.orb){const cx=W-15,cy=Math.round(H*.17),R=ph==='day'?5:4;for(let y=-R;y<=R;y++)for(let x=-R;x<=R;x++)if(x*x+y*y<=R*R+1)put(cx+x,cy+y,P.orb);if(ph==='night')for(let y=-R;y<=R;y++)for(let x=-R;x<=R;x++)if((x+2)*(x+2)+(y-1)*(y-1)<=R*R-2)put(cx+x+2,cy+y-1,P.s[0]);}
  for(let x=0;x<W;x++){const t=Math.round(H*.81+3*Math.sin(x*.11+1)+2*Math.sin(x*.27));for(let y=t;y<H;y++)put(x,y,P.h[0]);}
  for(let x=0;x<W;x++){const t=Math.round(H*.875+2.5*Math.sin(x*.08+3)+1.5*Math.sin(x*.31));for(let y=t;y<H;y++)put(x,y,P.h[1]);}
  ctx.putImageData(img,0,0);
}
let skyRT=0;window.addEventListener('resize',()=>{clearTimeout(skyRT);skyRT=setTimeout(()=>drawSky(),150);});
setInterval(()=>{if(!document.hidden)drawSky();},60000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)drawSky();});
if(window.matchMedia){const mq=matchMedia('(prefers-color-scheme: dark)');if(mq.addEventListener)mq.addEventListener('change',()=>drawSky(true));}
'''
rep('/* ================= Start ================= */', SKY_JS + '\n/* ================= Start ================= */')
# redraw whenever appearance settings change, and once at start
rep("function applySettings(){", "function applySettings(){setTimeout(()=>drawSky(true),0);")


# ---- the Sky choice in Settings ----
rep("settings:{mood:'mix',sound:true,reduce:false,nudge:null,lore:true}", "settings:{mood:'mix',sound:true,reduce:false,nudge:null,lore:true,sky:'auto'}")
rep("Object.keys(D.settings).forEach(k=>{if(s.settings[k]===undefined)s.settings[k]=D.settings[k];});",
    "Object.keys(D.settings).forEach(k=>{if(s.settings[k]===undefined)s.settings[k]=D.settings[k];});if(!['auto','day','night','plain'].includes(s.settings.sky))s.settings.sky='auto';")
rep("""<button class="chip" data-settheme="${a[0]}" aria-pressed="${(S.theme||'auto')===a[0]}">${a[1]}</button>`).join('')}</div></div>""",
    """<button class="chip" data-settheme="${a[0]}" aria-pressed="${(S.theme||'auto')===a[0]}">${a[1]}</button>`).join('')}</div><div class="lbl2">Sky</div><p class="muted small" style="margin:2px 0 6px">The sky behind the app can follow your day, from dawn to night.</p><div class="chips" role="group" aria-label="Sky">${[['auto','Follows your day'],['day','Always day'],['night','Always night'],['plain','Plain']].map(a=>`<button class="chip" data-setsky="${a[0]}" aria-pressed="${(S.sky||'auto')===a[0]}">${a[1]}</button>`).join('')}</div></div>""")
rep("  else if(b.dataset.settheme){state.settings.theme=b.dataset.settheme;save();applySettings();renderSettings();}",
    "  else if(b.dataset.settheme){state.settings.theme=b.dataset.settheme;save();applySettings();renderSettings();}\n  else if(b.dataset.setsky){state.settings.sky=b.dataset.setsky;save();drawSky(true);renderSettings();}")
# ---- version and what is new ----
rep('<title>Forge (prototype 0.18.0)</title>', '<title>Forge (prototype 0.18.1)</title>')
rep("const VERSION='prototype 0.18.0';", "const VERSION='prototype 0.18.1';")
rep('const SEEN_V=21;', 'const SEEN_V=22;')
rep("""<ul class="newlist"><li><b>A clearer Today.</b>""",
    """<ul class="newlist"><li><b>A living sky.</b> The sky behind the app follows your day, from dawn to night, with a pixel horizon along the bottom. You can keep it always day, always night or plain in Settings.</li>
    <li><b>A clearer Today.</b>""")

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
