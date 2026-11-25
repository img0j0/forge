# 0.84: a lighter finished day, a quieter Hearth (Hunter, November 25: "Yes" to the app review).
#  1. Today, finished day: Change the answer, Change the photo, Remove the postcard and Edit your own words fold into one
#     "Edit today's page" sheet when two or more of them would show. "Make your cards yours" stops showing after day 30
#     (Settings > Your cards keeps it).
#  2. Hearth: no counts on the chips (By the fire, Postcard wall), no "bond N of 5", no bond points on Snack/Story/Play.
#  3. Map: when every realm reads the same, one line for the whole map instead of the same line per realm.
#  4. Japanese at 320 px: see JA block below.
#  5. The games sheet's focus outline sits inside the tilted card instead of past it.
#  6. Web save: the main save and the daily safety copy are stored compressed (lz-string UTF-16, "lz1:" prefix) once the
#     save passes 64 KB; the daily copy always. Older plain saves still load; backups and iCloud are unchanged.
import re,subprocess,os
S=open(os.environ.get('BASE','base832.html')).read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.83.2'","const VERSION='prototype 0.84'")
rep("<title>Forgelings (prototype 0.83.2)</title>","<title>Forgelings (prototype 0.84)</title>")

# 1. Today
rep("if(!state.wantAsked&&state.cards.length&&state.status!=='fresh'&&entryDays().size>=2)rows.unshift(row('btnWant'",
    "if(!state.wantAsked&&state.cards.length&&state.status!=='fresh'&&entryDays().size>=2&&dayN()<=30)rows.unshift(row('btnWant'")
rep("if(s==='done'||s==='rest')hero+=`<button class=\"ghost marginlink\" id=\"btnMargin\">${jr?'Edit your own words':s==='done'&&state.todayCard?'Add your own words, and ink today’s Forgeling':'Add your own words to the journal'}</button>`;const reflect='';",
    "if(s==='done'||s==='rest')hero+=`<button class=\"ghost marginlink\" id=\"btnMargin\">${jr?'Edit your own words':s==='done'&&state.todayCard?'Add your own words, and ink today’s Forgeling':'Add your own words to the journal'}</button>`;if(s==='done')hero=epFold(hero,!!jr);const reflect='';")
EP=r'''/* 0.84: a finished day's edits live in one sheet. The buttons stay in the page, hidden, so their handlers are unchanged. */
function epFold(h,jr){
  const ids=['askAgain','pcAdd','pcDel','btnMargin'].filter(id=>(id!=='pcAdd'||h.includes('id="pcDel"'))&&(id!=='btnMargin'||jr)&&h.includes(`id="${id}"`));
  if(ids.length<2)return h;let hid='';
  ids.forEach(id=>{h=h.replace(new RegExp(`<button [^>]*id="${id}"[^>]*>[^<]*</button>`),m=>{hid+=m;return '';});});
  h=h.replace(/<div class="row" style="justify-content:center;flex-wrap:wrap;margin:6px 0 0"><\/div>/,'');
  return h+`<button class="ghost marginlink" id="btnEditPage">Edit today’s page</button><div class="ephid" hidden>${hid}</div>`;}
function openEditPage(){
  const bs=[...document.querySelectorAll('#view-today .ephid button')];if(!bs.length)return;
  openSheet(`<h2>Edit today’s page</h2><div class="stack epl">${bs.map(b=>`<button class="outline" data-ep="${b.id}">${b.textContent}</button>`).join('')}</div><div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);}
modal.addEventListener('click',e=>{const b=e.target.closest('[data-ep]');if(!b)return;const id=b.dataset.ep;closeModal();const t=document.getElementById(id);if(t)t.click();});
'''
rep("function entryDays(){", EP+"function entryDays(){")
rep("  if(b.id==='btnWant'){openWant();return;}","  if(b.id==='btnWant'){openWant();return;}\n  if(b.id==='btnEditPage'){openEditPage();return;}")
rep(".hgrid{margin-top:8px}",".epl{gap:10px;margin:12px 0}.epl .outline{width:100%;min-height:48px}\n.hgrid{margin-top:8px}")

# 2. Hearth counts
rep("${HIC.snack}Snack<small>+1 or +2</small>","${HIC.snack}Snack")
rep("${HIC.story}Story<small>+2</small>","${HIC.story}Story")
rep("${HIC.play}Play<small>${left?'+1 to +3':'Just for fun'}</small>","${HIC.play}Play${left?'':'<small>Just for fun</small>'}")
rep("<span class=\"rs\">${BOND_NAMES[lv-1]}, bond ${lv} of 5${c.statue?' · has a statue':''}</span>","<span class=\"rs\">${BOND_NAMES[lv-1]}${c.statue?' · has a statue':''}</span>")
rep("<span class=\"muted small\">${BOND_NAMES[lv-1]}, bond ${lv} of 5</span>","<span class=\"muted small\">${BOND_NAMES[lv-1]}</span>")
rep("<button class=\"chip\" id=\"hFurn\">By the fire · ${fh} of ${FURN.length}</button>","<button class=\"chip\" id=\"hFurn\">By the fire</button>")
rep("`<button class=\"chip\" id=\"hPost\">Postcard wall · ${Object.keys(state.posts||{}).length+(state.pcGifts||[]).length}</button>`","'<button class=\"chip\" id=\"hPost\">Postcard wall</button>'")
rep("return `<h2>By the fire, ${have} of ${FURN.length}</h2>","return `<h2>By the fire</h2>")
rep("`After ${FURN_V} ${V.name} days. ${t.v[f.v]} so far.`","`After ${FURN_V} ${V.name} days.`")
rep("`After ${f.need===1?'your first calling':f.need+' callings done'}. ${t.all} so far.`","`After ${f.need===1?'your first calling':f.need+' callings done'}.`")

# 3. Map: one line when every realm reads the same
rep("  if(ms.some(m=>m.tier===0))notes+='<p class=\"muted small\">The rest is blank paper, for now.</p>';",
    "  if(ms.length>1&&ms.every(m=>m.tier===3&&placesFound(m.ti)===5&&!dkOf(m)))notes=`<p class=\"small\"><b>Every realm.</b> ${hasLantern()?'Inked and fully charted, front and back.':'Inked and fully charted. You could draw it all from memory.'}</p>`;\n  if(ms.some(m=>m.tier===0))notes+='<p class=\"muted small\">The rest is blank paper, for now.</p>';")

# 4. the date line breaks after the greeting, never inside "Day N, date" (Japanese at 320 px split 111 from 日め)
rep("$('#dateLabel').textContent=(tab==='today'?greeting()+' \\u00B7 ':'')+`Day ${dayN()}, ${dateLabel(todayKey())}`;",
    "$('#dateLabel').innerHTML=(tab==='today'?'<span class=\"nw\">'+esc(greeting())+' \\u00B7</span> ':'')+`<span class=\"nw\">Day ${dayN()}, ${dateLabel(todayKey())}</span>`;")
rep(".hgrid{margin-top:8px}",".nw{white-space:nowrap}\n.hgrid{margin-top:8px}")

# 5. games sheet focus outline
rep("#modal .pcard b,#modal .pcard span{color:#2E2A47}","#modal .pcard b,#modal .pcard span{color:#2E2A47}\n#modal .pcard:focus-visible{outline-offset:-4px;border-radius:4px}")

# 6. compressed web save. The daily copy is written once a day, so it is always packed. The main save is written on
#    every change, so it stays plain (fast) until it is big enough for space to matter.
LZ=open('vendor/lz-string-1.5.0.min.js').read()
rep("function nset(k,v){",
    "/* lz-string 1.5.0, MIT License, (c) 2013 pieroxy. vendor/lz-string-LICENSE.txt */\nconst LZS=(()=>{"+LZ.replace('var LZString=','return ',1)+"})();\n"
    "const LZ_MAIN=1536*1024;\nfunction lsPack(j){try{return 'lz1:'+LZS.compressToUTF16(j);}catch(e){return j;}}\n"
    "function lsUnpack(v){if(typeof v!=='string'||!v.startsWith('lz1:'))return v;try{return LZS.decompressFromUTF16(v.slice(4))||null;}catch(e){return null;}}\n"
    "function nset(k,v){")
rep("let nv=null,lv=null;try{nv=(await PL.Preferences.get({key:k})).value||null;}catch(e){}try{lv=localStorage.getItem(k);}catch(e){}",
    "let nv=null,lv=null;try{nv=(await PL.Preferences.get({key:k})).value||null;}catch(e){}try{lv=lsUnpack(localStorage.getItem(k));}catch(e){}")
rep("let lt=null;try{lt=localStorage.getItem(KEY);}catch(e){}","let lt=null;try{lt=lsUnpack(localStorage.getItem(KEY));}catch(e){}")
rep("let t=null;try{t=localStorage.getItem(KEY);}catch(e){}if(!t)return;","let t=null;try{t=lsUnpack(localStorage.getItem(KEY));}catch(e){}if(!t)return;")
rep("let raw=null;try{raw=localStorage.getItem(KEY);}catch(e){return null;}","let raw=null;try{raw=localStorage.getItem(KEY);}catch(e){return null;}\n  if(raw&&raw.startsWith('lz1:'))raw=lsUnpack(raw)||raw;")
rep("let dr=null,d=null;try{dr=localStorage.getItem(KEY+'-daily');}catch(e){}","let dr=null,d=null;try{dr=lsUnpack(localStorage.getItem(KEY+'-daily'));}catch(e){}")
rep("    const j=JSON.stringify(s);saveProblem('encode',false);let ok=true;\n    try{localStorage.setItem(KEY,j);saveProblem('web',false);}\n    catch(e){try{localStorage.removeItem(KEY+'-daily');dailyAt=null;localStorage.setItem(KEY,j);saveProblem('web',false);}catch(e2){ok=false;saveProblem('web',true);}}\n    if(ok&&dailyAt!==s.date){try{localStorage.setItem(KEY+'-daily',j);dailyAt=s.date;}catch(e){}}",
    "    const j=JSON.stringify(s);saveProblem('encode',false);let ok=true;const m=j.length>LZ_MAIN?lsPack(j):j;\n    try{localStorage.setItem(KEY,m);saveProblem('web',false);}\n    catch(e){try{localStorage.removeItem(KEY+'-daily');dailyAt=null;localStorage.setItem(KEY,m===j?lsPack(j):m);saveProblem('web',false);}catch(e2){ok=false;saveProblem('web',true);}}\n    if(ok&&dailyAt!==s.date){try{localStorage.setItem(KEY+'-daily',lsPack(j));dailyAt=s.date;}catch(e){}}")

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk84.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk84.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
