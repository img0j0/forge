from lib import *
# 0.22.3: panels in pixel material; the Forgeling stands on a pedestal in firelight.
with sync_playwright() as p:
    b=p.chromium.launch()
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,430,932,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); pg.wait_for_timeout(1400)
        css=pg.evaluate("""()=>[...document.querySelectorAll('#view-today .hero,#view-today .panel-box,#view-today .group')].filter(e=>e.offsetParent).map(e=>{const s=getComputedStyle(e);return [e.className,s.borderImageSource.includes('svg'),s.borderTopWidth,s.backgroundImage,s.clipPath]})""")
        # since 0.35.2 (Living Sky) panels are glass with stepped corners and gold rivets; Plain keeps the pixel frame
        glass=lambda c:c[2]=="0px" and c[3].count("rgb(255, 211, 107)")>=4 and (c[4].startswith("polygon") or "hero" in c[0])
        rec("Panels",f"{scheme}: every Today panel wears the pixel material (Living Sky glass with rivets, or the pixel frame in Plain)",css and all((c[1] and c[2]=="12px") or glass(c) for c in css),css[:2])
        hero=[c for c in css if "hero" in c[0]]
        rec("Panels",f"{scheme}: the Forgeling stands on a pedestal in firelight",hero and hero[0][3].count("svg")>=2 and "radial-gradient" in hero[0][3],hero[:1])
        tabto(pg,"settings"); n=pg.evaluate("[...document.querySelectorAll('#view-settings .setblock')].filter(e=>{const s=getComputedStyle(e);return e.offsetParent&&(s.borderImageSource.includes('svg')||(s.clipPath.startsWith('polygon')&&s.backgroundImage.includes('rgb(255, 211, 107)')))}).length")
        rec("Panels",f"{scheme}: Settings blocks share the same frame",n>=8,n)
        hs=pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
        rec("Panels",f"{scheme}: no sideways scrolling with the thicker frames",not hs)
        rec("All",f"{scheme}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    ctx,pg=newpage(b,320,640); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); pg.wait_for_timeout(1400)
    w=pg.evaluate("()=>{const c=document.querySelector('#view-today .hero #btnShowToday');return c?Math.round(c.getBoundingClientRect().width):0}")
    rec("Panels","on a 320px phone the card still fits inside its frame",0<w<=320-24-16 and not pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"),w); ctx.close()
    b.close()
save_results("qa_223"); print(sum(r["ok"] for r in RES),"/",len(RES))
