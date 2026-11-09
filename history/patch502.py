# 0.50.2: the update note's "Load it" button was hard to see (Hunter, November 8).
#   In the journal look, --bg is the dark desk, so in the day the note drew dark text and a dark
#   button on dark ink. They now use the journal's own paper and ink: ink bar, paper text, a paper "Load it" button.
import re,subprocess,os
S=open('base501.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.50.1'","const VERSION='prototype 0.50.2'")
rep("<title>Forgelings (prototype 0.50.1)</title>","<title>Forgelings (prototype 0.50.2)</title>")
CSS="""
/* 0.50.2: the update note uses the journal's paper and ink (its --bg is the dark desk) */
html.jr .updbar{background:var(--jink);color:var(--jpaper)}
html.jr .updbar{box-shadow:0 0 0 2px var(--jpaper),0 6px 18px rgba(0,0,0,.32)}
html.jr .updbar button{background:var(--jpaper);color:var(--jink)}
html.jr .updbar button.later{background:transparent;color:var(--jpaper)}
"""
i=S.index("</style>",S.index("</style>")+1); S=S[:i]+CSS+S[i:]
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk502.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk502.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
