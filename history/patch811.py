# 0.81.1: the Map/Tales switch fits two sections (Hunter, November 13, iPhone screenshot: "The tab bar at the top is
#   misshaped after moving the book"). The switch was built for three sections (Map, Tales, Journal): three grid columns
#   and a highlight a third wide, so with two the highlight covered a third and the last third sat empty. It now takes
#   its count from `--n`.
import re,subprocess,os
S=open('base81.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.81.0'","const VERSION='prototype 0.81.1'")
rep("<title>Forgelings (prototype 0.81.0)</title>","<title>Forgelings (prototype 0.81.1)</title>")
rep(".app .chips.seg{display:grid;grid-template-columns:repeat(3,1fr);",".app .chips.seg{display:grid;grid-template-columns:repeat(var(--n,3),1fr);")
rep("width:calc((100% - 6px)/3);border-radius:10px;background:#FFD36B;","width:calc((100% - 6px)/var(--n,3));border-radius:10px;background:#FFD36B;")
rep("""<div class="chips seg" role="group" aria-label="Map sections" style="--i:${si};--p:${sp}">""","""<div class="chips seg" role="group" aria-label="Map sections" style="--i:${si};--p:${sp};--n:${subs.length}">""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk82.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk82.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
