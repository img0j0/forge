from lib import *
# 0.22.2: adults only while testing, the privacy note and terms, and erasing everything.
import datetime
with sync_playwright() as p:
    b=p.chromium.launch(); yr=datetime.date.today().year
    ctx,pg=newpage(b); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#titleGo")
    rec("Title","the first screen says Forge is for adults 18 and up","For adults 18 and up" in pg.inner_text("#modal"))
    pg.tap("#titleGo"); pg.wait_for_timeout(300); t=pg.inner_text("#modal")
    rec("Age","the age question itself does not hint at the cutoff","18" not in t.split("Before we begin")[1].split("Month")[0],t[-160:])
    pg.select_option("#ageM","1"); pg.select_option("#ageY",str(yr-17)); pg.tap("#ageGo"); pg.wait_for_timeout(400)
    rec("Age","a 17-year-old is kindly turned away and nothing is saved","adults only" in mt(pg) and pg.evaluate("localStorage.getItem('forge-app-v1')") is None); ctx.close()
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); tabto(pg,"settings")
    t=pg.inner_text("#view-settings")
    rec("Settings","Privacy says only that you are an adult is kept, and offers the note, the terms and erasing","only that you are an adult" in t and pg.is_visible("#btnPrivacy") and pg.is_visible("#btnTerms") and pg.is_visible("#btnErase"))
    pg.evaluate("document.getElementById('btnPrivacy').click()"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Privacy","the privacy note covers what is kept, where, what never happens, hosting, deleting, age and changes",all(x in m for x in ("What Forgelings keeps","Only on this device","No tracking, no analytics, no ads","GitHub Pages","Erase everything on this device","18 and up","updated first")),m[:120])
    closemodals(pg); pg.evaluate("document.getElementById('btnTerms').click()"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Terms","the terms cover testing, age, nothing to buy, not advice, your words, as-is and the art",all(x in m for x in ("early version","18 or older","cannot be bought","not medical","stays yours","as it is","belong to their creator")),m[:120])
    small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.offsetParent).map(b=>Math.round(b.getBoundingClientRect().height)).filter(h=>h<44)")
    rec("Terms","its buttons are easy to tap",not small,small); closemodals(pg)
    pg.evaluate("document.getElementById('btnErase').click()"); pg.wait_for_timeout(200)
    rec("Erase","the first tap only asks to confirm",len(st(pg)["cards"])>=1 and "cannot be undone" in pg.inner_text("#btnErase"))
    pg.evaluate("document.getElementById('btnErase').click()"); pg.wait_for_timeout(600)
    s=st(pg)
    rec("Erase","the second tap erases everything and starts fresh at the title",(s is None or len(s.get("cards",[]))==0) and pg.locator("#titleGo").count()==1,s and len(s.get("cards",[])))
    pg.reload(); pg.wait_for_timeout(600)
    rec("Erase","…and it stays erased after reopening",pg.locator("#titleGo").count()==1 and not pg._errs,pg._errs[:1])
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); tabto(pg,"settings")
        for bt in ("btnPrivacy","btnTerms"):
            pg.evaluate(f"document.getElementById('{bt}').click()"); pg.wait_for_timeout(400); pg.wait_for_function("!document.body.classList.contains('arrive')"); pg.evaluate(AXE)
            v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
            bad+=[f"{scheme}/{bt}: {x}" for x in v]; closemodals(pg)
        ctx.close()
    rec("A11y","axe: zero violations on the privacy note and terms, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_222"); print(sum(r["ok"] for r in RES),"/",len(RES))
