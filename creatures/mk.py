# Builds /tmp/c54.html: the current build with the creature files swapped in (so edits here can be seen before a
# patch) and a test hook (window.__H).
import os
H=os.path.dirname(os.path.abspath(__file__))
s=open(H+'/../work.html').read()
def swap(start,name,new,alt=None):
    global s
    i=s.find(start)
    if i<0 and alt: i=s.find(alt)
    if name=='commit' and 'function selout(' in s: name='selout'
    j=s.find('function '+name+'('); assert 0<i<=j,(start,name); j=s.find('\n}',j)+2; s=s[:i]+new.rstrip('\n')+s[j:]
R=lambda f:open(H+'/'+f).read()
a=s.find('/* 0.56: Forgelings are drawn on a 40x40');a=a if a>0 else s.find('const N=32;');b=s.find('/* Paint a mask into the grid');assert 0<a<b
s=s[:a]+R('helpers.js').rstrip('\n')+'\n'+s[b:]
OLDST="if(px>=0&&py>=0&&px<N&&py<N)g[py*N+px]=CH[ch];"
if OLDST in s: s=s.replace(OLDST,"if(px>=-SPP&&py>=-SPP&&px<SPC+SPP&&py<SPC+SPP)g[SPI(px,py)]=CH[ch];")
swap('/* 0.55: finer rendering','commit',R('render.js'),'function commit(')
swap('/* 0.55: the palette adds','makePal',R('palette.js'),'function makePal(')
swap('function genSpec(','genSpec',R('genSpec.js'))
swap('/* 0.54: the second generation of bright','buildSprite',R('cute2.js')+'\n'+R('buildSprite.js')+'\nwindow.__H={genSpec,buildSprite,makePal,N};')
open('/tmp/c54.html','w').write(s)
