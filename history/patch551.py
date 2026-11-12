# 0.55.1: holo rainbow (Hunter, November 12, with Urvyr, a holo Shade Forgeling: "Notice the top left side"). 0.55's
#   broad highlight used slot 4, which rarity-3 foil (FOIL3) paints rainbow, so holo Forgelings got a thick rainbow
#   wedge on the upper left. Slot 4 is the one-pixel lit rim again, as before 0.55; the broader glow toward the
#   light has soft tones of its own (39 body, 40 accent, 41 belly) that foil leaves alone. creatures/foil.py shows
#   foil pixels before and after.
import re,subprocess,os
S=open('base55.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
H='creatures/'
rep("const VERSION='prototype 0.55.0'","const VERSION='prototype 0.55.1'")
rep("<title>Forgelings (prototype 0.55.0)</title>","<title>Forgelings (prototype 0.55.1)</title>")
def swap(start,name,new):
    global S
    i=S.find(start); j=S.find('function '+name+'('); assert 0<i<=j,(start,name); j=S.find('\n}',j)+2; S=S[:i]+new.rstrip('\n')+S[j:]
R=lambda f:open(H+f).read()
swap('/* 0.55: finer rendering','selout',R('render.js'))
swap('/* 0.55: the palette adds','makePal',R('palette.js'))
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk551.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk551.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
