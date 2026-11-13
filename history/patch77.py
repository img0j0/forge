# 0.77: tucked in (journal and book design doc, part 4; Hunter asked to keep making the journal engaging and personal).
#   - A day's spread now holds what happened that day: postcards a Forgeling sent or brought home (`pcGifts` by date),
#     the season stamp if it was pressed that day, curios found that day (who brought them), and a folded letter on the
#     day it was written (tap to read). Pressed snowflakes and ribbons keep no date, so they stay where they are.
#   - Margin notes: on about one day in three with an answer, the day's Forgeling writes a short note in the margin in
#     its own voice (bright or Shade), shaped by the realm your answer leaned to (`MARGIN_C`/`MARGIN_D`).
#   - Doodles: on about one day in eleven, the day's Forgeling draws itself in your margin, in ink.
#   - Say more: once the day's question is answered and you have not written, a quiet "Say more" opens your words with
#     the question and your answer above them. Never counted, never a nudge.
import re,subprocess,os
S=open('base76.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.76.0'","const VERSION='prototype 0.77.0'")
rep("<title>Forgelings (prototype 0.76.0)</title>","<title>Forgelings (prototype 0.77.0)</title>")
rep("/* ================= 0.75: one book, in chapters ================= */","""/* ================= 0.77: tucked in ================= */
const MARGIN_C=[["You came back smelling like someone else's kitchen. I approve.","Whoever you saw today, tell them a Forgeling says hello."],
 ['You had ink on your hands again. Good.','I tried to make something too. It is a pebble. It is perfect.'],
 ['You rested, and I napped next to the page. Fair trade.','Slow days count. I wrote that down for you.'],
 ['Your thoughts looked tidier today. I could see right through them.','You found the one thing that mattered. I underlined it.'],
 ['You were somewhere far off today. Bring me back a souvenir.','I dreamed about your page. It had stars on it.']];
const MARGIN_D=[['You were with people today. I could tell. You stood taller.','Someone was glad to see you. So was I.'],
 ['You built something. I heard the hammering from here.','Rough edges are still edges. Keep going.'],
 ['You rested. The fire did the work. That is allowed.','Quiet day. I kept watch so you did not have to.'],
 ['Clear head, clear sky. I like you like this.','You cut away the noise. I heard the quiet.'],
 ['You wandered in your head again. I followed, a little.','Far-off thoughts. I keep them safe in the margin.']];
function bkTucked(k){const out=[];
  (state.pcGifts||[]).forEach(g=>{if(g&&g.d===k)out.push(giftFig(g));});
  const SS=state.seasons||{},sk=Object.keys(SS).find(x=>SS[x]===k),s=sk?SEASONS.find(x=>sk.indexOf(x.id+'-')===0):null;
  if(s)out.push(`<p class="bstamp bseas">${seasonStampSVG(s,30,true)}<span>${s.name}</span></p>`);
  Object.entries(state.curios||{}).forEach(([id,v])=>{const C=cuById(id);if(!v||v.at!==k||!C)return;const cc=v.cid!=null?cardById(v.cid):null;
    out.push(`<p class="bcurio">${cImg(id,32,{alt:''})}<span>${cc?`${C.name}, brought home by ${esc(cc.nick||cc.name)}`:C.name}</span></p>`);});
  return out.join('');}
function bkMargin(k,c){if(!c)return '';const out=[],d=dnum(k),a=askAns(k),n=esc(c.nick||c.name);
  if(a&&a[2]>=0&&a[2]<=4&&d%3===0){const L=(c.dark?MARGIN_D:MARGIN_C)[a[2]],t=L[(d>>2)%L.length];
    out.push(`<div class="bnote"><img src="${spriteURL(c)}" alt="" width="40" height="40"><p>${t}</p><span>${n}, in the margin</span></div>`);}
  if(d%11===5)out.push(`<figure class="bdood"><img src="${spriteURL(c)}" alt="" width="56" height="56"><figcaption>${n} drew itself in your margin.</figcaption></figure>`);
  (state.letters||[]).forEach((L,i)=>{if(!L||L.d!==k)return;const lc=cardById(L.c),ln=lc?esc(lc.nick||lc.name):'';
    out.push(`<button class="bletter" data-letter="${i}"><b>${ln?`A letter from ${ln}`:'A letter'}</b><span>Tap to read</span></button>`);});
  return out.join('');}
function sayMoreLead(){const k=state.date,Q=askFor(k),a=askAns(k);return a?`<p class="saylead"><i>${esc(Q.q)}</i> You answered: ${esc(a[0])}.</p>`:'';}
const SAYBTN='<button class="ghost" id="askMore" style="min-height:44px">Say more</button>';
/* ================= 0.75: one book, in chapters ================= */""")
# the spread: tucked-in things on the left, margin on the right
rep("""${p?pcFig(k,p,'inb'):''}</div><div class="br">""","""${p?pcFig(k,p,'inb'):''}${bkTucked(k)}</div><div class="br">""")
rep("""${e&&e.reply&&LATER[e.reply]?`<p class="later">${LATER[e.reply]}</p>`:''}</div></div></div>`;}""","""${e&&e.reply&&LATER[e.reply]?`<p class="later">${LATER[e.reply]}</p>`:''}${bkMargin(k,c)}</div></div></div>`;}""")
# Say more: after the day's question, when nothing is written yet
rep("function askHTML(){","""function askHTML(){const h=askHTML0(),k=state.date,jr=state.journal[k];if(jr&&jr.text||!askAns(k))return h;return h.replace(/(<button class="ghost" id="askAgain")/,SAYBTN+'$1');}
function openSayMore(){openMargin();const f=modal.querySelector('.sheet label.field');if(f)f.insertAdjacentHTML('beforebegin',sayMoreLead());}
function askHTML0(){""")
rep("  if(b.id==='askAgain'){","""  if(b.id==='askMore'){openSayMore();return;}
  if(b.id==='askAgain'){""")
rep(""".weekback{margin:10px 0;padding:10px 12px;border-left:3px solid rgba(201,150,46,.6)}""",""".weekback{margin:10px 0;padding:10px 12px;border-left:3px solid rgba(201,150,46,.6)}
/* 0.77: tucked in */
.bday .pcard.gift{margin:8px auto 0;transform:rotate(-4deg);max-width:220px}
.bday .pcard.gift img{width:100%;height:auto}
.bseas{justify-content:flex-start;margin:10px 0 0;transform:rotate(-3deg)}
.bcurio{display:flex;gap:8px;align-items:center;margin:8px 0 0;font-size:14px;color:#4A4366}.bcurio img{image-rendering:pixelated;flex:none}
.bnote{position:relative;margin:12px 0 4px;padding:6px 0 0 48px;min-height:44px}
.bnote img{position:absolute;left:0;top:4px;image-rendering:pixelated}
.bnote p{margin:0;font:700 20px/1.15 var(--hand,cursive);color:#5A4A8F}
.bnote span{display:block;font-size:13px;color:#6B5E7A;margin-top:2px}
.bdood{margin:10px 0 0;text-align:right}
.bdood img{image-rendering:pixelated;filter:grayscale(1) sepia(.6) contrast(1.6) brightness(.9);opacity:.75;transform:rotate(-8deg)}
.bdood figcaption{font-size:13px;color:#6B5E7A;font-style:italic}
.bletter{display:block;width:100%;min-height:56px;margin:12px 0 0;padding:10px 14px;text-align:left;background:#F4EAD2;border:1px solid #D9CBA8;color:#2E2A47;transform:rotate(-1.5deg);box-shadow:0 2px 3px rgba(0,0,0,.18);font:inherit;cursor:pointer;position:relative}
.bletter::after{content:'';position:absolute;right:14px;bottom:-8px;width:22px;height:22px;border-radius:50%;background:#B83A3A}
.bletter b{display:block;font:700 22px/1.1 var(--hand,cursive)}.bletter span{font-size:13px;color:#4A4366}
.saylead{margin:4px 0 10px}""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk77.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk77.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
