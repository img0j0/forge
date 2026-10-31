from lib import *
import datetime
# 0.35.1: Living Sky. 0.46: the field journal replaces it: a paper page by day, lamplit at dusk, night or Dark; ribbons for tabs;
# handwriting with a Plain print option. Plain still keeps the old flat look.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE)
    pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def html_attr(pg): return pg.evaluate("()=>({jr:document.documentElement.classList.contains('jr'),ls:document.documentElement.classList.contains('ls'),page:document.documentElement.getAttribute('data-page'),body:getComputedStyle(document.body).backgroundColor,meta:[...document.querySelectorAll('meta[name=theme-color]')].map(m=>m.content)})")
def setup(b,hr,scheme="light"):
    ctx,pg=newpage(b,color_scheme=scheme); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,hr,30))
    pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); s["opens"]+=[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg); return ctx,pg
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    DESK={"day":("#3B2A22","rgb(59, 42, 34)"),"lamp":("#140F0C","rgb(20, 15, 12)")}
    for hr,scheme,ph,page in [(11,"light","day","day"),(6,"light","dawn","day"),(18,"light","dusk","lamp"),(22,"light","night","lamp"),(11,"dark","day","lamp")]:
        ctx,pg=setup(b,hr,scheme); a=html_attr(pg)
        rec("Page",f"{scheme} {ph}: the journal is on by default, on a {page} page",a["jr"] and not a["ls"] and a["page"]==page,a)
        rec("Page",f"{scheme} {ph}: the desk colour and the browser bar match the page",a["body"]==DESK[page][1] and all(m==DESK[page][0] for m in a["meta"]),a)
        for t in ["today","hearth","binder","chronicle","settings"]:
            tabto(pg,t); pg.wait_for_timeout(500); bad+=[f"{scheme} {ph} {t}: "+v for v in axe(pg)]
        if ph=="dusk":
            tabto(pg,"hearth"); pg.evaluate("document.getElementById('hForge').click()"); pg.wait_for_timeout(600); bad+=["forge sheet: "+v for v in axe(pg)]; closemodals(pg)
            tabto(pg,"chronicle"); pg.evaluate("()=>{const b=document.querySelector('[data-sub=\"journal\"]');b&&b.click()}"); pg.wait_for_timeout(600); bad+=["journal: "+v for v in axe(pg)]
            pg.evaluate("()=>{const b=document.querySelector('[data-sub=\"tales\"]');b&&b.click()}"); pg.wait_for_timeout(600); bad+=["tales: "+v for v in axe(pg)]
        if ph=="day" and scheme=="light":
            tabto(pg,"today"); pr=pg.evaluate("()=>{const b=document.querySelector('#view-today .primary');const cs=getComputedStyle(b);return {bg:cs.backgroundImage.slice(0,40),r:cs.borderTopLeftRadius}}")
            rec("Look","the main button is gold with a press edge",("gradient" in pr["bg"]) and pr["r"]=="0px",pr)
            pn=pg.evaluate("()=>{const h=getComputedStyle(document.querySelector('#view-today .hero')),r=getComputedStyle(document.querySelector('#view-today .group'));return [h.backgroundColor,h.backgroundImage,r.backgroundColor,r.borderTopStyle,r.borderImageSource]}")
            rec("Look","panels are part of the page: no boxes, a dotted rule between sections",pn[0]=="rgba(0, 0, 0, 0)" and pn[1]=="none" and pn[2]=="rgba(0, 0, 0, 0)" and pn[3]=="dotted" and pn[4]=="none",pn)
            ic=pg.evaluate("()=>[...document.querySelectorAll('.tab svg')].map(s=>s.getAttribute('viewBox')+'|'+s.classList.contains('pi'))")
            rec("Look","all five tabs keep their pixel icons",len(ic)==5 and all(x=="0 0 12 12|true" for x in ic),ic)
            rb=pg.evaluate("()=>[...document.querySelectorAll('.tab')].map(t=>{const cs=getComputedStyle(t);return [cs.clipPath.slice(0,7),cs.backgroundColor,Math.round(t.getBoundingClientRect().height)]})")
            rec("Look","the tabs are ribbons, each its own colour, and the open page's ribbon hangs longer",all(x[0]=="polygon" for x in rb) and len(set(x[1] for x in rb))==5 and rb[0][2]>max(x[2] for x in rb[1:]),rb)
            h1=pg.evaluate("()=>getComputedStyle(document.getElementById('title')).fontFamily")
            rec("Look","page titles are handwritten",h1.startswith('Caveat'),h1)
            pg.focus("#view-today .primary"); pg.keyboard.press("Tab"); pg.keyboard.press("Shift+Tab")
            fs=pg.evaluate("()=>{const e=document.activeElement;return e&&e.classList.contains('primary')?getComputedStyle(e).outlineStyle+' '+getComputedStyle(e).outlineWidth:''}")
            rec("A11y","a focused button shows a clear gold ring",fs.startswith("solid 3"),fs)
            pg.evaluate("document.querySelector('.tab[data-tab=\"hearth\"]').click()"); en=pg.evaluate("()=>document.getElementById('view-hearth').classList.contains('enter')&&document.getAnimations().some(a=>a.animationName==='lsRise')")
            rec("Motion","opening a tab plays a short staggered entrance",en)
            pg.wait_for_timeout(1600); rec("Motion","…which ends and clears itself",not pg.evaluate("document.getElementById('view-hearth').classList.contains('enter')"))
            s=st(pg); s["settings"]["reduce"]=True; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
            pg.evaluate("document.querySelector('.tab[data-tab=\"binder\"]').click()"); rm=pg.evaluate("()=>document.getAnimations().some(a=>a.animationName==='lsRise')")
            rec("Motion","with reduced motion on, tabs open without the entrance",not rm)
            # Plain print
            tabto(pg,"settings"); pg.evaluate("document.querySelector('[data-sethand=\"0\"]').click()"); pg.wait_for_timeout(300)
            h1=pg.evaluate("()=>getComputedStyle(document.getElementById('title')).fontFamily")
            rec("Print","Plain print swaps the handwriting for the regular font",pg.evaluate("document.documentElement.classList.contains('plainhand')") and h1.startswith('Fredoka') and st(pg)["settings"]["hand"] is False,h1)
            pg.evaluate("document.querySelector('[data-sethand=\"1\"]').click()"); pg.wait_for_timeout(300)
            rec("Print","…and Handwriting brings it back",not pg.evaluate("document.documentElement.classList.contains('plainhand')"))
            # Plain: the old look, untouched
            pg.evaluate("document.querySelector('[data-setsky=\"plain\"]').click()"); pg.wait_for_timeout(500); a=html_attr(pg)
            pl=pg.evaluate("()=>{const b=document.querySelector('#view-settings .chip');return getComputedStyle(b).borderTopLeftRadius}")
            rec("Plain","Plain turns the journal off and brings back the old flat look",not a["jr"] and not a["ls"] and a["page"] is None and pl!="0px" and pg.evaluate("document.getElementById('skyCv').hidden"),(a,pl))
            rec("Plain","…and the browser bar colour returns to the app's own",a["meta"]==["#F1EDF8","#16132E"],a["meta"])
            rec("Plain","…and the Writing choice is hidden, since there is no handwriting",pg.locator("[data-sethand]").count()==0)
            bad+=["plain settings: "+v for v in axe(pg)]
            pg.evaluate("document.querySelector('[data-setsky=\"auto\"]').click()"); pg.wait_for_timeout(500)
            rec("Plain","switching back to Follows your day opens the journal again",html_attr(pg)["jr"])
            st_txt=pg.inner_text("#view-settings")
            rec("Copy","the page setting explains lamplight, Dark and Plain","paper by day and lamplit at dusk and night" in st_txt and "Plain keeps a quiet, flat look" in st_txt and "Always lamplit" in st_txt)
            pg.evaluate("document.querySelector('[data-settheme=\"dark\"]').click()"); pg.wait_for_timeout(400)
            rec("Page","choosing Dark gives the lamplit page straight away",html_attr(pg)["page"]=="lamp")
        rec("All",f"{scheme} {ph}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations on every tab at dawn, day, dusk and night, Light and Dark, and in Plain",not bad,bad[:4])
    b.close()
save_results("qa_351"); print(sum(r["ok"] for r in RES),"/",len(RES))
