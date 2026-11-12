# 0.56.0: nothing cut off (Hunter, November 12, with Wobly: "notice how the ears get cut off"). Forgelings were drawn
#   on a 32x32 grid and anything reaching past it was cut: tall ears and antennae, crowns, caps and hats, wings, tails
#   and wide arms. About half of all Forgelings, both generations, since the start. They are now drawn on a 40x40 grid
#   (the same creature coordinates with a 4-pixel margin, creatures/helpers.js), and every place that shows a sprite
#   puts that grid 4 pixels up and left of where the 32x32 went, so every pixel shown before stays where it was and the
#   cut-off tips appear: the card art and share picture (drawFrame), the Hearth. Ears, antennae and horns that would
#   reach past even the 40x40 frame sit just low enough to fit (about 6% of Forgelings; every other one keeps every pixel). Thumbnails (spriteURL), Hearth statues,
#   the cover Forgeling and 3D statues keep showing the middle 32x32. Also: second-generation Shade mouths with an odd
#   width (stitch, tusks) were never drawn (half-pixel position); now they are.
#   Checks: creatures/identity.py (the middle 32x32 matches 0.55.1 wherever 0.55.1 drew nothing cut), clip.py (nothing
#   cut by the 40x40 frame), check.py, float.py.
import re,subprocess,os
S=open('base551.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
H='creatures/'
rep("const VERSION='prototype 0.55.1'","const VERSION='prototype 0.56.0'")
rep("<title>Forgelings (prototype 0.55.1)</title>","<title>Forgelings (prototype 0.56.0)</title>")
R=lambda f:open(H+f).read()
a=S.find('const N=32;'); b=S.find('/* Paint a mask into the grid'); assert 0<a<b; S=S[:a]+R('helpers.js').rstrip('\n')+'\n'+S[b:]
rep("function stamp(g,x,y,rows,flipH){rows.forEach((row,j)=>{const r=flipH?row.split('').reverse().join(''):row;for(let i=0;i<r.length;i++){const ch=r[i];if(ch==='.')continue;const px=x+i,py=y+j;if(px>=0&&py>=0&&px<N&&py<N)g[py*N+px]=CH[ch];}});}",
    "function stamp(g,x,y,rows,flipH){rows.forEach((row,j)=>{const r=flipH?row.split('').reverse().join(''):row;for(let i=0;i<r.length;i++){const ch=r[i];if(ch==='.')continue;const px=x+i,py=y+j;if(px>=-SPP&&py>=-SPP&&px<SPC+SPP&&py<SPC+SPP)g[SPI(px,py)]=CH[ch];}});}")
def swap(start,name,new):
    global S
    i=S.find(start); j=S.find('function '+name+'('); assert 0<i<=j,(start,name); j=S.find('\n}',j)+2; S=S[:i]+new.rstrip('\n')+S[j:]
swap('/* 0.55: finer rendering','selout',R('render.js'))
swap('/* 0.55: the palette adds','makePal',R('palette.js'))
swap('function genSpec(','genSpec',R('genSpec.js'))
swap('/* 0.54: the second generation of bright','buildSprite',R('cute2.js')+'\n'+R('buildSprite.js'))
# the places that show sprites
rep("if(sx>=0&&sx<32&&sy>=0&&sy<32)slot=g[sy*32+sx];","{const X=sx+SPP,Y=sy+SPP;if(X>=0&&X<SPN&&Y>=0&&Y<SPN)slot=g[Y*SPN+X];}")
rep("for(let sy=0;sy<32;sy++)for(let sx=0;sx<32;sx++){const sl=g[sy*32+sx];if(!sl)continue;let q=pal[sl];if(OL(sl)",
    "for(let sy=-SPP;sy<SPC+SPP;sy++)for(let sx=-SPP;sx<SPC+SPP;sx++){const sl=g[SPI(sx,sy)];if(!sl)continue;let q=pal[sl];if(OL(sl)")
rep("const sl=sp[(2*y+1)*32+2*x+1]||sp[(2*y)*32+2*x];","const sl=sp[SPI(2*x+1,2*y+1)]||sp[SPI(2*x,2*y)];")
rep("for(let i=0;i<1024;i++){const sl=g[i];if(!sl)continue;let [r,gg,b]=pl.pal[sl];","for(let i=0;i<1024;i++){const sl=g[SPI(i&31,i>>5)];if(!sl)continue;let [r,gg,b]=pl.pal[sl];")
rep("for(let sy=0;sy<32;sy++)for(let sx=0;sx<32;sx++){const sl=g[sy*32+sx];if(sl)put(mx+sx,my+sy+breathe,e.pal[sl]);}",
    "for(let sy=0;sy<32;sy++)for(let sx=0;sx<32;sx++){const sl=g[SPI(sx,sy)];if(sl)put(mx+sx,my+sy+breathe,e.pal[sl]);}")
rep("for(let i=0;i<32&&!edge;i++){if(g[i]||g[32+i]||g[i*32]||g[i*32+31])edge=true;}",
    "for(let i=0;i<32&&!edge;i++){if(g[SPI(i,0)]||g[SPI(i,1)]||g[SPI(0,i)]||g[SPI(31,i)])edge=true;}")
rep("for(let i=0;i<1024;i++){const sl=g[i];if(!sl)continue;const q=e.pal[sl];im.data[i*4]=q[0];",
    "for(let i=0;i<1024;i++){const sl=g[SPI(i&31,i>>5)];if(!sl)continue;const q=e.pal[sl];im.data[i*4]=q[0];")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk56.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk56.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
