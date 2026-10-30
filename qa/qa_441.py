from lib import *
# 0.44.1 interface pass: the fireside picker fits every phone width, the Binder's summary stays clear of the sky's
# sun/moon, and the Hearth's lantern hint opens the Forge.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def setup(pg):
    s=st(pg); c0=s["cards"][0]; cards=[]
    for i in range(14):
        c=json.loads(json.dumps(c0)); c.update(id=300+i,seed=7000+i*977,theme=i%5,dark=False); cards.append(c)
    s["cards"]=cards; s["explore"]={"0":4}; s["forge"]["made"]=[m for m in s["forge"].get("made",[]) if m!="xlantern"]
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,568),(375,667),(430,932)]:
        ctx,pg=newpage(b,W,H); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); setup(pg)
        # picker
        hsheet(pg,"furn") if False else None
        tabto(pg,"hearth"); pg.evaluate("document.getElementById('hChange').click()"); pg.wait_for_timeout(500)
        g=pg.evaluate("(()=>{const g=document.querySelector('.pickgrid');const bs=[...g.querySelectorAll('.pickbtn')].map(b=>b.getBoundingClientRect());const gr=g.getBoundingClientRect();return {sw:g.scrollWidth,cw:g.clientWidth,out:bs.filter(r=>r.left<gr.left-1||r.right>gr.right+1).length,cols:getComputedStyle(g).gridTemplateColumns.split(' ').length}})()")
        rec("Picker",f"{W}: every Forgeling in Who sits by the fire? fits across, none cut off",g["sw"]<=g["cw"]+1 and g["out"]==0,g)
        rec("Picker",f"{W}: as many columns as fit ({g['cols']})",g["cols"]==(3 if W<400 else 4),g["cols"])
        closemodals(pg)
        # Binder summary vs the sky's sun/moon (drawn ~21vw from the right edge, 17% down, radius ~5.2vw)
        tabto(pg,"binder")
        hit=pg.evaluate("""(()=>{const k=innerWidth/96,cx=innerWidth-15*k,cy=.17*innerHeight,R=5.5*k;const p=document.querySelector('#view-binder .summary');
          const rg=document.createRange();rg.selectNodeContents(p);return [...rg.getClientRects()].some(r=>r.right>cx-R&&r.left<cx+R&&r.bottom>cy-R&&r.top<cy+R)})()""")
        rec("Sky",f"{W}: the Binder's summary text stays clear of the sun or moon",not hit)
        # lantern hint
        tabto(pg,"hearth"); lb=pg.locator("#hLanternGo")
        rec("Lantern",f"{W}: the lantern hint is a 44-point button",lb.count()==1 and lb.bounding_box()["height"]>=44,lb.inner_text() if lb.count() else "")
        if W==375:
            v=axe(pg); rec("A11y","the Hearth with the lantern link has no accessibility violations",not v,v)
            lb.click(); pg.wait_for_timeout(600)
            rec("Lantern","tapping it opens the Forge",not pg.evaluate("document.getElementById('modal').hidden") and "Crossing Lantern" in mt(pg),mt(pg)[:80])
        rec("All",f"{W}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_441"); print(sum(r["ok"] for r in RES),"/",len(RES))
