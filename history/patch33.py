# Forgelings 0.33.0: pacing for the long run (Hunter found nearly every curio and most of the map in a week).
# 1. One new find a day: the day's first wander (or a great game round) can bring a new curio and a new place.
#    Later wanders that day bring back a spare, a little story and +1 bond, and the sheet says tomorrow's first wander
#    will find something new. A daily player now finds all 20 curios in about three weeks, not five days.
# 2. The map inks more slowly: a realm is fully inked at 10 Forgelings (was 6) and drawn at 4 (was 3).
#    Nothing goes backwards: state.mapMax remembers the highest stage each realm reached, and older saves are
#    grandfathered with the old thresholds on their first load.
# Reads base32.html.
src = open('base32.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- map pace, grandfathered ----
rep("const mapTier=n=>n>=6?3:n>=3?2:n>=1?1:0", "const mapTier=n=>n>=10?3:n>=4?2:n>=1?1:0,mapTierOld=n=>n>=6?3:n>=3?2:n>=1?1:0")
rep("""  return THEMES.map((T,ti)=>{const cs=state.cards.filter(c=>c.theme===ti);return{ti,n:cs.length,tier:mapPreview!=null?mapPreview:mapTier(cs.length),shade:cs.some(c=>c.dark)};});""",
    """  if(!Array.isArray(state.mapMax))state.mapMax=[0,0,0,0,0];
  return THEMES.map((T,ti)=>{const cs=state.cards.filter(c=>c.theme===ti),t=Math.max(mapTier(cs.length),state.mapMax[ti]||0);if(t>(state.mapMax[ti]||0))state.mapMax[ti]=t;return{ti,n:cs.length,tier:mapPreview!=null?mapPreview:t,shade:cs.some(c=>c.dark)};});""")
rep("function migrate(s){sanitize(s);", "function migrate(s){sanitize(s);if(!Array.isArray(s.mapMax))s.mapMax=[0,1,2,3,4].map(ti=>mapTierOld(s.cards.filter(c=>c.theme===ti).length));")
rep("""  if(s.giftsSent!==undefined&&!(Number.isInteger(s.giftsSent)&&s.giftsSent>=0))s.giftsSent=0;""",
    """  if(s.giftsSent!==undefined&&!(Number.isInteger(s.giftsSent)&&s.giftsSent>=0))s.giftsSent=0;
  if(s.mapMax!==undefined&&!(Array.isArray(s.mapMax)&&s.mapMax.length===5&&s.mapMax.every(x=>Number.isInteger(x)&&x>=0&&x<=3)))delete s.mapMax;
  if(s.disc!==undefined&&typeof s.disc!=='string')delete s.disc;""")
rep("function fresh(){const k=dkey(new Date());return {v:1,", "function fresh(){const k=dkey(new Date());return {v:1,mapMax:[0,0,0,0,0],")

# ---- one new find a day: wanders ----
rep("""  const to=Number.isInteger(w.realm)&&w.realm>=0?w.realm:-1,base=to>=0?rCurios(to):CURIOS,unfound=base.filter(x=>!state.curios[x.id]),pool=unfound.length?unfound:base,cu=pool[Math.floor(r()*pool.length)];""",
    """  const fresh=state.disc!==todayKey(),to=Number.isInteger(w.realm)&&w.realm>=0?w.realm:-1,base=to>=0?rCurios(to):CURIOS,unfound=fresh?base.filter(x=>!state.curios[x.id]):[],owned=base.filter(x=>state.curios[x.id]),anyOwned=CURIOS.filter(x=>state.curios[x.id]);
  const pool=unfound.length?unfound:owned.length?owned:fresh||!anyOwned.length?base:anyOwned,cu=pool[Math.floor(r()*pool.length)];""")
rep("""  let place='';{const open=[0,1,2,3,4].filter(t=>rKnownTi(t)&&placesFound(t)<5),dto=to>=0?(open.includes(to)?to:-1):(open.length?open[Math.floor(r()*open.length)]:-1);""",
    """  if(isNew)state.disc=todayKey();
  let place='';if(fresh){const open=[0,1,2,3,4].filter(t=>rKnownTi(t)&&placesFound(t)<5),dto=to>=0?(open.includes(to)?to:-1):(open.length?open[Math.floor(r()*open.length)]:-1);""")
rep("""      place=`<div class="tale new"><b>A new place on your map: ${esc(pl.n)}</b>""", """      state.disc=todayKey();place=`<div class="tale new"><b>A new place on your map: ${esc(pl.n)}</b>""")
# the quiet-path note for a second wander in a day
rep("""  let done='';const rq=state.request,ra=rq?cardById(rq.cid):null;
  if(rq&&ra&&to===rq.realm){""", """  let quiet='';if(!fresh&&c){const nm0=c.nick||c.name,more=CURIOS.some(x=>!state.curios[x.id])||[0,1,2,3,4].some(t=>rKnownTi(t)&&placesFound(t)<5);c.bond=(c.bond||0)+1;
    quiet=`<div class="tale"><b>A quiet path today</b><p class="small">The paths share one new find a day, and today’s is already home. ${esc(nm0)} wandered happily anyway and came back with a spare. Bond with ${esc(nm0)} +1.${more?' Tomorrow’s first wander will find something new.':''}</p></div>`;}
  let done='';const rq=state.request,ra=rq?cardById(rq.cid):null;
  if(rq&&ra&&to===rq.realm){""")
rep("""    <p class="muted small center">Curios found: ${have} of ${CURIOS.length}</p>${place}${isNew?talePageHTML(cu.id):''}${done}""",
    """    <p class="muted small center">Curios found: ${have} of ${CURIOS.length}</p>${place}${isNew?talePageHTML(cu.id):''}${quiet}${done}""")
# the destination sheet is honest about it
rep("""This first time, they are back in about 20 minutes.':'They are back in about three hours.'}</p>${opts}""",
    """This first time, they are back in about 20 minutes.':'They are back in about three hours.'}${state.disc===todayKey()?' Today’s new find is already home, so this wander brings back a spare, a story and a little bond.':''}</p>${opts}""")

# ---- one new find a day: great game rounds share it ----
rep("const ti=Math.abs(g.c.theme|0)%5,all=rCurios(ti),un=all.filter(x=>!state.curios[x.id]),pool=un.length?un:all,",
    "const ti=Math.abs(g.c.theme|0)%5,all=rCurios(ti),un=state.disc===todayKey()?[]:all.filter(x=>!state.curios[x.id]),own=all.filter(x=>state.curios[x.id]),pool=un.length?un:own.length?own:all,")
rep("cur.n++;state.curios[cu.id]=cur;state.games.curioDay=todayKey();const nw=cur.n===1,", "cur.n++;state.curios[cu.id]=cur;state.games.curioDay=todayKey();const nw=cur.n===1;if(nw)state.disc=todayKey();const ")

rep('<title>Forgelings (prototype 0.32.0)</title>', '<title>Forgelings (prototype 0.33.0)</title>')
rep("const VERSION='prototype 0.32.0'", "const VERSION='prototype 0.33.0'")
rep('const SEEN_V=36;', 'const SEEN_V=37;')
rep("""<ul class="newlist"><li><b>The map, inked.</b>""",
    """<ul class="newlist"><li><b>A slower, longer road.</b> The paths now share one new find a day: the day’s first wander can bring a new curio and a new place, and later wanders bring a spare, a story and a little bond. Realms also take more Forgelings to ink in fully. Nothing you have already found or drawn changes.</li>
    <li><b>The map, inked.</b>""")
import re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
