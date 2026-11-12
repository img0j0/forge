# 0.54.1: second-generation layout (Hunter, November 12: "arms are covering facial features"). The face is laid out
#   first and fitted to the body (every eye, mouth, nose and blush pixel has body on all four sides, no outline
#   beneath it, eyes kept toward the middle); arms take the first placement that leaves a pixel of body between their
#   outline and the face, else a calmer pose; the face is drawn last, after keepsakes and crowns, and head keepsakes
#   sit above it. creatures/check.py renders 24,000 second-generation sprites (every rarity, keepsake and bob frame)
#   and finds no problems; creatures/same.py: the first generation is unchanged. Second-generation Forgelings found
#   under 0.54.0 may shift a pixel or two where their face or arms were crowded.
import re,subprocess,os
S=open('base54.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
H='creatures/'
rep("const VERSION='prototype 0.54.0'","const VERSION='prototype 0.54.1'")
rep("<title>Forgelings (prototype 0.54.0)</title>","<title>Forgelings (prototype 0.54.1)</title>")
def swap(start,name,new):
    global S
    i=S.find(start); j=S.find('function '+name+'('); assert 0<i<=j; j=S.find('\n}',j)+2; S=S[:i]+new.rstrip('\n')+S[j:]
swap('function genSpec(','genSpec',open(H+'genSpec.js').read())
swap('/* 0.54: the second generation of bright','buildSprite',open(H+'cute2.js').read()+'\n'+open(H+'buildSprite.js').read())
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk541.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk541.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
