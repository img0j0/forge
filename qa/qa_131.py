from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    rec("Fonts","no request leaves the device (fonts are bundled)",pg._reqs==[],pg._reqs[:2])
    ok=pg.evaluate("Promise.all(['16px Fredoka','700 16px \"Nunito Sans\"','16px \"Press Start 2P\"','16px VT323'].map(f=>document.fonts.load(f))).then(r=>r.every(x=>x.length>0))")
    rec("Fonts","all four bundled families load from the page itself",ok)
    s=build(base,[4,2,3,0,0]); s["seen"]=18; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    T=pg.inner_text("#view-today")
    # 0.43: the Map row left Today; its news lives on the Map tab itself
    rec("Today","no Map row on Today (0.43): the margin news is on the Map",pg.locator("#btnMapGo").count()==0,T[:120].replace("\n"," | "))
    openmap(pg); rec("Today","the Map tab opens the map",pg.evaluate("!!document.querySelector('.mapsvg')") and pg.inner_text("#title")=="The Map")
    # not shown with no cards or lore off
    s2=build(base,[0,0,0,0,0]); s2["seen"]=17; setst(pg,s2); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
    rec("Today","no Map card before the first Forgeling",pg.locator("#btnMapGo").count()==0)
    s3=build(base,[4,2,3,0,0]); s3["seen"]=17; s3["settings"]["lore"]=False; setst(pg,s3); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
    rec("Today","no Map card when lore is off",pg.locator("#btnMapGo").count()==0)
    # binder calling note
    s4=build(base,[6,0,0,0,0]); s4["seen"]=17
    for i,c in enumerate(s4["cards"]): c["v"]=2 if i<6 else 0
    setst(pg,s4); pg.reload(); pg.wait_for_timeout(600); closemodals(pg); tabto(pg,"binder")
    rec("Binder","no calling note while showing All",pg.locator("#view-binder .calling").count()==0)
    pick_calling(pg,"2")
    t=pg.inner_text("#view-binder"); rec("Binder","choosing a type shows its note (6 found unlocks the rumor tier)",pg.locator("#view-binder .calling").count()==1 and "rumor" in t.lower(),t[t.find("Depth"):][:100].replace("\n"," | "))
    pick_calling(pg,"5")
    rec("Binder","a type with none found invites the first one",pg.locator("#view-binder .calling").count()==1 and "Find a" in pg.inner_text("#view-binder"))
    rec("Console","no page errors",not pg._errs,pg._errs[:2])
    b.close()
save_results("qa_131"); print(sum(r["ok"] for r in RES),"/",len(RES))
