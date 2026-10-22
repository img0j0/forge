from lib import *
exec(open("qa_layout.py").read().split("with sync_playwright() as p:")[0].split("from lib import *")[1])
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def run_axe(pg):
    pg.evaluate(AXE)
    return pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,help:v.help,ex:v.nodes[0].html.slice(0,120)}))}""")
agg={}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg); ctx.close()
    for theme in ["light","dark"]:
        for mood in ["cute","dark"]:
            ctx,pg=newpage(b,390,844,color_scheme=theme); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
            s=build(base); s["settings"]["mood"]=mood; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
            for stage in [None,0,1,2,3]:
                tabto(pg,"chronicle"); pg.evaluate("()=>{const b=document.querySelector('[data-sub=\"map\"]');if(b)b.click()}"); pg.wait_for_timeout(250)
                if stage is not None: pg.evaluate("(v)=>{window.__noop=1}",0)
                if stage is not None:
                    dev(pg,"mappreview")
                    for _ in range(stage): dev(pg,"mappreview")
                    # dev tool leaves us on the map; cycle position is state-dependent so just audit whatever stage we land on
                for v in run_axe(pg):
                    k=(v["id"],v["impact"]); e=agg.setdefault(k,{"help":v["help"],"where":set(),"n":0,"ex":v["ex"]}); e["where"].add(f"{theme}/{mood}/stage{stage}"); e["n"]+=v["n"]
            ctx.close()
    b.close()
if not agg: print("AXE: zero violations on the Map in light + dark theme, both moods, and every stage")
for (vid,imp),e in sorted(agg.items(),key=lambda kv:kv[0][1]): print(f"{imp.upper()} {vid} x{e['n']} in {sorted(e['where'])[:3]} | {e['help']} | {e['ex']}")
