from lib import *
import datetime
# 0.38.5: the daily set. Week tiles (flame, moon), a This week panel with Latest finds on a shelf, feeling faces,
# pixel toasts (gold for a new ribbon), stepped fields and the pixel age check.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    for ph,hr,sch in [("day",11,"light"),("night",22,"dark")]:
        ctx,pg=newpage(b,color_scheme=sch); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,hr,30)); pg.goto(P); pg.wait_for_selector("#titleGo")
        pg.evaluate("document.getElementById('titleGo').click()"); pg.wait_for_timeout(900)
        if pg.locator("#ageM").count():
            a=pg.evaluate("()=>{const s=document.getElementById('ageM'),cs=getComputedStyle(s),c=getComputedStyle(document.querySelector('.title-card'));return {app:cs.appearance,img:cs.backgroundImage.includes('svg'),clip:cs.clipPath.startsWith('polygon'),card:c.clipPath.startsWith('polygon')&&c.borderTopLeftRadius==='0px'}}")
            rec("Age",f"{ph}: the age check's month and year are pixel fields with a pixel arrow, in a stepped panel",a["app"]=="none" and a["img"] and a["clip"] and a["card"],a)
            pg.focus("#ageM"); f=pg.evaluate("()=>getComputedStyle(document.getElementById('ageM')).boxShadow")
            rec("Age",f"{ph}: a focused field shows a clear gold inset ring","inset" in f and "255, 211, 107" in f,f)
            bad+=[f"{ph} age: "+v for v in axe(pg)]
        first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
        s=st(pg); s["opens"]+=[s["date"]]; s["status"]="done"; s["history"]=[h for h in s["history"] if h["date"]!=s["date"]]+[{"date":s["date"],"status":"done","v":s["todayV"]}]; setst(pg,s); pg.reload(); pg.wait_for_timeout(1000); closemodals(pg); tabto(pg,"today")
        w=pg.evaluate("()=>{const box=document.querySelector('#view-today .weekbox');const ds=[...box.querySelectorAll('.dots .dot')];return {n:ds.length,letters:ds.map(d=>d.dataset.d).join(''),done:ds.filter(d=>d.classList.contains('done')).map(d=>getComputedStyle(d).backgroundImage.includes('svg')).every(Boolean),rest:ds.filter(d=>d.classList.contains('rest')).map(d=>getComputedStyle(d).backgroundImage.includes('svg')).every(Boolean),nrest:ds.filter(d=>d.classList.contains('rest')).length,now:ds.filter(d=>d.classList.contains('now')).length,labels:ds.every(d=>d.getAttribute('role')==='img'&&/: /.test(d.getAttribute('aria-label'))),finds:!!box.querySelector('.latest.shelf button'),txt:box.innerText}}")
        rec("Week",f"{ph}: the week is seven tiles with weekday letters, flames for days shown up and a moon for the rest day, today ringed",w["n"]==7 and len(w["letters"])==7 and w["done"] and w["rest"] and w["nrest"]>=1 and w["now"]==1 and w["labels"],w)
        rec("Week",f"{ph}: one This week panel holds the count and Latest finds, on a shelf","This week" in w["txt"] and "days showed up" in w["txt"] and "Latest finds" in w["txt"] and w["finds"])
        pg.tap("#view-today [data-feel='hard']"); pg.wait_for_timeout(300)
        fb=pg.evaluate("()=>[...document.querySelectorAll('#view-today .facebtn')].map(b=>({f:b.dataset.feel,svg:!!b.querySelector('svg.feelface'),h:b.querySelector('svg').getBoundingClientRect().height,t:b.innerText.trim(),p:b.getAttribute('aria-pressed')}))")
        rec("Feel",f"{ph}: How did it feel? is three pixel faces with their words, and a tap still records it",len(fb)==3 and all(x["svg"] and x["h"]>=30 for x in fb) and [x["t"] for x in fb]==["Easy","Good","Hard"] and fb[2]["p"]=="true" and st(pg)["feel"].get(st(pg)["date"])=="hard",fb)
        sz=pg.evaluate("()=>[...document.querySelectorAll('#view-today .facebtn')].map(b=>[b.offsetWidth,b.offsetHeight])")
        rec("A11y",f"{ph}: face buttons are at least 44px",all(w_>=44 and h_>=44 for w_,h_ in sz),sz)
        bad+=[f"{ph} today: "+v for v in axe(pg)]
        # toasts
        tabto(pg,"settings"); pg.evaluate("document.querySelector('[data-setmood=\"cute\"]').click()"); pg.wait_for_timeout(300)
        t=pg.evaluate("()=>{const t=document.getElementById('toast'),cs=getComputedStyle(t);return {cls:t.className,bg:cs.backgroundColor,clip:cs.clipPath.startsWith('polygon'),txt:t.innerText}}")
        rec("Toast",f"{ph}: a toast is a stepped pixel banner, not a pill",t["clip"] and "medal" not in t["cls"] and t["bg"]=="rgb(30, 23, 64)",t)
        s=st(pg); s["ribbons"]=[]; setst(pg,s); pg.reload(); pg.wait_for_timeout(2600); closemodals(pg); pg.wait_for_timeout(1500)
        t=pg.evaluate("()=>{const t=document.getElementById('toast'),cs=getComputedStyle(t),b=getComputedStyle(t,'::before');return {cls:t.className,bg:cs.backgroundColor,txt:t.innerText,medal:b.backgroundImage.includes('svg')}}")
        rec("Toast",f"{ph}: a new ribbon arrives on a gold banner with a medal, and the words are unchanged","medal" in t["cls"] and t["bg"]=="rgb(255, 211, 107)" and t["txt"].startswith("New ribbon: ") and t["medal"],t)
        # fields
        tabto(pg,"today"); pg.evaluate("document.getElementById('btnMargin').click()"); pg.wait_for_timeout(500)
        fi=pg.evaluate("()=>{const i=document.getElementById('jIn'),cs=getComputedStyle(i);return [cs.clipPath.startsWith('polygon'),cs.borderTopLeftRadius]}")
        rec("Fields",f"{ph}: text fields have stepped pixel corners",fi[0] and fi[1]=="0px",fi)
        bad+=[f"{ph} margin: "+v for v in axe(pg)]; closemodals(pg)
        rec("All",f"{ph}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); tabto(pg,"today")
    pg.tap("#view-today [data-feel='good']"); pg.wait_for_timeout(200)
    rec("Motion","with reduced motion the chosen face does not jump",pg.evaluate("()=>getComputedStyle(document.querySelector('[data-feel=good] svg')).transform")=="none"); ctx.close()
    rec("A11y","axe: zero violations on the age check, Today with the week and faces, and the margin sheet, day and night",not bad,bad[:3])
    b.close()
save_results("qa_385"); print(sum(r["ok"] for r in RES),"/",len(RES))
