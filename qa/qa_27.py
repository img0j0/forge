from lib import *
# 0.27.0: places on the map. First place with your first Forgeling in a realm; each wander there uncovers the next.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
def ready(pg,s): s.pop("disc",None); setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)  # each wander here stands for a new day (0.33: one new find a day)
def places(pg): openmap(pg); return pg.locator(".mapsvg .mp-place").count()
def collect(pg,s,cid,realm,seed):
    s["hearth"]["slots"]=[cid]; s["wander"]={"id":cid,"start":0,"ready":1,"realm":realm,"seed":seed}; ready(pg,s); tabto(pg,"hearth"); pg.tap("#hCollect"); pg.wait_for_timeout(600); m=mt(pg); closemodals(pg); return m
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,390,844); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    rec("Start","a brand-new player's first Forgeling puts one place on the map",places(pg)==1,places(pg))
    s=build(base,[1,1,0,1,0]); s["seen"]=99; s["explore"]={}; ready(pg,s)
    rec("Start","each realm you know shows its first place",places(pg)==3,places(pg))
    rec("Notes","the notes under the map count each realm's places",pg.inner_text(".mapcap").count("One place drawn in so far.")==3 and not re.search(r"\d+\s*(of|/)\s*5",pg.inner_text("#view-chronicle")))
    # wander to Meadow
    m=collect(pg,st(pg),s["cards"][0]["id"],0,11)
    rec("Wander","a wander to Meadow uncovers its next place, Birdwait Oak","A new place on your map: Birdwait Oak" in m and "Another place is drawn on your map of Meadow." in m and "See it on the Map tab" in m,m[:240])
    rec("Wander","…it is saved, and the map draws it with a trail",st(pg)["explore"]=={"0":1} and places(pg)==4 and pg.locator('.mapsvg path[stroke-dasharray="1.5 3"]').count()==1,st(pg)["explore"])
    # wander anywhere
    m=collect(pg,st(pg),s["cards"][1]["id"],-1,5); ex=st(pg)["explore"]
    rec("Wander","a wander anywhere uncovers a place in one of your realms",("A new place on your map" in m) and sum(ex.values())==2 and set(ex)<= {"0","1","3"},ex)
    # chart Meadow fully
    s2=st(pg); s2["explore"]={"0":3}; ready(pg,s2); m=collect(pg,st(pg),s["cards"][0]["id"],0,21)
    rec("Charted","the fifth place charts the realm fully, and says so","A new place on your map: Fernlow" in m and "That is the last place in Meadow. The realm is fully charted." in m,m[:240])
    openmap(pg)
    rec("Charted","a fully charted realm wears a gold mark under its name",pg.locator(".mapsvg .mp-gold").count()==2 and "Fully charted." in pg.inner_text(".mapcap"))
    rec("Charted","…and earns the Cartographer ribbon","chart1" in (st(pg).get("ribbons") or []),st(pg).get("ribbons"))
    m=collect(pg,st(pg),s["cards"][0]["id"],0,33)
    rec("Charted","wandering a fully charted realm finds no new place",("A new place" not in m) and st(pg)["explore"]["0"]==4,m[:120])
    # realm page lists places
    openmap(pg); pg.evaluate("()=>{const r=document.querySelector('[data-realm=\"1\"]');r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); pg.wait_for_timeout(400); rp=pg.inner_text(".realmpage")
    rec("Realm page","a realm page lists the places found, with no counts, and says there is more to find","Places on the map" in rp and "Leaprock." in rp and "There is more to find here." in rp and not re.search(r"\d+\s*(of|/)\s*5",rp) and not JUNK.search(rp),rp[:240])
    openmap(pg); pg.evaluate("()=>{const r=document.querySelector('[data-realm=\"0\"]');r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); pg.wait_for_timeout(400); rp=pg.inner_text(".realmpage")
    rec("Realm page","a fully charted realm says so","Places on the map. Fully charted." in rp and "There is more to find here." not in rp and "The Slow Hill." in rp and "Fernlow's Seat." in rp)
    # an unknown realm stays blank
    rec("Unknown","realms you have no Forgeling from show no places",places(pg)==3+4)
    # damaged
    for bad in ("x",None,[1],{"0":"no","1":-3,"2":99,"7":2},{"3":2.6}):
        s3=st(pg); s3["explore"]=bad; ready(pg,s3); ex=st(pg)["explore"]
        rec("Damaged",f"damaged exploration records ({bad!r}) are repaired",isinstance(ex,dict) and all(k in "01234" and isinstance(v,int) and 1<=v<=4 for k,v in ex.items()) and not pg._errs,(ex,pg._errs[:1]))
    s4=st(pg); s4.pop("explore",None); ready(pg,s4)
    rec("Damaged","an older save without exploration picks it up",st(pg)["explore"]=={} and places(pg)==3)
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # every realm can fit all five places, inside its outline
    c2,p2=newpage(b,390,844); p2.goto(P); p2.wait_for_selector("#titleGo"); first_card(p2); closemodals(p2)
    s5=build(base,[1,1,1,1,1]); s5["seen"]=99; s5["explore"]={str(i):4 for i in range(5)}; setst(p2,s5); p2.reload(); p2.wait_for_timeout(800); closemodals(p2); openmap(p2)
    info=p2.evaluate("""()=>{const out=[];const pl=[...document.querySelectorAll('.mapsvg .mp-place')];const hits=[...document.querySelectorAll('.mapsvg .mphit')];
      for(const e of pl){const r=e.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;const inside=hits.filter(h=>h.isPointInFill&&h.isPointInFill(new DOMPoint(...(()=>{const m=h.getScreenCTM().inverse();const q=new DOMPoint(x,y).matrixTransform(m);return [q.x,q.y]})())));out.push(inside.map(h=>+h.dataset.realm));}
      const labels=[...document.querySelectorAll('.mapsvg text')].map(t=>t.getBoundingClientRect());const over=pl.filter(e=>{const r=e.getBoundingClientRect();return labels.some(l=>!(r.right<l.left||r.left>l.right||r.bottom<l.top||r.top>l.bottom))}).length;
      return {n:pl.length,realms:out,over}}""")
    per=[sum(1 for r in info["realms"] if r==[ti]) for ti in range(5)]
    rec("Layout","all 25 places fit, five inside each realm's outline",info["n"]==25 and per==[5,5,5,5,5],(info["n"],per))
    rec("Layout","no place sits on a realm name or the map's lettering",info["over"]==0,info["over"])
    c2.close()
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        for W,H in ((320,640),(430,932)):
            c3,p3=newpage(b,W,H,color_scheme=scheme); p3.goto(P); p3.wait_for_selector("#titleGo"); first_card(p3); closemodals(p3)
            setst(p3,s5); p3.reload(); p3.wait_for_timeout(800); closemodals(p3); openmap(p3)
            p3.evaluate("()=>{const r=document.querySelector('[data-realm=\"2\"]');r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); p3.wait_for_timeout(400)
            rec("Layout",f"{scheme} {W}px: the map and a realm page fit",not p3.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"))
            if W==430:
                p3.wait_for_function("document.getAnimations().filter(a=>a.playState==='running'&&a.effect&&a.effect.getComputedTiming().iterations!==Infinity).length===0",timeout=5000)
                p3.evaluate(AXE); bad+=[f"{scheme}: {v}" for v in p3.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")]
            rec("All",f"{scheme} {W}px: no page errors",not p3._errs,p3._errs[:1]); c3.close()
    rec("A11y","axe: zero violations on the map with places and a realm page, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_27"); print(sum(r["ok"] for r in RES),"/",len(RES))
