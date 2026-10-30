from lib import *
# 0.44: realm dioramas. A fully charted realm's page on the Map opens a small floating voxel island of its five places,
# drawn by the statue viewer: turn buttons, a place list that turns a place into view and lights it, and calm under
# reduced motion. Bright and Shade realms both have one; uncharted realms do not.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
RAF="()=>{if(window.__rafw)return;window.__rafw=1;window.__raf=0;const o=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=f=>{window.__raf++;return o(f)};}"
def realm(pg,ti):
    pg.evaluate("ti=>{const x=document.createElement('button');x.dataset.realmopen=ti;document.body.appendChild(x);x.click();x.remove()}",ti); pg.wait_for_timeout(600)
def pic(pg): return pg.evaluate("document.getElementById('stCv').toDataURL()")
from PIL import Image, ImageChops
import io,base64
def moved(a,b):  # share of pixels that changed clearly between two canvas pictures
    A,B=[Image.open(io.BytesIO(base64.b64decode(x.split(',')[1]))).convert("RGB") for x in (a,b)]
    d=ImageChops.difference(A,B).convert("L").point(lambda x:255 if x>40 else 0); return sum(1 for v in d.getdata() if v)/(A.size[0]*A.size[1])
def small(pg,sel): return pg.evaluate("s=>[...document.querySelectorAll(s)].filter(b=>{const r=b.getBoundingClientRect();return r.width&&(r.width<44||r.height<44)}).map(b=>b.id||b.textContent.slice(0,20))",sel)
def setup(pg,explore,lantern=False):
    s=st(pg); c0=s["cards"][0]; extra=[]
    for t,d in ((0,False),(0,True),(1,False)):
        c=dict(c0); c.update(id=200+len(extra),theme=t,dark=d); extra.append(c)
    s["cards"]=[c for c in s["cards"] if c["theme"] not in (0,1)]+extra; s["explore"]=explore; s["opens"]=s.get("opens",[])+[s["date"]]
    if lantern: s["forge"]["made"]=list(set(s["forge"].get("made",[])+["xlantern"]))
    setst(pg,s); pg.reload(); pg.wait_for_timeout(1000); closemodals(pg)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader'])
    for rm in ("no-preference","reduce"):
        ctx,pg=newpage(b,reduced_motion=rm); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
        if rm=="no-preference":
            # ---------- not yet charted ----------
            setup(pg,{"0":3,"1":1}); realm(pg,0)
            rec("Isle","a realm with places still to find has no 3D island yet",pg.locator(".realmpage [data-isle]").count()==0 and "There is more to find here" in pg.inner_text(".realmpage"))
            # ---------- charted ----------
            setup(pg,{"0":4,"1":2}); realm(pg,0)
            bt=pg.locator(".realmpage [data-isle]")
            rec("Isle","a fully charted realm offers its island on its page",bt.count()==1 and bt.inner_text()=="See Meadow in 3D",bt.inner_text() if bt.count() else "")
            rec("Isle","…and that button is a 44-point target",not small(pg,".realmpage [data-isle]"))
            realm(pg,1); rec("Isle","a realm half charted still has none",pg.locator(".realmpage [data-isle]").count()==0)
            v=axe(pg); rec("A11y","the realm page with its island button has no accessibility violations",not v,v)
            realm(pg,0); pg.tap(".realmpage [data-isle]"); pg.wait_for_timeout(1500)
            t=mt(pg)
            rec("Isle","the island opens with its name and all five places","FULLY CHARTED" in t.upper() and "Meadow" in t and all(n in t for n in ["The Slow Hill","Birdwait Oak","The Crooked Garden","Bramble Edge","Fernlow"]),t[:160])
            rec("Isle","it is drawn in 3D (not the fallback)",pg.locator("#stCv").is_visible() and pg.locator("#stNo").is_hidden())
            lab=pg.get_attribute("#stCv","aria-label"); rec("A11y","the canvas says what it shows and names every place","floating island" in lab and "The Slow Hill" in lab and "Fernlow" in lab,lab[:120])
            rec("A11y","focus lands on Close",pg.evaluate("document.activeElement.id")=="ovClose")
            v=axe(pg); rec("A11y","the island view has no accessibility violations",not v,v)
            sm=small(pg,"#modal button"); rec("Isle","every button in the island view is at least 44 points",not sm,sm)
            rec("Isle","the turntable runs without reduced motion",pg.get_attribute("#stTurn","aria-pressed")=="true")
            pg.evaluate(RAF); pg.evaluate("window.__raf=0"); pg.wait_for_timeout(1500); rec("Isle","…and keeps drawing while it turns",pg.evaluate("window.__raf")>=30,pg.evaluate("window.__raf"))
            # tap a place: it turns into view, lights up, and the turntable stops so it stays in view
            pg.tap("[data-isp='2']"); pg.wait_for_timeout(1500)
            rec("Isle","tapping a place marks it and stops the turntable",pg.get_attribute("[data-isp='2']","aria-pressed")=="true" and pg.get_attribute("[data-isp='0']","aria-pressed")=="false" and pg.get_attribute("#stTurn","aria-pressed")=="false")
            a=pic(pg); pg.wait_for_timeout(700); m=moved(a,pic(pg)); rec("Isle","…and the island settles facing it (only motes and the glow move)",m<.03,f"{m*100:.2f}%")
            pg.tap("[data-isp='2']"); pg.wait_for_timeout(500); rec("Isle","tapping it again lets it go",pg.get_attribute("[data-isp='2']","aria-pressed")=="false")
            a=pic(pg); pg.tap("#isL"); pg.wait_for_timeout(1200); m=moved(a,pic(pg)); rec("Isle","Turn left turns it",m>.05,f"{m*100:.1f}%")
            a=pic(pg); pg.tap("#isR"); pg.wait_for_timeout(1200); m=moved(a,pic(pg)); rec("Isle","Turn right turns it",m>.05,f"{m*100:.1f}%")
            pg.tap("#ovClose"); pg.wait_for_timeout(400)
            rec("Isle","Close returns to the realm page, with focus back on the button",pg.evaluate("document.getElementById('modal').hidden") and pg.evaluate("document.activeElement&&document.activeElement.dataset.isle")=="0")
            # ---------- the other side ----------
            setup(pg,{"0":4,"5":4},lantern=True); realm(pg,5)
            bt=pg.locator(".realmpage [data-isle]")
            rec("Shade","a charted Shade realm has its own island",bt.count()==1 and bt.inner_text()=="See Bramble in 3D",bt.inner_text() if bt.count() else "")
            bt.tap(); pg.wait_for_timeout(1500); t=mt(pg)
            rec("Shade","…with its own five places, as the other side of Meadow","Bramble" in t and "The other side of Meadow" in t and "Thornkeep Gate" in t and "Fernlow’s Other Seat" in t,t[:160])
            pg.tap("#ovClose"); pg.wait_for_timeout(300)
            s=st(pg); rec("Save","opening an island stores nothing new",not any(k for k in s if "isle" in k.lower()))
            # What's New
            s["seen"]=40; setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); w=mt(pg)
            rec("New","What is new leads with Realms in 3D and keeps eight notes",w.find("Realms in 3D")>=0 and (w.find("Realms in 3D")<w.find("Safer saving") or w.find("Safer saving")<0) and pg.locator("#modal .newlist li").count()==8,w[:120])
        else:
            setup(pg,{"0":4}); realm(pg,0); pg.evaluate(RAF); pg.tap(".realmpage [data-isle]"); pg.wait_for_timeout(1500)
            rec("Calm","with reduced motion the turntable starts off",pg.get_attribute("#stTurn","aria-pressed")=="false")
            pg.evaluate("window.__raf=0"); pg.wait_for_timeout(2000); n=pg.evaluate("window.__raf")
            rec("Calm","…and the island is drawn once and rests",n<=12,n)
            a=pic(pg); pg.tap("[data-isp='3']"); pg.wait_for_timeout(500); c=pic(pg)
            rec("Calm","tapping a place turns it into view at once, with no glide",c!=a and pg.get_attribute("[data-isp='3']","aria-pressed")=="true")
            pg.evaluate("window.__raf=0"); pg.wait_for_timeout(1500); rec("Calm","…and it rests again",pg.evaluate("window.__raf")<=6 and pic(pg)==c,pg.evaluate("window.__raf"))
            pg.tap("#ovClose"); pg.wait_for_timeout(300); pg.tap(".realmpage [data-isle]"); pg.wait_for_timeout(1500)
            pg.tap("[data-isp='3']"); pg.wait_for_timeout(500); rec("Calm","the same island is drawn the same way every time",pic(pg)==c)
        rec("All",f"no page errors ({rm})",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_44"); print(sum(r["ok"] for r in RES),"/",len(RES))
