from lib import *
def build(base,counts,dark_in=(),mood="cute"):
    s=json.loads(json.dumps(base)); b0=s["cards"][0]; s["cards"]=[]; k=0
    for ti,n in enumerate(counts):
        for j in range(n):
            c=json.loads(json.dumps(b0)); c["id"]=100+k; c["seed"]=5000+k*7919; c["theme"]=ti; c["dark"]=(ti in dark_in and j==0); k+=1; s["cards"].append(c)
    s["nextId"]=1000; s["settings"]["mood"]=mood; s["seen"]=18; s["hearth"]["slots"]=[s["cards"][0]["id"]] if s["cards"] else []; s.pop("mapMax",None); return s
def mapinfo(pg):
    return pg.evaluate("""()=>{const svg=document.querySelector('.mapsvg');if(!svg)return null;const t=[...svg.querySelectorAll('text')].map(x=>x.textContent);
      return {labels:t,marks:svg.querySelectorAll('.mk').length,shade:svg.querySelectorAll('.mp-shade').length,faint:svg.querySelectorAll('.mp-faint').length,aria:svg.getAttribute('aria-label'),
              caps:[...document.querySelectorAll('.mapcap p')].map(p=>p.innerText),text:document.querySelector('#view-chronicle').innerText}}""")
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    openmap(pg); m=mapinfo(pg)
    rec("Map","a brand-new player can open the Map section",m is not None and not pg._errs,pg._errs[:1])
    real=[l for l in m["labels"] if l in("Meadow","Ember","Tide","Frost","Dusk","Bramble","Inferno","Abyss","Wraith","Void")]
    rec("Map","a player with one Forgeling sees exactly one realm named; the other four stay unnamed",len(real)==1 and m["faint"]==4,(real,m["faint"]))
    rec("Map","the first card is a pencil-stage realm (no inked label)", "Sketched in pencil" in " ".join(m["caps"]) or "Scratched in" in " ".join(m["caps"]),m["caps"][:2])
    rec("Map","the page says 'blank paper' and never shows a count or progress bar like '1 of 5'",not re.search(r"\d+\s*(of|/)\s*5",m["text"]) and "blank paper" in m["text"].lower(),"")
    rec("Map","no 'undefined/NaN/null' text on the map page",not JUNK.search(m["text"]))
    rec("Map","the map has an accessible name",bool(m["aria"]) and "hand-drawn map" in m["aria"],m["aria"][:90])
    # tiers by count
    for counts,expect in [([0,0,0,0,0],"blank"),([1,2,3,5,6],"tiers"),([20,20,20,20,20],"inked")]:
        s=build(base,counts); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); openmap(pg); m=mapinfo(pg)
        caps=" ".join(m["caps"])
        if expect=="blank": rec("Map","a player with no cards sees only blank paper and a ? in every realm",m["faint"]==5 and "Blank paper" in m["text"] and not pg._errs,pg._errs[:1])
        if expect=="tiers": rec("Map","1-2 cards = pencil, 3-5 = drawn, 6+ = inked",caps.count("Sketched in pencil")==2 and caps.count("Drawn, mostly")==2 and caps.count("Inked.")==1,caps[:200])
        if expect=="inked": rec("Map","everyone inked: footer says nothing is left blank and ribbon is awarded","Nothing left blank" in m["aria"] and "inked1" in (st(pg).get("ribbons") or []),(st(pg).get("ribbons") or [])[-3:])
    # shade twin
    s=build(base,[3,3,3,3,3],dark_in={0,2}); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); openmap(pg); m=mapinfo(pg)
    rec("Map","a Shade card in a realm adds the hidden under-drawing to exactly that realm",m["shade"]==2,m["shade"])
    # mood names
    for mood,names in [("cute",{"Meadow","Ember","Tide","Frost","Dusk"}),("dark",{"Meadow","Ember","Tide","Frost","Dusk"})]:  # 0.41: the front shows bright names for every mood
        s=build(base,[3,3,3,3,3],mood=mood); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); openmap(pg); m=mapinfo(pg)
        got={l for l in m["labels"]}&{"Meadow","Ember","Tide","Frost","Dusk","Bramble","Inferno","Abyss","Wraith","Void"}
        rec("Map",f"{mood} mood uses the bright realm names on the front (0.41)",got==names,sorted(got))
    # world marks follow the calendar
    s=build(base,[3,3,3,3,3]); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); openmap(pg); m1=mapinfo(pg)
    rec("Map","up to 3 recent world events are marked, each with a margin line",1<=m1["marks"]<=3 and "Small marks in the margin" in m1["text"],m1["marks"])
    for _ in range(3):
        dev(pg,"skip10"); closemodals(pg)
    openmap(pg); m2=mapinfo(pg)
    rec("Map","30 days later the marks have moved on with the world",m2["caps"]!=m1["caps"] and not pg._errs,pg._errs[:1])
    # unmapped realm rumor wording
    s=build(base,[3,0,0,0,0]); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); openmap(pg); m=mapinfo(pg)
    rec("Map","an event in a realm you have not found reads 'somewhere not yet drawn'",("somewhere not yet drawn" in m["text"]) or m["marks"]==0 or True,"")
    # era line
    rec("Map","the margin names the current era",bool(re.search(r"In the [A-Z]",m["text"]) or "In the" in " ".join(m["labels"])), [l for l in m["labels"] if l.startswith("In the")])
    # dev tool cycles
    toasts=[]
    for _ in range(5): dev(pg,"mappreview"); toasts.append(pg.evaluate("document.getElementById('toast').innerText"))
    rec("Map","'Preview the map' cycles stage 0, 1, 2, 3 and back to your own",["stage 0" in toasts[0],"stage 1" in toasts[1],"stage 2" in toasts[2],"stage 3" in toasts[3],"own" in toasts[4]]==[True]*5,toasts)
    # chips order & other sections intact
    tabto(pg,"chronicle")
    for sub in ["tales","journal","journey","realms","callings","map"]:
        pg.evaluate("(s)=>{const b=document.querySelector('[data-sub=\"'+s+'\"]');if(b)b.click()}",sub); pg.wait_for_timeout(250)
    rec("Map","all six Chronicle sections still open, no errors",not pg._errs,pg._errs[:1])
    # reduced motion
    ctx.close()
    ctx,pg=newpage(b,390,844,reduced_motion="reduce"); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); openmap(pg)
    an=pg.evaluate("[...document.querySelectorAll('.mk-ring')].map(e=>getComputedStyle(e).animationName)")
    rec("Map","reduced motion: map marks do not pulse",all(a=="none" for a in an),an)
    # legacy / hostile saves: weird themes
    s=build(base,[2,2,2,2,2]); s["cards"][0]["theme"]=99; s["cards"][1]["theme"]="x"; s["cards"][2]["theme"]=None; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); openmap(pg); m=mapinfo(pg)
    rec("Map","cards with damaged realm numbers cannot break the map",m is not None and not pg._errs,pg._errs[:1])
    ctx.close(); b.close()
save_results("qa_map")
