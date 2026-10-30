from lib import *
# 0.18.0 design rules: one hero and one filled button per Today state, quiet grouped rows, 44px targets,
# Hearth extras folded but working, Binder counters as plain text.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
def primaries(pg):
    return pg.evaluate("()=>[...document.querySelectorAll('#view-today .primary')].filter(b=>b.offsetParent!==null).map(b=>b.id||b.textContent.trim())")
def small_targets(pg,view):
    return pg.evaluate("""v=>[...document.querySelectorAll('#view-'+v+' button, #view-'+v+' summary')].filter(b=>b.offsetParent!==null&&!b.disabled).map(b=>[Math.round(b.getBoundingClientRect().height),(b.id||b.className||b.tagName)+':'+b.textContent.trim().slice(0,20)]).filter(x=>x[0]<44)""",view)
with sync_playwright() as p:
    b=p.chromium.launch()
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,390,844,color_scheme=scheme); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        s=build(base,[4,3,5,2,3],dark_in={1,3}); s["seen"]=21; s["packs"]=1; s["progress"]=2
        s["hearth"]["slots"]=[s["cards"][0]["id"],s["cards"][5]["id"]]
        s["status"]="fresh"; s["todayCard"]=None; s["history"]=[h for h in s["history"] if h["date"]!=s["date"]]
        setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
        L=scheme
        rec("Today",f"{L}: fresh day shows one hero and exactly one filled button",pg.locator("#view-today .hero").count()==1 and primaries(pg)==["btnTurnGo"],primaries(pg))
        rec("Today",f"{L}: the waiting pack is a row, not a second big button",pg.locator("#view-today .rowl#btnPack").count()==1)
        pg.evaluate("document.getElementById('btnTurn').click()"); pg.wait_for_timeout(500); m=mt(pg)
        rec("Today",f"{L}: tapping the hero card back opens today's card",bool(m) and "Today's card" in m,m[:60])
        closemodals(pg); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        pg.evaluate("()=>{if(!document.getElementById('modal').hidden){const b=document.getElementById('vBack');if(b)b.click();}}"); pg.wait_for_timeout(800); closemodals(pg)
        pg.evaluate("()=>{const m=document.getElementById('modal');if(!m.hidden){const o=m.querySelector('#vOk');if(o)o.click();}}"); pg.wait_for_timeout(400)
        if st(pg)["status"]!="revealed":
            pg.evaluate("document.getElementById('btnTurnGo').click()"); pg.wait_for_timeout(500); pg.evaluate("document.getElementById('vBack').click()"); pg.wait_for_timeout(900); closemodals(pg)
            pg.evaluate("()=>{const o=document.querySelector('#modal #vOk');if(o)o.click();}"); pg.wait_for_timeout(400)
        rec("Today",f"{L}: revealed state shows the task as a card face with one filled button",pg.locator("#view-today .taskface").count()==1 and primaries(pg)==["btnDone"],primaries(pg))
        pg.evaluate("document.getElementById('btnDone').click()"); pg.wait_for_timeout(900)
        for _ in range(6):
            for sel in ("[data-mood]","#cover","#rvSkip","[data-close]"):
                if pg.locator("#modal "+sel).count(): pg.evaluate("s=>document.querySelector('#modal '+s).click()",sel); pg.wait_for_timeout(700)
        closemodals(pg); tabto(pg,"today")
        rec("Today",f"{L}: after the calling, the new Forgeling is the hero and the pack is the one filled button",pg.locator("#view-today .hero #btnShowToday").count()==1 and primaries(pg)==["btnPack"] and "joined your binder" in pg.inner_text("#view-today .hero"),primaries(pg))
        rec("Today",f"{L}: a new player gets a Hearth row (something waits there), and no Map row (0.43)",pg.locator("#view-today .rowl#btnHearth").count()==1 and pg.locator("#view-today .rowl#btnMapGo").count()==0)
        pg.evaluate("document.getElementById('btnHearth').click()"); pg.wait_for_timeout(500)
        rec("Today",f"{L}: …the Hearth row goes to the Hearth",pg.evaluate("!document.getElementById('view-hearth').hidden"))
        tabto(pg,"today")
        rec("Today",f"{L}: no junk text",not JUNK.search(pg.inner_text("#view-today")))
        # rest state
        s=st(pg); s["status"]="rest"; s["history"]=[h for h in s["history"] if h["date"]!=s["date"]]+[{"date":s["date"],"status":"rest","v":s["todayV"]}]; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
        rec("Today",f"{L}: resting shows no filled button at all",primaries(pg)==[] and "Resting today" in pg.inner_text("#view-today .hero"),primaries(pg))
        # touch targets
        for v in ("today","hearth","binder","chronicle","settings"):
            tabto(pg,v); sm=small_targets(pg,v)
            rec("Touch",f"{L}: every visible control on {v} is at least 44px tall",not sm,sm[:3])
        # hearth folding
        tabto(pg,"hearth")
        rec("Hearth",f"{L}: keepsakes, the curio shelf and the things by the fire are buttons that open sheets (0.43)",pg.locator("#view-hearth details").count()==0 and all(pg.locator(x).count()==1 for x in ("#hShelf","#hFurn","#hKeeps")))
        hsheet(pg,"keeps"); ok1=pg.locator("#modal [data-keep]").first.is_visible() and pg.locator("#modal [data-bd]").first.is_visible(); closemodals(pg)
        hsheet(pg,"shelf"); ok2=pg.locator("#modal .shelf").is_visible(); closemodals(pg)
        rec("Hearth",f"{L}: they show keepsakes, backdrops and the shelf",ok1 and ok2)
        hsheet(pg,"keeps"); pg.evaluate("document.querySelector('#modal [data-bd=\"\"]').click()"); pg.wait_for_timeout(400)
        rec("Hearth",f"{L}: a backdrop chip works from inside the sheet",not pg._errs and st(pg)["hearth"]["bd"]=="",pg._errs[:1]); closemodals(pg)
        # binder
        tabto(pg,"binder"); t=pg.inner_text("#view-binder")
        rec("Binder",f"{L}: counters are one sentence, not tappable-looking chips",pg.locator("#view-binder .stat-chip").count()==0 and re.search(r"\d+ Forgelings, \d+ rare or better\. \d+ of 12 callings and \d+ of 10 realms found\.",t) is not None,t[:120])
        rec("All",f"{L}: no page errors",not pg._errs,pg._errs[:2])
        ctx.close()
    # narrowest common phone
    ctx,pg=newpage(b,320,640); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    ov=pg.evaluate("()=>document.documentElement.scrollWidth>document.documentElement.clientWidth")
    hb=pg.evaluate("()=>{const h=document.querySelector('#view-today .hero');return h?Math.round(h.getBoundingClientRect().width):0}")
    rec("Layout","at 320px wide the hero fits with no sideways scrolling",not ov and 0<hb<=320,(ov,hb))
    ctx.close(); b.close()
save_results("qa_18"); print(sum(r["ok"] for r in RES),"/",len(RES))
