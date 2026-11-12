# 0.56.1: ears stretching as Forgelings bob (Hunter, November 12, with Wobly: "the ears ... are getting stretched/
#   elongated as the character bounces"). 0.56 fitted tall ears and horns into the frame separately in each bob frame,
#   so on the bob-down frame they sat a pixel higher relative to the body and looked stretched. The fit is now worked
#   out once on the resting pose and moves with the body, with one free row under the top of the frame. Hugging
#   paws' lowest point moves with the bob too (it could switch the arms' pose between frames).
#   creatures/bob.py: above the feet, every bob frame is the rest frame one pixel lower (0 of 6,000 differ; 379 in 0.56).
import re,subprocess,os
S=open('base56.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
H='creatures/'
rep("const VERSION='prototype 0.56.0'","const VERSION='prototype 0.56.1'")
rep("<title>Forgelings (prototype 0.56.0)</title>","<title>Forgelings (prototype 0.56.1)</title>")
def swap(start,name,new):
    global S
    i=S.find(start); j=S.find('function '+name+'('); assert 0<i<=j,(start,name); j=S.find('\n}',j)+2; S=S[:i]+new.rstrip('\n')+S[j:]
R=lambda f:open(H+f).read()
swap('/* 0.54: the second generation of bright','buildSprite',R('cute2.js')+'\n'+R('buildSprite.js'))
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk561.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk561.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
