# Forge 0.17.0: Echoes, the mirror, and the shared world.
# Applies count-asserted replacements to base16.html and writes work.html.
import sys
src = open('base16.html', encoding='utf8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:80]!r}'
    src = src.replace(old, new)

# ---- version ----
rep('<title>Forge (prototype 0.16.0)</title>', '<title>Forge (prototype 0.17.0)</title>')
rep("const VERSION='prototype 0.16.0';", "const VERSION='prototype 0.17.0';")
rep('const SEEN_V=19;', 'const SEEN_V=20;')

# ---- style: the echo sits inside the Today box, under a dashed rule ----
rep('.inkw{color:var(--plum);font-style:italic;font-weight:700}',
    '.inkw{color:var(--plum);font-style:italic;font-weight:700}\n'
    '.echo{margin-top:14px;padding-top:12px;border-top:1.5px dashed var(--line)}\n'
    '.echo .ghost{padding-left:0;margin-top:2px}\n'
    '.didlist{margin:8px 0 0;padding-left:20px;display:grid;gap:4px}')

# ---- Echoes and the mirror ----
ECHO_JS = r'''
/* ---- Echoes and the mirror (0.17.0): resurfacing what you already did. Nothing new to keep up with. ---- */
/* Said after "you've", in Vector order. These describe what the person did, never a score. */
const DID=['cut something that did not need doing','done the one thing that moves the rest','given something your full attention','shipped something before it was perfect','reached out to someone','done the hard thing first','done something just for fun','made something a little better','made room for quiet','said the thing you meant to say','fixed a small annoyance for good','put the phone away and stayed present'];
const ECHO_M=[1,2,3,6,9];
function addMonths(k,m){const p=String(k).split('-').map(Number),mo=p[1]-1+m,last=new Date(p[0],mo+1,0).getDate();return dkey(new Date(p[0],mo,Math.min(p[2],last)));}
/* One echo at most per day: the oldest card whose anniversary is today, preferring the daily card over pack finds. */
function echoFor(k){
  let best=null;
  for(const c of state.cards){
    if(!c||typeof c.date!=='string'||c.date>=k)continue;
    const age=dayDiff(c.date,k);if(!(age>=KEPT_DAYS))continue;
    let lab=null;
    if(age===KEPT_DAYS)lab='Two weeks ago today';
    for(const m of ECHO_M)if(addMonths(c.date,m)===k)lab=m===1?'A month ago today':m+' months ago today';
    for(let y=1;y<=20;y++)if(addMonths(c.date,12*y)===k){lab=y===1?'A year ago today':y+' years ago today';break;}
    if(!lab)continue;
    const score=age*2+(c.source==='daily'?1:0);
    if(!best||score>best.score)best={c,lab,score};
  }
  return best;
}
function echoHTML(){
  const e=echoFor(todayKey());if(!e)return '';
  const c=e.c,V=VECTORS[c.v]||VECTORS[0],fresh=keptAge(c)===KEPT_DAYS;
  return `<div class="echo"><p class="muted small" style="margin:0">${e.lab}</p><p>You found <b>${esc(c.nick||c.name)}</b> on a ${esc(V.name)} day.${fresh?' Its second reading has just opened.':''}</p><button class="ghost" data-kept="${c.id}">Read that day again</button></div>`;
}
/* How many times this calendar month the person has done today's kind of thing. */
function mirrorLine(){
  const v=state.todayV,k=todayKey(),from=k.slice(0,8)+'01';
  if(!DID[v])return '';
  const n=state.history.filter(h=>h.status==='done'&&h.v===v&&h.date>=from&&h.date<=k).length;
  if(n<1)return '';
  return n===1?`That's the first time this month you've ${DID[v]}.`:`That's ${n} times this month you've ${DID[v]}.`;
}
function didHTML(days){
  const from=days[0],to=days[days.length-1],cnt={};
  state.history.forEach(h=>{if(h.status==='done'&&h.v!=null&&DID[h.v]&&h.date>=from&&h.date<=to)cnt[h.v]=(cnt[h.v]||0)+1;});
  const top=Object.keys(cnt).map(Number).sort((a,b)=>cnt[b]-cnt[a]||a-b).slice(0,4);
  if(!top.length)return '';
  return `<p class="small" style="margin-top:12px">In these five weeks you've:</p><ul class="didlist small">${top.map(v=>`<li>${esc(DID[v])}${cnt[v]>1?`, ${cnt[v]} times`:''}</li>`).join('')}</ul>`;
}
'''
rep('const doneDays=()=>state.history.filter(h=>h.status===\'done\').length;',
    ECHO_JS + 'const doneDays=()=>state.history.filter(h=>h.status===\'done\').length;')

# Today, done: the mirror replaces the fixed sign-off, and the echo appears below.
rep('''<div><h2>Today's Forgeling is in your binder</h2><p class="muted">Come back tomorrow for the next card.</p></div></div>`;}''',
    '''<div><h2>Today's Forgeling is in your binder</h2><p class="muted">${esc(mirrorLine()||'Come back tomorrow for the next card.')}</p></div></div>${echoHTML()}`;}''')
# Today, resting: the echo still appears. It is a memory, not a task.
rep('''<div class="row"><button class="ghost" id="btnUnrest">Actually, show me today's card</button></div>`;''',
    '''<div class="row"><button class="ghost" id="btnUnrest">Actually, show me today's card</button></div>${echoHTML()}`;''')

# Journal tab: what you've actually done, under the five-week calendar.
rep('''<div class="cal">${head}${cells}</div></div>`;''',
    '''<div class="cal">${head}${cells}</div>${didHTML(days.filter(k=>k>=state.startDate))}</div>`;''')

# ---- The shared world: everyone's calendar is the same, so say so ----
rep('''return (a===0?'Today':a===1?'Yesterday':a+' days ago')+', '+nm+'. '+cap(EVENTS[e.realm][e.kind][mood==='dark'?1:0])+'.';}}''',
    '''return (a===0?'Today':a===1?'Yesterday':a+' days ago')+', '+nm+'. '+cap(EVENTS[e.realm][e.kind][mood==='dark'?1:0])+'.'+(a===0?' It happened in every Forge at once.':'');}}''')
rep('''<p class="muted small">Day ${d} of the world. Era ${E.k+1}, ${E.len-(d-E.start)} days left.</p>''',
    '''<p class="muted small">Day ${d} of the world. Era ${E.k+1}, ${E.len-(d-E.start)} days left. Every Forge shares this calendar.</p>''')

# ---- What is new ----
rep('''<ul class="newlist"><li><b>A map, mostly blank.</b>''',
    '''<ul class="newlist"><li><b>On this day.</b> When a Forgeling's anniversary comes round (two weeks, a month, a year), it may appear under today's card so you can read that day again.</li>
    <li><b>A mirror.</b> After today's card, the Forge notes how often this month you have done that kind of thing. The Journal shows the last five weeks the same way. No scores, just what you did.</li>
    <li><b>One world.</b> The world's events are the same in every Forge. If something happens today, it happened for everyone.</li>
    <li><b>A map, mostly blank.</b>''')

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
