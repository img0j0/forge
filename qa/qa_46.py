from lib import *
import datetime
# 0.46: the field journal. Cover, taped-in find with its calling stamped, the Binder as an album of captioned prints,
# Plain print, and What's New. (qa_351 covers the page, lamplight, ribbons and Plain; qa_contrast covers day and night.)
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
with sync_playwright() as p:
    b=p.chromium.launch()
    for W in (390,320):
        ctx,pg=newpage(b,W,844 if W==390 else 568); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,11,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.wait_for_timeout(500)
        cov=pg.evaluate("()=>{const s=document.querySelector('.scrim');const i=document.querySelector('.jlabel img');return {jc:s.classList.contains('jcov'),img:!!i&&i.src.startsWith('data:image')&&i.complete,canvas:getComputedStyle(document.getElementById('titleCv')).display}}")
        rec("Cover",f"{W}: first open is a leather journal with a Forgeling on its label",cov["jc"] and cov["img"] and cov["canvas"]=="none",cov)
        ov=pg.evaluate("()=>{const a=document.querySelector('.tagline').getBoundingClientRect(),b=document.querySelector('.jlabel img').getBoundingClientRect(),g=document.getElementById('titleGo').getBoundingClientRect();return [a.top>=b.bottom-2,g.top>=a.bottom,g.height>=44,g.bottom<=innerHeight]}")
        rec("Cover",f"{W}: the tagline sits under the picture and Begin is a full-size button on screen",all(ov),ov)
        if W==390:
            v=axe(pg); rec("A11y","the cover has no accessibility violations",not v,v)
        first_card(pg); closemodals(pg)
        if W==390:
            # Today: the find is taped in with its calling stamped beside it
            s=st(pg); c=[x for x in s["cards"] if x["id"]==s["todayCard"]][0]
            stamp=pg.evaluate("()=>{const e=document.querySelector('#view-today .jstamp');return e?[e.getAttribute('aria-hidden'),e.innerText,getComputedStyle(e).display]:null}")
            rec("Today","today's calling is stamped beside the find, as decoration",stamp and stamp[0]=="true" and stamp[2]=="flex" and "· 1" in stamp[1],stamp)
            tr=pg.evaluate("()=>getComputedStyle(document.querySelector('#view-today .herocard')).transform")
            rec("Today","the find is taped in at a slight angle",tr.startswith("matrix") and tr!="matrix(1, 0, 0, 1, 0, 0)",tr)
            hf=pg.evaluate("()=>getComputedStyle(document.querySelector('#view-today .hero h2')).fontFamily")
            rec("Today","its line is handwritten",hf.startswith("Caveat"),hf)
            v=axe(pg); rec("A11y","the journal Today page has no accessibility violations",not v,v)
            # Binder: captioned prints, nine to a page
            s=st(pg); c0=s["cards"][0]; s["cards"]=[]
            for i in range(11):
                c=json.loads(json.dumps(c0)); c.update(id=600+i,seed=3000+i*911,theme=i%5,nick="Pip" if i==10 else ""); s["cards"].append(c)
            setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg); tabto(pg,"binder")
            caps=pg.evaluate("()=>[...document.querySelectorAll('#view-binder .binder .jcap')].map(e=>[e.textContent,getComputedStyle(e).display,e.closest('button').getAttribute('aria-label')])")
            rec("Binder","each print has a handwritten caption with its name (or the name you gave it)",len(caps)==9 and caps[0][0]=="Pip" and all(x[1]=="block" for x in caps),caps[:2])
            rec("Binder","the caption is hidden from screen readers, which already hear the button's name",all(x[2].startswith("Look at") for x in caps))
            ov=pg.evaluate("()=>{const g=document.querySelector('#view-binder .binder').getBoundingClientRect();return [...document.querySelectorAll('#view-binder .binder>*')].every(e=>{const r=e.getBoundingClientRect();return r.left>=g.left-6&&r.right<=g.right+6})}")
            rec("Binder","the prints fit across the page",ov)
            v=axe(pg); rec("A11y","the album has no accessibility violations",not v,v)
            # Plain print stays after a reload
            s=st(pg); s["settings"]["hand"]=False; setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)
            rec("Print","Plain print is remembered",pg.evaluate("document.documentElement.classList.contains('plainhand')") and pg.evaluate("getComputedStyle(document.getElementById('title')).fontFamily").startswith("Fredoka"))
            # Plain look: no captions, no stamp
            s["settings"]["sky"]="plain"; setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg); tabto(pg,"binder")
            rec("Plain","in the Plain look there are no captions or stamps",pg.evaluate("[...document.querySelectorAll('.jcap,.jstamp')].every(e=>getComputedStyle(e).display==='none')"))
            s["settings"]["sky"]="auto"; s["seen"]=40; setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); w=mt(pg)
            rec("New","What's New leads with the field journal and keeps eight notes",w.find("A field journal")>=0 and w.find("A field journal")<w.find("Relics and gifts") and pg.locator("#modal .newlist li").count()==8,w[:100])
        rec("All",f"{W}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_46"); print(sum(r["ok"] for r in RES),"/",len(RES))
