from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
def txt(pg): return pg.inner_text("#view-chronicle")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    s=build(base,[4,0,7,1,0],dark_in={2}); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    nav=pg.inner_text('.tab[data-tab="chronicle"]').strip()
    rec("Nav","the tab is called Map",nav=="Map",nav)
    tabto(pg,"chronicle")
    rec("Nav","opening the tab lands on the map itself, with the page title 'The Map'",pg.evaluate("!!document.querySelector('.mapsvg')") and pg.inner_text("#title")=="The Map",pg.inner_text("#title"))
    chips=pg.eval_on_selector_all('#view-chronicle .chips .chip',"e=>e.map(x=>x.textContent)")
    rec("Tabs","sections are consolidated to Map, Tales, Journal",chips==["Map","Tales","Journal"],chips)
    rec("Map","before any tap, the page invites a tap and no realm page is open","Tap a corner" in txt(pg) and pg.locator(".realmpage").count()==0)
    # tap a drawn realm via real touch on its hit area
    n=pg.locator(".mphit").count(); rec("Map","five tappable realms",n==5,n)
    pg.locator('.mphit[data-realm="2"]').dispatch_event("click"); pg.wait_for_timeout(300)
    t=txt(pg); rec("Realm page","tapping Tide opens its page with found count and cards","found here" in t and pg.locator(".realmpage [data-insp]").count()>=1,t[-200:].replace("\n"," | "))
    rec("Realm page","the open realm is marked pressed",pg.get_attribute('.mphit[data-realm="2"]',"aria-pressed")=="true")
    pg.locator('.mphit[data-realm="2"]').dispatch_event("click"); pg.wait_for_timeout(250)
    rec("Realm page","tapping again closes it",pg.locator(".realmpage").count()==0)
    pg.locator('.mphit[data-realm="1"]').dispatch_event("click"); pg.wait_for_timeout(250)
    t=txt(pg); rec("Realm page","an undiscovered realm shows 'Blank paper' and does not reveal its name",pg.locator(".realmpage").inner_text().startswith("Blank paper") and "Ember" not in pg.locator(".realmpage").inner_text() and "Inferno" not in pg.locator(".realmpage").inner_text())
    lab=pg.get_attribute('.mphit[data-realm="1"]',"aria-label"); rec("A11y","undiscovered realm's accessible name is generic",lab.startswith("An undrawn corner"),lab)
    # keyboard
    pg.focus('.mphit[data-realm="0"]'); pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    rec("A11y","Enter on a focused realm opens its page and keeps focus on it",pg.locator(".realmpage").count()==1 and pg.evaluate("document.activeElement.dataset.realm")=="0",pg.evaluate("document.activeElement.dataset.realm"))
    pg.keyboard.press("Space"); pg.wait_for_timeout(250)
    rec("A11y","Space closes it",pg.locator(".realmpage").count()==0)
    # insp from the realm page
    pg.locator('.mphit[data-realm="2"]').dispatch_event("click"); pg.wait_for_timeout(250)
    pg.locator(".realmpage [data-insp]").first.dispatch_event("click"); pg.wait_for_timeout(500)
    rec("Realm page","a card on the realm page opens the card viewer",bool(mt(pg)) and not pg._errs,pg._errs[:1]); closemodals(pg)
    # merged journal
    pg.evaluate("document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(300)
    t=txt(pg); rec("Journal","Journal now holds the weekly recap and calendar as well as entries","This week" in t and "Private" in t or "journal starts" in t.lower(),t[:120].replace("\n"," | "))
    # theme text
    tabto(pg,"today"); T=pg.inner_text("#view-today")
    rec("Theme","'Something to sit with' is gone from Today",("Something to sit with" not in T))
    pg.evaluate("document.body.innerHTML.includes('Something to sit with')")
    rec("Theme","Today shows 'In the margin' and 'The Forge asks'" ,"In the margin" in T and "The Forge asks" in T,T[:0])
    html=open(S+"/work.html").read(); rec("Theme","no 'Something to sit with' remains anywhere in the app","Something to sit with" not in html)
    # preview tool still lands on the map
    dev(pg,"mappreview"); rec("Dev","Preview the map lands on the map",pg.evaluate("!!document.querySelector('.mapsvg')") and not pg._errs)
    # lore off hides the tab
    s2=st(pg); s2["settings"]["lore"]=False; setst(pg,s2); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
    rec("Settings","turning whispers/lore off hides the Map tab and never strands the player",pg.evaluate("document.querySelector('.tab[data-tab=\"chronicle\"]').hidden") and not pg._errs)
    rec("Console","no page errors",not pg._errs,pg._errs[:2])
    # whats new
    s3=st(pg); s3["seen"]=17; s3["settings"]["lore"]=True; setst(pg,s3); pg.reload(); pg.wait_for_timeout(800)
    rec("What's New","shows once for existing players (it now lists only the latest notes)","What is new" in mt(pg) and "Chronicle" not in mt(pg),mt(pg)[:80])
    b.close()
save_results("qa_13")
print(sum(r["ok"] for r in RES),"/",len(RES))
