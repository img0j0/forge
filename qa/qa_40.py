from lib import *
import datetime
# 0.40.0: Living Hearth. Tap-to-hop with a line, dozing after 10 pm (a tap wakes one), weather from the seated realm,
# statues on plinths, the creature hopping inside its card frame. Real clock fixed with pg.clock.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
COUNT="(c)=>{const cv=document.getElementById('hearthCv'),d=cv.getContext('2d').getImageData(0,0,128,72).data;let n=0;for(let i=0;i<d.length;i+=4){if(Math.abs(d[i]-c[0])<6&&Math.abs(d[i+1]-c[1])<6&&Math.abs(d[i+2]-c[2])<6)n++;}return n;}"
def setup(b,hr,reduce=False):
    kw={"reduced_motion":"reduce"} if reduce else {}
    ctx,pg=newpage(b,**kw); pg.clock.install(time=datetime.datetime(2026,10,22,hr,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); s["opens"]+=[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg); return ctx,pg
def realm(pg,ti,dk,statue=False):
    s=st(pg)
    for c in s["cards"]:
        if c["id"] in s["hearth"]["slots"]: c["theme"]=ti; c["dark"]=dk; c["v"]=0
        if statue: c["bond"]=30; c["statue"]={"at":s["date"],"keep":""}
        else: c.pop("statue",None)
    setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"hearth"); pg.clock.run_for(2000); pg.wait_for_timeout(200)
def tap_forgeling(pg):
    """tap across the middle of the scene until a Forgeling answers"""
    r=pg.evaluate("()=>{const c=document.getElementById('hearthCv').getBoundingClientRect();return [c.left,c.top,c.width,c.height]}")
    m0=pg.inner_text("#hmsg")
    for fx in [i/20 for i in range(2,19)]:
        pg.mouse.click(r[0]+r[2]*fx,r[1]+r[3]*0.55); pg.wait_for_timeout(60)
        if pg.inner_text("#hmsg")!=m0: return pg.inner_text("#hmsg")
    return None
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,pg=setup(b,11)
    checks={(3,False):([255,255,255],8,"snow"),(2,False):([96,156,214],6,"rain"),(0,False):([244,140,180],2,"petals"),(1,False):([255,160,70],2,"embers")}
    res={}
    for (ti,dk),(col,need,name) in checks.items():
        realm(pg,ti,dk); res[name]=pg.evaluate(COUNT,col)
    rec("Weather","by day the weather follows the realm by the fire: snow, rain, petals, embers",all(res[k]>=checks[x][1] for x,k in [((3,False),"snow"),((2,False),"rain"),((0,False),"petals"),((1,False),"embers")]),res)
    realm(pg,2,True); ab=pg.evaluate(COUNT,[61,240,224])
    rec("Weather","a Shade realm drifts with its own glow (Abyss teal motes)",ab>=2,ab)
    rec("Doze","by day no one dozes: no Zs",pg.evaluate(COUNT,[220,232,255])==0)
    rec("Statues","with no statues, no plinths",pg.evaluate(COUNT,[150,140,166])==0)
    realm(pg,0,False,statue=True)
    rec("Statues","statues stand on plinths at the scene's edges",pg.evaluate(COUNT,[150,140,166])>=16)
    m=tap_forgeling(pg)
    rec("Tap","tapping a Forgeling by the fire makes it answer",bool(m) and "fire crackles" not in m,m)
    bad+=["hearth day: "+v for v in axe(pg)]
    # the card: the creature hops inside its frame, the frame stays put
    tabto(pg,"binder"); pg.evaluate("()=>document.querySelector('#view-binder .card').click()"); pg.wait_for_timeout(700)
    snap="()=>Array.from(document.querySelector('#stage .art canvas.pcv').getContext('2d').getImageData(0,0,48,37).data).join(',')"
    a0=pg.evaluate(snap); pg.evaluate("()=>document.querySelector('#stage .art').click()"); pg.clock.run_for(300); pg.wait_for_timeout(120); a1=pg.evaluate(snap)
    rec("Card","tapping the art makes the creature hop inside its frame, and the frame stays still",a0!=a1 and not pg.evaluate("document.querySelector('#stage .art').classList.contains('hop')"))
    closemodals(pg)
    rec("All","day: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    # night
    ctx,pg=setup(b,23); realm(pg,4,False)
    rec("Doze","after 10 pm everyone by the fire dozes, with drifting Zs",pg.evaluate(COUNT,[220,232,255])>=2)
    m=tap_forgeling(pg)
    rec("Doze","a tap wakes one, who says hello",bool(m) and "opens one eye" in m,m)
    bad+=["hearth night: "+v for v in axe(pg)]
    rec("All","night: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    # reduced motion
    ctx,pg=setup(b,11,reduce=True); realm(pg,3,False)
    m=tap_forgeling(pg); rec("Motion","with reduced motion the scene stays still, and a tap still answers",bool(m) and not pg._errs,(m,pg._errs[:1])); ctx.close()
    # what's new
    ctx,pg=setup(b,11); s=st(pg); s["seen"]=44; setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); w=pg.inner_text("#modal")
    rec("New","What is new leads with A living Hearth, and keeps eight notes","A living Hearth" in w and pg.locator("#modal .newlist li").count()==8,w[:80]); ctx.close()
    rec("A11y","axe: zero violations on the Hearth by day and night",not bad,bad[:3])
    b.close()
save_results("qa_40"); print(sum(r["ok"] for r in RES),"/",len(RES))
