from lib import *
import datetime
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
FAKE="""(()=>{const R=Date;let off=+(sessionStorage.getItem('__off')||localStorage.getItem('__off')||0);window.__setOff=v=>{off=v;sessionStorage.setItem('__off',String(v));localStorage.setItem('__off',String(v));};window.__real=()=>R.now();
class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"""
def mk(b,tz="America/New_York"):
    ctx=b.new_context(viewport={"width":390,"height":844},has_touch=True,is_mobile=True,timezone_id=tz,locale="en-US")
    pg=ctx.new_page(); pg._errs=[]; pg.on("pageerror",lambda e:pg._errs.append(str(e))); pg.add_init_script(FAKE); pg.set_default_timeout(7000); return ctx,pg
def setclock(pg,iso_local):
    # make "now" equal the given local wall-clock time in the page's timezone
    ms=pg.evaluate("(s)=>{const t=new Date(s).getTime();return t-window.__real();}",iso_local); pg.evaluate("(v)=>window.__setOff(v)",ms)
def hist_ok(h):
    ds=[x["date"] for x in h]; return len(ds)==len(set(ds)) and ds==sorted(ds)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg); ctx.close()
    # 1. midnight passes while the app is open
    ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    before=st(pg); d0=before["date"]; n0=len(before["cards"])
    ms=pg.evaluate("()=>{const n=new Date();const m=new Date(n.getFullYear(),n.getMonth(),n.getDate()+1);return m-n;}"); pg.evaluate("(v)=>window.__setOff(v)",ms-12000)
    pg.wait_for_timeout(45000)
    a=st(pg); rec("Clock","midnight passing with the app open starts a new day by itself",a["date"]!=d0 and a["status"]=="fresh" and a["todayCard"] is None,(d0,a["date"],a["status"]))
    rec("Clock","…keeping every card, and logging yesterday as done",len(a["cards"])==n0 and any(h["date"]==d0 and h["status"]=="done" for h in a["history"]) ,[h for h in a["history"] if h["date"]==d0])
    rec("Clock","…with no errors",not pg._errs,pg._errs[:1]); ctx.close()
    # 2. daylight saving, fall back (2026-11-01) and spring forward (2027-03-14)
    for label,start,now,expect in [("fall back","2026-10-30","2026-11-03T12:00:00",["2026-10-31","2026-11-01","2026-11-02"]),("spring forward","2027-03-12","2027-03-16T12:00:00",["2027-03-13","2027-03-14","2027-03-15"])]:
        ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
        pg.wait_for_timeout(1500); s=json.loads(json.dumps(base)); s["date"]=start; s["startDate"]=start; s["status"]="done"; s["history"]=[{"date":start,"status":"done","v":0}]; s["opens"]=[start]; s["offset"]=0; s["seen"]=18
        for c in s["cards"]: c["date"]=start
        setst(pg,s); setclock(pg,now); pg.reload(); pg.wait_for_timeout(1000); closemodals(pg)
        a=st(pg); dates=[h["date"] for h in a["history"]]
        rec("Clock",f"{label}: every calendar day appears exactly once in order, none skipped or doubled",hist_ok(a["history"]) and all(d in dates for d in expect),dates)
        lbl=pg.inner_text("#dateLabel"); want={"fall back":"Nov 3","spring forward":"Mar 16"}[label]
        rec("Clock",f"{label}: app shows the right date and no errors",a["date"]==now[:10] and not pg._errs and want in lbl,lbl)
        ctx.close()
    # 3. device clock set backwards, and a long absence
    ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); s["seen"]=18; setst(pg,s)
    pg.evaluate("(v)=>window.__setOff(v)",-3*86400e3); pg.reload(); pg.wait_for_timeout(900); closemodals(pg); a=st(pg)
    rec("Clock","a device clock moved back three days does not crash or corrupt the save",not pg._errs and isinstance(a["cards"],list) and len(a["cards"])>=1 and hist_ok(a["history"]),pg._errs[:1])
    rec("Clock","…and the day counter never shows zero or negative",bool(re.search(r"Day [1-9]",pg.inner_text("#dateLabel"))),pg.inner_text("#dateLabel"))
    pg.evaluate("(v)=>window.__setOff(v)",0); t0=time.time(); pg.reload(); pg.wait_for_timeout(900); closemodals(pg); rec("Clock","…and moving it forward again recovers",not pg._errs and st(pg)["cards"],pg._errs[:1])
    pg.evaluate("(v)=>window.__setOff(v)",400*86400e3); t0=time.time(); pg.reload(); pg.wait_for_selector(".tab",state="attached"); dt=time.time()-t0; pg.wait_for_timeout(700); closemodals(pg); a=st(pg)
    rec("Clock","a 400-day absence loads quickly, with a bounded history and the deepest sleep",dt<4 and not pg._errs and len(a["history"])<=90 and (a["hearth"].get("sleep") or {}).get("tier")==3,(round(dt,2),len(a["history"]),a["hearth"].get("sleep")))
    ctx.close()
    # 4. travelling to another time zone
    ctx,pg=mk(b,"Asia/Tokyo"); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); s=st(pg); s["seen"]=18; setst(pg,s); ctx.close()
    ctx,pg=mk(b,"America/Los_Angeles"); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    s=json.loads(json.dumps(base)); today_ny=pg.evaluate("()=>new Date().toLocaleDateString('en-CA')"); s["seen"]=18; s["date"]=(datetime.date.fromisoformat(today_ny)+datetime.timedelta(days=1)).isoformat(); s["opens"]=[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
    rec("Clock","opening after flying west (saved date is ahead of the local date) does not crash",not pg._errs and bool(st(pg)["cards"]),pg._errs[:1]); ctx.close()
    b.close()
save_results("qa_clock"); print(sum(r["ok"] for r in RES),"/",len(RES))
