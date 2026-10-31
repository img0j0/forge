# 0.46: the field journal (Hunter chose direction A on the UI canvas Wb4dmocNbNL9E8reVn17cr, boards "Field journal").
# The app becomes the Keeper's journal: a paper page on a desk, ribbon bookmarks for tabs, three hands (your
# handwriting in Caveat, the world's voice in italic world ink, the Forge's stamps in VT323), a lamplit page at night,
# a leather cover on first open, and a Plain print option. Today and the Binder get their journal layouts; the other
# pages take the journal's paper and type here and get their own layouts in 0.47. "Plain" keeps the old flat look.
import re,subprocess,base64
S=open('base45.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)

rep("const VERSION='prototype 0.45.0'","const VERSION='prototype 0.46.0'")
rep("<title>Forgelings (prototype 0.45.0)</title>","<title>Forgelings (prototype 0.46.0)</title>")
rep("const SEEN_V=50;","const SEEN_V=51;")

# ---------- the handwriting font (Caveat 700, OFL, Latin subset)
B64=open('/tmp/claude-0/-home-claude/3a1600c1-f458-5b63-b996-90af70055acb/scratchpad/fonts/caveat700.b64').read().strip()
i=S.index("@font-face{font-family:'VT323'"); j=S.index("}",i)+1
S=S[:j]+"@font-face{font-family:'Caveat';font-style:normal;font-weight:700;font-display:swap;src:url(data:font/woff2;base64,"+B64+") format('woff2')}"+S[j:]

# ---------- the journal replaces the living sky (Plain keeps the flat look); lamplight follows dusk, night or Dark
rep("""function lsApply(){const el=document.documentElement,on=lsOn();el.classList.toggle('ls',on);const ph=on?skyPhase():'',ink=on&&!skyDark()&&(ph==='day'||ph==='dawn')?'dark':'light';if(on)el.setAttribute('data-skyink',ink);else el.removeAttribute('data-skyink');return on;}""",
"""function jrLamp(){const S=state.settings,th=S.theme||'auto',ph=skyPhase(),dk=th==='dark'||(th==='auto'&&!!(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches));return th!=='light'&&dk||ph==='dusk'||ph==='night';}
function lsApply(){const el=document.documentElement,on=lsOn();el.classList.remove('ls');el.removeAttribute('data-skyink');el.classList.toggle('jr',on);
  if(on){const lamp=jrLamp();el.setAttribute('data-theme',lamp?'dark':'light');el.setAttribute('data-page',lamp?'lamp':'day');el.classList.toggle('plainhand',state.settings.hand===false);
    document.querySelectorAll('meta[name=theme-color]').forEach(m=>m.setAttribute('content',lamp?'#140F0C':'#3B2A22'));}
  else{el.removeAttribute('data-page');el.classList.remove('plainhand');const th=(state&&state.settings&&state.settings.theme)||'auto';if(th==='auto')el.removeAttribute('data-theme');else el.setAttribute('data-theme',th);}
  return false;}""")

# ---------- Settings: the page, and plain print
rep("""<div class="lbl2">Sky</div><p class="muted small" style="margin:2px 0 6px">The sky behind the app follows your day, from dawn to night, and the app’s colours follow the sky. Light and Dark set how bright it is. Plain keeps a quiet, flat look.</p><div class="chips" role="group" aria-label="Sky">${[['auto','Follows your day'],['day','Always day'],['night','Always night'],['plain','Plain']]""",
    """<div class="lbl2">The page</div><p class="muted small" style="margin:2px 0 6px">Your journal is paper by day and lamplit at dusk and night. Dark keeps it lamplit. Plain keeps a quiet, flat look instead of the journal.</p><div class="chips" role="group" aria-label="The page">${[['auto','Follows your day'],['day','Always day'],['night','Always lamplit'],['plain','Plain']]""")
rep("""`<button class="chip" data-setsky="${a[0]}" aria-pressed="${(S.sky||'auto')===a[0]}">${a[1]}</button>`).join('')}</div>`)}""",
    """`<button class="chip" data-setsky="${a[0]}" aria-pressed="${(S.sky||'auto')===a[0]}">${a[1]}</button>`).join('')}</div>${S.sky!=='plain'?`<div class="lbl2">Writing</div><p class="muted small" style="margin:2px 0 6px">Your words are handwritten in the journal. Plain print is easier to read for some people.</p><div class="chips" role="group" aria-label="Writing"><button class="chip" data-sethand="1" aria-pressed="${S.hand!==false}">Handwriting</button><button class="chip" data-sethand="0" aria-pressed="${S.hand===false}">Plain print</button></div>`:''}`)}""")
rep("SK={auto:'Follows your day',day:'Always day',night:'Always night',plain:'Plain'}","SK={auto:'Follows your day',day:'Always day',night:'Always lamplit',plain:'Plain'}")
rep("""  else if(b.dataset.setsky){""","""  else if(b.dataset.sethand){state.settings.hand=b.dataset.sethand==='1';save();lsApply();renderSettings();}
  else if(b.dataset.setsky){""")

# ---------- Today: a stamp for the day's calling beside the taped-in find
rep("""<h2>${c?esc(c.nick||c.name)+' joined your binder':'Today’s Forgeling is in your binder'}</h2>""",
    """${c&&VECTORS[c.v]?`<span class="jstamp" aria-hidden="true"><b>${esc(VECTORS[c.v].ability.toUpperCase())}</b><i>${esc(VECTORS[c.v].name.toUpperCase())} · ${dayN()}</i></span>`:''}<h2>${c?esc(c.nick||c.name)+' joined your binder':'Today’s Forgeling is in your binder'}</h2>""")

# ---------- Binder: prints with a handwritten caption
rep("""const slice=list.slice(bf.page*9,bf.page*9+9),w=Math.floor((vw()-32-24-20)/3),slots=[];""",
    """const jrb=document.documentElement.classList.contains('jr'),slice=list.slice(bf.page*9,bf.page*9+9),w=Math.floor((vw()-32-24-20-(jrb?36:0))/3),slots=[];""")
rep("""slots.push(c?`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}, ${RAR[c.rarity].name}">${cardHTML(c,{w,mini:true})}${c.fav?'<span class="favmark" aria-hidden="true">\\u2605</span>':''}</button>`""",
    """slots.push(c?`<button data-insp="${c.id}" aria-label="Look at ${c.nick?esc(c.nick)+' ('+esc(c.name)+')':esc(c.name)}, ${RAR[c.rarity].name}">${cardHTML(c,{w,mini:true})}${c.fav?'<span class="favmark" aria-hidden="true">\\u2605</span>':''}<span class="jcap" aria-hidden="true">${esc(c.nick||c.name)}</span></button>`""")

# ---------- the cover: first open is a leather journal
rep("""  openOverlay(`<canvas id="titleCv" aria-hidden="true"></canvas>
    <div class="title-top"><h1 class="wordmark" id="dlgTitle">Forgelings</h1><p class="tagline">One small thing a day.<br>A small creature to keep it.</p>""",
"""  const cov=lsOn(),img=cov?`<img src="${spriteURL({id:-1,seed:20261031,rarity:0,dark:false,theme:0,v:0,keep:'',bond:0,name:'',nick:''})}" alt="A small Forgeling waving from the cover">`:'';
  openOverlay(`<canvas id="titleCv" aria-hidden="true"></canvas>${cov?'<div class="jcover" aria-hidden="true"><span class="jstitch"></span><span class="jband"></span></div>':''}
    <div class="title-top">${cov?'<p class="jkick">The Keeper’s journal</p>':''}<h1 class="wordmark" id="dlgTitle">Forgelings</h1>${cov?'<div class="jlabel">'+img:''}<p class="tagline">One small thing a day.<br>A small creature to keep it.</p>${cov?'</div>':''}""")
rep("""  const sc=modal.querySelector('.scrim');sc.classList.add('titlemode');""","""  const sc=modal.querySelector('.scrim');sc.classList.add('titlemode');sc.classList.toggle('jcov',lsOn());""")

CSS=open('/home/claude/forge/journal46.css').read()
i=S.index("</style>",S.index("</style>")+1)
S=S[:i]+"\n"+CSS+"\n"+S[i:]

# ---------- What's New
rep("""<ul class="newlist"><li><b>Relics and gifts.</b>""","""<ul class="newlist"><li><b>A field journal.</b> Forgelings is now your journal: a paper page by day and lamplight at night, ribbon bookmarks for the tabs, today’s find taped in with its calling stamped beside it, and your binder as an album of prints. Prefer the old look? Choose Plain under Look and feel. Handwriting can be switched to plain print there too.</li><li><b>Relics and gifts.</b>""")
m=re.search(r'<ul class="newlist">(.*?)</ul>',S,re.S); items=re.findall(r'<li>.*?</li>',m.group(1),re.S)
assert len(items)==9,len(items); rep(items[-1],"")

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk46.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk46.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
