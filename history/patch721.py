# 0.72.1: a flipped card shows the clean card back (Hunter, November 12: "I was expecting the words to be taken off.
#   Just the clean art"). "Flip card" now turns the card to the full Leather journal back (the same one face-down cards
#   have), and the words that used to be printed on it (the day it was earned, the date, the calling, its tale and
#   ink, the season, the edition number) appear under the card while it is flipped, in place of the hint line.
import re,subprocess,os
S=open('base72.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.72.0'","const VERSION='prototype 0.72.1'")
rep("<title>Forgelings (prototype 0.72.0)</title>","<title>Forgelings (prototype 0.72.1)</title>")
rep("function flipCard(){","""function backCap(cd){
  const h=$('#inspHint');let el=$('#inspBack');if(!el&&h){h.insertAdjacentHTML('afterend','<div class="inspback" id="inspBack" hidden></div>');el=$('#inspBack');}
  if(!el)return;const on=cd.classList.contains('showback');
  if(on){const bi=cd.querySelector('.cbk .binfo');el.innerHTML=bi?bi.innerHTML:'';el.hidden=false;if(h)h.hidden=true;}else{el.hidden=true;if(h)h.hidden=false;}}
function flipCard(){""")
rep("cd.classList.toggle('showback');cd.classList.remove('sq');","cd.classList.toggle('showback');backCap(cd);cd.classList.remove('sq');")
css="""
/* 0.72.1: the flipped card is the clean back; its words sit under the card */
.card .face.cbk{background:var(--cbP) 0 0/100% 100% no-repeat,#5A2C2A !important;border:0}
.card .cbk>.bsp,.card .cbk>.binfo{display:none !important}
.card .face.cbk::after{content:"";position:absolute;inset:-30% -60%;pointer-events:none;background:linear-gradient(110deg,transparent 42%,rgba(255,230,160,.34) 50%,transparent 58%);transform:translateX(-60%);animation:cbSheen 5.5s ease-in-out infinite}
html.reduce .card .face.cbk::after{animation:none;opacity:0}
.inspback{margin:6px auto 2px;text-align:center;display:grid;gap:3px;max-width:330px;padding:0 12px}
.inspback>div,.inspback>p{font:400 15px/1.35 var(--body);color:inherit;opacity:1;max-width:none;margin:0}
.inspback .m1{font-weight:700;font-size:16px}.inspback .m4{opacity:.7;font-size:13px}.inspback .m3,.inspback .inkl{font-style:italic;color:inherit}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk721.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk721.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
