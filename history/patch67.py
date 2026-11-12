# 0.67: letters from your companion at page milestones (brainstorm plan, idea 3).
#   At 10, 30, 60, 100, 200, 365, 500, 730 and 1000 pages your companion writes you a letter. It quotes one of your
#   own answers (and replies to it in its own voice), one of your own lines if you wrote any, says which way your
#   answers lean, and counts your postcards. Bright and dark Forgelings write differently. A player who already has
#   many pages gets one letter, for the highest milestone passed. The letter is written when it is read (only which
#   answer and line it quotes is saved), so it follows the app's language. Today shows it until it is read; the Book
#   keeps them all ("Letters").
#   Save: state.letters = [{n, d, c, q, l, read}], state.letterAt = the last milestone written.
import re,subprocess,os
S=open('base66.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.66.0'","const VERSION='prototype 0.67.0'")
rep("<title>Forgelings (prototype 0.66.0)</title>","<title>Forgelings (prototype 0.67.0)</title>")

rep("function todayTask(){","""/* ================= 0.67: letters from your companion ================= */
const LETTER_AT=[10,30,60,100,200,365,500,730,1000];
const LET_OPEN={10:'Ten pages. That is a real start, and I have read every one.',30:'Thirty pages now. Your book has a ribbon, and I have read every page.',60:'Sixty pages. Someone with a quill reads with us now, but I always read them first.',100:'One hundred pages. I did not know a book could get this warm.',200:'Two hundred pages. Some nights I just sit and turn them.',365:'A whole year of pages. I have read every one, some of them twice.',500:'Five hundred pages. We are going to need a bigger shelf.',730:'Two years of pages. Thank you for letting me read them.',1000:'A thousand pages. I have no words for it, so I am using all of mine.'};
const LET_REPLY=['I liked reading that. People are good for you.','I could tell. You had that busy-hands look.','I hope it helped. You deserve the slow days.','I noticed. You see things clearly when you let yourself.','I wondered where you were. Somewhere nice, I hope.'];
const LET_REPLY_D=['Good. Keep your people close.','Good. Keep making things. It suits you.','Rest is not weakness. I would know.','Clear eyes. I respect that.','Dreaming is allowed, even here in the dark.'];
const LET_LEAN=['Most of your answers lean toward the people around you. I have started to notice it too.','Most of your answers lean toward making things. I can hear it in how you write.','Most of your answers lean toward rest. Good. Keep it that way.','Most of your answers lean toward thinking clearly. It shows.','Most of your answers lean toward dreaming. I like where your head goes.'];
function letterCheck(){
  if(!state||!state.cards.length)return;
  const P=entryDays().size,due=LETTER_AT.filter(x=>x<=P&&x>(state.letterAt||0));if(!due.length)return;
  const n=due[due.length-1],m=companion()||mateNow()||state.cards[state.cards.length-1];state.letterAt=n;
  const used=new Set((state.letters||[]).flatMap(x=>[x.q,x.l]).filter(Boolean)),pick=a=>{const f=a.filter(k=>!used.has(k)),b=(f.length?f:a).slice(-60);return b.length?b[Math.floor(Math.random()*b.length)]:'';};
  const q=pick(Object.keys(state.ask||{}).filter(k=>askAns(k)).sort()),l=pick(Object.keys(state.journal||{}).filter(k=>state.journal[k]&&state.journal[k].text).sort());
  state.letters=(state.letters||[]).concat([{n,d:state.date,c:m.id,q,l,read:0}]).slice(-40);
  hf.msg=`${m.nick||m.name} has left you a letter by the fire.`;save();}
const letterFrom=L=>{const c=cardById(L.c);return c?(c.nick||c.name):'A Forgeling';};
function letterHTML(i){
  const L=(state.letters||[])[i];if(!L)return '';const c=cardById(L.c),dk=!!(c&&c.dark),n=letterFrom(L),ps=[];
  ps.push(LET_OPEN[L.n]||`${L.n} pages now, and I have read every one.`);
  const a=L.q?askAns(L.q):null;if(a)ps.push(`On ${esc(dateLabel(L.q))}, your page said: “${esc(a[1])}” ${(dk?LET_REPLY_D:LET_REPLY)[a[2]]}`);
  const j=L.l&&state.journal[L.l]&&state.journal[L.l].text;if(j)ps.push(`You also wrote this, in your own hand: “${esc(j)}” I keep thinking about it.`);
  const cnt=[0,0,0,0,0];Object.keys(state.ask||{}).forEach(k=>{if(k<=L.d){const x=askAns(k);if(x)cnt[x[2]]++;}});const tot=cnt.reduce((s,x)=>s+x,0);if(tot>=3)ps.push(LET_LEAN[cnt.indexOf(Math.max(...cnt))]);
  const pc=Object.keys(state.posts||{}).filter(k=>k<=L.d).length;if(pc)ps.push(pc===1?'You sent me a postcard. It is on the wall.':`You have sent me ${pc} postcards. They are all on the wall.`);
  ps.push(dk?'I will keep the fire lit. Come back when you can.':'I will be here by the fire tomorrow, whatever kind of day it is.');
  return `<div class="csheet" data-k="letter"><p class="muted small center">A letter from ${esc(n)}, ${esc(dateLabel(L.d))}</p><div class="lpaper${dk?' dk':''}">${c?`<img class="lsprite" src="${spriteURL(c)}" alt="" width="64" height="64">`:''}<p class="lhi">${dk?'To the one who keeps my fire,':'Dear friend,'}</p>${ps.map(p=>`<p>${p}</p>`).join('')}<p class="lsign">— ${esc(n)}</p></div><div class="stack"><button class="primary" data-close>Fold it away</button>${(state.letters||[]).length>1?'<button class="ghost" id="bookLetters">All your letters</button>':''}</div></div>`;}
function openLetter(i){const L=(state.letters||[])[i];if(!L)return;const h=letterHTML(i);if(!L.read){L.read=1;save();renderToday();}openSheet(h);sfx('open');}
function lettersHTML(){
  const A=(state.letters||[]).map((L,i)=>[L,i]).reverse();
  return `<div class="csheet" data-k="letters"><h2>Letters</h2><p class="muted small">Your Forgelings write to you when your book reaches 10, 30, 60 and 100 pages, and on from there.</p><div class="group">${A.map(([L,i])=>`<button class="rowl" data-letter="${i}"><span class="rt"><b>From ${esc(letterFrom(L))}</b><span class="rs">For ${L.n} pages · ${esc(dateLabel(L.d))}</span></span><span class="chev" aria-hidden="true">›</span></button>`).join('')}</div><div class="stack"><button class="ghost" data-close>Close</button></div></div>`;}
const ENVELOPE='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>';
function todayTask(){""")
# Today: the unread letter
rep("  if(yearReady())rows.unshift(row('btnYear',","""  letterCheck();{const ui2=(state.letters||[]).map((L,i)=>[L,i]).filter(x=>!x[0].read).pop();if(ui2)rows.unshift(row('btnLetter',ENVELOPE,`A letter from ${esc(letterFrom(ui2[0]))}`,`For your first ${ui2[0].n} pages. It is waiting for you.`,'',true));}
  if(yearReady())rows.unshift(row('btnYear',""")
rep("  else if(b.id==='btnYear'){openSheet(yearHTML());}","""  else if(b.id==='btnYear'){openSheet(yearHTML());}
  else if(b.id==='btnLetter'){const u=(state.letters||[]).map((L,i)=>[L,i]).filter(x=>!x[0].read).pop();if(u)openLetter(u[1]);}""")
# the Book keeps them
rep("""${L>=30?'<button class="outline" id="bookRibbon" style="margin-top:6px">Open to an old page</button>':''}""","""${L>=30?'<button class="outline" id="bookRibbon" style="margin-top:6px">Open to an old page</button>':''}${(state.letters||[]).length?`<button class="outline" id="bookLetters" style="margin-top:6px">Letters (${state.letters.length})</button>`:''}""")
rep("  if(e.target.closest('#bookRibbon')){openRibbon();return;}","""  if(e.target.closest('#bookRibbon')){openRibbon();return;}
  if(e.target.closest('#bookLetters')){openSheet(lettersHTML());return;}
  {const lt=e.target.closest('[data-letter]');if(lt){openLetter(+lt.dataset.letter);return;}}""")
# the save
rep("  if(s.ask!==undefined){if(!s.ask","""  {const DK=/^\\d{4}-\\d{2}-\\d{2}$/;s.letterAt=Number.isInteger(s.letterAt)&&s.letterAt>=0?s.letterAt:0;
   s.letters=(Array.isArray(s.letters)?s.letters:[]).filter(x=>x&&Number.isInteger(x.n)&&x.n>0&&typeof x.d==='string'&&DK.test(x.d)&&Number.isFinite(x.c)).slice(-40).map(x=>({n:x.n,d:x.d,c:x.c,q:typeof x.q==='string'&&DK.test(x.q)?x.q:'',l:typeof x.l==='string'&&DK.test(x.l)?x.l:'',read:x.read?1:0}));}
  if(s.ask!==undefined){if(!s.ask""")
# a stray: the ribbon toast's "and 1 more" was English in Japanese, and Japanese ribbon toasts lost their medal look
rep("ribbonMsg='New ribbon: '+r.name+(add.length>1?' and '+(add.length-1)+' more':'');","ribbonMsg=add.length>1?`New ribbon: ${r.name}, and ${add.length-1} more`:`New ribbon: ${r.name}`;")
rep("t.classList.toggle('medal',/^New ribbon/.test(m));","t.classList.toggle('medal',/^(New ribbon|新しいリボン)/.test(m));")
css="""
/* 0.67: letters */
.lpaper{position:relative;background:#FFF8EA;color:#3A2E25;border-radius:4px;padding:18px 18px 14px;margin:8px 0 14px;box-shadow:0 2px 8px rgba(0,0,0,.25);background-image:repeating-linear-gradient(transparent 0 27px,rgba(90,70,50,.12) 27px 28px);line-height:28px;font-size:15px}
.lpaper p{margin:0 0 10px;line-height:1.75}.lpaper .lhi{font-weight:700}.lpaper .lsign{text-align:right;font-weight:700;margin-top:6px}
.lpaper.dk{background-color:#2A2233;color:#EDE4F6;background-image:repeating-linear-gradient(transparent 0 27px,rgba(255,255,255,.07) 27px 28px)}
.lsprite{float:right;width:64px;height:64px;image-rendering:pixelated;margin:-6px -4px 4px 8px}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk67.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk67.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
