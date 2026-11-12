# 0.57.1: Japanese follow-ups (Hunter, November 12).
#   "on the Home Screen it still says 'good, easy, hard' for your daily task": the How did it feel? faces showed their
#   save keys (easy/good/hard) as labels, and the lines that repeat a feeling ("Today felt good.", "It felt hard that
#   day.", "Felt easy.") spliced the key in. Each is now a whole text of its own (FEEL_L, FEEL_TODAY, FEEL_DAY,
#   FEEL_SHORT), so it can be translated; the saved keys are unchanged.
#   "Katakana names for the forgelings would be a great addition": a Forgeling's name is a first and a last syllable
#   (PRE+SUF, PRE_D+SUF_D). In Japanese each syllable has a katakana reading, so Hazrin shows as ハズリン. The save keeps
#   the Latin name (a card's toJSON writes it back), links and backups carry it, and English shows it as before.
#   Nicknames are shown as typed. A name that is not two known syllables stays as it is. The binder's name search finds
#   both spellings.
import re,subprocess,os
S=open('base57.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.57.0'","const VERSION='prototype 0.57.1'")
rep("<title>Forgelings (prototype 0.57.0)</title>","<title>Forgelings (prototype 0.57.1)</title>")

# feelings: whole words and sentences for each saved key
rep("const FEELS=['easy','good','hard'];","""const FEELS=['easy','good','hard'];
/* 0.57.1: what each feeling says (the keys above are what the save keeps) */
const FEEL_L={easy:'Easy',good:'Good',hard:'Hard'};
const FEEL_TODAY={easy:'Today felt easy.',good:'Today felt good.',hard:'Today felt hard.'};
const FEEL_DAY={easy:'It felt easy that day.',good:'It felt good that day.',hard:'It felt hard that day.'};
const FEEL_SHORT={easy:'Felt easy.',good:'Felt good.',hard:'Felt hard.'};""")
rep("""${fl?'Today felt '+fl+'.':'How did it feel?'}""","""${fl&&FEEL_TODAY[fl]?FEEL_TODAY[fl]:'How did it feel?'}""")
rep("""<span>${f[0].toUpperCase()+f.slice(1)}</span>""","""<span>${FEEL_L[f]}</span>""")
rep("""${(state.feel||{})[k]?`<p class="muted small center">It felt ${state.feel[k]} that day.</p>`:''}""",
    """${FEEL_DAY[(state.feel||{})[k]]?`<p class="muted small center">${FEEL_DAY[state.feel[k]]}</p>`:''}""")
rep("""${f?`<p class="muted small feelc">Felt ${f}.</p>`:''}""","""${FEEL_SHORT[f]?`<p class="muted small feelc">${FEEL_SHORT[f]}</p>`:''}""")

# katakana names
rep("const PRE_D=[","""/* 0.57.1: katakana readings of the name syllables, used when the app runs in Japanese */
const KANA_P={Mo:'モ',Pip:'ピップ',Nim:'ニム',Bru:'ブル',Ket:'ケット',Lum:'ルム',Zo:'ゾ',Wob:'ウォブ',Fen:'フェン',Tam:'タム',Orri:'オリ',Sal:'サル',Jun:'ジュン',Bix:'ビックス',Quill:'クイル',Dov:'ドヴ',Haz:'ハズ',Miro:'ミロ',Tuck:'タック',Yara:'ヤラ',
  Gor:'ゴル',Vex:'ヴェクス',Mor:'モル',Nox:'ノクス',Skar:'スカー',Ur:'ウル',Zul:'ズール',Krag:'クラグ',Vor:'ヴォル',Grim:'グリム',Thul:'スール',Bael:'バエル'};
const KANA_S={bo:'ボ',ko:'コ',ly:'リー',nix:'ニックス',wick:'ウィック',ble:'ブル',mer:'マー',dle:'ドル',rin:'リン',tuft:'タフト',pa:'パ',zle:'ズル',ton:'トン',fin:'フィン',bell:'ベル',mo:'モ',
  gash:'ガッシュ',thorn:'ソーン',maw:'モー',wraith:'レイス',fang:'ファング',dread:'ドレッド',bane:'ベイン',moth:'モス',skull:'スカル',rot:'ロット',vyr:'ヴィル',kra:'クラ'};
function kanaName(n){
  for(const p in KANA_P){if(!n.startsWith(p))continue;const r=n.slice(p.length);if(!KANA_S[r])continue;
    let a=KANA_P[p];if(/ム$/.test(a)&&/^[bpm]/.test(r))a=a.slice(0,-1)+'ン';return a+KANA_S[r];}
  return n;}
/* in Japanese a card's name reads in katakana; the save, links and backups keep the Latin name */
function jaName(c){
  if(!(typeof LANG!=='undefined'&&LANG==='ja')||!c||typeof c.name!=='string'||Object.getOwnPropertyDescriptor(c,'nameEn'))return c;
  let v=c.name;
  Object.defineProperty(c,'name',{get:()=>kanaName(v),set:x=>{v=x;},enumerable:true,configurable:true});
  Object.defineProperty(c,'nameEn',{get:()=>v,enumerable:false,configurable:true});
  Object.defineProperty(c,'toJSON',{value:function(){const o=Object.assign({},this);o.name=v;return o;},enumerable:false,configurable:true});
  return c;}
const PRE_D=[""")
rep("""    top=Math.max(top,c.id);return c;});""","""    top=Math.max(top,c.id);return jaName(c);});""")
m=re.search(r"\n  return \{id:state\.nextId\+\+,seed,[\s\S]*?gen:2\};\n\}",S); assert m
blk=m.group(0); S=S.replace(blk,blk.replace("\n  return {id:state.nextId++","\n  return jaName({id:state.nextId++").replace("gen:2};\n}","gen:2});\n}"))
rep("""((c.nick||'')+' '+c.name).toLowerCase().includes(bf.q.toLowerCase())""","""((c.nick||'')+' '+c.name+' '+(c.nameEn||'')).toLowerCase().includes(bf.q.toLowerCase())""")

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk571.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk571.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
