# Forgelings 0.38.0: The Scribe (design doc https://claude.ai/artifact/Kt3TnuTRS44Ax69aMDsmy4, part 3 and part 4).
#  - The Scribe: once you have written 60 lines in total (never in a row), an owl-like Forgeling with an ink-dipped
#    quill tail comes to your fire for good. Its colours come from your own save, so every player's Scribe is a
#    little different. It never plays or wanders. Once a day, when you open the Hearth, it opens your book and reads
#    one of your older lines back to you.
#  - Hearth lines about your own things: on a day you do one of your own small things, the Forgeling who notices your
#    day says so ("You did “Text Mom” again. Pip noticed.").
#  - Ribbon: The Scribe (write 60 lines).
# Reads base37.html.
src = open('base37.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

SCRIBE_JS = r"""
/* ---- 0.38: the Scribe, for people who write ---- */
const SCRIBE_AT=60;
const scribeHere=()=>linesWritten()>=SCRIBE_AT;
const SCRIBE_SPR=['.k.....k.','.kb...bk.','kbbbbbbbk','kbwwbwwbk','kbwpbwpbk','kbbbybbbk','kblllllbk','kblklklbk','kbllllllk','.kbbbbbk.','..k.k.kqq','.......Qq'];
function scribePal(){const h=whash((String(state.sid||'')+state.startDate).split('').reduce((a,ch)=>a*31+ch.charCodeAt(0)|0,7)),B=['#8B6A4E','#6E6A8E','#8E7A5E','#5E7A8E','#7E5E8E','#6E8A5E'][Math.abs(h)%6],L=['#E9D9B8','#D9D2EC','#E6DCC4','#CFE0E6','#E2D2E6','#D8E6CC'][Math.abs(h>>3)%6];
  return {k:hexRGB('#2E2A47'),b:hexRGB(B),l:hexRGB(L),w:hexRGB('#F4ECD8'),p:hexRGB('#2E2A47'),y:hexRGB('#FFD36B'),q:hexRGB('#5A3FC0'),Q:hexRGB('#B9A6FF')};}
const SCRIBE_L=['{d} days ago you wrote: “{t}” And here you are.','It finds a page from {d} days ago: “{t}” It reads it twice, slowly.','{d} days ago, in your hand: “{t}” The Scribe nods, as if it remembers too.'];
function scribeRead(){
  const k=todayKey();if(!scribeHere()||state.scribeDay===k)return '';
  const ks=Object.keys(state.journal).filter(j=>state.journal[j].text&&dayDiff(j,k)>=7).sort();if(!ks.length)return '';
  const pool=ks.filter(j=>dayDiff(j,k)>=14),pick=(pool.length?pool:ks)[whash(dnum(k)*13)%((pool.length?pool:ks).length)],t=state.journal[pick].text,d=dayDiff(pick,k);
  state.scribeDay=k;save();
  return 'The Scribe opens your book. '+SCRIBE_L[whash(dnum(k))%SCRIBE_L.length].replace('{d}',d).replace('{t}',t.length>90?t.slice(0,88)+'…':t);
}
const OWN_L=['You did “{o}” again. {n} noticed.','{n} remembers the last time you did “{o}”. Here you are again.','{n} heard you did “{o}” today, and looks quietly pleased.'];
"""
rep("function compNotice(){", SCRIBE_JS + "function compNotice(){")
rep("  const line=L[whash(dnum(state.date)*31+c.id)%L.length].replace(/\\{n\\}/g,n),after=bondLevel(c);",
    "  const ow=todayOwnObj(),line=(ow?(ow.days.length<=1?'{n} saw you do \\u201C{o}\\u201D today, and thinks that is nice.':OWN_L[whash(dnum(state.date)*7+c.id)%OWN_L.length]).replace(/\\{o\\}/g,ow.text):L[whash(dnum(state.date)*31+c.id)%L.length]).replace(/\\{n\\}/g,n),after=bondLevel(c);")
# it reads to you when you open the Hearth (once a day, when nothing else is being said)
rep("  if(tab==='hearth'&&state.comp&&state.comp.date===state.date&&!state.comp.seen){",
    "  if(tab==='hearth'&&!hf.msg){const sr=scribeRead();if(sr)hf.msg=sr;}\n  if(tab==='hearth'&&state.comp&&state.comp.date===state.date&&!state.comp.seen){")
# drawn by the fire, inside the firelight, on its own post at the right
rep("  {const fc=heapOn?null:fireCurio(),px=fc&&cpix(fc);if(px)px.forEach(([x,y,c])=>setpx(39+x,55+y,c));}",
    "  {const fc=heapOn?null:fireCurio(),px=fc&&cpix(fc);if(px)px.forEach(([x,y,c])=>setpx(39+x,55+y,c));}\n  if(!heapOn&&scribeHere()){const P=scribePal(),X=99,Y=60,bob=REDUCE?0:Math.floor(t/1400)%2;for(let x=X;x<X+9;x++)setpx(x,Y+12,[40,30,26]);SCRIBE_SPR.forEach((row,j)=>{for(let i=0;i<row.length;i++){const ch=row[i];if(ch!=='.'&&P[ch])setpx(X+i-1,Y+j-bob,ch==='w'&&!REDUCE&&(t%5200)<160?P.b:P[ch]);}});}")
# the arrival
rep("  if(!t)delete state.journal[state.date];else state.journal[state.date]={v:state.todayV,text:t};",
    "  const wasL=linesWritten();\n  if(!t)delete state.journal[state.date];else state.journal[state.date]={v:state.todayV,text:t};\n  ui.scribeArr=wasL<SCRIBE_AT&&linesWritten()>=SCRIBE_AT;if(ui.scribeArr)hf.msg='Someone new has come to the fire. It carries a quill, and it would like to read with you.';")
rep("closeModal();renderToday();renderChronicle();checkRibbons();toast('Saved to your Journal. It stays on this device.');}",
    "closeModal();renderToday();renderChronicle();checkRibbons();toast(ui.scribeArr?'Sixty lines. The Scribe has come to your Hearth.':'Saved to your Journal. It stays on this device.');ui.scribeArr=false;}")
rep("<p class=\"muted small\">${nxt}</p>", "<p class=\"muted small\">${L>=SCRIBE_AT?'The Scribe sits by your fire and reads with you. ':''}${nxt}</p>")
rep("  {id:'forge1',name:'First Forging',", "  {id:'scribe',name:'The Scribe',desc:'Write 60 lines in your book, whenever you like.',g:60,f:()=>linesWritten()},\n  {id:'forge1',name:'First Forging',")
rep("\\nInk-touched Forgelings: ${state.cards.filter(c=>c.ink).length}", "\\nInk-touched Forgelings: ${state.cards.filter(c=>c.ink).length}\\nScribe: ${scribeHere()?'by the fire':'not yet'}")
rep("  if(s.homeFav!==undefined&&s.homeFav!==null&&!Number.isInteger(s.homeFav))delete s.homeFav;",
    "  if(s.homeFav!==undefined&&s.homeFav!==null&&!Number.isInteger(s.homeFav))delete s.homeFav;\n  if(s.scribeDay!==undefined&&typeof s.scribeDay!=='string')delete s.scribeDay;")

rep('<title>Forgelings (prototype 0.37.0)</title>', '<title>Forgelings (prototype 0.38.0)</title>')
rep("const VERSION='prototype 0.37.0'", "const VERSION='prototype 0.38.0'")
rep('const SEEN_V=42;', 'const SEEN_V=43;')
rep("""<ul class="newlist"><li><b>Ink.</b>""",
    """<ul class="newlist"><li><b>The Scribe.</b> Write sixty lines in your book, whenever you like, and a Scribe comes to your fire for good, with an ink-dipped quill. Now and then it reads one of your old lines back to you. And on days you do one of your own small things, your Forgelings notice.</li>
    <li><b>Ink.</b>""")
import re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:8])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
