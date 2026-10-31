from lib import *
import datetime
# 0.47.1: How did it feel? Each face and its word sit inside the journal's ink circle, centred, by day and lamplight,
# before and after a tap, and with Plain print.
GEO="""()=>[...document.querySelectorAll('#view-today .facebtn')].map(b=>{const r=b.getBoundingClientRect(),f=b.querySelector('.feelface').getBoundingClientRect(),l=b.lastElementChild.getBoundingClientRect(),
 cx=r.left+r.width/2,cy=r.top+r.height/2,R=r.width/2-3,inside=[[f.left,f.top],[f.right,f.top]].every(([x,y])=>Math.hypot(x-cx,y-cy)<=R);
 return {feel:b.dataset.feel,inside,top:+(f.top-r.top).toFixed(1),bot:+(r.bottom-l.bottom).toFixed(1),w:r.width,h:r.height}})"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for hr in (11,22):
        tag="day" if hr==11 else "lamp"
        for W,H in [(320,568),(390,844)]:
            ctx,pg=newpage(b,W,H); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,hr,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); tabto(pg,"today")
            for when in ("before","after"):
                if when=="after": pg.tap("#view-today [data-feel='good']"); pg.wait_for_timeout(400)
                g=pg.evaluate(GEO)
                rec("Faces",f"{tag} {W} {when} a tap: each face sits inside its circle",len(g)==3 and all(x["inside"] for x in g),g)
                rec("Faces",f"{tag} {W} {when} a tap: face and word are centred top to bottom",all(abs(x["top"]-x["bot"])<=6 for x in g),[(x["top"],x["bot"]) for x in g])
                rec("Faces",f"{tag} {W} {when}: still 44-point targets",all(x["w"]>=44 and x["h"]>=44 for x in g))
            rec("All",f"{tag} {W}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_471"); print(sum(r["ok"] for r in RES),"/",len(RES))
