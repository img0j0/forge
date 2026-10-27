from lib import *
import datetime as _d
# 0.39.0: Voxel Statues. Cast at the Forge at bond 5 for 6 embers, one per Forgeling, keepsake as worn, 10 stands,
# Hearth shelf, close-up button, card mark, Save picture, reduced motion, no-WebGL fallback, damaged saves, axe.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def load(pg,s): s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def days(s,n):
    base=_d.date.fromisoformat(s["date"]); s["history"]+=[{"date":(base-_d.timedelta(days=40+i)).isoformat(),"status":"done","v":1} for i in range(n)]
def forge(pg): tabto(pg,"hearth"); pg.evaluate("document.getElementById('hForge').click()"); pg.wait_for_timeout(600); return pg.inner_text("#modal")
def drawn(pg): return pg.evaluate("()=>{const c=document.getElementById('stCv');if(!c||!c.width)return 0;const t=document.createElement('canvas');t.width=64;t.height=64;const x=t.getContext('2d');x.drawImage(c,0,0,64,64);const d=x.getImageData(0,0,64,64).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)n++;return n;}")
GL=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']
with sync_playwright() as p:
    b=p.chromium.launch(args=GL); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); load(pg,s)
    t=forge(pg); rec("Forge","before any Forgeling is Forgebound, the Forge explains how statues come","Statues" in t and "When a Forgeling becomes Forgebound (bond 5)" in t and pg.locator("#modal [data-scast]").count()==0)
    closemodals(pg)
    # bond-up to 5 announces it
    s=st(pg); hid=s["hearth"]["slots"][0]; c=[x for x in s["cards"] if x["id"]==hid][0]; c["bond"]=24; load(pg,s)
    tabto(pg,"hearth"); pg.evaluate("document.getElementById('hSnack').click()"); pg.wait_for_timeout(400); pg.evaluate("document.querySelector('#modal [data-snack]').click()"); pg.wait_for_timeout(900)
    rec("Bond","becoming Forgebound says the Forge could cast a statue now, for 6 embers","could cast" in pg.inner_text("#modal") and "6 embers" in pg.inner_text("#modal"),pg.inner_text("#modal")[:160])
    closemodals(pg)
    # not enough embers
    s=st(pg); s["forge"]["spent"]=max(0,len([h for h in s["history"] if h["status"]=="done"])+5); c=[x for x in s["cards"] if x["id"]==hid][0]; c["bond"]=30; c["keep"]="flower"; load(pg,s)
    t=forge(pg); rec("Forge","a Forgebound Forgeling with too few embers shows the cost, with no Cast button","statue" in t and "Needs 6 embers" in t and pg.locator("#modal [data-scast]").count()==0)
    closemodals(pg)
    s=st(pg); s["forge"]["spent"]=0; days(s,6); load(pg,s)
    e0=pg.evaluate("()=>+document.getElementById('hEmbers').textContent.split(' ')[0]") if pg.locator("#hEmbers").count() else None
    t=forge(pg); bad+=["forge sheet: "+v for v in axe(pg)]
    pg.tap("#modal [data-scast]"); pg.wait_for_timeout(3200)
    s=st(pg); c=[x for x in s["cards"] if x["id"]==hid][0]
    rec("Cast","casting spends 6 embers and keeps the keepsake it wore",c.get("statue",{}).get("keep")=="flower" and c["statue"]["at"]==s["date"] and s["forge"]["spent"]==6,(c.get("statue"),s["forge"]["spent"]))
    rec("View","the statue opens in 3D straight away, drawn on the canvas",pg.locator("#stCv").count()==1 and drawn(pg)>200 and pg.is_hidden("#stNo"),drawn(pg))
    rec("View","it is named for screen readers and can be turned with the keyboard",pg.get_attribute("#stCv","role")=="img" and "Drag to turn" in pg.get_attribute("#stCv","aria-label") and pg.get_attribute("#stCv","tabindex")=="0")
    bad+=["statue view: "+v for v in axe(pg)]
    pg.tap("#stTurn"); pg.wait_for_timeout(150); pg.tap("#stBase"); pg.wait_for_timeout(300)
    rec("View","Turntable and Stand switch, and say so",pg.get_attribute("#stTurn","aria-pressed")=="false" and pg.get_attribute("#stBase","aria-pressed")=="false" and drawn(pg)>100)
    pg.tap("#stBase"); pg.wait_for_timeout(200)
    pg.tap("#stPic"); pg.wait_for_timeout(2500)
    rec("Picture","Save picture makes a square image ready to share",pg.locator("#modal img.shareimg").count()==1 and pg.evaluate("()=>{const i=document.querySelector('#modal img.shareimg');return i.naturalWidth===1080&&i.naturalHeight===1080}") and pg.locator("#shDo").count()==1)
    bad+=["statue picture: "+v for v in axe(pg)]
    pg.tap("#stBack"); pg.wait_for_timeout(1500); rec("Picture","Back returns to the statue",pg.locator("#stCv").count()==1 and drawn(pg)>100)
    closemodals(pg)
    # one per Forgeling; the keepsake is a snapshot
    s=st(pg); c=[x for x in s["cards"] if x["id"]==hid][0]; c["keep"]="hat"; load(pg,s)
    t=forge(pg); rec("Forge","one statue per Forgeling: the Forge now offers See it, not Cast it","Cast " in t and pg.locator(f"#modal [data-scast='{hid}']").count()==0 and pg.locator(f"#modal [data-statue='{hid}']").count()==1)
    rec("Cast","changing the keepsake later leaves the statue as cast",st(pg)["cards"][[x["id"] for x in st(pg)["cards"]].index(hid)]["statue"]["keep"]=="flower")
    closemodals(pg)
    tabto(pg,"hearth"); rec("Shelf","the Forge panel at the Hearth has a Statues shelf",pg.locator(f"#view-hearth .stshelf [data-statue='{hid}']").count()==1)
    pg.evaluate(f"document.querySelector('#view-hearth .stshelf [data-statue=\"{hid}\"]').click()"); pg.wait_for_timeout(1500)
    rec("Shelf","…which opens the statue",pg.locator("#stCv").count()==1 and drawn(pg)>100); closemodals(pg)
    tabto(pg,"binder"); mk=pg.evaluate(f"()=>{{const c=document.querySelector('#view-binder .card[data-cid=\"{hid}\"] .stb');return c?c.getAttribute('aria-label'):null}}")
    rec("Card","its card wears a small statue mark",mk=="Has a statue",mk)
    pg.evaluate(f"document.querySelector('#view-binder .card[data-cid=\"{hid}\"]').click()"); pg.wait_for_timeout(800)
    rec("Card","the card's close-up has See the statue",pg.locator(f"#modal [data-statue='{hid}']").count()==1)
    pg.evaluate(f"document.querySelector('#modal [data-statue=\"{hid}\"]').click()"); pg.wait_for_timeout(1500); rec("Card","…which opens it",pg.locator("#stCv").count()==1); closemodals(pg)
    # backup round trip keeps it
    tabto(pg,"settings"); pg.evaluate("document.getElementById('btnExport').click()"); pg.wait_for_timeout(300); exp=pg.input_value("#expText"); closemodals(pg)
    s=st(pg); del s["cards"][[x["id"] for x in s["cards"]].index(hid)]["statue"]; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    tabto(pg,"settings"); pg.evaluate("document.getElementById('btnRestore').click()"); pg.wait_for_timeout(300); pg.fill("#resText",exp); pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(200); pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(700)
    rec("Backup","a backup brings the statue back",st(pg)["cards"][[x["id"] for x in st(pg)["cards"]].index(hid)].get("statue",{}).get("keep")=="flower")
    # damaged saves
    s=st(pg); s["cards"][0]["statue"]="x"; s["cards"][1]["statue"]={"at":"soon","keep":5}; s["cards"][2]["statue"]={"at":"2026-01-02","keep":7}; load(pg,s); s=st(pg)
    rec("Damaged","broken statues are dropped, a good one is kept and tidied","statue" not in s["cards"][0] and "statue" not in s["cards"][1] and s["cards"][2]["statue"]=={"at":"2026-01-02","keep":""} and not pg._errs,(s["cards"][0].get("statue"),s["cards"][2].get("statue")))
    # all ten stands draw
    ok=[]
    for ti in range(5):
        for dk in [False,True]:
            s=st(pg); c=s["cards"][2]; c["theme"]=ti; c["dark"]=dk; load(pg,s)
            pg.evaluate(f"()=>{{const b=document.createElement('button');b.dataset.statue='{c['id']}';document.getElementById('view-hearth').appendChild(b);b.click();}}"); pg.wait_for_timeout(900)
            ok.append(drawn(pg)>200); closemodals(pg)
    rec("Stands","every realm and its Shade has a stand that draws",all(ok),ok)
    s=st(pg); s["seen"]=43; setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); m=pg.inner_text("#modal")
    rec("New","What is new opens once and leads with Voxel statues","What is new" in m and m.index("Voxel statues")<m.index("The Scribe"),m[:120]); closemodals(pg)
    rec("All","no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    # reduced motion: no rise, no turntable
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); c=s["cards"][0]; c["bond"]=30; days(s,7); load(pg,s); forge(pg); pg.tap("#modal [data-scast]"); pg.wait_for_timeout(500)
    rec("Motion","with reduced motion the statue simply appears and does not spin",pg.get_attribute("#stTurn","aria-pressed")=="false" and drawn(pg)>200)
    closemodals(pg); ctx.close()
    # no WebGL: a clear fallback
    ctx,pg=newpage(b); pg.add_init_script("(()=>{const g=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,o){return /webgl/.test(t)?null:g.call(this,t,o)}})()")
    pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); s=st(pg); s["cards"][0]["bond"]=30; s["cards"][0]["statue"]={"at":s["date"],"keep":""}; load(pg,s)
    tabto(pg,"hearth"); pg.evaluate(f"document.querySelector('#view-hearth .stshelf [data-statue]').click()"); pg.wait_for_timeout(600)
    rec("Fallback","without 3D the viewer explains and shows the card sprite, with no dead buttons",pg.is_visible("#stNo") and pg.is_hidden("#stPic") and not pg._errs,pg._errs[:1])
    ctx.close()
    rec("A11y","axe: zero violations on the Forge, the statue and its picture",not bad,bad[:3])
    b.close()
save_results("qa_39"); print(sum(r["ok"] for r in RES),"/",len(RES))
