# Forgelings 0.40.1: a statue to look forward to. Any Forgeling's statue can be previewed in clay: the same 3D shape in
# plain stone, no colours, no keepsake, no stand, turnable by hand. The Forge's Statues section shows the Forgeling
# closest to Forgebound with its points to go and a Preview; the companion panel at the Hearth says a statue waits at
# Forgebound (or is ready to cast, or opens it). The full colours, shine and realm stand stay the reward for casting.
# Reads base40.html.
src = open('base40.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# clay: the figure without colour or keepsake
rep("function statueSprite(c){\n  const cc=Object.assign({},c,{keep:c.statue?c.statue.keep:(c.keep||'')}),",
    "function statueSprite(c,clay){\n  const cc=Object.assign({},c,{keep:clay?'':(c.statue?c.statue.keep:(c.keep||''))}),")
rep("    col[i]=[r/255,gg/255,b/255];out[i]=sl===1?1:0;}\n  return {col,out};",
    "    if(clay){const L=Math.round((.3*r+.59*gg+.11*b)/255*4)/4;col[i]=sl===1?[.30,.28,.34]:[.50+.36*L,.48+.36*L,.54+.34*L];}else col[i]=[r/255,gg/255,b/255];out[i]=sl===1?1:0;}\n  return {col,out};")
rep("function statueFigure(c){\n  const {col,out}=statueSprite(c),", "function statueFigure(c,clay){\n  const {col,out}=statueSprite(c,clay),")
rep("st=statueStand(c.theme,c.dark),fig=statueFigure(c);", "st=statueStand(c.theme,c.dark),fig=statueFigure(c,o.clay);if(o.clay)st.gc=[.78,.72,.9];")
rep("holo=c.rarity===3?1:c.rarity===4?2:0;", "holo=o.clay?0:c.rarity===3?1:c.rarity===4?2:0;")
rep("const v={yaw:-.35,pitch:.28,zoom:1,turn:!REDUCE,base:true,", "const v={yaw:-.35,pitch:.28,zoom:1,turn:!REDUCE,base:!o.clay,")
# the preview sheet
rep("function keepName(k){",
    "/* 0.40.1: preview a statue in clay before it can be cast */\n"
    "const bondToGo=c=>Math.max(0,BOND_AT[4]-(c.bond||0));\n"
    "function openStatuePreview(id){\n"
    "  const c=cardById(id);if(!c)return;if(stv){stv.stop();stv=null;}const n=c.nick||c.name,left=bondToGo(c);\n"
    "  ovMode='statue';\n"
    "  openOverlay(`<div class=\"stview\" style=\"--sg:#C9B8FF\"><p class=\"rv-title\">${esc(n)}’s statue, in clay</p><p class=\"stsub\">A preview · ${left?`${left} more bond ${left===1?'point':'points'} to Forgebound`:'Ready to cast at the Forge'}</p>\n"
    "    <div class=\"stcan\"><canvas id=\"stCv\" tabindex=\"0\" role=\"img\" aria-label=\"A clay preview of ${esc(n)}'s statue. Drag to turn it, pinch or scroll to zoom, arrow keys to turn.\"></canvas><p class=\"stno\" id=\"stNo\" hidden>This phone could not start 3D drawing, so here is ${esc(n)} as on the card.<img src=\"${spriteURL(c)}\" alt=\"${esc(n)}\"></p></div>\n"
    "    <p class=\"rv-hint\">This is ${esc(n)}’s shape. When ${esc(n)} is Forgebound, cast it at the Forge for ${STATUE_EMB} embers and it comes to life in full colour, wearing its keepsake, on a stand from ${esc(realmName(c))}.</p>\n"
    "    <div class=\"row stbtns\"><button class=\"chip\" id=\"stTurn\" aria-pressed=\"${!REDUCE}\">Turntable</button></div>\n"
    "    <button class=\"ghost\" id=\"ovClose\">Close</button></div>`,true);\n"
    "  ovMode='statue';const cv=$('#stCv');stvId=null;stv=statueView(cv,c,{clay:true});\n"
    "  if(!stv){cv.hidden=true;$('#stNo').hidden=false;const b=$('#stTurn');if(b)b.hidden=true;}\n"
    "  const f=$('#ovClose');if(f)f.focus({preventScroll:true});\n"
    "}\n"
    "function keepName(k){")
# the Forge: Forgebound rows as before, plus the closest Forgeling still on its way, each with a clay Preview
rep("  if(!fb.length)return `<h3 class=\"fgh\">Statues</h3><p class=\"muted small\">When a Forgeling becomes Forgebound (bond 5), the Forge can cast it as a 3D statue for ${STATUE_EMB} embers.</p>`;",
    "  const near=state.cards.filter(c=>bondLevel(c)<5).sort((a,b)=>(b.bond||0)-(a.bond||0)||a.id-b.id)[0];\n"
    "  const nearHTML=near?`<li><span class=\"fi\" aria-hidden=\"true\"><img class=\"cimg\" src=\"${spriteURL(near)}\" width=\"30\" height=\"30\" alt=\"\"></span><span><b>${esc(near.nick||near.name)}’s statue</b><small>Closest to Forgebound: ${bondToGo(near)} more bond ${bondToGo(near)===1?'point':'points'}.</small></span><button class=\"chip\" data-spre=\"${near.id}\">Preview</button></li>`:'';\n"
    "  if(!fb.length)return `<h3 class=\"fgh\">Statues</h3><p class=\"muted small\">When a Forgeling becomes Forgebound (bond 5), the Forge can cast it as a 3D statue for ${STATUE_EMB} embers. Preview one in clay now.</p>${nearHTML?`<ul class=\"furn forgel\">${nearHTML}</ul>`:''}`;")
rep("return `<li class=\"${ok?'on':can?'can':''}\"><span class=\"fi\" aria-hidden=\"true\"><img class=\"cimg\" src=\"${spriteURL(c)}\" width=\"30\" height=\"30\" alt=\"\"></span><span><b>${esc(n)}’s statue</b><small>Statue. ${esc(n)} in 3D on a ${esc(realmName(c))} stand.</small><small>${ok?`Cast ${esc(dateLabel(c.statue.at))}.`:`Needs ${STATUE_EMB} embers (you have ${e}).`}</small></span>${ok?`<button class=\"chip\" data-statue=\"${c.id}\">See it</button>`:can?`<button class=\"chip\" data-scast=\"${c.id}\">Cast it</button>`:''}</li>`;}).join('')}</ul>`;",
    "return `<li class=\"${ok?'on':can?'can':''}\"><span class=\"fi\" aria-hidden=\"true\"><img class=\"cimg\" src=\"${spriteURL(c)}\" width=\"30\" height=\"30\" alt=\"\"></span><span><b>${esc(n)}’s statue</b><small>Statue. ${esc(n)} in 3D on a ${esc(realmName(c))} stand.</small><small>${ok?`Cast ${esc(dateLabel(c.statue.at))}.`:`Needs ${STATUE_EMB} embers (you have ${e}).`}</small></span>${ok?`<button class=\"chip\" data-statue=\"${c.id}\">See it</button>`:can?`<button class=\"chip\" data-scast=\"${c.id}\">Cast it</button>`:`<button class=\"chip\" data-spre=\"${c.id}\">Preview</button>`}</li>`;}).join('')}${nearHTML}</ul>`;")
# the companion panel at the Hearth
rep("""Bond never fades.`:'Forgebound. A golden glow outlines '+esc(n)+'.'}</p>""",
    """Bond never fades.`:'Forgebound. A golden glow outlines '+esc(n)+'.'}</p>
      <p class="small stline">${c.statue?`<button class="ghost" data-statue="${c.id}">See ${esc(n)}’s statue</button>`:lv>=5?`${esc(n)}’s statue is ready to cast at the Forge. <button class="ghost" data-spre="${c.id}">Preview</button>`:`A statue waits at Forgebound. <button class="ghost" data-spre="${c.id}">Preview it in clay</button>`}</p>""")
# clicks
rep("  if(b.dataset.statue){openStatue(+b.dataset.statue);return;}", "  if(b.dataset.statue){openStatue(+b.dataset.statue);return;}\n  if(b.dataset.spre){openStatuePreview(+b.dataset.spre);return;}")
rep("  else if(b.dataset.statue)openStatue(+b.dataset.statue);", "  else if(b.dataset.statue)openStatue(+b.dataset.statue);\n  else if(b.dataset.spre)openStatuePreview(+b.dataset.spre);")
rep(".fgh{font:600 16px var(--display);margin:14px 0 4px}", ".fgh{font:600 16px var(--display);margin:14px 0 4px}\n.stline{margin:4px 0 0;display:flex;align-items:center;flex-wrap:wrap;gap:0 8px;color:var(--muted)}.stline .ghost{min-height:44px;padding:0 4px}")
# what's new: mention the preview in the statues note
rep("Find statues on the Forge panel at the Hearth and on the card's close-up.</li>",
    "Find statues on the Forge panel at the Hearth and on the card's close-up, and preview any Forgeling's statue in clay before it is Forgebound.</li>")
rep('<title>Forgelings (prototype 0.40.0)</title>', '<title>Forgelings (prototype 0.40.1)</title>')
rep("const VERSION='prototype 0.40.0'", "const VERSION='prototype 0.40.1'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
