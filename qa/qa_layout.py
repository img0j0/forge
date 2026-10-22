from lib import *
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
def build(base):
    s=json.loads(json.dumps(base)); b0=s["cards"][0]; s["cards"]=[]; k=0
    for ti,n in enumerate([8,4,2,1,0]):
        for j in range(n):
            c=json.loads(json.dumps(b0)); c["id"]=100+k; c["seed"]=5000+k*7919; c["theme"]=ti; c["dark"]=(j==0 and ti in(0,2)); k+=1; s["cards"].append(c)
    s["nextId"]=1000; s["seen"]=18; s["hearth"]["slots"]=[s["cards"][0]["id"],s["cards"][9]["id"]]; return s
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg); ctx.close()
    for (w,h) in [(320,568),(344,640),(360,640),(390,844),(430,932),(768,1024),(1280,800)]:
        ctx,pg=newpage(b,w,h); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
        setst(pg,build(base)); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
        ov=[];junk=[];small=[]
        views=[("today",None),("binder",None),("hearth",None),("settings",None)]+[("chronicle",s) for s in ["tales","journal","journey","map","realms","callings"]]
        for t,sub in views:
            tabto(pg,t)
            if sub: pg.evaluate("(s)=>{const b=document.querySelector('[data-sub=\"'+s+'\"]');if(b)b.click()}",sub); pg.wait_for_timeout(300)
            closemodals(pg)
            sw=pg.evaluate("[document.documentElement.scrollWidth,innerWidth]")
            if sw[0]>w+1 or sw[1]>w+1: ov.append((t,sub,sw))
            m=JUNK.findall(pg.inner_text("body"))
            if m: junk.append((t,sub,m[:2]))
            bad=pg.evaluate("""()=>[...document.querySelectorAll('button,.chip,.tab,[role=button]')].filter(e=>e.offsetParent!==null&&e.getBoundingClientRect().height>0).map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height),(e.innerText||'').trim().slice(0,16)]}).filter(a=>a[1]<36||a[0]<36)""")
            if bad: small.append((t,sub,bad[:3]))
        rec("Layout",f"{w}x{h}: no sideways overflow on any screen (incl. Map)",not ov,ov)
        rec("Content",f"{w}x{h}: no undefined/NaN/null text anywhere",not junk,junk)
        rec("Touch",f"{w}x{h}: every tappable control >= 36px",not small,small[:2])
        rec("Console",f"{w}x{h}: no page errors",not pg._errs,pg._errs[:1])
        rec("Privacy",f"{w}x{h}: external requests",not pg._reqs,pg._reqs[:2]); ctx.close()
    b.close()
save_results("qa_layout")
