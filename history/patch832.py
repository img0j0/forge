# 0.83.2: Today's card matches the deck (Hunter, November 24, iPhone screenshot: "the card design doesn't match our
#   update"). Today's face-down card still used the older back made to carry words (--cbT: seal high, room for a label),
#   while the three cards in the choose sheet use the 0.72 back (--cbP: ribbons crossing, seal centred). Today's card now
#   uses --cbP. The "Today's card" label on it goes (the heading under it already says so; the button keeps its name).
import re,subprocess,os
S=open('base831.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.83.1'","const VERSION='prototype 0.83.2'")
rep("<title>Forgelings (prototype 0.83.1)</title>","<title>Forgelings (prototype 0.83.2)</title>")
rep(".heroback{background:var(--cbT) 0 0/100% 100% no-repeat !important;",".heroback{background:var(--cbP) 0 0/100% 100% no-repeat !important;")
rep(".heroback svg{display:none}",".heroback svg{display:none}\n.heroback>span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk832.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk832.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
