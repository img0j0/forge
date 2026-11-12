# 0.66: a Forgeling peeks into your postcard, and your latest postcard on the home-screen widget
#   (Hunter, November 12: "Yes please build a plan of action and execute"; ideas 1 and 2 of the brainstorm).
#   Peek: about one new postcard in three, your companion (or today's Forgeling) peeks up over its bottom edge, from
#   the left or the right. Stored with the postcard as k = {c: card id, s: 0 left / 1 right}; drawn as its sprite over
#   the photo, so "Change the photo" rolls again. Widget: the app sends the latest postcard (with its peek, 288 x 216,
#   nearest-neighbour) as `post`; the iPhone's medium widget and the Android widget show it instead of the sprite when
#   no one is out wandering. The website is unchanged: it has no widget.
import re,subprocess,os
S=open('base651.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.65.1'","const VERSION='prototype 0.66.0'")
rep("<title>Forgelings (prototype 0.65.1)</title>","<title>Forgelings (prototype 0.66.0)</title>")

# the save keeps the peek
rep("o[k]={r:v.r,p:v.p};});s.posts=o;","o[k]={r:v.r,p:v.p};if(v.k&&typeof v.k==='object'&&Number.isFinite(v.k.c)&&(v.k.s===0||v.k.s===1))o[k].k={c:v.k.c,s:v.k.s};});s.posts=o;")
# the postcard, with its peek
rep("""function pcFig(k,p,cls){return `<figure class="pcard${cls?' '+cls:''}" style="--pr:${PC_RAMP[p.r][3]}"><img src="${pcURL(p.p,p.r)}" alt="Your photo postcard, ${esc(dateLabel(k))}" width="${PC_W*3}" height="${PC_H*3}"><span""",
"""const pcPeek=p=>{const c=p&&p.k?cardById(p.k.c):null;return c?{c,n:c.nick||c.name,s:p.k.s}:null;};
function pcFig(k,p,cls){const pk=pcPeek(p);return `<figure class="pcard${cls?' '+cls:''}" style="--pr:${PC_RAMP[p.r][3]}"><span class="pcwin"><img src="${pcURL(p.p,p.r)}" alt="${pk?`Your photo postcard, ${esc(dateLabel(k))}, with ${esc(pk.n)} peeking in`:`Your photo postcard, ${esc(dateLabel(k))}`}" width="${PC_W*3}" height="${PC_H*3}">${pk?`<img class="pcpeek ${pk.s?'r':'l'}" src="${spriteURL(pk.c)}" alt="" width="64" height="64">`:''}</span><span""")
rep("""  state.posts=state.posts||{};state.posts[k]={r,p:pcPack(idx)};""","""  state.posts=state.posts||{};state.posts[k]={r,p:pcPack(idx)};
  {const m=companion()||mateNow()||c;if(m&&Math.random()<.35)state.posts[k].k={c:m.id,s:Math.random()<.5?0:1};}""")

# the widget gets the latest postcard
rep("let wLast='',wAct=0;","""let wLast='',wAct=0,wPost={k:'',b64:'',busy:''};
/* the latest postcard for the widget: 288 x 216, nearest-neighbour, with its peek drawn in */
function postForWidget(){
  const ks=Object.keys(state.posts||{}).sort();if(!ks.length)return '';
  const k=ks[ks.length-1],p=state.posts[k],key=k+':'+p.p.length+':'+p.p.slice(-24)+':'+(p.k?p.k.c+'/'+p.k.s:'');
  if(wPost.k===key)return wPost.b64;if(wPost.busy===key)return wPost.b64;wPost.busy=key;
  const load=u=>new Promise(r=>{if(!u){r(null);return;}const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=u;});
  const pk=pcPeek(p);
  Promise.all([load(pcURL(p.p,p.r)),load(pk?spriteURL(pk.c):'')]).then(([im,sp])=>{
    if(!im){wPost.busy='';return;}
    const cv=document.createElement('canvas');cv.width=288;cv.height=216;const x=cv.getContext('2d');x.imageSmoothingEnabled=false;x.drawImage(im,0,0,288,216);
    if(sp){const z=128,y=216-z+30;if(pk.s){x.save();x.translate(288-9,0);x.scale(-1,1);x.drawImage(sp,0,y,z,z);x.restore();}else x.drawImage(sp,9,y,z,z);}
    wPost={k:key,b64:cv.toDataURL('image/png').split(',')[1],busy:''};wLast='';widgetSync();});
  return wPost.b64;}""")
rep("    const key=JSON.stringify(snap)+'|'+ckey(c);","    snap.post=postForWidget();\n    const key=JSON.stringify(snap)+'|'+ckey(c);")

css="""
/* 0.66: a Forgeling peeks into the postcard */
.pcwin{position:relative;display:block;overflow:hidden;line-height:0;border-radius:1px}
.pcard img.pcpeek{position:absolute;bottom:-14%;width:42%;height:auto;image-rendering:pixelated;filter:drop-shadow(0 0 1px rgba(255,248,234,.9))}
.pcard img.pcpeek.l{left:3%}.pcard img.pcpeek.r{right:3%;transform:scaleX(-1)}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk66.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk66.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
