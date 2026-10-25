from lib import *
import datetime
# 0.38.6: emblems for games, snacks and wander realms; parchment for the map's notes and the realm page; gold wander button.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def rows(pg,sel):
    return pg.evaluate(f"()=>[...document.querySelectorAll('#modal {sel}')].map(b=>{{const s=b.querySelector('svg.rowsig');return {{svg:s?s.innerHTML:'',h:s?s.getBoundingClientRect().height:0,img:!!b.querySelector('img.gpick')}}}})")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    for ph,hr,sch in [("day",11,"light"),("night",22,"dark")]:
        ctx,pg=newpage(b,color_scheme=sch); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,hr,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
        s=st(pg); s["opens"]+=[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(1000); closemodals(pg)
        tabto(pg,"hearth"); pg.evaluate("document.getElementById('hPlay').click()"); pg.wait_for_timeout(700)
        g=rows(pg,"[data-game]")
        rec("Games",f"{ph}: each of the five games shows its own emblem, not the same Forgeling five times",len(g)==5 and all(x["svg"] and x["h"]>=36 and not x["img"] for x in g) and len({x["svg"] for x in g})==5,len({x["svg"] for x in g}))
        bad+=[f"{ph} games: "+v for v in axe(pg)]; closemodals(pg)
        tabto(pg,"hearth"); pg.evaluate("document.getElementById('hSnack').click()"); pg.wait_for_timeout(700)
        sn=rows(pg,"[data-snack]")
        rec("Snacks",f"{ph}: each snack has its own pixel food",len(sn)==4 and all(x["svg"] for x in sn) and len({x["svg"] for x in sn})==4)
        bad+=[f"{ph} snacks: "+v for v in axe(pg)]; closemodals(pg)
        tabto(pg,"hearth"); pg.evaluate("document.getElementById('hWander').click()"); pg.wait_for_timeout(700)
        wr=rows(pg,"[data-wgo]")
        rec("Wander",f"{ph}: every realm in the wander list, and Anywhere, has its mark",len(wr)>=2 and all(x["svg"] for x in wr) and len({x["svg"] for x in wr})==len(wr),len(wr))
        bad+=[f"{ph} wander: "+v for v in axe(pg)]; closemodals(pg)
        tabto(pg,"chronicle"); pg.wait_for_timeout(600)
        mc=pg.evaluate("()=>{const m=document.querySelector('.mapcap'),cs=getComputedStyle(m);return {parch:m.classList.contains('parch'),bg:cs.backgroundColor,clip:cs.clipPath.startsWith('polygon'),ink:getComputedStyle(m.querySelector('p')).color}}")
        rec("Map",f"{ph}: the notes under the map are on parchment, in dark ink",mc["parch"] and mc["bg"]=="rgb(251, 245, 230)" and mc["clip"] and mc["ink"] in ("rgb(46, 42, 71)","rgb(94, 88, 120)"),mc)
        bad+=[f"{ph} map: "+v for v in axe(pg)]
        pg.evaluate("()=>{const r=[...document.querySelectorAll('svg .mphit')].find(x=>x.dataset&&x.dataset.realm!==undefined)||document.querySelector('svg .mphit');r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); pg.wait_for_timeout(700)
        rp=pg.evaluate("()=>{const r=document.querySelector('.realmpage');if(!r)return null;const n=r.querySelector('.realmnotes'),w=r.querySelector('[data-wto]');return {notes:!!n&&getComputedStyle(n).backgroundColor==='rgb(251, 245, 230)',inside:!!w&&!!w.closest('.realmnotes'),gold:!!w&&w.classList.contains('primary'),places:!!r.querySelector('.realmnotes ul.places'),cards:r.querySelectorAll('.realmnotes [data-insp]').length}}")
        rec("Realm",f"{ph}: a realm page's places, tale and cards sit on parchment, with a gold wander button",rp and rp["notes"] and rp["inside"] and rp["gold"] and rp["places"] and rp["cards"]>=1,rp)
        bad+=[f"{ph} realm: "+v for v in axe(pg)]
        rec("All",f"{ph}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations on the games, snacks and wander sheets, the map and a realm page, day and night",not bad,bad[:3])
    b.close()
save_results("qa_386"); print(sum(r["ok"] for r in RES),"/",len(RES))
