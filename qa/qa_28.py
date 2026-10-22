from lib import *
# 0.28.0: a Forgeling that notices your days. Showing up warms the bond of the Forgeling by the fire; the Hearth brings
# back an old margin line to answer. Played with real taps.
import datetime as _dt
BASE=[_dt.date.today()]
def ago(n): return (BASE[0]-_dt.timedelta(days=n)).isoformat()
def load(pg,s):
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def bond(pg,cid): return [c for c in st(pg)["cards"] if c["id"]==cid][0]["bond"]
def do_day(pg):
    tabto(pg,"today"); pg.tap("#btnTurnGo"); pg.wait_for_selector("#vBack",state="visible"); pg.tap("#vBack")
    pg.wait_for_timeout(700); pg.evaluate("()=>{const o=document.querySelector('#modal #vOk');if(o)o.click();}"); pg.wait_for_timeout(500); closemodals(pg)
    pg.wait_for_selector("#btnDone",state="visible"); pg.tap("#btnDone"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{const m=[...document.querySelectorAll('#modal [data-mood]')].find(b=>/mix/i.test(b.textContent));if(m)m.click()}"); pg.wait_for_timeout(900)
    pg.wait_for_selector("#cover",state="visible"); pg.tap("#cover")
    pg.wait_for_selector("#rvSkip",state="visible",timeout=8000); pg.tap("#rvSkip"); pg.wait_for_timeout(1500)
    for _ in range(4):
        if not mt(pg): break
        pg.evaluate("()=>{const b=document.querySelector('#modal [data-close]')||document.getElementById('rvDone')||document.getElementById('skipNames');b&&b.click()}"); pg.wait_for_timeout(500)
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,390,844); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); first=s["cards"][0]["id"]
    rec("Day 1","on the first day nobody else is by the fire, so there is no notice",s.get("comp") in (None,) and "Showing up grew" not in pg.inner_text("#view-today"),s.get("comp"))
    # ---------- day 2: the first Forgeling notices ----------
    dev(pg,"next"); closemodals(pg); b0=bond(pg,first); do_day(pg)
    t=pg.inner_text("#view-today"); s=st(pg)
    rec("Notice","doing the small thing grows the bond of the Forgeling by the fire by 1",bond(pg,first)==b0+1,(b0,bond(pg,first)))
    rec("Notice","Today says so in the Forgeling's voice",s["comp"] and s["comp"]["cid"]==first and s["comp"]["line"] in t and "Showing up grew" in t and "bond by 1" in t,t[:300])
    rec("Notice","today's new Forgeling is not the one who notices",s["comp"]["cid"]!=s["todayCard"] and bond(pg,s["todayCard"])==0)
    tabto(pg,"hearth"); h=pg.inner_text("#view-hearth")
    rec("Notice","the Hearth shows the same line",s["comp"]["line"] in h,h[:500])
    rec("Notice","no junk text",not JUNK.search(t+h),JUNK.findall(t+h)[:3])
    # ---------- rest days cost nothing and give nothing ----------
    dev(pg,"next"); closemodals(pg); b1=bond(pg,first); tabto(pg,"today"); pg.tap("#btnTurnGo"); pg.wait_for_selector("#vBack",state="visible"); pg.tap("#vBack"); pg.wait_for_timeout(500); pg.evaluate("()=>{const o=document.querySelector('#modal #vOk');if(o)o.click();}"); pg.wait_for_timeout(400); pg.wait_for_selector("#btnRest",state="visible"); pg.tap("#btnRest"); pg.wait_for_timeout(600); closemodals(pg)
    rec("Rest","a rest day neither grows nor lowers the bond, and shows no notice",bond(pg,first)==b1 and "Showing up grew" not in pg.inner_text("#view-today"))
    # ---------- someone out wandering is skipped ----------
    s=st(pg); ids=[c["id"] for c in s["cards"]]; A,B=ids[0],ids[1]
    s["hearth"]["slots"]=[A,B]; s["wander"]={"id":A,"start":0,"ready":9e15,"realm":s["cards"][0]["theme"]}; load(pg,s)
    dev(pg,"next"); closemodals(pg); bA,bB=bond(pg,A),bond(pg,B); do_day(pg)
    rec("Wander","if the first by the fire is out wandering, the next one notices",bond(pg,A)==bA and bond(pg,B)==bB+1 and st(pg)["comp"]["cid"]==B,(bA,bond(pg,A),bB,bond(pg,B)))
    # ---------- a bond level-up from showing up is named ----------
    s=st(pg); s["wander"]=None; s["hearth"]["slots"]=[A]; [c.update(bond=2) for c in s["cards"] if c["id"]==A]; load(pg,s)
    dev(pg,"next"); closemodals(pg); do_day(pg); t=pg.inner_text("#view-today")
    rec("Level","when showing up reaches a new bond level, Today names it",bond(pg,A)==3 and "is now Friendly" in t,t[:300])
    # ---------- the margin comes back ----------
    s=st(pg); BASE[0]=_dt.date.fromisoformat(s["date"]); s["startDate"]=ago(20); s["journal"]={ago(10):{"v":2,"text":"Finish the essay draft"},ago(3):{"v":1,"text":"Too recent to echo"},ago(80):{"v":1,"text":"Too old to echo"}}
    s["mEcho"]=None; s["mEchoed"]=[]; s["hearth"]["slots"]=[A]; s["wander"]=None; load(pg,s); tabto(pg,"hearth"); h=pg.inner_text("#view-hearth")
    nmA=[c for c in s["cards"] if c["id"]==A][0]; nmA=nmA.get("nick") or nmA["name"]
    rec("Echo","from day 8, the Hearth brings back a margin line from 7 to 60 days ago","Finish the essay draft" in h and "Too recent" not in h and "Too old" not in h and f"{nmA} found something" in h,h[:300])
    rec("Echo","…with the question it answered, and three gentle replies",pg.locator("[data-mecho]").count()==3 and "when the Forge asked" in h)
    small=pg.evaluate("[...document.querySelectorAll('[data-mecho]')].filter(b=>b.getBoundingClientRect().height<44).length")
    rec("Echo","the replies are easy to tap",small==0)
    vis_before=st(pg)["hearth"]["visits"]
    pg.tap("[data-mecho='did']"); pg.wait_for_timeout(500); h=pg.inner_text("#view-hearth"); s2=st(pg)
    rec("Echo","answering 'I did it' shows the Forgeling's reply and keeps the line",s2["journal"][ago(10)].get("reply")=="did" and s2["mEcho"]["ans"]=="did" and s2["mEcho"]["line"] in pg.inner_text(".mecho") and pg.locator("[data-mecho]").count()==0,h[:300])
    rec("Echo","answering uses no visit",st(pg)["hearth"]["visits"]==vis_before)
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(300)
    rec("Echo","the Journal shows how it went","Later: you did it." in pg.inner_text("#view-chronicle"))
    pg.reload(); pg.wait_for_timeout(800); closemodals(pg); tabto(pg,"hearth")
    rec("Echo","the answered note stays put for the rest of the day, without the buttons","Finish the essay draft" in pg.inner_text("#view-hearth") and pg.locator("[data-mecho]").count()==0)
    # gap: nothing new for a few days; then the next unanswered line; answered lines never return
    s=st(pg); s["journal"][ago(12)]={"v":3,"text":"Call grandma"}; s["mEcho"]["date"]=ago(2); load(pg,s); tabto(pg,"hearth")
    rec("Echo","no new note within five days of the last one",pg.locator(".mecho").count()==0)
    s=st(pg); s["mEcho"]["date"]=ago(6); load(pg,s); tabto(pg,"hearth"); h=pg.inner_text("#view-hearth")
    rec("Echo","after that, the next line comes back, and an answered one never does","Call grandma" in h and "Finish the essay" not in h,h[:200])
    pg.tap("[data-mecho='let']"); pg.wait_for_timeout(400)
    rec("Echo","'Let it go' is kept in the Journal too",st(pg)["journal"][ago(12)].get("reply")=="let")
    # still on it can come back later
    s=st(pg); s["journal"][ago(15)]={"v":3,"text":"Plant the herbs"}; s["mEcho"]["date"]=ago(6); load(pg,s); tabto(pg,"hearth"); pg.tap("[data-mecho='still']"); pg.wait_for_timeout(300)
    rec("Echo","'Still on it' is kept too",st(pg)["journal"][ago(15)].get("reply")=="still")
    # an unanswered note can come back another day
    s=st(pg); s["journal"][ago(20)]={"v":3,"text":"Fix the bike"}; s["mEcho"]={"date":ago(6),"k":ago(20),"ans":None,"cid":A}; load(pg,s); tabto(pg,"hearth")
    rec("Echo","a note you never answered can come back",("Fix the bike" in pg.inner_text("#view-hearth")))
    # before day 8, nothing
    s=st(pg); s["startDate"]=ago(4); s["mEcho"]=None; load(pg,s); tabto(pg,"hearth")
    rec("Echo","in the first week the Hearth brings nothing back",pg.locator(".mecho").count()==0)
    # ---------- damaged saves ----------
    for junk in [{"comp":"x","mEcho":5,"mEchoed":"y"},{"comp":{"date":3},"mEcho":{"k":None},"mEchoed":[1,None,"a"]}]:
        s=st(pg); s.update(junk); s["journal"][ago(9)]={"v":1,"text":"ok","reply":"maybe"}; load(pg,s); tabto(pg,"hearth"); tabto(pg,"today"); tabto(pg,"chronicle")
    s=st(pg)
    rec("Damaged","broken notice and echo data is repaired without errors",not pg._errs and (s.get("comp") is None or isinstance(s["comp"],dict)) and all(isinstance(x,str) for x in s.get("mEchoed",[])) and "reply" not in s["journal"][ago(9)],pg._errs[:1])
    # ---------- accessibility ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    s=st(pg); s["startDate"]=ago(20); s["mEcho"]=None; s["journal"][ago(25)]={"v":2,"text":"Read one chapter"}; s["comp"]={"date":s["date"],"cid":A,"line":"Test line.","up":0}; s["status"]="done"
    for scheme in ("light","dark"):
        c2,p2=newpage(b,390,844,color_scheme=scheme); p2.goto(P); p2.wait_for_selector("#titleGo"); first_card(p2); closemodals(p2); load(p2,s)
        for tb in ("hearth","today"):
            tabto(p2,tb); p2.wait_for_timeout(300)
            p2.wait_for_function("document.getAnimations().filter(a=>a.playState==='running'&&a.effect&&a.effect.getComputedTiming().iterations!==Infinity).length===0",timeout=5000)
            p2.evaluate(AXE); bad+=[f"{scheme} {tb}: {v}" for v in p2.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")]
        rec("A11y",f"{scheme}: the margin note is on the Hearth for the test","found something" in p2.inner_text("#view-hearth"))
        rec("All",f"{scheme}: no page errors",not p2._errs,p2._errs[:1]); c2.close()
    rec("A11y","axe: zero violations on the Hearth note and Today notice, light and dark",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_28"); print(sum(r["ok"] for r in RES),"/",len(RES))
