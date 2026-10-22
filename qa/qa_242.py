from lib import *
# 0.24.2: every game is played the way a person plays it: real touch taps on what is visible on screen, and real finger
# drags. (Earlier suites fired events straight at elements, which missed seeds that never rose into view.)
import time
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
NAMES=["meadow","ember","tide","frost","dusk"]; TITLES=["Dandelion Drift","Keep the Fire","Skipping Stones","Snowflake Catch","Lantern Lights"]
WATCH="""()=>{window.__seq=[];new MutationObserver(ms=>{for(const m of ms){const t=m.target;if(t.classList&&t.classList.contains('lant')&&t.classList.contains('on')&&document.getElementById('pgMsg').textContent==='Watch.')window.__seq.push(+t.dataset.lant);}}).observe(document.getElementById('pg'),{subtree:true,attributes:true,attributeFilter:['class']});}"""
# a target only counts if a finger at its centre would really land on it (inside the play area, not covered)
VISIBLE="""sel=>{const P=document.getElementById('pg');if(!P)return null;const R=P.getBoundingClientRect();
  for(const el of P.querySelectorAll(sel)){const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;
    if(x<R.left+4||x>R.right-4||y<R.top+4||y>R.bottom-4)continue;const hit=document.elementFromPoint(x,y);if(hit&&(hit===el||el.contains(hit)))return [x,y];}
  return null}"""
def drag(pg,cdp,x0,y,x1,steps=6):
    cdp.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":x0,"y":y}]})
    for i in range(1,steps+1): cdp.send("Input.dispatchTouchEvent",{"type":"touchMove","touchPoints":[{"x":x0+(x1-x0)*i/steps,"y":y}]}); pg.wait_for_timeout(12)
    cdp.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]})
def center(pg,sel): return pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}",sel)
def play(pg,cdp,g,secs=23,rounds=3):
    if g=="dusk": pg.evaluate(WATCH)
    t0=time.time()
    while time.time()-t0<secs and pg.locator("#pg").count():
        if g=="meadow":
            xy=pg.evaluate(VISIBLE,".seed:not(.caught)")
            if xy: pg.touchscreen.tap(*xy)
        elif g=="ember":
            xy=pg.evaluate(VISIBLE,".emb:not(.caught)")
            if xy: pg.touchscreen.tap(*xy)
        elif g=="tide":
            if pg.evaluate("()=>{const s=document.getElementById('pgStone'),c=document.getElementById('pgCalm');if(!s||!c)return false;const a=s.getBoundingClientRect(),z=c.getBoundingClientRect(),m=a.left+a.width/2;return m>z.left+3&&m<z.right-3}"):
                pg.touchscreen.tap(*center(pg,"#pgSkip"))
        elif g=="frost":
            f=pg.evaluate("()=>{const f=[...document.querySelectorAll('#pg .flake')].sort((a,b)=>parseFloat(b.style.top)-parseFloat(a.style.top))[0];return f?f.getBoundingClientRect().left+10:null}")
            if f:
                bx,by=center(pg,"#pgBasket"); R=pg.evaluate("()=>{const r=document.getElementById('pg').getBoundingClientRect();return r.top+r.height/2}")
                drag(pg,cdp,bx,R,f)
        elif g=="dusk":
            if pg.evaluate("document.getElementById('pgMsg').textContent")=="Your turn.":
                seq=pg.evaluate("window.__seq.slice()"); pg.evaluate("window.__seq=[]")
                if len(seq)>rounds:
                    pg.touchscreen.tap(*center(pg,f"#pg [data-lant='{(seq[0]+1)%4}']")); pg.wait_for_timeout(1200); break
                for v in seq: pg.touchscreen.tap(*center(pg,f"#pg [data-lant='{v}']")); pg.wait_for_timeout(90)
            pg.wait_for_timeout(60); continue
        pg.wait_for_timeout(40)
    pg.wait_for_timeout(1400)
def one(base,ti,used=0):
    s=build(base,[1 if i==ti else 0 for i in range(5)]); s["seen"]=99; s["hearth"]["slots"]=[s["cards"][0]["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":used}; s["games"]={"best":{},"played":0,"curioDay":""}; return s
def ready(pg,s): setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)
with sync_playwright() as p:
    b=p.chromium.launch()
    for (W,H,extra) in [(390,844,{}),(375,667,{}),(390,844,{"reduced_motion":"reduce"})]:
        tag=f"{W}x{H}"+(" reduced motion" if extra else "")
        ctx,pg=newpage(b,W,H,**extra); cdp=ctx.new_cdp_session(pg); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        for ti,g in enumerate(NAMES):
            ready(pg,one(base,ti)); tabto(pg,"hearth"); pg.tap("#hPlay"); pg.wait_for_timeout(300); pg.tap("#modal [data-game]"); pg.wait_for_timeout(300); pg.tap("#pgGo"); pg.wait_for_timeout(300)
            opened=pg.locator("#pg").count()==1 and TITLES[ti] in mt(pg) and pg.locator("#pgReady").count()==0
            rec("Touch",f"{tag}: tapping Play opens {TITLES[ti]}",opened,mt(pg)[:40])
            if not opened: continue
            if g=="meadow":
                pg.wait_for_timeout(1200); seen=pg.evaluate(VISIBLE,".seed:not(.caught)")
                rec("Touch",f"{tag}: seeds rise into view where a finger can reach them",seen is not None)
            if g=="frost":
                bx,_=center(pg,"#pgBasket"); R=pg.evaluate("()=>{const r=document.getElementById('pg').getBoundingClientRect();return [r.left,r.top+r.height/2,r.width]}")
                drag(pg,cdp,R[0]+30,R[1],R[0]+R[2]-30,10); pg.wait_for_timeout(100); bx2,_=center(pg,"#pgBasket")
                rec("Touch",f"{tag}: dragging a finger across Snowflake Catch carries your Forgeling with it",bx2>R[0]+R[2]-80,(round(bx),round(bx2)))
            sy0=pg.evaluate("scrollY"); play(pg,cdp,g); s=st(pg); best=s["games"]["best"].get(g,0)
            rec("Touch",f"{tag}: {TITLES[ti]} scores with real taps and drags",best>=(3 if g=="dusk" else 2),best)
            rec("Touch",f"{tag}: {TITLES[ti]} grows the bond and uses a visit",s["cards"][0]["bond"]>=1 and s["hearth"]["visits"]["used"]==1,(s["cards"][0]["bond"],s["hearth"]["visits"]))
            rec("Touch",f"{tag}: the page never scrolled while playing",pg.evaluate("scrollY")==sy0)
        rec("All",f"{tag}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    b.close()
save_results("qa_242"); print(sum(r["ok"] for r in RES),"/",len(RES))
