# 0.82.2: a way out of the book (Hunter, November 13, iPhone screenshot of the cover: "There is no way to get out of
#   this"). Since 0.82 the tab is the book and nothing in it closed: the cover kept a Back button that did nothing.
#   - The cover is the closed book: "Open the book" (to the ribbon, else the latest page) and Contents; no Back/Next.
#   - Every page inside has "Close the book": back to the tab you came from when something opened the book (On this
#     day, the echo, "Your {month} is bound", "Read that page"), otherwise to the cover.
#   - The ribbon only marks pages you read: resting on the cover or the contents no longer moves it.
import re,subprocess,os
S=open('base821.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.82.1'","const VERSION='prototype 0.82.2'")
rep("<title>Forgelings (prototype 0.82.1)</title>","<title>Forgelings (prototype 0.82.2)</title>")
rep("""function bookHTMLAt(i){const P=bookPages();i=Math.max(0,Math.min(P.length-1,i));ui.book={i};state.bookAt=bkKey(P[i]);const lt=bkLatestIdx();
  return `<div class="zine jbook binline" data-k="jbook"><h2 class="vh">Your book</h2><div class="zbox" aria-live="polite">${bookPageHTML(P[i])}</div><div class="row znav"><button class="outline" id="bkPrev" ${i?'':'disabled'}>Back a page</button><button class="primary" id="bkNext" ${i<P.length-1?'':'disabled'}>Next page</button></div><div class="row bkjump"><button class="ghost" id="bkToc" ${i===1?'disabled':''}>Contents</button>${lt>=0?`<button class="ghost" id="bkLatest" ${i===lt?'disabled':''}>Latest page</button>`:''}</div></div>`;}""",
"""function bookHTMLAt(i){const P=bookPages();i=Math.max(0,Math.min(P.length-1,i));ui.book={i};const k=bkKey(P[i]);if(k!=='c'&&k!=='t')state.bookAt=k;const lt=bkLatestIdx();
  if(k==='c')return `<div class="zine jbook binline" data-k="jbook"><h2 class="vh">Your book</h2><div class="zbox" aria-live="polite">${bookPageHTML(P[i])}</div><div class="stack bkshut"><button class="primary" id="bkOpenB">Open the book</button><button class="ghost" id="bkToc">Contents</button></div></div>`;
  return `<div class="zine jbook binline" data-k="jbook"><h2 class="vh">Your book</h2><div class="zbox" aria-live="polite">${bookPageHTML(P[i])}</div><div class="row znav"><button class="outline" id="bkPrev">Back a page</button><button class="primary" id="bkNext" ${i<P.length-1?'':'disabled'}>Next page</button></div><div class="row bkjump"><button class="ghost" id="bkToc" ${i===1?'disabled':''}>Contents</button>${lt>=0?`<button class="ghost" id="bkLatest" ${i===lt?'disabled':''}>Latest page</button>`:''}<button class="ghost" id="bkClose">Close the book</button></div></div>`;}""")
rep("""function openBook(key){let i=key?bookIdx(key):-1;if(i<0)i=bkLatestIdx();if(i<0)i=1;ui.bookTo=i;if(!modal.hidden)closeModal();tab='book';render();window.scrollTo(0,0);save();}""",
"""function openBook(key){let i=key?bookIdx(key):-1;if(i<0)i=bkLatestIdx();if(i<0)i=1;ui.bookTo=i;ui.bookFrom=tab!=='book'?tab:null;if(!modal.hidden)closeModal();tab='book';render();window.scrollTo(0,0);save();}""")
rep("""  if(tab==='book'){let i=ui.bookTo!=null?ui.bookTo:bookIdx(state.bookAt);ui.bookTo=null;""","""  if(tab==='book'){if(ui.bookTo==null)ui.bookFrom=null;let i=ui.bookTo!=null?ui.bookTo:bookIdx(state.bookAt);ui.bookTo=null;""")
rep("""  if(e.target.closest('#bkLatest')){const j=bkLatestIdx();if(j>=0)bookGo(0,'bkNext',j);return;}""","""  if(e.target.closest('#bkLatest')){const j=bkLatestIdx();if(j>=0)bookGo(0,'bkNext',j);return;}
  if(e.target.closest('#bkOpenB')){let j=bookIdx(state.bookAt);if(j<2)j=bkLatestIdx();if(j<0)j=1;bookGo(0,'bkNext',j);return;}
  if(e.target.closest('#bkClose')){const f=ui.bookFrom;ui.bookFrom=null;if(f&&f!=='book'){tab=f;render();window.scrollTo(0,0);sfx('select');}else bookGo(0,'bkOpenB',0);return;}""")
rep(".bkjump{justify-content:center;gap:18px;margin-top:4px}",".bkjump{justify-content:center;flex-wrap:wrap;gap:4px 18px;margin-top:4px}\n.bkshut{margin-top:12px}")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk822.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk822.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
