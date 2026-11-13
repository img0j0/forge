# 0.79: one place to look back (look-back and progress design doc, decision 1; Hunter, November 13: "Let's go with the
#   recommendations").
#   - Today shows at most one look-back line a day, in this order: Close the day (evening), an unread letter, Your year,
#     "Your {month} is bound", On this day. The others wait for another day or live in the book.
#   - The echo ("Read that day again") is folded into On this day: when no page from a month or year ago exists, the row
#     names the Forgeling found then. On this day now opens the book at that day's spread (the echo falls back to the
#     second reading if that day has no page).
#   - A day's spread in the book offers the Forgeling's second reading once it is open, so the echo's reason to look
#     stays one tap away.
#   - The Hearth's memory echo can open the book at the page it found ("Read that page").
#   - The This week box leaves Today (the book's last five weeks show it); Latest finds stays.
import re,subprocess,os
S=open('base78.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.78.0'","const VERSION='prototype 0.79.0'")
rep("<title>Forgelings (prototype 0.78.0)</title>","<title>Forgelings (prototype 0.79.0)</title>")
# --- the echo leaves the hero ---
rep("""<div style="width:100%;text-align:left">${echoHTML()}</div>""","",3)
# --- On this day: an old page, else the echo ---
rep("""{const o=otdKey();if(o&&state.otd!==todayKey())rows.unshift(row('btnOtd',IC.pack,'On this day',o.y?'A year ago today, you wrote a page. Have a look.':'A month ago today, you wrote a page. Have a look.','',true));}""",
"""{const o=otdKey();if(o&&state.otd!==todayKey())rows.unshift(row('btnOtd',IC.pack,'On this day',o.y?'A year ago today, you wrote a page. Have a look.':'A month ago today, you wrote a page. Have a look.','',true));
    else if(!o&&state.otd!==todayKey()&&state.cards.length){const e=echoToday();if(e){const en=esc(e.c.nick||e.c.name),eV=esc((VECTORS[e.c.v]||VECTORS[0]).name);rows.unshift(row('btnOtd',IC.pack,e.lab,`You found ${en} on a ${eV} day. Read that day again.`,'',true));}}}""")
rep("""else if(b.id==='btnOtd'){const o=otdKey();if(o){state.otd=todayKey();save();renderToday();openOldPage(o.k,o.y?'A year ago today':'A month ago today');}}""",
"""else if(b.id==='btnOtd'){const o=otdKey(),e=o?null:echoToday();state.otd=todayKey();save();renderToday();
    if(o)openBook('d:'+o.k);else if(e){const k='d:'+e.c.date;if(bookIdx(k)>=0)openBook(k);else keptOpen(e.c.id);}}""")
# --- one look-back line a day ---
rep("""  const latest=state.cards.slice(-5).reverse(),done=state.history.filter(h=>h.status==='done').length;""",
"""  {const LB=['btnClose','btnLetter','btnYear','btnZine','btnOtd'],has=id=>rows.some(r=>r.includes(`id="${id}"`)),keep=LB.find(has);
    if(keep)for(let i=rows.length-1;i>=0;i--)if(LB.some(id=>id!==keep&&rows[i].includes(`id="${id}"`)))rows.splice(i,1);}
  const latest=state.cards.slice(-5).reverse();""")
# --- This week leaves Today; Latest finds stays ---
rep("""    <div class="panel-box weekbox"><div class="weekhead"><h2 class="sub3">This week</h2><span class="muted small">${done} ${done===1?'day':'days'} showed up</span></div><div class="dots" role="group" aria-label="This week">${weekDots()}</div>
    ${latest.length?`<h2 class="sub3">Latest finds</h2><div class="latest shelf">${latest.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}">${cardHTML(c,{w:58,mini:true})}</button>`).join('')}</div>`:''}</div>`;""",
"""    ${latest.length?`<div class="panel-box weekbox"><h2 class="sub3">Latest finds</h2><div class="latest shelf">${latest.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.name)}">${cardHTML(c,{w:58,mini:true})}</button>`).join('')}</div></div>`:''}`;""")
# --- second reading on a day's spread ---
rep("""${bkTucked(k)}</div><div class="br">""","""${bkTucked(k)+bkKept(c)}</div><div class="br">""")
rep("""function bkDay(k){""","""const bkKept=c=>c&&keptAge(c)>=KEPT_DAYS?`<button class="ghost bkept" data-kept="${c.id}">Second reading</button>`:'';
function bkDay(k){""")
# --- the memory echo opens its page ---
rep("""<p class="small" style="margin:6px 0 0">${esc(e.line||'')}</p></div>`;""","""<p class="small" style="margin:6px 0 0">${esc(e.line||'')}</p><button class="ghost" data-oldpage="${e.k}">Read that page</button></div>`;""")
rep("""<button class="chip" data-mecho="let">Let it go</button></div></div>`;""","""<button class="chip" data-mecho="let">Let it go</button></div><button class="ghost" data-oldpage="${e.k}">Read that page</button></div>`;""")
rep("""document.addEventListener('click',e=>{
  const k=e.target.closest&&e.target.closest('[data-kept]');""","""document.addEventListener('click',e=>{
  const op=e.target.closest&&e.target.closest('[data-oldpage]');if(op){const k='d:'+op.dataset.oldpage;if(bookIdx(k)>=0)openBook(k);return;}
  const k=e.target.closest&&e.target.closest('[data-kept]');""")
rep(".zcover h3{",".bday .bkept{display:block;margin:2px auto 6px;min-height:44px}\n.zcover h3{")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk79.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk79.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
