from lib import *
# 0.30.0: pixel-art curios, a real shelf, a curio by the fire, the gift unwrap. Real taps.
import base64
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
def load(pg,s):
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def openshelf(pg):
    tabto(pg,"hearth"); pg.evaluate("()=>{document.querySelectorAll('#view-hearth details.more').forEach(d=>{if(/Curio shelf/.test(d.querySelector('summary').textContent))d.open=true})}"); pg.wait_for_timeout(250)
EMOJI=re.compile("[\U0001F300-\U0001FAFF✨❄⭐]")
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def heartpx(pg):
    return pg.evaluate("()=>{const c=document.getElementById('hearthCv');const d=c.getContext('2d').getImageData(39,55,16,16).data;let s=0;for(let i=0;i<d.length;i+=4)s+=d[i+2]-d[i];return s/256}")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,A=newpage(b); A.goto(P); A.wait_for_selector("#titleGo"); first_card(A); closemodals(A)
    s=build(st(A),[2,1,0,1,0]); s["seen"]=99; ids=[c["id"] for c in s["cards"]]; s["hearth"]["slots"]=ids[:2]
    s["curios"]={k:{"n":1,"cid":ids[0],"at":s["date"]} for k in ["acorn","mushroom","snow"]}; s["curios"]["moon"]={"n":2,"cid":0,"at":s["date"],"gift":1,"from":"Pip"}
    load(A,s)
    rec("Room","the app stays under its size budget (1 MB, as qa_22)",len(open(P.replace("file://","")).read().encode())<1_000_000 if P.startswith("file://") else True)
    rec("Room","the unused Fredoka 400 face is gone, the used ones remain",A.evaluate("[...document.styleSheets].flatMap(s=>{try{return [...s.cssRules]}catch(e){return []}}).filter(r=>r.cssText&&r.cssText.startsWith('@font-face')&&r.cssText.includes('Fredoka')).map(r=>r.style.fontWeight).sort().join(',')")=="500,600")
    openshelf(A); sh=A.inner_text("#view-hearth .shelf")
    rec("Shelf","the shelf has a shelf per realm with four places each",A.locator(".shelf .splank").count()==5 and A.locator(".shelf .scur").count()==20)
    rec("Shelf","found curios are drawn, missing ones are faint outlines",A.locator(".shelf .scur:not(.off)").count()==4 and A.locator(".shelf .scur.off").count()==16 and A.evaluate("[...document.querySelectorAll('.shelf .cimg')].every(i=>i.complete&&i.naturalWidth===16)"))
    rec("Shelf","realms you know are named the way the Map names them, others are not given away","Meadow" in sh and "Frost" in sh and "A realm not yet on your map" in sh and "Tide" not in sh and "Dusk" not in sh,sh[:200])
    rec("Shelf","no emoji left on the shelf",not EMOJI.search(A.inner_html("#view-hearth .shelf")))
    small=A.evaluate("[...document.querySelectorAll('.shelf .scur')].filter(b=>{const r=b.getBoundingClientRect();return r.height<44||r.width<44}).length")
    rec("Shelf","every curio on the shelf is easy to tap",small==0,small)
    bad+=["shelf: "+v for v in axe(A)]
    # close up
    A.tap("[data-cur='mushroom']"); A.wait_for_timeout(600); m=mt(A)
    rec("Close up","tapping a curio shows it large with its story, when it was found and its tale page","Moonlit mushroom" in m and "glowed whenever nobody looked" in m and "Found " in m and "A page of an old" in m and A.locator("#modal .cbig .cimg").count()==1,m[:200])
    bad+=["closeup: "+v for v in axe(A)]
    A.tap("#curFire"); A.wait_for_timeout(500)
    rec("Fire","Set it by the fire puts it there",st(A)["hearth"].get("curio")=="mushroom" and "now sits by the fire" in A.inner_text("#hmsg"))
    openshelf(A); A.tap("[data-cur='moon']"); A.wait_for_timeout(500); m=mt(A)
    rec("Close up","a gifted curio says who sent it, and how many you have","Pip sent this as a gift" in m and "You have 2" in m,m[:200]); closemodals(A)
    openshelf(A); A.tap("[data-cur='coin']"); A.wait_for_timeout(500); m=mt(A)
    rec("Close up","a missing curio from an unknown realm doesn't give the realm away","Not found yet" in m and "somewhere you have not been yet" in m and "Tide" not in m,m[:200]); closemodals(A)
    openshelf(A); A.tap("[data-cur='bell']"); A.wait_for_timeout(500); m=mt(A)
    rec("Close up","a missing curio from a known realm says where to wander","somewhere in Frost" in m,m[:200]); closemodals(A)
    # the Hearth scene
    s1=st(A); s1["hearth"]["curio"]="snow"; load(A,s1); tabto(A,"hearth"); A.wait_for_timeout(400); with_c=heartpx(A)
    s2=st(A); s2["curios"]={}; s2["hearth"].pop("curio",None); load(A,s2); tabto(A,"hearth"); A.wait_for_timeout(400); without=heartpx(A)
    rec("Fire","the curio is drawn beside the fire in the Hearth scene, and nothing is drawn with no curios",with_c-without>8,(round(with_c),round(without)))
    s3=st(A); s3["curios"]={"acorn":{"n":1,"cid":ids[0],"at":s3["date"]},"snow":{"n":1,"cid":ids[0],"at":s3["date"]}}; load(A,s3); tabto(A,"hearth"); A.wait_for_timeout(400); x1=heartpx(A)
    s3=st(A); s3["curios"]={"snow":{"n":1,"cid":ids[0],"at":s3["date"]},"acorn":{"n":1,"cid":ids[0],"at":s3["date"]}}; load(A,s3); tabto(A,"hearth"); A.wait_for_timeout(400); x2=heartpx(A)
    rec("Fire","with none chosen, the latest curio found sits by the fire",x1-x2>15,(round(x1),round(x2)))
    # wander return uses the sprite
    s4=st(A); s4["wander"]={"id":ids[0],"start":0,"ready":0,"realm":0}; load(A,s4); tabto(A,"hearth")
    A.evaluate("()=>{const b=document.getElementById('hCollect');b&&b.click()}"); A.wait_for_timeout(900); m=mt(A)
    rec("Wander","the wander return shows the curio as pixel art, not an emoji",A.locator("#modal .cbig .cimg").count()==1 and not EMOJI.search(A.inner_html("#modal .cbig")),m[:100])
    closemodals(A)
    # tales list
    tabto(A,"chronicle"); A.evaluate("()=>document.querySelector('[data-sub=\"tales\"]').click()"); A.wait_for_timeout(300)
    rec("Tales","the old tales list uses the curio sprites",A.locator(".otale li .g .cimg").count()>=1 and not EMOJI.search(A.inner_html(".otale")))
    # gift unwrap
    g={"v":1,"g":"abcdef123456","s":"zzzzzz999999","c":"crystal","n":"Pip","t":0,"d":0,"r":2,"e":123456789,"k":3}
    code=base64.urlsafe_b64encode(json.dumps(g).encode()).decode().rstrip("=")
    A.goto("about:blank"); A.goto(P.split("#")[0]+"#gift="+code); A.wait_for_timeout(3000)
    rec("Gift","a gift arrives as a bundle that opens to the curio",A.locator("#modal .gcur .gbun").count()==1 and A.locator("#modal .gcur .gitem").count()==1)
    A.wait_for_timeout(1700)
    rec("Gift","after the unwrap, the curio is showing and the bundle is gone",A.evaluate("(()=>{const b=getComputedStyle(document.querySelector('#modal .gbun')).opacity,i=getComputedStyle(document.querySelector('#modal .gitem')).opacity;return +b<.05&&+i>.95})()"))
    bad+=["gift: "+v for v in axe(A)]
    A.tap("#giftKeep"); A.wait_for_timeout(400)
    rec("Gift","the kept gift remembers who sent it",st(A)["curios"]["crystal"].get("from")=="Pip"); closemodals(A)
    # reduced motion: the curio is simply there
    c2,R=newpage(b,reduced_motion="reduce"); R.goto(P); R.wait_for_selector("#titleGo"); first_card(R); closemodals(R); sR=st(R); sR["seen"]=99; load(R,sR)
    R.goto("about:blank"); R.goto(P.split("#")[0]+"#gift="+base64.urlsafe_b64encode(json.dumps(dict(g,g="qqqqqq123456")).encode()).decode().rstrip("=")); R.wait_for_timeout(3000)
    rec("Motion","with reduced motion the gift shows the curio at once, no bundle",R.evaluate("(()=>{const b=document.querySelector('#modal .gbun'),i=document.querySelector('#modal .gitem');return !!i&&getComputedStyle(b).display==='none'&&+getComputedStyle(i).opacity>.95})()"))
    # dark theme
    c3,D=newpage(b,color_scheme="dark"); D.goto(P); D.wait_for_selector("#titleGo"); first_card(D); closemodals(D); load(D,s); openshelf(D)
    bad+=["dark shelf: "+v for v in axe(D)]
    rec("Dark","in dark theme found curios get a soft light edge",D.evaluate("getComputedStyle(document.querySelector('.shelf .scur:not(.off) .cimg')).filter").startswith("drop-shadow"))
    # damaged save
    s5=st(A); s5["hearth"]["curio"]="<dragon>"; load(A,s5); tabto(A,"hearth")
    rec("Damaged","a broken fire curio in a save is repaired","curio" not in st(A)["hearth"] and not A._errs)
    rec("A11y","axe: zero violations on the shelf, close-up and gift, light and dark",not bad,bad[:3])
    for nm,pg in (("main",A),("reduced",R),("dark",D)): rec("All",f"{nm}: no page errors",not pg._errs,pg._errs[:1])
    b.close()
save_results("qa_30"); print(sum(r["ok"] for r in RES),"/",len(RES))
