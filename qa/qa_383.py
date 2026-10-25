from lib import *
# 0.38.3: Settings folds into sections, each showing its current choice. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def opened(pg): return pg.evaluate("()=>[...document.querySelectorAll('#view-settings details.setsec')].filter(d=>d.open).map(d=>d.dataset.sec)")
def summ(pg,k): return pg.inner_text(f"#view-settings [data-sec='{k}'] .ssum")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    for scheme in ["light","dark"]:
        ctx,pg=newpage(b,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
        tabto(pg,"settings",fold=True); pg.wait_for_timeout(500)
        secs=pg.evaluate("()=>[...document.querySelectorAll('#view-settings details.setsec')].map(d=>d.dataset.sec)")
        rec("Fold",f"{scheme}: Settings is six folding sections in order of use",secs==["cards","sound","look","coll","about","feedback"],secs)
        rec("Fold",f"{scheme}: with nothing set yet, only Your cards starts open",opened(pg)==["cards"],opened(pg))
        rec("Summary",f"{scheme}: each folded row shows its current choice",summ(pg,"sound")=="On · soft music · normal volume" and summ(pg,"look")=="A mix · Follows your day" and summ(pg,"cards")=="Nothing picked yet",(summ(pg,"sound"),summ(pg,"look")))
        sz=pg.evaluate("()=>[...document.querySelectorAll('#view-settings .setsec>summary')].map(s=>s.getBoundingClientRect().height)")
        rec("A11y",f"{scheme}: every row is at least 44px tall",min(sz)>=44,sz)
        bad+=[f"{scheme} folded: "+v for v in axe(pg)]
        pg.tap("#view-settings [data-sec='sound']>summary"); pg.wait_for_timeout(300)
        rec("Open",f"{scheme}: tapping a row opens it in place",pg.is_visible("#setMusic"))
        pg.tap("#setMusic"); pg.wait_for_timeout(300)
        rec("Open",f"{scheme}: changing a setting keeps the section open, and the row updates","sound" in opened(pg) and summ(pg,"sound")=="On · no music · normal volume" and st(pg)["settings"]["music"]==False)
        pg.tap("#view-settings [data-sec='look']>summary"); pg.wait_for_timeout(300); pg.tap("[data-setsky='night']"); pg.wait_for_timeout(400)
        rec("Open",f"{scheme}: Look and feel holds mood, comfort, appearance and sky","Always night" in summ(pg,"look") and all(pg.locator(x).count()==1 for x in ["[data-setmood='cute']","#setReduce","[data-settheme='dark']","#setLore"]))
        pg.tap("[data-setsky='auto']"); pg.wait_for_timeout(300)
        bad+=[f"{scheme} open: "+v for v in axe(pg)]
        pg.tap("#view-settings [data-sec='sound']>summary"); pg.wait_for_timeout(300)
        rec("Close",f"{scheme}: tapping it again folds it",not pg.is_visible("#setMusic") and "sound" not in opened(pg))
        tabto(pg,"today"); tabto(pg,"settings",fold=True)
        rec("Remember",f"{scheme}: open sections stay open when you come back to the tab","look" in opened(pg) and "sound" not in opened(pg),opened(pg))
        if scheme=="light":
            pg.focus("#view-settings [data-sec='about']>summary"); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
            rec("Keys","Enter opens a section from the keyboard","about" in opened(pg) and pg.is_visible("#btnOdds"))
            rec("Erase","Erase sits on its own at the bottom, outside the sections",pg.evaluate("()=>{const e=document.getElementById('btnErase');return !e.closest('details')&&!!e.closest('.erase')}"))
            pg.tap("#view-settings [data-sec='cards'] [data-swant='1']"); pg.wait_for_timeout(300)
            rec("Summary","Your cards row lists what you picked","Calm" in summ(pg,"cards"))
            pg.reload(); pg.wait_for_timeout(900); closemodals(pg); tabto(pg,"settings",fold=True)
            rec("Fold","once you have picked something, Your cards starts folded too",opened(pg)==[],opened(pg))
        rec("All",f"{scheme}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations, folded and open, Light and Dark",not bad,bad[:3])
    b.close()
save_results("qa_383"); print(sum(r["ok"] for r in RES),"/",len(RES))
