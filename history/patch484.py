# 0.48.4: the other card backs follow (Hunter: "it's still showing the old card backs"). The daily calling card on
# Today, the calling-card flip and a Forgeling's Moment side (--cbT, the backs that carry words) were still the
# campfire. They take the leather back too, with the seal high and the ribbon ending above the words.
import re,subprocess,sys
sys.path.insert(0,'art'); from cardback import BACKS, packed
S=open('base483.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.48.3'","const VERSION='prototype 0.48.4'")
rep("<title>Forgelings (prototype 0.48.3)</title>","<title>Forgelings (prototype 0.48.4)</title>")
m=re.search(r'--cbT:url\("data:image/svg\+xml,[^"]*"\)',S); assert m
rep(m.group(0),'--cbT:url("data:image/svg+xml,'+packed(BACKS['leather_text'])+'")')
open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk484.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk484.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
