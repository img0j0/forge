# Builds /tmp/c54.html: the current build with the creature files swapped in (so edits here can be seen before a
# patch) and a test hook (window.__H).
import os
H=os.path.dirname(os.path.abspath(__file__))
s=open(H+'/../work.html').read()
def swap(start,name,new):
    global s
    i=s.find(start); j=s.find('function '+name+'('); j=s.find('\n}',j)+2; assert 0<i<=s.find('function '+name+'('); s=s[:i]+new.rstrip('\n')+s[j:]
swap('function genSpec(','genSpec',open(H+'/genSpec.js').read())
swap('/* 0.54: the second generation of bright','buildSprite',open(H+'/cute2.js').read()+'\n'+open(H+'/buildSprite.js').read()+'\nwindow.__H={genSpec,buildSprite,makePal};')
open('/tmp/c54.html','w').write(s)
