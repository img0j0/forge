from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
import datetime
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def run_axe(pg):
    pg.evaluate(AXE)
    return pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,help:v.help,ex:v.nodes[0].html.slice(0,140)}))}""")
agg={}
def audit(pg,label):
    for v in run_axe(pg):
        k=(v["id"],v["impact"]); e=agg.setdefault(k,{"help":v["help"],"where":set(),"n":0,"ex":v["ex"]}); e["where"].add(label); e["n"]+=v["n"]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg); ctx.close()
    for theme in ["light","dark"]:
        for mood in ["cute","dark"]:
            ctx,pg=newpage(b,390,844,color_scheme=theme); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
            s=build(base,[4,2,7,3,1],dark_in={1,3}); s["settings"]["mood"]=mood; s["seen"]=18; s["packs"]=1; s["hearth"]["slots"]=[s["cards"][0]["id"],s["cards"][5]["id"]]
            s["journal"]={ (datetime.date.today()-datetime.timedelta(days=i)).isoformat():{"v":i%12,"text":"a line"} for i in range(3)}
            setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)
            L=f"{theme}/{mood}"
            for t in ["today","hearth","binder","chronicle","settings"]: tabto(pg,t); pg.wait_for_timeout(250); audit(pg,L+"/"+t)
            for sub in ["tales","journal"]:
                tabto(pg,"chronicle"); pg.evaluate("s=>document.querySelector('[data-sub=\"'+s+'\"]').click()",sub); pg.wait_for_timeout(250); audit(pg,L+"/chron-"+sub)
            tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"map\"]').click()"); pg.evaluate("()=>document.querySelector('.mphit[data-realm=\"2\"]').dispatch_event?0:document.querySelector('.mphit[data-realm=\"2\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); pg.wait_for_timeout(300); audit(pg,L+"/map-realm-open")
            tabto(pg,"binder"); pick_calling(pg,"2"); audit(pg,L+"/binder-calling-note")
            pg.evaluate("()=>document.querySelector('[data-insp]')&&document.querySelector('[data-insp]').click()"); pg.wait_for_timeout(500); audit(pg,L+"/inspect")
            pg.evaluate("()=>document.getElementById('inspFlip').click()"); pg.wait_for_timeout(600); audit(pg,L+"/inspect-back")
            pg.evaluate("()=>document.getElementById('ovClose').click()"); pg.wait_for_timeout(200)
            dev(pg,"agecard"); closemodals(pg); tabto(pg,"binder"); pick_calling(pg,"all"); pg.evaluate("()=>{const e=document.querySelector('[data-insp]');e&&e.click()}"); pg.wait_for_timeout(400)
            if pg.locator('#modal [data-kept]').count():
                pg.evaluate("()=>document.querySelector('#modal [data-kept]').click()"); pg.wait_for_timeout(400); audit(pg,L+"/second-reading")
            closemodals(pg); pg.evaluate("()=>{const b=document.getElementById('keptBack')||document.getElementById('ovClose');b&&b.click()}"); pg.wait_for_timeout(200)
            tabto(pg,"today"); pg.evaluate("()=>{const b=document.getElementById('btnPack');b&&b.click()}"); pg.wait_for_timeout(500); audit(pg,L+"/pack-sealed")
            ctx.close()
    b.close()
if not agg: print("AXE2: zero violations across Today, Hearth, Binder (with calling note), Map tabs, realm page, Tales, Journal, Settings, card, card back, second reading and pack, in light and dark theme, both moods")
for (vid,imp),e in sorted(agg.items(),key=lambda kv:kv[0][1]): print(f"{imp.upper()} {vid} x{e['n']} in {sorted(e['where'])[:4]} | {e['help']} | {e['ex']}")
