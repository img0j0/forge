from lib import *
CLK="""(()=>{const R=Date;window.__off=+sessionStorage.getItem('__off')||0;class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+window.__off)}static now(){return R.now()+window.__off}}window.Date=D;})()"""
def walk(pg):
    for t in ["today","binder","hearth","chronicle","settings","hearth","today"]:
        pg.evaluate("t=>{const e=document.querySelector('.tab[data-tab=\"'+t+'\"]');if(e)e.click()}",t); pg.wait_for_timeout(100)
        if t=="chronicle":
            for s in ["map","realms","tales"]: pg.evaluate("(s)=>{const b=document.querySelector('[data-sub=\"'+s+'\"]');if(b)b.click()}",s); pg.wait_for_timeout(80)
        pg.evaluate("()=>{const m=document.getElementById('modal');if(m&&!m.hidden){const b=m.querySelector('[data-close]');if(b)b.click();}}")
def usable(pg): return pg.evaluate("()=>{const gate=!!(document.getElementById('ageGo')||document.getElementById('titleGo'));const tabs=!!document.querySelector('.tabs');const app=document.querySelector('.app');return gate||(tabs&&app&&app.innerText.trim().length>10)}")
def boot(b,val,init=None):
    ctx,pg=newpage(b)
    if init: ctx.add_init_script(init)
    pg.set_default_timeout(3000); pg.goto(P); pg.wait_for_timeout(300)
    if val is not None: pg.evaluate("([k,s])=>localStorage.setItem(k,typeof s==='string'?s:JSON.stringify(s))",[KEY,val]); pg.reload(); pg.wait_for_timeout(700)
    return ctx,pg
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); dev(pg,"week"); closemodals(pg); pg.reload(); pg.wait_for_timeout(800); closemodals(pg); base=st(pg)
    # ---- smoke: every developer tool, then every screen
    tools=pg.evaluate("[...document.querySelectorAll('[data-tool]')].map(e=>e.dataset.tool).filter(t=>t!=='reset')")
    bad=[]
    for t in tools:
        try: dev(pg,t); closemodals(pg)
        except Exception as e: bad.append((t,str(e)[:60]))
    walk(pg)
    rec("Smoke",f"all {len(tools)} developer tools run without errors",not bad and not pg._errs,(bad,pg._errs[:1]))
    # ---- backup round trip
    tabto(pg,"settings"); pg.evaluate("document.getElementById('btnExport').click()"); pg.wait_for_timeout(300); exp=pg.input_value("#expText"); closemodals(pg)
    before=st(pg); s2=json.loads(json.dumps(before)); s2["cards"]=s2["cards"][:1]; setst(pg,s2); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    tabto(pg,"settings"); pg.evaluate("document.getElementById('btnRestore').click()"); pg.wait_for_timeout(300); pg.fill("#resText",exp)
    pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(200); pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(700)
    after=st(pg); rec("Backup","export then restore returns every card, identical",len(after["cards"])==len(before["cards"]) and all(json.dumps(a,sort_keys=True)==json.dumps(c,sort_keys=True) for a,c in zip(before["cards"],after["cards"])),(len(after["cards"]),len(before["cards"])))
    rec("Backup","restored game opens the Map without errors",(openmap(pg) or True) and not pg._errs,pg._errs[:1])
    ctx.close()
    # ---- overnight rollover
    ctx,pg=newpage(b); ctx.add_init_script(CLK); pg.set_default_timeout(5000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); d0=st(pg)["date"]
    off=pg.evaluate("()=>{const n=new Date();const t=new Date(n.getFullYear(),n.getMonth(),n.getDate()+1,7,30,0);return t.getTime()-n.getTime()}")
    pg.evaluate("Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(150)
    pg.evaluate("(o)=>{window.__off=o;sessionStorage.setItem('__off',String(o))}",off); pg.evaluate("Object.defineProperty(document,'hidden',{get:()=>false,configurable:true});document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(700)
    rec("Date","returning after midnight starts a new day without a restart",st(pg)["date"]!=d0,(d0,st(pg)["date"]))
    ctx.close()
    # ---- damaged saves
    cases=[("invalid JSON text","{not json"),("empty string",""),("array instead of object","[1,2,3]"),
     ("wrong version",lambda s:s.__setitem__("v",2)),("cards not an array",lambda s:s.__setitem__("cards","x")),("settings missing",lambda s:s.pop("settings")),
     ("card theme 99",lambda s:s["cards"][0].__setitem__("theme",99)),("card theme is a string",lambda s:s["cards"][0].__setitem__("theme","x")),("card theme null",lambda s:s["cards"][0].__setitem__("theme",None)),
     ("card calling 50",lambda s:s["cards"][0].__setitem__("v",50)),("card rarity 9",lambda s:s["cards"][0].__setitem__("rarity",9)),("card seed null",lambda s:s["cards"][0].__setitem__("seed",None)),
     ("card name missing",lambda s:s["cards"][0].pop("name")),("card stats missing",lambda s:s["cards"][0].pop("stats")),("null card in list",lambda s:s["cards"].insert(1,None)),
     ("hearth slots reference deleted card",lambda s:s["hearth"].__setitem__("slots",[999,s["cards"][0]["id"]])),("hearth has 6 residents",lambda s:s["hearth"].__setitem__("slots",[c["id"] for c in s["cards"][:6]])),
     ("wander points at missing card",lambda s:s.__setitem__("wander",{"id":4242,"start":0,"ready":1,"seed":3,"notified":False})),("unknown curios",lambda s:s.__setitem__("curios",{"zzz":{"n":1}})),
     ("bad date in opens",lambda s:s["opens"].append("garbage")),("future date in opens",lambda s:s["opens"].append("2031-01-01")),("quiet.g string",lambda s:s["hearth"]["quiet"].__setitem__("g","abc")),
     ("pity huge",lambda s:s["pity"].__setitem__("since",10**9)),("bond string",lambda s:s["cards"][0].__setitem__("bond","lots")),("offset huge",lambda s:s.__setitem__("offset",100000)),
     ("journal wrong shape",lambda s:s.__setitem__("journal",{"2026-01-01":"just a string"})),("hearth missing",lambda s:s.pop("hearth")),("era 99 / gossip number",lambda s:(s["cards"][0].__setitem__("era",99),s["cards"][1].__setitem__("gossip",12345)))]
    for name,val in cases:
        if callable(val):
            s=json.loads(json.dumps(base)); val(s); val=s
        ctx,pg=boot(b,val)
        try: walk(pg); u=usable(pg)
        except Exception as e: u=False; pg._errs.append("walk:"+str(e)[:80])
        rec("Damaged save",name,u and not pg._errs,pg._errs[:1]); ctx.close()
    b.close()
save_results("qa_core")
