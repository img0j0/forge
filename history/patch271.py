# Forge 0.27.1: gaps found in a full walkthrough.
# 1. One name per realm. The map, the wander sheet, wander returns, old tales, places and world events now all use the
#    name the Map shows (before, a lone Shade Forgeling could make the wander say Bramble while the map said Meadow).
# 2. No promise we can't keep: the morning nudge never sent anything. The first-day note now points to the Hearth and
#    the home-screen tip instead, and the dead setting is gone.
# 3. Copy: "Whispers and Chronicle" is now "Whispers and tales"; no "Chronicle" in player text; journal grammar on day 1;
#    the Tales tab says how to find pages once, not five times; no return toast on top of an open sheet.
src = open('base27.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# 1. realm names
rep("""function mapState(){""", """/* 0.27.1: one name per realm everywhere, the one the Map shows. */
function mapName(ti){if(!(ti>=0&&ti<=4))return 'somewhere';const m=mapState()[ti],mood=state.settings.mood,dk=mood==='dark'||(mood==='mix'&&whash(m.ti*7+m.tier)%2===0);return dk?THEMES[ti].dark.name:THEMES[ti].name;}
function mapState(){""")
rep("""function rName(ti){if(!(ti>=0&&ti<=4))return 'somewhere';const cs=state.cards.filter(c=>c.theme===ti);return REALM_PAGES[ti+'-'+(cs.length&&cs.every(c=>c.dark)?1:0)].t;}""",
    """function rName(ti){return mapName(ti);}""")
rep("const T=TALES[q.ti],n=talePages(q.ti),R=THEMES[q.ti].name;", "const T=TALES[q.ti],n=talePages(q.ti),R=mapName(q.ti);")
rep("TALES.map((T,ti)=>{const n=talePages(ti),R=THEMES[ti].name;", "TALES.map((T,ti)=>{const n=talePages(ti),R=mapName(ti);")
rep("That is the last place in ${esc(THEMES[dto].name)}.", "That is the last place in ${esc(mapName(dto))}.")
rep("Another place is drawn on your map of ${esc(THEMES[dto].name)}.", "Another place is drawn on your map of ${esc(mapName(dto))}.")
rep("days ago')}, ${esc(THEMES[e.realm].name)}.</b>", "days ago')}, ${esc(mapName(e.realm))}.</b>")
assert src.count("old ${THEMES[q.ti].name} tale") == 2
src = src.replace("old ${THEMES[q.ti].name} tale", "old ${mapName(q.ti)} tale")

# 2. the first-day note, without the nudge
i = src.index("function openNudge(){"); j = src.index("/* Weekly pack */", i)
src = src[:i] + r"""function openNudge(){
  const c=state.cards[state.cards.length-1],n=c?esc(c.nick||c.name):'';
  openSheet(`<h2>That’s your first day</h2><p class="muted">${c?n+' is in your binder, and t':'T'}he Hearth is ready whenever you are. A new card arrives tomorrow.</p>
    ${c?`<h3 style="margin:14px 0 0">Something to try now</h3><p class="muted small">At the Hearth, send ${n} out to wander. This first time they are back in about 20 minutes, with something small for your shelf.</p>`:''}
    ${installTipHTML().replace('class="setblock"','class="setblock" style="margin-top:12px"')}
    <div class="stack" style="margin-top:12px">${c?'<button class="primary" id="fdHearth">Go to the Hearth</button>':''}</div>
    <div class="row" style="justify-content:center"><button class="ghost" data-close>${c?'Maybe later':'Got it'}</button></div>`);
}

""" + src[j:]
rep("""  else if(b.id==='nudgeOk'){""", """  else if(b.id==='fdHearth'){closeModal();tab='hearth';render();window.scrollTo(0,0);}
  else if(b.id==='nudgeOk'){""")
i = src.index('    <div class="setblock"><b>Morning nudge</b>'); j = src.index('    ${installTipHTML()}', i)
src = src[:i] + src[j:]

# 3. copy
rep("Whispers and Chronicle ${S.lore!==false?'on':'off'}", "Whispers and tales ${S.lore!==false?'on':'off'}")
rep("<p class=\"muted\">Your Chronicle begins with your first Forgeling.</p>", "<p class=\"muted\">Your Forgelings and their tales appear here once you find your first one.</p>")
rep("""    <p>You showed up on <b>${done}</b> of the last ${days.length} ${days.length===1?'day':'days'}${rest?`, and rested on ${rest}`:''}.</p>""",
    """    <p>${days.length===1?(done?'You showed up today.':'This week starts today.'):`You showed up on <b>${done}</b> of the last ${days.length} days${rest?`, and rested on ${rest}`:''}.`}</p>""")
rep("""<p class="muted small" style="margin:0">${any?`No pages yet. Send a Forgeling to wander in ${R}.`:'Send a Forgeling wandering to find your first curio.'}</p>""",
    """<p class="muted small" style="margin:0">${any?`No pages yet. Send a Forgeling to wander in ${R}.`:'No pages yet.'}</p>""")
rep("""Each of its four curios remembers one page. Wander a realm to bring its pages home.</p>`+""",
    """Each of its four curios remembers one page. Wander a realm to bring its pages home.${any?'':' Your first wander starts at the Hearth.'}</p>`+""")
rep("if(!w.notified){w.notified=true;save();toast((c.nick||c.name)+' is back from wandering.');chime(1);render();}",
    "if(!w.notified){w.notified=true;save();if(modal.hidden)toast((c.nick||c.name)+' is back from wandering.');chime(1);render();}")

rep('<title>Forge (prototype 0.27.0)</title>', '<title>Forge (prototype 0.27.1)</title>')
rep("const VERSION='prototype 0.27.0';", "const VERSION='prototype 0.27.1';")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
