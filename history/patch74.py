# 0.74: a calmer, easier read (Hunter, November 12: "Is the user interface, colors, layout, and usability optimized to the
#   highest level we can achieve" ... "Let's do it" to the polish pass).
#   - Type scale. Plain text now uses 12 (tab and button captions), 14, 16, 18 and 20 px: every 13, 15 and 17 px rule moves
#     up one step, except card faces and icons, whose sizes are fitted to fixed boxes. Handwriting uses 44 (page titles),
#     36 (reveals), 28 (section headings) and 22 (everything else); a few decorative stamps keep their sizes. The restore box
#     is 14 px. Measured before: 14 sizes on the five tabs and 12 handwriting sizes in the stylesheet.
#   - Explanations fade. The Forge's long explanation, the choose sheet's how-to line, the Map's tap hint and the "book in
#     two inks" line show on the first five days they are seen, then stay away (`tipFade`, localStorage forge-tips-v1, per
#     device, never in the save). The elements are removed after render, so no translated template changes.
#   - One focal point at the Hearth: when an action is ready (gold), the others draw a lighter one-pixel frame; the Hearth's
#     list of extras (shelf, by the fire, keepsakes...) reads in plain type instead of handwriting.
import re,subprocess,os
S=open('base731.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.73.1'","const VERSION='prototype 0.74.0'")
rep("<title>Forgelings (prototype 0.73.1)</title>","<title>Forgelings (prototype 0.74.0)</title>")
# type scale: 43 rules, each replaced exactly once
rep("h3{font:600 17px/1.2 var(--display);margin:20px 0 8px}","h3{font:600 18px/1.2 var(--display);margin:20px 0 8px}")
rep(".outline{display:block;width:100%;background:transparent;color:var(--plum);border:2px solid var(--plum);border-radius:999px;padding:12px 18px;font:600 17px/1.2 var(--display)}",".outline{display:block;width:100%;background:transparent;color:var(--plum);border:2px solid var(--plum);border-radius:999px;padding:12px 18px;font:600 18px/1.2 var(--display)}")
rep(".ghost{background:none;border:0;color:var(--muted);text-decoration:underline;text-underline-offset:3px;padding:8px 6px;font-size:15px}",".ghost{background:none;border:0;color:var(--muted);text-decoration:underline;text-underline-offset:3px;padding:8px 6px;font-size:16px}")
rep(".setblock b{font:600 17px var(--display)}",".setblock b{font:600 18px var(--display)}")
rep(".ssum{color:var(--muted);font-size:13px;line-height:1.35}",".ssum{color:var(--muted);font-size:14px;line-height:1.35}")
rep("textarea.box{width:100%;min-height:150px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);border-radius:12px;padding:10px;font:13px/1.4 ui-monospace,Menlo,monospace}","textarea.box{width:100%;min-height:150px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);border-radius:12px;padding:10px;font:14px/1.4 ui-monospace,Menlo,monospace}")
rep(".heroback{width:136px;height:190px;border:0;padding:0;display:grid;align-content:center;justify-items:center;gap:10px;color:#fff;font:600 15px var(--display);background:radial-gradient(circle,rgba(255,255,255,.2) 0 1.8px,transparent 2.6px) 0 0/16px 16px,#5B4A9E;box-shadow:inset 0 0 0 6px #4A3B88}",".heroback{width:136px;height:190px;border:0;padding:0;display:grid;align-content:center;justify-items:center;gap:10px;color:#fff;font:600 16px var(--display);background:radial-gradient(circle,rgba(255,255,255,.2) 0 1.8px,transparent 2.6px) 0 0/16px 16px,#5B4A9E;box-shadow:inset 0 0 0 6px #4A3B88}")
rep(".summary{color:var(--muted);font-size:15px;margin:0 2px 6px;padding-right:max(0px,calc(21vw - 14px))}",".summary{color:var(--muted);font-size:16px;margin:0 2px 6px;padding-right:max(0px,calc(21vw - 14px))}")
rep(".tale b{display:block;font:600 15px/1.3 var(--display)}",".tale b{display:block;font:600 16px/1.3 var(--display)}")
rep("ul.furn li small{display:block;color:var(--muted);font-size:13px;line-height:1.35}","ul.furn li small{display:block;color:var(--muted);font-size:14px;line-height:1.35}")
rep(".skips{position:absolute;left:0;right:0;top:220px;text-align:center;font:600 15px var(--display);color:#D9D2F5}",".skips{position:absolute;left:0;right:0;top:220px;text-align:center;font:600 16px var(--display);color:#D9D2F5}")
rep(".gwho button{display:flex;align-items:center;gap:6px;min-height:44px;padding:4px 12px 4px 6px;border-radius:999px;border:2px solid var(--line);background:var(--surface);color:var(--ink);font:600 15px var(--display)}",".gwho button{display:flex;align-items:center;gap:6px;min-height:44px;padding:4px 12px 4px 6px;border-radius:999px;border:2px solid var(--line);background:var(--surface);color:var(--ink);font:600 16px var(--display)}")
rep(".otale h3{margin:0 0 2px;font:600 17px var(--display)}",".otale h3{margin:0 0 2px;font:600 18px var(--display)}")
rep(".otale .meta{margin:0 0 8px;color:var(--muted);font-size:13px}",".otale .meta{margin:0 0 8px;color:var(--muted);font-size:14px}")
rep(".mecho .q{margin:6px 0 0;color:var(--muted);font-size:13px}",".mecho .q{margin:6px 0 0;color:var(--muted);font-size:14px}")
rep(".later{margin:2px 0 0;color:var(--muted);font-size:13px}",".later{margin:2px 0 0;color:var(--muted);font-size:14px}")
rep(".gpick button{min-height:64px;border-radius:12px;border:2px solid var(--line);background:var(--surface);color:var(--ink);font:600 13px var(--display);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:6px}",".gpick button{min-height:64px;border-radius:12px;border:2px solid var(--line);background:var(--surface);color:var(--ink);font:600 14px var(--display);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:6px}")
rep(".giftnote{margin:10px 0 0;font:600 15px var(--display);color:#3B2E6E;background:rgba(255,246,207,.85);border-radius:12px;padding:8px 12px;display:inline-block}",".giftnote{margin:10px 0 0;font:600 16px var(--display);color:#3B2E6E;background:rgba(255,246,207,.85);border-radius:12px;padding:8px 12px;display:inline-block}")
rep(".slab{font:600 13px var(--display);color:var(--muted)}",".slab{font:600 14px var(--display);color:var(--muted)}")
rep(".islelist button{display:block;width:100%;min-height:44px;padding:8px 12px;border:0;background:#F7EEDA;color:#3A2E22;font:400 13px/1.4 var(--body,inherit);text-align:left;cursor:pointer}",".islelist button{display:block;width:100%;min-height:44px;padding:8px 12px;border:0;background:#F7EEDA;color:#3A2E22;font:400 14px/1.4 var(--body,inherit);text-align:left;cursor:pointer}")
rep(".ownitem .ot small{display:block;color:var(--muted);font-size:13px;margin-left:20px}",".ownitem .ot small{display:block;color:var(--muted);font-size:14px;margin-left:20px}")
rep("h2.sub3{font:600 17px/1.2 var(--display);margin:20px 0 8px}","h2.sub3{font:600 18px/1.2 var(--display);margin:20px 0 8px}")
rep(".ov .rv-hint{color:#D9D2F5;font-size:15px;text-align:center}",".ov .rv-hint{color:#D9D2F5;font-size:16px;text-align:center}")
rep(".whisper{font-style:italic;color:#CFC2FF;border-left:3px solid #8E78E8;padding:2px 0 2px 10px;max-width:320px;text-align:left;line-height:1.35;font-size:17px}",".whisper{font-style:italic;color:#CFC2FF;border-left:3px solid #8E78E8;padding:2px 0 2px 10px;max-width:320px;text-align:left;line-height:1.35;font-size:18px}")
rep(".tpage{font-size:17px;line-height:1.55}",".tpage{font-size:18px;line-height:1.55}")
rep(".scrawl{margin:10px 0 0;padding:2px 0 2px 10px;border-left:2px dashed var(--scr);color:var(--scr);font:italic 500 15px/1.4 var(--body);transform:rotate(-.5deg);transform-origin:left}",".scrawl{margin:10px 0 0;padding:2px 0 2px 10px;border-left:2px dashed var(--scr);color:var(--scr);font:italic 500 16px/1.4 var(--body);transform:rotate(-.5deg);transform-origin:left}")
rep(".rib small{display:block;color:var(--muted);font-size:13px;line-height:1.3}",".rib small{display:block;color:var(--muted);font-size:14px;line-height:1.3}")
rep(".favmark{position:absolute;top:3px;right:5px;color:#FFD36B;font-size:15px;text-shadow:0 1px 2px #000,0 0 4px #000;pointer-events:none}",".favmark{position:absolute;top:3px;right:5px;color:#FFD36B;font-size:16px;text-shadow:0 1px 2px #000,0 0 4px #000;pointer-events:none}")
rep("html.jr .app .rowl b{font:700 calc(var(--hs)*23px)/1.05 var(--hand)}","html.jr .app .rowl b{font:700 calc(var(--hs)*22px)/1.05 var(--hand)}")
rep("html.jr .app h2.sub3{font:700 calc(var(--hs)*25px)/1 var(--hand);margin:14px 0 6px}","html.jr .app h2.sub3{font:700 calc(var(--hs)*28px)/1 var(--hand);margin:14px 0 6px}")
rep("html.jr .app .hero:is(:has(#btnShowToday),:has(#btnShowFav))>p.muted{grid-column:2;grid-row:2;margin:0;font:700 calc(var(--hs)*21px)/1.15 var(--hand);color:var(--world)}","html.jr .app .hero:is(:has(#btnShowToday),:has(#btnShowFav))>p.muted{grid-column:2;grid-row:2;margin:0;font:700 calc(var(--hs)*22px)/1.15 var(--hand);color:var(--world)}")
rep("html.jr .app .feel .feelq{font:700 calc(var(--hs)*24px)/1 var(--hand);margin:6px 0 6px}","html.jr .app .feel .feelq{font:700 calc(var(--hs)*22px)/1 var(--hand);margin:6px 0 6px}")
rep("html.jr .app .summary{padding-right:0;font:700 calc(var(--hs)*21px)/1.2 var(--hand);color:var(--ink)}","html.jr .app .summary{padding-right:0;font:700 calc(var(--hs)*22px)/1.2 var(--hand);color:var(--ink)}")
rep("html.jr .app .binder .jcap{display:block;font:700 calc(var(--hs)*19px)/1.1 var(--hand);color:#2E2A47;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:3px 2px 0}","html.jr .app .binder .jcap{display:block;font:700 calc(var(--hs)*22px)/1.1 var(--hand);color:#2E2A47;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:3px 2px 0}")
rep("html.jr .app .binder .empty{border:2px dashed var(--line);border-radius:0;color:var(--muted);font:700 calc(var(--hs)*20px)/1 var(--hand)}","html.jr .app .binder .empty{border:2px dashed var(--line);border-radius:0;color:var(--muted);font:700 calc(var(--hs)*22px)/1 var(--hand)}")
rep("html.jr .app :is(.calling,.realm) b{font:700 calc(var(--hs)*24px)/1 var(--hand)}","html.jr .app :is(.calling,.realm) b{font:700 calc(var(--hs)*22px)/1 var(--hand)}")
rep("html.jr .sheet .forgel li.fgsec{display:block;border:0;padding:12px 0 2px;font:700 calc(var(--hs)*24px)/1 var(--hand);color:var(--ink);min-height:0}","html.jr .sheet .forgel li.fgsec{display:block;border:0;padding:12px 0 2px;font:700 calc(var(--hs)*28px)/1 var(--hand);color:var(--ink);min-height:0}")
rep("html.jr .app .jplate span:last-child{font-size:13px;color:var(--muted)}","html.jr .app .jplate span:last-child{font-size:14px;color:var(--muted)}")
rep(".gres .gd{margin:0;font:400 15px/1 'VT323','Courier New',monospace;letter-spacing:.08em;text-transform:uppercase;color:#6B5A3A}",".gres .gd{margin:0;font:400 16px/1 'VT323','Courier New',monospace;letter-spacing:.08em;text-transform:uppercase;color:#6B5A3A}")
rep(".gres .gl{margin:8px 0 0;font:italic 400 15px/1.4 var(--body);color:#4B3C8C}",".gres .gl{margin:8px 0 0;font:italic 400 16px/1.4 var(--body);color:#4B3C8C}")
rep("html.jr .app .matestrip .rt b{font-size:calc(var(--hs,1)*21px)}","html.jr .app .matestrip .rt b{font-size:calc(var(--hs,1)*22px)}")
rep(".sseason small{font-size:13px;line-height:1.35}",".sseason small{font-size:14px;line-height:1.35}")
rep(".lpaper{position:relative;background:#FFF8EA;color:#3A2E25;border-radius:4px;padding:18px 18px 14px;margin:8px 0 14px;box-shadow:0 2px 8px rgba(0,0,0,.25);background-image:repeating-linear-gradient(transparent 0 27px,rgba(90,70,50,.12) 27px 28px);line-height:28px;font-size:15px}",".lpaper{position:relative;background:#FFF8EA;color:#3A2E25;border-radius:4px;padding:18px 18px 14px;margin:8px 0 14px;box-shadow:0 2px 8px rgba(0,0,0,.25);background-image:repeating-linear-gradient(transparent 0 27px,rgba(90,70,50,.12) 27px 28px);line-height:28px;font-size:16px}")
# explanations that fade after five days
rep("const inspHint=c=>","""const TIPS='forge-tips-v1';
function tipFade(k,el){if(!el)return;let t={};try{t=JSON.parse(localStorage.getItem(TIPS)||'{}')||{};}catch(e){t={};}
  const d=todayKey(),r=t[k]&&typeof t[k]==='object'?t[k]:{n:0,d:''};
  if(r.d!==d){r.n=(+r.n||0)+1;r.d=d;t[k]=r;try{localStorage.setItem(TIPS,JSON.stringify(t));}catch(e){}}
  if(r.n>5)el.remove();}
const inspHint=c=>""")
rep("""    <div class="row" style="justify-content:center"><button class="ghost" data-close>Close</button></div>`);
}
function fgMake(id){""","""    <div class="row" style="justify-content:center"><button class="ghost" data-close>Close</button></div>`);
  tipFade('forge',document.querySelectorAll('#modal p.muted.small')[1]);
}
function fgMake(id){""")
rep("if(up.length)ui.chSel=up[up.length-1];chooseSync();}","if(up.length)ui.chSel=up[up.length-1];chooseSync();tipFade('choose',document.querySelector('#modal h2 + p.muted.small'));}")
rep("""You write your Forgelings.</span></p>'}`;
  hydrate(el);
}""","""You write your Forgelings.</span></p>'}`;
  hydrate(el);
  if(ch.sub==='map')tipFade('maptap',el.querySelector('.mapwrap + p.muted.small.center'));else tipFade('twoinks',el.querySelector(':scope > p.muted.small:last-child'));
}""")
# one focal point at the Hearth; extras in plain type
rep("""
.inspback,.inspback *{overflow-wrap:anywhere}
</style>""","""
.inspback,.inspback *{overflow-wrap:anywhere}
/* 0.74: one focal point at the Hearth. When an action is ready, the others draw a lighter frame; the extras read in plain type */
html.jr .app .hgrid:has(.act.ready) .act:not(.ready){border-width:1px !important;padding:11px 5px !important}
html.jr .app .hmore .chip{font:700 16px/1.3 var(--body)}
</style>""")
# Japanese: binder captions at 22 px pushed the grid wider than the screen (their text set the column's minimum width)
rep("""html.jr .app .hmore .chip{font:700 16px/1.3 var(--body)}
</style>""","""html.jr .app .hmore .chip{font:700 16px/1.3 var(--body)}
html.jr .app .binder .jcap{width:0;min-width:100%}
</style>""")
# Found while checking Japanese (already in 0.73.1): the Hearth showed the companion's line as saved, in the language of that
#   moment; Settings glued "normal volume" and "184 Forgeling+s" from pieces. Now written when shown, as whole phrases.
rep("hf.msg=state.comp.line+(/new by the fire|new things by the fire/.test(hf.msg||'')?' '+hf.msg:'');}",
    "const cc=state.cards.find(x=>x.id===state.comp.cid),ow=todayOwnObj();hf.msg=(cc?compLine(cc,state.comp.f!==undefined?!!state.comp.f:!!ow&&ow.days.length<=1):state.comp.line)+(/new by the fire|new things by the fire/.test(hf.msg||'')?' '+hf.msg:'');}")
rep("""(S.vol||'normal')+' volume'""","""({quiet:'quiet volume',loud:'loud volume'})[S.vol]||'normal volume'""")
rep("""state.cards.length+' Forgeling'+(state.cards.length===1?'':'s')+' \\u00B7 save or restore a copy'""","""state.cards.length===1?'1 Forgeling \\u00B7 save or restore a copy':`${state.cards.length} Forgelings \\u00B7 save or restore a copy`""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk74.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk74.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
