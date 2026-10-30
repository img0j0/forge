from lib import *
# 0.22.0: aesthetic polish. Pixel card back and paper face, the night stage for big moments,
# Journal stamps and ribbon rosettes, and the Binder filter sheet.
import datetime
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
def bg(pg,sel): return pg.evaluate("s=>{const e=document.querySelector(s);return e?getComputedStyle(e).backgroundImage:''}",sel)
STAGEPX="()=>{const c=document.querySelector('#modal .stageCv');if(!c)return -1;const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n}"
def hist(s,days):
    d0=datetime.date.fromisoformat(s["date"]); s["startDate"]=(d0-datetime.timedelta(days=days)).isoformat(); h=[]
    for i in range(days,0,-1):
        dd=(d0-datetime.timedelta(days=i)).isoformat(); r=i%7
        if r in (2,5): continue
        h.append({"date":dd,"status":"rest" if r==3 else "done","v":i%12})
    s["history"]=h; return s
with sync_playwright() as p:
    b=p.chromium.launch()
    if P.startswith("file://"):
        size=os.path.getsize(P.replace("file://",""))
        rec("Size","the whole app stays under the 1 MB budget (raised whenever a wanted feature needs room)",size<1_000_000,size)
    ctx,pg=newpage(b); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo")
    rec("Stage","the title screen keeps its own scene, with no night stage behind it",pg.locator("#modal .stageCv").count()==0)
    first_card(pg); closemodals(pg); base=st(pg)
    # ---------- the daily card ----------
    s=build(base,[2,2,2,1,1]); s["seen"]=99; s["status"]="fresh"; s["todayCard"]=None; s["history"]=[h for h in s["history"] if h["date"]!=s["date"]]; s["packs"]=1
    setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    rec("Card","Today's card back is pixel art, with its words still readable","svg+xml" in bg(pg,"#btnTurn") and "Today's card" in pg.inner_text("#btnTurn") and pg.get_attribute("#btnTurn","aria-label")=="Turn over today's card")
    pg.evaluate("document.getElementById('btnTurn').click()"); pg.wait_for_timeout(400)
    rec("Card","the card in the sheet has the same pixel back","svg+xml" in bg(pg,"#vBack"))
    pg.evaluate("document.getElementById('vBack').click()"); pg.wait_for_timeout(1000)
    rec("Card","…and turns over to a paper face with the calling, the small thing and the question","svg+xml" in bg(pg,".vface.vfront") and all(x in mt(pg) for x in ("Today's small thing","The Forge asks")))
    closemodals(pg); pg.evaluate("()=>{const o=document.getElementById('vOk');if(o)o.click();}"); pg.wait_for_timeout(300)
    rec("Card","the card face on Today is paper too","svg+xml" in bg(pg,"#view-today .taskface"))
    # ---------- the night stage ----------
    pg.evaluate("document.getElementById('btnDone').click()"); pg.wait_for_timeout(900)
    if pg.locator("#modal [data-mood]").count(): pg.evaluate("document.querySelector('#modal [data-mood]').click()"); pg.wait_for_timeout(900)
    pg.wait_for_selector("#cover",state="visible"); pg.wait_for_timeout(300)
    rec("Stage","the reveal happens at night by the fire: a drawn, hidden-from-screen-readers backdrop",pg.evaluate(STAGEPX)>500 and pg.get_attribute("#modal .stageCv","aria-hidden")=="true",pg.evaluate(STAGEPX))
    rec("Stage","…the card waiting to be turned has the pixel back","svg+xml" in bg(pg,"#cover"))
    a=pg.evaluate("()=>document.querySelector('#modal .stageCv').toDataURL()"); pg.wait_for_timeout(400); b2=pg.evaluate("()=>document.querySelector('#modal .stageCv').toDataURL()")
    rec("Stage","…embers move",a!=b2)
    pg.evaluate("document.getElementById('cover').click()"); pg.wait_for_timeout(1500)
    for _ in range(4):
        for sel in ("#rvSkip","[data-close]"):
            if pg.locator("#modal "+sel).count(): pg.evaluate("s=>document.querySelector('#modal '+s).click()",sel); pg.wait_for_timeout(500)
    closemodals(pg); pg.wait_for_timeout(300)
    rec("Stage","closing it leaves no stage behind",pg.locator(".stageCv").count()==0)
    tabto(pg,"today"); pg.evaluate("()=>{const b=document.getElementById('btnPack');if(b)b.click();}"); pg.wait_for_timeout(700)
    rec("Stage","the pack opens on the same night stage",pg.evaluate(STAGEPX)>500)
    rec("Card","the pack carries the campfire, not the old gem",pg.evaluate("()=>{const s=document.querySelector('#modal svg');return !!s&&s.innerHTML.includes('#FFD66A')&&!s.innerHTML.includes('M80 62l26 22')}"))
    closemodals(pg); pg.keyboard.press("Escape"); pg.wait_for_timeout(300); pg.evaluate("()=>{if(!document.getElementById('modal').hidden){document.getElementById('modal').hidden=true;document.getElementById('modal').innerHTML='';}}")
    rec("All","no page errors through the card and the stage",not pg._errs,pg._errs[:2]); ctx.close()
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    tabto(pg,"binder"); pg.evaluate("document.querySelector('#view-binder [data-insp]').click()"); pg.wait_for_timeout(500)
    a=pg.evaluate(STAGEPX); x1=pg.evaluate("()=>document.querySelector('#modal .stageCv').toDataURL()"); pg.wait_for_timeout(500); x2=pg.evaluate("()=>document.querySelector('#modal .stageCv').toDataURL()")
    rec("Stage","with reduced motion the stage is drawn and holds still (card close-up)",a>500 and x1==x2); ctx.close()
    # ---------- Journal ----------
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    s=hist(build(base,[2,2,2,1,1]),30); s["seen"]=99; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400)
    cells=pg.evaluate("[...document.querySelectorAll('.cal span.c')].map(c=>[c.className,getComputedStyle(c).backgroundImage.includes('svg'),c.getAttribute('aria-label')])")
    done=[c for c in cells if " done" in c[0]]; rest=[c for c in cells if " rest" in c[0]]; miss=[c for c in cells if " skipped" in c[0] or c[0].strip()=="c"]
    rec("Journal","days you showed up get a flame stamp, rest days a moon, other days nothing",done and rest and all(c[1] for c in done) and all(c[1] for c in rest) and not any(c[1] for c in miss),(len(done),len(rest),len(miss)))
    rec("Journal","…and each day still says what happened for screen readers",all("showed up" in c[2] for c in done) and all("rested" in c[2] for c in rest))
    rec("Journal","a small key explains the stamps",pg.locator(".calkey").count()==1 and "showed up" in pg.inner_text(".calkey"))
    # 0.43: ribbons are medals; earned ones are gold and say so, the rest say how close; details open on tap, never a progress bar
    ribs=pg.evaluate("[...document.querySelectorAll('#view-chronicle .medal')].map(r=>[r.classList.contains('on'),r.querySelector('.sr').textContent,r.offsetHeight,r.querySelector('.pb')?1:0])")
    rec("Journal","ribbons are medals: earned ones say so, the rest say how close, never a progress bar",ribs and all(r[3]==0 for r in ribs) and all(r[1].endswith("Earned")==r[0] for r in ribs) and all(r[2]>=44 for r in ribs),ribs[:4])
    bad=[r for r in ribs if not r[0] and not re.search(r"\d+ of \d+$",r[1])]
    rec("Journal","…and the dots match the count",not bad,bad[:2])
    # ---------- Binder ----------
    s=st(pg); s["cards"][0]["fav"]=True
    for i,c in enumerate(s["cards"]): c["v"]=2 if i<3 else 4; c["dark"]=(i%2==1)
    setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"binder")
    rec("Binder","the filters are one quiet row: Filter and Sort",pg.locator("#view-binder .filters").count()==0 and pg.is_visible("#btnFilter") and pg.is_visible("#btnSort") and pg.inner_text("#btnFilter")=="Filter")
    pg.evaluate("document.getElementById('btnFilter').click()"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Binder","the filter sheet lists every calling with counts, the moods and favorites",pg.locator("#modal [data-ftype]").count()==13 and "Depth 3" in m and "Connection 5" in m and pg.locator("#modal [data-fmood]").count()==3 and pg.locator("#modal #fFav").count()==1,m[:120])
    pg.evaluate("document.querySelector('#modal [data-ftype=\"2\"]').click()"); pg.wait_for_timeout(300)
    rec("Binder","choosing a calling updates the sheet in place and the count on its button",pg.get_attribute("#modal [data-ftype=\"2\"]","aria-pressed")=="true" and "Show 3 Forgelings" in mt(pg))
    pg.evaluate("document.querySelector('#modal [data-fmood=\"cute\"]').click()"); pg.wait_for_timeout(300)
    rec("Binder","…a mood narrows it further","Show 2 Forgelings" in mt(pg),mt(pg)[-60:])
    pg.evaluate("document.querySelector('#modal [data-close]').click()"); pg.wait_for_timeout(400)
    t=pg.inner_text("#view-binder")
    rec("Binder","back in the binder: two cards, 'Filter · 2', and what is being shown",pg.locator("#view-binder .binder [data-insp]").count()==2 and pg.inner_text("#btnFilter")=="Filter · 2" and "Showing Depth, Cute only." in t,t[:200])
    rec("Binder","…the Depth calling note still appears",pg.locator("#view-binder .calling").count()==1)
    pg.evaluate("document.getElementById('fClear').click()"); pg.wait_for_timeout(300)
    rec("Binder","Show all clears every filter",pg.inner_text("#btnFilter")=="Filter" and pg.locator("#view-binder .binder [data-insp]").count()==8 and pg.locator("#fClear").count()==0)
    pg.evaluate("document.getElementById('btnFilter').click()"); pg.wait_for_timeout(300); pg.evaluate("document.querySelector('#modal #fFav').click()"); pg.wait_for_timeout(300)
    rec("Binder","favorites only works from the sheet","Show 1 Forgeling" in mt(pg))
    small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.offsetParent).map(b=>[Math.round(b.getBoundingClientRect().height),b.textContent.trim()]).filter(x=>x[0]<44)")
    rec("Binder","every control in the filter sheet is at least 44px tall",not small,small[:3])
    closemodals(pg)
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # ---------- accessibility ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    def axe(pg,where,scheme):
        pg.wait_for_function("!document.body.classList.contains('arrive')"); pg.evaluate(AXE); v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
        bad.extend(f"{scheme}/{where}: {x}" for x in v)
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
        s=hist(build(base,[2,2,2,1,1]),30); s["seen"]=99; s["status"]="fresh"; s["todayCard"]=None; s["history"]=[h for h in s["history"] if h["date"]!=s["date"]]; s["packs"]=1
        setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); axe(pg,"today",scheme)
        pg.evaluate("document.getElementById('btnTurn').click()"); pg.wait_for_timeout(400); pg.evaluate("document.getElementById('vBack').click()"); pg.wait_for_timeout(1000); axe(pg,"card face",scheme)
        closemodals(pg); pg.evaluate("()=>{const o=document.getElementById('vOk');if(o)o.click();}"); pg.wait_for_timeout(300)
        pg.evaluate("document.getElementById('btnPack').click()"); pg.wait_for_timeout(700); axe(pg,"pack",scheme)
        pg.evaluate("()=>{document.getElementById('modal').hidden=true;document.getElementById('modal').innerHTML='';}")
        tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400); axe(pg,"journal",scheme)
        tabto(pg,"binder"); pg.evaluate("document.getElementById('btnFilter').click()"); pg.wait_for_timeout(400); axe(pg,"filter sheet",scheme)
        ctx.close()
    rec("A11y","axe: zero violations on Today, the card face, the pack, the Journal and the filter sheet, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_22"); print(sum(r["ok"] for r in RES),"/",len(RES))
