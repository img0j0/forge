from lib import *
# 0.38.4: today's card has a real face: the deck's indigo and gold frame, a pixel emblem per calling, a ribbon
# with name and ability, the small thing on a plate, a card number. Checked for all twelve callings and own things.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def setday(pg,v,own=None):
    s=st(pg); s["owns"]=[own] if own else []; s["todayOwn"]=own["id"] if own else None
    if v is not None: s["todayV"]=v
    s["status"]="revealed"; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"today")
def face(pg):
    pg.evaluate("document.getElementById('btnCard').click()"); pg.wait_for_timeout(1100)
    return pg.evaluate("""()=>{const f=document.querySelector('#modal .vfront');const b=f.querySelector('.vband b'),sm=f.querySelector('.vband small'),fr=f.getBoundingClientRect(),by=f.querySelector('.vbody').getBoundingClientRect();
      return {sig:f.querySelector('.ccart svg.sigil')?f.querySelector('.ccart svg.sigil').innerHTML:'',name:b.innerText,ab:sm?sm.innerText:'',no:f.querySelector('.ccno').innerText,
        cut:b.scrollWidth>b.clientWidth+1,fits:by.bottom<=fr.bottom+0.5&&f.scrollHeight<=f.clientHeight+1,cc:f.style.getPropertyValue('--cc'),plate:f.querySelector('.ccplate').innerText}}""")
VN=["Clarity","Leverage","Depth","Velocity","Connection","Resilience","Play","Craft","Silence","Courage","Systems","Presence"]
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    for scheme,w in [("light",390),("dark",320)]:
        ctx,pg=newpage(b,color_scheme=scheme,w=w,h=700); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"next"); closemodals(pg)
        sigs=set(); allok=True; notes=[]
        for v in range(12):
            setday(pg,v); f=face(pg); sigs.add(f["sig"])
            ok=f["sig"]!="" and f["name"].lower()==VN[v].lower() and f["no"]==f"No. {v+1:02d}" and f["ab"]!="" and not f["cut"] and f["fits"] and f["cc"].startswith("#") and "Today's small thing".upper() in f["plate"].upper()
            if not ok: allok=False; notes.append((v,f["name"],f["cut"],f["fits"]))
            if v in (0,5) : bad+=[f"{scheme} card {v}: "+x for x in axe(pg)]
            closemodals(pg)
        rec("Face",f"{scheme} {w}px: all twelve callings show their emblem, full name, ability and number, and everything fits on the card",allok,notes[:3])
        rec("Face",f"{scheme}: each calling has its own emblem",len(sigs)==12,len(sigs))
        t=pg.evaluate("()=>{const t=document.querySelector('#view-today .taskface');return {sig:!!t.querySelector('.tfart svg.sigil'),band:t.querySelector('.band').innerText,cc:t.style.getPropertyValue('--cc'),bg:getComputedStyle(t).backgroundImage}}")
        rec("Today",f"{scheme}: Today's card shows the emblem and calling, in the calling's colour",t["sig"] and t["band"].lower()=="presence" and t["cc"].upper()=="#BDE5CB" and "svg+xml" in t["bg"],t)
        bad+=[f"{scheme} today: "+x for x in axe(pg)]
        own={"id":1,"text":"Walk around the block slowly and notice three new things","k":4,"days":[]}
        setday(pg,None,own); f=face(pg)
        rec("Own",f"{scheme}: your own small thing gets the quill, 'Yours' and no ability line",f["sig"]!="" and f["sig"] not in sigs and f["name"].upper().startswith("YOURS") and f["ab"]=="" and f["no"]=="Yours" and not f["cut"] and f["fits"],f)
        bad+=[f"{scheme} own card: "+x for x in axe(pg)]; closemodals(pg)
        rec("All",f"{scheme}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"next"); closemodals(pg); setday(pg,3)
    rec("Motion","with reduced motion, the emblem keeps still",not pg.evaluate("()=>document.getAnimations().some(a=>a.animationName==='sigBob')")); ctx.close()
    rec("A11y","axe: zero violations on Today's card and the full card, Light and Dark",not bad,bad[:3])
    b.close()
save_results("qa_384"); print(sum(r["ok"] for r in RES),"/",len(RES))
