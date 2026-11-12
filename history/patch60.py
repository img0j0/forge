# 0.60: Your year in Forgelings (Hunter, November 12: "Please prioritize and execute the additions"; third of five).
#   A keepsake of the year: the days you showed up and rested, the Forgelings you found (the rarest one large, nine more
#   in a grid), the calling you came back to most, the realms you reached, the season stamps you pressed, the lines you
#   wrote and one of them quoted. It opens from the Journal's "Your year" button, and from Today from December 20 to
#   January 10 ("Your year in Forgelings is ready"). In the first ten days of January it shows the year just ended.
#   "Save as a picture" makes a 1080 x 1920 picture (story size) to keep or send. It is made on the phone; nothing is
#   uploaded. No streaks or missed days are counted: rest days are shown as rest, gaps are not shown at all.
import re,subprocess,os
S=open('base59.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.59.0'","const VERSION='prototype 0.60.0'")
rep("<title>Forgelings (prototype 0.59.0)</title>","<title>Forgelings (prototype 0.60.0)</title>")

rep("/* ================= Cards ================= */","""/* ================= 0.60: your year in Forgelings ================= */
/* the year shown: the year just ended in the first ten days of January, else this year so far */
function yearShown(){const k=todayKey(),y=+k.slice(0,4),md=k.slice(5);return md<='01-10'?y-1:y;}
const yearReady=()=>{const md=todayKey().slice(5);return (md>='12-20'||md<='01-10')&&yearStats(yearShown()).found>0;};
function yearStats(y){
  const inY=k=>typeof k==='string'&&k.slice(0,4)===String(y);
  const H=state.history.filter(h=>h&&inY(h.date)),done=H.filter(h=>h.status==='done'),rest=H.filter(h=>h.status==='rest').length;
  const cards=state.cards.filter(c=>inY(c.date));
  const vc={};done.forEach(h=>{if(VECTORS[h.v])vc[h.v]=(vc[h.v]||0)+1;});const topV=Object.keys(vc).sort((a,b)=>vc[b]-vc[a]||a-b)[0];
  const best=cards.slice().sort((a,b)=>b.rarity-a.rarity||(b.bond||0)-(a.bond||0)||a.id-b.id)[0]||null;
  const grid=cards.filter(c=>!best||c.id!==best.id).sort((a,b)=>b.rarity-a.rarity||(b.bond||0)-(a.bond||0)||a.id-b.id).slice(0,9);
  const realms=new Set(cards.map(c=>c.theme+(c.dark?5:0))).size;
  const lines=Object.keys(state.journal||{}).filter(k=>inY(k)&&state.journal[k]&&typeof state.journal[k].text==='string'&&state.journal[k].text.trim());
  const pick=lines.length?lines.slice().sort((a,b)=>{const la=state.journal[a].text.length,lb=state.journal[b].text.length;return (lb>140?0:lb)-(la>140?0:la)||(a<b?-1:1);})[0]:null;
  const stamps=SEASONS.filter(s=>state.seasons&&state.seasons[s.id+'-'+y]);
  const first=H.length?H.map(h=>h.date).sort()[0]:null;
  return {y,days:done.length,rest,found:cards.length,topV:topV!=null?VECTORS[+topV]:null,topN:topV!=null?vc[topV]:0,best,grid,realms,lines:lines.length,quote:pick?state.journal[pick].text.trim():'',quoteDate:pick,stamps,first};}
function yearHTML(){
  const t=yearStats(yearShown());
  if(!t.found)return `<div class="csheet" data-k="year"><h2>Your year in Forgelings</h2><p class="muted">Your year starts with your first Forgeling. Turn over a card, and it will begin to fill.</p><div class="stack"><button class="ghost" data-close>Close</button></div></div>`;
  const cell=c=>`<button class="ycell" data-insp="${c.id}" aria-label="${esc(lookLabel(c))}"><img src="${spriteURL(c)}" alt=""><small>${esc(c.nick||c.name)}</small></button>`;
  const nums=[[t.days,t.days===1?'day you showed up':'days you showed up'],[t.found,t.found===1?'Forgeling found':'Forgelings found'],[t.rest,t.rest===1?'rest day':'rest days'],[t.lines,t.lines===1?'line written':'lines written']];
  return `<div class="csheet yearbook" data-k="year"><p class="ykick">${t.y}</p><h2>Your year in Forgelings</h2>
    <div class="ynums">${nums.map(([n,l])=>`<div><b>${n}</b><span>${l}</span></div>`).join('')}</div>
    ${t.best?`<div class="ybest"><img src="${spriteURL(t.best)}" alt=""><div><p class="muted small" style="margin:0">Your rarest find</p><b>${esc(t.best.nick||t.best.name)}</b><span class="muted small">${RAR[t.best.rarity].name} · ${esc(realmName(t.best))} · ${esc(dateLabel(t.best.date))}</span></div></div>`:''}
    ${t.grid.length?`<div class="ygrid">${t.grid.map(cell).join('')}</div>`:''}
    ${t.topV?`<p class="small">The calling you came back to most: <b>${t.topV.name}</b>, ${t.topN} ${t.topN===1?'time':'times'}.</p>`:''}
    <p class="small">You reached ${t.realms} of 10 realms.</p>
    ${t.stamps.length?`<div class="ystamps" role="img" aria-label="${t.stamps.map(s=>s.name).join(', ')}">${t.stamps.map(s=>seasonStampSVG(s,32,true)).join('')}</div>`:''}
    ${t.quote?`<p class="mine">\\u201C${esc(t.quote)}\\u201D</p><p class="muted small" style="margin-top:-4px">You wrote this on ${esc(dateLabel(t.quoteDate))}.</p>`:''}
    <div class="stack"><button class="primary" id="yearPic">Save as a picture</button><button class="ghost" data-close>Close</button></div></div>`;}
const JPF='"Hiragino Maru Gothic ProN","Hiragino Sans","Noto Sans JP","Noto Sans CJK JP",sans-serif';
async function yearPicture(){
  const t=yearStats(yearShown());if(!t.found)return;await shareFonts();
  const W=1080,H=1920,cv=document.createElement('canvas');cv.width=W;cv.height=H;const x=cv.getContext('2d');
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#24183F');g.addColorStop(1,'#3A2240');x.fillStyle=g;x.fillRect(0,0,W,H);
  x.fillStyle='rgba(255,255,255,.04)';for(let yy=120;yy<H;yy+=56)x.fillRect(60,yy,W-120,2);
  const img=u=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=u;});
  const font=(w,s,f)=>`${w} ${s}px ${f||'Fredoka'}, ${JPF}`;x.textAlign='center';
  const ft=(t,yy,w,s,f,max)=>{let z=s;do{x.font=font(w,z,f);z-=2;}while(x.measureText(t).width>(max||W-120)&&z>14);x.fillText(t,W/2,yy);};
  x.fillStyle='#FFD36B';x.font='26px "Press Start 2P", monospace';x.fillText(String(t.y),W/2,150);
  x.fillStyle='#FFF7EC';ft('Your year in Forgelings',250,600,78);
  const nums=[[t.days,t.days===1?'day you showed up':'days you showed up'],[t.found,t.found===1?'Forgeling found':'Forgelings found'],[t.rest,t.rest===1?'rest day':'rest days'],[t.lines,t.lines===1?'line written':'lines written']];
  nums.forEach(([n,l],i)=>{const cx=W/2+(i%2?1:-1)*250,cy=370+Math.floor(i/2)*170;x.fillStyle='#FFD36B';x.font=font(600,84);x.fillText(String(n),cx,cy);x.fillStyle='#CDBFDB';let z=30;do{x.font=font(400,z,'"Nunito Sans"');z-=2;}while(x.measureText(l).width>440&&z>14);x.fillText(l,cx,cy+48);});
  x.imageSmoothingEnabled=false;
  if(t.best){const im=await img(spriteURL(t.best));const R=RAR[t.best.rarity];x.fillStyle=R.edge;x.fillRect(W/2-190,700,380,380);x.fillStyle='#1B1430';x.fillRect(W/2-180,710,360,360);if(im)x.drawImage(im,W/2-176,714,352,352);
    x.fillStyle='#CDBFDB';x.font=font(400,30,'"Nunito Sans"');x.fillText('Your rarest find',W/2,670);
    x.fillStyle='#FFF7EC';ft(t.best.nick||t.best.name,1150,600,58);
    x.fillStyle=R.glow||'#FFD36B';x.font=font(700,30,'"Nunito Sans"');x.fillText(`${R.name} · ${realmName(t.best)}`,W/2,1196);}
  const G=t.grid.slice(0,9);for(let i=0;i<G.length;i++){const im=await img(spriteURL(G[i]));const cx=W/2+((i%3)-1)*180,cy=1240+Math.floor(i/3)*140;x.fillStyle='rgba(255,255,255,.07)';x.fillRect(cx-64,cy,128,128);if(im)x.drawImage(im,cx-60,cy+4,120,120);}
  let y=1240+Math.ceil(G.length/3)*140+50;x.font=font(400,32,'"Nunito Sans"');x.fillStyle='#EDE6FF';
  if(t.topV){ft(`The calling you came back to most: ${t.topV.name}`,y,400,32,'"Nunito Sans"');y+=50;}
  ft(`You reached ${t.realms} of 10 realms.`,y,400,32,'"Nunito Sans"');y+=40;
  if(t.stamps.length){const sz=56,sx=W/2-(t.stamps.length*(sz+16)-16)/2;for(let i=0;i<t.stamps.length;i++){const im=await img('data:image/svg+xml,'+encodeURIComponent(seasonStampSVG(t.stamps[i],sz,true).replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ')));if(im)x.drawImage(im,sx+i*(sz+16),y,sz,sz);}y+=sz+30;}
  x.fillStyle='#FFD36B';x.font='22px "Press Start 2P", monospace';x.fillText('FORGELINGS',W/2,H-34);
  const blob=await new Promise(r=>{try{cv.toBlob(r,'image/png');}catch(e){r(null);}});
  shareCv={c:{name:'Forgelings-'+t.y},cv,blob};const can=canShareFiles(),url=cv.toDataURL('image/png');
  openOverlay(`<p class="rv-title">Your year in Forgelings</p><img class="shareimg" src="${url}" alt="A picture of your ${t.y} in Forgelings: ${t.days} days showed up and ${t.found} Forgelings found">
    <p class="rv-hint">${can?'Send it to a friend, or save it to your photos.':'Save the picture, then send it however you like.'} It's made on this phone, and nothing is uploaded.</p>
    <div class="btnrow"><button class="primary" id="shDo">${can?'Share':'Save picture'}</button><button class="ghost" data-close>Close</button></div>`,true);
  ovMode='share';const d=$('#shDo');if(d)d.focus({preventScroll:true});}
/* ================= Cards ================= */""")

# where it opens: the Journal, and Today near the turn of the year
rep('''<button class="chip" id="jSeasons">Seasons</button>''','''<button class="chip" id="jSeasons">Seasons</button><button class="chip" id="jYear">Your year</button>''')
rep('''  if(e.target.closest('#jSeasons')){''','''  if(e.target.closest('#jYear')){openCSheet(yearHTML());return;}
  if(e.target.closest('#jSeasons')){''')
rep("""  {const n=seasonNow();if(n&&state.cards.length){""","""  if(yearReady())rows.unshift(row('btnYear',IC.pack,'Your year in Forgelings is ready',`A keepsake of ${yearShown()}: the days you showed up, the Forgelings you found and the lines you wrote.`,'',true));
  {const n=seasonNow();if(n&&state.cards.length){""")
rep("""  else if(b.id==='btnSeason'){openSheet(seasonsHTML());}""","""  else if(b.id==='btnSeason'){openSheet(seasonsHTML());}
  else if(b.id==='btnYear'){openSheet(yearHTML());}""")
# the picture button inside the sheet (sheets live in #modal)
rep("""  else if(b.dataset.statue)openStatue(+b.dataset.statue);""","""  else if(b.id==='yearPic')yearPicture();
  else if(b.dataset.statue)openStatue(+b.dataset.statue);""")

css="""
/* 0.60: your year */
.yearbook .ykick{font:22px 'Press Start 2P',monospace;color:#C9772E;margin:0}
.ynums{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}
.ynums div{display:flex;flex-direction:column;align-items:center;padding:8px;border:1px dashed var(--line);border-radius:8px}
.ynums b{font:600 30px var(--display)}.ynums span{font-size:13px;text-align:center}
.ybest{display:flex;gap:12px;align-items:center;margin:10px 0}.ybest img{width:84px;height:84px;image-rendering:pixelated}
.ybest div{display:flex;flex-direction:column}
.ygrid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:8px 0}
.ycell{display:flex;flex-direction:column;align-items:center;gap:2px;min-height:44px;padding:4px;background:none;border:0;color:inherit;cursor:pointer}
.ycell img{width:56px;height:56px;image-rendering:pixelated}.ycell small{font-size:12px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ystamps{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk60.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk60.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
