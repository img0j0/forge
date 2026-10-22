# Forge 0.24.0: share a Forgeling picture, backups that nudge and save as a file, more variety in callings,
# and one optional small thing of your own. Reads base23.html, writes work.html.
src = open('base23.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ================= CSS =================
rep('/* Nav */', r'''/* ---- 0.24: share picture, backups, your own small thing ---- */
.shareimg{display:block;width:min(100%,300px);height:auto;margin:4px auto 2px;box-shadow:0 10px 30px rgba(0,0,0,.45)}
.filepick{position:relative;display:inline-flex;align-items:center;justify-content:center;min-height:44px;cursor:pointer;overflow:hidden}
.filepick input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:pointer;font-size:16px}
.filepick:focus-within{outline:3px solid var(--butter);outline-offset:2px}
.cal .c{position:relative}
.cal .c.own::after,#view-chronicle .cal span.c.own::after{content:'';position:absolute;right:3px;bottom:3px;width:7px;height:7px;background:#F2B23E;box-shadow:0 0 0 1.5px var(--ink)}
.calkey i.ownkey{width:8px;height:8px;background:#F2B23E;box-shadow:0 0 0 1.5px var(--ink);vertical-align:1px}
.rowl.ownrow[aria-pressed="true"] .ri{color:#3E8E4F}
/* Nav */''')

# ================= Calling variety =================
rep('/* Each theme has a cute palette and a dark twin.', r'''/* 0.24: more ways to say each calling, so the daily card stays fresh. The original phrasing is one of them. */
const TASK_ALT=[
 [`Pick one thing on your plate and decide you won't do it.`,`Clear one small space: a drawer, a desktop or an inbox folder.`,`Say no to one thing that doesn't need a yes.`],
 [`Do first the one thing that would make today feel done.`,`Find the task that unblocks someone else, and do it.`,`Spend ten minutes setting up tomorrow so it starts easier.`],
 [`Pick one thing and give it 25 minutes with notifications off.`,`Read something long for 20 minutes without skimming.`,`Stay with one problem until you've made real progress, no switching.`],
 [`Send the draft you've been sitting on.`,`Make a rough first version of something, start to finish.`,`Make the decision you've been going back and forth on.`],
 [`Tell someone one specific thing you appreciate about them.`,`Call or voice-message someone instead of texting.`,`Check in on someone you haven't heard from in a while.`],
 [`Start the task you'd rather avoid. Five minutes is enough.`,`Make the call or send the email you've been dreading.`,`Do the hardest thing on your list before anything else.`],
 [`Spend ten minutes on something with no purpose but fun.`,`Try one small thing you've never done before.`,`Make something silly, just for you.`],
 [`Go back to something you made and fix one small thing.`,`Spend ten minutes tidying up a piece of your work.`,`Learn one small trick that makes your work better.`],
 [`Take a five-minute walk with nothing in your ears.`,`Sit somewhere quiet and let your thoughts wander for five minutes.`,`Write down whatever is on your mind, then put the pen down.`],
 [`Ask the question you've been holding back.`,`Tell someone honestly how you feel about something.`,`Bring up the small problem you've been ignoring.`],
 [`Simplify one thing you do every week.`,`Give one thing you keep losing a place where it lives.`,`Write down the steps for something you always have to remember.`],
 [`Eat one meal without a screen.`,`Notice five things around you that you'd usually walk past.`,`Give your full attention to the next conversation you have.`]];
function taskFor(v,k){const V=VECTORS[v];if(!V)return '';const all=[V.task].concat(TASK_ALT[v]||[]),n=Math.floor(Date.parse(String(k)+'T00:00:00Z')/864e5);if(!Number.isFinite(n))return V.task;return all[((Math.imul(n,0x9E3779B1)>>>0)+v)%all.length];}
/* Each theme has a cute palette and a dark twin.''')
rep("<p><strong>Today's small thing</strong>${V.task}</p>", "<p><strong>Today's small thing</strong>${taskFor(state.todayV,state.date)}</p>")
rep('<div class="taskface"><div class="band" style="background:${V.color}">${V.name}</div><p>${V.task}</p></div>',
    '<div class="taskface"><div class="band" style="background:${V.color}">${V.name}</div><p>${taskFor(state.todayV,state.date)}</p></div>')

# ================= State =================
rep("games:{best:{},played:0,curioDay:''}};}", "games:{best:{},played:0,curioDay:''},own:{text:'',days:[]},backup:{at:'',ask:''}};}")
rep("  s.keepsR=Array.isArray(s.keepsR)?", r"""  {const o=s.own&&typeof s.own==='object'&&!Array.isArray(s.own)?s.own:{};const DK=/^\d{4}-\d{2}-\d{2}$/;s.own={text:typeof o.text==='string'?o.text.trim().slice(0,60):'',days:(Array.isArray(o.days)?o.days:[]).filter((d,i,a)=>typeof d==='string'&&DK.test(d)&&a.indexOf(d)===i).sort().slice(-800)};
   const bk=s.backup&&typeof s.backup==='object'&&!Array.isArray(s.backup)?s.backup:{};s.backup={at:typeof bk.at==='string'&&DK.test(bk.at)?bk.at:'',ask:typeof bk.ask==='string'&&DK.test(bk.ask)?bk.ask:''};}
  s.keepsR=Array.isArray(s.keepsR)?""")

# ================= Today: your own small thing, and the backup nudge =================
rep("""<path d="M4 7h16M12 11l2.5 2-2.5 4-2.5-4z"/></svg>'};""",
    """<path d="M4 7h16M12 11l2.5 2-2.5 4-2.5-4z"/></svg>',
    tick:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="2"/><path d="M7.5 12.5l3 3 6-7"/></svg>',
    ring:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="2"/></svg>',
    save:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v11M7.5 10l4.5 4.5 4.5-4.5"/><path d="M4 15v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/></svg>'};""")
rep("  const jr=state.journal[state.date],reflect=", r"""  if(state.own&&state.own.text){const on=state.own.days.includes(todayKey());rows.unshift(`<button class="rowl ownrow${on?' ready':''}" id="btnOwn" aria-pressed="${on}"><span class="ri">${on?IC.tick:IC.ring}</span><span class="rt"><b>${esc(state.own.text)}</b><span class="rs">${on?'Done today. Tap again if you didn’t mean to.':'Your own small thing. Tap when it’s done.'}</span></span></button>`);}
  if(backupDue())rows.push(row('btnBackup',IC.save,'Save a copy of your collection','It all lives on this phone. A copy once a month keeps it safe.'));
  const jr=state.journal[state.date],reflect=""")
rep("  if(b.id==='btnTurn'||b.id==='btnTurnGo'||b.id==='btnCard')openVector();",
    "  if(b.id==='btnOwn'){toggleOwn();return;}\n  if(b.id==='btnBackup'){openBackupNudge();return;}\n  if(b.id==='btnTurn'||b.id==='btnTurnGo'||b.id==='btnCard')openVector();")

# ================= Journal calendar =================
rep("  let n=0;\n  const cells=days.map(k=>{", "  let n=0,no=0;const ownSet=new Set((state.own&&state.own.days)||[]);\n  const cells=days.map(k=>{")
rep("    if(k===today)cls+=' now';\n    return `<span class=\"${cls}\"",
    "    if(k===today)cls+=' now';\n    if(ownSet.has(k)&&k>=state.startDate){cls+=' own';label+=', your own small thing done';no++;}\n    return `<span class=\"${cls}\"")
rep("""<span><i style="background-image:var(--stM)"></i>rested</span></div>${didHTML(days.filter(k=>k>=state.startDate))}</div>`;""",
    """<span><i style="background-image:var(--stM)"></i>rested</span>${ownSet.size?'<span><i class="ownkey"></i>your own small thing</span>':''}</div>${didHTML(days.filter(k=>k>=state.startDate))}${no?`<p class="small" style="margin-top:10px">You did your own small thing on ${no} of these days${state.own.text?': '+esc(state.own.text).replace(/[.!?]+$/,''):''}.</p>`:''}</div>`;""")

# ================= Settings: your own small thing =================
rep("""    <div class="setblock"><b>Morning nudge</b>""",
    """    <div class="setblock"><b>Your own small thing</b><p class="muted small">Optional. One habit of your own to tick off on Today, beside the daily card. It never earns packs, and missing it never counts against you.</p>
      <label class="field"><span>Your small thing</span><input id="ownIn" maxlength="60" value="${esc(state.own.text)}" placeholder="For example: drink a glass of water" autocomplete="off"></label>
      <div class="chips"><button class="pill" id="ownSave">${state.own.text?'Save changes':'Add it to Today'}</button>${state.own.text?'<button class="pill" id="ownClear">Remove it</button>':''}</div></div>
    <div class="setblock"><b>Morning nudge</b>""")
rep("  else if(b.id==='btnExport')openExport();",
    """  else if(b.id==='ownSave'){const v=(($('#ownIn')||{}).value||'').trim().slice(0,60);if(!v){sfx('no');toast('Write a few words first.');return;}state.own.text=v;save();renderSettings();renderToday();toast('Saved. It is on Today, ready to tick.');}
  else if(b.id==='ownClear'){state.own.text='';save();renderSettings();renderToday();toast('Removed. Your past ticks stay in the Journal.');}
  else if(b.id==='btnExport')openExport();""")

# ================= Backup: save as a file, restore from a file =================
rep("""  openSheet(`<h2>Save a copy</h2><p class="muted small">Copy this text and keep it somewhere safe. Paste it into Restore on any device.</p>
    <textarea class="box" id="expText" readonly>${esc(txt)}</textarea>
    <div class="stack"><button class="primary" id="copyExp">Copy</button><button class="ghost" data-close>Close</button></div>`);""",
    """  openSheet(`<h2>Save a copy</h2><p class="muted small">Save your whole collection as a small file. Keep it in Files, a notes app or your email, and restore it on this phone or a new one.</p>
    <button class="primary" id="saveFile" style="width:100%">Save as a file</button>
    <p class="muted small" style="margin:14px 0 4px">Or copy it as text:</p>
    <textarea class="box" id="expText" readonly aria-label="Your saved copy as text">${esc(txt)}</textarea>
    <div class="stack"><button class="ghost" id="copyExp">Copy the text</button><button class="ghost" data-close>Close</button></div>`);""")
rep("  const t=$('#expText');if(t){t.focus();t.select();}\n", "")
rep("""  openSheet(`<h2>Restore a copy</h2><p class="muted small">Paste a saved copy here. This replaces what is on this device.</p>
    <textarea class="box" id="resText" placeholder="Paste your saved copy"></textarea>""",
    """  openSheet(`<h2>Restore a copy</h2><p class="muted small">Choose a saved file, or paste the text of a saved copy. This replaces what is on this device.</p>
    <label class="pill filepick">Choose a saved file<input type="file" id="resFile" accept=".json,application/json,text/plain"></label>
    <textarea class="box" id="resText" placeholder="Or paste your saved copy" aria-label="Saved copy text"></textarea>""")
rep("  else if(b.id==='copyExp')copyText($('#expText').value,'Copied. Keep it somewhere safe.');",
    """  else if(b.id==='copyExp'){copyText($('#expText').value,'Copied. Keep it somewhere safe.');state.backup.at=todayKey();save();}
  else if(b.id==='saveFile')backupFile();
  else if(b.id==='backupLater'){state.backup.ask=todayKey();save();closeModal();renderToday();toast('No problem. I’ll ask again next month.');}
  else if(b.id==='inspShare')openShare(inspId);
  else if(b.id==='shDo')doShare();
  else if(b.id==='shBack'){const id=+b.dataset.cid;closeModal();inspect(id);}""")
rep("modal.addEventListener('input',e=>{if(e.target.id==='nickIn')syncNick();});",
    """modal.addEventListener('input',e=>{if(e.target.id==='nickIn')syncNick();});
modal.addEventListener('change',e=>{
  if(e.target.id!=='resFile')return;const f=e.target.files&&e.target.files[0];if(!f)return;
  if(f.size>20e6){sfx('no');toast('That file is too big to be a Forge copy.');return;}
  const r=new FileReader();
  r.onload=()=>{const t=$('#resText');if(t)t.value=String(r.result||'');const d=$('#doRestore');if(d){d.dataset.armed='0';d.textContent='Restore';d.focus({preventScroll:true});}toast('File loaded. Tap Restore to use it.');};
  r.onerror=()=>toast('That file could not be read.');r.readAsText(f);
});""")

# ================= Share button on the card =================
rep('<div class="row" style="justify-content:center;gap:22px"><button class="ghost" id="inspFav">','<div class="row" style="justify-content:center;gap:4px 10px;flex-wrap:wrap"><button class="ghost" id="inspFav">')
rep("""<button class="ghost" data-tale="${c.id}">Story</button>${keptAge(c)>=KEPT_DAYS?keptLine(c):''}""",
    """<button class="ghost" data-tale="${c.id}">Story</button><button class="ghost" id="inspShare">Share</button>${keptAge(c)>=KEPT_DAYS?keptLine(c):''}""")

# ================= New functions =================
rep('/* ================= Events ================= */', r'''/* ---- 0.24: your own small thing, backups, and the share picture ---- */
function toggleOwn(){const k=todayKey(),d=state.own.days,i=d.indexOf(k);if(i>=0)d.splice(i,1);else{d.push(k);d.sort();if(d.length>800)d.splice(0,d.length-800);chime(0);}save();renderToday();const b=$('#btnOwn');if(b)b.focus({preventScroll:true});}
function backupDue(){const b=state.backup||{};if(state.cards.length<5||dayN()<7)return false;const last=[b.at,b.ask].filter(Boolean).sort().pop();return !last||daysBetween(last,todayKey())>=30;}
function openBackupNudge(){openSheet(`<h2>Keep your Forgelings safe</h2><p class="muted">Your collection lives only on this phone. If the browser ever clears its storage, a saved copy brings everything back.</p><p class="muted small">Save it to Files, a notes app or your own email. You can restore it any time from Settings, on this phone or a new one.</p><div class="stack"><button class="primary" id="saveFile">Save a copy</button><button class="ghost" id="backupLater">Remind me next month</button></div>`);}
function canShareFiles(){try{return !!(navigator.share&&navigator.canShare&&navigator.canShare({files:[new File([new Blob(['x'])],'x.png',{type:'image/png'})]}));}catch(e){return false;}}
function downloadBlob(blob,name){try{const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;a.rel='noopener';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),4000);return true;}catch(e){toast('Saving did not work here. Try copying the text instead.');return false;}}
function backupFile(){
  const k=todayKey(),name=`forge-backup-${k}.json`,blob=new Blob([JSON.stringify(state)],{type:'application/json'});
  const done=msg=>{state.backup.at=k;save();closeModal();if(tab==='today')renderToday();toast(msg);};
  let f=null;try{f=new File([blob],name,{type:'application/json'});}catch(e){}
  try{if(f&&navigator.share&&navigator.canShare&&navigator.canShare({files:[f]})){navigator.share({files:[f],title:'Forge backup'}).then(()=>done('Saved. Keep it somewhere safe.')).catch(err=>{if(err&&err.name==='AbortError')return;if(downloadBlob(blob,name))done('Saved to your downloads. Keep it somewhere safe.');});return;}}catch(e){}
  if(downloadBlob(blob,name))done('Saved to your downloads. Keep it somewhere safe.');
}
let shareCv=null;
async function shareFonts(){try{await Promise.race([Promise.all(['600 52px Fredoka','400 28px "Nunito Sans"','22px "Press Start 2P"'].map(f=>document.fonts.load(f))),new Promise(r=>setTimeout(r,1500))]);}catch(e){}}
function shareCanvas(c){
  const W=720,H=960,cv=document.createElement('canvas');cv.width=W;cv.height=H;const x=cv.getContext('2d'),R=RAR[c.rarity],nm=c.nick||c.name;
  const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#1B1430');g.addColorStop(1,'#35223C');x.fillStyle=g;x.fillRect(0,0,W,H);
  x.fillStyle=R.edge;x.fillRect(0,0,W,14);x.fillRect(0,H-14,W,14);x.fillRect(0,0,14,H);x.fillRect(W-14,0,14,H);
  x.fillStyle=R.glow;x.fillRect(14,14,W-28,4);x.fillRect(14,14,4,H-28);
  x.fillStyle='#E2B04A';[[22,22],[W-38,22],[22,H-38],[W-38,H-38]].forEach(p=>x.fillRect(p[0],p[1],16,16));
  const src=document.createElement('canvas');src.width=48;src.height=37;drawFrame(prep(c),src,300-(Math.abs(c.seed|0)%2000),null);
  x.fillStyle=R.edge;x.fillRect(64,74,592,460);x.fillStyle=R.glow;x.fillRect(68,78,584,452);
  x.imageSmoothingEnabled=false;x.drawImage(src,72,82,576,444);
  const fit=(t,max,size,w,fam)=>{let s=size;do{x.font=`${w} ${s}px ${fam}`;s-=2;}while(x.measureText(t).width>max&&s>14);};
  const wrap=(t,max)=>{const words=t.split(' '),out=[];let line='';words.forEach(wd=>{const tr=line?line+' '+wd:wd;if(x.measureText(tr).width>max&&line){out.push(line);line=wd;}else line=tr;});if(line)out.push(line);return out;};
  x.textAlign='center';x.textBaseline='alphabetic';let y=604;
  x.fillStyle='#FFF3D6';fit(nm,600,54,600,'Fredoka, sans-serif');x.fillText(nm,W/2,y);
  if(c.nick&&c.nick!==c.name){y+=40;x.fillStyle='#CDBFDB';fit(c.name,600,26,400,'"Nunito Sans", sans-serif');x.fillText(c.name,W/2,y);}
  y+=46;x.fillStyle=R.glow;fit(`${R.name} · ${realmName(c)}`,600,28,600,'"Nunito Sans", sans-serif');x.fillText(`${R.name} · ${realmName(c)}`,W/2,y);
  const found=c.source==='pack'?'Found in a pack, earned by showing up.':(DID[c.v]?`Found the day I'd ${DID[c.v]}.`:'Found by showing up.');
  x.fillStyle='#EDE3F2';x.font='400 27px "Nunito Sans", sans-serif';wrap(found,600).slice(0,3).forEach(l=>{y+=40;x.fillText(l,W/2,y);});
  let when='';try{when=new Date(c.date+'T00:00:00').toLocaleDateString(undefined,{month:'long',day:'numeric',year:'numeric'});}catch(e){}
  if(when){y+=38;x.fillStyle='#B9A9C9';x.font='400 22px "Nunito Sans", sans-serif';x.fillText(when,W/2,y);}
  x.fillStyle='#FFD36B';x.font='22px "Press Start 2P", monospace';x.fillText('FORGE',W/2,H-72);
  x.fillStyle='#B9A9C9';x.font='400 20px "Nunito Sans", sans-serif';x.fillText('Every Forgeling is one of a kind',W/2,H-40);
  return cv;
}
async function openShare(id){
  const c=cardById(id);if(!c)return;await shareFonts();
  const cv=shareCanvas(c),url=cv.toDataURL('image/png'),blob=await new Promise(r=>{try{cv.toBlob(r,'image/png');}catch(e){r(null);}});
  shareCv={c,cv,blob};const can=canShareFiles(),nm=c.nick||c.name;
  ovMode='share';
  openOverlay(`<p class="rv-title">Share ${esc(nm)}</p><img class="shareimg" id="shareImg" src="${url}" alt="A picture card of ${esc(nm)}, ${RAR[c.rarity].name}, from ${esc(realmName(c))}">
    <p class="rv-hint">${can?'Send it to a friend, or save it to your photos.':'Save the picture, then send it however you like.'} It's made on this phone, and nothing is uploaded.</p>
    <div class="btnrow"><button class="primary" id="shDo">${can?'Share':'Save picture'}</button><button class="ghost" id="shBack" data-cid="${c.id}">Back</button></div>`,true);
  ovMode='share';const d=$('#shDo');if(d)d.focus({preventScroll:true});
}
function doShare(){
  const s=shareCv;if(!s)return;if(!s.blob){toast('That picture could not be made here.');return;}
  const nm=s.c.nick||s.c.name,name=(nm.replace(/[^\w\- ]+/g,'').trim().replace(/\s+/g,'-')||'forgeling')+'.png';
  let f=null;try{f=new File([s.blob],name,{type:'image/png'});}catch(e){}
  if(f&&canShareFiles()){navigator.share({files:[f],title:nm}).then(()=>toast('Shared.')).catch(err=>{if(err&&err.name==='AbortError')return;if(downloadBlob(s.blob,name))toast('Picture saved.');});return;}
  if(downloadBlob(s.blob,name))toast('Picture saved.');
}

/* ================= Events ================= */''')

# ================= version and what's new =================
rep('<title>Forge (prototype 0.23.0)</title>', '<title>Forge (prototype 0.24.0)</title>')
rep("const VERSION='prototype 0.23.0';", "const VERSION='prototype 0.24.0';")
rep('const SEEN_V=27;', 'const SEEN_V=28;')
rep("""<ul class="newlist"><li><b>Play together.</b>""",
    """<ul class="newlist"><li><b>Share a Forgeling.</b> Open any Forgeling and tap Share for a picture card you can send a friend. It's made on your phone, and nothing is uploaded.</li>
    <li><b>Keep your collection safe.</b> Once a month, Today offers to save a copy as a file. Restore it from Settings on this phone or a new one.</li>
    <li><b>Fresh callings.</b> Each calling now has several ways of asking, so the daily card keeps surprising you.</li>
    <li><b>Your own small thing.</b> In Settings you can add one habit of your own to tick off on Today. It shows in your Journal, never earns packs and never counts against you.</li>
    <li><b>Play together.</b>""")
# Keep What's new to the latest ten notes (0.22 to 0.24): a phone sheet, not a changelog.
import re as _re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=_re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],_re.S)
assert len(_items)==38, len(_items)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:10])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
