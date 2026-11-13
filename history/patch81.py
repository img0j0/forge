# 0.81: the Forge keeps its own count (look-back and progress design doc, decision 3; Hunter, November 13: "Let's go with
#   the recommendations"). The doc asked for a look at the Forge's prices before merging embers and spares. The look found
#   that spares can't become one material without breaking what the Forge means: a realm's charm is made from that realm's
#   curios, and a relic needs each of its realm's four. So both stay as ingredients, and the decision's aim is kept:
#   the Forge's numbers live only inside the Forge.
#   - The reveal no longer says "An ember for the Forge".
#   - The Hearth's Forge button no longer counts embers; it says "Something is ready" when a piece can be made.
#   - The Forge sheet drops "n of m pieces made" (Made is a section already); embers and spares stay there, together.
import re,subprocess,os
S=open('base80.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.80.0'","const VERSION='prototype 0.81.0'")
rep("<title>Forgelings (prototype 0.80.0)</title>","<title>Forgelings (prototype 0.81.0)</title>")
rep("""      <p class="muted small" id="rvEmber">${allIn?'Two embers':'An ember'} for the Forge.</p>\n""","")
rep("""<button class="act" id="hForge">${HIC.forge}The Forge<small id="hEmbers">${embRoll(e,e===1?'ember':'embers')}</small></button>""",
"""<button class="act" id="hForge">${HIC.forge}The Forge${fgList().some(fgCan)?'<small id="hEmbers">Something is ready</small>':''}</button>""")
rep("""<p class="muted small">${e} ${e===1?'ember':'embers'} and ${sp} spare ${sp===1?'curio':'curios'}. ${made} of ${L.length} pieces made.${s?""","""<p class="muted small">${e} ${e===1?'ember':'embers'} and ${sp} spare ${sp===1?'curio':'curios'}.${s?""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk81.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk81.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
