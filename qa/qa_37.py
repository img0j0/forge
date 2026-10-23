from lib import *
# 0.37.0: Ink. How did it feel? (one tap), ink-touched Forgelings on line days, the book that grows with total lines,
# the month in words, the ribbon, the Journal list with feelings, damaged saves. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def load(pg,s):
    s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def journal(pg):
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(500); return pg.inner_text("#view-chronicle")
def write(pg,txt):
    tabto(pg,"today"); pg.evaluate("document.getElementById('btnMargin').click()"); pg.wait_for_timeout(400); pg.fill("#jIn",txt); pg.evaluate("document.getElementById('jSave').click()"); pg.wait_for_timeout(400)
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); tabto(pg,"today")
    h=pg.inner_text("#view-today .hero")
    rec("Feel","after a done day, Today asks How did it feel? with Easy, Good and Hard","How did it feel?" in h and pg.locator("#view-today [data-feel]").count()==3)
    rec("Feel","the line link now says it inks today's Forgeling","Add a line, and ink today’s Forgeling" in pg.inner_text("#btnMargin"))
    bad+=["today: "+v for v in axe(pg)]
    pg.tap("#view-today [data-feel='good']"); pg.wait_for_timeout(300); s=st(pg)
    rec("Feel","one tap records it, and Today says so",s["feel"].get(s["date"])=="good" and "Today felt good." in pg.inner_text("#view-today .hero") and pg.get_attribute("#view-today [data-feel='good']","aria-pressed")=="true")
    rec("Feel","a tap alone does not ink the Forgeling or count as a line",not [c for c in s["cards"] if c.get("ink")] and s["journal"]=={})
    pg.tap("#view-today [data-feel='good']"); pg.wait_for_timeout(300)
    rec("Feel","tapping it again takes it back",st(pg)["feel"]=={})
    pg.tap("#view-today [data-feel='hard']"); pg.wait_for_timeout(300)
    t=journal(pg); rec("Journal","the Journal lists a tap-only day with its feeling","Felt hard." in t)
    rec("Book","before any line, the book says writing is never needed","Your book" in t and "Writing is never needed" in t)
    # ink
    write(pg,"Scared to start. Started anyway."); s=st(pg); c=[x for x in s["cards"] if x["id"]==s["todayCard"]][0]
    rec("Ink","writing a line on a done day inks today's Forgeling",c.get("ink")=="Scared to start. Started anyway.")
    tabto(pg,"binder"); pg.evaluate(f"()=>{{const e=document.querySelector('#view-binder .card[data-cid=\"{c['id']}\"]');e&&e.click()}}"); pg.wait_for_timeout(800)
    iv=pg.evaluate("()=>{const card=document.querySelector('#stage .card');return {cls:card.classList.contains('inked'),wash:!!card.querySelector('.inkwash'),drop:!!card.querySelector('.inkdrop')}}")
    rec("Ink","the card shows the ink wash and the ink drop",iv["cls"] and iv["wash"] and iv["drop"],iv)
    pg.evaluate("document.getElementById('inspFlip').click()"); pg.wait_for_timeout(800)
    rec("Ink","…and your line on its back","Scared to start. Started anyway." in pg.inner_text("#stage .cbk"))
    bad+=["inked card: "+v for v in axe(pg)]
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    st0=st(pg); others=[x for x in st0["cards"] if x["id"]!=c["id"]]
    rec("Ink","no other Forgeling is inked, and stats are unchanged",not [x for x in others if x.get("ink")] and c["stats"]==[x for x in st0["cards"] if x["id"]==c["id"]][0]["stats"])
    write(pg,""); s=st(pg); c2=[x for x in s["cards"] if x["id"]==c["id"]][0]
    rec("Ink","clearing the line takes the ink away",not c2.get("ink") and s["date"] not in s["journal"])
    write(pg,"Scared to start. Started anyway.")
    # next day: a line written before the card is done does not ink anything
    dev(pg,"next"); closemodals(pg); tabto(pg,"today")
    rec("Feel","before today's card is done, nothing is asked",pg.locator("#view-today [data-feel]").count()==0)
    # the book grows with totals
    s=st(pg); base=s["date"]; import datetime as _d
    def daysago(n): return (_d.date.fromisoformat(base)-_d.timedelta(days=n)).isoformat()
    for L,expect in [(1,"plain"),(10,"leather"),(30,"ribbon"),(60,"someone"),(100,"gold")]:
        s=st(pg); s["journal"]={daysago(i*3+1):{"v":i%12,"text":f"line {i}"} for i in range(L)}; load(pg,s); t=journal(pg)
        lab=pg.get_attribute("#view-chronicle .book","aria-label")
        ok={"plain":"leather" not in lab and f"{L} line written" in t,
            "leather":"bound in leather" in lab and "ribbon" not in lab,
            "ribbon":"with a ribbon" in lab and pg.locator("#bookRibbon").count()==1,
            "someone":"At 100, gold edges" in t,
            "gold":"gold edges and a clasp" in lab}[expect]
        rec("Book",f"{L} lines: {expect}",ok,(lab,t[:160].replace("\n"," | ")))
    rec("Book","lines count in total, never in a row: gaps of three days still count","100 lines written" in t)
    pg.tap("#bookRibbon"); pg.wait_for_timeout(500); m=mt(pg)
    rec("Ribbon","the ribbon opens to an old line","The ribbon falls open at" in m and "line " in m)
    bad+=["ribbon: "+v for v in axe(pg)]; closemodals(pg)
    # the month in words
    s=st(pg); ym=s["date"][:7]; days=[f"{ym}-{d:02d}" for d in range(1,8)]
    s["history"]=[h for h in s["history"] if not h["date"].startswith(ym)]+[{"date":d,"status":"done","v":4} for d in days[:5]]+[{"date":days[5],"status":"rest","v":2}]
    s["feel"]={days[0]:"good",days[1]:"good",days[2]:"hard",days[3]:"hard",days[4]:"good"}
    s["owns"]=[{"id":1,"text":"Text Mom","k":2,"days":days[:2]}]
    load(pg,s); t=journal(pg)
    rec("Month","the month reads in words: days shown up, rests, your own things, how it felt, the hardest week, lines",
        "Your month in words" in t and "you showed up on 5 days, and rested on 1" in t and "You did “Text Mom” twice." in t and "Most days felt good." in t and "Your hardest week was the first." in t,
        [l for l in t.split("\n") if "In " in l][:2])
    rec("Month","no percentages or charts",not re.search(r"\d+\s*%",t))
    bad+=["journal: "+v for v in axe(pg)]
    # damaged
    s=st(pg); s["feel"]={"x":"good","2026-01-01":"meh","2026-01-02":"hard"}; s["cards"][0]["ink"]=7; load(pg,s); s=st(pg)
    rec("Damaged","broken feelings and ink are repaired",s["feel"]=={"2026-01-02":"hard"} and not s["cards"][0].get("ink") and all("ink" not in c for c in s["cards"][1:] if not c.get("ink")) and not pg._errs,s["feel"])
    s=st(pg); s["cards"][0]["ink"]="<img src=x onerror=alert(1)>"; load(pg,s); tabto(pg,"binder"); pg.evaluate(f"()=>{{const e=document.querySelector('#view-binder .card[data-cid=\"{s['cards'][0]['id']}\"]');e&&e.click()}}"); pg.wait_for_timeout(700)
    pg.evaluate("document.getElementById('inspFlip').click()"); pg.wait_for_timeout(700)
    rec("Safe","ink lines show as text, never markup",pg.locator("#stage .cbk img").count()==0 and "<img src=x" in pg.inner_text("#stage .cbk"))
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    s=st(pg); del s["feel"]; load(pg,s); rec("Migrate","an older save without feelings picks them up",st(pg)["feel"]=={})
    rec("A11y","axe: zero violations on Today's check-in, an inked card, the book, the ribbon and the month",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_37"); print(sum(r["ok"] for r in RES),"/",len(RES))
