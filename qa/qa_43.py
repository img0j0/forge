from lib import *
import time,re
# 0.43: tidier pages. On a well-played save every everyday page fits about one phone screen, and everything that
# moved off a page is still one tap away: the Hearth's grid and sheets, Tales as a bookshelf and a book, ribbons as
# medals, This week and the month in sheets. Real taps; page lengths measured at 390x844.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def screens(pg): pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(250); return round(pg.evaluate("document.documentElement.scrollHeight/innerHeight"),2)
def small(pg,root):
    return pg.evaluate("""r=>[...document.querySelectorAll(r+' button')].filter(b=>b.offsetParent!==null&&!b.disabled).map(b=>[Math.round(b.getBoundingClientRect().height),(b.id||b.className)+':'+b.textContent.trim().slice(0,18)]).filter(x=>x[0]<44)""",root)
def tap(pg,sel): pg.locator(sel).first.scroll_into_view_if_needed(); pg.tap(sel); pg.wait_for_timeout(450)
def load(pg,s): setst(pg,s); pg.reload(); pg.wait_for_timeout(1000); closemodals(pg)
def played(b,**kw):
    ctx,pg=newpage(b,**kw); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    for t in ["week","skip10","skip10","spares","shade"]: dev(pg,t); closemodals(pg)
    s=st(pg); s["seen"]=99; s["wantAsked"]=True; s["backup"]={"at":s["date"]}; setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); closemodals(pg)
    pg.add_style_tag(content="details.dev{display:none!important}")
    tabto(pg,"hearth")
    for _ in range(3):
        if pg.locator("#hRelight").count()==0: break
        pg.evaluate("document.getElementById('hRelight').click()"); pg.wait_for_timeout(9000); closemodals(pg); tabto(pg,"today"); tabto(pg,"hearth")
    return ctx,pg
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=played(b,color_scheme="dark")
    # ---------- page lengths ----------
    tabto(pg,"hearth"); h=screens(pg); rec("Length","the Hearth fits about one screen (was 1.8 folded, 4.7 open)",h<=1.15,h)
    tabto(pg,"binder"); rec("Length","the Binder still fits one screen",screens(pg)<=1.05,screens(pg))
    tabto(pg,"chronicle"); pg.evaluate("document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(400); t=screens(pg)
    rec("Length","Tales fits about one screen (was 5.3)",t<=1.2,t)
    pg.evaluate("document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400); j=screens(pg)
    rec("Length","the Journal is about one and a half screens (was 5)",j<=1.55,j)
    pg.evaluate("document.querySelector('[data-sub=\"map\"]').click()"); pg.wait_for_timeout(400); m=screens(pg)
    rec("Length","the Map stays under one and a half screens",m<=1.5,m)
    tabto(pg,"settings",fold=True); sf=screens(pg); rec("Length","Settings opens with every section folded and fits one screen",sf<=1.1 and pg.evaluate("[...document.querySelectorAll('#view-settings details.setsec')].every(d=>!d.open)"),sf)
    tabto(pg,"today"); td=screens(pg); rec("Length","Today on a settled day fits about one and a half screens (was 2)",td<=1.5,td)
    # ---------- Today ----------
    rec("Today","the Map row is gone (its news lives on the Map)",pg.locator("#btnMapGo").count()==0)
    s=st(pg); s["wstat"]["sent"]=max(1,s["wstat"].get("sent",0)); s["hearth"]["fseen"]=["rug","lights","tree","flies","hedge","stones","pond","kite","mail","stump","ball","lamp","menhir","bell","fence","fern"]; s["request"]=None; s["hearth"]["sleep"]=None; load(pg,s); tabto(pg,"today")
    rec("Today","…and the Hearth row only shows when something waits there",pg.locator("#btnHearth").count()==0,pg.inner_text("#view-today")[:200])
    # ---------- Hearth ----------
    tabto(pg,"hearth")
    ids=pg.evaluate("[...document.querySelectorAll('#view-hearth .hgrid .act')].map(b=>b.id)")
    rec("Hearth","one grid holds Sit with, Snack, Story, Play, Wander and Forge",ids==["hAffection","hSnack","hStory","hPlay","hWander","hForge"],ids)
    rec("Hearth","every Hearth button is 44 points or more",not small(pg,"#view-hearth"),small(pg,"#view-hearth"))
    rec("Hearth","no folding sections are left on the Hearth",pg.locator("#view-hearth details").count()==0)
    rec("Hearth","the ember count is on the Forge button",re.search(r"\d+ embers?",pg.inner_text("#hEmbers")) is not None,pg.inner_text("#hEmbers"))
    tap(pg,"#hShelf"); mm=mt(pg)
    rec("Sheets","Curio shelf opens as a sheet with the planks and Send a curio",pg.locator("#modal .shelf .scur").count()>=20 and pg.locator("#modal #hGift").count()==1 and "Curio shelf" in mm,mm[:80])
    bad+=["shelf: "+v for v in axe(pg)]
    tap(pg,"#modal .scur:not(.off)"); rec("Sheets","…a curio on it opens its close-up","Set it by the fire" in mt(pg) or "You have" in mt(pg),mt(pg)[:80]); closemodals(pg)
    tap(pg,"#hFurn"); rec("Sheets","By the fire opens as a sheet listing all 16",pg.locator("#modal .furn li").count()==16 and "By the fire" in mt(pg)); bad+=["furn: "+v for v in axe(pg)]; closemodals(pg)
    tap(pg,"#hKeeps"); before=st(pg)
    chip=pg.evaluate("[...document.querySelectorAll('#modal [data-keep]')].filter(b=>!b.disabled&&b.getAttribute('aria-pressed')!=='true').map(b=>b.dataset.keep)[0]")
    tap(pg,f'#modal [data-keep="{chip}"]')
    rec("Sheets","Keepsakes opens as a sheet; choosing one saves it and the sheet stays open, updated",not pg.evaluate("document.getElementById('modal').hidden") and pg.get_attribute(f'#modal [data-keep="{chip}"]',"aria-pressed")=="true" and any((c.get("keep") or "")==chip for c in st(pg)["cards"]),chip)
    bd=pg.evaluate("[...document.querySelectorAll('#modal [data-bd]')].filter(b=>!b.disabled).map(b=>b.dataset.bd).pop()")
    tap(pg,f'#modal [data-bd="{bd}"]'); rec("Sheets","…and so does a backdrop",(st(pg)["hearth"].get("bd") or "")==bd and pg.get_attribute(f'#modal [data-bd="{bd}"]',"aria-pressed")=="true",bd)
    bad+=["keeps: "+v for v in axe(pg)]; closemodals(pg)
    tap(pg,"#hComp"); mm=mt(pg)
    rec("Sheets","the companion row opens bond, statue, story chapters and memories",pg.locator("#modal .bondbar").count()==1 and pg.locator("#modal [data-tale]").count()==1 and pg.locator("#modal [data-spre],#modal [data-statue]").count()>=1 and "Bond never fades" in mm,mm[:120])
    bad+=["comp: "+v for v in axe(pg)]
    pg.evaluate("document.querySelector('#modal [data-tale]').click()"); pg.wait_for_timeout(400); rec("Sheets","…and the story opens from there","chapter" in mt(pg).lower() or "Chapter" in mt(pg),mt(pg)[:80]); closemodals(pg)
    s=st(pg); s["wander"]=None; load(pg,s); tabto(pg,"hearth")
    tap(pg,"#hWander"); rec("Wander","Wander opens the wander sheet",pg.locator("#modal [data-wrealm],#modal [data-wto],#modal .moodbtn").count()>=1,mt(pg)[:80]); closemodals(pg)
    s=st(pg); now=int(time.time()*1000); cid=s["hearth"]["slots"][0]; s["wander"]={"id":cid,"start":now-3600*1000,"ready":now+2*3600*1000,"seed":3,"notified":False,"realm":0}
    s["forge"]["made"]=list(set(s["forge"]["made"]+["bell"])); s["forge"]["bell"]=None; load(pg,s); tabto(pg,"hearth")
    rec("Wander","while out, the grid shows Wandering with the time left",pg.locator("#hWOut").count()==1 and "Back in" in pg.inner_text("#hWOut"),pg.inner_text("#view-hearth .hgrid")[:120])
    tap(pg,"#hWOut"); rec("Wander","…which opens a sheet with the bell",pg.locator("#modal #hBell").count()==1,mt(pg)[:100])
    tap(pg,"#modal #hBell"); rec("Wander","ringing the bell brings them back: the sheet offers to see what they found",pg.locator("#modal #hCollect").count()==1,mt(pg)[:100])
    tap(pg,"#modal #hCollect"); pg.wait_for_timeout(600); rec("Wander","…and collecting works from the sheet",st(pg).get("wander") is None,st(pg).get("wander")); closemodals(pg)
    s=st(pg); s["wander"]={"id":cid,"start":now-5*3600*1000,"ready":now-1000,"seed":4,"notified":True,"realm":0}; load(pg,s); tabto(pg,"hearth")
    rec("Wander","a wanderer who is back shows in the grid, ready to collect",pg.locator("#view-hearth .hgrid #hCollect.ready").count()==1)
    tabto(pg,"today"); rec("Today","…and then the Hearth row shows on Today",pg.locator("#btnHearth").count()==1)
    # ---------- Tales ----------
    tabto(pg,"chronicle"); pg.evaluate("document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(400)
    rec("Tales","five tale rows with curio page marks",pg.locator("#view-chronicle .otale").count()==5 and pg.locator("#view-chronicle .tmarks .g").count()==20)
    tap(pg,'[data-tside="1"]'); rows=pg.evaluate("[...document.querySelectorAll('#view-chronicle .otale b')].map(b=>b.textContent)")
    rec("Tales","the Other side switch shows the five Shade tales",len(rows)==5 and pg.get_attribute('[data-tside="1"]',"aria-pressed")=="true",rows)
    tap(pg,'[data-tside="0"]')
    whole=pg.evaluate("(()=>{const r=document.querySelector('#view-chronicle .otale.whole');return r?r.dataset.otale:null})()")
    if whole is None:
        s=st(pg); [s["curios"].setdefault(i,{"n":1,"d":s["date"]}) for i in ("acorn","flower","feather","mushroom")]; load(pg,s); tabto(pg,"chronicle"); pg.evaluate("document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(400); whole="0"
    tap(pg,f'#view-chronicle [data-otale="{whole}"]'); p1=pg.inner_text("#modal .tpage")
    rec("Book","a whole tale opens as a book on page one",pg.locator("#modal .tpg").count()==4 and "Page 1 of 4" in mt(pg),mt(pg)[:120])
    texts=[p1]
    for i in range(3): tap(pg,"#modal .stack .primary"); texts.append(pg.inner_text("#modal .tpage"))
    rec("Book","Next page turns through all four pages, and the last shows the ending",len(set(texts))==4 and pg.locator("#modal .done").count()==1 and "Back to page one" in mt(pg),[t[:20] for t in texts])
    tap(pg,'#modal .tpg[data-tpage="1"]'); rec("Book","a page tab jumps straight to that page",pg.inner_text("#modal .tpage")==texts[1] and pg.get_attribute('#modal .tpg[data-tpage="1"]',"aria-pressed")=="true")
    rec("Book","page tabs are 44 points or more",not small(pg,"#modal"),small(pg,"#modal")); bad+=["book: "+v for v in axe(pg)]; closemodals(pg)
    tap(pg,"#fgTales"); n=pg.locator("#modal .chron").count()
    rec("Tales","Your Forgelings' tales opens every Forgeling's entry in a sheet",n==min(12,len(st(pg)["cards"])) and pg.locator("#modal [data-edit],#modal .mine").count()>=1,n)
    bad+=["fgtales: "+v for v in axe(pg)]
    if pg.locator("#modal [data-edit]").count():
        tap(pg,"#modal [data-edit]"); rec("Tales","…and Add a name or tale opens from there","tale" in mt(pg).lower() and pg.locator("#modal textarea,#modal input").count()>=1,mt(pg)[:80])
    closemodals(pg)
    # ---------- Journal ----------
    pg.evaluate("document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400)
    nm=pg.locator("#view-chronicle .medal").count(); on=pg.locator("#view-chronicle .medal.on").count()
    rec("Ribbons","ribbons are a grid of medals, earned ones gold",nm>=30 and 1<=on<nm and f"{on} of {nm} earned" in pg.inner_text("#view-chronicle .ribp"),(nm,on))
    rec("Ribbons","every medal is a 44-point button named for its ribbon",not small(pg,"#view-chronicle .medals") and "First Spark" in pg.inner_text("#view-chronicle .medals"))
    tap(pg,"#view-chronicle .medal:not(.on)"); mm=mt(pg)
    rec("Ribbons","tapping a medal shows what it is for and how close you are","so far" in mm and pg.locator("#modal .medal.big").count()==1,mm[:100]); bad+=["ribbon: "+v for v in axe(pg)]; closemodals(pg)
    tap(pg,"#jWeek"); rec("Journal","This week opens as a sheet","This week" in mt(pg) and "showed up" in mt(pg),mt(pg)[:80]); closemodals(pg)
    if pg.locator("#jMonth").count(): tap(pg,"#jMonth"); rec("Journal","the month in words opens as a sheet","Your month in words" in mt(pg)); closemodals(pg)
    s=st(pg); d0=s["date"]
    import datetime
    for i in range(6):
        k=(datetime.date.fromisoformat(d0)-datetime.timedelta(days=i)).isoformat(); s["journal"][k]={"text":f"Line number {i}","v":0}
    load(pg,s); tabto(pg,"chronicle"); pg.evaluate("document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400)
    rec("Journal","the Journal shows your three latest lines and a way to the rest",pg.locator("#view-chronicle .calling").count()==3 and pg.locator("#jLines").count()==1)
    tap(pg,"#jLines"); rec("Journal","…which lists them all",pg.locator("#modal .calling").count()>=6,pg.locator("#modal .calling").count()); closemodals(pg)
    bad+=["journal dark: "+v for v in axe(pg)]
    pg.evaluate("document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(400); bad+=["tales dark: "+v for v in axe(pg)]
    tabto(pg,"hearth"); bad+=["hearth dark: "+v for v in axe(pg)]
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # ---------- light, plain sky, 320 px ----------
    ctx,pg=played(b,w=320,h=640,color_scheme="light")
    s=st(pg); s["settings"]["sky"]="plain"; s["settings"]["theme"]="light"; load(pg,s)
    tabto(pg,"hearth"); w=pg.evaluate("document.documentElement.scrollWidth"); rec("Layout","no sideways scroll on the Hearth at 320 px",w<=320,w)
    rec("Layout","Hearth buttons stay 44 points at 320 px",not small(pg,"#view-hearth"),small(pg,"#view-hearth")); bad+=["hearth light: "+v for v in axe(pg)]
    tabto(pg,"chronicle"); pg.evaluate("document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(400)
    rec("Layout","no sideways scroll on Tales at 320 px",pg.evaluate("document.documentElement.scrollWidth")<=320); bad+=["tales light: "+v for v in axe(pg)]
    pg.evaluate("document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400)
    rec("Layout","no sideways scroll on the Journal at 320 px",pg.evaluate("document.documentElement.scrollWidth")<=320); bad+=["journal light: "+v for v in axe(pg)]
    tap(pg,"#view-chronicle .medal"); bad+=["ribbon light: "+v for v in axe(pg)]; closemodals(pg)
    tabto(pg,"hearth"); tap(pg,"#hKeeps"); bad+=["keeps light: "+v for v in axe(pg)]; closemodals(pg)
    rec("A11y","zero accessibility violations on the new pages and sheets, dark and light",not bad,bad[:4])
    rec("All","no page errors (light, 320 px)",not pg._errs,pg._errs[:2]); ctx.close()
save_results("qa_43")
