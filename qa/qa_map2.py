from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # only Meadow discovered -> every margin line is either Meadow or 'somewhere not yet drawn'
    for day_skip in range(0,4):
        s=build(base,[3,0,0,0,0]); setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
        for _ in range(day_skip*3): dev(pg,"skip10"); closemodals(pg)
        openmap(pg); m=mapinfo(pg)
        lines=[c for c in m["caps"] if re.match(r"(Today|Yesterday|\d+ days ago),",c)]
        ok=all(re.match(r"(Today|Yesterday|\d+ days ago), (Meadow|somewhere not yet drawn)\.",l) for l in lines)
        undrawn=sum("somewhere not yet drawn" in l for l in lines)
        rec("Map",f"skip +{day_skip*30}d: margin lines name only drawn realms ({len(lines)} lines, {undrawn} from undrawn realms)",ok and len(lines)>0,lines[:3])
    # no-drawn-realm leak: realm names of undrawn realms never appear in margin line prefixes
    s=build(base,[0,0,0,0,0]); setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg); openmap(pg); m=mapinfo(pg)
    lines=[c for c in m["caps"] if re.match(r"(Today|Yesterday|\d+ days ago),",c)]
    rec("Map","a player with no cards: every margin line says 'somewhere not yet drawn'",len(lines)>0 and all("somewhere not yet drawn" in l for l in lines),lines[:2])
    ctx.close()
    # control: normal motion pulses, reduced motion does not
    ctx,pg=newpage(b,390,844); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); openmap(pg)
    an=pg.evaluate("[...document.querySelectorAll('.mk-ring')].map(e=>getComputedStyle(e).animationName)")
    rec("Map","control: with normal motion settings the marks DO pulse",len(an)>0 and all(a=="mkp" for a in an),an)
    ctx.close(); b.close()
