# 0.48.1: the new Forgelings icon (Hunter chose the seal mark on November 1, 2026): a red wax seal pressed with a
# journal and a flame, on warm amber. The page's own favicon and apple-touch-icon (data URIs) are swapped here;
# pwa.py copies the web icons and the iPhone app's ios-setup.py the app icon, all rendered by art/make_icons.py.
import re,subprocess,base64
S=open('base48.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.48.0'","const VERSION='prototype 0.48.1'")
rep("<title>Forgelings (prototype 0.48.0)</title>","<title>Forgelings (prototype 0.48.1)</title>")
b64=lambda f: base64.b64encode(open(f,'rb').read()).decode()
for rel,f in [('icon','art/out/favicon-64.png'),('apple-touch-icon','art/out/apple-touch-icon.png')]:
    m=re.findall(r'<link rel="'+rel+r'"[^>]*href="data:image/png;base64,[A-Za-z0-9+/=]+"',S); assert len(m)==1,(rel,len(m))
    new=re.sub(r'base64,[A-Za-z0-9+/=]+"','base64,'+b64(f)+'"',m[0]); rep(m[0],new)
open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk481.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk481.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
