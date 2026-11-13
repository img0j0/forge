# 0.73.1: the season stamp is easy to see, and a done day always presses it (Hunter, November 12, a screenshot of
#   "Maple Days": "The logo next to maple days is kind of hard to make out due to the colors/contrast").
#   - A stamp not yet pressed was drawn pale grey at 45% opacity, nearly invisible on the gold tile. It now draws in
#     the row's own ink (like the other row icons), so it reads on the gold tile and on plain rows, by day and at night;
#     a pressed stamp keeps its colours.
#   - His card was done today before the seasons arrived (0.59), so its stamp was never pressed and the row still said
#     "Turn over today's card to press its stamp". Today now presses the stamp whenever the day is done.
import re,subprocess,os
S=open('base73.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.73.0'","const VERSION='prototype 0.73.1'")
rep("<title>Forgelings (prototype 0.73.0)</title>","<title>Forgelings (prototype 0.73.1)</title>")
rep("""fill="${on?c[ch]:'#B9B0A0'}"/>`;}});""","""fill="${on?c[ch]:'currentColor'}"/>`;}});""")
rep("""shape-rendering="crispEdges" aria-hidden="true" style="opacity:${on?1:.45}">""","""shape-rendering="crispEdges" aria-hidden="true" style="opacity:${on?1:.8}">""")
rep("  {const n=seasonNow();if(n&&state.cards.length){const got=state.seasons&&state.seasons[seasonKey(n)];",
    "  {const n=seasonNow();if(n&&state.cards.length&&s==='done'&&!(state.seasons&&state.seasons[seasonKey(n)])&&seasonPress())save();}\n  {const n=seasonNow();if(n&&state.cards.length){const got=state.seasons&&state.seasons[seasonKey(n)];")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk731.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk731.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
