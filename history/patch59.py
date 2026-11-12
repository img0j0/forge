# 0.59: seasons (Hunter, November 12: "Please prioritize and execute the additions"; second of five).
#   Seven short seasons on the real calendar, the same for everyone: First Lanterns (Dec 31 - Jan 6), Blossom Days
#   (Mar 25 - Apr 10), Firefly Evenings (Jun 8 - 22), Star Wishes (Jul 1 - 7), Moon Viewing (Sep 12 - 26), Maple Days
#   (Nov 5 - 22) and First Snow (Dec 8 - 24). During a season its weather drifts over the Hearth (petals, fireflies,
#   leaves, snow...; still, not moving, when motion is reduced), Today shows a row for it, and turning over a card during it
#   presses that season's stamp into your journal, once a year each. Missing a season costs nothing: it comes back next
#   year. The Seasons sheet (from the row, or the Journal's Seasons button) shows every stamp you have pressed.
#   Also: Today's "The Map" row checked for English text ('Today,'), so it never showed in Japanese; it now asks the world
#   calendar whether something happened today.
import re,subprocess,os
S=open('base58.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.58.0'","const VERSION='prototype 0.59.0'")
rep("<title>Forgelings (prototype 0.58.0)</title>","<title>Forgelings (prototype 0.59.0)</title>")

rep("if(ml.startsWith('Today,'))rows.push(row('btnMapGo'","if(ml&&worldEvent(dnum(todayKey())))rows.push(row('btnMapGo'")

# the back of the map's title lines, as their own text (like the front's in 0.57)
rep('''>The other side, by lantern light</text>''','''>${'The other side, by lantern light'}</text>''')
rep('''font-size="10">Turned over in the ${esc(era.n)}</text>''','''font-size="10">${`Turned over in the ${esc(era.n)}`}</text>''')
# ---------- the seasons ----------
rep("/* ================= Cards ================= */","""/* ================= 0.59: seasons ================= */
/* from/to are month-day; a season that wraps the new year belongs to the year it starts in.
   px: the weather over the Hearth (colours of its little pieces, and how they move). st: its stamp, 12x12 pixels. */
const SEASONS=[
 {id:'lantern',from:'12-31',to:'01-06',name:'First Lanterns',line:'Paper lanterns rise over the fire to start the year.',px:['#FFD36B','#FF9F43','#FFE9A8'],mv:'rise',
  st:['....aaaa....','...abbbba...','..abbccbba..','..abccccba..','..abccccba..','..abbccbba..','...abbbba...','....aaaa....','.....dd.....','.....dd.....','............','............'],sc:{a:'#C9772E',b:'#FFB04A',c:'#FFE9A8',d:'#8A5A2B'}},
 {id:'blossom',from:'03-25',to:'04-10',name:'Blossom Days',line:'Blossom petals drift down over the Hearth.',px:['#F7C6D9','#F29BB5','#FFE4EE'],mv:'fall',
  st:['.....aa.....','....abba....','.aa.abba.aa.','abbaabbaabba','abbbbccbbbba','.abbccccbba.','..abccccba..','.abbbccbbba.','abbaabbaabba','.aa.abba.aa.','....abba....','.....aa.....'],sc:{a:'#C9608A',b:'#F7B8CF',c:'#FFE58A'}},
 {id:'firefly',from:'06-08',to:'06-22',name:'Firefly Evenings',line:'Fireflies blink in the grass around the fire.',px:['#E9FF8A','#FFF6B0','#C8F06A'],mv:'blink',
  st:['............','....a..a....','.....aa.....','...bbaabb...','..bcbaabcb..','..bcbaabcb..','...bbaabb...','.....dd.....','.....ee.....','....eeee....','.....ee.....','............'],sc:{a:'#3A3550',b:'#B9D8F0',c:'#E6F4FF',d:'#5A5370',e:'#E9FF6A'}},
 {id:'star',from:'07-01',to:'07-07',name:'Star Wishes',line:'Stars come out early, and every Forgeling makes a wish.',px:['#FFFFFF','#FFE08A','#B9A6FF'],mv:'twinkle',
  st:['.....aa.....','.....aa.....','....abba....','aaaabbbbaaaa','.aabbccbbaa.','..abbccbba..','..abbbbbba..','.abbaaaabba.','.aba....aba.','.aa......aa.','............','............'],sc:{a:'#C9962E',b:'#FFD36B',c:'#FFF4C2'}},
 {id:'moon',from:'09-12',to:'09-26',name:'Moon Viewing',line:'A big harvest moon sits over the Hearth.',px:['#FFF4C2','#FFE08A','#E8E0CC'],mv:'moon',
  st:['....aaaa....','..aabbbbaa..','.abbbbbbbba.','.abbcbbbbba.','abbbbbbcbbba','abbbbbbbbbba','abcbbbbbbbba','abbbbbcbbbba','.abbbbbbbba.','.aabbbbbbaa.','..aaabbaaa..','....aaaa....'],sc:{a:'#C9A24A',b:'#FFEFB0',c:'#E8D28A'}},
 {id:'maple',from:'11-05',to:'11-22',name:'Maple Days',line:'Red and gold leaves tumble past the fire.',px:['#E2562E','#F29B3A','#C9302C','#F5C04A'],mv:'fall',
  st:['.....aa.....','....abba....','.a..abba..a.','.ab.abba.ba.','.abbabbabba.','..abbbbbba..','aabbbbbbbbaa','.abbbbbbbba.','..aabbbbaa..','....aaaa....','.....cc.....','.....cc.....'],sc:{a:'#9E2A1E',b:'#E2562E',c:'#7A4A22'}},
 {id:'snow',from:'12-08',to:'12-24',name:'First Snow',line:'The first snow falls softly around the Hearth.',px:['#FFFFFF','#E6F0FF','#CFE0F5'],mv:'fall',
  st:['.....aa.....','..a..aa..a..','...a.aa.a...','....aaaa....','.aaaabbaaaa.','aa..abba..aa','aa..abba..aa','.aaaabbaaaa.','....aaaa....','...a.aa.a...','..a..aa..a..','.....aa.....'],sc:{a:'#8FB4E0',b:'#FFFFFF'}}];
/* the season today (with the year it belongs to), or null */
function seasonNow(k){k=k||todayKey();const md=k.slice(5),y=+k.slice(0,4);
  for(const s of SEASONS){const wrap=s.from>s.to,inS=wrap?(md>=s.from||md<=s.to):(md>=s.from&&md<=s.to);
    if(inS)return {s,y:wrap&&md<=s.to?y-1:y};}
  return null;}
const seasonKey=n=>n.s.id+'-'+n.y;
function seasonStampSVG(s,px,on){const W=12,c=s.sc;let r='';s.st.forEach((row,y)=>{for(let x=0;x<W;x++){const ch=row[x];if(ch&&ch!=='.')r+=`<rect x="${x}" y="${y}" width="1" height="1" fill="${on?c[ch]:'#B9B0A0'}"/>`;}});
  return `<svg viewBox="0 0 12 12" width="${px}" height="${px}" shape-rendering="crispEdges" aria-hidden="true" style="opacity:${on?1:.45}">${r}</svg>`;}
const seasonEnd=n=>{const [m,d]=n.s.to.split('-').map(Number);return dateLabel(dkey(new Date(n.s.from>n.s.to?n.y+1:n.y,m-1,d)));};
/* pressed when today's card is turned over during the season */
function seasonPress(){const n=seasonNow();if(!n)return false;state.seasons=state.seasons||{};const k=seasonKey(n);if(state.seasons[k])return false;state.seasons[k]=state.date;return true;}
/* the weather over the Hearth: little pieces placed by a fixed pattern, so it looks the same each visit */
function seasonFX(){const n=seasonNow();if(!n)return '';const s=n.s,N=s.mv==='moon'?6:s.mv==='blink'?12:16;let out='';
  for(let i=0;i<N;i++){const h=whash(i*7919+s.id.length*31),x=h%96+2,y=(h>>7)%80+4,d=6+(h>>11)%7,dl=-((h>>5)%9),col=s.px[i%s.px.length],sz=s.mv==='twinkle'?2:s.mv==='blink'?3:5;
    out+=`<i style="left:${x}%;--y:${y}%;width:${sz}px;height:${sz}px;background:${col};animation-duration:${d}s;animation-delay:${dl}s"></i>`;}
  if(s.mv==='moon')out='<b class="sfxmoon"></b>'+out;
  return `<div class="sfx sfx-${s.mv}" aria-hidden="true">${out}</div>`;}
function seasonsHTML(){const have=state.seasons||{},n=seasonNow();
  const items=SEASONS.map(s=>{const got=Object.keys(have).filter(k=>k.startsWith(s.id+'-')).sort(),on=got.length>0,cur=n&&n.s.id===s.id;
    const md=x=>{const [m,d]=x.split('-').map(Number);return new Date(2026,m-1,d).toLocaleDateString(LOC(),{month:'short',day:'numeric'});},when=`${md(s.from)} to ${md(s.to)}`;
    return `<li class="sseason${cur?' now':''}">${seasonStampSVG(s,40,on)}<span><b>${s.name}</b><small>${s.line}</small><small class="muted">${when}${on?' · '+(got.length===1?'Pressed once':`Pressed ${got.length} times`):''}</small></span></li>`;}).join('');
  const k=Object.keys(have).length;
  return `<div class="csheet" data-k="seasons"><h2>Seasons</h2><p class="muted small">${k?`${k} ${k===1?'stamp':'stamps'} pressed into your journal.`:'No stamps yet.'} Turn over a card during a season to press its stamp. Missing one costs nothing: every season comes back next year.</p><ul class="seasons">${items}</ul><div class="stack"><button class="ghost" data-close>Close</button></div></div>`;}
/* ================= Cards ================= */""")

# Today: the season row
rep("""  {const ml=state.cards.length&&state.settings.lore!==false?mapLatest():'';""","""  {const n=seasonNow();if(n&&state.cards.length){const got=state.seasons&&state.seasons[seasonKey(n)];
    rows.unshift(row('btnSeason',seasonStampSVG(n.s,24,!!got),n.s.name,got?`Its stamp is pressed into your journal. Until ${seasonEnd(n)}.`:`${n.s.line} Turn over today's card to press its stamp. Until ${seasonEnd(n)}.`,'',!got&&s==='done'));}}
  {const ml=state.cards.length&&state.settings.lore!==false?mapLatest():'';""")
rep("""  else if(b.id==='btnMapGo'){""","""  else if(b.id==='btnSeason'){openSheet(seasonsHTML());}
  else if(b.id==='btnMapGo'){""")
# pressed when the card is done
rep("""  state.cards.push(c);state.todayCard=c.id;state.status='done';""","""  state.cards.push(c);state.todayCard=c.id;state.status='done';seasonPress();""")
# the Hearth's weather
n=S.count('<div class="hearthwrap"><canvas id="hearthCv"'); assert n==2,n
S=S.replace('role="img" aria-label="Your Forgelings sitting around a campfire"></canvas></div>','role="img" aria-label="Your Forgelings sitting around a campfire"></canvas>${seasonFX()}</div>')
rep('''<button class="chip" id="jWeek">This week</button>${''','''<button class="chip" id="jWeek">This week</button><button class="chip" id="jSeasons">Seasons</button>${''')
rep('''  if(e.target.closest('#jWeek')){''','''  if(e.target.closest('#jSeasons')){openCSheet(seasonsHTML());return;}
  if(e.target.closest('#jWeek')){''')
# the save: seasons is a map of season-year -> date
rep("""  if(s.mEchoed!==undefined&&!Array.isArray(s.mEchoed))s.mEchoed=[];""","""  if(s.mEchoed!==undefined&&!Array.isArray(s.mEchoed))s.mEchoed=[];
  if(s.seasons!==undefined){if(!s.seasons||typeof s.seasons!=='object'||Array.isArray(s.seasons))s.seasons={};else Object.keys(s.seasons).forEach(k=>{if(!/^[a-z]+-\\d{4}$/.test(k)||typeof s.seasons[k]!=='string')delete s.seasons[k];});}""")

css="""
/* 0.59: seasons */
.hearthwrap{position:relative}
.sfx{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:1}
.sfx i{position:absolute;top:var(--y);display:block;image-rendering:pixelated}
.sfx-fall i{top:-6%;animation:sfxFall linear infinite}
.sfx-rise i{top:auto;bottom:-6%;animation:sfxRise linear infinite;box-shadow:0 0 6px rgba(255,200,90,.8)}
.sfx-blink i{animation:sfxBlink ease-in-out infinite;box-shadow:0 0 6px currentColor;border-radius:50%}
.sfx-twinkle i,.sfx-moon i{top:calc(var(--y)*.5);animation:sfxBlink ease-in-out infinite}
.sfxmoon{position:absolute;right:9%;top:8%;width:15%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 40% 40%,#FFF8D8,#FFE08A 60%,#E8C46A);box-shadow:0 0 18px rgba(255,230,150,.7)}
@keyframes sfxFall{0%{transform:translate(0,0) rotate(0)}100%{transform:translate(-30px,260px) rotate(300deg)}}
@keyframes sfxRise{0%{transform:translate(0,0);opacity:0}15%{opacity:1}100%{transform:translate(12px,-240px);opacity:0}}
@keyframes sfxBlink{0%,100%{opacity:.15}50%{opacity:1}}
html.reduce .sfx i{animation:none;top:var(--y);bottom:auto;opacity:.85}
ul.seasons{list-style:none;padding:0;margin:8px 0}
.sseason{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px dashed var(--line)}
.sseason.now b::after{content:' \\2022';color:#E2562E}
.sseason span{display:flex;flex-direction:column;gap:2px}.sseason small{font-size:13px;line-height:1.35}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk59.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk59.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
