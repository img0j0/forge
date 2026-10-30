import json, time, re, datetime, os
from playwright.sync_api import sync_playwright
S=os.environ.get("FORGE_DIR",os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P=os.environ.get("FORGE_HTML","file://"+S+"/work.html"); KEY="forge-app-v1"
RES=[]
def rec(area,check,ok,detail=""):
    RES.append({"area":area,"check":check,"ok":bool(ok),"detail":str(detail)[:300]}); print(("PASS " if ok else "FAIL ")+area+" | "+check+((" | "+str(detail)[:200]) if detail else ""))
def st(pg): return pg.evaluate("(k)=>JSON.parse(localStorage.getItem(k))",KEY)
def setst(pg,s): pg.evaluate("([k,s])=>localStorage.setItem(k,JSON.stringify(s))",[KEY,s])
def mt(pg): return "" if pg.evaluate("document.getElementById('modal').hidden") else pg.inner_text("#modal")
def first_card(pg):
    if pg.locator("#titleGo").count(): pg.tap("#titleGo"); pg.wait_for_selector("#ageM",state="visible")
    pg.select_option("#ageM","6"); pg.select_option("#ageY","1995"); pg.tap("#ageGo")
    pg.tap("#vBack"); pg.wait_for_selector("#vDoneNow",state="visible"); pg.tap("#vDoneNow")
    pg.wait_for_selector("#cover",state="visible"); pg.tap("#cover"); pg.wait_for_selector("#rvSkip",state="visible"); pg.tap("#rvSkip"); pg.wait_for_timeout(1500)
    for _ in range(3):
        if mt(pg) and pg.locator("[data-close]").count():
            try: pg.tap("[data-close]",timeout=2000); pg.wait_for_timeout(300)
            except Exception: break
def dev(pg,tool):
    pg.evaluate("document.querySelector('.tab[data-tab=\"settings\"]').click()"); pg.wait_for_timeout(250)
    if not pg.evaluate("document.querySelector('details.dev').open"): pg.evaluate("document.querySelector('details.dev summary').click()")
    pg.evaluate("(t)=>document.querySelector('[data-tool=\"'+t+'\"]').click()",tool); pg.wait_for_timeout(500)
def closemodals(pg):
    for _ in range(4):
        if pg.evaluate("document.getElementById('modal').hidden"): return
        try: pg.evaluate("()=>{const b=document.querySelector('#modal [data-close]');if(b)b.click();}"); pg.wait_for_timeout(300)
        except Exception: return
def tabto(pg,t,fold=False):
    pg.evaluate("t=>document.querySelector('.tab[data-tab=\"'+t+'\"]').click()",t); pg.wait_for_timeout(350)
    if t=="settings" and not fold: opensecs(pg)
def opensecs(pg):  # 0.38.3: Settings folds; most suites want every section open, as a person would open the one they need
    pg.evaluate("()=>document.querySelectorAll('#view-settings details.setsec:not([open])').forEach(d=>d.open=true)"); pg.wait_for_timeout(80)
def newpage(b,w=390,h=844,**kw):
    ctx=b.new_context(viewport={"width":w,"height":h},has_touch=True,is_mobile=w<600,permissions=["clipboard-read","clipboard-write"],**kw)
    pg=ctx.new_page(); pg._errs=[]; pg._cons=[]; pg._reqs=[]
    pg.on("pageerror",lambda e:pg._errs.append(str(e)))
    pg.on("console",lambda m:pg._cons.append((m.type,m.text)) if m.type in("error","warning") else None)
    pg.on("request",lambda r:pg._reqs.append(r.url) if not r.url.startswith(("file:","data:","blob:")) else None)
    return ctx,pg
def save_results(name): json.dump(RES,open(f"{S}/qa/{name}.json","w"),indent=1)
def openmap(pg):
    tabto(pg,"chronicle"); pg.evaluate("()=>{const b=document.querySelector('[data-sub=\"map\"]');if(b)b.click();}"); pg.wait_for_timeout(400)
def pick_calling(pg,v):
    """Choose a calling filter in the Binder. From 0.22 the filters live in a sheet behind one button."""
    if pg.locator("#btnFilter").count():
        pg.evaluate("document.getElementById('btnFilter').click()"); pg.wait_for_timeout(250)
        pg.evaluate("v=>document.querySelector('#modal [data-ftype=\"'+v+'\"]').click()",str(v)); pg.wait_for_timeout(200)
        pg.evaluate("()=>{const b=document.querySelector('#modal [data-close]');if(b)b.click();}"); pg.wait_for_timeout(300)
    else:
        pg.evaluate("v=>document.querySelector('[data-ftype=\"'+v+'\"]').click()",str(v)); pg.wait_for_timeout(300)
def hsheet(pg,k):  # 0.43: the Hearth's lists open as sheets (shelf, furn, keeps, comp); tests read them in #modal
    ids={"shelf":"hShelf","furn":"hFurn","keeps":"hKeeps","comp":"hComp"}
    pg.evaluate("t=>document.querySelector('.tab[data-tab=\"hearth\"]').click()","x"); pg.wait_for_timeout(300)
    pg.evaluate("i=>document.getElementById(i).click()",ids[k]); pg.wait_for_timeout(350)
