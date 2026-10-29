from lib import *
import time
# 0.42: the living map. Pixel landmarks for every place (front and back) with 44-point targets and a close-up;
# gentle realm weather and the walking wanderer on a canvas that only draws while the Map is open and holds still
# with Reduce Motion; the place found today glows. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
COUNT="(()=>{window.__clr=0;const o=CanvasRenderingContext2D.prototype.clearRect;CanvasRenderingContext2D.prototype.clearRect=function(...a){if(this.canvas&&this.canvas.classList&&this.canvas.classList.contains('mpfx'))window.__clr++;return o.apply(this,a)}})()"
FXPX="()=>{const c=document.querySelector('#view-chronicle .mpfx');if(!c||!c.width)return [-1,''];const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0,h=0;for(let i=3;i<d.length;i+=4)if(d[i]>0){n++;h=(h*31+d[i-3]+d[i-2]*7+d[i-1]*13+i)%1000000007}return [n,String(h)]}"
def load(pg,s): s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def setup(pg):
    pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg)
    for i,c in enumerate(s["cards"]): c["theme"]=i%5
    s["explore"]={"0":4,"1":2,"2":4,"3":1,"4":3}; s["seen"]=99; return s
def rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b,color_scheme="dark"); pg.add_init_script(COUNT); s=setup(pg); load(pg,s); openmap(pg); pg.wait_for_timeout(600)
    # ---------- landmarks ----------
    n=pg.locator(".mapsvg .mp-place").count(); fills=pg.evaluate("[...document.querySelectorAll('.mapsvg .mp-place path')].map(p=>p.getAttribute('fill'))")
    rec("Landmarks","every place found is a pixel landmark (19 here), drawn in colours, not lines",n==19 and len(fills)>=19*3,(n,len(fills)))
    rec("Landmarks","realms colour their landmarks (Ember's grove is warm, Meadow's is green)","#E2703A" in fills and "#5FB86A" in fills)
    sizes=pg.evaluate("[...document.querySelectorAll('.mapsvg .mpplace')].map(c=>Math.round(c.getBoundingClientRect().width))")
    rec("Targets","each landmark has its own 44-point target",len(sizes)==19 and min(sizes)>=44,(len(sizes),min(sizes) if sizes else 0))
    rec("Targets","the five realm targets are still there",pg.locator(".mphit").count()==5)
    box=pg.locator('.mpplace[data-place="3:1"]').bounding_box(); pg.mouse.click(box["x"]+box["width"]/2,box["y"]+box["height"]/2); pg.wait_for_timeout(500); m=mt(pg)
    rec("Close-up","tapping a landmark opens its close-up: the art, its name and its line","Bell Peak" in m and "Nobody speaks" in m and pg.locator("#modal svg.lmbig path").count()>=3,m[:120])
    rec("Close-up","…with a way to wander there and to open the realm's page",pg.locator('#modal [data-wto="3"]').count()==1 and pg.locator('#modal [data-realmopen="3"]').count()==1)
    bad+=["closeup: "+v for v in axe(pg)]
    pg.tap('#modal [data-realmopen="3"]'); pg.wait_for_timeout(500)
    rec("Close-up","Open Frost’s page shows Frost’s page on the map",not mt(pg) and "Frost" in pg.inner_text(".realmpage") and pg.get_attribute('.mphit[data-realm="3"]',"aria-pressed")=="true")
    box=pg.locator('.mpplace[data-place="1:0"]').bounding_box(); pg.mouse.click(box["x"]+box["width"]/2,box["y"]+box["height"]/2); pg.wait_for_timeout(500)
    pg.tap('#modal [data-wto="1"]'); pg.wait_for_timeout(600); s2=st(pg)
    rec("Close-up","Send … to wander here starts a wander to that realm",s2.get("wander") and s2["wander"]["realm"]==1 and not mt(pg),s2.get("wander"))
    pg.focus('.mpplace[data-place="0:0"]'); pg.keyboard.press("Enter"); pg.wait_for_timeout(400)
    rec("Keyboard","a landmark opens from the keyboard too","The Slow Hill" in mt(pg)); closemodals(pg)
    # ---------- the living canvas ----------
    openmap(pg); pg.wait_for_timeout(1200)
    a=pg.evaluate(FXPX); pg.wait_for_timeout(700); a2=pg.evaluate(FXPX)
    rec("Living","the map canvas draws weather and the wanderer, and it moves",a[0]>40 and a[1]!=a2[1],(a[0],a2[0]))
    pg.evaluate("()=>window.__clr=0"); pg.wait_for_timeout(1000); on=pg.evaluate("()=>window.__clr")
    tabto(pg,"settings",fold=True); pg.wait_for_timeout(700); pg.evaluate("()=>window.__clr=0"); pg.wait_for_timeout(1500); off=pg.evaluate("()=>window.__clr")
    rec("Battery","it draws about 12 times a second on the Map and not at all on other tabs",8<=on<=16 and off==0,(on,off))
    openmap(pg); pg.wait_for_timeout(300); pg.evaluate("()=>window.__clr=0"); pg.wait_for_timeout(600)
    rec("Battery","…and wakes at once when the Map opens again",pg.evaluate("()=>window.__clr")>=4)
    # the wanderer: drawn where the wander's real time puts it
    s=st(pg); now=int(time.time()*1000); c0=s["cards"][0]; c0["theme"]=0
    s["wander"]={"id":c0["id"],"start":now-3600*1000,"ready":now+3*3600*1000,"seed":5,"notified":False,"realm":1}; load(pg,s); openmap(pg); pg.wait_for_timeout(900)
    w1=pg.evaluate(FXPX)[0]; s=st(pg); s["wander"]=None; load(pg,s); openmap(pg); pg.wait_for_timeout(900); w0=pg.evaluate(FXPX)[0]
    rec("Wanderer","a Forgeling out wandering walks the trail on the map (more drawn than with nobody out)",w1>w0+60,(w1,w0))
    # the place found today glows
    s=st(pg); s["lastPlace"]={"ti":3,"k":1,"d":s["date"]}; load(pg,s); openmap(pg); pg.wait_for_timeout(900)
    rec("Glow","the place found today keeps a glow, and the save keeps it",st(pg).get("lastPlace",{}).get("ti")==3)
    for junk in ({"ti":12,"k":1,"d":"x"},"x",{"ti":3,"k":9,"d":"2026-01-01"}):
        s=st(pg); s["lastPlace"]=junk; load(pg,s)
        rec("Damaged",f"a damaged last place ({str(junk)[:20]}) is dropped, not a crash","lastPlace" not in st(pg) and not pg._errs,pg._errs[:1])
    pg.wait_for_timeout(300); bad+=["map dark: "+v for v in axe(pg)]
    # a wander that finds a place records it for the glow
    s=st(pg); s["wander"]={"id":s["cards"][0]["id"],"start":now-4*3600*1000,"ready":now-1000,"seed":9,"notified":True,"realm":3}; s.pop("disc",None); load(pg,s)
    tabto(pg,"hearth"); pg.tap("#hCollect"); pg.wait_for_timeout(700); lp=st(pg).get("lastPlace")
    rec("Glow","finding a new place on a wander marks it to glow today",lp and lp["ti"]==3 and lp["d"]==st(pg)["date"],lp); closemodals(pg)
    # ---------- the back of the map ----------
    dev(pg,"shade"); closemodals(pg); pg.wait_for_timeout(1000)
    nb=pg.locator(".mapwrap.mback .mp-place").count(); fb=pg.evaluate("[...document.querySelectorAll('.mapsvg .mp-place path')].map(p=>p.getAttribute('fill'))")
    rec("Back","the back of the map has pixel landmarks too, in Shade colours",nb>=4 and "#0B0816" in fb,(nb,))
    px=pg.evaluate(FXPX)[0]; rec("Back","Shade realms drift glowing motes",px>10,px)
    box=pg.locator('.mapwrap.mback .mpplace').first.bounding_box(); pg.mouse.click(box["x"]+box["width"]/2,box["y"]+box["height"]/2); pg.wait_for_timeout(500)
    rec("Back","a Shade landmark's close-up says it is on the other side","the other side" in mt(pg),mt(pg)[:80]); bad+=["back closeup: "+v for v in axe(pg)]; closemodals(pg)
    pg.wait_for_timeout(300); bad+=["back: "+v for v in axe(pg)]
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # ---------- reduced motion: one still frame ----------
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.add_init_script(COUNT); s=setup(pg); now=int(time.time()*1000); c0=s["cards"][0]; c0["theme"]=0
    s["wander"]={"id":c0["id"],"start":now-3600*1000,"ready":now+3*3600*1000,"seed":5,"notified":False,"realm":1}; load(pg,s); openmap(pg); pg.wait_for_timeout(1500)
    a=pg.evaluate(FXPX); pg.wait_for_timeout(1200); a2=pg.evaluate(FXPX); pg.evaluate("()=>window.__clr=0"); pg.wait_for_timeout(1500)
    rec("Motion","with Reduce Motion the map shows the wanderer in one still frame, with no weather",a[0]>60 and a[1]==a2[1] and pg.evaluate("()=>window.__clr")==0,(a[0],pg.evaluate("()=>window.__clr")))
    # light theme, plain sky, 320 px
    ctx.close(); ctx,pg=newpage(b,320,640,color_scheme="light"); s=setup(pg); s["settings"]["sky"]="plain"; s["settings"]["theme"]="light"; load(pg,s); openmap(pg); pg.wait_for_timeout(600)
    sizes=pg.evaluate("[...document.querySelectorAll('.mapsvg .mpplace')].map(c=>Math.round(c.getBoundingClientRect().width))")
    rec("Targets","at 320 px every landmark target is still 44 points",min(sizes)>=44,min(sizes))
    w=pg.evaluate("document.documentElement.scrollWidth"); rec("Layout","no sideways scroll at 320 px",w<=320,w)
    bad+=["light 320: "+v for v in axe(pg)]
    rec("A11y","zero accessibility violations on the map, both sides, and the close-ups",not bad,bad[:4])
    rec("All","no page errors (light, 320 px)",not pg._errs,pg._errs[:2]); ctx.close()
save_results("qa_42")
