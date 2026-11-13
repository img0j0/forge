# 0.82: the Book tab is the book (Hunter, November 13: asked how the book felt and whether to change anything; the review
#   suggested three changes; "Let's do it").
#   - The tab shows the book itself, open at the ribbon (or the latest page), with page turns in place: no summary page,
#     no sheet. Anything that opened the book (On this day, the echo, "Your {month} is bound", "Read that page") now opens
#     the Book tab at that page (`openBook` sets `ui.bookTo` and switches tab).
#   - What sat beside the book moves into it: the cover keeps the binding line (10/30/60/100) and the Scribe; the contents
#     add the last five weeks, one row per week that opens its first page; the back has letters, this week, your month in
#     words, seasons, your year, an old page and all your pages.
#   - Getting around: no "Page 22 of 108"; Contents and Latest page sit under Back and Next. "Second reading" shows only on
#     the day an echo opened (`ui.bkEcho`), not on every spread.
import re,subprocess,os
S=open('base811.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.81.1'","const VERSION='prototype 0.82.0'")
rep("<title>Forgelings (prototype 0.81.1)</title>","<title>Forgelings (prototype 0.82.0)</title>")
# --- the tab is the book ---
m=re.search(r"\n  if\(tab==='book'\)\{el\.innerHTML=journeyHTML\(\)[^\n]*",S); assert m
S=S.replace(m.group(0),"""
  if(tab==='book'){let i=ui.bookTo!=null?ui.bookTo:bookIdx(state.bookAt);ui.bookTo=null;if(i<0)i=bkLatestIdx();if(i<0)i=0;el.innerHTML=`<div class="bkhost">${bookHTMLAt(i)}</div>`;hydrate(el);return;}""",1)
rep("""function openBook(key){let i=key?bookIdx(key):-1;if(i<0)i=1;openSheet(bookHTMLAt(i));save();}""",
"""function openBook(key){let i=key?bookIdx(key):-1;if(i<0)i=bkLatestIdx();if(i<0)i=1;ui.bookTo=i;if(!modal.hidden)closeModal();tab='book';render();window.scrollTo(0,0);save();}
function bkLatestIdx(){const P=bookPages();for(let j=P.length-1;j>=0;j--)if(P[j].k==='d')return j;return -1;}""")
rep("""function bookGo(d,focusId,to){const b=ui.book;if(!b)return;const sh=modal.querySelector('.sheet');if(!sh)return;const ni=to!=null?to:b.i+d;
  sh.innerHTML=bookHTMLAt(ni);nameDialog();sfx('select');save();""","""function bookGo(d,focusId,to){const b=ui.book;if(!b)return;const host=tab==='book'?document.querySelector('#view-chronicle .bkhost'):null,sh=host||modal.querySelector('.sheet');if(!sh)return;const ni=to!=null?to:b.i+d;
  sh.innerHTML=bookHTMLAt(ni);if(!host)nameDialog();sfx('select');save();
  if(host){hydrate(host);const r=host.getBoundingClientRect();if(r.top<0)host.scrollIntoView({block:'start',behavior:REDUCE?'auto':'smooth'});}""")
rep("""function bookHTMLAt(i){const P=bookPages();i=Math.max(0,Math.min(P.length-1,i));ui.book={i};state.bookAt=bkKey(P[i]);
  return `<div class="csheet zine jbook" data-k="jbook"><h2 class="vh">Your book</h2><div class="zbox" aria-live="polite">${bookPageHTML(P[i])}</div><p class="muted small center" style="margin:6px 0">Page ${i+1} of ${P.length}</p><div class="row znav"><button class="outline" id="bkPrev" ${i?'':'disabled'}>Back a page</button><button class="primary" id="bkNext" ${i<P.length-1?'':'disabled'}>Next page</button></div><div class="stack"><button class="ghost" id="bkToc">Contents</button><button class="ghost" data-close>Close the book</button></div></div>`;}""",
"""function bookHTMLAt(i){const P=bookPages();i=Math.max(0,Math.min(P.length-1,i));ui.book={i};state.bookAt=bkKey(P[i]);const lt=bkLatestIdx();
  return `<div class="zine jbook binline" data-k="jbook"><h2 class="vh">Your book</h2><div class="zbox" aria-live="polite">${bookPageHTML(P[i])}</div><div class="row znav"><button class="outline" id="bkPrev" ${i?'':'disabled'}>Back a page</button><button class="primary" id="bkNext" ${i<P.length-1?'':'disabled'}>Next page</button></div><div class="row bkjump"><button class="ghost" id="bkToc" ${i===1?'disabled':''}>Contents</button>${lt>=0?`<button class="ghost" id="bkLatest" ${i===lt?'disabled':''}>Latest page</button>`:''}</div></div>`;}""")
rep("""  if(e.target.closest('#bkToc')){bookGo(0,null,1);return;}""","""  if(e.target.closest('#bkToc')){bookGo(0,null,1);return;}
  if(e.target.closest('#bkLatest')){const j=bkLatestIdx();if(j>=0)bookGo(0,'bkNext',j);return;}""")
# --- the cover keeps the binding line and the Scribe ---
rep("""<p class="muted small">Started ${esc(dateLabel(state.startDate))}</p></div>`;}""","""<p class="muted small">Started ${esc(dateLabel(state.startDate))}</p>${bkNextLine(L)}</div>`;}
function bkNextLine(L){const nx=BOOK_AT.find(x=>L<x),nxt={1:'Your first page gives it a cover.',10:'At 10 pages, it is bound in leather.',30:'At 30, it gets a ribbon that opens to an old page.',60:'At 60, someone will come to the fire to read with you.',100:'At 100, gold edges and a clasp.'}[nx]||'Every page from here is just for you.';
  return `<p class="small bcovnx">${L>=SCRIBE_AT?'The Scribe sits by your fire and reads with you. ':''}${nxt}</p>`;}""")
# --- contents: the last five weeks, a row a week ---
rep("""<span class="muted small">${ym===cur?`${ymName(ym)}, still being written`:`${ymName(ym)} ${ym.slice(0,4)} \\u00B7 ${n===1?'one page':`${n} pages`}`}</span></span></button>`;}).join('')}</div>`;}""",
"""<span class="muted small">${ym===cur?`${ymName(ym)}, still being written`:`${ymName(ym)} ${ym.slice(0,4)} \\u00B7 ${n===1?'one page':`${n} pages`}`}</span></span></button>`;}).join('')}${bkWeeks()}</div>`;}
function bkWeeks(){const D=lastDays(35),E=entryDays(),fm=k=>new Date(k+'T00:00:00').toLocaleDateString(LOC(),{month:'short',day:'numeric'}),W=[];
  for(let w=0;w<5;w++)W.push(D.slice(w*7,w*7+7));
  const rows=W.reverse().map(ds=>{const pg=ds.filter(k=>E.has(k));if(!pg.length)return '';
    const dots=ds.map(k=>{const h=state.history.find(x=>x.date===k);return `<i class="${k<state.startDate?'':h?h.status:''}"></i>`;}).join('');
    return `<button class="btrow bkwk" data-bkgo="d:${pg[0]}"><span class="wkd" aria-hidden="true">${dots}</span><span><b>${fm(ds[0])} \\u2013 ${fm(ds[6])}</b><span class="muted small">${pg.length===1?'one page':`${pg.length} pages`}</span></span></button>`;}).join('');
  return rows?`<p class="zk" style="margin-top:16px">The last five weeks</p>${rows}`:'';}""")
# --- the back: everything that sat beside the book ---
rep("""<button class="outline" id="jYear">Your year</button>${L>=30?'<button class="outline" id="bookRibbon">Open to an old page</button>':''}<p class="zend">More pages are written every day you show up.</p></div>`;}""",
"""<button class="outline" id="jWeek">This week</button>${monthHTML()?'<button class="outline" id="jMonth">Your month in words</button>':''}<button class="outline" id="jSeasons">Seasons</button><button class="outline" id="jYear">Your year</button>${L>=30?'<button class="outline" id="bookRibbon">Open to an old page</button>':''}${L?'<button class="outline" id="jLines">All your pages</button>':''}<p class="zend">More pages are written every day you show up.</p></div>`;}""")
# --- second reading only on the echo's day ---
rep("""const bkKept=c=>c&&keptAge(c)>=KEPT_DAYS?""","""const bkKept=c=>c&&ui.bkEcho===c.id&&keptAge(c)>=KEPT_DAYS?""")
rep("""if(o)openBook('d:'+o.k);else if(e){const k='d:'+e.c.date;if(bookIdx(k)>=0)openBook(k);else keptOpen(e.c.id);}}""","""if(o)openBook('d:'+o.k);else if(e){const k='d:'+e.c.date;ui.bkEcho=e.c.id;if(bookIdx(k)>=0)openBook(k);else keptOpen(e.c.id);}}""")
# --- styles ---
rep(".bday .bkept{",""".binline .zbox{min-height:0}
.binline{margin-top:4px}
.bkjump{justify-content:center;gap:18px;margin-top:4px}
.bcovnx{margin-top:10px;opacity:.9}
.bkwk{min-height:56px}
.bkwk .wkd{display:grid;grid-template-columns:repeat(7,9px);gap:3px;flex:none}
.bkwk .wkd i{width:9px;height:9px;border:1.5px solid #B9AE96;border-radius:2px}
.bkwk .wkd i.done{background:#C0562E;border-color:#8A3A2C}
.bkwk .wkd i.rest{border-style:dashed;border-color:#8A3A2C}
.bday .bkept{""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk82.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk82.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
