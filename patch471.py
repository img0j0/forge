# 0.47.1: How did it feel? centres each face and its word inside the journal's ink circle (Hunter, on his phone:
# the faces sat high and crossed the circle's top edge).
import re,subprocess
S=open('base47.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.47.0'","const VERSION='prototype 0.47.1'")
rep("<title>Forgelings (prototype 0.47.0)</title>","<title>Forgelings (prototype 0.47.1)</title>")
rep("html.jr .app .facebtn{clip-path:none;border-radius:50%;background:none;box-shadow:inset 0 0 0 3px currentColor;width:76px;height:76px;min-height:76px;padding:0;",
    "html.jr .app .facebtn{clip-path:none;border-radius:50%;background:none;box-shadow:inset 0 0 0 3px currentColor;width:76px;height:76px;min-height:76px;padding:4px 0 0;justify-content:center;box-sizing:border-box;")
rep("html.jr .app .facebtn .feelface{width:30px;height:30px}","html.jr .app .facebtn .feelface{width:30px;height:30px;flex:none}\nhtml.jr .app .facebtn[aria-pressed=\"true\"] .feelface{transform:none}")
open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk471.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk471.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
