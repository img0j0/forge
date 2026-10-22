from lib import *
# 0.33.0: pacing for the long run. One new find a day; the map inks more slowly; nothing ever goes backwards.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
def load(pg,s):
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def tiers(pg):
    openmap(pg); t=pg.inner_text(".mapcap"); out={}
    for nm in ["Meadow","Ember","Tide","Frost","Dusk","Bramble","Inferno","Abyss","Wraith","Void"]:
        m=re.search(nm+r"\. (Sketched|Scratched|Drawn|Inked)",t)
        if m: out[nm]={"Sketched":1,"Scratched":1,"Drawn":2,"Inked":3}[m.group(1)]
    return out
def collect(pg,s,cid,realm,seed):
    s["hearth"]["slots"]=[cid]; s["wander"]={"id":cid,"start":0,"ready":1,"realm":realm,"seed":seed}; load(pg,s); tabto(pg,"hearth")
    pg.tap("#hCollect"); pg.wait_for_timeout(900); m=mt(pg); closemodals(pg); return m
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # ---------- the map, for a new player ----------
    for n,want in [(1,1),(3,1),(4,2),(6,2),(9,2),(10,3)]:
        s=build(base,[n,0,0,0,0],(),"cute"); s["mapMax"]=[0,0,0,0,0]; s["seen"]=99; load(pg,s)
        rec("Map",f"a new player with {n} Meadow Forgelings sees stage {want}",tiers(pg).get("Meadow")==want,tiers(pg))
    # grandfathered: an older save keeps the old stages
    s=build(base,[6,3,0,0,0],(),"cute"); s["seen"]=99; load(pg,s)
    rec("Map","an older save keeps what it had: 6 Forgelings stay inked, 3 stay drawn",tiers(pg).get("Meadow")==3 and tiers(pg).get("Ember")==2 and st(pg).get("mapMax",[None])[:2]==[3,2],(tiers(pg),st(pg).get("mapMax")))
    # never backwards
    s=st(pg); s["mapMax"]=[3,2,0,0,0]; s["cards"]=[c for c in s["cards"] if c["theme"]!=0][:3]+[c for c in s["cards"] if c["theme"]==0][:1]; load(pg,s)
    rec("Map","a realm never fades: once inked, it stays inked",tiers(pg).get("Meadow")==3,tiers(pg))
    rec("Map","still no counts on the Map",not re.search(r"\d+ of \d+",pg.evaluate("document.querySelector('.mapsvg').textContent")))
    # ---------- one new find a day ----------
    s=build(base,[4,0,0,0,0],(),"cute"); s["seen"]=99; s["curios"]={}; s["explore"]={}; s.pop("disc",None); cid=s["cards"][0]["id"]
    m1=collect(pg,s,cid,0,101); s1=st(pg)
    rec("Daily","the day's first wander brings a new curio and a new place","A new curio for your shelf" in m1 and "A new place on your map" in m1 and len(s1["curios"])==1 and s1["explore"].get("0")==1 and s1["disc"]==s1["date"],m1[:160])
    b0=[c for c in s1["cards"] if c["id"]==cid][0]["bond"]
    tabto(pg,"hearth"); pg.evaluate("()=>{const b=document.getElementById('hWander');b&&b.click()}"); pg.wait_for_timeout(400); sh=mt(pg); closemodals(pg)
    rec("Daily","the destination sheet says today's new find is already home","Today’s new find is already home" in sh,sh[:200])
    m2=collect(pg,st(pg),cid,0,202); s2=st(pg)
    rec("Daily","a second wander the same day brings a spare, not a new curio or place","Another one for the pile" in m2 and "A new place" not in m2 and len(s2["curios"])==1 and list(s2["curios"].values())[0]["n"]==2 and s2["explore"].get("0")==1,m2[:200])
    rec("Daily","…with a quiet-path note, +1 bond, and a promise for tomorrow","A quiet path today" in m2 and "Tomorrow’s first wander will find something new" in m2 and [c for c in s2["cards"] if c["id"]==cid][0]["bond"]==b0+1,m2[-300:])
    m3=collect(pg,st(pg),cid,-1,303)
    rec("Daily","a wander to 'anywhere' the same day is quiet too","Another one for the pile" in m3 and "A new place" not in m3)
    dev(pg,"next"); closemodals(pg)
    m4=collect(pg,st(pg),cid,0,404); s4=st(pg)
    rec("Daily","the next day's first wander finds something new again","A new curio for your shelf" in m4 and len(s4["curios"])==2 and s4["explore"].get("0")==2,m4[:160])
    # a request still completes on a quiet day
    s5=st(pg); s5["request"]={"cid":cid,"realm":0,"made":s5["date"]}; load(pg,s5)
    m5=collect(pg,st(pg),cid,0,505)
    rec("Daily","a Forgeling's request still completes on a quiet day","request is done" in m5 and st(pg)["request"] is None,m5[:300])
    # nothing left to find: no promise
    s6=st(pg); s6["curios"]={x:{"n":1,"cid":cid,"at":s6["date"]} for x in ["acorn","flower","feather","mushroom","leaf","spark","bone","crystal","shell","pebble","rain","coin","snow","moon","bell","glimmer","key","candle","thread","map"]}
    s6["explore"]={"0":4}; s6["disc"]=s6["date"]; load(pg,s6); m6=collect(pg,st(pg),cid,0,606)
    rec("Daily","with everything found, the quiet note makes no promise","A quiet path today" in m6 and "Tomorrow" not in m6,m6[-200:])
    # damaged saves
    s7=st(pg); s7["mapMax"]="lots"; s7["disc"]=7; load(pg,s7); s7=st(pg)
    rec("Damaged","broken pacing data is repaired",isinstance(s7.get("mapMax"),list) and len(s7["mapMax"])==5 and "disc" not in s7 or isinstance(s7.get("disc"),str),(s7.get("mapMax"),s7.get("disc")))
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_33"); print(sum(r["ok"] for r in RES),"/",len(RES))
