# 0.44.2: the "See <realm> in 3D" button on a realm page was dark ink on the app's night/dark surface colour (1.18:1)
# whenever the sky is at night or the theme is dark (Hunter, 10pm screenshot). The realm page is always cream paper,
# so the button now carries its own paper colours in every mode. New qa_contrast scans every screen day and night.
import re,subprocess
S=open('base441.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.44.1'","const VERSION='prototype 0.44.2'")
rep("<title>Forgelings (prototype 0.44.1)</title>","<title>Forgelings (prototype 0.44.2)</title>")
rep(".isgo{display:block;margin:8px 0 0;min-height:44px}",
    ".isgo{display:block;margin:8px 0 0;min-height:44px}\n.parch .chip.isgo{background:#FFFDF6;color:#2E2A47;border:2px solid #2E2A47}")
open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk442.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk442.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:400])
