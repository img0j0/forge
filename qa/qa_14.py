from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); c=s["cards"][-1]
    rec("Kept","a new card records the hour it was found",isinstance(c.get("kh"),int) and 0<=c["kh"]<=23,c.get("kh"))
    s["seen"]=18; setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
    cid=c["id"]
    pg.evaluate("i=>document.querySelector('[data-insp=\"'+i+'\"]').click()",cid); pg.wait_for_timeout(500)
    t=mt(pg); rec("Kept","a young card says when its second reading opens, calmly","A second reading opens in 14 days" in t,t[-160:].replace("\n"," | "))
    rec("Kept","no button yet for a young card",pg.locator('#modal [data-kept]').count()==0)
    pg.evaluate("document.getElementById('ovClose').click()"); pg.wait_for_timeout(300)
    dev(pg,"agecard"); closemodals(pg)
    s=st(pg); c=s["cards"][-1]; rec("Kept","the dev tool ages the card and sets an hour and a journal line",keptAgeOk:=(c["kh"]==19 and c["date"] in s["journal"]),c["date"])
    pg.evaluate("i=>document.querySelector('[data-insp=\"'+i+'\"]').click()",cid); pg.wait_for_timeout(500)
    rec("Kept","an old card shows a Second reading button",pg.locator('#modal [data-kept]').count()==1 and "opens in" not in mt(pg))
    pg.evaluate("document.querySelector('#modal [data-kept]').click()"); pg.wait_for_timeout(400)
    t=mt(pg); rec("Kept","the reading states the hour, the era, and quotes the journal line","at dusk" in t and "The world was in the" in t and "Tired, but I kept my promise." in t,t[:300].replace("\n"," | "))
    rec("Kept","no junk text in the reading",not JUNK.search(t))
    rec("Kept","it has a dialog name",pg.evaluate("!!document.querySelector('#modal [role=dialog]').getAttribute('aria-labelledby')"))
    pg.evaluate("document.getElementById('keptBack').click()"); pg.wait_for_timeout(500)
    rec("Kept","Close returns to the card, not to nothing","Flip card" in mt(pg),mt(pg)[:40])
    pg.evaluate("document.getElementById('ovClose').click()"); pg.wait_for_timeout(300)
    # tales entry
    tabto(pg,"chronicle"); pg.evaluate("document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(300)
    rec("Kept","Tales lists the Second reading button for the old card",pg.locator('#view-chronicle [data-kept]').count()==1)
    pg.evaluate("document.querySelector('#view-chronicle [data-kept]').click()"); pg.wait_for_timeout(300)
    rec("Kept","opening from Tales then Close closes cleanly","Second reading" in mt(pg)); pg.evaluate("document.getElementById('keptBack').click()"); pg.wait_for_timeout(300)
    rec("Kept","…and does not pop a card open",pg.evaluate("document.getElementById('modal').hidden"))
    # no journal that day, no hour (legacy card), dark mood
    s=st(pg); c=s["cards"][-1]; del c["kh"]; s["journal"].pop(c["date"],None); c["dark"]=True; c["tale"]=""; setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
    pg.evaluate("i=>{document.querySelector('.tab[data-tab=\"binder\"]').click();}",cid); pg.wait_for_timeout(300)
    pg.evaluate("i=>document.querySelector('[data-insp=\"'+i+'\"]').click()",cid); pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('#modal [data-kept]').click()"); pg.wait_for_timeout(300); t=mt(pg)
    rec("Kept","a legacy card without an hour still reads well, and says so kindly when no words were written","You left no words that day" in t and "at dusk" not in t and not JUNK.search(t),t[:200].replace("\n"," | "))
    # damaged values
    for bad in ("x",99,-5,None,1.7):
        s=st(pg); s["cards"][-1]["kh"]=bad; setst(pg,s); pg.reload(); pg.wait_for_timeout(500); closemodals(pg)
        e=len(pg._errs); ok=st(pg)["cards"][-1].get("kh"); rec("Kept",f"damaged hour {bad!r} is repaired on load",(ok is None or (isinstance(ok,int) and 0<=ok<=23)) and not pg._errs,ok)
    rec("Console","no page errors",not pg._errs,pg._errs[:2])
    b.close()
save_results("qa_14"); print(sum(r["ok"] for r in RES),"/",len(RES))
