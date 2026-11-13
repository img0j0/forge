# 0.82.1: the back of the book matches the book (Hunter, November 13, iPhone screenshot of "At the back": "could we just
#   improve the look of it to match our aesthetic"). The back was a stack of plain outlined boxes. It is now an index like
#   the contents: rows on dotted rules, each with a little taped-in tile (an envelope, this week's own days, a quill, the
#   season stamp you pressed last, a sun, a ribbon, a stack of pages), a handwritten title and one quiet line.
#   Fixed with it: in lamplight the book's quiet lines (contents and back) took the night's pale ink on the book's paper.
import re,subprocess,os
S=open('base82.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.82.0'","const VERSION='prototype 0.82.1'")
rep("<title>Forgelings (prototype 0.82.0)</title>","<title>Forgelings (prototype 0.82.1)</title>")
m=re.search(r"function bkBack\(\)\{.*?\n.*?</div>`;\}",S); assert m and m.group(0).count('\n')==1
S=S.replace(m.group(0),r"""const BKI={
  week:'',
  quill:'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4c-6 1-11 6-13 13l-2 3"/><path d="M20 4c0 6-4 10-10 11"/><path d="M8 15l3 1"/></svg>',
  sun:'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/></svg>',
  ribbon:'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="4" y="3" width="13" height="18" rx="1"/><path d="M13 3v9l2-1.5 2 1.5V3" fill="#C0562E" stroke="#8A3A2C"/></svg>',
  pages:'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="7" y="3" width="12" height="16" rx="1"/><path d="M5 6v15h11"/><path d="M10 8h6M10 11h6M10 14h4"/></svg>'};
function bkRow(id,ic,t,sub){return `<button class="btrow bkb" id="${id}"><span class="bki" aria-hidden="true">${ic}</span><span><b>${t}</b><span class="muted small">${sub}</span></span></button>`;}
function bkBack(){const nL=(state.letters||[]).length,L=entryDays().size,ym=todayKey().slice(0,7);
  const wk=`<span class="wkd">${lastDays(7).map(k=>{const h=state.history.find(x=>x.date===k);return `<i class="${k<state.startDate?'':h?h.status:''}"></i>`;}).join('')}</span>`;
  const sk=Object.keys(state.seasons||{}).sort((a,b)=>(state.seasons[a]<state.seasons[b]?-1:1)).pop(),ss=sk?SEASONS.find(x=>x.id===sk.split('-')[0]):null,sn=seasonNow();
  const stamp=ss?seasonStampSVG(ss,28,true):seasonStampSVG(sn?sn.s:SEASONS[0],28,false);
  const rows=[nL?bkRow('bookLetters',ENVELOPE,nL===1?'One letter':`${nL} letters`,'Folded and kept for you'):'',
    bkRow('jWeek',wk,'This week','The Scribe reads your week back'),
    monthHTML()?bkRow('jMonth',BKI.quill,'Your month in words',`The Scribe’s account of ${ymName(ym)}`):'',
    bkRow('jSeasons',stamp,'Seasons','The stamps you have pressed'),
    bkRow('jYear',BKI.sun,'Your year','A keepsake of the year so far'),
    L>=30?bkRow('bookRibbon',BKI.ribbon,'Open to an old page','Let the ribbon fall open somewhere'):'',
    L?bkRow('jLines',BKI.pages,'All your pages','Every page, newest first'):''].join('');
  return `<div class="zpage bback"><p class="zk">At the back</p>${rows}<p class="zend">More pages are written every day you show up.</p></div>`;}""",1)
rep(".bkwk{min-height:56px}",""".bkwk{min-height:56px}
.bkb{min-height:60px}
.bkb .bki{width:46px;height:46px;flex:none;display:grid;place-items:center;background:#fff;color:#2E2A47;box-shadow:0 1px 2px rgba(0,0,0,.25);transform:rotate(-2deg)}
.bkb:nth-of-type(even) .bki{transform:rotate(2deg)}
.bkb .bki svg{display:block}
.bkb .bki .wkd{display:grid;grid-template-columns:repeat(4,7px);gap:2px}
.bkb .bki .wkd i{width:7px;height:7px;border:1.2px solid #B9AE96;border-radius:1px}
.bkb .bki .wkd i.done{background:#C0562E;border-color:#8A3A2C}
.bkb .bki .wkd i.rest{border-style:dashed;border-color:#8A3A2C}
.bback .zend{margin-top:14px}
/* the book's paper keeps its own ink at night too (0.82's contents and back rows went pale in lamplight) */
html.jr .app .jbook .zpage:not(.zcover) .muted{color:#5E5470}""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk821.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk821.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
