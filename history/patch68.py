# 0.68: postcards from the road, and On this day (brainstorm plan, ideas 4 and 5).
#   Road: halfway through a wander, the Forgeling sends a postcard: a little drawn scene of where it is, and a note in
#   its own voice (bright or dark), tied to which way your answers lean ("You said you needed rest, so I am walking
#   slowly"). It shows on the wander sheet and the Hearth's wander panel, and Today says one came. When the Forgeling
#   is back, the postcard goes on the postcard wall with the others. Composed when shown, from the wander's seed.
#   On this day: when you have a page from exactly a year ago (or, failing that, a month ago), Today offers it once
#   that day: the page's words, your own words and its postcard.
#   Save: pcGifts entries may carry t:1 (from the road) and l (the lean); state.otd = the date it was opened.
import re,subprocess,os
S=open('base67.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.67.0'","const VERSION='prototype 0.68.0'")
rep("<title>Forgelings (prototype 0.67.0)</title>","<title>Forgelings (prototype 0.68.0)</title>")

rep("function todayTask(){","""/* ================= 0.68: postcards from the road ================= */
const ROAD_N=[['The grass here is taller than me. I am fine. I am having a wonderful time.','I found a hill with exactly one tree on it. I sat under it for a while.'],
  ['It is warm here. I found a spot by a vent and had a little nap.','Someone here was forging tiny bells. I listened for a long time.'],
  ['I found a tide pool with a very small crab in it. We are friends now.','The waves keep bringing me shells. I can only carry three.'],
  ['I made one footprint in perfect snow and then stood very still to admire it.','My breath makes little clouds here. I have been making a lot of them.'],
  ['The stars came out early just for me, I think.','I followed a firefly until it followed me back.']];
const ROAD_D=[['The brambles tried to keep me. They did not succeed.','The thorns here know my name now.'],
  ['The ground here hums. I like it more than I should.','I watched the lava for an hour. It did not blink first.'],
  ['The water here is deep and quiet. I did not go in. Mostly.','Something under the waves followed me along the shore. It was polite about it.'],
  ['The cold here is sharp and honest. I respect it.','The wind howled at me. I howled back.'],
  ['Something in the dark said hello. I said hello back.','There are no stars here tonight. I brought my own.']];
const ROAD_TIE=['You said people made your day, so I am waving at everyone I pass.','You have been in a making mood, so I am bringing back something to tinker with.','You said you needed rest, so I am walking slowly and stopping often.','You wanted a clear head, so I took the quietest path I could find.','You were somewhere far away, dreaming, so I followed the strangest trail.'];
const ROAD_TIE_D=['You said people mattered today. I nodded at everyone I passed.','You wanted to make things. I am bringing back something sharp to work with.','You needed rest. I am taking the slow road, for you.','You wanted a clear head. I took the coldest, quietest path.','You were dreaming. I followed the trail no one else takes.'];
const roadR=w=>w.realm>=0?w.realm%5:w.lean>=0&&w.lean<=4?w.lean:(w.seed>>>3)%5;
const roadHalf=w=>!!(w&&Date.now()>=w.start+(w.ready-w.start)/2);
function roadNote(c,r,seed,lean){const L=(c&&c.dark?ROAD_D:ROAD_N)[r],t=L[(seed>>>5)%L.length];return lean>=0&&lean<=4?(t+' '+(c&&c.dark?ROAD_TIE_D:ROAD_TIE)[lean]).replace(/([。！？]) /g,'$1'):t;}
function roadHTML(){
  const w=state.wander,c=w?cardById(w.id):null;if(!c||!roadHalf(w))return '';
  const r=roadR(w),n=c.nick||c.name,g={d:todayKey(),r,s:(w.seed%2147483646)+1,c:c.id};
  return `<div class="road"><p class="muted small" style="margin:0 0 6px">A postcard from the road</p><figure class="pcard gift"><img src="${giftURL(g)}" alt="A drawing of ${pcRealm(r)}, sent by ${esc(n)}" width="${PC_W*3}" height="${PC_H*3}"><figcaption>${esc(roadNote(c,r,w.seed%2147483646,w.lean))}</figcaption></figure><p class="small" style="margin:6px 0 0;text-align:right">— ${esc(n)}</p></div>`;}
/* ================= 0.68: On this day ================= */
function otdKey(){const t=todayKey(),d=new Date(t+'T00:00:00'),y=new Date(d);y.setFullYear(d.getFullYear()-1);const m=new Date(d);m.setMonth(d.getMonth()-1);
  const E=entryDays(),yk=dkey(y),mk=dkey(m);if(E.has(yk)&&yk.slice(5)===t.slice(5))return {k:yk,y:1};if(E.has(mk)&&mk.slice(8)===t.slice(8))return {k:mk,y:0};return null;}
function openOldPage(k,lead){
  const w=entryLine(k),j=state.journal[k]&&state.journal[k].text?state.journal[k].text:'';
  openSheet(`<p class="muted center small">${lead}</p><h2 class="center">${esc(dateLabel(k))}</h2>${(state.posts||{})[k]?`<div class="center">${pcFig(k,state.posts[k])}</div>`:''}${w?`<p class="world entry" style="margin:12px 0 6px">${esc(w)}</p>`:''}${j?`<p class="mine" style="margin:6px 0 12px">“${esc(j)}”</p>`:''}${FEEL_DAY[(state.feel||{})[k]]&&!w?`<p class="muted small center">${FEEL_DAY[state.feel[k]]}</p>`:''}<div class="stack"><button class="primary" data-close>Close the book</button></div>`);}
function todayTask(){""")

# where it shows while they wander
rep("""    return `<h2>${wn} is out wandering${w.realm>=0?' in '+esc(rName(w.realm)):''}</h2><p class="muted small">Back in ${wLeftText()}. There is no rush. If you are away, they will wait by the fire.</p>""",
    """    return `<h2>${wn} is out wandering${w.realm>=0?' in '+esc(rName(w.realm)):''}</h2><p class="muted small">Back in ${wLeftText()}. There is no rush. If you are away, they will wait by the fire.</p>${roadHTML()}""")
rep("""There is no rush. If you are away, they will wait by the fire.</p>${fgMade('bell')?(fgState().bell===todayKey()?'<p class="muted small">The bell has rung today.</p>':'<button class="outline" id="hBell" style="margin-""",
    """There is no rush. If you are away, they will wait by the fire.</p>${roadHTML()}${fgMade('bell')?(fgState().bell===todayKey()?'<p class="muted small">The bell has rung today.</p>':'<button class="outline" id="hBell" style="margin-""")
rep("const ms=wo&&wOut()?`Back in ${wLeftText()}. `+","const ms=wo&&wOut()?`Back in ${wLeftText()}. `+(roadHalf(state.wander)?'A postcard came from the road. ':'')+")
# it goes on the wall when they are back
rep("  state.wstat.back++;state.wander=null;","""  if(c){const rr=roadR(w);state.pcGifts=(state.pcGifts||[]).concat([{d:todayKey(),r:rr,s:(w.seed%2147483646)+1,c:c.id,t:1,l:w.lean>=0&&w.lean<=4?w.lean:-1}]).slice(-200);}
  state.wstat.back++;state.wander=null;""")
rep("s.pcGifts=(Array.isArray(s.pcGifts)?s.pcGifts:[]).filter(g=>g&&typeof g.d==='string'&&DK.test(g.d)&&Number.isInteger(g.r)&&g.r>=0&&g.r<=4&&Number.isInteger(g.s)).slice(-200).map(g=>({d:g.d,r:g.r,s:g.s,c:Number.isFinite(g.c)?g.c:-1}));",
    "s.pcGifts=(Array.isArray(s.pcGifts)?s.pcGifts:[]).filter(g=>g&&typeof g.d==='string'&&DK.test(g.d)&&Number.isInteger(g.r)&&g.r>=0&&g.r<=4&&Number.isInteger(g.s)).slice(-200).map(g=>Object.assign({d:g.d,r:g.r,s:g.s,c:Number.isFinite(g.c)?g.c:-1},g.t===1?{t:1,l:Number.isInteger(g.l)&&g.l>=0&&g.l<=4?g.l:-1}:{}));\n   s.otd=typeof s.otd==='string'&&DK.test(s.otd)?s.otd:'';")
# the wall: road postcards carry their note
rep("""<figcaption>From ${esc(n)}, ${rn}</figcaption></figure>`;}""","""<figcaption>${g.t===1?`${esc(roadNote(cardById(g.c),g.r,g.s-1,g.l))} — ${esc(n)}`:`From ${esc(n)}, ${rn}`}</figcaption></figure>`;}""")
rep("Every fifth postcard you make, one of them comes back with a postcard of its own. They stay on this device.","Every fifth postcard you make, one of them comes back with a postcard of its own, and they send one from the road when they wander. They stay on this device.")
# On this day, on Today
rep("  letterCheck();{","""  {const o=otdKey();if(o&&state.otd!==todayKey())rows.unshift(row('btnOtd',IC.pack,'On this day',o.y?'A year ago today, you wrote a page. Have a look.':'A month ago today, you wrote a page. Have a look.','',true));}
  letterCheck();{""")
rep("  else if(b.id==='btnLetter'){","""  else if(b.id==='btnOtd'){const o=otdKey();if(o){state.otd=todayKey();save();renderToday();openOldPage(o.k,o.y?'A year ago today':'A month ago today');}}
  else if(b.id==='btnLetter'){""")
css="""
/* 0.68: postcards from the road */
.road{margin:12px 0 4px;text-align:center}.road .pcard{width:100%;max-width:280px;text-align:left}.road .pcard img{width:100%}
.road .pcard figcaption{padding-right:0;font-size:13px;line-height:1.45}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk68.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk68.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
