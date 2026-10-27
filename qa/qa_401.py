from lib import *
# 0.40.1: preview a statue in clay before it can be cast (companion panel, Forge), no colour, no stand, no picture.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
DRAWN="()=>{const c=document.getElementById('stCv');if(!c||!c.width)return [0,0];const t=document.createElement('canvas');t.width=64;t.height=64;const x=t.getContext('2d');x.drawImage(c,0,0,64,64);const d=x.getImageData(0,0,64,64).data;let n=0,sat=0;for(let i=0;i<d.length;i+=4)if(d[i+3]>0){n++;const mx=Math.max(d[i],d[i+1],d[i+2]),mn=Math.min(d[i],d[i+1],d[i+2]);if(mx-mn>40)sat++;}return [n,sat];}"
def load(pg,s): s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader']); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); hid=s["hearth"]["slots"][0]; c=[x for x in s["cards"] if x["id"]==hid][0]; c["bond"]=19; load(pg,s)
    tabto(pg,"hearth"); t=pg.inner_text("#view-hearth .stline")
    rec("Panel","the companion panel says a statue waits at Forgebound, with a clay preview","A statue waits at Forgebound" in t and pg.locator(f"#view-hearth .stline [data-spre='{hid}']").count()==1,t)
    pg.tap(f"#view-hearth .stline [data-spre='{hid}']"); pg.wait_for_timeout(1500); d=pg.evaluate(DRAWN); m=pg.inner_text("#modal")
    rec("Clay","the preview opens the Forgeling's own shape in grey clay, with the points to go","in clay" in m and "6 more bond points to Forgebound" in m and d[0]>200 and d[1]<d[0]*.05,(d,m[:80]))
    rec("Clay","the preview has no stand, no Save picture, and casts nothing",pg.locator("#stBase").count()==0 and pg.locator("#stPic").count()==0 and "statue" not in [x for x in st(pg)["cards"] if x["id"]==hid][0])
    bad+=["clay: "+v for v in axe(pg)]; closemodals(pg)
    tabto(pg,"hearth"); pg.evaluate("document.getElementById('hForge').click()"); pg.wait_for_timeout(600); t=pg.inner_text("#modal")
    rec("Forge","before anyone is Forgebound, the Forge shows the closest Forgeling with points to go and a Preview","Closest to Forgebound: 6 more bond points" in t and pg.locator("#modal [data-spre]").count()==1,t[-220:])
    bad+=["forge: "+v for v in axe(pg)]; closemodals(pg)
    s=st(pg); c=[x for x in s["cards"] if x["id"]==hid][0]; c["bond"]=30; load(pg,s); tabto(pg,"hearth")
    rec("Panel","once Forgebound, the panel says the statue is ready to cast","ready to cast at the Forge" in pg.inner_text("#view-hearth .stline"))
    pg.evaluate("document.getElementById('hForge').click()"); pg.wait_for_timeout(600)
    rec("Forge","a Forgebound Forgeling without enough embers can still be previewed",pg.locator(f"#modal [data-spre='{hid}']").count()==1 or pg.locator(f"#modal [data-scast='{hid}']").count()==1)
    closemodals(pg)
    s=st(pg); c=[x for x in s["cards"] if x["id"]==hid][0]; c["statue"]={"at":s["date"],"keep":""}; load(pg,s); tabto(pg,"hearth")
    rec("Panel","after casting, the panel opens the real statue",pg.locator(f"#view-hearth .stline [data-statue='{hid}']").count()==1)
    pg.tap(f"#view-hearth .stline [data-statue='{hid}']"); pg.wait_for_timeout(1500); d=pg.evaluate(DRAWN)
    rec("Statue","the cast statue is in full colour, with its stand",d[1]>d[0]*.1 and pg.locator("#stBase").count()==1,d); closemodals(pg)
    rec("All","no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations on the clay preview and the Forge",not bad,bad[:3])
    b.close()
save_results("qa_401"); print(sum(r["ok"] for r in RES),"/",len(RES))
