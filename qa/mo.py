from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,568),(360,640),(375,667),(390,844),(412,915),(568,320)]:
        ctx,pg=newpage(b,W,H); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        for nick,age in [("",0),("M"*14,0),("",20)]:
            s=json.loads(json.dumps(base)); c=s["cards"][0]; c["nick"]=nick; s["seen"]=18
            if age: 
                import datetime; c["date"]=(datetime.date.today()-datetime.timedelta(days=age)).isoformat()
            setst(pg,s); pg.reload(); pg.wait_for_timeout(500); closemodals(pg); tabto(pg,"binder"); pg.evaluate("()=>document.querySelector('[data-insp]').click()"); pg.wait_for_timeout(500)
            m=pg.evaluate("()=>{const o=document.querySelector('#modal .ov'),sc=document.querySelector('#modal .scrim');const t=document.querySelector('#modal .rv-title').getBoundingClientRect(),cl=document.getElementById('ovClose').getBoundingClientRect();return {titleTop:Math.round(t.top),closeBot:Math.round(cl.bottom),vh:innerHeight,ovH:Math.round(o.getBoundingClientRect().height),scrimScroll:sc.scrollHeight>sc.clientHeight,ovScroll:o.scrollHeight>o.clientHeight,scrollTop:o.scrollTop,ovOver:getComputedStyle(o).overflowY,scrOver:getComputedStyle(sc).overflowY}}")
            ok=m["titleTop"]>=0 and m["scrollTop"]==0 and (m["closeBot"]<=m["vh"] or m["scrimScroll"] or m["ovScroll"])
            rec("Inspect",f"{W}x{H} nick={'long' if nick else 'none'} age={age}: title and Close reachable",ok,m)
        ctx.close()
    b.close()
print(sum(r["ok"] for r in RES),"/",len(RES))
