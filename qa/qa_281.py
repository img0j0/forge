from lib import *
# 0.28.1: the app is called Forgelings; "the Forge" stays as the world. Support email in the privacy note.
EMAIL="forgelings.app@gmail.com"
APPNAME=re.compile(r"(?<![Tt]he )(?<![Ee]very )\bForge\b(?!ling|bound)")
def stray(t): return [t[max(0,m.start()-30):m.end()+20].replace("\n"," ") for m in APPNAME.finditer(t)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in ((320,568),(390,844)):
        ctx,pg=newpage(b,w,h); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.wait_for_timeout(600)
        r=pg.evaluate("()=>{const e=document.getElementById('dlgTitle');const b=e.getBoundingClientRect();return [e.textContent,b.left,b.right,innerWidth,e.scrollWidth<=e.clientWidth+1]}")
        rec("Title",f"{w}px: the title reads Forgelings and fits on screen",r[0]=="Forgelings" and r[1]>=0 and r[2]<=r[3] and r[4] and not pg.evaluate("document.scrollingElement.scrollWidth>innerWidth"),r)
        if w==390:
            t0=pg.inner_text("#modal"); first_card(pg); closemodals(pg)
            seen=[t0]
            for tb in ["today","hearth","binder","chronicle","settings"]:
                tabto(pg,tb); seen.append(pg.evaluate("document.querySelector('.app').innerText"))
            pg.evaluate("document.getElementById('btnPrivacy').click()"); pg.wait_for_timeout(300); priv=mt(pg)
            rec("Privacy","the privacy note gives the support email as a link",EMAIL in priv and pg.locator(f"#modal a[href='mailto:{EMAIL}']").count()==1,priv[-200:])
            closemodals(pg); pg.evaluate("document.getElementById('btnTerms').click()"); pg.wait_for_timeout(300); terms=mt(pg); closemodals(pg)
            rec("Terms","the terms give the support email",EMAIL in terms)
            s=st(pg); s["seen"]=0; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); wn=mt(pg)
            rec("What's New","What's New announces the new name (or it has rolled off the latest eight notes)","A new name: Forgelings" in wn or pg.locator("#modal .newlist li").count()==8,wn[:200])
            allt="\n".join(seen+[priv,terms,wn])
            rec("Copy","no screen calls the app plain 'Forge' (the Forge, every Forge and Forgebound are the world, and stay)",not stray(allt),stray(allt)[:5])
            rec("Copy","the world is still the Forge","The Forge" in allt)
            rec("Save","the save key is unchanged, so no one loses their collection",pg.evaluate("!!localStorage.getItem('forge-app-v1')"))
            rec("All","no page errors",not pg._errs,pg._errs[:1])
        ctx.close()
    # public pages
    import os
    d=os.path.dirname(P.replace("file://","")) if P.startswith("file://") else None
    for f in ("privacy","terms","support"):
        ctx,pg=newpage(b); pg.goto("file:///home/claude/forge/legal/out/"+f+".html"); t=pg.inner_text("body")
        rec("Pages",f"{f}: names Forgelings, gives the support email, and never calls the app plain Forge",EMAIL in t and "Forgelings" in t and not stray(t) and pg.locator(f"a[href='mailto:{EMAIL}']").count()>=1,stray(t)[:3]); ctx.close()
    b.close()
save_results("qa_281"); print(sum(r["ok"] for r in RES),"/",len(RES))
