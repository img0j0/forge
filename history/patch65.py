# 0.65: photo postcards (the design doc's Part 4; Hunter, November 12: "Execute the plan"; he will try it before deciding).
#   On a done day, Today's page offers "Add a photo postcard": one photo of your small thing becomes a 64 x 48 pixel
#   postcard, dithered into eight shades of that day's realm, with a date stamp. The photo itself is never kept or sent:
#   it is read on the phone, turned into 1,152 bytes of palette indices, and let go. The postcard sits in Today's page,
#   in the journal beside the entry, on the ribbon's old page and in Your year (not in Your year's shared picture:
#   photos stay private). Every fifth postcard you make, a Forgeling comes home with a postcard of its own from that
#   realm (drawn by the app, not a photo) for the postcard wall by the fire.
#   Storage: state.posts = {date: {r, p}} (p = base64 of 3-bit indices, 1,536 characters), at most 500 kept;
#   state.pcGifts = [{d, r, s, c}] (date, realm, scene seed, the Forgeling's id); state.pcMade, state.pcLast count the
#   days that got a postcard (a removed and re-added one does not count twice). The iCloud copy drops the oldest
#   postcards if the save would not fit iCloud's key-value limit; the device keeps them all.
import re,subprocess,os
S=open('base64.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.64.0'","const VERSION='prototype 0.65.0'")
rep("<title>Forgelings (prototype 0.64.0)</title>","<title>Forgelings (prototype 0.65.0)</title>")

# ---- constants before sanitize (it runs at load) ----
rep("function sanitize(s){","""/* 0.65: photo postcards */
const PC_W=64,PC_H=48,PC_MAX=500,PC_B64=4*Math.ceil(PC_W*PC_H*3/8/3);
const PC_RAMP=[['#14201A','#24402E','#3E6B3F','#5E9450','#8FBF6A','#C4DE8A','#EDF2C0','#FFFBEA'],
  ['#1A0B10','#4D1A1A','#8A2E22','#C2502E','#E8823F','#F5B060','#FFD99A','#FFF5E0'],
  ['#04101E','#0B3350','#1A5C82','#2F86AE','#5FB5E0','#8FD6E8','#C8EEF7','#F4FDFF'],
  ['#0E1426','#26355A','#4A5F8C','#7189B8','#9FB4DE','#C9DDF7','#E6F0FC','#FFFFFF'],
  ['#0C071A','#2A1450','#4B3F9A','#7E6BD6','#B07CC8','#E07CB0','#F2B8D0','#FFF0F6']];
function sanitize(s){""")
rep("""  if(s.ask!==undefined){if(!s.ask""","""  {const DK=/^\\d{4}-\\d{2}-\\d{2}$/,P=s.posts&&typeof s.posts==='object'&&!Array.isArray(s.posts)?s.posts:{},o={};
   Object.keys(P).filter(k=>DK.test(k)).sort().slice(-PC_MAX).forEach(k=>{const v=P[k];if(v&&Number.isInteger(v.r)&&v.r>=0&&v.r<=4&&typeof v.p==='string'&&v.p.length===PC_B64&&/^[A-Za-z0-9+/=]+$/.test(v.p))o[k]={r:v.r,p:v.p};});s.posts=o;
   s.pcMade=Number.isInteger(s.pcMade)&&s.pcMade>=0?s.pcMade:0;s.pcLast=typeof s.pcLast==='string'&&DK.test(s.pcLast)?s.pcLast:'';
   s.pcGifts=(Array.isArray(s.pcGifts)?s.pcGifts:[]).filter(g=>g&&typeof g.d==='string'&&DK.test(g.d)&&Number.isInteger(g.r)&&g.r>=0&&g.r<=4&&Number.isInteger(g.s)).slice(-200).map(g=>({d:g.d,r:g.r,s:g.s,c:Number.isFinite(g.c)?g.c:-1}));}
  if(s.ask!==undefined){if(!s.ask""")

# ---- the postcard code ----
rep("function todayTask(){","""/* 0.65: photo postcards. 3-bit indices into the realm's ramp, packed little-endian. */
const BAYER4=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5];
function pcPack(idx){const b=new Uint8Array(Math.ceil(idx.length*3/8));for(let i=0;i<idx.length;i++){const bit=i*3,by=bit>>3,o=bit&7,v=idx[i]&7;b[by]|=(v<<o)&255;if(o>5)b[by+1]|=v>>(8-o);}let s='';for(let i=0;i<b.length;i++)s+=String.fromCharCode(b[i]);return btoa(s);}
function pcUnpack(p){const s=atob(p),n=PC_W*PC_H,out=new Uint8Array(n);for(let i=0;i<n;i++){const bit=i*3,by=bit>>3,o=bit&7;let v=s.charCodeAt(by)>>o;if(o>5)v|=(s.charCodeAt(by+1)||0)<<(8-o);out[i]=v&7;}return out;}
const pcCache=new Map();
function pcDraw(idx,r){const cv=document.createElement('canvas');cv.width=PC_W;cv.height=PC_H;const x=cv.getContext('2d'),im=x.createImageData(PC_W,PC_H),rgb=(PC_RAMP[r]||PC_RAMP[0]).map(h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)));
  for(let i=0;i<idx.length;i++){const c=rgb[idx[i]&7];im.data[i*4]=c[0];im.data[i*4+1]=c[1];im.data[i*4+2]=c[2];im.data[i*4+3]=255;}x.putImageData(im,0,0);return cv.toDataURL('image/png');}
function pcURL(p,r){const key=r+':'+p;if(pcCache.has(key))return pcCache.get(key);let u='';try{u=pcDraw(pcUnpack(p),r);}catch(e){}pcCache.set(key,u);return u;}
function giftURL(g){const key='g:'+g.r+':'+g.s;if(pcCache.has(key))return pcCache.get(key);let u='';try{u=pcDraw(pcScene(g.r,g.s),g.r);}catch(e){}pcCache.set(key,u);return u;}
/* a photo to indices: centre-cropped to 4:3, scaled down in two steps, levels stretched, ordered dither to 8 shades */
function pcFromImage(img){
  const iw=img.naturalWidth||img.width,ih=img.naturalHeight||img.height;if(!iw||!ih)return null;
  const s=Math.max(PC_W/iw,PC_H/ih),sw=PC_W/s,sh=PC_H/s;
  const m=document.createElement('canvas');m.width=256;m.height=192;const mx=m.getContext('2d');mx.imageSmoothingEnabled=true;mx.imageSmoothingQuality='high';mx.drawImage(img,(iw-sw)/2,(ih-sh)/2,sw,sh,0,0,256,192);
  const cv=document.createElement('canvas');cv.width=PC_W;cv.height=PC_H;const x=cv.getContext('2d');x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high';x.drawImage(m,0,0,PC_W,PC_H);
  const d=x.getImageData(0,0,PC_W,PC_H).data,n=PC_W*PC_H,L=new Float32Array(n);
  for(let i=0;i<n;i++)L[i]=.2126*d[i*4]+.7152*d[i*4+1]+.0722*d[i*4+2];
  const so=Array.from(L).sort((a,b)=>a-b),lo=so[Math.floor(n*.02)],hi=Math.max(lo+24,so[Math.floor(n*.98)]);
  const idx=new Uint8Array(n);
  for(let y=0;y<PC_H;y++)for(let xx=0;xx<PC_W;xx++){const i=y*PC_W+xx,t=Math.min(1,Math.max(0,(L[i]-lo)/(hi-lo)));idx[i]=Math.max(0,Math.min(7,Math.round(t*7+(BAYER4[(y&3)*4+(xx&3)]/16-.47)*.9)));}
  return idx;}
/* a Forgeling's own postcard: a little scene of the realm, drawn from a seed */
function pcScene(r,seed){
  const R=mulberry32(seed|0),W=PC_W,H=PC_H,idx=new Uint8Array(W*H),B=(x,y)=>BAYER4[(y&3)*4+(x&3)]/16-.47;
  const put=(x,y,v)=>{x|=0;y|=0;if(x>=0&&x<W&&y>=0&&y<H)idx[y*W+x]=v;};
  const grad=(y0,y1,a,b)=>{for(let y=y0;y<y1;y++)for(let x=0;x<W;x++){const t=(y-y0)/Math.max(1,y1-y0-1);put(x,y,Math.max(0,Math.min(7,Math.round(a+(b-a)*t+B(x,y)*.9))));}};
  const disc=(cx,cy,rad,v)=>{for(let y=-rad;y<=rad;y++)for(let x=-rad;x<=rad;x++)if(x*x+y*y<=rad*rad+rad*.6)put(cx+x,cy+y,v);};
  const ridge=(base,amp,f,ph,v,top)=>{const hs=[];for(let x=0;x<W;x++){const h=base-amp*(Math.sin(x*f+ph)+.5*Math.sin(x*f*2.3+ph*1.7));hs.push(h);for(let y=Math.round(h);y<H;y++)put(x,y,v);if(top!=null)put(x,Math.round(h),top);}return hs;};
  const hz=26+Math.floor(R()*6);
  if(r===0){grad(0,hz+6,5,6.4);disc(10+R()*44,8+R()*6,5,7);ridge(hz,3,.09+R()*.04,R()*6,3);const h=ridge(hz+8,3,.13+R()*.05,R()*6,2,3);
    for(let i=0;i<26;i++){const x=Math.floor(R()*W),y=Math.round(h[x])+2+Math.floor(R()*(H-h[x]-2));put(x,y,R()<.5?7:6);}}
  else if(r===1){grad(0,H,2,6);const px=14+R()*36;for(let y=10;y<H;y++){const w=(y-10)*.75+2;for(let x=-w;x<=w;x++)put(px+x,y,1);}
    for(let y=10;y<H;y++)if(R()<.8)put(px+Math.sin(y*.5)*2,y,6);for(let i=0;i<5;i++)put(px-1+i%3,9-Math.floor(i/2),5);
    for(let i=0;i<18;i++)put(R()*W,R()*24,R()<.5?7:6);ridge(H-6,1.5,.2,R()*6,0);}
  else if(r===2){grad(0,hz,7,5);const sx=8+R()*48;disc(sx,hz-4,4,7);
    for(let y=hz;y<H;y++)for(let x=0;x<W;x++)put(x,y,(y-hz)%3===0?3:2);
    for(let i=0;i<40;i++){const y=hz+1+Math.floor(R()*(H-hz-1)),x=Math.floor(R()*W);put(x,y,5);put(x+1,y,5);}
    for(let y=hz+1;y<H;y+=2)put(sx+(R()*4-2),y,7);}
  else if(r===3){grad(0,hz+4,4,6);let h=hz-4;const hs=[];for(let x=0;x<W;x++){h+=R()*4-2-(h-(hz-6))*.08;h=Math.max(8,Math.min(hz+2,h));hs.push(h);for(let y=Math.round(h);y<H;y++)put(x,y,y-h<3?7:2);}
    for(let y=hz+6;y<H;y++)for(let x=0;x<W;x++)put(x,y,Math.max(5,Math.min(7,Math.round(6+B(x,y)))));
    for(let i=0;i<22;i++)put(R()*W,R()*H,7);}
  else{grad(0,H,0,3);for(let i=0;i<34;i++)put(R()*W,R()*30,R()<.3?7:5);const mx=10+R()*44,my=8+R()*6;disc(mx,my,5,7);disc(mx+2,my-1,4,1);
    ridge(hz+4,2.5,.11+R()*.05,R()*6,1);const wx=Math.floor(8+R()*48),wy=hz+8;put(wx,wy,6);put(wx+1,wy,6);}
  return idx;}
const pcDate=k=>new Date(k+'T00:00:00').toLocaleDateString(LOC(),{month:'short',day:'numeric'});
const pcRealm=r=>THEMES[r]?THEMES[r].name:THEMES[0].name;
const giftFrom=g=>{const c=g.c>=0?cardById(g.c):null;return c?(c.nick||c.name):'A Forgeling';};
function pcFig(k,p,cls){return `<figure class="pcard${cls?' '+cls:''}" style="--pr:${PC_RAMP[p.r][3]}"><img src="${pcURL(p.p,p.r)}" alt="Your photo postcard, ${esc(dateLabel(k))}" width="${PC_W*3}" height="${PC_H*3}"><span class="pstamp" aria-hidden="true">${esc(pcDate(k))}</span></figure>`;}
function giftFig(g){const n=giftFrom(g),rn=pcRealm(g.r);return `<figure class="pcard gift" style="--pr:${PC_RAMP[g.r][3]}"><img src="${giftURL(g)}" alt="A postcard from ${rn}, brought home by ${esc(n)}" width="${PC_W*3}" height="${PC_H*3}"><span class="pstamp" aria-hidden="true">${esc(pcDate(g.d))}</span><figcaption>From ${esc(n)}, ${rn}</figcaption></figure>`;}
function pcHTML(){
  const k=state.date,p=(state.posts||{})[k];
  if(p)return `<div class="pctoday">${pcFig(k,p)}<div class="row" style="justify-content:center;flex-wrap:wrap;margin:6px 0 0"><button class="ghost" id="pcAdd">Change the photo</button><button class="ghost" id="pcDel">Remove the postcard</button></div></div>`;
  return `<div class="pctoday"><button class="ghost marginlink" id="pcAdd">Add a photo postcard</button><p class="muted small center" style="margin:2px 0 0">One photo of your small thing becomes a little pixel postcard. Only that tiny picture is kept, on this device.</p></div>`;}
let pcIn=null;
function pcPick(){
  if(!pcIn){pcIn=document.createElement('input');pcIn.type='file';pcIn.accept='image/*';pcIn.hidden=true;pcIn.tabIndex=-1;pcIn.setAttribute('aria-hidden','true');document.body.appendChild(pcIn);
    pcIn.addEventListener('change',()=>{const f=pcIn.files&&pcIn.files[0];if(!f)return;const u=URL.createObjectURL(f),im=new Image();
      const bad=()=>{URL.revokeObjectURL(u);pcIn.value='';sfx('no');toast('That photo could not be opened. Try another one.');};
      im.onload=()=>{let idx=null;try{idx=pcFromImage(im);}catch(e){}URL.revokeObjectURL(u);pcIn.value='';if(!idx){bad();return;}pcSave(idx);};im.onerror=bad;im.src=u;});}
  pcIn.click();}
function pcSave(idx){
  if(state.status!=='done')return;
  const k=state.date,c=state.todayCard!=null?cardById(state.todayCard):null,r=c&&c.theme>=0&&c.theme<5?c.theme:(state.lean&&state.lean.date===k?state.lean.r:0);
  state.posts=state.posts||{};state.posts[k]={r,p:pcPack(idx)};
  const ks=Object.keys(state.posts).sort();if(ks.length>PC_MAX)ks.slice(0,ks.length-PC_MAX).forEach(x=>delete state.posts[x]);
  let msg='Your postcard is on today’s page.';
  if(state.pcLast!==k){state.pcLast=k;state.pcMade=(state.pcMade||0)+1;
    if(state.pcMade%5===0){const m=companion()||mateNow()||c;state.pcGifts=(state.pcGifts||[]).concat([{d:k,r,s:Math.floor(Math.random()*2147483646)+1,c:m?m.id:-1}]).slice(-200);
      const g=state.pcGifts[state.pcGifts.length-1];msg=`${giftFrom(g)} has come home with a postcard from ${pcRealm(r)}. It is on the wall by the fire.`;hf.msg=msg;}}
  sfx('save');save();renderToday();renderChronicle();renderHearth();toast(msg);
  const b=$('#pcAdd');if(b)b.focus({preventScroll:true});}
function pcWallHTML(){
  const G=(state.pcGifts||[]).slice().reverse(),P=Object.keys(state.posts||{}).sort().reverse().slice(0,30);
  return `<h2>The postcard wall</h2><p class="muted small">Your photo postcards, and the ones your Forgelings bring home. Every fifth postcard you make, one of them comes back with a postcard of its own. They stay on this device.</p>
    ${G.length?`<h3 class="sub3">From your Forgelings</h3><div class="pcwall">${G.map(giftFig).join('')}</div>`:`<p class="muted small">${5-(state.pcMade||0)%5===1?'One more postcard, and a Forgeling will bring one home.':`${5-(state.pcMade||0)%5} more postcards, and a Forgeling will bring one home.`}</p>`}
    ${P.length?`<h3 class="sub3">Yours</h3><div class="pcwall">${P.map(k=>pcFig(k,state.posts[k])).join('')}</div>`:''}
    <div class="stack"><button class="ghost" data-close>Close</button></div>`;}
/* the iCloud copy drops the oldest postcards when the save would not fit iCloud's key-value limit */
async function cloudFit(t){let z=await czip(t);if(z.length<=880000)return z;
  try{const o=JSON.parse(t),ks=Object.keys(o.posts||{}).sort();while(z.length>880000&&ks.length){ks.splice(0,Math.max(1,Math.ceil(ks.length/4))).forEach(k=>delete o.posts[k]);z=await czip(JSON.stringify(o));}}catch(e){}
  return z;}
function todayTask(){""")
rep("await p.set({key:KEY,value:await czip(t)});","await p.set({key:KEY,value:await cloudFit(t)});")

# ---- Today's page ----
rep("if(s==='done')hero+=askHTML();","if(s==='done')hero+=askHTML()+pcHTML();")
rep("  if(b.id==='btnOwn'){toggleOwn();return;}","""  if(b.id==='btnOwn'){toggleOwn();return;}
  if(b.id==='pcAdd'){pcPick();return;}
  if(b.id==='pcDel'){if(state.posts)delete state.posts[state.date];save();renderToday();renderChronicle();renderHearth();toast('The postcard is gone. The photo was never kept.');const a=$('#pcAdd');if(a)a.focus({preventScroll:true});return;}""")
# ---- the journal ----
rep("""return `<div class="calling" style="--rc:${V.color}"><div class="row" style="margin:0"><b>${V.name}</b><span class="muted small">${esc(dateLabel(k))}</span></div>${w?""","""const pc=(state.posts||{})[k];
    return `<div class="calling" style="--rc:${V.color}"><div class="row" style="margin:0"><b>${V.name}</b><span class="muted small">${esc(dateLabel(k))}</span></div>${pc?pcFig(k,pc,'inj'):''}${w?""")
# the ribbon's old page
rep("""<h2 class="center">${esc(dateLabel(k))}</h2><p class="mine" style="margin:12px 0">""","""<h2 class="center">${esc(dateLabel(k))}</h2>${(state.posts||{})[k]?`<div class="center">${pcFig(k,state.posts[k])}</div>`:''}<p class="mine" style="margin:12px 0">""")
# ---- Your year (not the shared picture) ----
rep("""    ${t.quote?`<p class="mine">\\u201C${esc(t.quote)}\\u201D</p>""","""    ${(pk=>pk.length?`<h3 class="sub3">Your postcards</h3><div class="ypc">${pk.map(k=>`<img src="${pcURL(state.posts[k].p,state.posts[k].r)}" alt="Your photo postcard, ${esc(dateLabel(k))}" width="${PC_W*2}" height="${PC_H*2}">`).join('')}</div><p class="muted small">Your photos stay on this device. They are not in the picture.</p>`:'')(Object.keys(state.posts||{}).filter(k=>k.slice(0,4)===String(t.y)).sort().slice(-30))}
    ${t.quote?`<p class="mine">\\u201C${esc(t.quote)}\\u201D</p>""")
# ---- the wall by the fire ----
rep("""<button class="chip" id="hKeeps">Keepsakes</button>""","""<button class="chip" id="hKeeps">Keepsakes</button>${Object.keys(state.posts||{}).length||(state.pcGifts||[]).length?`<button class="chip" id="hPost">Postcard wall · ${Object.keys(state.posts||{}).length+(state.pcGifts||[]).length}</button>`:''}""")
rep("  if(b.id==='hKeeps'){openHSheet('keeps');return;}","  if(b.id==='hKeeps'){openHSheet('keeps');return;}\n  if(b.id==='hPost'){openSheet(pcWallHTML());return;}")

css="""
/* 0.65: photo postcards */
.pcard{position:relative;display:inline-block;margin:0;padding:6px 6px 16px;background:#FFF8EA;border-radius:3px;box-shadow:0 2px 6px rgba(0,0,0,.28);transform:rotate(-1.2deg);color:#3A2E25;max-width:100%}
.pcard:nth-child(2n){transform:rotate(1deg)}
.pcard img{display:block;width:192px;max-width:100%;height:auto;image-rendering:pixelated;image-rendering:crisp-edges;border-radius:1px}
.pcard .pstamp{position:absolute;right:6px;bottom:2px;font:700 10px/1.2 var(--body);letter-spacing:.04em;color:var(--pr);padding:0 4px;border:1.5px solid var(--pr);border-radius:8px;background:#FFF8EA}
.pcard figcaption{font-size:12px;line-height:1.3;margin:4px 0 0;padding-right:56px;color:#3A2E25}
.pcard.gift{padding-bottom:6px}.pcard.gift .pstamp{top:2px;bottom:auto;right:2px}
.pctoday{text-align:center;margin:8px 0 2px}.pctoday .pcard{margin:4px auto 0}
.pcard.inj{float:right;margin:4px 0 4px 10px;padding:4px 4px 12px}.pcard.inj img{width:96px}.pcard.inj .pstamp{font-size:8px;right:3px;bottom:1px}
.calling::after{content:"";display:block;clear:both}
.pcwall{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px;margin:8px 0 14px}.pcwall .pcard img{width:100%}
.ypc{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:6px 0}.ypc img{width:100%;height:auto;image-rendering:pixelated;border-radius:3px;border:2px solid #FFF8EA}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk65.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk65.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
