# 0.76: the Scribe writes the chapters (journal and book design doc, part 1; Hunter took all five recommendations
#   November 13, and asked to keep making the journal more engaging and personal while he was away).
#   - `scribeTell(from,to,week)` picks moments from a stretch of days and writes them as whole sentences: how the stretch
#     began (a calling and who came, or your own small thing), how often you came back (in words, never a count), a
#     season stamp, the realm your answers leaned to, the rarest find, a curio or a road postcard brought home, a letter,
#     your own photos, hard days done anyway. A month keeps six, a week three; nothing happened gets one quiet line.
#     Then one of your own lines, the longest, quoted ("The Scribe underlined it." once the Scribe has come).
#   - Where it shows: a chapter's title page (the current month says it is still being written); the Journal's
#     "Your month in words" and "This week" (the week keeps its best-find card, the calling chips are gone); and on a
#     Sunday evening, Close the day reads the week back before goodnight.
#   - The chapter's closing page no longer repeats the counts.
import re,subprocess,os
S=open('base75.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.75.0'","const VERSION='prototype 0.76.0'")
rep("<title>Forgelings (prototype 0.75.0)</title>","<title>Forgelings (prototype 0.76.0)</title>")
rep("/* ================= 0.75: one book, in chapters ================= */","""/* ================= 0.76: the Scribe writes the chapters ================= */
const SC_LEAN=['Your answers kept turning toward people: who you saw, and who you called.','Your answers kept turning toward making things with your hands.','Your answers kept asking for rest, and you let yourself have some.','Your answers kept asking for a clear head.','Your answers kept drifting somewhere far off, dreaming.'];
function scribeTell(from,to,week){
  const inR=k=>typeof k==='string'&&k>=from&&k<=to,today=todayKey(),out=[];let h=11;for(const ch of from)h=(h*33+ch.charCodeAt(0))>>>0;
  const hs=state.history.filter(x=>x&&inR(x.date)),seen=new Set(),done=hs.filter(x=>x.status==='done'&&!seen.has(x.date)&&seen.add(x.date)).sort((a,b)=>a.date<b.date?-1:1);
  const mn=ymName(from.slice(0,7)),pick=a=>a[h%a.length];
  if(!done.length)return {s:[week?'A quiet week. The fire kept itself, and it will be here when you come back.':`A quiet ${mn}. The fire kept itself, and it will be here when you come back.`],q:''};
  const f=done[0],fc=f.card!=null?cardById(f.card):null,fn=fc?(fc.nick||fc.name):'',FV=VECTORS[VECTORS[f.v]?f.v:0];
  if(fc&&fc.own)out.push(week?`The week began with your own small thing, \\u201C${esc(fc.own)}\\u201D.`:`${mn} began with your own small thing, \\u201C${esc(fc.own)}\\u201D.`);
  else if(fc)out.push(week?`The week began on a ${FV.name} day, and ${esc(fn)} came to the fire.`:`${mn} began on a ${FV.name} day, and ${esc(fn)} came to the fire.`);
  const a=from>state.startDate?from:state.startDate,b=to<today?to:today,span=Math.max(1,Math.round((new Date(b+'T00:00:00')-new Date(a+'T00:00:00'))/864e5)+1),ratio=done.length/span;
  const showed=ratio>=.85?'You came back to the fire almost every day.':ratio>=.5?'You came back most days, and rested when you needed to.':'It was a quieter stretch, with a few good days by the fire.';
  const hl=[];
  const SS=state.seasons||{},sk=Object.keys(SS).find(k=>inR(SS[k]));if(sk){const s=SEASONS.find(x=>sk.indexOf(x.id+'-')===0);if(s)hl.push([SS[sk],`${s.name} came, and you pressed its stamp on ${esc(dateLabel(SS[sk]))}.`]);}
  const n=[0,0,0,0,0];let any=0;done.forEach(x=>{const aa=askAns(x.date);if(aa&&aa[2]>=0&&aa[2]<=4){n[aa[2]]++;any++;}});const lean=any>=2?n.indexOf(Math.max(...n)):-1;
  const cards=state.cards.filter(c=>inR(c.date)&&!c.own).sort((x,y)=>y.rarity-x.rarity||x.id-y.id),best=cards[0];
  if(best&&best.rarity>=2)hl.push([best.date,`${esc(best.nick||best.name)}, a ${RAR[best.rarity].name} from ${realmName(best)}, turned up on ${esc(dateLabel(best.date))}.`]);
  const road=(state.pcGifts||[]).filter(g=>g&&g.t===1&&inR(g.d)),rg=road.length?pick(road):null,rc=rg?cardById(rg.c):null;
  if(rc)hl.push([rg.d,`${esc(rc.nick||rc.name)} sent you a postcard from ${mapName(rg.r)}.`]);
  else{const cu=Object.entries(state.curios||{}).filter(([id,v])=>v&&inR(v.at)&&cuById(id));if(cu.length){const [id,v]=pick(cu),cc=v.cid!=null?cardById(v.cid):null,C=cuById(id);
    if(cc&&C)hl.push([v.at,`${esc(cc.nick||cc.name)} brought home a curio from ${mapName(CREALM[id])}: ${C.name}.`]);}}
  const lt=(state.letters||[]).find(L=>L&&inR(L.d)),lc=lt?cardById(lt.c):null;if(lc)hl.push([lt.d,`${esc(lc.nick||lc.name)} wrote you a letter.`]);
  const pc=Object.keys(state.posts||{}).filter(inR).length;if(pc)hl.push(['~',pc===1?'You taped a photo of your own into the pages.':'You taped photos of your own into the pages.']);
  const hard=Object.keys(state.feel||{}).filter(k=>inR(k)&&state.feel[k]==='hard').length;if(hard>=2)hl.push(['~~','Some days were hard, and you did them anyway.']);
  const top=hl.slice(0,week?1:4).sort((x,y)=>x[0]<y[0]?-1:x[0]>y[0]?1:0).map(x=>x[1]);
  if(week){out.push(...top);out.push(lean>=0?SC_LEAN[lean]:showed);}
  else{out.push(showed);if(lean>=0)out.push(SC_LEAN[lean]);out.push(...top);}
  const used=new Set();if(!week)chMonths().filter(m=>m<from.slice(0,7)).forEach(m=>{const q=scQuote(...monthRange(m),used);if(q)used.add(q);});
  return {s:out.slice(0,week?3:6),q:scQuote(from,to,used)};}
function scQuote(from,to,used){const L=Object.keys(state.journal||{}).filter(k=>k>=from&&k<=to&&state.journal[k]&&state.journal[k].text).map(k=>state.journal[k].text).filter(t=>!used||!used.has(t)).sort((x,y)=>y.length-x.length||(x<y?-1:1));return L[0]||'';}
function scribeHTML(from,to,week,open){const t=scribeTell(from,to,week),sc=entryDays().size>=SCRIBE_AT;
  const para=a=>a.join(' ').replace(/([。！？]) /g,'$1'),P1=t.s.slice(0,3),P2=t.s.slice(3);
  return `<div class="scribe"><p class="world">${para(P1)}</p>${P2.length?`<p class="world">${para(P2)}</p>`:''}${t.q?`<p class="mine">\\u201C${esc(t.q)}\\u201D</p>${sc?'<p class="scby">The Scribe underlined it.</p>':''}`:''}${open?'<p class="scby">Still being written.</p>':''}</div>`;}
const monthRange=ym=>{const d=new Date(ym+'-01T00:00:00');d.setMonth(d.getMonth()+1);d.setDate(0);return [ym+'-01',dkey(d)];};
const weekRange=()=>{const t=todayKey(),d=new Date(t+'T00:00:00');d.setDate(d.getDate()-6);return [dkey(d),t];};
function scribeMonth(ym){const [a,b]=monthRange(ym);return scribeHTML(a,b,false,ym===todayKey().slice(0,7));}
/* ================= 0.75: one book, in chapters ================= */""")
# the chapter title page carries the chapter
rep("""<p class="muted small">${ymName(ym)} ${ym.slice(0,4)}${nm?` \\u00B7 named by ${esc(nm)}`:''}</p></div>`;}""","""<p class="muted small">${ymName(ym)} ${ym.slice(0,4)}${nm?` \\u00B7 named by ${esc(nm)}`:''}</p>${scribeMonth(ym)}</div>`;}""")
rep("function bkEnd(ym){const w=monthWords(ym),mn=ymName(ym);","function bkEnd(ym){const w='',mn=ymName(ym);")
# the Journal's month and week
rep("function monthHTML(){","""function monthHTML(){const k=todayKey(),cur=k.slice(0,7),pm=prevYM(),hasC=zineDays(cur).length,hasP=zineDays(pm).length;if(!hasC&&!hasP)return '';
  return `<div class="panel-box scribebox"><h2>Your month in words</h2>${hasC?scribeMonth(cur):''}${hasP?`<details class="more"${hasC?'':' open'}><summary>${ymName(pm)}</summary>${scribeMonth(pm)}</details>`:''}</div>`;}
function monthHTMLOld(){""")
rep("function recapHTML(){","""function recapHTML(){
  const [a,b]=weekRange(),days=lastDays(7).filter(k=>k>=state.startDate),cards=state.cards.filter(c=>days.includes(c.date)),best=cards.slice().sort((x,y)=>y.rarity-x.rarity||y.id-x.id)[0];
  return `<div class="panel-box scribebox"><h2>This week</h2>${scribeHTML(a,b,true,false)}${best?`<div class="chron" style="margin:10px 0 0;padding:8px"><button class="minibtn" data-insp="${best.id}" aria-label="Look at ${esc(best.nick||best.name)}">${cardHTML(best,{w:56,mini:true})}</button><div class="cbody"><b>Best find: ${esc(best.nick||best.name)}</b><div class="muted small">${RAR[best.rarity].name}, ${realmName(best)}</div></div></div>`:''}</div>`;}
function recapHTMLOld(){""")
# Sunday evening: Close the day reads the week back
rep("function closeDayHTML(){","""function closeDayHTML(){const h=closeDayHTML0();if(new Date(state.date+'T00:00:00').getDay()!==0||state.cards.length<3)return h;
  const [a,b]=weekRange(),wb=`<div class="weekback"><p class="muted small">Your week, as the Scribe tells it</p>${scribeHTML(a,b,true,false)}</div>`;return h.replace('<div class="gnrow">',wb+'<div class="gnrow">');}
function closeDayHTML0(){""")
rep("""html.reduce .jbook .zpage{animation:none !important}""","""html.reduce .jbook .zpage{animation:none !important}
/* 0.76: the Scribe's chapters */
.scribe{text-align:left;margin-top:12px}
.scribe .world{margin:0 0 8px;line-height:1.5}
.scribe .mine{margin:8px 0 2px}
.scby{font-size:14px;color:#6B5E7A;text-align:right;margin:0 0 4px;font-style:italic}
.bch .scribe{border-top:1px dotted rgba(90,70,50,.35);padding-top:10px}
.bch{justify-content:flex-start;padding-top:22px}
.scribebox .scribe{margin-top:4px}.scribebox .scby{color:inherit;opacity:.8}
.weekback{margin:10px 0;padding:10px 12px;border-left:3px solid rgba(201,150,46,.6)}""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk76.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk76.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
