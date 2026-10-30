from lib import *
# 0.19.0: bond stories (a chapter of each Forgeling's own story per bond level) and the Hearth that grows from your callings.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity|\{[a-z]+\}")
def hist(s,spec):
    """spec: list of (status, v) going back from yesterday."""
    d0=datetime.date.fromisoformat(s["date"]); out=[]
    for i,(stt,v) in enumerate(reversed(spec)):
        out.append({"date":(d0-datetime.timedelta(days=i+1)).isoformat(),"status":stt,"v":v})
    s["history"]=list(reversed(out)); return s
def ready(pg,s):
    setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # ---------- stories ----------
    s=build(base,[2,2,2,2,2],dark_in={0,1,2,3,4}); s["seen"]=99; s["hearth"]["slots"]=[s["cards"][0]["id"],s["cards"][1]["id"]]
    for i,c in enumerate(s["cards"]): c["source"]="daily" if i%2 else "pack"; c["v"]=i%12; c["bond"]=25
    ready(pg,s)
    def chapters(pg,idx):
        s2=st(pg); s2["hearth"]["slots"]=[s2["cards"][idx]["id"]]; ready(pg,s2); tabto(pg,"hearth")
        hsheet(pg,"comp"); pg.evaluate("document.querySelector('#modal [data-tale]').click()"); pg.wait_for_timeout(300)
        ch=pg.evaluate("[...document.querySelectorAll('#modal .tale p')].map(p=>p.textContent)"); closemodals(pg)
        pg.evaluate("()=>{const b=document.getElementById('taleBack');if(b)b.click();}"); pg.wait_for_timeout(200); return ch
    names=[c.get("nick") or c["name"] for c in st(pg)["cards"]]
    all_ch=[chapters(pg,i) for i in range(len(names))]
    flat=[t for ch in all_ch for t in ch]
    rec("Story","every Forgeling in all 10 realms has five chapters with no junk or unfilled blanks",all(len(ch)==5 for ch in all_ch) and not any(JUNK.search(t) for t in flat),[t for t in flat if JUNK.search(t)][:2])
    rec("Story","no two Forgelings share the same first three chapters",len({"|".join(ch[:3]) for ch in all_ch})==len(all_ch))
    rec("Story","each chapter names the Forgeling and chapter 1 names its realm",all(all((nm in t) for t in ch) for ch,nm in zip(all_ch,names)) and all(any(r in ch[0] for r in ("Meadow","Bramble","Ember","Inferno","Tide","Abyss","Frost","Wraith","Dusk","Void")) for ch in all_ch))
    daily_ok=all(("You had just" in ch[3])==(i%2==1) for i,ch in enumerate(all_ch))
    rec("Story","'The day it found you' recalls the calling you did for daily finds and the pack for pack finds",daily_ok,[ch[3][:60] for ch in all_ch[:2]])
    rec("Story","the story is the same after reopening the app",chapters(pg,3)==all_ch[3])
    s=st(pg); s["cards"][3]["dark"]=not s["cards"][3]["dark"]; ready(pg,s)
    rec("Story","cute and Shade Forgelings get different voices",chapters(pg,3)[1]!=all_ch[3][1])
    # sheet from the Hearth, chapters locked by bond level
    s=st(pg); s["cards"][0]["bond"]=8; s["hearth"]["slots"]=[s["cards"][0]["id"]]; ready(pg,s); tabto(pg,"hearth")
    hsheet(pg,"comp"); row=pg.inner_text("#modal [data-tale]"); closemodals(pg)
    rec("Story","the Hearth shows the story row with the chapter count and what opens next","3 of 5 chapters" in row and "Devoted" in row,row)
    hsheet(pg,"comp"); pg.evaluate("document.querySelector('#modal [data-tale]').click()"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Story","at bond level 3 the first three chapters are open and the last two are not",all(t in m for t in ("1. Where it began","2. What it loves","3. What it keeps")) and m.count("Opens when you are")==2,m[:200])
    pg.evaluate("document.getElementById('taleBack').click()"); pg.wait_for_timeout(300)
    rec("Story","…Close returns to the Hearth",pg.evaluate("document.getElementById('modal').hidden") and not pg.evaluate("document.getElementById('view-hearth').hidden"))
    # nickname follows
    s=st(pg); s["cards"][0]["nick"]="Biscuit"; ready(pg,s)
    rec("Story","a new nickname appears in the story",all("Biscuit" in t for t in chapters(pg,0)[:3]))
    # bond-up shows the new chapter
    s=st(pg); s["cards"][0]["bond"]=14; s["hearth"]["slots"]=[s["cards"][0]["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":0}; ready(pg,s); tabto(pg,"hearth"); pg.evaluate("[...document.querySelectorAll('#view-hearth [data-hslot]')][0].click()"); pg.wait_for_timeout(200)
    pg.evaluate("document.getElementById('hStory').click()"); pg.wait_for_timeout(300); pg.fill("#storyIn","We found a bridge."); pg.evaluate("document.getElementById('storySave').click()"); pg.wait_for_timeout(1300); m=mt(pg)
    rec("Story","growing a bond opens the next chapter right in the bond-up note","New chapter: The day it found you" in m and "Biscuit" in m,m[:220])
    closemodals(pg)
    # from the card view, and back
    tabto(pg,"binder"); pg.evaluate("document.querySelector('#view-binder [data-insp]').click()"); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('#modal [data-tale]').click()"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Story","the card view has a Story button that opens the story","’s story" in m and " of 5 chapters" in m,m[:80])
    pg.evaluate("document.getElementById('taleBack').click()"); pg.wait_for_timeout(500)
    rec("Story","…and Close returns to the card",pg.locator("#modal #inspFlip").count()==1)
    closemodals(pg); pg.evaluate("()=>{const c=document.getElementById('ovClose');if(c)c.click();}"); pg.wait_for_timeout(300)
    # ---------- the Hearth grows ----------
    s=build(base,[1,1,1,0,0]); s["seen"]=99; s["hearth"]["slots"]=[c["id"] for c in s["cards"]]; s["hearth"]["fseen"]=[]; s["history"]=[]; ready(pg,s)
    tabto(pg,"hearth"); hsheet(pg,"furn"); t=mt(pg); closemodals(pg)
    rec("Hearth","the list says 0 of 16 and shows how to get the first thing","By the fire, 0 of 16" in t and "After your first calling. 0 so far." in t,t[-400:])
    s=hist(st(pg),[("done",2),("rest",5),("done",2),("skipped",4),("done",2)]); s["hearth"]["fseen"]=[]; ready(pg,s)
    tabto(pg,"today"); r=pg.inner_text("#btnHearth")
    rec("Hearth","Today's Hearth row says something new is waiting and is marked ready","Something new is waiting by the fire" in r and pg.evaluate("document.getElementById('btnHearth').classList.contains('ready')"),r)
    tabto(pg,"hearth"); msg=pg.inner_text("#hmsg")
    rec("Hearth","3 days done (rest and missed days not counted) bring the rug, and 3 Depth days the pond; opening the Hearth announces them once",msg=="2 new things by the fire. Have a look around." and sorted(st(pg)["hearth"]["fseen"])==["pond","rug"],msg)
    tabto(pg,"today"); r=pg.inner_text("#btnHearth") if pg.locator("#btnHearth").count() else ""
    rec("Hearth","…after that, Today's row goes back to normal","Something new" not in r and not pg.evaluate("document.getElementById('btnHearth').classList.contains('ready')"),r)
    tabto(pg,"hearth"); hsheet(pg,"furn"); t=mt(pg); closemodals(pg)
    rec("Hearth","the list explains each one in your own terms","You have given something your full attention 3 times." in t and "After 3 Clarity days. 0 so far." in t and "By the fire, 2 of 16" in t,t[-500:])
    s=st(pg); s["history"].append({"date":s["history"][-1]["date"],"status":"done","v":2}); ready(pg,s)
    tabto(pg,"hearth"); hsheet(pg,"furn")
    rec("Hearth","a doubled day in a damaged history counts once","After 5 callings done. 3 so far." in mt(pg)); closemodals(pg)
    # one at a time: a single new thing gets its own name
    s=hist(st(pg),[("done",2)]*3+[("done",3)]*3); s["hearth"]["fseen"]=["pond","rug","lights"]; ready(pg,s); tabto(pg,"hearth")
    rec("Hearth","a single new thing is named",pg.inner_text("#hmsg")=="Something new by the fire: a paper kite.",pg.inner_text("#hmsg"))
    # the pixels actually change: one Forgeling by the fire, at night, nothing earned vs everything earned
    PX="()=>[...document.getElementById('hearthCv').getContext('2d').getImageData(0,0,128,72).data]"
    BOX={"rug":(44,64,84,69),"lights":(0,2,127,10),"tree":(0,22,14,51),"hedge":(111,45,119,50),"stones":(31,60,38,68),"pond":(0,63,19,70),"kite":(28,9,36,20),"mail":(119,57,124,67),"stump":(89,61,96,68),"ball":(23,61,27,65),"lamp":(123,27,125,51),"menhir":(82,43,85,50),"bell":(41,41,47,50),"fence":(0,44,127,51),"fern":(106,60,112,68)}
    shots={}
    for label,spec in (("none",[]),("all",[("done",i%12) for i in range(60)])):
        s=build(base,[1,0,0,0,0]); s["seen"]=99; s["hearth"]["slots"]=[s["cards"][0]["id"]]; s=hist(s,spec); s["hearth"]["fseen"]=[]; s["settings"]["reduce"]=True; ready(pg,s); tabto(pg,"hearth"); pg.wait_for_timeout(400)
        shots[label]=pg.evaluate(PX)
        if label=="none": rec("Hearth","with reduced motion on, the Hearth scene is drawn (it used to stay blank)",sum(shots[label])>0)
    def changed(box):
        x0,y0,x1,y1=box; n=0
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                o=(y*128+x)*4
                if sum(abs(shots["all"][o+k]-shots["none"][o+k]) for k in range(3))>60: n+=1
        return n
    miss=[k for k,bx in BOX.items() if changed(bx)<4]
    rec("Hearth","every one of the 15 still things by the fire is visible in the scene",not miss,miss)
    rec("Hearth","all 16 are counted once everything is earned","By the fire · 16 of 16" in pg.inner_text("#view-hearth"))
    # asleep: nothing is announced until they wake
    s=hist(st(pg),[("done",i%12) for i in range(36)]); s["hearth"]["fseen"]=[]; s["hearth"]["sleep"]={"tier":1,"since":s["date"],"dream":0}; ready(pg,s); tabto(pg,"hearth")
    rec("Hearth","while your Forgelings are asleep, new things wait to be announced",st(pg)["hearth"]["fseen"]==[] and not pg._errs,pg._errs[:1])
    # damaged and older saves
    for bad in ("x",{"a":1},[1,"rug","rug",None],None):
        s=st(pg); s["hearth"]["sleep"]=None; s["hearth"]["fseen"]=bad; ready(pg,s)
        fs=st(pg)["hearth"]["fseen"]
        rec("Damaged",f"a damaged list of seen things ({bad!r}) is repaired",isinstance(fs,list) and all(isinstance(x,str) for x in fs) and len(fs)==len(set(fs)) and not pg._errs,(fs,pg._errs[:1]))
    s=st(pg); del s["hearth"]["fseen"]; ready(pg,s); tabto(pg,"hearth")
    rec("Damaged","someone updating from an older version is greeted with everything they already earned",len(st(pg)["hearth"]["fseen"])>0 and "new things by the fire" in pg.inner_text("#hmsg"),pg.inner_text("#hmsg"))
    rec("All","no page errors",not pg._errs,pg._errs[:2])
    ctx.close()
    # ---------- accessibility of the new parts ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        ctx,pg=newpage(b,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
        s=build(base,[1,1,1,0,0],dark_in={1}); s["seen"]=99; s["hearth"]["slots"]=[c["id"] for c in s["cards"]]; s["cards"][0]["bond"]=9; s=hist(s,[("done",i%12) for i in range(40)]); s["hearth"]["fseen"]=[]
        setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
        for where in ("today","hearth","story"):
            if where=="today": tabto(pg,"today")
            if where=="hearth": tabto(pg,"hearth"); hsheet(pg,"furn")
            if where=="story": hsheet(pg,"comp"); pg.evaluate("document.querySelector('#modal [data-tale]').click()"); pg.wait_for_timeout(500)
            pg.wait_for_function("!document.body.classList.contains('arrive')"); pg.evaluate(AXE); v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
            bad+=[f"{scheme}/{where}: {x}" for x in v]
        ctx.close()
    rec("A11y","axe: zero violations on Today, the Hearth with its lists open, and a story, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_19"); print(sum(r["ok"] for r in RES),"/",len(RES))
