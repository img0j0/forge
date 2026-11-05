from lib import *
import datetime,os,re
# 0.49: the binder finds Forgelings by name and filters by realm (in the Filter sheet); on the website in a browser tab,
# Today offers once (from the third Forgeling) to keep Forgelings on the home screen, with iPhone steps that save a copy
# first. Never in the iPhone app, on the home screen, or in the dev build.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
SRC=P.replace('file://','') if P.startswith('file://') else None
REL='/tmp/forge_qa49_release.html'
if SRC:
    h=open(SRC,encoding='utf8').read().replace('<meta charset="utf-8">','<meta charset="utf-8">\n<meta name="forge-build" content="release">',1)
    open(REL,'w',encoding='utf8').write(h)
PR='file://'+REL
IOS="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
def grow(pg,n):
    s=st(pg); c0=s["cards"][0]; names=["Hazrin","Tuckbell","Fenbo","Salmer","Miroton","Tuckbo","Ketfin","Salfin","Nimko","Hazel"]
    for i in range(1,n):
        c=dict(c0); c.update(id=c0["id"]+i,seed=c0["seed"]+i*7919,theme=i%5,dark=(i%4==3),name=names[i%len(names)],nick="")
        s["cards"].append(c)
    s["cards"][0]["nick"]="Pip"; s["cards"][0]["theme"]=0; s["cards"][0]["dark"]=False
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg); return st(pg)
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    # ---------- binder: name and realm ----------
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s=grow(pg,20); tabto(pg,"binder"); pg.evaluate("document.getElementById('btnFilter').click()"); pg.wait_for_timeout(400)
    chips=pg.evaluate("[...document.querySelectorAll('#modal [data-frealm]')].map(b=>b.textContent.trim())")
    have={}
    for c in s["cards"]:
        k=(c["theme"],c["dark"]); have[k]=have.get(k,0)+1
    rec("Find","the Filter sheet has a name field and one realm chip per realm found, with counts",pg.locator("#modal #fName").count()==1 and len(chips)==len(have)+1 and chips[0]=="All",chips)
    pg.locator("#fName").click(); pg.keyboard.type("haz",delay=40); pg.wait_for_timeout(300)
    want=sum(1 for c in s["cards"] if "haz" in (c.get("nick","")+" "+c["name"]).lower())
    shown=pg.locator("#view-binder .binder [data-insp]").count(); lab=pg.inner_text("#fShow")
    rec("Find",f"typing a name narrows the binder as you go ({want} match)",shown==min(9,want) and lab==f"Show {want} Forgelings",(shown,lab))
    rec("Find","the keyboard stays up: the name field keeps focus while typing",pg.evaluate("document.activeElement&&document.activeElement.id")=="fName")
    pg.locator("#fName").fill("pip"); pg.wait_for_timeout(250)
    rec("Find","a filtered page shows only its matches: no \"not yet\" placeholders",pg.locator("#view-binder .binder .empty").count()==0)
    rec("Find","a nickname finds it too",pg.locator("#view-binder .binder [data-insp]").count()==1 and pg.inner_text("#fShow")=="Show 1 Forgeling")
    bad+=["filter: "+v for v in axe(pg)]
    pg.locator("#fName").fill(""); pg.wait_for_timeout(200)
    k=sorted(have,key=lambda x:(x[1],x[0]))[1]; key=f"{k[0]}-{1 if k[1] else 0}"
    pg.evaluate(f"document.querySelector('#modal [data-frealm=\"{key}\"]').click()"); pg.wait_for_timeout(300)
    ids=pg.evaluate("[...document.querySelectorAll('#view-binder .binder [data-insp]')].map(b=>+b.dataset.insp)")
    th={c["id"]:(c["theme"],c["dark"]) for c in s["cards"]}
    rec("Find","a realm chip shows that realm only, and the chip is pressed",len(ids)==min(9,have[k]) and all(th[i]==k for i in ids) and pg.evaluate(f"document.querySelector('#modal [data-frealm=\"{key}\"]').getAttribute('aria-pressed')")=="true",(len(ids),have[k]))
    pg.locator("#fName").fill("zzz"); pg.wait_for_timeout(250)
    rec("Find","nothing matching says so, kindly",pg.inner_text("#fShow")=="Nothing matches yet")
    closemodals(pg); pg.wait_for_timeout(200); t=pg.inner_text("#view-binder")
    rec("Find","the binder says what it is showing, with a way back",'names with “zzz”' in t and "No Forgelings match this yet" in t and pg.locator("#fClear").count()==1,t[:160])
    pg.evaluate("document.getElementById('fClear').click()"); pg.wait_for_timeout(250)
    rec("Find","Show all clears the name and the realm too",pg.locator("#view-binder .binder [data-insp]").count()==9 and pg.locator("#fClear").count()==0)
    rec("All","binder: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # ---------- home screen tip ----------
    def home(ua=None,release=True,n=3,stand=False):
        kw={"user_agent":ua} if ua else {}
        c,g=newpage(b,**kw)
        if stand: g.add_init_script("Object.defineProperty(navigator,'standalone',{get:()=>true})")
        g.clock.install(time=datetime.datetime(2026,11,5,10,0)); g.goto(PR if release else P); g.wait_for_selector("#titleGo"); first_card(g); closemodals(g)
        if n>1: grow(g,n)
        tabto(g,"today"); return c,g
    c,g=home(IOS,n=2); rec("Home","with two Forgelings, not yet",g.locator("#btnHomeTip").count()==0); c.close()
    c,g=home(IOS,n=3)
    rec("Home","from the third Forgeling, Today offers to keep it on the home screen (a 44-point row)",g.locator("#btnHomeTip").count()==1 and g.locator("#btnHomeTip").bounding_box()["height"]>=44)
    g.evaluate("document.getElementById('btnHomeTip').click()"); g.wait_for_timeout(400); m=mt(g)
    rec("Home","on iPhone the steps save a copy first and restore it on the home screen",g.locator("#modal #htSave").count()==1 and "Save a copy first" in m and "Restore a copy" in m and "Add to Home Screen" in m,m[:200])
    bad+=["home tip: "+v for v in axe(g)]
    g.evaluate("document.getElementById('htLater').click()"); g.wait_for_timeout(300)
    rec("Home","Not now hides it, for a week",g.locator("#btnHomeTip").count()==0 and st(g)["homeTip"]=="2026-11-12",st(g)["homeTip"])
    g.clock.set_system_time(datetime.datetime(2026,11,12,10,0)); g.reload(); g.wait_for_timeout(1000); closemodals(g); tabto(g,"today")
    rec("Home","a week later it is back",g.locator("#btnHomeTip").count()==1)
    g.evaluate("document.getElementById('btnHomeTip').click()"); g.wait_for_timeout(300); g.evaluate("document.getElementById('htDone').click()"); g.wait_for_timeout(300)
    g.clock.set_system_time(datetime.datetime(2026,12,30,10,0)); g.reload(); g.wait_for_timeout(1000); closemodals(g); tabto(g,"today")
    rec("Home","once it's on the home screen, it never asks again",g.locator("#btnHomeTip").count()==0 and st(g)["homeTip"]=="done")
    rec("All","home tip: no page errors",not g._errs,g._errs[:2]); c.close()
    c,g=home(None,n=3); g.evaluate("document.getElementById('btnHomeTip').click()"); g.wait_for_timeout(300); m=mt(g)
    rec("Home","elsewhere, the steps are the browser's install, and the collection comes along",g.locator("#modal #htSave").count()==0 and "Install app" in m and "comes with it" in m,m[:160]); c.close()
    c,g=home(IOS,n=3,stand=True); rec("Home","already on the home screen: never shown",g.locator("#btnHomeTip").count()==0); c.close()
    c,g=home(IOS,release=False,n=3); rec("Home","the dev build never shows it",g.locator("#btnHomeTip").count()==0); c.close()
    rec("A11y","axe: the Filter sheet and the home screen steps have no violations",not bad,bad[:3])
    b.close()
save_results("qa_49"); print(sum(r["ok"] for r in RES),"/",len(RES))
