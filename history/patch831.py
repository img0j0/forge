# 0.83.1: the curio shelf stops counting (found while retaking the store screenshots: the Hearth's chip read
#   "Curio shelf · 20 of 40"). The look-back and progress doc (0.80) said curios are things you have, not progress, and
#   the Map never counts; the shelf already shows found curios and faint outlines for the rest.
import re,subprocess,os
S=open('base83.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.83.0'","const VERSION='prototype 0.83.1'")
rep("<title>Forgelings (prototype 0.83.0)</title>","<title>Forgelings (prototype 0.83.1)</title>")
rep("Curio shelf · ${have} of ${shelfSet().length}<","Curio shelf<")
rep("<summary>Curio shelf, ${have} of ${shelfSet().length}<","<summary>Curio shelf<")
rep('<p class="muted small">${have} of ${shelfSet().length} found.</p>','')
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk831.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk831.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
