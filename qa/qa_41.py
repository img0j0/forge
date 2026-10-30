from lib import *
# 0.41: the other side. The Crossing Lantern (visible from the start, first once a realm is charted), turning the map
# over, Shade realms lit realm by realm, Shade wanders/curios/places/tales, wards, Home on the wander sheet, bright
# names on the front for everyone, the compass, gifts staying front-side, saves surviving a reload. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def settle(pg): pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
def load(pg,s): s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def days(s,n):
    d=datetime.date.fromisoformat(s["startDate"])
    have={h["date"] for h in s["history"]}; k=1
    while n>0:
        x=(d-datetime.timedelta(days=k)).isoformat(); k+=1
        if x in have: continue
        s["history"].append({"date":x,"status":"done","v":0}); n-=1
def tapm(pg,sel): pg.locator(sel).scroll_into_view_if_needed(); pg.tap(sel); pg.wait_for_timeout(450)
SHADE5=["thorn","seed","nest","rosehip"]
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    # ---------- a new player: the lantern is listed, nothing Shade shows ----------
    s=st(pg); s["settings"]["mood"]="dark"
    for i,c in enumerate(s["cards"]): c["theme"]=[0,0,1,2,3,0][i%6]
    cs=s["cards"]; cs[1]["dark"]=True; s["hearth"]["slots"]=[cs[1]["id"],cs[0]["id"]]; s["hearth"]["sel"]=0
    load(pg,s); tabto(pg,"hearth"); pg.tap("#hForge"); pg.wait_for_timeout(500); m=mt(pg)
    rec("Lantern","a new player sees the Crossing Lantern in the Forge, saying it needs a charted realm","Crossing Lantern" in m and "a fully charted realm" in m and "no realm fully charted yet" in m,m[-400:])
    rec("Hidden","…but no wards before the lantern","Ward of" not in m)
    rec("Forge","eleven pieces are listed (the lantern joins the ten)","0 of 11 pieces made" in m and m.count("Needs ")==11,m[:120])
    closemodals(pg)
    rec("Hidden","no Turn the map over control before the lantern",(openmap(pg) or True) and pg.locator("#mapTurn").count()==0)
    labels=pg.evaluate("[...document.querySelectorAll('.mapsvg text')].map(t=>t.textContent)")
    rec("Names","a dark-mood player sees the bright names on the front of the map","Meadow" in labels and "Bramble" not in labels,labels)
    tabto(pg,"hearth"); shelf=pg.inner_text("#hShelf")
    rec("Hidden","the curio shelf counts the 20 front curios only","of 20" in shelf and pg.locator("#view-hearth .sside").count()==0,shelf)
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(300)
    rec("Hidden","no Shade tales before the lantern","Tales from the other side" not in pg.inner_text("#view-chronicle"))
    pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(300)
    rec("Hidden","the two Shade ribbons stay hidden","Lantern Light" not in pg.inner_text("#view-chronicle") and "Both Sides" not in pg.inner_text("#view-chronicle"))
    # ---------- Meadow charted: the lantern comes first and the panel says so ----------
    s=st(pg); s["explore"]={"0":4}; days(s,8)
    for cid,n in [("acorn",2),("leaf",2),("snow",3),("flower",1)]: s["curios"][cid]={"n":n,"cid":0,"at":s["date"]}
    load(pg,s); tabto(pg,"hearth"); t=pg.inner_text("#hLantern")
    rec("Lantern","a charted realm puts a line at the Hearth","A charted realm is waiting for a lantern" in t and "You have what it needs" in t,t)
    pg.tap("#hForge"); pg.wait_for_timeout(500)
    first=pg.evaluate("document.querySelector('#modal .forgel li b').textContent")
    rec("Lantern","…and lists the lantern first",first=="Crossing Lantern",first)
    e0=pg.evaluate("+document.getElementById('hEmbers').textContent.split(' ')[0]") if pg.locator("#hEmbers").count() else 0
    tapm(pg,"#modal [data-fmake='xlantern']"); m=mt(pg)
    s=st(pg)
    rec("Lantern","making it takes one spare from each of three realms and 6 embers",s["curios"]["acorn"]["n"]==1 and s["curios"]["leaf"]["n"]==1 and s["curios"]["snow"]["n"]==2 and s["forge"]["spent"]==6 and "xlantern" in s["forge"]["made"],[s["curios"][k]["n"] for k in ("acorn","leaf","snow")])
    rec("Lantern","the finished lantern is signed and offers to turn the map over","Forged by" in m and pg.locator("#modal #fgTurn").count()==1,m[:200])
    bad+=["made: "+v for v in axe(pg)]
    tapm(pg,"#modal #fgTurn"); pg.wait_for_timeout(400)
    rec("Map","Turn the map over opens the back of the map",pg.locator(".mapwrap.mback").count()==1 and pg.locator("#mapTurn").inner_text()=="Turn back to the front")
    labels=pg.evaluate("[...document.querySelectorAll('.mapsvg text')].map(t=>t.textContent)")
    rec("Map","only Meadow's twin, Bramble, is lit; the others stay dark","Bramble" in labels and not any(x in labels for x in ("Inferno","Abyss","Wraith","Void")) and labels.count("?")==4,labels)
    txt=pg.inner_text("#view-chronicle")
    rec("Map","the back has no counts, only gentle words",not re.search(r"\b\d+ of \d+\b",pg.inner_text(".mapcap")) and "Lit by your lantern" in txt,pg.inner_text(".mapcap")[:200])
    pg.evaluate("()=>document.querySelector('.mphit[data-realm=\"5\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); pg.wait_for_timeout(400)
    rp=pg.inner_text(".realmpage")
    rec("Map","tapping Bramble opens its page: its place, its tale and a wander button","The other side of Meadow" in rp and "Thornkeep Gate" in rp and "Shade tale" in rp and pg.locator(".realmpage [data-wto='5']").count()==1,rp[:200])
    pg.evaluate("()=>document.querySelector('.mphit[data-realm=\"6\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); pg.wait_for_timeout(400)
    rec("Map","an unlit Shade realm says how to light it","Chart Ember fully on the front" in pg.inner_text(".realmpage"))
    settle(pg); bad+=["back: "+v for v in axe(pg)]
    w=pg.evaluate("document.documentElement.scrollWidth"); rec("Layout","the back fits the phone with no sideways scroll",w<=390,w)
    tapm(pg,"#mapTurn"); rec("Map","turning back shows the front again",pg.locator(".mapwrap.mback").count()==0 and "Its twin is lit on the back." in pg.inner_text(".mapcap"))
    # ---------- crossing over: Home, a Shade find, a place on the back ----------
    tabto(pg,"hearth"); pg.tap("#hWander"); pg.wait_for_timeout(500); m=mt(pg)
    rec("Wander","the wander sheet lists Bramble on the other side","On the other side, by lantern" in m and pg.locator("#modal [data-wgo='5']").count()==1 and pg.locator("#modal [data-wgo='6']").count()==0,m[-300:])
    rec("Wander","…marked Home for a Shade Forgeling born in Meadow","Bramble · Home" in m)
    bad+=["wsheet: "+v for v in axe(pg)]
    tapm(pg,"#modal [data-wgo='5']"); s=st(pg)
    rec("Wander","the wanderer crosses over to Bramble",s["wander"]["realm"]==5 and "crosses over to Bramble" in pg.inner_text("#view-hearth"),pg.inner_text("#hmsg") if pg.locator("#hmsg").count() else "")
    pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
    rec("Save","a wander to a Shade realm survives a reload",st(pg)["wander"]["realm"]==5)
    s=st(pg); s.pop("disc",None); load(pg,s); dev(pg,"wander"); closemodals(pg); tabto(pg,"hearth"); pg.tap("#hCollect"); pg.wait_for_timeout(700); m=mt(pg); s=st(pg)
    got=[k for k in SHADE5 if k in s["curios"]]
    rec("Find","the first wander of the day brings a Bramble curio home",len(got)==1 and "Back from Bramble" in m,got)
    rec("Find","…draws a second place on the back of the map","A new place on the back of your map: The Sleeping Bed" in m and s["explore"].get("5")==1,s.get("explore"))
    rec("Find","…and shows its page of the Shade tale","A page of an old Bramble tale: The Keepers of the Edge" in m)
    rec("Find","the find counts against all forty curios now","of 40" in m,re.findall(r"\d+ of \d+",m))
    closemodals(pg)
    pg.reload(); pg.wait_for_timeout(900); closemodals(pg); s=st(pg)
    rec("Save","a Shade curio and a Shade place survive a reload",got and got[0] in s["curios"] and s["explore"].get("5")==1)
    # second wander the same day: a quiet path with a Bramble spare
    tabto(pg,"hearth"); pg.tap("#hWander"); pg.wait_for_timeout(400); tapm(pg,"#modal [data-wgo='5']"); dev(pg,"wander"); closemodals(pg); tabto(pg,"hearth"); pg.tap("#hCollect"); pg.wait_for_timeout(700); m=mt(pg); s=st(pg)
    rec("Find","a later wander that day is a quiet path with a Bramble spare","A quiet path today" in m and sum(s["curios"][k]["n"] for k in SHADE5 if k in s["curios"])==2,m[:160])
    closemodals(pg)
    # ---------- shelf, tales, ribbons ----------
    hsheet(pg,"shelf"); shelf=mt(pg)
    rec("Shelf","the shelf turns over too: ten planks, the other side labelled, counting 40","The other side" in shelf and "of 40" in shelf and pg.locator("#modal .srow").count()==10 and "Across from Ember, not crossed yet" in shelf,shelf[:200])
    pg.tap(f"#modal [data-cur='{got[0]}']"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Shelf","a Shade curio opens with its own art and tale page",pg.locator("#modal .cbig img").count()==1 and "The Keepers of the Edge" in m,m[:120]); closemodals(pg)
    other=[k for k in ("cinder","obsidian") if k not in st(pg)["curios"]][0]
    hsheet(pg,"shelf"); pg.tap(f"#modal [data-cur='{other}']"); pg.wait_for_timeout(400)
    rec("Shelf","an unfound Inferno curio says where it is and how to get there","across from Ember" in mt(pg) and "Chart Ember fully" in mt(pg),mt(pg)[:200]); closemodals(pg)
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(300); pg.evaluate("document.querySelector('[data-tside=\"1\"]').click()"); pg.wait_for_timeout(300); t=pg.inner_text("#view-chronicle")
    rec("Tales","Tales shows the other side: Bramble's tale begun, the rest untold","Other side" in t and "The Keepers of the Edge" in t and t.count("an untold tale")>=4,(t.find("Tales from"),t[:200]))
    settle(pg); bad+=["tales: "+v for v in axe(pg)]
    pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(300); t=pg.inner_text("#view-chronicle")
    rec("Ribbons","with the lantern, Lantern Light is earned and Both Sides is listed","Lantern Light" in t and "Both Sides" in t and "cross1" in (st(pg).get("ribbons") or []))
    # ---------- a ward ----------
    s=st(pg); s["curios"]["nest"]={"n":3,"cid":0,"at":s["date"]}; days(s,4); load(pg,s); tabto(pg,"hearth"); pg.tap("#hForge"); pg.wait_for_timeout(500); m=mt(pg)
    rec("Ward","the Forge now lists five wards, made from Shade spares","Ward of Bramble" in m and "Ward of Void" in m and "Needs 2 Bramble spares" in m and "of 16 pieces made" in m,m[:120])
    tapm(pg,"#modal [data-fmake='ward0']"); m=mt(pg)
    rec("Ward","the ward is forged and can be worn by whoever helped",pg.locator("#modal [data-equip='ward0']").count()==1,m[:160])
    tapm(pg,"#modal [data-equip='ward0']"); s=st(pg); wc=[c for c in s["cards"] if c.get("keep")=="ward0"]
    rec("Ward","the Forgeling wears the ward",len(wc)==1)
    pg.reload(); pg.wait_for_timeout(900); closemodals(pg); s=st(pg)
    rec("Save","the ward is still worn after a reload",any(c.get("keep")=="ward0" for c in s["cards"]))
    # the ward shows on the card: the pendant pixels and the badge
    tabto(pg,"binder"); wid=[c for c in s["cards"] if c.get("keep")=="ward0"][0]["id"]
    pg.evaluate(f"()=>{{const b=document.querySelector('#view-binder [data-insp=\"{wid}\"]')||[...document.querySelectorAll('#view-binder .card')].find(x=>x.closest('[data-insp=\"{wid}\"]'));if(b)b.click();}}"); pg.wait_for_timeout(700)
    red=pg.evaluate("()=>{const c=document.querySelector('#stage canvas.pcv');if(!c)return -1;const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=0;i<d.length;i+=4)if(Math.abs(d[i]-255)<3&&Math.abs(d[i+1]-77)<3&&Math.abs(d[i+2]-94)<3)n++;return n}")
    rec("Ward","the card shows the ward pendant in Bramble red and a badge",red>0 and pg.locator("#stage .chb, #modal .chb, .ov .chb").count()>=1,red)
    closemodals(pg)
    # ---------- compass points across; gifts stay front-side ----------
    s=st(pg)
    for c in [x["id"] for x in [{"id":k} for k in ["acorn","flower","feather","mushroom","leaf","spark","bone","crystal","shell","pebble","rain","coin","snow","moon","bell","glimmer","key","candle","thread","map"]]]: s["curios"].setdefault(c,{"n":1,"cid":0,"at":s["date"]})
    s["explore"].update({"1":4,"2":4,"3":4,"4":4}); s["cards"].append(dict(s["cards"][0],id=s["nextId"],theme=4)); s["nextId"]+=1
    s["forge"]["made"].append("compass"); s["forge"]["comp"]=""
    for k in ("cinder","obsidian","ring","ash","bottle","pearl","anchor","seaglass","mitten","stillstone","icicle","snowglass","letter","inkpot","locket","mirror"): s["curios"][k]={"n":1,"cid":0,"at":s["date"]}
    for k in ("5","6","7","8","9"): s["explore"][k]=4
    for k in SHADE5: s["curios"].setdefault(k,{"n":1,"cid":0,"at":s["date"]})
    s["explore"]["9"]=2; del s["curios"]["mirror"]
    load(pg,s); tabto(pg,"hearth"); pg.tap("#hCompass"); pg.wait_for_timeout(400)
    rec("Compass","with only Void unfinished, the compass points across to Void","toward Void" in pg.inner_text("#hCompLine"),pg.inner_text("#hCompLine"))
    hsheet(pg,"shelf"); pg.tap("#hGift"); pg.wait_for_timeout(400)
    rec("Gift","gift links offer front curios only",pg.locator("#modal [data-gcur]").count()==20 and pg.locator("#modal [data-gcur='thorn']").count()==0)
    closemodals(pg)
    openmap(pg); pg.tap("#mapTurn"); pg.wait_for_timeout(400); labels=pg.evaluate("[...document.querySelectorAll('.mapsvg text')].map(t=>t.textContent)")
    rec("Map","with every realm charted, all five Shade realms are lit",all(x in labels for x in ("Bramble","Inferno","Abyss","Wraith","Void")),labels)
    pg.evaluate("document.documentElement.setAttribute('data-theme','light')"); settle(pg); bad+=["back light: "+v for v in axe(pg)]
    # plain look by day
    s=st(pg); s["settings"]["sky"]="plain"; s["settings"]["theme"]="light"; load(pg,s); openmap(pg); pg.tap("#mapTurn"); pg.wait_for_timeout(400); settle(pg); bad+=["back plain: "+v for v in axe(pg)]
    rec("A11y","zero accessibility violations on the Forge, the back of the map, the wander sheet and Tales",not bad,bad[:4])
    # old save with dark mood: loads clean, bright names on the front
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    ctx,pg=newpage(b,320,640,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg); dev(pg,"shade"); closemodals(pg)
    w=pg.evaluate("document.documentElement.scrollWidth"); rec("Layout","at 320 px with reduced motion, the back of the map fits and draws",w<=320 and pg.locator(".mapwrap.mback").count()==1,w)
    small=pg.evaluate("[...document.querySelectorAll('#mapTurn')].filter(b=>b.getBoundingClientRect().height<44).length")
    rec("Layout","Turn the map over is a 44-point target",small==0)
    rec("All","no page errors at 320 px",not pg._errs,pg._errs[:2]); ctx.close()
save_results("qa_41")
