from lib import *
# 0.36.0: Your small things. What you want more of (leaning the deck), up to three own small things on the card,
# the Mix setting, realm leanings, card backs, migration of the old single own small thing, damaged saves. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def load(pg,s):
    s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def turn(pg):
    tabto(pg,"today"); pg.tap("#btnTurnGo"); pg.wait_for_selector("#vBack",state="visible"); pg.tap("#vBack"); pg.wait_for_timeout(600)
def finish(pg):
    pg.evaluate("()=>{const o=document.getElementById('vOk');o&&o.click()}"); pg.wait_for_timeout(300); pg.tap("#btnDone"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{const m=[...document.querySelectorAll('#modal [data-mood]')].find(b=>/mix/i.test(b.textContent));m&&m.click()}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{const c=document.getElementById('cover');c&&c.click()}"); pg.wait_for_selector("#rvSkip",state="visible",timeout=8000); pg.tap("#rvSkip"); pg.wait_for_timeout(1300)
    for _ in range(4):
        if not mt(pg): break
        pg.evaluate("()=>{const b=document.querySelector('#modal [data-close]')||document.getElementById('rvDone');b&&b.click()}"); pg.wait_for_timeout(400)
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); rec("Start","a fresh save starts with no wants, no own things, the Mix setting, and the old field still shaped",s["want"]==[] and s["owns"]==[] and s["settings"]["ownMix"]=="mix" and s["own"]=={"text":"","days":[]} and not s["wantAsked"])
    tabto(pg,"today")
    rec("Ask","after the first find, Today offers 'Make your cards yours' first",pg.evaluate("document.querySelector('#view-today .group .rowl').id")=="btnWant" and "What do you want more of" in pg.inner_text("#btnWant"))
    pg.tap("#btnWant"); pg.wait_for_timeout(500); t=mt(pg)
    rec("Ask","it opens 'What do you want more of?' with eight choices",t.startswith("What do you want more of?") and pg.locator("#modal [data-want]").count()==8)
    bad+=["want sheet: "+v for v in axe(pg)]
    for k in (0,1,2): pg.tap(f"#modal [data-want='{k}']"); pg.wait_for_timeout(120)
    pg.tap("#modal [data-want='3']"); pg.wait_for_timeout(200)
    rec("Ask","a fourth choice is refused, gently",pg.locator("#modal [aria-pressed='true']").count()==3 and "Three at most" in pg.inner_text("#toast"))
    pg.tap("#modal [data-want='2']"); pg.tap("#modal [data-want='4']"); pg.tap("#wantSave"); pg.wait_for_timeout(500); s=st(pg)
    rec("Ask","Save keeps the three chosen and the row goes away",s["want"]==[0,1,4] and s["wantAsked"] and pg.locator("#btnWant").count()==0,s["want"])
    # the deck leans: over many new days, at least about half the cards come from the chosen callings
    lean={11,6,5,8,2,1,0}; hits=0; N=40
    for i in range(N):
        dev(pg,"next"); closemodals(pg)
        if st(pg)["todayV"] in lean: hits+=1
    rec("Lean",f"the daily card leans to what you want more of ({hits} of {N} days; a random deck would give about {round(N*7/12)})",hits>=N*0.7,hits)
    # Settings: your cards
    tabto(pg,"settings"); t=pg.inner_text("#yourCards")
    rec("Settings","Settings has Your cards, with the wants and room for own small things",
        "Your cards" in t and pg.locator("#yourCards [data-swant][aria-pressed='true']").count()==3 and pg.locator("#ownIn").count()==1)
    pg.evaluate("document.getElementById('ownAdd').click()"); pg.wait_for_timeout(200)
    rec("Own","adding an empty one does nothing",st(pg)["owns"]==[])
    pg.fill("#ownIn","  Walk for ten minutes <b>outside</b> and then some words that make it far too long  "); pg.tap("#yourCards [data-ownk='0']"); pg.evaluate("document.getElementById('ownAdd').click()"); pg.wait_for_timeout(300)
    o=st(pg)["owns"]; rec("Own","an own small thing is saved, trimmed to 60 characters, with its kind",len(o)==1 and o[0]["text"].startswith("Walk for ten minutes <b>outside</b>") and len(o[0]["text"])<=60 and o[0]["k"]==0,o)
    rec("Own","its words show as written, never as markup",pg.locator("#yourCards b",has_text="<b>outside</b>").count()==1)
    pg.fill("#ownIn","Text Mom"); pg.tap("#yourCards [data-ownk='2']"); pg.evaluate("document.getElementById('ownAdd').click()"); pg.wait_for_timeout(300)
    pg.fill("#ownIn","Water before coffee"); pg.tap("#yourCards [data-ownk='1']"); pg.evaluate("document.getElementById('ownAdd').click()"); pg.wait_for_timeout(300)
    rec("Own","three is the most: the add form goes away",len(st(pg)["owns"])==3 and pg.locator("#ownIn").count()==0)
    rec("Own","How often yours come up shows, on Every other day or so",pg.locator("#yourCards [data-ownmix='mix'][aria-pressed='true']").count()==1)
    bad+=["settings: "+v for v in axe(pg)]
    # Mix: about half the days are yours; Most days: most; Only the world's: none
    def share(mode,n=30):
        if mode: pg.evaluate(f"document.querySelector('[data-ownmix=\"{mode}\"]').click()"); pg.wait_for_timeout(200)
        k=0
        for i in range(n):
            dev(pg,"next"); closemodals(pg)
            if st(pg)["todayOwn"] is not None: k+=1
        tabto(pg,"settings"); return k
    tabto(pg,"settings"); m=share(None); rec("Mix",f"Mix: about every other day is yours ({m} of 30)",8<=m<=22,m)
    mm=share("mine"); rec("Mix",f"Most days: most days are yours ({mm} of 30)",mm>=19,mm)
    ms=share("surprise"); rec("Mix",f"Only the world's cards: none are yours ({ms} of 30)",ms==0,ms)
    pg.evaluate("document.querySelector('[data-ownmix=\"mix\"]').click()"); pg.wait_for_timeout(200)
    # an own day, end to end
    s=st(pg); o=[x for x in s["owns"] if x["text"]=="Text Mom"][0]; s["todayOwn"]=o["id"]; s["todayV"]=4; s["status"]="fresh"; load(pg,s)
    turn(pg); t=mt(pg)
    rec("Card","an own-thing card reads 'Yours · Connection', with your words as the small thing",t.count("Yours · Connection")==1 and "Your small thing" in t and "Text Mom" in t and "Something you chose for yourself" in t,t[:200])
    rec("Card","…with a little pen mark",pg.locator("#modal .vfront .pen").count()>=1)
    bad+=["own card: "+v for v in axe(pg)]
    pg.evaluate("()=>{const o=document.getElementById('vOk');o&&o.click()}"); pg.wait_for_timeout(300); closemodals(pg); tabto(pg,"today")
    rec("Card","Today's card face shows it too",("Yours · Connection" in pg.inner_text("#view-today .taskface")) and ("Text Mom" in pg.inner_text("#view-today .taskface")))
    finish(pg); s=st(pg); c=[x for x in s["cards"] if x["id"]==s["todayCard"]][0]; h=s["history"][-1]; o2=[x for x in s["owns"] if x["id"]==o["id"]][0]
    rec("Done","doing it is a done day like any other, and remembers whose it was",s["status"]=="done" and h["status"]=="done" and h.get("own")==o["id"] and s["date"] in o2["days"] and c["own"]=="Text Mom",(h,c.get("own")))
    tabto(pg,"binder"); pg.evaluate(f"()=>{{const e=document.querySelector('#view-binder .card[data-cid=\"{c['id']}\"]');e&&e.click()}}"); pg.wait_for_timeout(700)
    pg.evaluate("document.getElementById('inspFlip').click()"); pg.wait_for_timeout(800)
    rec("Back","its card back says 'Yours: Text Mom'","Yours: Text Mom" in pg.inner_text("#stage .cbk"),pg.inner_text("#stage .cbk")[:120])
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    # realm leaning: own Moving days find Meadow Forgelings more often
    s=st(pg); mv=[x for x in s["owns"] if x["k"]==0][0]
    meadow=0
    for i in range(24):
        dev(pg,"next"); closemodals(pg); s=st(pg); s["todayOwn"]=mv["id"]; s["status"]="revealed"; load(pg,s); tabto(pg,"today")
        pg.evaluate("document.getElementById('btnDone').click()"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{const c=document.getElementById('cover');c&&c.click()}"); pg.wait_for_timeout(300); pg.evaluate("()=>{const b=document.getElementById('rvSkip');b&&b.click()}"); pg.wait_for_timeout(500); closemodals(pg)
        s=st(pg); cc=[x for x in s["cards"] if x["id"]==s["todayCard"]]
        if cc and cc[0]["theme"]==0: meadow+=1
    rec("Realm",f"own Moving days lean to Meadow ({meadow} of 24; random would be about 5)",meadow>=10,meadow)
    # removing keeps the past days for the Journal calendar
    s=st(pg); before=len([x for x in s["owns"] if x["id"]==mv["id"]][0]["days"])
    tabto(pg,"settings"); pg.evaluate(f"document.querySelector('[data-ownrm=\"{mv['id']}\"]').click()"); pg.wait_for_timeout(300); s=st(pg)
    rec("Remove","removing one keeps its past days for the Journal",all(x["id"]!=mv["id"] for x in s["owns"]) and len(s["own"]["days"])>=before and before>0 and pg.locator("#ownIn").count()==1,(before,len(s["own"]["days"])))
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(500)
    rec("Journal","the Journal calendar still marks those days",pg.locator("#view-chronicle .cal .c.own").count()>=1)
    # migration from the old single own small thing
    s=st(pg); s["owns"]=[]; s["own"]={"text":"Drink a glass of water","days":["2026-01-02","2026-01-05"]}; del s["want"]; del s["wantAsked"]; del s["settings"]["ownMix"]; load(pg,s); s=st(pg)
    rec("Migrate","the old own small thing becomes your first one, with its ticks",len(s["owns"])==1 and s["owns"][0]["text"]=="Drink a glass of water" and s["owns"][0]["days"]==["2026-01-02","2026-01-05"] and s["owns"][0]["k"]==-1 and s["own"]["text"]=="" and s["settings"]["ownMix"]=="mix" and s["want"]==[],s["owns"])
    tabto(pg,"today"); rec("Migrate","the old tick row is gone from Today",pg.locator("#btnOwn").count()==0)
    tabto(pg,"settings"); rec("Migrate","Settings lists it as 'Any kind'","Any kind" in pg.inner_text("#yourCards"))
    # damaged saves
    s=st(pg); s["want"]=[9,"x",1,1,2,3,4]; s["owns"]=[{"id":"a","text":"  ok  ","k":99,"days":["bad","2026-02-02","2026-02-02"]},{"text":""},5,{"id":1,"text":"two","k":3,"days":[]},{"id":7,"text":"three"},{"id":8,"text":"four"}]; s["todayOwn"]=42; s["settings"]["ownMix"]="weird"; load(pg,s); s=st(pg)
    rec("Damaged","broken wants and own things are repaired",s["want"]==[1,2,3] and len(s["owns"])==3 and s["owns"][0]["text"]=="ok" and s["owns"][0]["k"]==-1 and s["owns"][0]["days"]==["2026-02-02"] and len({o["id"] for o in s["owns"]})==3 and s["todayOwn"] is None and s["settings"]["ownMix"]=="mix" and not pg._errs,(s["want"],s["owns"]))
    s=st(pg); s["owns"][0]["text"]="<img src=x onerror=alert(1)>"; s["todayOwn"]=s["owns"][0]["id"]; s["status"]="revealed"; load(pg,s); tabto(pg,"today")
    rec("Safe","own words are shown as text everywhere, never run as markup",pg.locator("#view-today .taskface img").count()==0 and "<img src=x" in pg.inner_text("#view-today .taskface") and not pg._errs)
    rec("A11y","axe: zero violations on the want sheet, Your cards and an own-thing card",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_36"); print(sum(r["ok"] for r in RES),"/",len(RES))
