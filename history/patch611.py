# 0.61.1: the privacy note names visit links (0.61): what they hold, and that they go only where you send them.
#   legal/page.py (the website and App Store privacy page) says the same, dated November 12, 2026.
import re,subprocess,os
S=open('base61.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.61.0'","const VERSION='prototype 0.61.1'")
rep("<title>Forgelings (prototype 0.61.0)</title>","<title>Forgelings (prototype 0.61.1)</title>")
rep("DOCS_DATE='November 11, 2026'","DOCS_DATE='November 12, 2026'")
rep('''<div class="tale"><b>When you choose to share</b><p>"Save a copy", "Send my report" and gift links create something that goes only where you put it, for example a message to a friend. A gift link holds only the curio, your Forgeling’s name and look, and your note. A statue link holds only what the statue is built from: its look, name and the day it was cast.''',
    '''<div class="tale"><b>When you choose to share</b><p>"Save a copy", "Send my report", gift links and visit links create something that goes only where you put it, for example a message to a friend. A gift link holds only the curio, your Forgeling’s name and look, and your note. A visit link holds only your Forgeling’s name and look, and your note. A statue link holds only what the statue is built from: its look, name and the day it was cast.''')
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk611.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk611.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
