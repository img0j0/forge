# 0.71: the Scribe's monthly book (brainstorm plan, idea 10).
#   Every month with pages becomes a little stitched book you flip through: a cover (the month, how many pages and
#   postcards), one page per day (its postcard, its words, your own words), and a back page with the month in words.
#   In the first week of a month, Today says last month is bound (by the Scribe, once you have met it). The Book keeps
#   them all ("Monthly books"). "Save as a picture" makes a shareable picture of the month with no photos and no
#   words of yours in it: the numbers and the Forgelings you found.
#   Save: state.zineSeen = the last month whose "bound" note was opened.
import re,subprocess,os
S=open('base70.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.70.0'","const VERSION='prototype 0.71.0'")
rep("<title>Forgelings (prototype 0.70.0)</title>","<title>Forgelings (prototype 0.71.0)</title>")

rep("function todayTask(){","""/* ================= 0.71: the Scribe's monthly book ================= */
const ymName=ym=>MONTHS_L[+ym.slice(5,7)-1];
const zineDays=ym=>[...entryDays()].filter(k=>k.slice(0,7)===ym).sort();
const zineMonths=()=>[...new Set([...entryDays()].map(k=>k.slice(0,7)))].sort().reverse();
function prevYM(){const d=new Date(todayKey()+'T00:00:00');d.setDate(1);d.setMonth(d.getMonth()-1);return dkey(d).slice(0,7);}
function zinePageHTML(ym,p){
  const ks=zineDays(ym),N=ks.length+2,mn=ymName(ym),pc=ks.filter(k=>(state.posts||{})[k]).length;
  if(p<=0)return `<div class="zpage zcover"><p class="zk">${ym.slice(0,4)}</p><h3>${mn}</h3><p>${ks.length===1?'One page':`${ks.length} pages`}${pc?(pc===1?', one postcard':`, ${pc} postcards`):''}</p><p class="muted small">${entryDays().size>=SCRIBE_AT?'Stitched together by the Scribe.':'Stitched together by the fire.'}</p></div>`;
  if(p>=N-1){const w=monthWords(ym);return `<div class="zpage zback">${w?`<p>${w}</p>`:''}<p class="zend">The end of ${mn}.</p></div>`;}
  const k=ks[p-1],w=entryLine(k),j=state.journal[k]&&state.journal[k].text?state.journal[k].text:'',f=(state.feel||{})[k];
  return `<div class="zpage"><p class="zdate">${esc(dateLabel(k))}</p>${(state.posts||{})[k]?`<div class="center">${pcFig(k,state.posts[k])}</div>`:''}${w?`<p class="world entry">${esc(w)}</p>`:''}${j?`<p class="mine">\\u201C${esc(j)}\\u201D</p>`:''}${!w&&FEEL_DAY[f]?`<p class="muted small">${FEEL_DAY[f]}</p>`:''}</div>`;}
function zineHTML(ym,p){
  const N=zineDays(ym).length+2;p=Math.max(0,Math.min(N-1,p));ui.zine={ym,p};
  return `<div class="csheet zine" data-k="zine"><h2 class="vh">Your ${ymName(ym)} book</h2><div class="zbox" aria-live="polite">${zinePageHTML(ym,p)}</div><p class="muted small center" style="margin:6px 0">Page ${p+1} of ${N}</p><div class="row znav"><button class="outline" id="zPrev" ${p?'':'disabled'}>Back a page</button><button class="primary" id="zNext" ${p<N-1?'':'disabled'}>Next page</button></div><div class="stack"><button class="ghost" id="zPic">Save as a picture</button><button class="ghost" data-close>Close the book</button></div></div>`;}
function zineGo(d,focusId){const z=ui.zine;if(!z)return;const sh=modal.querySelector('.sheet');if(!sh)return;sh.innerHTML=zineHTML(z.ym,z.p+d);nameDialog();sfx('select');
  const f=document.getElementById(focusId);if(f&&!f.disabled)f.focus({preventScroll:true});else{const o=document.getElementById(focusId==='zNext'?'zPrev':'zNext');if(o)o.focus({preventScroll:true});}}
function zinesHTML(){const M=zineMonths();
  return `<div class="csheet" data-k="zines"><h2>Monthly books</h2><p class="muted small">Every month with pages is stitched into a little book.</p><div class="group">${M.map(ym=>`<button class="rowl" data-zine="${ym}"><span class="rt"><b>${ymName(ym)} ${ym.slice(0,4)}</b><span class="rs">${zineDays(ym).length===1?'One page':`${zineDays(ym).length} pages`}</span></span><span class="chev" aria-hidden="true">\\u203A</span></button>`).join('')}</div><div class="stack"><button class="ghost" data-close>Close</button></div></div>`;}
async function zinePicture(ym){
  const ks=zineDays(ym);if(!ks.length)return;await shareFonts();
  const inM=k=>typeof k==='string'&&k.slice(0,7)===ym,cards=state.cards.filter(c=>inM(c.date)).sort((a,b)=>b.rarity-a.rarity||a.id-b.id).slice(0,8);
  const rest=state.history.filter(h=>h&&inM(h.date)&&h.status==='rest').length,pc=ks.filter(k=>(state.posts||{})[k]).length;
  const W=1080,H=1350,cv=document.createElement('canvas');cv.width=W;cv.height=H;const x=cv.getContext('2d');
  x.fillStyle='#F6EDD9';x.fillRect(0,0,W,H);x.fillStyle='rgba(90,70,50,.10)';for(let yy=150;yy<H-80;yy+=54)x.fillRect(80,yy,W-160,2);
  x.fillStyle='#7A2E2A';x.fillRect(60,0,18,H);
  const img=u=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=u;});
  const font=(w,s,f)=>`${w} ${s}px ${f||'Fredoka'}, ${JPF}`;x.textAlign='center';
  const ft=(t,yy,w,s,f)=>{let z=s;do{x.font=font(w,z,f);z-=2;}while(x.measureText(t).width>W-200&&z>14);x.fillText(t,W/2,yy);};
  x.fillStyle='#A4471F';x.font='26px "Press Start 2P", monospace';x.fillText(ym.slice(0,4),W/2,150);
  x.fillStyle='#2E2A47';ft(ymName(ym),260,600,96);
  x.fillStyle='#6B5E7A';ft(entryDays().size>=SCRIBE_AT?'Stitched together by the Scribe':'Stitched together by the fire',320,400,34,'"Nunito Sans"');
  const nums=[[ks.length,ks.length===1?'page':'pages'],[cards.length,cards.length===1?'Forgeling found':'Forgelings found'],[rest,rest===1?'rest day':'rest days'],[pc,pc===1?'postcard':'postcards']];
  nums.forEach(([n,l],i)=>{const cx=W/2+(i%2?1:-1)*230,cy=470+Math.floor(i/2)*170;x.fillStyle='#A4471F';x.font=font(600,84);x.fillText(String(n),cx,cy);x.fillStyle='#4A4060';let z=30;do{x.font=font(400,z,'"Nunito Sans"');z-=2;}while(x.measureText(l).width>400&&z>14);x.fillText(l,cx,cy+46);});
  x.imageSmoothingEnabled=false;
  for(let i=0;i<cards.length;i++){const im=await img(spriteURL(cards[i]));const cx=W/2+((i%4)-1.5)*200,cy=820+Math.floor(i/4)*190;x.fillStyle='rgba(46,42,71,.07)';x.fillRect(cx-80,cy,160,160);if(im)x.drawImage(im,cx-72,cy+8,144,144);}
  x.fillStyle='#A4471F';x.font='22px "Press Start 2P", monospace';x.fillText('FORGELINGS',W/2,H-40);
  const blob=await new Promise(r=>{try{cv.toBlob(r,'image/png');}catch(e){r(null);}});
  shareCv={c:{name:'Forgelings-'+ym},cv,blob};const can=canShareFiles(),url=cv.toDataURL('image/png');
  openOverlay(`<p class="rv-title">Your ${ymName(ym)}</p><img class="shareimg" src="${url}" alt="A picture of your ${ymName(ym)} in Forgelings: ${ks.length} pages and ${cards.length} Forgelings found">
    <p class="rv-hint">${can?'Send it to a friend, or save it to your photos.':'Save the picture, then send it however you like.'} No photos and none of your words are in it. It's made on this phone, and nothing is uploaded.</p>
    <div class="btnrow"><button class="primary" id="shDo">${can?'Share':'Save picture'}</button><button class="ghost" data-close>Close</button></div>`,true);
  ovMode='share';const d=$('#shDo');if(d)d.focus({preventScroll:true});}
function todayTask(){""")
# Today: last month is bound
rep("  {const o=otdKey();if(o&&state.otd!==todayKey())","""  {const pm=prevYM();if(+todayKey().slice(8,10)<=7&&state.zineSeen!==pm&&zineDays(pm).length>=3)rows.unshift(row('btnZine',IC.pack,`Your ${ymName(pm)} is bound`,entryDays().size>=SCRIBE_AT?`The Scribe stitched your ${ymName(pm)} pages into a little book. Flip through it.`:`Your ${ymName(pm)} pages are stitched into a little book. Flip through it.`,'',true));}
  {const o=otdKey();if(o&&state.otd!==todayKey())""")
rep("  else if(b.id==='btnClose'){","  else if(b.id==='btnZine'){const pm=prevYM();state.zineSeen=pm;save();renderToday();openSheet(zineHTML(pm,0));}\n  else if(b.id==='btnClose'){")
# the Book keeps them
rep("""${(state.letters||[]).length?`<button class="outline" id="bookLetters" style="margin-top:6px">Letters (${state.letters.length})</button>`:''}""",
    """${(state.letters||[]).length?`<button class="outline" id="bookLetters" style="margin-top:6px">Letters (${state.letters.length})</button>`:''}${L?'<button class="outline" id="bookZines" style="margin-top:6px">Monthly books</button>':''}""")
rep("  if(e.target.closest('#bookLetters')){openSheet(lettersHTML());return;}","""  if(e.target.closest('#bookLetters')){openSheet(lettersHTML());return;}
  if(e.target.closest('#bookZines')){openSheet(zinesHTML());return;}
  {const zb=e.target.closest('[data-zine]');if(zb){openSheet(zineHTML(zb.dataset.zine,0));return;}}
  if(e.target.closest('#zPrev')){zineGo(-1,'zPrev');return;}
  if(e.target.closest('#zNext')){zineGo(1,'zNext');return;}
  if(e.target.closest('#zPic')){if(ui.zine)zinePicture(ui.zine.ym);return;}""")
rep("  s.closed=typeof s.closed==='string'","  s.zineSeen=typeof s.zineSeen==='string'&&/^\\d{4}-\\d{2}$/.test(s.zineSeen)?s.zineSeen:'';\n  s.closed=typeof s.closed==='string'")
css="""
/* 0.71: the monthly book */
.zine .vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.zbox{min-height:340px;display:flex}
.zpage{flex:1;background:#FFF8EA;color:#3A2E25;border-radius:4px 10px 10px 4px;padding:18px 18px 14px 26px;box-shadow:inset 8px 0 0 #7A2E2A,0 2px 8px rgba(0,0,0,.25);background-image:repeating-linear-gradient(transparent 0 27px,rgba(90,70,50,.12) 27px 28px)}
.zpage .world,.zpage .mine{color:#3A2E25}.zpage .muted{color:#6B5E7A}
.zcover{display:flex;flex-direction:column;justify-content:center;text-align:center;background:#7A2E2A;color:#FFF3D6;background-image:none;box-shadow:inset 8px 0 0 #4E1C1A,0 2px 8px rgba(0,0,0,.3)}
.zcover h3{font:600 40px var(--title,inherit);margin:6px 0;color:#FFD36B}.zcover .zk{font:12px "Press Start 2P",monospace;margin:0;color:#FFD36B}.zcover .muted{color:#F2D9C0}
.zdate{font-weight:700;margin:0 0 8px}.zend{text-align:center;font-style:italic;margin-top:18px}
.znav{justify-content:space-between;gap:10px}.znav button{flex:1;min-height:44px}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk71.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk71.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
