from lib import *
# 0.20.0: wanders go to a realm on your map, curios belong to realms, and Forgelings make requests.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity|\{[a-z]+\}")
CREALM={"acorn":0,"flower":0,"feather":0,"mushroom":0,"leaf":1,"spark":1,"bone":1,"crystal":1,"shell":2,"pebble":2,"rain":2,"coin":2,"snow":3,"moon":3,"bell":3,"glimmer":3,"key":4,"candle":4,"thread":4,"map":4}
def ready(pg,s):
    s.pop("disc",None)  # each wander in this suite stands for a new day (0.33: one new find a day)
    setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
def back_now(pg):
    s=st(pg); s["wander"]["ready"]=0; ready(pg,s); tabto(pg,"hearth")
def collect(pg):
    pg.evaluate("document.getElementById('hCollect').click()"); pg.wait_for_timeout(500); return mt(pg)
def base_state(base,counts=(2,0,2,0,0)):
    s=build(base,list(counts)); s["seen"]=99; s["hearth"]["slots"]=[c["id"] for c in s["cards"][:3]]
    d0=datetime.date.fromisoformat(s["date"]); s["startDate"]=(d0-datetime.timedelta(days=10)).isoformat()
    s["wstat"]={"sent":0,"back":0}; s["request"]=None; s["reqLast"]=""; s["keepsR"]=[]; s["curios"]={}; s["wander"]=None
    for c in s["cards"]: c["bond"]=0
    return s
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # ---------- choosing where to wander ----------
    ready(pg,base_state(base)); tabto(pg,"hearth")
    pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(400); m=mt(pg)
    opts=pg.evaluate("[...document.querySelectorAll('#modal [data-wgo]')].map(b=>b.dataset.wgo)")
    rec("Wander","the wander button asks where, offering only realms on your map plus Anywhere",opts==["0","2","-1"] and "Meadow" in m and "Tide" in m and "Ember" not in m,(opts,m[:120]))
    rec("Wander","…and says how many of each realm's curios you have found","0 of 4 curios from here found" in m)
    pg.evaluate("document.querySelector('#modal [data-wgo=\"2\"]').click()"); pg.wait_for_timeout(400)
    w=st(pg)["wander"]; hm=pg.inner_text("#hmsg"); pg.evaluate("document.getElementById('hWOut').click()"); pg.wait_for_timeout(300); t=mt(pg); closemodals(pg)
    rec("Wander","choosing Tide sends them to Tide and says so",w and w["realm"]==2 and "heads off toward Tide" in hm and "out wandering in Tide" in t,(w,hm))
    back_now(pg); m=collect(pg); cu=[k for k in st(pg)["curios"]]
    rec("Wander","they come back from Tide with a Tide curio",len(cu)==1 and CREALM[cu[0]]==2 and "Back from Tide" in m,(cu,m[:60]))
    pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(400)
    # every Tide curio, then repeats stay in Tide
    for i in range(5):
        tabto(pg,"hearth"); pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(300); pg.evaluate("document.querySelector('#modal [data-wgo=\"2\"]').click()"); pg.wait_for_timeout(300)
        back_now(pg); collect(pg); pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(300)
    cu=st(pg)["curios"]
    rec("Wander","Tide gives each of its four curios before repeating, and never one from another realm",sorted(cu)==sorted(k for k,v in CREALM.items() if v==2) and sum(x["n"] for x in cu.values())==6,{k:v["n"] for k,v in cu.items()})
    tabto(pg,"hearth"); pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(300); pg.evaluate("document.querySelector('#modal [data-wgo=\"-1\"]').click()"); pg.wait_for_timeout(300)
    back_now(pg); m=collect(pg); new=[k for k in st(pg)["curios"] if CREALM[k]!=2]
    rec("Wander","Anywhere still finds something new from any realm",len(new)==1 and "Back from" not in m,(new,m[:50]))
    pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(300)
    # a wander already out when someone updates (no realm saved) still comes back fine
    s=st(pg); s["wander"]={"id":s["cards"][0]["id"],"start":0,"ready":0,"seed":12345,"notified":False}; ready(pg,s); tabto(pg,"hearth"); m=collect(pg)
    rec("Wander","a wander that started before the update comes back as usual",bool(m) and "Curios found" in m and not pg._errs,(m[:60],pg._errs[:1]))
    pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(300)
    # ---------- from the Map ----------
    ready(pg,base_state(base)); openmap(pg); pg.evaluate("()=>{const r=document.querySelector('[data-realm=\"2\"]')||document.querySelectorAll('[data-realm]')[1];r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); pg.wait_for_timeout(500)
    btn=pg.locator("#view-chronicle [data-wto]")
    rec("Map","a realm's page offers to send your Hearth Forgeling to wander there",btn.count()==1 and "to wander here" in btn.inner_text(),btn.count())
    to=int(btn.get_attribute("data-wto")); pg.evaluate("document.querySelector('#view-chronicle [data-wto]').click()"); pg.wait_for_timeout(500)
    rec("Map","…tapping it sends them, and the page then says they are out wandering there",st(pg)["wander"]["realm"]==to and pg.locator("#view-chronicle [data-wto]").count()==0 and "is out wandering in" in pg.inner_text("#view-chronicle"))
    s=st(pg); s["wander"]=None; s["hearth"]["sleep"]={"tier":1,"since":s["date"],"dream":0}; ready(pg,s); openmap(pg); pg.evaluate("()=>{const r=document.querySelectorAll('[data-realm]')[0];r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); pg.wait_for_timeout(400)
    rec("Map","…but not while your Forgelings are asleep",pg.locator("#view-chronicle [data-wto]").count()==0)
    # ---------- requests ----------
    s=base_state(base); s["cards"][0]["bond"]=3; ready(pg,s); tabto(pg,"hearth")
    rec("Request","no request before you have had a Forgeling come back from a wander",st(pg)["request"] is None)
    s=base_state(base); s["wstat"]={"sent":1,"back":1}; ready(pg,s); tabto(pg,"hearth")
    rec("Request","no request until someone by the fire is at least Friendly",st(pg)["request"] is None)
    s=base_state(base); s["wstat"]={"sent":1,"back":1}; s["cards"][0]["bond"]=3; s["startDate"]=s["date"]; ready(pg,s); tabto(pg,"hearth")
    rec("Request","no request on your first day",st(pg)["request"] is None)
    s=base_state(base); s["wstat"]={"sent":1,"back":1}; s["cards"][0]["bond"]=3; ready(pg,s); tabto(pg,"today"); tabto(pg,"hearth"); rq=st(pg)["request"]; t=pg.inner_text("#view-hearth")
    rec("Request","then, visiting the Hearth, a Friendly Forgeling asks for something from a realm on your map",rq and rq["cid"]==s["cards"][0]["id"] and rq["realm"] in (0,2),rq)
    nm=s["cards"][0]["name"]; rn={0:"Meadow",2:"Tide"}[rq["realm"]]
    rec("Request","…the Hearth says so and shows the request",f"{nm} has a small request." in pg.inner_text("#hmsg") and f"A request from {nm}" in t and f"from {rn}" in t and "requests never run out" in t and not JUNK.search(t),pg.inner_text("#hmsg"))
    tabto(pg,"today")
    rec("Request","…and Today's Hearth row mentions it",f"{nm} has a small request." in pg.inner_text("#btnHearth"))
    tabto(pg,"hearth"); pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(300)
    rec("Request","the wander choices point out which realm was asked for",f"{nm} asked for something from here." in pg.inner_text(f"#modal [data-wgo=\"{rq['realm']}\"]"))
    other=2 if rq["realm"]==0 else 0
    pg.evaluate(f"document.querySelector('#modal [data-wgo=\"{other}\"]').click()"); pg.wait_for_timeout(300); back_now(pg); m=collect(pg)
    rec("Request","wandering somewhere else does not answer it",st(pg)["request"] is not None and "request is done" not in m)
    pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(300)
    s=st(pg); s["request"]["made"]="2026-01-01"; ready(pg,s); tabto(pg,"hearth")
    rec("Request","requests never expire, even months later",st(pg)["request"] is not None and "A request from" in pg.inner_text("#view-hearth"))
    # answered by a different Forgeling
    s=st(pg); s["hearth"]["slots"]=[s["cards"][1]["id"]]+s["hearth"]["slots"]; s["hearth"]["slots"]=list(dict.fromkeys(s["hearth"]["slots"]))[:3]; ready(pg,s); tabto(pg,"hearth")
    who=pg.evaluate("document.querySelectorAll('#view-hearth [data-hslot]')[0].textContent")
    b0=st(pg)["cards"][0]["bond"]
    pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(300); pg.evaluate(f"document.querySelector('#modal [data-wgo=\"{rq['realm']}\"]').click()"); pg.wait_for_timeout(300)
    back_now(pg); m=collect(pg); s2=st(pg); K={0:"daisies",2:"shells"}[rq["realm"]]; KN={0:"Flower crown",2:"Shell necklace"}[rq["realm"]]
    rec("Request","anyone can answer it: the asker gains 3 bond and a thank-you keepsake arrives",f"{nm}’s request is done" in m and s2["cards"][0]["bond"]==b0+3 and K in s2["keepsR"] and KN in m,(who,m[-200:]))
    rec("Request","…the request is closed and dated",s2["request"] is None and s2["reqLast"]==s2["date"] and s2["reqDone"]==1)
    pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(300)
    hsheet(pg,"keeps"); chips=pg.evaluate("[...document.querySelectorAll('#modal [data-keep]')].map(b=>b.textContent)")
    rec("Keepsake","the thank-you keepsake is in the keepsake list for every Forgeling, with no level needed",KN in chips and pg.evaluate(f"!document.querySelector('#modal [data-keep=\"{K}\"]').disabled"),chips)
    rec("Keepsake","…and the list says more come from requests","More keepsakes come as thank-yous" in mt(pg))
    pg.evaluate(f"document.querySelector('#modal [data-keep=\"{K}\"]').click()"); pg.wait_for_timeout(300); closemodals(pg)
    rec("Keepsake","wearing it is saved",any(c["keep"]==K for c in st(pg)["cards"]))
    # the sprite really changes for each new keepsake
    PX="()=>{const c=document.getElementById('hearthCv');return [...c.getContext('2d').getImageData(0,0,128,72).data]}"
    s=st(pg); s["keepsR"]=["daisies","charm","shells","cap","lantern"]; s["hearth"]["slots"]=[s["cards"][0]["id"]]; s["settings"]["reduce"]=True; s["request"]=None; s["reqLast"]=s["date"]
    diffs={}
    for k in ("","daisies","charm","shells","cap","lantern"):
        s["cards"][0]["keep"]=k; ready(pg,s); tabto(pg,"hearth"); pg.wait_for_timeout(300); diffs[k]=pg.evaluate(PX)
    nd={k:sum(1 for i in range(0,len(diffs[""]),4) if abs(diffs[k][i]-diffs[""][i])+abs(diffs[k][i+1]-diffs[""][i+1])+abs(diffs[k][i+2]-diffs[""][i+2])>40) for k in diffs if k}
    rec("Keepsake","each of the five new keepsakes visibly changes the Forgeling",all(v>=6 for v in nd.values()),nd)
    # spacing between requests
    s=st(pg); s["settings"]["reduce"]=False; s["request"]=None; s["reqLast"]=s["date"]; ready(pg,s); tabto(pg,"hearth")
    rec("Request","no new request the same day one was answered",st(pg)["request"] is None)
    d0=datetime.date.fromisoformat(s["date"])
    s=st(pg); s["reqLast"]=(d0-datetime.timedelta(days=1)).isoformat(); ready(pg,s); tabto(pg,"hearth")
    rec("Request","…or the next day",st(pg)["request"] is None)
    s=st(pg); s["reqLast"]=(d0-datetime.timedelta(days=2)).isoformat(); ready(pg,s); tabto(pg,"hearth")
    rec("Request","…but two days later another may come",st(pg)["request"] is not None)
    # a request that grows the bond to a new level opens the bond-up note after Lovely
    s=st(pg); rq=s["request"]; a=[c for c in s["cards"] if c["id"]==rq["cid"]][0]; a["bond"]=13; s["wander"]={"id":s["hearth"]["slots"][0],"start":0,"ready":0,"seed":99,"notified":True,"realm":rq["realm"]}; ready(pg,s); tabto(pg,"hearth"); collect(pg)
    pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(900); m=mt(pg)
    rec("Request","if answering it grows the bond a level, the bond-up note and new chapter follow",("is now Devoted" in m) and "New chapter" in m,m[:120])
    closemodals(pg)
    # damaged saves
    for bad in ({"cid":99999,"realm":1},{"cid":"x"},"hello",{"cid":None,"realm":9},[1,2]):
        s=st(pg); s["request"]=bad; s["keepsR"]=["cap","cap","bogus",7]; s["wander"]={"id":s["cards"][0]["id"],"start":0,"ready":9e15,"seed":1,"notified":False,"realm":"far"}; ready(pg,s); tabto(pg,"hearth"); s2=st(pg)
        rec("Damaged",f"a damaged request ({bad!r}), keepsake list and wander destination are repaired",(s2["request"] is None or isinstance(s2["request"],dict)) and s2["keepsR"]==["cap"] and s2["wander"]["realm"]==-1 and not pg._errs,(s2["request"],s2["keepsR"],pg._errs[:1]))
    s=st(pg); s["request"]={"cid":s["cards"][0]["id"],"realm":2,"made":s["date"]}; ok_card=s["cards"][0]["id"]; s["cards"]=[c for c in s["cards"] if c["id"]!=ok_card]; s["hearth"]["slots"]=[c for c in s["hearth"]["slots"] if c!=ok_card]; s["wander"]=None; ready(pg,s)
    rec("Damaged","a request from a Forgeling that is no longer in the save is quietly dropped",st(pg)["request"] is None or st(pg)["request"]["cid"]!=ok_card)
    for k in ("request","reqLast","reqDone","keepsR"):
        s=st(pg); s.pop(k,None); ready(pg,s)
    rec("Damaged","an older save without any of the new fields loads and fills them in",all(k in st(pg) for k in ("request","reqLast","reqDone","keepsR")) and not pg._errs)
    rec("All","no page errors",not pg._errs,pg._errs[:2])
    ctx.close()
    # ---------- accessibility ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
        s=base_state(base); s["wstat"]={"sent":1,"back":1}; s["cards"][0]["bond"]=13; s["cards"][1]["dark"]=True; ready(pg,s); tabto(pg,"hearth")
        def axe(where):
            pg.wait_for_function("!document.body.classList.contains('arrive')"); pg.evaluate(AXE); v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
            bad.extend(f"{scheme}/{where}: {x}" for x in v)
        axe("hearth with request")
        pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(400); axe("where to")
        rq=st(pg)["request"]; pg.evaluate(f"document.querySelector('#modal [data-wgo=\"{rq['realm']}\"]').click()"); pg.wait_for_timeout(300); back_now(pg); collect(pg); axe("request done")
        pg.evaluate("document.getElementById('wcOk').click()"); pg.wait_for_timeout(900); axe("bond up after request")
        closemodals(pg); openmap(pg); pg.evaluate("()=>{const r=document.querySelectorAll('[data-realm]')[0];r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); pg.wait_for_timeout(400); axe("realm page")
        ctx.close()
    rec("A11y","axe: zero violations on the request, the wander choices, a finished request, the bond-up after it and a realm page, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_20"); print(sum(r["ok"] for r in RES),"/",len(RES))
