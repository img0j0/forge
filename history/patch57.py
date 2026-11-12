# 0.57: Japanese (Hunter, November 12: "lets do the japanese integration").
#   The English app is unchanged in what it says. Sentences that were glued together from English pieces are now whole
#   templates, so i18n/build.mjs can give each one Japanese word order: memoryLine, memoryHTML, gossipLine, mapLatest,
#   openNudge, openIsle and keptHTML's world line.
#   Card backs' "news from away" was saved as English text when a card was made. Each card now also keeps which event it
#   was (c.gev = [realm, kind, gap]), so the line is written in whatever language the app runs in; old cards get it from
#   the same deterministic pick, and a saved line that no longer matches keeps its own text.
#   Settings > Look and feel: a Language choice (English / 日本語), saved on this device ('forge-lang'), then a reload.
import re,subprocess,os
S=open('base561.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.56.1'","const VERSION='prototype 0.57.0'")
rep("<title>Forgelings (prototype 0.56.1)</title>","<title>Forgelings (prototype 0.57.0)</title>")

# memoryLine / memoryHTML
rep("""  if(cu&&dnum(todayKey())%2===0)return n+' turns '+cu.name.toLowerCase()+' over carefully. The first treasure they brought home.';
  if(c.source==='daily'&&dayDiff(c.date,todayKey())>0){
    if(c.own)return n+' remembers the day you chose “'+c.own+'”. That was the day you met.';
    return n+' remembers the day you had '+(DID[c.v]||'shown up')+'. That was the day you met.';
  }
  return cu?n+' keeps their first '+cu.name.toLowerCase()+' close beside the fire.':'';""",
"""  const cn=cu?cu.name.toLowerCase():'';
  if(cu&&dnum(todayKey())%2===0)return `${n} turns ${cn} over carefully. The first treasure they brought home.`;
  if(c.source==='daily'&&dayDiff(c.date,todayKey())>0){
    if(c.own)return `${n} remembers the day you chose “${c.own}”. That was the day you met.`;
    return DID[c.v]?`${n} remembers the day you had ${DID[c.v]}. That was the day you met.`:`${n} remembers the day you had shown up. That was the day you met.`;
  }
  return cu?`${n} keeps their first ${cn} close beside the fire.`:'';""")
rep("""  return '<div class="tale"><b>First treasure</b><p>'+esc(c.nick||c.name)+' brought home '+esc(cu.name.toLowerCase())+' on '+esc(dateLabel(c.firstFind.at))+'.</p>'+cImg(cu.id,40)+'</div>';""",
"""  return `<div class="tale"><b>First treasure</b><p>${esc(c.nick||c.name)} brought home ${esc(cu.name.toLowerCase())} on ${esc(dateLabel(c.firstFind.at))}.</p>${cImg(cu.id,40)}</div>`;""")

# gossip: whole sentences, and which event it was
rep("""function gossipLine(e,gap,dark){
  const w=gap<=9?'during the week that ':gap<=29?'during the weeks when ':'after the long quiet, when ';
  return 'Found '+w+EVENTS[e.realm][e.kind][dark?1:0]+'.';
}""","""function gossipLine(e,gap,dark){
  const ev=EVENTS[e.realm][e.kind][dark?1:0];
  return gap<=9?`Found during the week that ${ev}.`:gap<=29?`Found during the weeks when ${ev}.`:`Found after the long quiet, when ${ev}.`;
}
/* 0.57: the event a card's news came from, so the line follows the app's language */
const gevOK=v=>v===0||(Array.isArray(v)&&v.length===3&&v.every(Number.isInteger)&&!!EVENTS[v[0]]&&!!EVENTS[v[0]][v[1]]);
const gossipOf=c=>Array.isArray(c.gev)&&gevOK(c.gev)?gossipLine({realm:c.gev[0],kind:c.gev[1]},c.gev[2],c.dark):(c.gossip||'');""")
rep("""    const c=state.cards[i];if(c.era!==undefined&&c.gossip!==undefined)continue;""",
"""    const c=state.cards[i];if(c.era!==undefined&&c.gossip!==undefined&&c.gev!==undefined)continue;""")
rep("""    if(c.gossip===undefined){let txt='';if(prev){const pd=dnum(prev.date),g=d-pd;if(g>=3){const e=pickEvent(pd+1,d,c);if(e)txt=gossipLine(e,g,c.dark);}}c.gossip=txt;}""",
"""    if(c.gossip===undefined||c.gev===undefined){let txt='',gv=0;if(prev){const pd=dnum(prev.date),g=d-pd;if(g>=3){const e=pickEvent(pd+1,d,c);if(e){txt=gossipLine(e,g,c.dark);gv=[e.realm,e.kind,g];}}}
      if(c.gossip===undefined)c.gossip=txt;else if(c.gossip!==txt&&!(typeof LJ!=='undefined'&&LJ))gv=0;
      c.gev=gv;}""")
rep("""${c.gossip?`<div class="m5">${esc(c.gossip)}</div>`:''}""","""${gossipOf(c)?`<div class="m5">${esc(gossipOf(c))}</div>`:''}""")
rep("""if(c.gossip!==undefined&&typeof c.gossip!=='string')c.gossip='';""","""if(c.gossip!==undefined&&typeof c.gossip!=='string')c.gossip='';if(c.gev!==undefined&&!gevOK(c.gev))delete c.gev;""")
rep("""c.era=eraAt(dnum(c.date)).mood;c.gossip='';""","""c.era=eraAt(dnum(c.date)).mood;c.gossip='';c.gev=0;""")

# mapLatest
rep("""    return (a===0?'Today':a===1?'Yesterday':a+' days ago')+', '+nm+'. '+cap(EVENTS[e.realm][e.kind][mood==='dark'?1:0])+'.'+(a===0?' It happened in every Forge at once.':'');}}""",
"""    const ev=cap(EVENTS[e.realm][e.kind][mood==='dark'?1:0]);
    return a===0?`Today, ${nm}. ${ev}. It happened in every Forge at once.`:a===1?`Yesterday, ${nm}. ${ev}.`:`${a} days ago, ${nm}. ${ev}.`;}}""")

# openNudge, openIsle
rep("""<p class="muted">${c?n+' is in your binder, and t':'T'}he Hearth is ready whenever you are. A new card arrives tomorrow.</p>""",
"""<p class="muted">${c?`${n} is in your binder, and the Hearth is ready whenever you are.`:'The Hearth is ready whenever you are.'} A new card arrives tomorrow.</p>""")
rep("""${dk?'The other side of '+esc(THEMES[b].name)+'. ':''}Five places""","""${dk?`The other side of ${esc(THEMES[b].name)}. `:''}Five places""")

# keptHTML: the world line
rep("""${ev?'That day, '+esc(EVENTS[ev.realm][ev.kind][dk?1:0])+'.':'Nothing else was written down that day.'} ${era.n===nowE.n?'It is still going.':'It is the '+esc(nowE.n)+' now.'}""",
"""${ev?`That day, ${esc(EVENTS[ev.realm][ev.kind][dk?1:0])}.`:'Nothing else was written down that day.'} ${era.n===nowE.n?'It is still going.':`It is the ${esc(nowE.n)} now.`}""")

# Settings: language
rep("""`<div class="lbl2">Forgeling mood</div><p class="muted small">Which Forgelings you find""",
"""`<div class="lbl2">Language · 言語</div><div class="chips" role="group" aria-label="Language"><button class="chip" data-lang="en" lang="en" aria-pressed="${curLang()==='en'}">English</button><button class="chip" data-lang="ja" lang="ja" aria-pressed="${curLang()==='ja'}">日本語</button></div><div class="lbl2">Forgeling mood</div><p class="muted small">Which Forgelings you find""")
rep("""  if(b.dataset.setmood){state.settings.mood=b.dataset.setmood;""",
"""  if(b.dataset.lang){if(b.dataset.lang===curLang())return;try{localStorage.setItem('forge-lang',b.dataset.lang);}catch(_){}save();location.reload();}
  else if(b.dataset.setmood){state.settings.mood=b.dataset.setmood;""")
rep("""const sOn=()=>""","""/* 0.57: the language the app runs in (i18n/build.mjs sets LANG in the shipped app; the English build has none) */
const curLang=()=>typeof LANG!=='undefined'?LANG:'en';
const sOn=()=>""")

# the map's title lines, as their own text (the map drawing around them is not text)
rep(""">The Forge, as it is remembered</text>""",""">${'The Forge, as it is remembered'}</text>""")
rep("""font-size="10">In the ${esc(era.n)}</text>""","""font-size="10">${`In the ${esc(era.n)}`}</text>""")

# the Forge list: whole sentences for a piece's kind line and what it needs
rep("""<small>${r.what?r.kind+'. '+esc(r.what):r.kind}</small>""","""<small>${r.what?`${r.kind}. ${esc(r.what)}`:r.kind}</small>""")
rep("""  return `Needs ${r.sp} ${rn}${r.sp===1?'spare':'spares'} and ${r.emb} embers (you have ${sp} and ${e}).`;}""",
"""  return r.ti!==undefined?`Needs ${r.sp} ${mapName(r.ti)} ${r.sp===1?'spare':'spares'} and ${r.emb} embers (you have ${sp} and ${e}).`:`Needs ${r.sp} ${r.sp===1?'spare':'spares'} and ${r.emb} embers (you have ${sp} and ${e}).`;}""")
rep("""const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?mapName(r.ti)+' ':'';""","""const sp=spareTotal(r.ti),e=embers();""")

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk57.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk57.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
