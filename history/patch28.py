# Forge 0.28.0: a Forgeling that notices your days.
# 1. Showing up warms the bond: when you do the day's small thing, the first Forgeling by the fire (not today's new one,
#    not one out wandering) gains 1 bond and says something about it. Rest and missed days cost nothing.
# 2. It remembers what you wrote: every few days, from day 8 on, the Hearth brings back one of your margin lines from
#    7 to 60 days ago. You answer gently (I did it / Still on it / Let it go); the answer shows in the Journal.
# Reads base271.html.
src = open('base271.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep('/* Nav */', '''.mecho{border:1.5px dashed #E0A82E;border-radius:14px;padding:12px 14px;margin:8px 0;background:var(--surface)}
.mecho h2{margin:0 0 4px;font:600 16px var(--display)}
.mecho .q{margin:6px 0 0;color:var(--muted);font-size:13px}
.mecho .chips{margin-top:10px}
.mecho .chips button{min-height:44px}
.comp{margin:6px 0 0;font-size:14px}
.later{margin:2px 0 0;color:var(--muted);font-size:13px}
/* Nav */''')

# ---- save repair ----
rep("""  Object.keys(s.journal).forEach(k=>{const j=s.journal[k];if(!j||typeof j!=='object'||typeof j.text!=='string')delete s.journal[k];});""",
    """  Object.keys(s.journal).forEach(k=>{const j=s.journal[k];if(!j||typeof j!=='object'||typeof j.text!=='string')delete s.journal[k];else if(j.reply!==undefined&&!['did','still','let'].includes(j.reply))delete j.reply;});
  if(s.comp!==undefined&&s.comp!==null&&(typeof s.comp!=='object'||typeof s.comp.date!=='string'||!Number.isFinite(s.comp.cid)||typeof s.comp.line!=='string'))s.comp=null;
  if(s.mEcho!==undefined&&s.mEcho!==null&&(typeof s.mEcho!=='object'||typeof s.mEcho.date!=='string'||typeof s.mEcho.k!=='string'))s.mEcho=null;
  if(s.mEchoed!==undefined&&!Array.isArray(s.mEchoed))s.mEchoed=[];
  if(Array.isArray(s.mEchoed))s.mEchoed=s.mEchoed.filter(x=>typeof x==='string');""")

# ---- 1. showing up warms the bond ----
COMP_JS = r'''/* ---- 0.28: a Forgeling that notices your days ---- */
const COMP_L=[['{n} sat a little closer.','{n} did a small happy hop by the fire.','{n} saved you the warm spot.','{n} hums something that sounds like well done.'],
  ['{n} nodded once. From {n}, that is a lot.','{n} moved over to make room for you.','{n} kept the fire high for you.','{n} watched you come in, and looked quietly proud.']];
function companion(){
  return slotCards().filter(c=>c.id!==state.todayCard&&!(wOut()&&state.wander.id===c.id))[0]||null;
}
function compNotice(){
  const c=companion();if(!c){state.comp=null;return;}
  const before=bondLevel(c),L=COMP_L[c.dark?1:0],n=c.nick||c.name;
  c.bond=(c.bond||0)+1;
  const line=L[whash(dnum(state.date)*31+c.id)%L.length].replace(/\{n\}/g,n),after=bondLevel(c);
  state.comp={date:state.date,cid:c.id,line,up:after>before?after:0};
  hf.msg=line;
}
function compHTML(){
  const p=state.comp;if(!p||p.date!==state.date)return '';const c=cardById(p.cid);if(!c)return '';const n=c.nick||c.name;
  return `<p class="comp"><b>${esc(p.line)}</b> Showing up grew ${esc(n)}’s bond by 1.${p.up?` ${esc(n)} is now ${BOND_NAMES[p.up-1]}.`:''}</p>`;
}
/* ---- 0.28: it remembers what you wrote ---- */
const MECHO_GAP=5,SPOTS=['tucked under the rug','in the woodpile','between two warm stones','folded in its pocket','caught in the grass by the fire'];
function mEchoPick(){
  const k=todayKey();if(dayN()<8)return null;
  if(state.mEcho&&state.mEcho.date===k)return state.mEcho;
  if(state.mEcho&&dayDiff(state.mEcho.date,k)<MECHO_GAP)return null;
  const done=state.mEchoed||[];
  const ks=Object.keys(state.journal).filter(j=>{const d=dayDiff(j,k);return d>=7&&d<=60&&!done.includes(j)&&!state.journal[j].reply;}).sort();
  if(!ks.length)return null;
  const cp=companion();state.mEcho={date:k,k:ks[0],ans:null,cid:cp?cp.id:0};save();return state.mEcho;
}
function mEchoHTML(c0){
  const e=mEchoPick();if(!e)return '';const c=(e.cid&&slotCards().find(x=>x.id===e.cid))||c0;const j=state.journal[e.k];if(!j){state.mEcho=null;return '';}
  const n=esc(c.nick||c.name),V=VECTORS[j.v]||VECTORS[0],spot=SPOTS[whash(dnum(e.k))%SPOTS.length];
  if(e.ans)return `<div class="mecho" aria-live="polite"><h2>${n} found something ${spot}</h2><p class="mine">“${esc(j.text)}”</p><p class="small" style="margin:6px 0 0">${esc(e.line||'')}</p></div>`;
  return `<div class="mecho" aria-live="polite"><h2>${n} found something ${spot}</h2><p class="mine">“${esc(j.text)}”</p>
    <p class="q">You wrote this on ${esc(dateLabel(e.k))}, when the Forge asked: ${esc(V.question)}</p>
    <div class="chips" role="group" aria-label="How did it go?"><button class="chip" data-mecho="did">I did it</button><button class="chip" data-mecho="still">Still on it</button><button class="chip" data-mecho="let">Let it go</button></div></div>`;
}
const MECHO_L={did:['{n} looks very pleased for you, and puts it somewhere safe.','{n} gives a short, approving rumble and keeps it.'],
  still:['{n} tucks it back where it found it. No rush.','{n} puts it back carefully. It will keep.'],
  let:['{n} folds it into a paper boat and lets the fire take it.','{n} drops it in the fire. It crackles once, and is gone.']};
function mEchoAnswer(c,a){
  const e=state.mEcho;if(!e||e.ans||!state.journal[e.k])return;
  const L=MECHO_L[a];e.ans=a;e.line=L[c.dark?1:0].replace(/\{n\}/g,c.nick||c.name);
  state.journal[e.k].reply=a;state.mEchoed=(state.mEchoed||[]).concat(e.k);save();sfx('save');
  renderHearth();renderChronicle();
}
const LATER={did:'Later: you did it.',still:'Later: still on it.',let:'Later: you let it go.'};
'''
rep("function earnDaily(allIn){", COMP_JS + "function earnDaily(allIn){")
rep("""  state.progress++;let packGained=false;if(state.progress>=5){state.progress=0;state.packs++;packGained=true;}
  save();return {c,packGained};""",
    """  state.progress++;let packGained=false;if(state.progress>=5){state.progress=0;state.packs++;packGained=true;}
  compNotice();save();return {c,packGained};""")
rep("""<p class="muted">${esc(mirrorLine()||'Come back tomorrow for the next card.')}</p>${state.packs>0""",
    """<p class="muted">${esc(mirrorLine()||'Come back tomorrow for the next card.')}</p>${compHTML()}${state.packs>0""")

# ---- 2. the Hearth brings it back ----
rep("  const c=cs[hf.sel],lv=bondLevel(c)", "  if(tab==='hearth'&&state.comp&&state.comp.date===state.date&&!state.comp.seen){state.comp.seen=1;save();hf.msg=state.comp.line+(/new by the fire|new things by the fire/.test(hf.msg||'')?' '+hf.msg:'');}\n  const c=cs[hf.sel],lv=bondLevel(c)")
rep("    ${wPanelHTML(c,n)}\n", "    ${away?'':mEchoHTML(c)}${wPanelHTML(c,n)}\n")
rep("""  if(b.dataset.hslot!==undefined){hf.sel=+b.dataset.hslot;hf.msg='';renderHearth();}""",
    """  if(b.dataset.mecho&&c){const e=state.mEcho;mEchoAnswer((e&&e.cid&&cs.find(x=>x.id===e.cid))||c,b.dataset.mecho);return;}
  if(b.dataset.hslot!==undefined){hf.sel=+b.dataset.hslot;hf.msg='';renderHearth();}""")
# the Journal shows the answer
rep("""<p class="mine">\\u201C${esc(e.text)}\\u201D</p></div>`;}).join('');""",
    """<p class="mine">\\u201C${esc(e.text)}\\u201D</p>${e.reply?`<p class="later">${LATER[e.reply]}</p>`:''}</div>`;}).join('');""")

# ---- What's New ----
rep('<title>Forge (prototype 0.27.1)</title>', '<title>Forge (prototype 0.28.0)</title>')
rep("const VERSION='prototype 0.27.1';", "const VERSION='prototype 0.28.0';")
rep('const SEEN_V=31;', 'const SEEN_V=32;')
rep("""<ul class="newlist"><li><b>Places on the map.</b>""",
    """<ul class="newlist"><li><b>A Forgeling that notices.</b> When you do your small thing, the Forgeling by the fire notices, and your bond grows. Every so often it also brings back something you wrote in the margin a while ago, so you can say how it went.</li>
    <li><b>Places on the map.</b>""")
import re as _re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=_re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],_re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:10])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
