# 0.58: accessibility (Hunter, November 12: "Please prioritize and execute the additions"; first of five).
#   Text size: Settings > Look and feel > Text size (Phone setting / Standard / Larger / Largest). It scales text only
#   (text-size-adjust), never the layout, so games and the map keep working. "Phone setting" follows the iPhone's
#   text size (the system body font's size); Android's web view follows the phone's font size by itself.
#   Forgeling descriptions: each Forgeling now has a spoken description built from its own shape, colour, ears or
#   horns, eyes, mouth, wings, crown and keepsake ("Hazrin, Common: a round-bodied Forgeling in soft lavender, with long
#   bunny ears, big eyes and a little smile."). The card art reads it, and the buttons that open a Forgeling say a
#   short form. Every piece is its own text, so it is translated.
import re,subprocess,os
S=open('base572.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.57.2'","const VERSION='prototype 0.58.0'")
rep("<title>Forgelings (prototype 0.57.2)</title>","<title>Forgelings (prototype 0.58.0)</title>")

# ---------- descriptions ----------
rep("function keepName(k){","""/* 0.58: a spoken description of a Forgeling, built from what it is drawn from */
const FLD={
  shape:{round:'round-bodied',tall:'tall and slim',wide:'wide and squat',chonk:'big and chunky',pear:'pear-shaped',drop:'droplet-shaped',loaf:'loaf-shaped',blob:'soft and blobby',noodle:'long and noodly',mush:'mushroom-shaped',
    hulk:'big and hulking',wraith:'wispy, wraith-like',beast:'beast-like, heavy-set',shard:'sharp and crystalline',imp:'small and impish',slink:'long and slinking',tower:'tall and towering'},
  ears:{pointy:'pointy ears',round:'round ears',bunny:'long bunny ears',nubs:'little nub ears',antenna:'a pair of antennae',tuft:'tufted ears',floppy:'floppy ears'},
  horns:{up:'upright horns',ram:'curled ram horns',crown:'a crown of horns'},
  eyes:{big:'big eyes',round:'round eyes',dot:'tiny dot eyes',sleepy:'sleepy eyes',happy:'happy curved eyes',sparkle:'sparkling eyes',bean:'bean-shaped eyes',wink:'a cheeky wink',line:'calm line eyes',
    glare:'glaring eyes',slit:'slit-pupil eyes',hollow:'hollow eyes',cyclops:'a single great eye',many:'many small eyes',void:'dark void eyes'},
  mouth:{smile:'a little smile',cat:'a cat-like mouth',open:'an open smile',tiny:'a tiny mouth',fang:'one small fang',o:'an O-shaped mouth',wavy:'a wavy mouth',flat:'a flat little mouth',tongue:'a poking-out tongue',
    fangs:'bared fangs',grin:'a wide grin',maw:'a gaping maw',snarl:'a curled snarl',stitch:'a stitched mouth',tusks:'two tusks'}};
const FLD_COL={red:['soft red','deep red'],orange:['warm orange','burnt orange'],yellow:['golden yellow','dark gold'],green:['leafy green','deep green'],teal:['soft teal','deep teal'],
  blue:['sky blue','deep blue'],purple:['soft lavender','deep purple'],pink:['rose pink','deep plum'],brown:['warm brown','dark brown'],grey:['pale grey','charcoal grey']};
const FLD_PALE={red:'pale coral',orange:'pale peach',yellow:'creamy yellow',green:'pale mint',teal:'pale aqua',blue:'icy blue',purple:'pale lilac',pink:'blush pink'};
function flColour(hex){
  const n=parseInt(String(hex).replace('#',''),16);if(!Number.isFinite(n))return FLD_COL.grey[0];
  const r=(n>>16&255)/255,g=(n>>8&255)/255,b=(n&255)/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),l=(mx+mn)/2,d=mx-mn;
  const sat=d===0?0:d/(1-Math.abs(2*l-1));let h=0;
  if(d){h=mx===r?((g-b)/d)%6:mx===g?(b-r)/d+2:(r-g)/d+4;h=(h*60+360)%360;}
  const dark=l<.4?1:0;
  if(sat<.18)return FLD_COL.grey[dark];
  if(h>=15&&h<45&&l<.45)return FLD_COL.brown[dark];
  const k=h<15||h>=345?'red':h<40?'orange':h<65?'yellow':h<160?'green':h<195?'teal':h<250?'blue':h<300?'purple':'pink';
  return l>.8?FLD_PALE[k]:FLD_COL[k][dark];}
function flParts(c){
  let sp=null;try{sp=genSpec(c);}catch(e){}
  if(!sp)return null;
  const top=sp.dark?FLD.horns[sp.horns]:(sp.ears&&sp.ears!=='none'?FLD.ears[sp.ears]:'');
  return {col:flColour(sp.body),shape:FLD.shape[sp.shape]||'',a:top||'',b:FLD.eyes[sp.eyes]||'',m:FLD.mouth[sp.mouth]||'',wings:!!sp.wings,crown:!!sp.crown};}
function flShort(c){const p=flParts(c);if(!p||!p.shape)return '';return `A ${p.shape} Forgeling in ${p.col}.`;}
function flDesc(c){
  const p=flParts(c),n=c.nick||c.name,R=RAR[c.rarity]?RAR[c.rarity].name:'';
  if(!p||!p.shape)return `${n}, a Forgeling.`;
  let out=p.a?`${n}, ${R}: a ${p.shape} Forgeling in ${p.col}, with ${p.a}, ${p.b} and ${p.m}.`:`${n}, ${R}: a ${p.shape} Forgeling in ${p.col}, with ${p.b} and ${p.m}.`;
  if(p.wings)out+=' '+'It has small wings.';
  if(p.crown)out+=' '+'It wears a little crown.';
  if(c.keep)out+=' '+`It is wearing the ${keepName(c.keep).toLowerCase()}.`;
  return out;}
function lookLabel(c){const n=c.nick?`${c.nick} (${c.name})`:c.name,R=RAR[c.rarity]?RAR[c.rarity].name:'';return `Look at ${n}, ${R}. ${flShort(c)}`;}
function keepName(k){""")
rep("""<canvas class="pcv" width="48" height="37" data-k="${ckey(cc)}" aria-label="${esc(c.name)}, a ${R.name} ${dk?'dark':'cute'} Forgeling"></canvas>""",
    """<canvas class="pcv" width="48" height="37" data-k="${ckey(cc)}" role="img" aria-label="${esc(flDesc(c))}"></canvas>""")
rep('''aria-label="Look at ${esc(c.nick||c.name)}"''','''aria-label="${esc(lookLabel(c))}"''',3)
rep('''aria-label="Look at ${c.nick?esc(c.nick)+' ('+esc(c.name)+')':esc(c.name)}, ${RAR[c.rarity].name}"''','''aria-label="${esc(lookLabel(c))}"''')
rep('''<button class="herocard" id="btnShowFav" aria-label="Look at ${fn}">''','''<button class="herocard" id="btnShowFav" aria-label="${esc(lookLabel(f))}">''')

# ---------- text size ----------
rep("function applySettings(){","""/* 0.58: text size. Text only (text-size-adjust), never the layout. 'auto' follows the iPhone's text size. */
const TSIZE={std:100,l:115,xl:130};
function sysTextPct(){try{const d=document.createElement('div');d.style.cssText='position:absolute;visibility:hidden;font:-apple-system-body';
    if(!d.style.font)return 100;document.body.appendChild(d);const f=parseFloat(getComputedStyle(d).fontSize);d.remove();
    return Number.isFinite(f)&&f>0?Math.round(Math.min(160,Math.max(100,f/17*100))):100;}catch(e){return 100;}}
function applyTextSize(){const t=state&&state.settings&&state.settings.tsize,p=TSIZE[t]||sysTextPct(),h=document.documentElement;
  h.style.webkitTextSizeAdjust=h.style.textSizeAdjust=p+'%';h.classList.toggle('bigtext',p>=115);}
function applySettings(){applyTextSize();""")
rep("""<div class="lbl2">Forgeling mood</div><p class="muted small">Which Forgelings you find""",
"""<div class="lbl2">Text size</div><div class="chips" role="group" aria-label="Text size">${[['auto','Phone setting'],['std','Standard'],['l','Larger'],['xl','Largest']].map(a=>`<button class="chip" data-tsize="${a[0]}" aria-pressed="${(TSIZE[S.tsize]?S.tsize:'auto')===a[0]}">${a[1]}</button>`).join('')}</div><div class="lbl2">Forgeling mood</div><p class="muted small">Which Forgelings you find""")
rep("""  else if(b.dataset.setmood){state.settings.mood=b.dataset.setmood;""",
"""  else if(b.dataset.tsize){state.settings.tsize=b.dataset.tsize;save();applyTextSize();renderSettings();}
  else if(b.dataset.setmood){state.settings.mood=b.dataset.setmood;""")
# larger text: let fixed one-line rows wrap
i=S.rindex("</style>",0,S.index("<body"));S=S[:i]+"""
/* 0.58: larger text wraps instead of clipping */
html.bigtext .chip,html.bigtext .pill{white-space:normal;height:auto}
html.bigtext .rowl .rs,html.bigtext .rowl b{white-space:normal}
"""+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk58.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk58.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
