# Forge 0.21.0: first impressions. A title scene before the age question, a home-screen icon,
# a calmer first minute, and a gentle arrival on every open. Reads base20.html, writes work.html.
import base64, struct, zlib
src = open('base20.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ================= 1. Title scene =================
rep('/* Nav */', '''.scrim.titlemode{background:#0B0E26;padding:0;align-items:stretch}
.titlemode .ov{max-width:none;width:100%;height:100dvh;padding:0;display:block;position:relative;overflow:hidden}
#titleCv{position:absolute;inset:0;width:100%;height:100%;transition:transform .5s ease;image-rendering:pixelated;image-rendering:crisp-edges;image-rendering:pixelated}
.title-top{position:absolute;left:0;right:0;top:calc(9vh + env(safe-area-inset-top,0px));text-align:center;padding:0 24px}
.wordmark{font:600 64px/1 var(--display);letter-spacing:.02em;margin:0;color:#FFF6CF;text-shadow:0 4px 0 rgba(10,8,30,.45)}
.tagline{font:500 18px/1.4 var(--display);margin:12px 0 0;color:#EDE6FF}
.titlemode.lite .wordmark{color:#3B2E6E;text-shadow:0 4px 0 rgba(255,255,255,.55)}
.titlemode.lite .tagline{color:#3B2E6E}
.title-bottom{position:absolute;left:0;right:0;bottom:0;padding:0 20px calc(26px + env(safe-area-inset-bottom,0px));display:grid;justify-items:center;gap:10px}
.title-bottom .primary{max-width:340px;box-shadow:0 6px 0 rgba(10,8,30,.25)}
.tsmall{font-size:14px;color:#EDE6FF;text-align:center;margin:0;text-shadow:0 1px 2px rgba(0,0,0,.5)}
.titlemode.lite .tsmall{color:#2E2A47;text-shadow:0 1px 2px rgba(255,255,255,.7)}
.title-card{width:100%;max-width:400px;background:rgba(22,18,46,.9);border:1px solid rgba(255,255,255,.14);border-radius:22px;padding:18px 18px 16px;display:grid;gap:10px;justify-items:center;color:#fff;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);animation:rise .35s ease-out}
.title-card .rv-title{margin:0}.title-card .rv-hint{margin:0}
@keyframes rise{from{transform:translateY(24px);opacity:0}to{transform:none;opacity:1}}
@media (prefers-reduced-motion: reduce){.title-card{animation:none}#titleCv{transition:none}}
.titlemode.asking #titleCv{transform:translateY(-13vh)}
/* Nav */''')

TITLE_JS = r'''
/* ---- The title scene: the first thing a new player sees. The living sky for their time of day,
   a small fire, and a Forgeling asleep beside it. The age question rises into it on Begin. ---- */
const TITLE_MATE={id:-7,seed:20261016,rarity:1,dark:false,theme:0,v:11,keep:'',bond:0,name:'',nick:'',stats:[3,3,3]};
let titleRAF=0,titleLast=0;
function titleDark(){const ph=skyPhase();return skyDark()||ph==='night'||ph==='dusk';}
function drawTitle(t){
  const cv=document.getElementById('titleCv');if(!cv){cancelAnimationFrame(titleRAF);titleRAF=0;return;}
  const asp=Math.max(1,innerHeight)/Math.max(1,innerWidth);let W=80,H=Math.round(80*asp);if(H<120){H=120;W=Math.min(360,Math.round(120/asp));}
  if(cv.width!==W||cv.height!==H){cv.width=W;cv.height=H;}
  const ph=skyPhase(),dk=titleDark(),P=SKY[dk?'dark':'light'][ph],ctx=cv.getContext('2d'),img=ctx.createImageData(W,H),d=img.data;
  const put=(x,y,c)=>{x=Math.floor(x);y=Math.floor(y);if(x<0||y<0||x>=W||y>=H)return;const q=typeof c==='string'?hexRGB(c):c,o=(y*W+x)*4;d[o]=q[0];d[o+1]=q[1];d[o+2]=q[2];d[o+3]=255;};
  const s0=hexRGB(P.s[0]),s1=hexRGB(P.s[1]),NB=8,GY=Math.round(H*.6);
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){const f=Math.min(1,y/GY)*NB;let bi=Math.floor(f);if(f-bi>(BAY[(y&3)*4+(x&3)]+.5)/16)bi++;const k=Math.min(1,bi/NB),o=(y*W+x)*4;d[o]=lerp(s0[0],s1[0],k);d[o+1]=lerp(s0[1],s1[1],k);d[o+2]=lerp(s0[2],s1[2],k);d[o+3]=255;}
  const r=mulberry32(808);
  if(P.st)for(let i=0,n=Math.round(W*GY/170);i<n;i++){const x=r()*W,y=r()*GY*.8,tw=REDUCE?1:Math.sin(t/700+i*1.7);if(y<H*.27&&x>W*.08&&x<W*.92)continue;if(tw>-.4)put(x,y,P.st);}
  if(P.orb){const cx=W-16,cy=Math.round(H*.41),R=ph==='day'?5:4;for(let y=-R;y<=R;y++)for(let x=-R;x<=R;x++)if(x*x+y*y<=R*R+1&&!(ph==='night'&&(x-2)*(x-2)+(y+1)*(y+1)<=R*R-2))put(cx+x,cy+y,P.orb);}
  for(let x=0;x<W;x++){const top=Math.round(GY-9+3*Math.sin(x*.09+1)+2*Math.sin(x*.23));for(let y=top;y<H;y++)put(x,y,P.h[0]);}
  for(let x=0;x<W;x++){const top=Math.round(GY-3+2*Math.sin(x*.07+3)+1.2*Math.sin(x*.31));for(let y=top;y<H;y++)put(x,y,P.h[1]);}
  const g0=hexRGB(P.h[1]),gD=[Math.round(g0[0]*.8),Math.round(g0[1]*.8),Math.round(g0[2]*.8)];
  const rg=mulberry32(99);for(let i=0,n=Math.round(W*(H-GY)/60);i<n;i++){const x=Math.floor(rg()*W),y=GY+3+Math.floor(rg()*(H-GY-3));put(x,y,gD);put(x+1,y-1,gD);put(x+2,y,gD);}
  /* the Forgeling, asleep */
  const cx=Math.round(W/2)+8,FY=GY+4,mx=cx-40,my=FY-30,breathe=REDUCE?0:Math.floor(t/1600)%2;
  for(let y=-2;y<=2;y++)for(let x=-11;x<=11;x++)if(x*x/121+y*y/5<=1){const X=mx+16+x,Y=my+30+y;if(X>=0&&Y>=0&&X<W&&Y<H){const o=(Y*W+X)*4;d[o]*=.65;d[o+1]*=.65;d[o+2]*=.65;}}
  try{const e=prep(TITLE_MATE),si=1;if(!e.sp[si])e.sp[si]=buildSprite(e.spec,0,1);const g=e.sp[si];
    for(let sy=0;sy<32;sy++)for(let sx=0;sx<32;sx++){const sl=g[sy*32+sx];if(sl)put(mx+sx,my+sy+breathe,e.pal[sl]);}}catch(err){}
  const zt=REDUCE?1:((t/900)%3);if(zt<2.5){const zy=my+2-Math.floor(zt*3),zx=mx+24+Math.floor(zt*1.5);ZB.forEach((row,j)=>{for(let k=0;k<3;k++)if(row[k]==='#')put(zx+k,zy+j,[230,236,255]);});}
  /* the fire */
  const fl=k=>REDUCE?0:Math.sin(t/80+k*1.9)*.9+Math.sin(t/37+k)*.5;
  for(let x=cx-7;x<=cx+7;x++){put(x,FY,[107,74,46]);put(x,FY+1,[75,50,31]);}
  for(let h=0;h<12;h++){const half=Math.max(0,Math.round(4-h*.32+fl(h)*.6)),y=FY-1-h,col=h<3?[229,68,30]:h<6?[255,138,46]:h<9?[255,214,90]:[255,243,176],sh=Math.round(fl(h+3)*.8);for(let x=-half;x<=half;x++)put(cx+x+sh,y,col);}
  if(!REDUCE)for(let i=0;i<5;i++){const p2=((t/60)+i*13)%30,x=cx+Math.round(Math.sin(t/500+i*2.3)*6),y=FY-6-p2;if(y>GY-40)put(x,y,p2<18?[255,200,90]:[255,120,60]);}
  for(let y=Math.max(0,FY-34);y<Math.min(H,FY+30);y++)for(let x=Math.max(0,cx-40);x<Math.min(W,cx+40);x++){const dist=Math.hypot(x-cx,(y-FY)*1.3);if(dist<38){let k=1-dist/38;k=k*k*(dk?.5:.28);const o=(y*W+x)*4;d[o]=lerp(d[o],255,k);d[o+1]=lerp(d[o+1],160,k);d[o+2]=lerp(d[o+2],70,k);}}
  ctx.putImageData(img,0,0);
}
function titleLoop(ts){if(!document.getElementById('titleCv')){titleRAF=0;return;}if(ts-titleLast>90){titleLast=ts;drawTitle(ts);}titleRAF=requestAnimationFrame(titleLoop);}
function openTitle(){
  openOverlay(`<canvas id="titleCv" aria-hidden="true"></canvas>
    <div class="title-top"><h1 class="wordmark" id="dlgTitle">Forge</h1><p class="tagline">One small thing a day.<br>A small creature to keep it.</p></div>
    <div class="title-bottom" id="titleBottom"><button class="primary" id="titleGo">Begin</button><p class="tsmall">No account. Everything stays on this phone.</p></div>`,false);
  const sc=modal.querySelector('.scrim');sc.classList.add('titlemode');sc.classList.toggle('lite',!titleDark());
  drawTitle(performance.now());if(!REDUCE&&!titleRAF)titleRAF=requestAnimationFrame(titleLoop);
}
window.addEventListener('resize',()=>{if(document.getElementById('titleCv'))drawTitle(performance.now());});
'''
rep('/* ================= Start ================= */', TITLE_JS + '\n/* ================= Start ================= */')

# The age question now rises into the title scene. Same question, same rules, same ids.
rep("""function openAgeGate(){
  const yr=new Date().getFullYear();
  openOverlay(`<p class="rv-title">Before we begin</p>
    <p class="rv-hint">When were you born? We use this to set up Forge for you, and we do not keep your birth date.</p>
    <div class="form">""", """function ageFormHTML(){
  const yr=new Date().getFullYear();
  return `<div class="title-card" role="group" aria-labelledby="ageHead"><p class="rv-title" id="ageHead">Before we begin</p>
    <p class="rv-hint">When were you born? We use this to set up Forge for you, and we do not keep your birth date.</p>
    <div class="form">""")
rep("""    <button class="primary" id="ageGo">Continue</button>`,false);
}""", """    <button class="primary" id="ageGo">Continue</button></div>`;
}
function openAgeGate(){openTitle();}
function showAgeForm(){const b=$('#titleBottom');if(!b)return;const sc=modal.querySelector('.scrim');if(sc)sc.classList.add('asking');b.innerHTML=ageFormHTML();const m=$('#ageM');if(m)m.focus({preventScroll:true});}""")

rep("  else if(b.id==='ageGo')submitAge();", "  else if(b.id==='ageGo')submitAge();\n  else if(b.id==='titleGo')showAgeForm();")


# ================= 2. Home-screen icon and colours =================
rep('<title>Forge (prototype 0.20.0)</title>', '<title>Forge (prototype 0.20.0)</title>\n<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAAOuklEQVR4nMVaSYwkx3V970dk1tLdM8OeGc6QHJMUJVKiSEEiaVkLYEmwVli2IMIwDJi++KCzYV0MGPbJMGD7YMCADRjwwRdD0EGQDwJsA4K8iIIAWftGiRLFfWZ6tp5ea8mM+M+HrOqu7srqaY5JKJBVqMqMjPgv/v4j+L5H/gRvYKMzCABocFPW6z1BBF73Mfcb4St5nXBCFXsjLvH1ni7qDQMgMKp+ePy1gKpQ/Urx8HPlE4XGAme7kYR020RE3P67RzQRAEg4QgQkUTTKKQe4h0FCytmMZjxqvMXtDeGAIzgNoMt3t5IpFV6NllWXhbKLjEqAJBSFrZzojkf1uMrk7WC4FQcII1zH1xRlFufyS2f8UuWx38Nn/uy+Tgfs8VtPp3//t68uLdEdL8a3p9Df3hj81qfe8tf/8Km//Yuv/NM/fn/1dC8nf80AjuAAgZRRVSwKFPFYckrIYcu+fj69NMzFSj++58NPYDngRDG48vL/fuH5k70yJ70SHqwEC9jYHH//O5euXR2ESJduQxwWAiCQHCeWdP6BfP26rW9ZsOMML8AdoWaZWNQIu9uplwXHcIxknRpFphzInvv9+K1vXnrqyc+XZVhajjnn10o9AIPUehm1M8D73zH63OevfPqDw80dmrX3PHTJHRCnlxkt0AKN2Ls56SnFwOXloigoP9bg89dCDrhQFnjhcvjivyz98BexU7ofS4iagW/VaR8uWrtz0u3WbaESu9At9ePnwzf/8mS3q37H/VYcni6wG2GBAbSwwLCo+Syk0CcDHgPAEXojoYhYPZXc6bdaDYEZBaCa5WBX28Nq5JB76/pon1ELNXDhs0MAju4mIeVbDyWw0PgBf9YMu7v4yAf12BMP1bvqdK3smFxzJl6tHDBit7J33TP4+z94+QtfP/03/332dD8nP4oTx7OOt2oOFqru9V9EcnNYvefxh977mXuxXsOIneSpccwgJxc0AXBobmFiBUaVVRmNoh9N4K2DuT233xqHNc+MAlCjdLAmB0P4eu0368b+TMYRUlJOylnoCNzThJmFEHpFfvZa+Ym/ezOJla7X3j7vPoCjfQfhUbmhMzPMxmF7v0gImppOEDKDBWKGeghFyZWTcelEzFllnWqvjNllCeEQDkId5gZ0ZhDsKACLrBChGvGcrr3df1yjCEg/sMc2eCoiCSQAgsCEYvCIYMwCsZPe+7Ezj39wtVGGv/qjZy6/Mu6X+SrO/SQ8EpEclEAoIZ7Sxjv9uwmxQP2MPXKF5wokLbBJ7RzgVMkCc8dqAwokQwaccJAEMZXpxheavBGYEA5GZTQAEGJHsTtZy4Ipqi6QAzMNcBEgG8vkhty1uoYK1IG58e6zMexBAG0cqBEI1IzDFLbGrMEIG3VDHaIAEyIT0UwdEwmGpLB9sw6Rm+t1Nfa9eBl5gEbEPIrF9C73ruYjISkIqBFHHjZGlsECHHZCFWOjyREtnqhdiS/oYol6mOLbVrc/+qZYJ4uB6bm1i9ub3ZCG6N2wswYJdkZXl7RbebhjxT/5ybuNHA3zmx5exthJgBEnHwcDGDC+xOELYDE7IyHSTRBx3te6GI5yvGdl+JvvijmziLF44fpP18e9kCoUazx3XBF6QC+c4O5mZe+7M37q410MhJIXr77aXc8nLN/A6Ru405CTxXP1pfO6tDsK95zvPfnZJxqiMHQMnRRY4PRHYV2EHtb/C7vPIpZ7WieAhBGUBLtXr6zixnYdHjkRPv2RHiqhH3e+uJbWXj3Z8y0tXeadbRxoF6GiYlnThsl8V2mImDT2WDOMkWsEQkYYkRErlDVDpSLfrBvbaNYkilMRUoYyVLUEB4IBZjKpRmiGGjvzQLlClIYp1rSKXqtoJTUKLTnEJJCkjDJDMJjtx5JGmTV200lRk0ehNfKhTa42FSRBc7pIGUVNbHEwwGAG435g20rq4mDOVVUutdlggZJRsDkvQ0Ma4PSHsPJu+AAMsBLyBYEZAQTCJjF2KyGz87ZzoLWn+v3QWS7LMu+Na4Q1qyKQMtPEZ5EhzGblQlhCeRZ5FzQotcQ8xtAkCTbhp0lmjThhkUtpJTViji/BuLudP/CROz7+1P3f/tfnMdy1YACGFXaGYNYgEN0oUCGOtrQ7qgdVGOykmakcqqEaaJecwU7a2Uxe5nFXWG3EOAx3WWTtVBhWi+hvE6F5P+COIvLS2vjbT6/f3KhxgXBAePR+O7WsXhmvDtPmlbUyqKrsHe8sL5w9Nx5i9c7i4DBTN93WHv/AHfe/re708Oq1cvvZS0X0Kttj96WzvTis7MKZfcFseDVB0CpC85zJUrdr3/vh9pef3v6NxyOeKDQAMz75/gACJS+/VL34uWd6PW7dTE/+7sMP//absFGDxCBPKF/Upo9+54/vh4RTxU++dOWlz/7gxGocDvX77+vedV8HlSCgblw9Brtp82bun12YILR7YglFwZWVEMNk+SF4BXdY1qCiW5FJGUdD+Ubtm8niayhO+U7yJANGQykUmdFNg4o+lFdolIEERv7rHzv7wId6X/vSxc0NwVqIXRhOS3CXSEQyAgZzobHxwLiWBYwrCdPA87WU1syIAAsUMK5U1hrXImBT6wkjSVT50Q+dfvTeM9/5zyv5ulC2W6EF1kuwyOp62np6OMqk69Sj/eJkRK27z/BPf6+wwDziXRcMNeyogHcRBqDGWy/Ynz9VhG70rLvPEDUsst5MGz8ayNilf/mrz/+surhxY1yU3dbcpkWE2JAPgPBK9bV6LDJJ9SQL6ZZ4870EiZrot9oGzVw4+HumOZb6eMt9REEISE3QCdUaX6sVGIIuvjL46eb49BJIqS3BvlVGRrAgnZy1KII3YUEFequDjbAOlKaxtMM6YGwB6tB4gm5fBgkWRCANZc/6KZJpPn2bALh1Tty2fHaUkTTU6xj8Aj5qMh9IsC7qdczlVmyUdX6c6aRyuAthcvc1KPFttmaxN7+JzW/MPTNYB3rN5dvZ0edvtSgxAd9POOCCN8I/y4oZcWopxjEA8wJzsNukNneQPE16eWMGm1x7n5hWHZi/SRTIJVIBlfR+EAhCsSBKTkhP07eioYwAMJtHZsd8JcyIEA4AKCPijFAVbL5jwb5JAX1TSS+QSuRC+TDgZv75ewJ+lO/q0CuE3eEOLq1VCln6xA9H51fGVaXyRFh5qAcXguHn13BxEz6NNwnUjvtXcc9J1HlfB4qAi5t4cR3FXo1bMMOgQmhyO27/dFht5bLk2rb+40o3kCXz10bnnsdy6bmSqU2R23VgzVeMdIustVTHhFhL7748OLXhg0r9s8XKW3twwIhrOwd4SGKcsNrHr5zaH1iAEVsjvHgDnXi4fzQ4EDC6Wg+u1f2SN4b23e1+QUbwBS6v4Q5TcsmOGcwJiEgByFJpuW9KUO2KBVnSABaEEQEgUIaDNR1CQGEIhsgpB4BgKAxlRHkIwPTbyIJWkiVjYt9UGCJUeoqqA1IWsjgvRO0cmPVDLjjke0oMKCvtZGQBCB0yHspqhFHC1ghV2hehccYoHajqYuKz8lgAEDjZRJ4qsUt+kJLj+oGJ8yRcaqKh2YcWWG/lq/+z2fjp07+63LtQoprWbBpxf+4anrs2PxmKsE+9gIKjtfrGt3asnCyBBR6iUpJLBu3vaRwGMAfLNdnYEx2AYBN7umdSOeOQFkQJ7b7p0N+DL+6ZTp+YzmZqCHKpManzSnCEI5NkhHeQCCPQNy1FFQ4XxtOSNwuiM7U/e6QntJjRwAOzCeiQxT7QnsmI0tQ3lUgFUMBtsmiLJGhBKOEAJGPe9PIHOC/Swa9sXH9mZzxwO1P6r51MSWDg4OVxtZ72ySU8oXdX0TkzU88UEDm+Xg8v1zaLwZh2MgMlROLrG8X1yvrml1PnZzxjEqFNLylviuzeFjm3cECYlL4Nvq1y07vRKPIbWzt3yHc8PLiU33syCTDD4HIFP7D8PlbosnMowzRUN9PWs0Pr8AATDBbpgAHf2yp+vhuWLd9k9yU7DXkSTNngeXHEtiAjm8Iy5AI5ii72o6/A6ewHn1hRwQruUe+aerO4X7neA8ZI67DRVzsQiUzqc/3gK5HL5mO55cogunKz8JqGLMfhAKZ6LEGkC1kSWbmNLVQKY2GYWelAQGRAaVM7mOWVUM+IEKCsPcUdZfrBeCoTY00Gr2CCHMr7wVG7pQDA++76WCtr2BSCOEnugrGAFwZnOM3h47y0lwgQSMJqqT+8ZzS5Y2Q4OCGhDE1V5Z8vdterA/7DoO/i7hvqmefaUcHc5cK+/VkgQ0flA1OzNYlCalp2yDAGB+I00AGBWuj5TPE7C2luuBmJGjp3ncUBABiDY4FiFoTJwYNF5n8fwMKkvuGdmBUCkTOCMRAuytgl60m6BQIUusDJY2fGXbAUy+ncDhSAi8lJ0YGc4Wj2djOgRdszRwEAlJ29YrzS2RXMIBIkBQSmK6xnRSgDo6Av7hwXwMuh3u0ckDKDotZXFK3xXA6BgG+Pl0Z1CS6qri4WIcKzx04c3XXycvIwe6pK4MW54QT8eOu4lZVuUbE4fLPE9dNTRCQERubq5oXdcSdYXrTVd+ROPZSF5LEBMIMNse2tzrFFyNUCVTCf+SMQ1uhDY4Xa6YxHJalyTAr2hzfLWwe7ndMyB0fl4b/NoRbfj4TnWjsH7l9d68RUJZw9WTx4z50pzZ8VeMObhBjZ7Wxf21wvI8Ypvrh+fr5bS60GQBnqTqgpdIrQLUOyXxqATuGdUJVh4cHGqDYRImHW7ILJSCN+CQAAI/e2uUi0ktpuRjdHvWFVVplW8PrmMOVjHd15fZuAGHBjp1gfxrJS5aGV1HYz+srNVQrJw9ZoW2ktKXChrXqjmojI/ML6+fXdlWhZRGBrUt8GKzA3RziCeQhBfrvHUv8frakEBPNgKdjCk58Lk3pMKpEyuvGXI0JGR3NmaPE5vIWeuHl/e1T+5MqdR8UimOwF4aCvn1f6Q/MIi53TtAOJcR2NCw6uNQAWx0IAVbuNhx0uPnPE+R9HMmu2KHHox/zIEszENtHfa/8Hzao6PKzfE+cAAAAASUVORK5CYII=">\n<link rel="apple-touch-icon" href="data:image/png;base64,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">\n<meta name="apple-mobile-web-app-title" content="Forge">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<meta name="theme-color" content="#F1EDF8" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#16132E" media="(prefers-color-scheme: dark)">')

# ================= 3. A calmer first minute =================
# Ribbon notes wait until nothing else is on screen, so they never land on top of the reveal.
rep("function checkRibbons(){\n  if(pk||rv||!state||!state.ageBand)return;", "let ribbonMsg='';\nfunction flushRibbon(){if(ribbonMsg&&modal.hidden&&!pk&&!rv){const m=ribbonMsg;ribbonMsg='';toast(m);chime(3);}}\nfunction checkRibbons(){\n  if(ribbonMsg)setTimeout(flushRibbon,600);\n  if(pk||rv||!state||!state.ageBand)return;")
rep("const r=RIBBONS.find(x=>x.id===add[0]);setTimeout(()=>{toast('New ribbon: '+r.name+(add.length>1?' and '+(add.length-1)+' more':''));chime(3);},600);}", "const r=RIBBONS.find(x=>x.id===add[0]);ribbonMsg='New ribbon: '+r.name+(add.length>1?' and '+(add.length-1)+' more':'');setTimeout(flushRibbon,600);}")
# The nudge question becomes the close of the first day.
rep("""function openNudge(){
  openSheet(`<h2>Want a gentle nudge?</h2><p class="muted">Pick a time and you'll hear when your next card is ready. Change it anytime in Settings.</p>""",
    """function openNudge(){
  const first=doneDays()<=1,c=state.cards[state.cards.length-1];
  openSheet(`${first?`<h2>That\\u2019s your first day</h2><p class="muted">${c?esc(c.nick||c.name)+' is in your binder, and t':'T'}he Hearth is ready whenever you are. A new card arrives tomorrow.</p><h3 style="margin:14px 0 0">Want a gentle nudge?</h3><p class="muted small">Pick a time and you\\u2019ll hear when your next card is ready. Change it anytime in Settings.</p>`:`<h2>Want a gentle nudge?</h2><p class="muted">Pick a time and you'll hear when your next card is ready. Change it anytime in Settings.</p>`}""")
rep("""    <p class="muted small center" style="margin-top:6px">Prototype only. Nothing is sent yet.</p>`);
}""", """    <p class="muted small center" style="margin-top:6px">Prototype only. Nothing is sent yet.</p>`);
}""")

rep("  if(!state.nudgeAsked){state.nudgeAsked=true;save();setTimeout(openNudge,1200);}", "  if(!state.nudgeAsked){state.nudgeAsked=true;save();setTimeout(openNudge,500);}")

# ================= 4. A gentle arrival, and a greeting =================
rep('/* Nav */', """@keyframes arrive{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes skyIn{from{opacity:0}to{opacity:1}}
body.arrive #skyCv{animation:skyIn .8s ease both}
body.arrive .app header.top{animation:arrive .5s ease both}
body.arrive .app section:not([hidden])>*{animation:arrive .55s ease both}
body.arrive .app section:not([hidden])>*:nth-child(1){animation-delay:.1s}
body.arrive .app section:not([hidden])>*:nth-child(2){animation-delay:.2s}
body.arrive .app section:not([hidden])>*:nth-child(3){animation-delay:.3s}
body.arrive .app section:not([hidden])>*:nth-child(n+4){animation-delay:.38s}
/* Nav */""")
rep("  $('#dateLabel').textContent=`Day ${dayN()}, ${dateLabel(todayKey())}`;",
    "  $('#dateLabel').textContent=(tab==='today'?greeting()+' \\u00B7 ':'')+`Day ${dayN()}, ${dateLabel(todayKey())}`;")
rep('/* ================= Start ================= */', r"""function greeting(){const h=new Date().getHours();return h>=5&&h<12?'Good morning':h>=12&&h<17?'Good afternoon':h>=17&&h<22?'Good evening':'Hello, night owl';}
let arriveT=0,hiddenAt=0;
function arrive(){if(REDUCE)return;document.body.classList.remove('arrive');void document.body.offsetWidth;document.body.classList.add('arrive');clearTimeout(arriveT);arriveT=setTimeout(()=>document.body.classList.remove('arrive'),1300);}
document.addEventListener('visibilitychange',()=>{if(document.hidden)hiddenAt=Date.now();else if(hiddenAt&&Date.now()-hiddenAt>10*60*1000&&state&&state.ageBand&&modal.hidden){renderNav();arrive();}});
/* ================= Start ================= */""")
rep("""  if(returned&&modal.hidden){tab='hearth';render();window.scrollTo(0,0);}
  wanderTick();""", """  if(returned&&modal.hidden){tab='hearth';render();window.scrollTo(0,0);}
  if(state.ageBand)arrive();
  wanderTick();""")

# ================= version =================
rep('<title>Forge (prototype 0.20.0)</title>', '<title>Forge (prototype 0.21.0)</title>')
rep("const VERSION='prototype 0.20.0';", "const VERSION='prototype 0.21.0';")
rep('const SEEN_V=24;', 'const SEEN_V=25;')
rep("""<ul class="newlist"><li><b>Wander somewhere.</b>""",
    """<ul class="newlist"><li><b>A warmer welcome.</b> Forge now opens gently, with a greeting for the time of day. New players start by a small fire under your own sky.</li>
    <li><b>An icon for your home screen.</b> Add Forge to your home screen and it gets its own little campfire.</li>
    <li><b>Wander somewhere.</b>""")

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
