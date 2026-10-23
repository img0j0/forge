from lib import *
import datetime
# 0.35.1: Living Sky. The page is the sky; the interface is dark glass on it. Plain keeps the old look.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE)
    pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def html_attr(pg): return pg.evaluate("()=>({ls:document.documentElement.classList.contains('ls'),ink:document.documentElement.getAttribute('data-skyink'),bg:getComputedStyle(document.documentElement).getPropertyValue('--bg').trim(),meta:[...document.querySelectorAll('meta[name=theme-color]')].map(m=>m.content)})")
def setup(b,hr,scheme="light"):
    ctx,pg=newpage(b,color_scheme=scheme); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,hr,30))
    pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); s["opens"]+=[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg); return ctx,pg
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    for hr,scheme,ph,ink in [(11,"light","day","dark"),(6,"light","dawn","dark"),(18,"light","dusk","light"),(22,"light","night","light"),(11,"dark","day","light")]:
        ctx,pg=setup(b,hr,scheme); a=html_attr(pg)
        rec("Sky",f"{scheme} {ph}: Living Sky is on by default, with {ink} ink for text on the sky",a["ls"] and a["ink"]==ink,a)
        rec("Sky",f"{scheme} {ph}: the page colour and the browser bar follow the sky",a["bg"].startswith("#") and all(m.lower()==a["bg"].lower() for m in a["meta"]),a)
        for t in ["today","hearth","binder","chronicle","settings"]:
            tabto(pg,t); pg.wait_for_timeout(500); bad+=[f"{scheme} {ph} {t}: "+v for v in axe(pg)]
        if ph=="dusk":
            tabto(pg,"hearth"); pg.evaluate("document.getElementById('hForge').click()"); pg.wait_for_timeout(600); bad+=["forge sheet: "+v for v in axe(pg)]; closemodals(pg)
            tabto(pg,"chronicle"); pg.evaluate("()=>{const b=document.querySelector('[data-sub=\"journal\"]');b&&b.click()}"); pg.wait_for_timeout(600); bad+=["journal: "+v for v in axe(pg)]
            pg.evaluate("()=>{const b=document.querySelector('[data-sub=\"tales\"]');b&&b.click()}"); pg.wait_for_timeout(600); bad+=["tales: "+v for v in axe(pg)]
        if ph=="day" and scheme=="light":
            tabto(pg,"today"); pr=pg.evaluate("()=>{const b=document.querySelector('#view-today .primary');const cs=getComputedStyle(b);return {clip:cs.clipPath.slice(0,20),bg:cs.backgroundImage.slice(0,40),r:cs.borderTopLeftRadius}}")
            rec("Look","the main button is pixel-stepped gold with a press edge",pr["clip"].startswith("polygon") and "gradient" in pr["bg"] and pr["r"]=="0px",pr)
            pn=pg.evaluate("()=>getComputedStyle(document.querySelector('#view-today .hero')).backgroundColor==='rgba(20, 15, 48, 0.9)'")
            rec("Look","panels are dark glass over the sky",pn)
            ic=pg.evaluate("()=>[...document.querySelectorAll('.tab svg')].map(s=>s.getAttribute('viewBox')+'|'+s.classList.contains('pi'))")
            rec("Look","all five tabs have pixel icons",len(ic)==5 and all(x=="0 0 12 12|true" for x in ic),ic)
            h1=pg.evaluate("()=>getComputedStyle(document.getElementById('title')).fontFamily")
            rec("Look","page titles use the pixel font",'VT323' in h1,h1)
            pg.focus("#view-today .primary"); pg.keyboard.press("Tab"); pg.keyboard.press("Shift+Tab")
            fs=pg.evaluate("()=>{const e=document.activeElement;return e&&e.classList.contains('primary')?getComputedStyle(e).boxShadow:''}")
            rec("A11y","a focused pixel button shows a clear inset ring (outlines would be clipped)","inset" in fs,fs)
            pg.evaluate("document.querySelector('.tab[data-tab=\"hearth\"]').click()"); en=pg.evaluate("()=>document.getElementById('view-hearth').classList.contains('enter')&&document.getAnimations().some(a=>a.animationName==='lsRise')")
            rec("Motion","opening a tab plays a short staggered entrance",en)
            pg.wait_for_timeout(900); rec("Motion","…which ends and clears itself",not pg.evaluate("document.getElementById('view-hearth').classList.contains('enter')"))
            # reduced motion: no entrance
            s=st(pg); s["settings"]["reduce"]=True; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
            pg.evaluate("document.querySelector('.tab[data-tab=\"binder\"]').click()"); rm=pg.evaluate("()=>document.getAnimations().some(a=>a.animationName==='lsRise')")
            rec("Motion","with reduced motion on, tabs open without the entrance",not rm)
            # Plain: the old look, untouched
            tabto(pg,"settings"); pg.evaluate("document.querySelector('[data-setsky=\"plain\"]').click()"); pg.wait_for_timeout(500); a=html_attr(pg)
            pl=pg.evaluate("()=>{const b=document.querySelector('#view-settings .chip');return getComputedStyle(b).borderTopLeftRadius}")
            rec("Plain","Sky: Plain turns Living Sky off and brings back the old look",not a["ls"] and a["ink"] is None and pl!="0px" and pg.evaluate("document.getElementById('skyCv').hidden"),(a,pl))
            rec("Plain","…and the browser bar colour returns to the app's own",a["meta"]==["#F1EDF8","#16132E"],a["meta"])
            bad+=["plain settings: "+v for v in axe(pg)]
            pg.evaluate("document.querySelector('[data-setsky=\"auto\"]').click()"); pg.wait_for_timeout(500)
            rec("Plain","switching back to Follows your day turns Living Sky on again",html_attr(pg)["ls"])
            st_txt=pg.inner_text("#view-settings")
            rec("Copy","the Sky setting explains Light, Dark and Plain","Light and Dark set how bright it is" in st_txt and "Plain keeps a quiet, flat look" in st_txt)
            pg.evaluate("document.querySelector('[data-settheme=\"dark\"]').click()"); pg.wait_for_timeout(400)
            rec("Sky","choosing Dark gives the deep sky and light ink straight away",html_attr(pg)["ink"]=="light")
        rec("All",f"{scheme} {ph}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations on every tab at dawn, day, dusk and night, Light and Dark, and in Plain",not bad,bad[:4])
    b.close()
save_results("qa_351"); print(sum(r["ok"] for r in RES),"/",len(RES))
