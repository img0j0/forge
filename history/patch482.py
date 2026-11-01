# 0.48.2: the cover (Hunter, on his phone): the Forgeling on the cover label is drawn at its true size, scaled to the
# screen, instead of falling back to a tiny 32-pixel picture; the cover picks a Forgeling whose ears fit inside its
# frame (the old seed's ears were cut flat at the top); and the "No account..." line sits inside the stitching.
import re,subprocess
S=open('base481.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.48.1'","const VERSION='prototype 0.48.2'")
rep("<title>Forgelings (prototype 0.48.1)</title>","<title>Forgelings (prototype 0.48.2)</title>")
rep("""  const cov=lsOn(),img=cov?`<img src="${spriteURL({id:-1,seed:20261031,rarity:0,dark:false,theme:0,v:0,keep:'',bond:0,name:'',nick:''})}" alt="A small Forgeling waving from the cover">`:'';""",
"""  const cov=lsOn(),img=cov?`<img src="${spriteURL(coverMate())}" alt="A small Forgeling waving from the cover">`:'';""")
rep("function openTitle(){","""/* 0.48.2: the cover's Forgeling: the first of a fixed run of seeds whose sprite stays clear of its frame's edges */
let COVER_MATE=null;
function coverMate(){
  if(COVER_MATE)return COVER_MATE;const base={id:-1,seed:20261031,rarity:0,dark:false,theme:0,v:0,keep:'',bond:0,name:'',nick:''};
  for(let s=20261031;s<20261031+60;s++){const c=Object.assign({},base,{seed:s});try{const e=prep(c);if(!e.sp[0])e.sp[0]=buildSprite(e.spec,0,0);const g=e.sp[0];let edge=false;
    for(let i=0;i<32&&!edge;i++){if(g[i]||g[32+i]||g[i*32]||g[i*32+31])edge=true;}if(!edge)return COVER_MATE=c;}catch(err){}}
  return COVER_MATE=base;
}
function openTitle(){""")
rep(".scrim.jcov .jlabel img{flex:0 1 auto;min-height:0;width:auto;height:min(190px,100%);max-height:100%;aspect-ratio:1;image-rendering:pixelated}",
    ".scrim.jcov .jlabel img{flex:none;width:auto;height:clamp(84px,min(22vh,46vw),180px);aspect-ratio:1;image-rendering:pixelated}")
rep(".scrim.jcov .title-top{z-index:2;top:calc(5vh + 26px + env(safe-area-inset-top,0px));bottom:calc(150px + env(safe-area-inset-bottom,0px));",
    ".scrim.jcov .title-top{z-index:2;top:calc(5vh + 26px + env(safe-area-inset-top,0px));bottom:calc(172px + env(safe-area-inset-bottom,0px));")
rep(".scrim.jcov .title-bottom{z-index:2;padding-left:40px;padding-right:74px}",
    ".scrim.jcov .title-bottom{z-index:2;padding-left:40px;padding-right:74px;padding-bottom:calc(48px + env(safe-area-inset-bottom,0px))}")
rep(".scrim.jcov .wordmark{color:#FFD36B;text-shadow:0 2px 0 #8A5A10;margin:0}",".scrim.jcov .wordmark{color:#FFD36B;text-shadow:0 2px 0 #8A5A10;margin:0;font-size:min(64px,calc((100vw - 140px) / 4.6))}")
rep("padding:0 64px 0 34px;display:flex;flex-direction:column;align-items:center;gap:4px}","padding:0 74px 0 34px;display:flex;flex-direction:column;align-items:center;gap:4px}")
open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk482.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk482.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
