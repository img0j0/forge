from lib import *
# 0.23.0: a game for each realm (with your Forgeling in it), rewards within visits, free play after, and a fuller first week.
import time, datetime
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
SRC=open(P.replace("file://","")).read() if P.startswith("file://") else open(S+"/work.html").read()
TIDE_HI=int(re.search(r"id:'tide'[^}]*?hi:(\d+)",SRC).group(1))
TITLES=["Dandelion Drift","Keep the Fire","Skipping Stones","Snowflake Catch","Lantern Lights"]
WATCH="""()=>{window.__seq=[];const o=new MutationObserver(ms=>{for(const m of ms){const t=m.target;if(t.classList&&t.classList.contains('lant')&&t.classList.contains('on')&&document.getElementById('pgMsg').textContent==='Watch.')window.__seq.push(+t.dataset.lant);}});o.observe(document.getElementById('pg'),{subtree:true,attributes:true,attributeFilter:['class']});window.__obs=o;}"""
def bot(pg,gid,secs=23,rounds=4,blunder=True):
    t0=time.time()
    while time.time()-t0<secs and pg.locator("#pg").count():
        if gid==0: pg.evaluate("()=>{const b=document.querySelector('#pg .seed:not(.caught)');if(b)b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))}")
        elif gid==1: pg.evaluate("()=>{const b=document.querySelector('#pg .emb:not(.caught)');if(b)b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))}")
        elif gid==2: pg.evaluate("()=>{const s=document.getElementById('pgStone'),c=document.getElementById('pgCalm');if(!s||!c)return;const a=s.getBoundingClientRect(),z=c.getBoundingClientRect(),m=a.left+a.width/2;if(m>z.left+3&&m<z.right-3)document.getElementById('pgSkip').click()}")
        elif gid==3: pg.evaluate("()=>{const f=[...document.querySelectorAll('#pg .flake')].sort((a,b)=>parseFloat(b.style.top)-parseFloat(a.style.top))[0];if(!f)return;const r=document.getElementById('pg').getBoundingClientRect();document.getElementById('pg').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:f.getBoundingClientRect().left+10,clientY:r.top+40}))}")
        elif gid==4:
            st_=pg.evaluate("()=>[document.getElementById('pgMsg')&&document.getElementById('pgMsg').textContent,window.__seq.length]")
            if st_[0]=="Your turn.":
                seq=pg.evaluate("window.__seq.slice()"); pg.evaluate("window.__seq=[]")
                if blunder and len(seq)>rounds:
                    wrong=(seq[0]+1)%4; pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",wrong); pg.wait_for_timeout(1200); break
                for v in seq: pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",v); pg.wait_for_timeout(90)
            pg.wait_for_timeout(60); continue
        pg.wait_for_timeout(40 if gid in (2,3) else 110)
    pg.wait_for_timeout(1300)
def playopen(pg):
    pg.evaluate("document.getElementById('hPlay').click()"); pg.wait_for_timeout(250)
    pg.evaluate("()=>{const b=document.querySelector('#modal [data-game]');if(b)b.click()}"); pg.wait_for_timeout(250)
    pg.evaluate("()=>{const b=document.getElementById('pgGo');if(b)b.click()}")
def ready(pg,s): setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)
def one(base,ti,used=0,bond=0):
    s=build(base,[1 if i==ti else 0 for i in range(5)]); s["seen"]=99; s["hearth"]["slots"]=[s["cards"][0]["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":used}; s["cards"][0]["bond"]=bond; s["games"]={"best":{},"played":0,"curioDay":""}; return s
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b,430,932,color_scheme="dark"); pg.set_default_timeout(8000); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    for ti in range(5):
        ready(pg,one(base,ti)); tabto(pg,"hearth")
        rec("Game",f"the Hearth says Play opens all the games (realm {ti})","Play any of the five games" in pg.inner_text("#view-hearth"))
        playopen(pg); pg.wait_for_timeout(400)
        if ti==4: pg.evaluate(WATCH)
        mate=pg.evaluate("()=>{const m=document.querySelector('#pg .pgmate');return m?[m.src.slice(0,22),m.getAttribute('alt')]:null}")
        rec("Game",f"{TITLES[ti]}: opens with the right title and your Forgeling in the scene",TITLES[ti] in mt(pg) and mate and mate[0]=="data:image/png;base64," and mate[1]=="",(mt(pg)[:40],mate))
        small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.offsetParent&&!b.classList.contains('seed')&&!b.classList.contains('emb')).map(b=>[Math.round(b.getBoundingClientRect().height),b.id||b.className]).filter(x=>x[0]<44)")
        rec("Game",f"{TITLES[ti]}: every control is easy to tap",not small,small)
        bot(pg,ti)
        s=st(pg); best=s["games"]["best"].get(["meadow","ember","tide","frost","dusk"][ti],0)
        rec("Game",f"{TITLES[ti]}: a good round grows the bond, uses a visit and records a best",best>0 and s["cards"][0]["bond"]>=2 and s["hearth"]["visits"]["used"]==1 and s["games"]["played"]==1,(best,s["cards"][0]["bond"],s["hearth"]["visits"]))
        rec("Game",f"{TITLES[ti]}: the Hearth says how it went",any(w in pg.inner_text("#hmsg") for w in ("cheers","rumbles")),pg.inner_text("#hmsg")[:80])
    # the lantern sequence grows by one each round, and a wrong lantern ends it
    ready(pg,one(base,4)); tabto(pg,"hearth"); playopen(pg); pg.wait_for_timeout(300); pg.evaluate(WATCH)
    bot(pg,4,secs=40,rounds=3)
    rec("Game","Lantern Lights: rounds grow one lantern at a time and a wrong lantern ends the game on the last full round",st(pg)["games"]["best"].get("dusk")==3,st(pg)["games"]["best"])
    # sit together instead
    ready(pg,one(base,0)); tabto(pg,"hearth"); playopen(pg); pg.wait_for_timeout(300); pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(500)
    s=st(pg); rec("Game","'Just sit together instead' still gives a calm +1 and uses the visit",s["cards"][0]["bond"]==1 and s["hearth"]["visits"]["used"]==1,(s["cards"][0]["bond"],s["hearth"]["visits"]))
    # free play
    ready(pg,one(base,1,used=3,bond=4)); tabto(pg,"hearth")
    rec("Free","with visits used up, Play stays open and says Just for fun","Just for fun" in pg.inner_text("#hPlay") and not pg.evaluate("document.getElementById('hPlay').disabled") and "just for fun" in pg.inner_text("#view-hearth"))
    playopen(pg); pg.wait_for_timeout(300)
    rec("Free","the game says it is just for fun",("Just for fun" in mt(pg)) and pg.inner_text("#pgSit")=="Stop playing")
    bot(pg,1); m=mt(pg); s=st(pg)
    rec("Free","a free round ends on a little result screen with your best, and no bond is added",("points" in m) and pg.locator("#pgAgain").count()==1 and s["cards"][0]["bond"]==4 and s["games"]["best"].get("ember",0)>0,(m[:80],s["cards"][0]["bond"]))
    pg.evaluate("document.getElementById('pgAgain').click()"); pg.wait_for_timeout(400)
    rec("Free","Play again starts another round",pg.locator("#pg").count()==1 and "Keep the Fire" in mt(pg))
    pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(400)
    rec("Free","Stop playing closes it with nothing changed",pg.evaluate("document.getElementById('modal').hidden") and st(pg)["cards"][0]["bond"]==4)
    # switching away mid-game ends the round kindly
    playopen(pg); pg.wait_for_timeout(500)
    pg.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});}"); pg.wait_for_timeout(400)
    rec("Free","leaving the app mid-game ends the round instead of leaving it running",pg.locator("#pg").count()==0 and pg.locator("#pgAgain").count()==1 and not pg._errs,pg._errs[:1])
    closemodals(pg); pg.evaluate("()=>{const d=document.getElementById('pgDone');if(d)d.click()}"); pg.wait_for_timeout(300)
    # a great round can turn up a curio from that realm, once a day
    ready(pg,one(base,2)); tabto(pg,"hearth"); playopen(pg); pg.wait_for_timeout(300)
    bot(pg,2,secs=3); pg.evaluate("()=>{Math.random=()=>0.01}")
    pg.evaluate("()=>{for(let i=0;i<8;i++){}}")
    s=st(pg)
    pg.evaluate("()=>{const st=document.getElementById('pgScore');}")
    pg.wait_for_timeout(100)
    # force a top score by finishing with many skips: replay with a stubbed random and a quick bot run
    ready(pg,one(base,2)); tabto(pg,"hearth"); playopen(pg); pg.wait_for_timeout(300)
    bot(pg,2,secs=23); s=st(pg); cur=[k for k in s["curios"]]
    if s["games"]["best"].get("tide",0)>=TIDE_HI:
        pass
    ready(pg,one(base,2)); tabto(pg,"hearth"); pg.evaluate("()=>{const R=Math.random;window.__R=R;}")
    playopen(pg); pg.wait_for_timeout(300); pg.evaluate("()=>{Math.random=()=>0.02}")
    bot(pg,2,secs=23); s=st(pg)
    TIDE={"shell","pebble","rain","coin"}
    got=[k for k in s["curios"] if k in TIDE]
    rec("Curio","a great round can turn up a curio from that Forgeling's realm, and the Hearth says so",s["games"]["best"].get("tide",0)>=TIDE_HI and (len(got)==1 and s["games"]["curioDay"]==s["date"] and "found something nearby" in pg.inner_text("#hmsg")),(s["games"]["best"],got,pg.inner_text("#hmsg")[:120]))
    if got:
        s["hearth"]["visits"]={"date":s["date"],"used":0}; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"hearth")
        playopen(pg); pg.wait_for_timeout(300); pg.evaluate("()=>{Math.random=()=>0.02}"); bot(pg,2,secs=23)
        rec("Curio","…but only once a day",sum(v["n"] for k,v in st(pg)["curios"].items())==1,st(pg)["curios"])
    # damaged game data
    for bad in ("x",{"best":"y"},{"best":{"tide":-4,"meadow":"9","frost":5000}},None,[1]):
        s=st(pg); s["games"]=bad; ready(pg,s); g=st(pg)["games"]
        rec("Damaged",f"damaged game records ({bad!r}) are repaired",isinstance(g,dict) and isinstance(g["best"],dict) and all(isinstance(v,int) and 0<v<=999 for v in g["best"].values()) and not pg._errs,(g,pg._errs[:1]))
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # reduced motion
    ctx,pg=newpage(b,430,932,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    ready(pg,one(base,1)); tabto(pg,"hearth"); playopen(pg); pg.wait_for_timeout(400)
    rec("Motion","with reduced motion, the moving games can still be played",pg.locator("#pg").count()==1 and "Keep the Fire" in mt(pg)); closemodals(pg); pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click()}"); pg.wait_for_timeout(300)
    ready(pg,one(base,4)); tabto(pg,"hearth"); playopen(pg); pg.wait_for_timeout(400)
    rec("Motion","…and so can the lantern game",pg.locator("#pg .lant").count()==4); ctx.close()
    # a fuller first week
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); s["seen"]=99; s["hearth"]["slots"]=[s["cards"][0]["id"]]; s["hearth"]["fseen"]=[]; ready(pg,s); tabto(pg,"hearth")
    rec("First week","the first calling already brings the rug","woven rug" in pg.inner_text("#hmsg"),pg.inner_text("#hmsg"))
    pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(300)
    rec("First week","the first wander says it will be back in about 20 minutes","about 20 minutes" in mt(pg))
    pg.evaluate("document.querySelector('#modal [data-wgo]').click()"); pg.wait_for_timeout(300); w=st(pg)["wander"]
    rec("First week","…and it really is about 20 minutes",abs((w["ready"]-w["start"])/60000-20)<1,(w["ready"]-w["start"])/60000)
    s=st(pg); s["wander"]=None; ready(pg,s); tabto(pg,"hearth"); pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(300); pg.evaluate("document.querySelector('#modal [data-wgo]').click()"); pg.wait_for_timeout(300); w=st(pg)["wander"]
    rec("First week","later wanders take the usual three hours",abs((w["ready"]-w["start"])/3600000-3)<.05)
    d0=datetime.date.fromisoformat(st(pg)["date"]); s=st(pg); s["wander"]=None; s["startDate"]=(d0-datetime.timedelta(days=1)).isoformat(); s["cards"][0]["bond"]=3; s["request"]=None; s["reqLast"]=""; s["wstat"]={"sent":1,"back":1}; ready(pg,s); tabto(pg,"hearth")
    rec("First week","a request can come on day two",st(pg)["request"] is not None,st(pg)["request"])
    rec("All","no page errors in the first week",not pg._errs,pg._errs[:1]); ctx.close()
    # accessibility of a game and its result
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,430,932,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
        for ti in (2,4):
            ready(pg,one(base,ti,used=3)); tabto(pg,"hearth"); playopen(pg); pg.wait_for_timeout(500)
            pg.wait_for_function("!document.body.classList.contains('arrive')"); pg.evaluate(AXE)
            v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
            bad+=[f"{scheme}/{TITLES[ti]}: {x}" for x in v]
            pg.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});}"); pg.wait_for_timeout(400); pg.evaluate(AXE)
            v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
            bad+=[f"{scheme}/{TITLES[ti]} result: {x}" for x in v]; closemodals(pg); pg.evaluate("()=>{const d=document.getElementById('pgDone');if(d)d.click()}")
        ctx.close()
    rec("A11y","axe: zero violations on a game and its result screen, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_23"); print(sum(r["ok"] for r in RES),"/",len(RES))
