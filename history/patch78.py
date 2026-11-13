# 0.78: one voice, and a tab for the book (Hunter, November 13: asked whether everything ties together; the review found
#   the book hidden under Map and two voices asking questions; "Absolutely" to fixing both and a design doc for the rest).
#   - One voice: your words' sheet (Add your own words, Say more) now shows the question your companion asked today, with
#     your answer once you have given it, in place of "The Forge asks" (that question stays on the card face, as the
#     card's prompt). `sayMoreLead` works with or without an answer; `openMargin` swaps it in after rendering.
#   - The book's own tab: a sixth tab, Book, opens the journal (book, chapters, letters, calendar, pages). The Map tab keeps
#     Map and Tales. Both share #view-chronicle (`tab==='book'` shows it with the journal), so nothing else moves.
#     The printable book (formerly planned as 0.78) waits for TestFlight, as decided.
import re,subprocess,os
S=open('base77.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.77.0'","const VERSION='prototype 0.78.0'")
rep("<title>Forgelings (prototype 0.77.0)</title>","<title>Forgelings (prototype 0.78.0)</title>")
# --- one voice ---
rep("""function sayMoreLead(){const k=state.date,Q=askFor(k),a=askAns(k);return a?`<p class="saylead"><i>${esc(Q.q)}</i> You answered: ${esc(a[0])}.</p>`:'';}""",
"""function sayMoreLead(){const k=state.date,Q=askFor(k),a=askAns(k),c=companion()||mateNow(),n=c?esc(c.nick||c.name):'';
  if(a)return n?`<p class="saylead">${n} asked: <i>${esc(Q.q)}</i> You answered: ${esc(a[0])}.</p>`:`<p class="saylead"><i>${esc(Q.q)}</i> You answered: ${esc(a[0])}.</p>`;
  return n?`<p class="saylead">${n} would like to know: <i>${esc(Q.q)}</i></p>`:`<p class="saylead"><i>${esc(Q.q)}</i></p>`;}""")
rep("""function openSayMore(){openMargin();const f=modal.querySelector('.sheet label.field');if(f)f.insertAdjacentHTML('beforebegin',sayMoreLead());}""","""function openSayMore(){openMargin();}""")
rep("""  setTimeout(()=>{const i=$('#jIn');if(i)i.focus({preventScroll:true});},60);
}
function saveJournal(text){""","""  {const q=modal.querySelector('.sheet p.muted > i');if(q&&q.parentElement)q.parentElement.outerHTML=sayMoreLead();}
  setTimeout(()=>{const i=$('#jIn');if(i)i.focus({preventScroll:true});},60);
}
function saveJournal(text){""")
# --- the Book tab ---
rep("""  <button class="tab" data-tab="chronicle"><svg class="pi" viewBox="0 0 12 12" aria-hidden="true"><path fill="currentColor" d="M1 2h3v9h-3zM5 1h2v9h-2zM8 2h3v9h-3z"/></svg>Map</button>""",
"""  <button class="tab" data-tab="chronicle"><svg class="pi" viewBox="0 0 12 12" aria-hidden="true"><path fill="currentColor" d="M1 2h3v9h-3zM5 1h2v9h-2zM8 2h3v9h-3z"/></svg>Map</button>
  <button class="tab" data-tab="book"><svg class="pi" viewBox="0 0 12 12" aria-hidden="true"><path fill="currentColor" d="M2 1h8v1h-8zM2 2h1v9h-1zM9 2h1v9h-1zM3 10h6v1h-6zM4 3h4v1h-4zM4 5h4v1h-4zM4 7h2v1h-2z"/></svg>Book</button>""")
rep("""  ['today','hearth','binder','chronicle','settings'].forEach(n=>{$('#view-'+n).hidden=tab!==n;});
  $('#title').textContent=tab==='today'?'Today':tab==='hearth'?'The Hearth':tab==='binder'?'Your binder':tab==='chronicle'?'The Map':'Settings';""",
"""  ['today','hearth','binder','chronicle','settings'].forEach(n=>{$('#view-'+n).hidden=tab!==n&&!(n==='chronicle'&&tab==='book');});
  $('#view-chronicle').setAttribute('aria-label',tab==='book'?'Your book':'Map');
  $('#title').textContent=tab==='today'?'Today':tab==='hearth'?'The Hearth':tab==='binder'?'Your binder':tab==='chronicle'?'The Map':tab==='book'?'Your book':'Settings';""")
rep("""  const el=$('#view-chronicle'),subs=[['map','Map'],['tales','Tales'],['journal','Journal']];
  if(!subs.some(x=>x[0]===ch.sub))ch.sub='map';
  const body=ch.sub==='tales'?talesHTML():ch.sub==='journal'?journeyHTML()+journalHTML():(ch.side&&hasLantern()?mapBackHTML():mapHTML());""",
"""  const el=$('#view-chronicle'),subs=[['map','Map'],['tales','Tales']];
  if(!subs.some(x=>x[0]===ch.sub))ch.sub='map';
  if(tab==='book'){el.innerHTML=journeyHTML()+journalHTML()+'<p class="muted small" style="margin-top:14px">A book in two inks. <span class="inkw">The Forge writes the world.</span> <span class="inkm">You write your Forgelings.</span></p>';hydrate(el);tipFade('twoinks',el.querySelector(':scope > p.muted.small:last-child'));return;}
  const body=ch.sub==='tales'?talesHTML():(ch.side&&hasLantern()?mapBackHTML():mapHTML());""")
rep("if(tab==='chronicle')renderChronicle();if(tab==='hearth')renderHearth();renderNav();window.scrollTo(0,0);lsEnter($('#view-'+tab));","if(tab==='chronicle'||tab==='book')renderChronicle();if(tab==='hearth')renderHearth();renderNav();window.scrollTo(0,0);lsEnter($('#view-'+(tab==='book'?'chronicle':tab)));")
rep("""html.jr .tab[data-tab="chronicle"]{background:#2F6B45}""","""html.jr .tab[data-tab="chronicle"]{background:#2F6B45}
html.jr .tab[data-tab="book"]{background:#8A3A2C}""")
rep("""html.jr[data-page="lamp"] .tab[data-tab="chronicle"]{background:#275A3A}""","""html.jr[data-page="lamp"] .tab[data-tab="chronicle"]{background:#275A3A}
html.jr[data-page="lamp"] .tab[data-tab="book"]{background:#743024}""")
rep("""html.jr .tab[data-tab="chronicle"]:not([aria-current="page"]){background:#36432F !important}""","""html.jr .tab[data-tab="chronicle"]:not([aria-current="page"]){background:#36432F !important}
html.jr .tab[data-tab="book"]:not([aria-current="page"]){background:#523029 !important}""")
rep("""html.jr .tab[data-tab="book"]:not([aria-current="page"]){background:#523029 !important}""","""html.jr .tab[data-tab="book"]:not([aria-current="page"]){background:#523029 !important}
/* 0.78: six tabs on a narrow phone keep 44 pt and their labels */
@media (max-width:380px){html.jr .tabs-in{padding:0 6px;gap:4px}.tabs .tab{font-size:11px;letter-spacing:-.01em}}""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk78.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk78.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
