from lib import *
# 0.38.9: the companionship button sits beside the awake Hearth scene; the sleeping Hearth renders without errors.
# Also They Remember: affection is free and unlimited, a wander's first find is remembered, the favourite snack is learned.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); s["opens"]+=[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(1000); closemodals(pg)
    tabto(pg,"hearth"); pg.wait_for_timeout(500)
    pos=pg.evaluate("()=>{const b=document.getElementById('hAffection'),cv=document.getElementById('hearthCv');if(!b)return null;return {txt:b.innerText,after:!!(cv.compareDocumentPosition(b)&Node.DOCUMENT_POSITION_FOLLOWING),gap:b.getBoundingClientRect().top-cv.getBoundingClientRect().bottom,h:b.offsetHeight,inPanel:!!b.closest('.panel-box')}}")
    rec("Sit","the awake Hearth offers Sit with … under the scene, first in the action grid (0.43)",pos and pos["txt"].startswith("Sit with") and pos["after"] and 0<=pos["gap"]<240 and pos["h"]>=44 and pg.evaluate("document.querySelector('.hgrid .act').id")=="hAffection",pos)
    s0=st(pg); c0=[c for c in s0["cards"] if c["id"]==s0["hearth"]["slots"][0]][0]
    for i in range(5): pg.tap("#hAffection"); pg.wait_for_timeout(150)
    s1=st(pg); c1=[c for c in s1["cards"] if c["id"]==c0["id"]][0]
    rec("Sit","sitting together is free: no visits used and bond unchanged, however often",c1.get("bond",0)==c0.get("bond",0) and s1["hearth"]["visits"]==s0["hearth"]["visits"])
    m=pg.inner_text("#hmsg"); rec("Sit","…and the line under the scene answers",len(m)>10 and pg.get_attribute("#hmsg","aria-live")=="polite",m)
    bad+=["hearth awake: "+v for v in axe(pg)]
    # the sleeping Hearth: the reported crash
    pg._errs.clear(); dev(pg,"sleep"); closemodals(pg); tabto(pg,"hearth"); pg.wait_for_timeout(900)
    sl=pg.evaluate("()=>({cv:!!document.getElementById('hearthCv'),btn:!!document.getElementById('hAffection'),relight:!!document.getElementById('hRelight'),txt:document.getElementById('view-hearth').innerText.slice(0,80)})")
    rec("Sleep","the sleeping Hearth opens without errors, with the fire to relight and no companionship button",sl["cv"] and not sl["btn"] and not pg._errs,(sl,pg._errs[:1]))
    bad+=["hearth asleep: "+v for v in axe(pg)]
    pg.evaluate("()=>{const b=document.getElementById('hRelight');b&&b.click()}"); pg.wait_for_timeout(9500); closemodals(pg); tabto(pg,"hearth"); pg.wait_for_timeout(600)
    rec("Sleep","after relighting, the button is back beside the scene",pg.locator("#hAffection").count()==1 and not pg._errs,pg._errs[:1])
    # first treasure from a wander
    pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(500); pg.evaluate("document.querySelector('#modal [data-wgo]').click()"); pg.wait_for_timeout(400); closemodals(pg)
    wid=st(pg)["wander"]["id"] if st(pg).get("wander") else None
    dev(pg,"wander"); closemodals(pg); tabto(pg,"hearth"); pg.wait_for_timeout(500); closemodals(pg)
    pg.evaluate("()=>{const b=document.getElementById('hCollect');b&&b.click()}"); pg.wait_for_timeout(1200); closemodals(pg)
    s2=st(pg); w=[c for c in s2["cards"] if c["id"]==wid]
    rec("Remember","a Forgeling remembers the first thing it brings home from a wander",bool(w) and isinstance(w[0].get("firstFind"),dict) and bool(w[0]["firstFind"].get("id")),w[0].get("firstFind") if w else None)
    # sanitizer keeps good memories, drops broken ones
    s=st(pg); s["cards"][0]["firstFind"]={"id":"nope","at":"2026-01-01"}; s["cards"][1]["firstFind"]={"id":w[0]["firstFind"]["id"] if w else "x","at":"yesterday"}; s["cards"][0]["snackKnown"]="yes"; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
    s3=st(pg); rec("Damaged","broken memories are dropped and snackKnown is only ever true or false","firstFind" not in s3["cards"][0] and "firstFind" not in s3["cards"][1] and "snackKnown" not in s3["cards"][0],(s3["cards"][0].get("firstFind"),s3["cards"][1].get("firstFind")))
    rec("A11y","axe: zero violations on the awake and sleeping Hearth",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_389"); print(sum(r["ok"] for r in RES),"/",len(RES))
