# 0.48.3: the card back is a sealed journal page (Hunter picked option 3, "Leather journal", on the canvas, November 1):
# stitched dark leather, a gold ribbon, and the seal mark in pixels, in place of the campfire. It is the cover you tap
# to turn a Forgeling over (reveals and packs). The envelope's peeking and fanned cards take the same leather look.
# The calling card and a card's Moment back (--cbT, they carry words) are unchanged.
import re,subprocess,sys
sys.path.insert(0,'art'); from cardback import BACKS, packed
S=open('base482.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.48.2'","const VERSION='prototype 0.48.3'")
rep("<title>Forgelings (prototype 0.48.2)</title>","<title>Forgelings (prototype 0.48.3)</title>")
m=re.search(r'--cbP:url\("data:image/svg\+xml,[^"]*"\)',S); assert m
rep(m.group(0),'--cbP:url("data:image/svg+xml,'+packed(BACKS['leather'])+'")')
# the envelope's card backs: leather with a gold ribbon and a small seal
rep("""  const cb=(x,y,r)=>`<g transform="translate(${x} ${y}) rotate(${r})"><rect width="44" height="62" fill="#5B4A9E" stroke="#FFFFFF" stroke-width="3"/><rect x="6" y="6" width="32" height="50" fill="none" stroke="#FFD36B" stroke-width="1.2" stroke-dasharray="3 2.5"/><path d="M22 22l7 9-7 9-7-9z" fill="#FFD36B"/></g>`;""",
"""  const cb=(x,y,r)=>`<g transform="translate(${x} ${y}) rotate(${r})"><rect width="44" height="62" rx="2" fill="#5A2C2A" stroke="#2E1614" stroke-width="2"/><rect x="4" y="4" width="36" height="54" fill="none" stroke="#C9A15A" stroke-width="1" stroke-dasharray="2.5 2"/><rect x="20" y="1" width="4" height="60" fill="#E0A82E"/><circle cx="22" cy="31" r="8" fill="#B3283A"/><circle cx="22" cy="31" r="5.5" fill="none" stroke="#8A1C2C" stroke-width="1.2"/><path d="M22 26.5c1.6 2 3 3.2 3 5a3 3 0 0 1-6 0c0-1.4 1-2.2 1.4-3.4.4 1 .8 1.4 1.6 1.4 0-1.2-.3-2 0-3z" fill="#F6DCC8"/></g>`;""")
open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk483.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk483.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
