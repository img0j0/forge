from lib import *
# 0.31.0: the inked map. Paper, inked coasts, watercolour realms, sea waves, trails, fog, compass and ribbon.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
INFO="""()=>{const s=document.querySelector('.mapsvg');const q=x=>s.querySelectorAll(x).length;
 const hits=[...s.querySelectorAll('.mphit')];
 const waves=[...s.querySelectorAll('path')].filter(p=>(p.getAttribute('stroke-opacity')||'')==='.38'&&/^M[\\d.-]+ [\\d.-]+q/.test(p.getAttribute('d')||''));
 const starts=waves.length?[...waves[0].getAttribute('d').matchAll(/M([\\d.-]+) ([\\d.-]+)q/g)].map(m=>[+m[1],+m[2]]):[];
 const wet=starts.filter(([x,y])=>hits.some(h=>h.isPointInFill(new DOMPoint(x,y)))).length;
 return {paper:q('.mp-paper'),grain:q('.mp-grain'),ribbon:q('.mp-rib'),compass:q('.mp-inkf'),fog:q('.mp-fog'),trails:[...s.querySelectorAll('path')].filter(p=>p.getAttribute('stroke-dasharray')==='0.1 4.2').length,
  waves:starts.length,wet,filters:[...s.querySelectorAll('filter')].map(f=>f.id).sort(),wash:q('[filter="url(#mpWash)"]'),ink:q('[filter="url(#mpInk)"]'),text:s.textContent}}"""
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        for nm,counts,known,pairs in [("one realm",[1,0,0,0,0],1,0),("three realms",[4,2,0,1,0],3,3),("all five",[12,8,6,9,5],5,6)]:
            s=build(base,counts,(),"mix"); s["seen"]=99; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
            t0=pg.evaluate("performance.now()"); openmap(pg); t1=pg.evaluate("performance.now()")
            i=pg.evaluate(INFO)
            rec("Sheet",f"{scheme}, {nm}: drawn on paper with grain, a ribbon title and a compass rose",i["paper"]==1 and i["grain"]==1 and i["ribbon"]==1 and i["compass"]==1,i)
            rec("Realms",f"{scheme}, {nm}: each known realm gets a watercolour wash and an inked edge",i["wash"]==known and i["ink"]==known,(i["wash"],i["ink"]))
            rec("Fog",f"{scheme}, {nm}: realms not found yet sit under fog",i["fog"]==5-known,i["fog"])
            rec("Trails",f"{scheme}, {nm}: trails join neighbouring realms you know",i["trails"]==pairs,i["trails"])
            rec("Sea",f"{scheme}, {nm}: waves fill the open sea and none fall inside a realm",i["waves"]>=12 and i["wet"]==0,(i["waves"],i["wet"]))
            rec("Rules",f"{scheme}, {nm}: still no counts on the Map",not re.search(r"\d+ of \d+|\d+/\d+",i["text"]),i["text"][:120])
            rec("Speed",f"{scheme}, {nm}: the map opens quickly",t1-t0<900,round(t1-t0))
        bad+=[f"{scheme}: "+v for v in axe(pg)]
        pg.screenshot(path=f"{S}/qa/qa31-{scheme}.png")
        rec("All",f"{scheme}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations on the inked map, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_31"); print(sum(r["ok"] for r in RES),"/",len(RES))
