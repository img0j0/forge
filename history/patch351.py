# Forgelings 0.35.1: Living Sky (the interface pass Hunter chose on October 22, direction C of the design canvas).
# The interface now belongs to the same world as the art:
#  - The page IS the sky. Whenever the Sky setting is not Plain, the living sky is drawn in vivid colours that follow
#    the time of day (Light appearance) or in deep ones (Dark appearance), and the interface sits on it as dark glass
#    panels with gold rivets and gold buttons. Plain keeps the old look, untouched.
#  - Text that sits straight on the sky flips between dark ink (day, dawn) and light ink (dusk, night, Dark).
#  - Pixel-stepped buttons with a press edge, stepped chips and rows, a floating glass tab bar with pixel icons,
#    VT323 page titles. A short staggered entrance when you open a tab (off with reduced motion).
# Implementation: html.ls (Living Sky on) and html[data-skyink=dark|light], set by lsApply() from applySettings and
# drawSky. Panels, sheets, the tab bar and the binder re-declare the light-ink tokens, so anything inside them reads
# as before. Reads base35.html.
src = open('base35.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

STEP = "polygon(0 4px,4px 4px,4px 0,calc(100% - 4px) 0,calc(100% - 4px) 4px,100% 4px,100% calc(100% - 4px),calc(100% - 4px) calc(100% - 4px),calc(100% - 4px) 100%,4px 100%,4px calc(100% - 4px),0 calc(100% - 4px))"
INK = "--ink:#FFF7EC;--muted:#D2C9EE;--plum:#FFD36B;--plum-ink:#2E2A47;--chip:rgba(255,255,255,.1);--line:rgba(255,244,201,.2);--bg:#120E30;--scr:#FFB067"
CSS = """
/* ---- 0.35.1: Living Sky. The page is the sky; the interface is dark glass on it. ---- */
:root{--step:%(STEP)s}
.pi{shape-rendering:crispEdges}
html:root.ls{--bg:#17152A;--surface:#1E1846;%(INK)s;--stamp:#3A2C2E;--stampEdge:#7A5A3A;--mpaper:#1F1B38;--mburn:rgba(0,0,0,.42);--mfog:#3D3768;--mgrain:#FFFFFF;--mrib:#2C2750;--mbleed:.4;--frame:var(--frameD);--ped:var(--pedD);--dot:var(--dotD);--glow:rgba(255,180,100,.26);--glass:rgba(20,15,48,.9);--tsh:rgba(14,10,36,.55)}
html:root.ls[data-skyink="dark"]{--ink:#17203A;--muted:#2C3850;--plum:#4A2E8C;--plum-ink:#FFFFFF;--chip:rgba(255,255,255,.55);--line:rgba(23,32,58,.28);--scr:#8A3A12;--tsh:rgba(255,255,255,.5)}
html.ls :is(.panel-box,.group,.hero,.setblock,.sheet,.tabs,.binder,.mapwrap){%(INK)s;color:var(--ink)}
html.ls body{background:var(--bg)}
html.ls .panel-box,html.ls .group,html.ls .hero,html.ls .setblock{background:var(--dot) 0 0/8px 8px repeat,var(--glass) !important;background-clip:padding-box !important}
html.ls .hero:is(:has(#btnShowToday),:has(#btnTurn),:has(#btnShowFav)){background:var(--ped) center 192px/176px 22px no-repeat,radial-gradient(circle at 50%% 104px,var(--glow) 0,transparent 128px),var(--dot) 0 0/8px 8px repeat,var(--glass) !important;background-clip:padding-box !important}
html.ls .sheet{background:var(--dot) 0 0/8px 8px repeat,#1E1846;border-radius:0;clip-path:polygon(0 8px,4px 8px,4px 4px,8px 4px,8px 0,calc(100%% - 8px) 0,calc(100%% - 8px) 4px,calc(100%% - 4px) 4px,calc(100%% - 4px) 8px,100%% 8px,100%% 100%%,0 100%%)}
html.ls .binder{background:var(--glass);border-radius:0;clip-path:var(--step)}
html.ls .top h1{font:400 46px/.9 var(--px2);letter-spacing:.5px;text-shadow:0 3px 0 var(--tsh)}
html.ls .top #dateLabel{font-weight:700;margin-top:4px}
html.ls .hmsg{font:400 22px/1.1 var(--px2);font-style:normal;color:var(--plum);text-shadow:0 2px 0 var(--tsh)}
html.ls .primary{border-radius:0;clip-path:var(--step);background:linear-gradient(to top,#C98A12 0 5px,#FFD36B 5px);color:#2E2A47;padding:14px 22px 19px}
html.ls .primary:active{transform:none;background:linear-gradient(to top,#C98A12 0 2px,#FFD36B 2px);padding:17px 22px 16px}
html.ls .outline{border:0;border-radius:0;clip-path:var(--step);box-shadow:inset 0 0 0 2px var(--plum);padding:14px 18px}
html.ls .outline:active{box-shadow:inset 0 0 0 2px var(--plum),inset 0 3px 0 rgba(0,0,0,.25)}
html.ls :is(.chip,.fchip,.pill){border:0;border-radius:0;clip-path:var(--step);background:var(--chip)}
html.ls :is(.chip,.fchip)[aria-pressed="true"]{background:var(--plum);color:var(--plum-ink)}
html.ls :is(.moodbtn,.tool){border-radius:0;clip-path:var(--step);border-color:var(--line);background:rgba(255,255,255,.06)}
html.ls .rowl .ri,html.ls .stat-chip,html.ls .num{border-radius:0;clip-path:var(--step)}
html.ls .hearthwrap{border:0;border-radius:0;clip-path:var(--step)}
html.ls .mapwrap{border-radius:0;clip-path:var(--step);border:0;box-shadow:none}
html.ls .act{border-radius:0;clip-path:var(--step);border:0;box-shadow:inset 0 0 0 2px var(--plum);background:rgba(255,255,255,.04)}
html.ls .pip{border-radius:0}
html.ls :is(.rib,.chron,.realm,.calling,.mecho,.otale),html.ls #view-chronicle .cal span.c{%(INK)s;color:var(--ink)}
html.ls :is(.rib,.chron,.realm,.calling,.mecho,.otale){background-color:var(--glass);border-radius:0;clip-path:var(--step)}
html.ls #view-chronicle .cal span.c:not(.done){background-color:var(--glass)}
html.ls[data-skyink="dark"] .inkm{color:#5A3A00}
html.ls[data-skyink="dark"] .mine{color:#4A3000}
html.ls[data-skyink="light"] .inkm,html.ls :is(.panel-box,.group,.hero,.setblock,.sheet,.mapwrap) .inkm{color:#FFD36B}
html.ls[data-skyink="light"] .mine,html.ls :is(.panel-box,.group,.hero,.setblock,.sheet,.mapwrap) .mine{color:#FFE9A8;background:rgba(255,211,107,.12)}
html.ls :is(.primary,.outline,.chip,.fchip,.pill,.moodbtn,.tool,.act,.binder button):focus-visible{outline:none;box-shadow:inset 0 0 0 3px #FFFFFF,inset 0 0 0 5px #2E2A47}
html.ls .tabs{left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));max-width:440px;margin:0 auto;padding:7px 4px 6px;background:rgba(16,12,40,.95);border:0;clip-path:var(--step)}
html.ls .tab{color:var(--muted)}
html.ls .tab[aria-current="page"]{color:var(--plum)}
html.ls .tab[aria-current="page"]::before{content:'';position:absolute;top:-3px;left:50%%;width:24px;height:3px;margin-left:-12px;background:var(--plum)}
html.ls .toast{border-radius:0;clip-path:var(--step);bottom:calc(92px + env(safe-area-inset-bottom,0px))}
html.ls .app{padding-bottom:116px}
html.ls:not(.reduce) main>section.enter>*{animation:lsRise .26s cubic-bezier(.2,.9,.3,1) both}
html.ls:not(.reduce) main>section.enter>*:nth-child(2){animation-delay:.04s}
html.ls:not(.reduce) main>section.enter>*:nth-child(3){animation-delay:.08s}
html.ls:not(.reduce) main>section.enter>*:nth-child(4){animation-delay:.12s}
html.ls:not(.reduce) main>section.enter>*:nth-child(n+5){animation-delay:.16s}
@keyframes lsRise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
""" % {'STEP': STEP, 'INK': INK}
rep("</style>\n</head>", CSS + "</style>\n</head>")

# ---- pixel icons in the tab bar (both looks) ----
ICONS = {
 'today': ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="3"/><path d="M9 8h6M9 12h6M9 16h3"/></svg>',
           'M3 1h6v1h-6zM3 10h6v1h-6zM2 2h1v8h-1zM9 2h1v8h-1zM6 4h1v1h-1zM5 5h3v2h-3zM5 7h2v1h-2z'),
 'hearth': ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3.2 2-4.2 0 2 1 3 2 3 0-3-1-5 1-8.8z"/></svg>',
            'M6 1h1v1h-1zM5 2h2v1h-2zM5 3h3v1h-3zM4 4h4v1h-4zM4 5h5v1h-5zM4 6h4v1h-4zM5 7h3v1h-3zM1 9h10v1h-10zM2 10h8v1h-8z'),
 'binder': ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="7" height="7" rx="2"/><rect x="13.5" y="3.5" width="7" height="7" rx="2"/><rect x="3.5" y="13.5" width="7" height="7" rx="2"/><rect x="13.5" y="13.5" width="7" height="7" rx="2"/></svg>',
            'M1 1h4v4h-4zM7 1h4v4h-4zM1 7h4v4h-4zM7 7h4v4h-4z'),
 'chronicle': ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6.5l6-2.5 6 2.5 6-2.5v13.5l-6 2.5-6-2.5-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg>',
               'M1 2h3v9h-3zM5 1h2v9h-2zM8 2h3v9h-3z'),
 'settings': ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/></svg>',
              'M5 0h2v2h-2zM5 10h2v2h-2zM0 5h2v2h-2zM10 5h2v2h-2zM3 2h6v1h-6zM3 9h6v1h-6zM2 3h1v6h-1zM9 3h1v6h-1zM5 5h2v2h-2z'),
}
for k, (old, d) in ICONS.items():
    rep(f'<button class="tab" data-tab="{k}"' + ('' if k != 'today' else ' aria-current="page"') + '>' + old,
        f'<button class="tab" data-tab="{k}"' + ('' if k != 'today' else ' aria-current="page"') + f'><svg class="pi" viewBox="0 0 12 12" aria-hidden="true"><path fill="currentColor" d="{d}"/></svg>')

# ---- the sky: vivid by day and dusk for Light, deep for Dark; it sets the ink for text on the sky ----
rep("function skyPhase(){", """const SKYV={dawn:{s:['#F4B7A6','#FCE3C4'],h:['#E8B9C2','#DDA9B8'],st:null,orb:null},
  day:{s:['#8FD3F2','#DFF3C8'],h:['#9AD48F','#7BC46F'],st:null,orb:'#FFEFA0'},
  dusk:{s:['#3F357F','#6E4596'],h:['#4A3A86','#34296A'],st:'#FFFFFF',orb:null},
  night:{s:['#0B0F2A','#2B2C6B'],h:['#1E1D45','#15143A'],st:'#FFFFFF',orb:'#FFF4C9'}};
function lsOn(){return !!(state&&state.settings&&state.settings.sky!=='plain');}
function lsApply(){const el=document.documentElement,on=lsOn();el.classList.toggle('ls',on);const ph=on?skyPhase():'',ink=on&&!skyDark()&&(ph==='day'||ph==='dawn')?'dark':'light';if(on)el.setAttribute('data-skyink',ink);else el.removeAttribute('data-skyink');return on;}
function lsEnter(sec){if(!sec||!lsOn())return;sec.classList.remove('enter');void sec.offsetWidth;sec.classList.add('enter');clearTimeout(sec._lsT);sec._lsT=setTimeout(()=>sec.classList.remove('enter'),700);}
function skyPhase(){""")
rep("  if(state&&state.settings&&state.settings.sky==='plain'){cv.hidden=true;skyKey='';return;}cv.hidden=false;",
    "  if(!lsApply()){cv.hidden=true;skyKey='';document.documentElement.style.removeProperty('--bg');return;}cv.hidden=false;")
rep("  const P=SKY[dk?'dark':'light'][ph],ctx=cv.getContext('2d'),img=ctx.createImageData(W,H),d=img.data;",
    "  const P=dk?SKY.dark[ph]:SKYV[ph],ctx=cv.getContext('2d'),img=ctx.createImageData(W,H),d=img.data;\n  document.documentElement.style.setProperty('--bg',P.s[0]);document.querySelectorAll('meta[name=theme-color]').forEach(m=>m.setAttribute('content',P.s[0]));")
# the theme and sky settings apply the look straight away (drawSky runs a moment later)
rep("const th=state.settings.theme||'auto';if(th==='auto')document.documentElement.removeAttribute('data-theme');else document.documentElement.setAttribute('data-theme',th);}",
    "const th=state.settings.theme||'auto';if(th==='auto')document.documentElement.removeAttribute('data-theme');else document.documentElement.setAttribute('data-theme',th);lsApply();}")
rep("  else if(b.dataset.setsky){state.settings.sky=b.dataset.setsky;save();drawSky(true);renderSettings();}",
    "  else if(b.dataset.setsky){state.settings.sky=b.dataset.setsky;save();drawSky(true);if(!lsOn())document.querySelectorAll('meta[name=theme-color]').forEach((m,i)=>m.setAttribute('content',i?'#16132E':'#F1EDF8'));renderSettings();}")
rep("The sky behind the app can follow your day, from dawn to night.",
    "The sky behind the app follows your day, from dawn to night, and the app’s colours follow the sky. Light and Dark set how bright it is. Plain keeps a quiet, flat look.")
# a short entrance when a tab opens
rep("if(tab==='hearth')renderHearth();renderNav();window.scrollTo(0,0);}));",
    "if(tab==='hearth')renderHearth();renderNav();window.scrollTo(0,0);lsEnter($('#view-'+tab));}));")

# ---- version, What's New ----
rep('<title>Forgelings (prototype 0.35.0)</title>', '<title>Forgelings (prototype 0.35.1)</title>')
rep("const VERSION='prototype 0.35.0'", "const VERSION='prototype 0.35.1'")
rep('const SEEN_V=39;', 'const SEEN_V=40;')
rep("""<ul class="newlist"><li><b>The Forge.</b>""",
    """<ul class="newlist"><li><b>Living Sky.</b> The whole app now sits in the sky that follows your day, from bright morning to dusk to a starry night, with glowing panels, gold buttons and pixel icons. Prefer the old look? Settings, Sky, Plain.</li>
    <li><b>The Forge.</b>""")
import re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
