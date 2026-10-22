from lib import *
# 0.25.0: your Forgeling shapes its game (trait from a stat, a bond gift at Close, a dark twist), and every game feels
# better (Start card, streaks, sparkles, a clear finish). Everything here is played with real touch, as in qa_242.
import time
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
NAMES=["meadow","ember","tide","frost","dusk"]; TITLES=["Dandelion Drift","Keep the Fire","Skipping Stones","Snowflake Catch","Lantern Lights"]
SRC=open(P.replace("file://","")).read() if P.startswith("file://") else open(S+"/work.html").read()
HI={g:int(re.search(r"id:'"+g+r"'[^}]*?hi:(\d+)",SRC).group(1)) for g in NAMES}
MID={g:int(re.search(r"id:'"+g+r"'[^}]*?mid:(\d+)",SRC).group(1)) for g in NAMES}
VISIBLE="""sel=>{const P=document.getElementById('pg');if(!P)return null;const R=P.getBoundingClientRect();
  for(const el of P.querySelectorAll(sel)){const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;
    if(x<R.left+4||x>R.right-4||y<R.top+4||y>R.bottom-4)continue;const hit=document.elementFromPoint(x,y);if(hit&&(hit===el||el.contains(hit)))return [x,y];}
  return null}"""
def center(pg,sel): return pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}",sel)
def card(base,ti,stats=(50,50,50),bond=0,dark=False,used=0):
    s=build(base,[1 if i==ti else 0 for i in range(5)]); s["seen"]=99; c=s["cards"][0]; c["stats"]=list(stats); c["bond"]=bond; c["dark"]=dark
    s["hearth"]["slots"]=[c["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":used}; s["games"]={"best":{},"played":0,"curioDay":""}; return s
def ready(pg,s):
    pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click();const d=document.getElementById('pgDone');if(d)d.click()}"); pg.wait_for_timeout(200)
    setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg); tabto(pg,"hearth")
def openg(pg): pg.tap("#hPlay"); pg.wait_for_timeout(300); pg.tap("#modal [data-game]"); pg.wait_for_timeout(350)
def start(pg): pg.tap("#pgGo"); pg.wait_for_timeout(150)
def tapvis(pg,sel):
    xy=pg.evaluate(VISIBLE,sel)
    if xy: pg.touchscreen.tap(*xy); return True
    return False
def wait_for(pg,js,ms=9000):
    t0=time.time()
    while time.time()-t0<ms/1000:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(80)
    return False
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b,390,844); cdp=ctx.new_cdp_session(pg); pg.set_default_timeout(8000); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    _v=re.search(r"const VERSION='prototype (\d+)\.(\d+)",SRC); rec("Version","the app is 0.25 or later",_v and (int(_v.group(1)),int(_v.group(2)))>=(0,25))

    # ---------- the Start card ----------
    for ti,g in enumerate(NAMES):
        ready(pg,card(base,ti,stats=(61,72,83))); openg(pg); r=pg.inner_text("#pgReady") if pg.locator("#pgReady").count() else ""
        si={"meadow":1,"ember":0,"tide":2,"frost":2,"dusk":1}[g]; nm=["Grit","Spark","Calm"][si]; val=[61,72,83][si]
        rec("Start",f"{TITLES[ti]}: the Start card names your Forgeling's trait ({nm} {val}) and shows the gift waiting at Close bond",f"{nm} {val}:" in r and "At Close bond:" in r and "twist" not in r and not JUNK.search(r),r[:160])
        rec("Start",f"{TITLES[ti]}: Start has focus and nothing moves until you press it",pg.evaluate("document.activeElement.id")=="pgGo" and pg.locator("#pg .seed,#pg .emb,#pg .flake,#pg .ripple").count()==0 and pg.inner_text("#pgTime") in ("20s",""))
    ready(pg,card(base,0,stats=(61,72,83),bond=9,dark=True)); openg(pg); r=pg.inner_text("#pgReady")
    rec("Start","a dark, bonded Forgeling's card uses its dark stat name, unlocks the gift and names its realm's twist","Dread 72:" in r and "Bond gift:" in r and "Bramble twist:" in r,r[:220])
    pg.wait_for_timeout(1500); rec("Start","…and still nothing moves while the card is up",pg.locator("#pg .seed").count()==0)
    pg.tap("#pgSit"); pg.wait_for_timeout(400); s=st(pg)
    rec("Start","'Just sit together instead' works from the Start card",s["hearth"]["visits"]["used"]==1 and s["cards"][0]["bond"]==10)
    ready(pg,card(base,0)); openg(pg)
    pg.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});}"); pg.wait_for_timeout(300)
    rec("Start","leaving the app on the Start card just closes it, with no visit used",pg.evaluate("document.getElementById('modal').hidden") and st(pg)["hearth"]["visits"]["used"]==0)

    # ---------- streaks, sparkles, the finish ----------
    ready(pg,card(base,0)); openg(pg); start(pg); n=0; t0=time.time(); seen_streak=False; seen_pt=False
    while n<5 and time.time()-t0<12:
        if tapvis(pg,".seed:not(.caught):not(.gold):not(.thorn)"):
            n+=1; pg.wait_for_timeout(40); seen_pt=seen_pt or pg.locator("#pg .pt").count()>0
            if n==3: seen_streak=pg.inner_text("#pgStreak")=="Streak 3"
        else: pg.wait_for_timeout(60)
    sc=int(pg.inner_text("#pgScore"))
    rec("Feel","catches build a streak, shown from 3 in a row",seen_streak)
    rec("Feel","five in a row adds a +2 streak bonus",n==5 and sc==7,(n,sc))
    rec("Feel","each catch gives a burst of sparkles",seen_pt)
    t1=time.time(); ok=wait_for(pg,"!!document.querySelector('#pg .pgend')",25000)
    rec("Feel","the round lasts 20 seconds and ends with a clear 'Time!'",ok and pg.inner_text("#pg .pgend")=="Time!" and 13<time.time()-t0<24,round(time.time()-t0,1))
    pg.wait_for_timeout(1500); s=st(pg)
    rec("Feel","…then the visit counts and the bond grows",s["hearth"]["visits"]["used"]==1 and s["cards"][0]["bond"]>=1,s["hearth"]["visits"])
    # a missed seed breaks the streak
    ready(pg,card(base,0)); openg(pg); start(pg); k=0
    while k<3:
        if tapvis(pg,".seed:not(.caught):not(.gold)"): k+=1
        pg.wait_for_timeout(60)
    st3=pg.inner_text("#pgStreak"); pg.wait_for_timeout(1200); st_mid=pg.inner_text("#pgStreak"); pg.wait_for_timeout(1100)
    rec("Feel","a streak survives a short pause but ends after about two seconds without a catch",st3=="Streak 3" and st_mid=="Streak 3" and pg.inner_text("#pgStreak")=="",(st3,st_mid,pg.inner_text("#pgStreak")))

    # ---------- traits change play ----------
    def calm_width(cv):
        ready(pg,card(base,2,stats=(50,50,cv))); openg(pg); start(pg); pg.wait_for_timeout(200)
        return pg.evaluate("document.getElementById('pgCalm').getBoundingClientRect().width")
    lo,hi=calm_width(15),calm_width(99)
    rec("Trait","Skipping Stones: a Forgeling with high Calm gets wider calm water",hi>lo*1.15,(round(lo),round(hi)))
    def heat_after(gv):
        ready(pg,card(base,1,stats=(gv,50,50))); openg(pg); start(pg); pg.evaluate("()=>{document.querySelectorAll('#pg .emb').forEach(e=>e.remove())}"); pg.wait_for_timeout(3000)
        return pg.evaluate("parseFloat(document.querySelector('#pg .heat i').style.width)")
    lo,hi=heat_after(15),heat_after(99)
    rec("Trait","Keep the Fire: a Forgeling with high Grit's fire burns down more slowly",hi>lo+5,(lo,hi))
    def fall(cv):
        ready(pg,card(base,3,stats=(50,50,cv))); openg(pg); pg.evaluate("()=>{Math.random=()=>0.5}"); start(pg); pg.wait_for_timeout(1200)
        return pg.evaluate("Math.max(...[...document.querySelectorAll('#pg .flake')].map(f=>parseFloat(f.style.top)))")
    lo,hi=fall(15),fall(99)
    rec("Trait","Snowflake Catch: high Calm makes the snow fall more gently",hi<lo*0.9,(round(lo),round(hi)))
    def golds(sv):
        ready(pg,card(base,0,stats=(50,sv,50))); openg(pg); pg.evaluate("()=>{let i=0;const q=[.95,.85,.5,.9,.88,.2,.83,.96,.86,.1];Math.random=()=>q[i++%q.length]}"); start(pg); pg.wait_for_timeout(5000)
        return pg.locator("#pg .seed.gold").count()
    lo,hi=golds(15),golds(99)
    rec("Trait","Dandelion Drift: high Spark brings more golden seeds",hi>lo,(lo,hi))
    def glow(sv):
        ready(pg,card(base,4,stats=(50,sv,50))); openg(pg)
        pg.evaluate("()=>{window.__on=[];new MutationObserver(ms=>{for(const m of ms){const t=m.target;if(t.classList&&t.classList.contains('lant'))window.__on.push([t.classList.contains('on'),performance.now()]);}}).observe(document.getElementById('pg'),{subtree:true,attributes:true,attributeFilter:['class']});}")
        start(pg); wait_for(pg,"document.getElementById('pgMsg').textContent==='Your turn.'",5000)
        ev=pg.evaluate("window.__on"); on=[t for o,t in ev if o]; off=[t for o,t in ev if not o]
        return off[0]-on[0] if on and off else 0
    lo,hi=glow(15),glow(99)
    rec("Trait","Lantern Lights: high Spark makes each lantern glow longer",hi>lo+80,(round(lo),round(hi)))

    # ---------- bond gifts ----------
    ready(pg,card(base,0,bond=9)); openg(pg); start(pg)
    ok=wait_for(pg,"!!document.querySelector('#pg .seed.puff')",8000)
    rec("Gift","Dandelion Drift at Close bond: a dandelion puff drifts by",ok)
    if ok:
        wait_for(pg,"(()=>{const P=document.getElementById('pg').getBoundingClientRect(),r=document.querySelector('#pg .seed.puff').getBoundingClientRect();return r.top>P.top+10&&r.bottom<P.bottom-10})()",4000)
        pg.evaluate("()=>{window.__add=0;new MutationObserver(ms=>{let k=0;for(const m of ms)for(const n of m.addedNodes)if(n.classList&&n.classList.contains('seed')&&!n.classList.contains('puff'))k++;window.__add=Math.max(window.__add,k);}).observe(document.getElementById('pg'),{childList:true});}")
        hitp=False
        for _ in range(3):
            if pg.evaluate("window.__add")>=5: break
            tapvis(pg,".seed.puff"); pg.wait_for_timeout(120)
        rec("Gift","…and tapping it scatters five seeds at once",pg.evaluate("window.__add")>=5,pg.evaluate("window.__add"))
    ready(pg,card(base,0,bond=0)); openg(pg); start(pg); pg.wait_for_timeout(8000)
    rec("Gift","…but a Forgeling below Close bond gets no puff",pg.locator("#pg .seed.puff").count()==0)
    ready(pg,card(base,1,bond=9)); openg(pg); start(pg); ok=wait_for(pg,"!!document.querySelector('#pg .emb.log')",9000)
    if ok: s0=int(pg.inner_text("#pgScore")); tapvis(pg,".emb.log"); pg.wait_for_timeout(100)
    rec("Gift","Keep the Fire at Close bond: a log turns up, and it is worth 3",ok and int(pg.inner_text("#pgScore"))>=s0+3)
    ready(pg,card(base,3,bond=9)); openg(pg); start(pg)
    rec("Gift","Snowflake Catch at Close bond: a big snowflake falls",wait_for(pg,"!!document.querySelector('#pg .flake.big')",8000))
    ready(pg,card(base,2,bond=9)); openg(pg); start(pg); pg.evaluate("()=>{window.__w=[]}")
    CLICKMID="""()=>new Promise(res=>{const f=()=>{const s=document.getElementById('pgStone'),c=document.getElementById('pgCalm');if(!s||!c)return res(false);const a=s.getBoundingClientRect(),z=c.getBoundingClientRect(),m=a.left+a.width/2;
      if(m>z.left+z.width*.4&&m<z.right-z.width*.4){document.getElementById('pgSkip').click();res(true);}else requestAnimationFrame(f)};f();})"""
    for i in range(5):
        if i==4: w4=pg.evaluate("document.getElementById('pgCalm').getBoundingClientRect().width")
        pg.evaluate(CLICKMID); pg.wait_for_timeout(250)
    w5=pg.evaluate("document.getElementById('pgCalm').getBoundingClientRect().width")
    rec("Gift","Skipping Stones at Close bond: the fifth skip brings a lucky stone that widens the calm water",pg.inner_text("#pgScore")=="5" and w5>w4 and "lucky stone" in pg.inner_text("#pgMsg"),(pg.inner_text("#pgScore"),round(w4),round(w5)))
    ready(pg,card(base,4,bond=9)); openg(pg); start(pg); wait_for(pg,"document.getElementById('pgMsg').textContent==='Your turn.'",5000)
    seq0=pg.evaluate("[...document.querySelectorAll('#pg .lant')].length")
    pg.touchscreen.tap(*center(pg,"#pg [data-lant='0']")); pg.wait_for_timeout(50); pg.touchscreen.tap(*center(pg,"#pg [data-lant='1']")); pg.touchscreen.tap(*center(pg,"#pg [data-lant='2']")); pg.wait_for_timeout(400)
    forgiven="evening star" in pg.inner_text("#pgMsg") or pg.inner_text("#pgMsg") in("Watch.","Your turn.")
    rec("Gift","Lantern Lights at Close bond: the evening star forgives a slip and the round plays again",forgiven and pg.locator("#pg .pgend").count()==0 and pg.locator("#pg").count()==1,pg.inner_text("#pgMsg"))

    # ---------- dark twists ----------
    ready(pg,card(base,0,dark=True)); openg(pg); start(pg)
    ok=wait_for(pg,"(()=>{const P=document.getElementById('pg').getBoundingClientRect();return [...document.querySelectorAll('#pg .seed.thorn')].some(e=>{const r=e.getBoundingClientRect();return r.top>P.top+10&&r.bottom<P.bottom-10})})()",17000)
    rec("Twist","Bramble: thorny burrs drift up among the seeds",ok)
    if ok:
        k=0
        while k<3:
            if tapvis(pg,".seed:not(.caught):not(.thorn):not(.gold)"): k+=1
            pg.wait_for_timeout(50)
        s0=int(pg.inner_text("#pgScore")); t0=time.time()
        while time.time()-t0<6:
            if tapvis(pg,".seed.thorn:not(.caught)"): break
            pg.wait_for_timeout(60)
        pg.wait_for_timeout(100)
        rec("Twist","…tapping one costs 2 and breaks the streak",int(pg.inner_text("#pgScore"))==max(0,s0-2) and pg.inner_text("#pgStreak")=="",(s0,pg.inner_text("#pgScore")))
    ready(pg,card(base,1,dark=True)); openg(pg); start(pg)
    rec("Twist","Inferno: a cold wind blows through and says so",wait_for(pg,"document.getElementById('pg').classList.contains('wind')&&document.getElementById('pgMsg').textContent.startsWith('A cold wind')",8000))
    ready(pg,card(base,2,dark=True)); openg(pg); start(pg); a=pg.evaluate("document.getElementById('pgCalm').getBoundingClientRect().left"); pg.wait_for_timeout(1500); b2=pg.evaluate("document.getElementById('pgCalm').getBoundingClientRect().left")
    rec("Twist","Abyss: the calm water drifts",abs(a-b2)>8,(round(a),round(b2)))
    ready(pg,card(base,3,dark=True)); openg(pg); start(pg)
    rec("Twist","Wraith: hailstones fall with the snow",wait_for(pg,"!!document.querySelector('#pg .flake.hail')",15000))
    def gaps(dark):
        ready(pg,card(base,4,dark=dark)); openg(pg)
        pg.evaluate("()=>{window.__t=[];new MutationObserver(ms=>{for(const m of ms){const t=m.target;if(t.classList&&t.classList.contains('lant')&&t.classList.contains('on')&&document.getElementById('pgMsg').textContent==='Watch.')window.__t.push([+t.dataset.lant,performance.now()]);}}).observe(document.getElementById('pg'),{subtree:true,attributes:true,attributeFilter:['class']});}")
        start(pg); out=[]
        for rnd in range(4):
            wait_for(pg,"document.getElementById('pgMsg').textContent==='Watch.'",4000)
            wait_for(pg,"document.getElementById('pgMsg').textContent==='Your turn.'",9000)
            ev=pg.evaluate("window.__t.splice(0)");
            if len(ev)>1: out.append((ev[-1][1]-ev[0][1])/(len(ev)-1))
            for v,_ in ev: pg.touchscreen.tap(*center(pg,f"#pg [data-lant='{v}']")); pg.wait_for_timeout(120)
            pg.wait_for_timeout(300)
        return out
    gl,gd=gaps(False),gaps(True)
    rec("Twist","Void: the lanterns are shown faster each round (and steady for a cute Forgeling)",len(gd)>=2 and gd[-1]<gd[0]-40 and len(gl)>=2 and abs(gl[-1]-gl[0])<30,([round(x) for x in gl],[round(x) for x in gd]))

    # ---------- rewards and results ----------
    ready(pg,card(base,0,used=3)); openg(pg); start(pg); wait_for(pg,"!!document.getElementById('pgAgain')",26000)
    m=mt(pg); rec("Result","a free round's result is counted in points",re.search(r"\d+ points?",m) is not None and pg.locator("#pgAgain").count()==1,m[:80])
    pg.tap("#pgAgain"); pg.wait_for_timeout(300)
    rec("Result","Play again shows the Start card again",pg.locator("#pgReady").count()==1)
    rec("Thresholds","targets: catching games need more than tide and lanterns, and 3 bond needs more than 2",all(HI[g]>MID[g]>0 for g in NAMES) and HI["meadow"]>HI["tide"] and HI["frost"]>HI["dusk"],(HI,MID))
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()

    # ---------- reduced motion: no sparkles or pop-ins, still playable ----------
    ctx,pg=newpage(b,390,844,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    ready(pg,card(base,0)); openg(pg); start(pg); hit=0; t0=time.time()
    while hit<3 and time.time()-t0<10:
        if tapvis(pg,".seed:not(.caught):not(.gold)"): hit+=1; pg.wait_for_timeout(30);
        else: pg.wait_for_timeout(60)
    rec("Motion","with reduced motion the seeds still rise and can be caught, without sparkles",hit==3 and pg.locator("#pg .pt,#pg .ptx").count()==0 and int(pg.inner_text("#pgScore"))==3)
    rec("All","reduced motion: no page errors",not pg._errs,pg._errs[:1]); ctx.close()

    # ---------- layout and accessibility ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        for W,H in ((320,640),(430,932)):
            ctx,pg=newpage(b,W,H,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
            for ti in range(5):
                ready(pg,card(base,ti,bond=9,dark=True)); openg(pg)
                fit=pg.evaluate("(()=>{const r=document.getElementById('pgReady');return r.scrollHeight<=r.clientHeight+1&&document.documentElement.scrollWidth<=document.documentElement.clientWidth})()")
                rec("Layout",f"{scheme} {W}px: {TITLES[ti]}'s Start card (dark, with gift and twist) fits its play area",fit)
                if W==430 and ti in (0,4):
                    pg.wait_for_function("!document.body.classList.contains('arrive')"); pg.evaluate(AXE)
                    bad+=[f"{scheme} {TITLES[ti]} start: {v}" for v in pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")]
                    start(pg); pg.wait_for_timeout(2500)
                    bad+=[f"{scheme} {TITLES[ti]} playing: {v}" for v in pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")]
            rec("All",f"{scheme} {W}px: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations on a Start card and mid-game, light and dark",not bad,bad[:4])
    b.close()
save_results("qa_25"); print(sum(r["ok"] for r in RES),"/",len(RES))
