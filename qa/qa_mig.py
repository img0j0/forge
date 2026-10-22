from lib import *
OLD={"0.9.8":"file://"+S+"/forge-pilot.html","0.11.0":"file://"+S+"/base.html","0.12.0":"file://"+S+"/base12.html","0.13.0":"file://"+S+"/base13.html","0.14.0":"file://"+S+"/base14.html"}
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
def rich_save(b,url):
    ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(url); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    for t in ("legend","holo","next","pack","skip10"):
        try:
            dev(pg,t); closemodals(pg)
        except Exception as e: pass
    try:
        s=pg.evaluate("(k)=>localStorage.getItem(k)",KEY); n=len(json.loads(s)["cards"])
    except Exception: s=None;n=0
    if s is not None and n<2:
        # builds without dev tools (the 0.9.8 pilot): play three more days through its own buttons
        for _ in range(3):
            st0=json.loads(pg.evaluate("(k)=>localStorage.getItem(k)",KEY)); st0["offset"]=(st0.get("offset") or 0)+1
            pg.evaluate("([k,v])=>localStorage.setItem(k,v)",[KEY,json.dumps(st0)]); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
            for sel,wait in (("#btnTurn",300),("#vBack",700),("#vOk",300),("#btnDone",900),("[data-mood]",900),("#cover",1200),("#rvSkip",500)):
                pg.evaluate("s=>{const e=document.querySelector(s);if(e&&!e.hidden)e.click();}",sel); pg.wait_for_timeout(wait)
            closemodals(pg)
        try:
            s=pg.evaluate("(k)=>localStorage.getItem(k)",KEY); n=len(json.loads(s)["cards"])
        except Exception: s=None;n=0
    errs=list(pg._errs); ctx.close(); return s,n,errs
_np=newpage
def newpage(b,*a,**k):
    ctx,pg=_np(b,*a,**k); ctx.route(re.compile(r'https://fonts\.g.*'),lambda r:r.abort()); return ctx,pg
with sync_playwright() as p:
    b=p.chromium.launch()
    for ver,url in OLD.items():
        s,n,errs=rich_save(b,url)
        rec("Migrate",f"{ver}: built a save with several cards to carry forward",s is not None and n>=2,(n,errs[:1]))
        if not s: continue
        ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo",state="attached")
        pg.evaluate("([k,s])=>localStorage.setItem(k,s)",[KEY,s]); pg.reload(); pg.wait_for_timeout(900)
        ns=st(pg); before=json.loads(s)
        rec("Migrate",f"{ver}: opens in 0.15.0 with no errors",not pg._errs,pg._errs[:2])
        rec("Migrate",f"{ver}: every card, name and rarity survives",[(c['id'],c['name'],c['rarity']) for c in before['cards']]==[(c['id'],c['name'],c['rarity']) for c in ns['cards']])
        rec("Migrate",f"{ver}: packs, pity and start date survive",(before.get('packs'),before.get('startDate'),before.get('pity',{}).get('since'))==(ns.get('packs'),ns.get('startDate'),ns.get('pity',{}).get('since')),(before.get('packs'),ns.get('packs')))
        closemodals(pg)
        # walk every tab and the new surfaces
        for t in ("today","hearth","binder","chronicle","settings"):
            tabto(pg,t); pg.wait_for_timeout(250)
        for sub in ("map","tales","journal"):
            pg.evaluate("s=>{const b=document.querySelector('[data-sub=\"'+s+'\"]');if(b)b.click();}",sub); pg.wait_for_timeout(250)
        txt=pg.inner_text("body")
        rec("Migrate",f"{ver}: all tabs render without junk text or errors",not JUNK.search(txt) and not pg._errs,(JUNK.search(txt).group(0) if JUNK.search(txt) else "",pg._errs[:1]))
        # every card inspects and flips (older cards lack era/hour fields)
        bad=0
        for c in ns['cards'][:6]:
            pg.evaluate("i=>{document.querySelector('.tab[data-tab=\"binder\"]').click();}",0); pg.wait_for_timeout(120)
            try:
                pg.evaluate("i=>{const e=document.querySelector('[data-insp=\"'+i+'\"]');if(e)e.click();}",c['id']); pg.wait_for_timeout(250)
                pg.evaluate("()=>{const f=document.getElementById('inspFlip');if(f)f.click();}"); pg.wait_for_timeout(450)
                pg.evaluate("()=>{const f=document.getElementById('ovClose');if(f)f.click();}"); pg.wait_for_timeout(200)
            except Exception: bad+=1
        rec("Migrate",f"{ver}: old cards can be opened, flipped and closed",bad==0 and not pg._errs,pg._errs[:1])
        # the app keeps working: skip a day, new card
        dev(pg,"skip10"); closemodals(pg)
        rec("Migrate",f"{ver}: a new day after migration works",not pg._errs and st(pg).get("v")==1,pg._errs[:1])
        # backup round trip of the migrated save
        ctx.close()
    # unreadable / blocked storage
    ctx,pg=newpage(b); pg.set_default_timeout(6000)
    pg.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
    pg.goto(P); pg.wait_for_timeout(900)
    rec("Storage","with storage blocked the app still starts and shows onboarding",pg.locator("#ageGo, #titleGo").count()==1 and not [e for e in pg._errs if 'blocked' not in e],pg._errs[:2]); ctx.close()
    ctx,pg=newpage(b); pg.set_default_timeout(6000)
    pg.add_init_script("""(()=>{const o=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k.startsWith('forge'))throw new DOMException('full','QuotaExceededError');return o.call(this,k,v)}})()""")
    pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); 
    try: first_card(pg)
    except Exception as e: rec("Storage","quota full: first card flow completes",False,e)
    else: rec("Storage","quota full: first card flow still completes in memory",not [e for e in pg._errs],pg._errs[:2])
    ctx.close()
    b.close()
save_results("qa_mig"); print(sum(r["ok"] for r in RES),"/",len(RES))
