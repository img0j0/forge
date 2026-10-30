from lib import *
# 0.17.0: Echoes (anniversaries on Today), the mirror (what you have done), and the shared-world line.
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
FAKE="""(()=>{const R=Date;let off=+(localStorage.getItem('__off')||sessionStorage.getItem('__off')||0);window.__setOff=v=>{off=v;sessionStorage.setItem('__off',String(v));localStorage.setItem('__off',String(v));};window.__real=()=>R.now();
class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"""
def mk(b):
    ctx,pg=newpage(b,timezone_id="America/New_York",locale="en-US"); pg.add_init_script(FAKE); pg.set_default_timeout(7000); return ctx,pg
def setclock(pg,iso):
    ms=pg.evaluate("(s)=>new Date(s).getTime()-window.__real()",iso); pg.evaluate("(v)=>window.__setOff(v)",ms)
def today_text(pg): return pg.inner_text("#view-today")
def scenario(pg,base,today,cards,status="done",todayV=4,hist=None,journal=None,extra=None):
    """cards: list of (date, source). Today's daily card is added when status is done."""
    s=json.loads(json.dumps(base)); tpl=s["cards"][0]; out=[]; nid=1
    for d,src in cards:
        c=dict(tpl); c["id"]=nid; c["date"]=d; c["source"]=src; c["name"]="Echo"+str(nid); c["nick"]=""; c["tale"]=""; c["v"]=nid%12
        for k in ("era","gossip"): c.pop(k,None)
        out.append(c); nid+=1
    s["history"]=list(hist or [])
    if status=="done":
        c=dict(tpl); c["id"]=nid; c["date"]=today; c["source"]="daily"; c["name"]="TodayOne"; c["v"]=todayV
        for k in ("era","gossip"): c.pop(k,None)
        out.append(c); s["todayCard"]=nid; nid+=1
        s["history"].append({"date":today,"status":"done","v":todayV,"card":s["todayCard"]})
    elif status=="rest": s["todayCard"]=None; s["history"].append({"date":today,"status":"rest","v":todayV})
    else: s["todayCard"]=None
    s["cards"]=out; s["nextId"]=nid; s["date"]=today; s["status"]=status; s["todayV"]=todayV; s["offset"]=0; s["seen"]=20
    s["startDate"]=min([d for d,_ in cards]+[today]); s["opens"]=[today]; s["journal"]=journal or {}
    s["hearth"]["sleep"]=None; s["wander"]=None; s.pop("echo",None)
    for k2,v2 in (extra or {}).items(): s[k2]=v2
    setst(pg,s); setclock(pg,today+"T12:00:00"); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
    return today_text(pg)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    t=today_text(pg)
    rec("Mirror","the first card of the month says so, in plain words","That's the first time this month you've" in t,t[:260].replace("\n"," | "))
    rec("Echo","a brand-new player sees no echo",pg.locator("#view-today .echo").count()==0)
    base=st(pg)
    # what is new
    s=st(pg); s["seen"]=19; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); m=mt(pg)
    rec("New","What is new opens once for an older save (it now lists only the latest notes)","What is new" in m and m.count("\n")>3,m[:120].replace("\n"," | "))
    closemodals(pg); pg.reload(); pg.wait_for_timeout(600); rec("New","…and not again",mt(pg)=="")
    # anniversaries
    t=scenario(pg,base,"2026-12-15",[("2026-11-15","daily")])
    rec("Echo","one month later, the card comes back under today's card","A month ago today" in t and "Echo1" in t,t[-200:].replace("\n"," | "))
    rec("Echo","…once, as a single quiet line",pg.locator("#view-today .echo").count()==1)
    rec("Echo","…with no junk text",not JUNK.search(pg.inner_text("#view-today .echo")))
    pg.evaluate("document.querySelector('#view-today .echo [data-kept]').click()"); pg.wait_for_timeout(500); m=mt(pg)
    rec("Echo","Read that day again opens its Second reading","Second reading" in m and "you found Echo1" in m,m[:160].replace("\n"," | "))
    pg.evaluate("document.getElementById('keptBack').click()"); pg.wait_for_timeout(400)
    rec("Echo","…and closing returns to Today with nothing left open",mt(pg)=="" and pg.locator("#view-today .echo").count()==1)
    t=scenario(pg,base,"2026-11-29",[("2026-11-15","daily")])
    rec("Echo","two weeks later, it notes that the second reading has just opened","Two weeks ago today" in t and "just opened" in t,t[-200:].replace("\n"," | "))
    t=scenario(pg,base,"2026-12-05",[("2026-11-15","daily")])
    rec("Echo","an ordinary day (20 days on) shows nothing",pg.locator("#view-today .echo").count()==0)
    t=scenario(pg,base,"2026-11-25",[("2026-11-15","daily")])
    rec("Echo","a card younger than two weeks never echoes",pg.locator("#view-today .echo").count()==0)
    t=scenario(pg,base,"2027-11-15",[("2026-11-15","daily"),("2027-10-15","daily")])
    rec("Echo","when two anniversaries fall on one day, the oldest wins","A year ago today" in t and "Echo1" in t and "Echo2" not in t,t[-200:].replace("\n"," | "))
    rec("Echo","…still only one echo",pg.locator("#view-today .echo").count()==1)
    t=scenario(pg,base,"2026-12-15",[("2026-11-15","pack"),("2026-11-15","daily")])
    rec("Echo","on a day with pack finds too, the daily card is the one remembered","Echo2" in t and "Echo1" not in t,t[-160:].replace("\n"," | "))
    t=scenario(pg,base,"2027-02-28",[("2027-01-31","daily")])
    rec("Echo","month-end: a card from 31 January echoes on 28 February","A month ago today" in t,t[-160:].replace("\n"," | "))
    t=scenario(pg,base,"2030-11-15",[("2026-11-15","daily")])
    rec("Echo","years later: four years ago today","4 years ago today" in t,t[-160:].replace("\n"," | "))
    t=scenario(pg,base,"2026-12-15",[("2026-11-15","daily")],status="rest")
    rec("Echo","a rest day still shows the echo",pg.locator("#view-today .echo").count()==1 and "Resting today" in t)
    for stt in ("fresh","revealed"):
        t=scenario(pg,base,"2026-12-15",[("2026-11-15","daily")],status=stt)
        rec("Echo",f"before today's calling is done ({stt}), nothing distracts from it",pg.locator("#view-today .echo").count()==0)
    t=scenario(pg,base,"2026-12-15",[("2026-11-15","daily")],journal={"2026-11-15":{"v":1,"text":"A very private line"}})
    rec("Echo","privacy: the Today line never shows journal words","A very private line" not in t)
    t=scenario(pg,base,"2026-12-15",[("2027-11-15","daily")])
    rec("Echo","a card dated in the future (clock moved back) is ignored safely",pg.locator("#view-today .echo").count()==0 and not pg._errs,pg._errs[:1])
    # mirror
    h=[{"date":"2026-12-0"+str(i),"status":"done","v":4} for i in (2,5,8)]+[{"date":"2026-11-28","status":"done","v":4},{"date":"2026-12-03","status":"done","v":2},{"date":"2026-12-04","status":"rest","v":4}]
    t=scenario(pg,base,"2026-12-10",[("2026-11-28","daily")],hist=h)
    rec("Mirror","counts only this month, this kind of thing, and only days done","That's 4 times this month you've reached out to someone." in t,t[:300].replace("\n"," | "))
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400); pg.evaluate("document.getElementById('jWeek').click()"); pg.wait_for_timeout(400); j=pg.inner_text("#modal"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    rec("Mirror","the Journal lists what you've done in the last five weeks","In these five weeks you've:" in j and "reached out to someone, 5 times" in j and "given something your full attention" in j,j[j.find("In these"):j.find("In these")+200].replace("\n"," | "))
    rec("Mirror","…with no junk text and no scores",not JUNK.search(j) and "score" not in j.lower())
    tabto(pg,"today")
    # shared world: find a day with a world event today
    found=False
    for i in range(12):
        day=(datetime.date(2026,12,1)+datetime.timedelta(days=i)).isoformat()
        t=scenario(pg,base,day,[("2026-11-15","daily")])
        if re.search(r"\bToday, ",t): found=True; break
    rec("World","on a day with a world event, the map line says it happened in every Forge",found and "It happened in every Forge at once." in t,day)
    if found:
        t=scenario(pg,base,(datetime.date.fromisoformat(day)+datetime.timedelta(days=1)).isoformat(),[("2026-11-15","daily")])
        rec("World","…and only on the day itself",("Yesterday, " not in t) or "every Forge" not in t)
    # 0.17.1: daily cards only, at most one echo a week, stable through the day
    t=scenario(pg,base,"2026-12-15",[("2026-11-15","pack")])
    rec("Echo","a pack find never echoes on its own",pg.locator("#view-today .echo").count()==0)
    t=scenario(pg,base,"2026-12-15",[("2026-11-15","daily")]); e1=st(pg).get("echo")
    rec("Echo","the day's echo is remembered in the save",bool(e1) and e1["date"]=="2026-12-15" and e1["lab"]=="A month ago today",e1)
    pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    rec("Echo","…and is the same after reopening the app that day",pg.locator("#view-today .echo").count()==1 and "Echo1" in pg.inner_text("#view-today .echo"))
    t=scenario(pg,base,"2026-12-18",[("2026-11-18","daily")],extra={"echo":{"date":"2026-12-15","id":999,"lab":"A month ago today"}})
    rec("Echo","three days after an echo, another anniversary stays quiet",pg.locator("#view-today .echo").count()==0)
    t=scenario(pg,base,"2026-12-22",[("2026-11-22","daily")],extra={"echo":{"date":"2026-12-15","id":999,"lab":"A month ago today"}})
    rec("Echo","a week after an echo, the next one may appear",pg.locator("#view-today .echo").count()==1)
    for junk in ("junk",{"date":5},{"date":"2026-12-01","id":"x","lab":"y"},[1,2]):
        t=scenario(pg,base,"2026-12-15",[("2026-11-15","daily")],extra={"echo":junk})
        rec("Echo",f"a damaged echo record ({str(junk)[:24]}) is repaired, not a crash",pg.locator("#view-today .echo").count()==1 and not pg._errs,pg._errs[:1])
    t=scenario(pg,base,"2026-12-10",[("2026-12-15","daily")],extra={"echo":{"date":"2027-01-01","id":1,"lab":"A month ago today"}})
    rec("Echo","an echo record from the future (clock moved back) is harmless",not pg._errs)
    # 0.17.1: relighting the Hearth survives closing the app mid-wake
    s=st(pg); s["hearth"]["sleep"]={"tier":1}; s["hearth"]["slots"]=[c["id"] for c in s["cards"][:2]]; w0=s["hearth"].get("welcomes",0); setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    tabto(pg,"hearth"); has=pg.locator("#hRelight").count()
    if has: pg.evaluate("document.getElementById('hRelight').click()"); pg.wait_for_timeout(400)
    pg.reload(); pg.wait_for_timeout(800); closemodals(pg); a=st(pg); tabto(pg,"hearth")
    rec("Hearth","relighting then closing the app at once still leaves everyone awake",has==1 and a["hearth"].get("sleep") is None and pg.locator("#hRelight").count()==0,(has,a["hearth"].get("sleep")))
    rec("Hearth","…and the welcome is counted exactly once",a["hearth"].get("welcomes",0)==w0+1,(w0,a["hearth"].get("welcomes")))
    s=st(pg); s["hearth"]["sleep"]={"tier":2}; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"hearth")
    pg.evaluate("document.getElementById('hRelight').click()"); pg.wait_for_timeout(9000); a=st(pg)
    rec("Hearth","a full, uninterrupted wake still ends awake with the welcome counted once",a["hearth"].get("sleep") is None and a["hearth"].get("welcomes",0)==w0+2 and "Everyone is awake" in pg.inner_text("#view-hearth"),(a["hearth"].get("welcomes"),))
    tabto(pg,"today")
    rec("All","no page errors in any scenario",not pg._errs,pg._errs[:2])
    ctx.close()
    # dark theme and dark mood render the echo legibly (axe covers contrast elsewhere); smoke test only
    ctx,pg=mk(b); pg.emulate_media(color_scheme="dark"); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); s["settings"]["mood"]="dark"; t=scenario(pg,s,"2026-12-15",[("2026-11-15","daily")])
    rec("Echo","dark appearance and dark mood: echo renders without errors",pg.locator("#view-today .echo").count()==1 and not pg._errs,pg._errs[:1])
    ctx.close(); b.close()
save_results("qa_17"); print(sum(r["ok"] for r in RES),"/",len(RES))
# ---- accessibility of the new states (axe-core): echo on Today, Second reading from an echo, the Journal list ----
try:
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
except Exception: AXE=None
if AXE:
    RES2=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); bad=[]
        for scheme in ("light","dark"):
            for mood in ("cute","dark"):
                ctx,pg=mk(b); pg.emulate_media(color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
                s=st(pg); s["settings"]["mood"]=mood
                h=[{"date":"2026-12-0"+str(i),"status":"done","v":4} for i in (2,5,8)]
                scenario(pg,s,"2026-12-15",[("2026-11-15","daily")],hist=h)
                def ax(label):
                    pg.evaluate(AXE); v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
                    bad.extend([f"{scheme}/{mood}/{label}: {x}" for x in v])
                ax("today with echo")
                pg.evaluate("document.querySelector('#view-today .echo [data-kept]').click()"); pg.wait_for_timeout(500); ax("second reading from echo"); closemodals(pg)
                pg.evaluate("()=>{const b=document.getElementById('keptBack');if(b)b.click();}"); pg.wait_for_timeout(300)
                tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400); ax("journal with mirror")
                ctx.close()
        b.close()
    rec("A11y","axe: zero violations on the echo, its Second reading, and the Journal list, light and dark, both moods",not bad,bad[:3])
    save_results("qa_17"); print(sum(r["ok"] for r in RES),"/",len(RES))
