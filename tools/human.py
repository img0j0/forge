import sys,os,time,random,json; sys.path.insert(0,"/home/claude/qa-src/forge-qa/qa"); os.chdir("/home/claude/qa-src/forge-qa/qa")
os.environ["FORGE_HTML"]="file:///home/claude/forge/work.html"
from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
NAMES=["meadow","ember","tide","frost","dusk"]; RUNS=int(sys.argv[1]) if len(sys.argv)>1 else 3
CFG={"new":dict(stats=[30,30,30],bond=0,dark=False),"strong":dict(stats=[85,85,85],bond=9,dark=False),"dark":dict(stats=[55,55,55],bond=9,dark=True)}
VIS="""kinds=>{const P=document.getElementById('pg').getBoundingClientRect();const out=[];for(const el of document.querySelectorAll('#pg .seed:not(.caught),#pg .emb:not(.caught)')){const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;if(y<P.top+6||y>P.bottom-6)continue;const h=document.elementFromPoint(x,y);if(h&&el.contains(h))out.push([x,y,el.className]);}return out}"""
def center(pg,sel): return pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}",sel)
def drag(pg,cdp,x0,y,x1,steps=5):
    cdp.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":x0,"y":y}]})
    for i in range(1,steps+1): cdp.send("Input.dispatchTouchEvent",{"type":"touchMove","touchPoints":[{"x":x0+(x1-x0)*i/steps,"y":y}]}); pg.wait_for_timeout(15)
    cdp.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]})
def human(pg,cdp,g,rng):
    cap=rng.randint(5,8)
    if g=="dusk": pg.evaluate("()=>{window.__seq=[];new MutationObserver(ms=>{for(const m of ms){const t=m.target;if(t.classList&&t.classList.contains('lant')&&t.classList.contains('on')&&document.getElementById('pgMsg').textContent==='Watch.')window.__seq.push(+t.dataset.lant);}}).observe(document.getElementById('pg'),{subtree:true,attributes:true,attributeFilter:['class']});}")
    t0=time.time()
    while time.time()-t0<(70 if g=="dusk" else 24) and pg.locator("#pg").count() and not pg.locator("#pg .pgend").count():
        if g in("meadow","ember"):
            pg.wait_for_timeout(rng.randint(260,520))
            vs=pg.evaluate(VIS,None); vs=[v for v in vs if "thorn" not in v[2] or rng.random()<.08]
            if not vs: continue
            pick=[v for v in vs if "gold" in v[2] or "puff" in v[2] or "log" in v[2]] or vs
            x,y,_=rng.choice(pick)
            if rng.random()<.12: x+=rng.choice([-40,40])
            pg.touchscreen.tap(x,y)
        elif g=="tide":
            a=pg.evaluate("()=>{const s=document.getElementById('pgStone'),c=document.getElementById('pgCalm');if(!s||!c)return null;const a=s.getBoundingClientRect(),z=c.getBoundingClientRect();return [a.left+a.width/2,z.left+z.width/2,performance.now()]}")
            pg.wait_for_timeout(30)
            b2=pg.evaluate("()=>{const s=document.getElementById('pgStone');if(!s)return null;const a=s.getBoundingClientRect();return [a.left+a.width/2,performance.now()]}")
            if a and b2:
                v=(b2[0]-a[0])/max(1,(b2[1]-a[2]))
                if abs(v)>0.02 and (a[1]-b2[0])/v>0:
                    tt=(a[1]-b2[0])/v
                    if tt<700:
                        pg.wait_for_timeout(int(max(0,tt+rng.gauss(0,75)))); pg.touchscreen.tap(*center(pg,"#pgSkip")); pg.wait_for_timeout(300)
        elif g=="frost":
            pg.wait_for_timeout(rng.randint(260,420))
            f=pg.evaluate("()=>{const F=[...document.querySelectorAll('#pg .flake:not(.hail)')].sort((a,b)=>parseFloat(b.style.top)-parseFloat(a.style.top));const f=F.find(x=>parseFloat(x.style.top)<document.getElementById('pg').clientHeight-80);return f?f.getBoundingClientRect().left+f.getBoundingClientRect().width/2:null}")
            if f:
                bx,_=center(pg,"#pgBasket"); R=pg.evaluate("()=>{const r=document.getElementById('pg').getBoundingClientRect();return r.top+r.height-60}")
                drag(pg,cdp,bx,R,f+rng.gauss(0,18))
        elif g=="dusk":
            pg.wait_for_timeout(80)
            if pg.evaluate("(document.getElementById('pgMsg')||{}).textContent||''")=="Your turn.":
                seq=pg.evaluate("window.__seq.slice()"); pg.evaluate("window.__seq=[]")
                err=len(seq)>cap and rng.random()<.75
                for k,v in enumerate(seq):
                    if err and k==len(seq)-1-rng.randint(0,2): v=(v+1)%4
                    pg.touchscreen.tap(*center(pg,f"#pg [data-lant='{v}']")); pg.wait_for_timeout(rng.randint(250,450))
                    if pg.evaluate("(document.getElementById('pgMsg')||{}).textContent||''")!="Your turn.": break
    pg.wait_for_timeout(1500)
res={}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,390,844); cdp=ctx.new_cdp_session(pg); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    for cname,cf in CFG.items():
        for ti,g in enumerate(NAMES):
            for r in range(RUNS):
                rng=random.Random(hash((cname,g,r))&0xffff)
                s=build(base,[1 if i==ti else 0 for i in range(5)]); s["seen"]=99; c=s["cards"][0]; c.update(cf); s["hearth"]["slots"]=[c["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":3}; s["games"]={"best":{},"played":0,"curioDay":""}
                pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click();const d=document.getElementById('pgDone');if(d)d.click()}"); pg.wait_for_timeout(300); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"hearth"); pg.tap("#hPlay"); pg.wait_for_timeout(300); pg.tap("#modal [data-game]"); pg.wait_for_timeout(300); pg.tap("#pgGo")
                human(pg,cdp,g,rng); sc=st(pg)["games"]["best"].get(g,0)
                res.setdefault(f"{g}/{cname}",[]).append(sc); closemodals(pg); pg.evaluate("()=>{const d=document.getElementById('pgDone');if(d)d.click()}"); pg.wait_for_timeout(200)
            print(g,cname,res[f"{g}/{cname}"],flush=True); json.dump(res,open("/tmp/claude-0/-home-claude/bd938e2e-992b-518b-b60c-27f2cca7a96c/scratchpad/human.json","w"))
    print("errors",pg._errs[:2]); b.close()
json.dump(res,open('/tmp/claude-0/-home-claude/bd938e2e-992b-518b-b60c-27f2cca7a96c/scratchpad/human.json','w'))
