from lib import *
# 0.26.0: the old tales. Each realm's four curios each remember one page; four pages make the tale whole.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
SRC=open(P.replace("file://","")).read() if P.startswith("file://") else open(S+"/work.html").read()
REALM={"acorn":0,"flower":0,"feather":0,"mushroom":0,"leaf":1,"spark":1,"bone":1,"crystal":1,"shell":2,"pebble":2,"rain":2,"coin":2,"snow":3,"moon":3,"bell":3,"glimmer":3,"key":4,"candle":4,"thread":4,"map":4}
NAMES=["Meadow","Ember","Tide","Frost","Dusk"]
def ready(pg,s): s.pop("disc",None); setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)  # each wander here stands for a new day (0.33: one new find a day)
def found(s,ids): s["curios"]={k:{"n":1,"cid":s["cards"][0]["id"],"at":s["date"]} for k in ids}; return s
def tales(pg): tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(400); return pg.inner_text("#view-chronicle")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,390,844); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # every curio belongs to exactly one tale page, four per realm, matching the realm it is found in
    pages=re.findall(r"\['(\w+)','[^']+'\]",SRC.split("const TALES=[")[1].split("const taleOf")[0])
    crealm=dict(re.findall(r"(\w+):(\d)",re.search(r"const CREALM=\{([^}]*)\}",SRC).group(1)))
    rec("Tales","each of the 20 curios remembers exactly one page, four per realm, from its own realm",len(pages)==20 and len(set(pages))==20 and all(int(crealm[k])==i//4 for i,k in enumerate(pages)),pages)
    # Chronicle with nothing found
    s=build(base,[1,1,1,1,1]); s["seen"]=99; ready(pg,found(s,[])); t=tales(pg)
    rec("Chronicle","the Tales tab opens with the old tales of all five realms","Old tales of the realms" in t and all(f"{n}: an untold tale" in t for n in NAMES) and t.count("0 of 4 pages")==5)
    rec("Chronicle","…and explains how to find pages","Each of its four curios remembers one page" in t and "Your first wander starts at the Hearth" in t)
    rec("Chronicle","your own Forgelings' tales still follow","Your Forgelings" in t)
    # some pages found, one tale whole
    ready(pg,found(s,["acorn","flower","feather","mushroom","shell","rain"])); t=tales(pg)
    rec("Chronicle","found pages show, in story order, and a whole tale shows its ending","The Slow Hill" in t and "Meadow. 4 of 4 pages. The tale is whole." in t and "It still grows at its own speed" in t and t.index("Before Meadow had a name")<t.index("The first spring"))
    rec("Chronicle","a missing page says another curio from that realm remembers it","Where the Tide Goes" in t and t.count("A page is missing. Another Tide curio remembers it.")==2 and "Tide. 2 of 4 pages" in t)
    rec("Chronicle","the whole tale wears a gold frame",pg.locator(".otale.whole").count()==1)
    rec("Chronicle","no broken text",not JUNK.search(t))
    # ribbon
    rb=[r["id"] for r in []]; s2=st(pg)
    rec("Ribbon","making a tale whole earns Tale Keeper","tale1" in (s2.get("ribbons") or []),s2.get("ribbons"))
    # wander home with a new curio: its page shows on the spot
    s3=found(st(pg),["shell","pebble","acorn"]); s3["hearth"]["slots"]=[s3["cards"][2]["id"]]; s3["wander"]={"id":s3["cards"][2]["id"],"start":0,"ready":1,"realm":2,"seed":777}
    ready(pg,s3); tabto(pg,"hearth"); pg.tap("#hCollect"); pg.wait_for_timeout(600); m=mt(pg); got=[k for k in st(pg)["curios"] if REALM[k]==2 and k not in("shell","pebble")]
    rec("Find","a new curio from wandering shows the page it remembers",len(got)==1 and "A page of an old Tide tale: Where the Tide Goes" in m and "Pages found: 3 of 4" in m and "Read the whole tale on the Map tab, under Tales" in m,m[:300])
    closemodals(pg)
    s4=st(pg); s4["wander"]={"id":s4["cards"][2]["id"],"start":0,"ready":1,"realm":2,"seed":991}; ready(pg,s4); tabto(pg,"hearth"); pg.tap("#hCollect"); pg.wait_for_timeout(600); m=mt(pg)
    rec("Find","the fourth page makes the tale whole, right there","The tale is whole." in m and "Tide still goes wherever you bring it" in m,m[:300])
    closemodals(pg)
    s5=st(pg); s5["wander"]={"id":s5["cards"][2]["id"],"start":0,"ready":1,"realm":2,"seed":55}; ready(pg,s5); tabto(pg,"hearth"); pg.tap("#hCollect"); pg.wait_for_timeout(600); m=mt(pg)
    rec("Find","a curio you already had shows no page again","A page of an old" not in m and "Another one for the pile" in m,m[:160])
    closemodals(pg)
    # realm page line
    openmap(pg); pg.evaluate("()=>{const r=document.querySelector('[data-realm=\"2\"]');r.dispatchEvent(new MouseEvent('click',{bubbles:true}))}"); pg.wait_for_timeout(400); txt=pg.inner_text("#view-chronicle")
    rec("Realm","the Tide realm page shows its old tale's progress","Old tale: Where the Tide Goes. The tale is whole." in txt,[l for l in txt.split("\n") if "Old tale" in l][:2])
    # lore off hides tales
    s6=st(pg); s6["settings"]["lore"]=False; ready(pg,s6); t=tales(pg)
    rec("Lore off","with lore off, the old tales are hidden and nothing else changes","Old tales of the realms" not in t and "Your Forgelings" not in t,t[:120])
    # damaged curio records still render
    s7=st(pg); s7["settings"]["lore"]=True; s7["curios"]={"shell":{"n":1},"nonsense":{"n":3},"pebble":"x"}; ready(pg,s7); t=tales(pg)
    rec("Damaged","damaged curio records are repaired and tales still render","Where the Tide Goes" in t and not pg._errs and not JUNK.search(t),pg._errs[:1])
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # layout and accessibility
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        for W,H in ((320,640),(430,932)):
            c2,p2=newpage(b,W,H,color_scheme=scheme); p2.goto(P); p2.wait_for_selector("#titleGo"); first_card(p2); closemodals(p2)
            s8=found(build(base,[1,1,1,1,1]),["acorn","flower","feather","mushroom","shell","rain","snow"]); s8["seen"]=99; setst(p2,s8); p2.reload(); p2.wait_for_timeout(800); closemodals(p2); tales(p2)
            rec("Layout",f"{scheme} {W}px: the tales fit without sideways scrolling",not p2.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"))
            if W==430:
                p2.wait_for_function("document.getAnimations().filter(a=>a.playState==='running'&&a.effect&&a.effect.getComputedTiming().iterations!==Infinity).length===0",timeout=5000)
                p2.evaluate(AXE); bad+=[f"{scheme}: {v}" for v in p2.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")]
            rec("All",f"{scheme} {W}px: no page errors",not p2._errs,p2._errs[:1]); c2.close()
    rec("A11y","axe: zero violations on the old tales, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_26"); print(sum(r["ok"] for r in RES),"/",len(RES))
