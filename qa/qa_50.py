from lib import *
# 0.50: the games get little worlds and one new thing each; the game sheet is postcards; your Forgeling reacts; a round
# ends on a journal page; the Map's terrain is drawn, clouds cover what you have not found, and lamplight brings stars.
import time, datetime
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
NAMES=["meadow","ember","tide","frost","dusk"]; TITLES=["Dandelion Drift","Keep the Fire","Skipping Stones","Snowflake Catch","Lantern Lights"]
WATCH="""()=>{window.__seq=[];new MutationObserver(ms=>{for(const m of ms){const t=m.target;if(t.classList&&t.classList.contains('lant')&&t.classList.contains('on')&&document.getElementById('pgMsg').textContent==='Watch.')window.__seq.push(+t.dataset.lant);}}).observe(document.getElementById('pg'),{subtree:true,attributes:true,attributeFilter:['class']});}"""
def card(base,ti,stats=(50,50,50),bond=0,dark=False,used=0,best=None,pressed=0):
    s=build(base,[1 if i==ti else 0 for i in range(5)]); s["seen"]=99; c=s["cards"][0]; c["stats"]=list(stats); c["bond"]=bond; c["dark"]=dark
    s["hearth"]["slots"]=[c["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":used}; s["games"]={"best":best or {},"played":0,"curioDay":"","pressed":pressed}; return s
def ready(pg,s):
    pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click();const d=document.getElementById('pgDone');if(d)d.click()}"); pg.wait_for_timeout(200)
    setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg); tabto(pg,"hearth")
def openg(pg,ti): pg.evaluate("document.getElementById('hPlay').click()"); pg.wait_for_timeout(300); pg.evaluate(f"document.querySelector('#modal [data-game=\"{ti}\"]').click()"); pg.wait_for_timeout(300)
def start(pg): pg.evaluate("document.getElementById('pgGo').click()"); pg.wait_for_timeout(150)
def wait_for(pg,js,ms=9000):
    t0=time.time()
    while (time.time()-t0)*1000<ms:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(80)
    return False
TAP="sel=>{const b=document.querySelector('#pg '+sel);if(b)b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));return !!b}"
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,90))}")
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b,390,844); pg.set_default_timeout(15000); pg.clock.install(time=datetime.datetime(2027,3,3,11,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)

    # ---------- the game sheet: postcards ----------
    ready(pg,card(base,0,best={"meadow":14}))
    pg.evaluate("document.getElementById('hPlay').click()"); pg.wait_for_timeout(400)
    pc=pg.evaluate("[...document.querySelectorAll('#modal [data-game]')].map(b=>({pc:b.classList.contains('pcard'),svg:!!b.querySelector('svg.pcs[aria-hidden=true]'),h:Math.round(b.getBoundingClientRect().height),t:b.innerText}))")
    rec("Sheet","every game is a postcard with a little picture of its world, and stays easy to tap",len(pc)==5 and all(x["pc"] and x["svg"] and x["h"]>=44 for x in pc),pc)
    rec("Sheet","…and your best is written on its postcard","Best: 14 points" in pc[0]["t"],pc[0]["t"])
    closemodals(pg)

    # ---------- every game is played inside its realm's scene ----------
    for ti in range(5):
        ready(pg,card(base,ti)); openg(pg,ti)
        sc=pg.evaluate("()=>{const s=document.querySelector('#pg > svg.pgsc');if(!s)return null;const r=s.getBoundingClientRect(),P=document.getElementById('pg').getBoundingClientRect();return {hid:s.getAttribute('aria-hidden'),z:getComputedStyle(s).zIndex,pe:getComputedStyle(s).pointerEvents,cover:r.width>=P.width-8&&r.height>=P.height-8}}")
        rec("Scene",f"{TITLES[ti]}: played inside a pixel scene of its realm, behind the play and hidden from screen readers",sc and sc["hid"]=="true" and sc["z"]=="-1" and sc["pe"]=="none" and sc["cover"],sc)
        start(pg); pg.wait_for_timeout(600)
        if ti==2: pg.wait_for_timeout(500)
        top=pg.evaluate("()=>{const P=document.getElementById('pg').getBoundingClientRect(),x=P.left+P.width/2,y=P.top+P.height*.45,e=document.elementFromPoint(x,y);return e&&e.closest('svg.pgsc')?'scene':e?e.id||e.className||e.tagName:null}")
        rec("Scene",f"{TITLES[ti]}: the scene never catches a tap",top!="scene",top)
        pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)

    # ---------- Dandelion Drift: swipe, gusts, the dandelion clock ----------
    ready(pg,card(base,0)); openg(pg,0); start(pg)
    wait_for(pg,"(()=>{const P=document.getElementById('pg').getBoundingClientRect();return [...document.querySelectorAll('#pg .seed:not(.caught):not(.gold):not(.thorn)')].filter(e=>{const r=e.getBoundingClientRect();return r.top>P.top+20&&r.bottom<P.bottom-20}).length>=3})()",9000)
    sw=pg.evaluate("""()=>{const P=document.getElementById('pg'),R=P.getBoundingClientRect(),s0=+document.getElementById('pgScore').textContent;
      const ss=[...P.querySelectorAll('.seed:not(.caught):not(.gold):not(.thorn)')].map(e=>{const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+20]}).filter(q=>q[1]>R.top+20&&q[1]<R.bottom-20).slice(0,3);
      const ev=(t,q)=>P.dispatchEvent(new PointerEvent(t,{bubbles:true,pointerId:7,clientX:q[0],clientY:q[1]}));
      ev('pointerdown',[R.left+4,R.top+4]);ss.forEach(q=>ev('pointermove',q));ev('pointerup',ss[ss.length-1]);
      return {n:ss.length,s0,s1:+document.getElementById('pgScore').textContent,ink:!!P.querySelector('.pgink polyline')}}""")
    rec("Meadow","swiping through three seeds catches all three and adds a +1 bonus for the sweep",sw["n"]==3 and sw["s1"]-sw["s0"]==4 and sw["ink"],sw)
    rec("Meadow","a gust bends the grass before it pushes the seeds",wait_for(pg,"document.getElementById('pg').classList.contains('gust')",8000))
    d0=pg.evaluate("document.querySelectorAll('#pgClock rect').length"); pg.wait_for_timeout(4200); d1=pg.evaluate("document.querySelectorAll('#pgClock rect').length")
    rec("Meadow","the dandelion clock loses its seeds as the round runs down",d1<d0<=12,(d0,d1))
    pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)

    # ---------- Keep the Fire: the fire is the meter, embers fly up and cool, a bonfire is worth 3 ----------
    ready(pg,card(base,1)); openg(pg,1); start(pg); pg.wait_for_timeout(300)
    fs=pg.evaluate("[...document.querySelectorAll('#pg .fstage span')].map(s=>[s.textContent,s.classList.contains('on')])")
    rec("Ember","four fire stages show, with one lit",[x[0] for x in fs]==["Spark","Kindling","Campfire","Bonfire"] and sum(x[1] for x in fs)==1,fs)
    rec("Ember","embers fly up out of the fire",wait_for(pg,"!!document.querySelector('#pg .emb.rise')",3000))
    rec("Ember","…and cool to grey before they vanish",wait_for(pg,"!!document.querySelector('#pg .emb.cool')",3000))
    s0=int(pg.inner_text("#pgScore")); n=0; t0=time.time()
    while time.time()-t0<6 and not pg.evaluate("document.querySelector('#pg .fstage span:last-child').classList.contains('on')"):
        if pg.evaluate(TAP,".emb:not(.caught)"): n+=1
        pg.wait_for_timeout(120)
    on=pg.evaluate("document.querySelector('#pg .fstage span:last-child').classList.contains('on')"); sc=int(pg.inner_text("#pgScore"))
    rec("Ember","building the fire to a bonfire lights the last stage and is worth 3 once",on and sc>=s0+n+3,(on,s0,n,sc))
    pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)

    # ---------- Skipping Stones: five stones, skips, crossing the lake ----------
    ready(pg,card(base,2)); openg(pg,2); start(pg); pg.wait_for_timeout(200)
    rec("Tide","the first stone is thrown and the count says so",pg.inner_text("#pgSkips")=="Stone 1 of 5")
    HIT="""()=>new Promise(res=>{const t0=performance.now();const f=()=>{const s=document.getElementById('pgStone'),c=document.getElementById('pgCalm');if(!s||!c)return res('gone');
      if(performance.now()-t0>4000)return res('timeout');const a=s.getBoundingClientRect(),z=c.getBoundingClientRect(),m=a.left+a.width/2;
      if(getComputedStyle(c).opacity!=='0'&&m>z.left+z.width*.35&&m<z.right-z.width*.35){document.getElementById('pgSkip').click();res(document.getElementById('pgSkips').textContent);}else requestAnimationFrame(f)};f();})"""
    seen=[]
    for i in range(10):
        r=pg.evaluate(HIT); seen.append(r)
        if r=="Across the lake!": break
    rec("Tide","tapping in the shimmer skips the stone again, and again",seen[:2]==["One skip!","2 skips!"],seen[:3])
    sc=int(pg.inner_text("#pgScore"))
    rec("Tide","a stone that crosses the lake is worth 2 more",seen[-1]=="Across the lake!" and sc==len(seen)+2,(seen,sc))
    ok=wait_for(pg,"document.getElementById('pgSkips').textContent==='Stone 2 of 5'",3000)
    rec("Tide","…and the next stone follows",ok)
    pg.wait_for_timeout(300); pg.evaluate("()=>{document.getElementById('pgSkip').click()}"); pg.wait_for_timeout(100)
    rec("Tide","tapping before the stone reaches the shimmer sinks it, and says how many are left","sank" in pg.inner_text("#pgSkips") and "3 stones left" in pg.inner_text("#pgSkips"),pg.inner_text("#pgSkips"))
    rec("Tide","ripples stay on the water for a moment",pg.locator("#pg .ripr").count()>=1)
    ok=wait_for(pg,"!!document.querySelector('#pg .pgend')",16000)
    rec("Tide","when the fifth stone sinks, the round ends",ok and pg.inner_text("#pg .pgend")=="Five stones!",pg.inner_text("#pg .pgend") if ok else "")
    pg.wait_for_timeout(1400); closemodals(pg)

    # ---------- Snowflake Catch: six kinds, one of a kind, hail shadows ----------
    ready(pg,card(base,3)); openg(pg,3); pg.evaluate("()=>{let i=0;const q=[.1,.2,.5,.3,.7,.9,.4,.6,.8,.15,.35,.55];Math.random=()=>q[i++%q.length]}"); start(pg)
    rec("Frost","a strip of six kinds waits to be filled",pg.locator("#pg .fcol i").count()==6 and pg.locator("#pg .fcol i.got").count()==0)
    kinds=pg.evaluate("()=>new Set([...document.querySelectorAll('#pg .flake')].map(f=>[...f.classList].find(c=>/^flk\\d$/.test(c)))).size")
    CATCH="""()=>{const f=[...document.querySelectorAll('#pg .flake:not(.hail)')].sort((a,b)=>parseFloat(b.style.top)-parseFloat(a.style.top))[0];if(!f)return;const P=document.getElementById('pg'),r=P.getBoundingClientRect();
      P.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerId:3,clientX:r.left+parseFloat(f.style.left)/100*r.width,clientY:r.top+r.height/2}));P.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:3}));}"""
    t0=time.time(); rare=False
    while time.time()-t0<16:
        pg.evaluate(CATCH); pg.wait_for_timeout(50)
        if not rare and "One of a kind" in (pg.inner_text("#pgMsg") or ""): rare=True
    got=pg.locator("#pg .fcol i.got").count()
    rec("Frost","catching snowflakes fills in their kinds",got>=3,got)
    rec("Frost","a one-of-a-kind snowflake falls, and catching it presses it into your journal",rare and st(pg)["games"]["pressed"]==1,(rare,st(pg)["games"]))
    wait_for(pg,"!!document.getElementById('pgDone')",12000); m=mt(pg)
    rec("Frost","…the journal page says so","pressed into your journal" in m,m[:300])
    pg.evaluate("document.getElementById('pgDone').click()"); pg.wait_for_timeout(500)
    pg.evaluate("document.getElementById('hPlay').click()"); pg.wait_for_timeout(400)
    rec("Frost","…and its postcard counts what you have pressed","1 pressed" in pg.inner_text("#modal [data-game='3']"),pg.inner_text("#modal [data-game='3']"))
    closemodals(pg)
    ready(pg,card(base,3,dark=True)); openg(pg,3); start(pg)
    rec("Frost","hail shows a shadow on the snow before it lands",wait_for(pg,"!!document.querySelector('#pg .hshad')",15000))
    pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)

    # ---------- Lantern Lights: a string, sky lanterns, a slower replay, a fifth lantern ----------
    ready(pg,card(base,4)); openg(pg,4); pg.evaluate(WATCH); start(pg)
    lay=pg.evaluate("()=>{const s=document.querySelector('#pg .lstr'),L=[...document.querySelectorAll('#pg .lant')].map(b=>b.getBoundingClientRect());return {s:!!s,n:L.length,ok:L.every(r=>r.height>=44&&r.width>=44),y:L.map(r=>Math.round(r.top))}}")
    rec("Dusk","four lanterns hang along a string, each easy to tap",lay["s"] and lay["n"]==4 and lay["ok"] and lay["y"][1]>lay["y"][0] and lay["y"][2]>lay["y"][3],lay)
    def turn(ms=15000):
        pg.wait_for_function("()=>!document.getElementById('pg')||(document.getElementById('pgMsg').textContent==='Your turn.'&&window.__seq.length>0)",timeout=ms)
        sq=pg.evaluate("window.__seq.slice()"); pg.evaluate("window.__seq=[]"); return sq
    sq=turn()
    for v in sq: pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",v); pg.wait_for_timeout(80)
    pg.wait_for_timeout(500)
    rec("Dusk","finishing a round lets a sky lantern float up",pg.locator("#pg .skyl").count()==1)
    sq=turn(); pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",(sq[0]+1)%4); pg.wait_for_timeout(250)
    rec("Dusk","the first slip plays the tune once more, slower",pg.inner_text("#pgMsg")=="The lanterns flicker. Once more, slower." and pg.locator("#pg").count()==1,pg.inner_text("#pgMsg"))
    for r in range(7):
        sq=turn()
        if len(sq)>=8 or pg.locator("#pg [data-lant='4']").count(): break
        for v in sq: pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",v); pg.wait_for_timeout(60)
    five=pg.evaluate("()=>[...document.querySelectorAll('#pg .lant')].map(b=>b.getAttribute('aria-label'))")
    rec("Dusk","at round 8 a fifth lantern joins the string",len(five)==5 and five[4]=="Violet lantern",five)
    rec("Dusk","…and the sky keeps one lantern for each finished round",pg.locator("#pg .skyl").count()==7,pg.locator("#pg .skyl").count())
    sq=pg.evaluate("window.__seq.slice()")
    pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",(sq[0]+1)%5 if sq else 0); pg.wait_for_timeout(300)
    rec("Dusk","a second slip ends the game",wait_for(pg,"!document.getElementById('pg')||!!document.querySelector('#pg .pgend')||!!document.getElementById('pgDone')",4000))
    pg.wait_for_timeout(1400); closemodals(pg)

    # ---------- your Forgeling reacts ----------
    ready(pg,card(base,0,best={"meadow":2})); openg(pg,0); start(pg); ch=False; t0=time.time()
    pg.evaluate("()=>{window.__ch=0;new MutationObserver(()=>{if(document.querySelector('#pg .pgmate.cheer'))window.__ch=1}).observe(document.getElementById('pg'),{subtree:true,attributes:true,attributeFilter:['class']})}")
    while time.time()-t0<8 and not pg.evaluate("window.__ch"):
        pg.evaluate(TAP,".seed:not(.caught):not(.thorn)"); pg.wait_for_timeout(150)
    rec("Mate","your Forgeling cheers the moment you pass your best",pg.evaluate("window.__ch")==1)
    pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300); ctx.close()
    ctx,pg=newpage(b,390,844); pg.clock.install(time=datetime.datetime(2027,3,3,22,40)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    ready(pg,card(base,1)); openg(pg,1); start(pg); pg.wait_for_timeout(200)
    rec("Mate","late at night it yawns before playing anyway",pg.locator("#pg .pgzz").count()==1 and pg.inner_text("#pg .pgzz")=="z z")
    pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)

    # ---------- a round ends on a journal page; a bond level waits until you close it ----------
    s=card(base,0,bond=2,best={"meadow":1}); ready(pg,s); openg(pg,0); start(pg); t0=time.time()
    while time.time()-t0<22 and pg.locator("#pg").count():
        pg.evaluate(TAP,".seed:not(.caught):not(.thorn)"); pg.wait_for_timeout(110)
    wait_for(pg,"!!document.getElementById('pgDone')",4000)
    jp=pg.evaluate("()=>{const g=document.querySelector('#modal .gres');return g?{h:g.querySelector('h2').textContent,s:g.querySelector('.gs').textContent,stamp:!!g.querySelector('.gstamp[aria-hidden=true]'),x:g.innerText,again:!!document.getElementById('pgAgain'),done:document.getElementById('pgDone').textContent}:null}")
    rec("Result","a round ends on a journal page: who played what, the score written in, and a stamp for a new best",jp and jp["h"].startswith("Played Dandelion Drift with") and "points" in jp["s"] and jp["stamp"] and "A new best!" in jp["x"],jp)
    rec("Result","…it says how the bond grew, and the Hearth still says how it went",jp and "bond grew" in jp["x"] and any(w in pg.inner_text("#hmsg") for w in ("cheers","rumbles")))
    rec("Result","when the bond reaches a new level, the page waits with Back to the fire, and the level-up follows",jp and not jp["again"] and jp["done"]=="Back to the fire" and pg.locator("#modal .sheet h2, #modal h2").count()>0,jp)
    pg.evaluate("document.getElementById('pgDone').click()"); pg.wait_for_timeout(900)
    rec("Result","…then the new bond level opens",("is now" in mt(pg)),mt(pg)[:80])
    closemodals(pg)
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()

    # ---------- the Map ----------
    for hr,tag in ((11,"day"),(22,"lamplight")):
        ctx,pg=newpage(b,390,844); pg.clock.install(time=datetime.datetime(2027,3,3,hr,10)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        s=build(base,[3,3,3,3,3]); s["seen"]=99; s["explore"]={"0":0,"1":1,"2":2,"3":3,"4":4}; s["mapMax"]=[3,3,3,3,3]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg); openmap(pg); pg.wait_for_timeout(900)
        mp=pg.evaluate("""()=>{const svg=document.querySelector('.mapsvg');const ter=[...svg.querySelectorAll('g.mp-ter')];
          return {ter:ter.length,hid:ter.every(g=>g.getAttribute('aria-hidden')==='true'),rects:ter.map(g=>g.querySelectorAll('rect').length),clouds:svg.querySelectorAll('g.mp-cloud').length,
            smoke:svg.querySelectorAll('.mp-smoke').length,glow:svg.querySelector('.mp-glow')?getComputedStyle(svg.querySelector('.mp-glow')).opacity:null,dark:document.documentElement.getAttribute('data-theme')}}""")
        rec("Map",f"{tag}: every drawn realm has pixel terrain (trees, peaks, waves, pines, lamp posts), hidden from screen readers",mp["ter"]==5 and mp["hid"] and all(x>=6 for x in mp["rects"]) and mp["smoke"]>=1,mp)
        rec("Map",f"{tag}: clouds cover what you have not found, thinning as places are found (3+3+2+1+0)",mp["clouds"]==9,mp["clouds"])
        rec("Map",f"{tag}: Dusk's lamps glow only by lamplight",(mp["glow"]=="0.4")==(mp["dark"]=="dark") and (hr==22)==(mp["dark"]=="dark"),mp)
        v=axe(pg); rec("A11y",f"{tag}: axe finds nothing on the new Map",not v,v)
        rec("All",f"{tag}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    ctx,pg=newpage(b,390,844,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    s=build(base,[3,3,3,3,3]); s["seen"]=99; s["explore"]={"0":0}; s["mapMax"]=[3,3,3,3,3]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg); openmap(pg); pg.wait_for_timeout(600)
    an=pg.evaluate("[...document.querySelectorAll('.mapsvg .mp-cloud,.mapsvg .mp-smoke')].map(e=>getComputedStyle(e).animationName)")
    rec("Motion","with reduced motion the clouds and smoke hold still",an and all(a=="none" for a in an),an[:3])
    ready(pg,card(base,4)); openg(pg,4); start(pg); pg.wait_for_timeout(300)
    rec("Motion","…and the games still play",pg.locator("#pg .lant").count()==4 and not pg._errs,pg._errs[:1]); ctx.close()

    # ---------- accessibility: games mid-play and the journal page, day and night ----------
    bad=[]
    for hr in (11,22):
        ctx,pg=newpage(b,390,844); pg.clock.install(time=datetime.datetime(2027,3,3,hr,10)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        for ti in range(5):
            ready(pg,card(base,ti,used=3)); openg(pg,ti); start(pg); pg.wait_for_timeout(1500)
            bad+=[f"{hr}h {NAMES[ti]}: "+x for x in axe(pg)]
            pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)
        ready(pg,card(base,2,used=3)); openg(pg,2); start(pg); wait_for(pg,"!!document.getElementById('pgDone')",25000)
        bad+=[f"{hr}h result: "+x for x in axe(pg)]
        small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.offsetParent&&b.getBoundingClientRect().height<44).map(b=>b.id)")
        bad+=[f"{hr}h small: "+x for x in small]
        if pg._errs: bad+=[f"{hr}h errors: "+pg._errs[0]]
        ctx.close()
    rec("A11y","axe finds nothing on all five games mid-play and on the journal page, day and night, and every button is easy to tap",not bad,bad[:6])
    b.close()
save_results("qa_50"); print(sum(r["ok"] for r in RES),"/",len(RES))
