# 0.44.1: interface pass (a look at every screen and sheet at 320, 375 and 430 wide, with ~4 months of play).
# Fixes: the "Who sits by the fire?" picker no longer cuts off its fourth column on smaller phones; the Binder's summary
# no longer runs under the sun or moon in the sky; the Hearth's lantern hint opens the Forge.
import re,subprocess,sys
S=open('base44.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old)
    assert c==n,(c,n,old[:90])
    S=S.replace(old,new)

rep("const VERSION='prototype 0.44.0'","const VERSION='prototype 0.44.1'")
rep("<title>Forgelings (prototype 0.44.0)</title>","<title>Forgelings (prototype 0.44.1)</title>")

# 1. picker: four fixed columns of 84px cards overflowed 335px (375 wide) and 280px (320 wide); fit as many as fit
rep(".pickgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;justify-items:center;margin:12px 0;",".pickgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(84px,1fr));gap:8px;justify-items:center;margin:12px 0;padding:3px;")

# 2. the sky's sun/moon sits ~21vw in from the right at 17% height, right where the Binder's summary wraps on most phones
rep(".summary{color:var(--muted);font-size:15px;margin:0 2px 6px}",
    ".summary{color:var(--muted);font-size:15px;margin:0 2px 6px;padding-right:max(0px,calc(21vw - 14px))}")

# 3. the lantern hint says what to do; now it also takes you there
rep("""notes+=`<p class="small" id="hLantern">A charted realm is waiting for a lantern. ${fgCan(FORGE_R.find(r=>r.id==='xlantern'))?'You have what it needs.':'See what it needs in the Forge.'}</p>`;""",
    """notes+=`<p class="small" id="hLantern">A charted realm is waiting for a lantern. <button type="button" class="ghost" id="hLanternGo">${fgCan(FORGE_R.find(r=>r.id==='xlantern'))?'You have what it needs. Open the Forge':'See what it needs in the Forge'}</button></p>`;""")
rep("  else if(b.id==='hForge')openForge();","  else if(b.id==='hForge'||b.id==='hLanternGo')openForge();")

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S)
open('/tmp/chk441.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk441.js'],capture_output=True,text=True)
print('node --check',r.returncode,r.stderr[:800])
