# 0.55.0: finer rendering for every Forgeling (Hunter, November 12: "Let's upgrade everything" after asking whether
#   the art could be better without hiring an artist). Same shapes, faces and colours; drawn more finely:
#   1. Round form shading (commit): light from the upper left; highlight, base, a new mid tone and shade by where a
#      pixel sits between the lit and the far edge of its part (small parts keep the old rim rule).
#   2. Selective outlines (selout): outlines take the colour of what they edge (accent, horn, gold get their own
#      dark line), the lit upper-left edge softens to the part's deep shade, and lines inside the silhouette (arms
#      over the body) soften too.
#   3. Palette: mid tones (29 body, 30 accent, 31 belly), part outlines (32 accent, 33 horn, 34 gold), warmer
#      highlights, cooler shadows.
#   4. Second generation: raised Shade arms only on the slimmer bodies; head keepsakes always rest on the head
#      (creatures/float.py), rounded to whole pixels (a noodle's daisies were not drawn).
#   Checks: creatures/identity.py (silhouette and face of 4,000 sprites per generation identical to 0.54.1),
#   check.py (faces clear: 0 problems), float.py (0 floating). qa_ref's reference images will differ by design.
import re,subprocess,os
S=open('base541.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
H='creatures/'
rep("const VERSION='prototype 0.54.1'","const VERSION='prototype 0.55.0'")
rep("<title>Forgelings (prototype 0.54.1)</title>","<title>Forgelings (prototype 0.55.0)</title>")
def swap(start,name,new):
    global S
    i=S.find(start); j=S.find('function '+name+'('); assert 0<i<=j,(start,name); j=S.find('\n}',j)+2; S=S[:i]+new.rstrip('\n')+S[j:]
R=lambda f:open(H+f).read()
swap('function commit(','commit',R('render.js'))
swap('function makePal(','makePal',R('palette.js'))
swap('function genSpec(','genSpec',R('genSpec.js'))
swap('/* 0.54: the second generation of bright','buildSprite',R('cute2.js')+'\n'+R('buildSprite.js'))
# outlines now come in several slots (OL): Forgebound gold, legendary foil and statue outlines follow all of them
rep("const FOIL3={4:1,6:1,9:1,10:1,17:1},FOIL4={1:1,17:1};","const FOIL3={4:1,6:1,9:1,10:1,17:1},FOIL4={1:1,17:1,32:1,33:1,34:1,35:1,36:1,37:1,38:1};")
rep("foil=!!(FS&&FS[slot])||(c.bond>=25&&slot===1);","foil=!!(FS&&FS[slot])||(c.bond>=25&&OL(slot));",2) if S.count("foil=!!(FS&&FS[slot])||(c.bond>=25&&slot===1);")==2 else rep("foil=!!(FS&&FS[slot])||(c.bond>=25&&slot===1);","foil=!!(FS&&FS[slot])||(c.bond>=25&&OL(slot));")
rep("if(sl===1&&c.bond>=BOND_AT[4])q=GOLD","if(OL(sl)&&c.bond>=BOND_AT[4])q=GOLD")
rep("if((FS&&FS[sl])||(c.bond>=25&&sl===1)){","if((FS&&FS[sl])||(c.bond>=25&&OL(sl))){")
rep("col[i]=sl===1?[.30,.28,.34]:","col[i]=OL(sl)?[.30,.28,.34]:")
rep("out[i]=sl===1?1:0;}","out[i]=OL(sl)?1:0;}")
assert not __import__('re').search(r'\bsl===1\b|\bslot===1\b',S),'an outline check was missed'
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk55.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk55.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
