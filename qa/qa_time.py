from lib import *
import datetime
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
def keyoff(n): return (datetime.date.today()-datetime.timedelta(days=n)).isoformat()
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    def reopen(s,wait=900):
        s["seen"]=18; setst(pg,s); pg.reload(); pg.wait_for_timeout(wait); closemodals(pg)
    # ---- Sleeper's Welcome tiers
    today=pg.evaluate("()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}")
    tod=datetime.date.fromisoformat(today)
    for gap,exp in [(0,0),(1,0),(2,0),(3,1),(6,1),(7,2),(29,2),(30,3),(400,3)]:
        s=json.loads(json.dumps(base)); s["opens"]=[(tod-datetime.timedelta(days=gap)).isoformat()]
        if gap==0: s["opens"]=[today]
        reopen(s); got=(st(pg).get("hearth",{}).get("sleep") or {}).get("tier",0)
        rec("Sleep",f"away {gap} days -> tier {exp}",got==exp,got)
    # wake and welcome
    s=json.loads(json.dumps(base)); s["opens"]=[(tod-datetime.timedelta(days=9)).isoformat()]; w0=s["hearth"].get("welcomes",0); reopen(s); tabto(pg,"hearth"); pg.wait_for_timeout(500)
    rec("Sleep","the Hearth shows the sleeping view",pg.locator("#hearthCv").count()==1 or "asleep" in pg.inner_text("#view-hearth").lower() or bool(st(pg)["hearth"]["sleep"]))
    pg.evaluate("document.getElementById('hearthCv').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); pg.wait_for_timeout(4500)
    h=st(pg)["hearth"]; rec("Sleep","tapping the fire wakes them and counts one welcome",not h.get("sleep") and h.get("welcomes",0)==w0+1,(h.get("sleep"),h.get("welcomes")))
    rec("Sleep","no errors through the wake sequence",not pg._errs,pg._errs[:1])
    # a longer gap after a shorter, unwoken one only raises the tier
    s=json.loads(json.dumps(base)); s["hearth"]["sleep"]={"tier":2}; s["opens"]=[(tod-datetime.timedelta(days=4)).isoformat()]; reopen(s)
    rec("Sleep","a shorter later gap never lowers an unwoken deeper sleep",st(pg)["hearth"]["sleep"]["tier"]==2)
    # ---- the Quiet Thing (sprout)
    now=int(time.time()*1000)
    def quiet(hours_away,g0=0,shown=0):
        s=json.loads(json.dumps(base)); q=s["hearth"].get("quiet") or {"g":0,"b":0,"v":0,"shown":0,"ready":0,"pulse":0}
        seen=int(time.time()*1000)-int(hours_away*3600e3)
        q.update({"g":g0,"shown":shown,"ready":0,"pulse":0,"seenAt":seen}); s["hearth"]["quiet"]=q; s["opens"]=[today]; s["seen"]=18
        c2,p2=newpage(b); p2.set_default_timeout(7000)
        p2.add_init_script("if(!sessionStorage.getItem('__i')){localStorage.setItem('forge-app-v1',%s);localStorage.setItem('forge-app-v1-seen','%d');sessionStorage.setItem('__i','1')}"%(json.dumps(json.dumps(s)),seen))
        p2.goto(P); p2.wait_for_timeout(1000); r=st(p2)["hearth"]["quiet"]; pg._errs+=p2._errs; c2.close(); return r
    for hrs,exp in [(1,0),(2.9,0),(3.2,3.2),(10,10),(47,47),(120,48),(1000,48)]:
        q=quiet(hrs); rec("Sprout",f"away {hrs}h grows {exp}h (min 3h, cap 48h per absence)",abs(q["g"]-exp)<0.6,round(q["g"],2))
    q=quiet(0.2,g0=50); rec("Sprout","opening the app again soon after does not grow it",abs(q["g"]-50)<0.1,q["g"])
    q=quiet(30,g0=125); rec("Sprout","growth stops at the bloom (140) and arms the reveal",q["g"]==140 and q["ready"]==1,(q["g"],q["ready"]))
    q=quiet(0.1,g0=140,shown=1); 
    q2=quiet(5,g0=140,shown=1); rec("Sprout","after a shown bloom, the next absence starts a fresh sprout",q2["g"]<=6 and q2["shown"]==0,(q2["g"],q2["shown"]))
    rec("Sprout","no errors",not pg._errs,pg._errs[:1])
    # ---- Wanderers and curios
    s=json.loads(json.dumps(base)); s["opens"]=[today]; s["wander"]={"id":s["cards"][0]["id"],"start":now-4*3600e3,"ready":now-3600e3,"seed":12345,"notified":False}; s["wstat"]=s.get("wstat") or {"sent":1,"back":0}; reopen(s); tabto(pg,"hearth"); pg.wait_for_timeout(400)
    rec("Wander","a Forgeling whose time has passed shows as back",pg.locator("#hCollect").count()==1,pg.inner_text("#view-hearth")[:80].replace("\n"," | "))
    pg.evaluate("document.getElementById('hCollect').click()"); pg.wait_for_timeout(500)
    t=mt(pg); rec("Wander","collecting gives a curio sheet with no junk",("curio" in t.lower() or "pile" in t.lower()) and not JUNK.search(t),t[:80].replace("\n"," | "))
    closemodals(pg); s2=st(pg); rec("Wander","wander state is cleared and the curio is recorded",s2.get("wander") is None and len(s2["curios"])==1,(s2.get("wander"),len(s2["curios"])))
    # not-ready wander is not collectable; sending uses the 3h window
    s=json.loads(json.dumps(base)); s["opens"]=[today]; s["wander"]={"id":s["cards"][0]["id"],"start":now,"ready":now+3*3600e3,"seed":7,"notified":False}; s["wstat"]={"sent":1,"back":0}; reopen(s); tabto(pg,"hearth"); pg.wait_for_timeout(300)
    hv=pg.inner_text("#view-hearth"); rec("Wander","an unfinished wander shows time left, with no collect button",pg.locator("#hCollect").count()==0 and bool(re.search(r"\d",hv)) and ("wander" in hv.lower()),hv[:300].replace("\n"," | "))
    # wander for a card that no longer exists
    s=json.loads(json.dumps(base)); s["opens"]=[today]; s["wander"]={"id":99999,"start":now,"ready":now-1,"seed":7,"notified":False}; reopen(s)
    rec("Wander","a wanderer whose card is gone is dropped without errors",st(pg).get("wander") is None and not pg._errs,pg._errs[:1])
    # all 20 curios then duplicates
    s=json.loads(json.dumps(base)); s["opens"]=[today]; s["wstat"]={"sent":0,"back":0}; s["curios"]={}; reopen(s)
    for i in range(23):
        s=st(pg); s.pop("disc",None); s["wander"]={"id":s["cards"][0]["id"],"start":now-4*3600e3,"ready":now-3600e3,"seed":1000+i*977,"notified":False}; setst(pg,s); pg.reload(); pg.wait_for_timeout(450); closemodals(pg); tabto(pg,"hearth"); pg.wait_for_timeout(150)
        try: pg.evaluate("document.getElementById('hCollect').click()"); pg.wait_for_timeout(200); closemodals(pg)
        except Exception: break
    s=st(pg); rec("Wander","23 wanders find all 20 curios exactly once each before any repeat",len(s["curios"])==20 and sum(c["n"] for c in s["curios"].values())==23 and not pg._errs,(len(s["curios"]),sum(c["n"] for c in s["curios"].values()),pg._errs[:1]))
    b.close()
save_results("qa_time"); print(sum(r["ok"] for r in RES),"/",len(RES))
