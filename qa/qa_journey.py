from lib import *
# A long, realistic run: ~4 months of days played only through taps a person would make.
# Mixes doing, going all in, resting, skipping single days and multi-day gaps; opens packs, visits the Hearth,
# sends wanderers, writes journal lines, follows echoes; checks the save stays consistent every day.
import random
# 0.44.1: over file:// this Chromium sometimes drops all of localStorage across the journey's many reloads (0.43.0 too),
# so the journey serves the build over local http, as the live app is served.
if P.startswith("file://"):
    import http.server, threading, functools
    _d,_f=os.path.split(P[len("file://"):])
    _srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=_d))
    _srv.RequestHandlerClass.log_message=lambda *a:None
    threading.Thread(target=_srv.serve_forever,daemon=True).start(); P=f"http://127.0.0.1:{_srv.server_address[1]}/{_f}"
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
FAKE="""(()=>{const R=Date;let off=+(localStorage.getItem('__off')||sessionStorage.getItem('__off')||0);window.__setOff=v=>{off=v;sessionStorage.setItem('__off',String(v));localStorage.setItem('__off',String(v));};window.__real=()=>R.now();
class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"""
DAYS=int(os.environ.get("JOURNEY_DAYS","125")); SEED=int(os.environ.get("JOURNEY_SEED","7"))
rng=random.Random(SEED)
def vis(pg,sel): return pg.evaluate("s=>{const e=document.querySelector(s);return !!(e&&!e.hidden&&e.offsetParent!==null)}",sel)
def click(pg,sel): pg.evaluate("s=>document.querySelector(s).click()",sel); pg.wait_for_timeout(260)
def settle(pg,limit=24):
    """Answer whatever dialog is open, the way a person would, until none is left."""
    for _ in range(limit):
        if pg.evaluate("document.getElementById('modal').hidden"): return True
        for sel in ["#cover","#rvSkip","#skipNames","[data-mood]","#packTear","#packNext","#packDone","#nudgeOk","#keptBack","#vBack","#vOk","[data-close]","#ovClose"]:
            if vis(pg,sel):
                click(pg,sel);
                if sel in("#cover","#packTear"): pg.wait_for_timeout(900)
                break
        else:
            pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
    return pg.evaluate("document.getElementById('modal').hidden")
problems=[]; returned_to_hearth=[]; echo_days=[]
def bad(day,msg):
    problems.append(f"{day}: {msg}")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,timezone_id="America/New_York",locale="en-US"); pg.add_init_script(FAKE); pg.set_default_timeout(8000)
    def go(day):
        ms=pg.evaluate("(s)=>new Date(s).getTime()-window.__real()",day+"T"+rng.choice(["08:10","12:30","19:45","22:20"])+":00"); pg.evaluate("(v)=>window.__setOff(v)",ms); pg.reload(); pg.wait_for_timeout(700)
    pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo")
    start=datetime.date(2026,10,20); go(start.isoformat()); first_card(pg); settle(pg)
    day=start; played=0; echoes=0; packs_opened=0; visits=0; wanders=0; collected=0; journal=0; rests=0; gaps=0; mirrors=0; relights=0
    while (day-start).days<DAYS:
        r=rng.random()
        if r<0.08: day+=datetime.timedelta(days=rng.choice([3,4,6])); gaps+=1
        elif r<0.20: day+=datetime.timedelta(days=2)
        else: day+=datetime.timedelta(days=1)
        k=day.isoformat(); go(k); settle(pg)
        if pg.evaluate("!document.getElementById('view-hearth').hidden") and vis(pg,"#hRelight"): returned_to_hearth.append(k)
        tabto(pg,"today")
        if pg._errs: bad(k,"page error "+pg._errs[-1]); pg._errs.clear()
        s=st(pg)
        if s["date"]!=k: bad(k,f"app date {s['date']}")
        if s["status"]!="fresh": bad(k,"new day did not start fresh: "+s["status"])
        # the day's calling
        a=rng.random()
        if vis(pg,"#btnTurn"):
            click(pg,"#btnTurn"); click(pg,"#vBack"); pg.wait_for_timeout(600); settle(pg)
            if a<0.12: click(pg,"#btnRest"); rests+=1
            elif vis(pg,"#btnDone"):
                click(pg,"#btnAll" if a>0.85 else "#btnDone"); pg.wait_for_timeout(500); settle(pg); played+=1
                t=pg.inner_text("#view-today")
                if "this month you've" in t: mirrors+=1
                else: bad(k,"no mirror line after doing the calling")
        else: bad(k,"no Turn over button on a fresh day")
        # echo
        if pg.locator("#view-today .echo").count():
            echoes+=1; echo_days.append(day); et=pg.inner_text("#view-today .echo")
            if JUNK.search(et): bad(k,"junk in echo: "+et)
            click(pg,"#view-today .echo [data-kept]"); m=pg.evaluate("document.getElementById('modal').innerText")
            if "Second reading" not in m: bad(k,"echo did not open a Second reading")
            settle(pg)
        # packs
        while vis(pg,"#btnPack"):
            n0=len(st(pg)["cards"]); click(pg,"#btnPack"); settle(pg,40); packs_opened+=1
            if len(st(pg)["cards"])!=n0+5: bad(k,"a pack did not add five cards")
            tabto(pg,"today")
        # journal, some days
        if rng.random()<0.35 and vis(pg,"#btnMargin"):
            click(pg,"#btnMargin"); pg.wait_for_timeout(300); pg.fill("#jIn",f"Line for {k}"); click(pg,"#jSave"); journal+=1
        # hearth
        if rng.random()<0.6:
            tabto(pg,"hearth")
            if vis(pg,"#hRelight"): click(pg,"#hRelight"); pg.wait_for_timeout(2500); settle(pg); relights+=1
            if pg.evaluate("!!document.querySelector('#view-hearth #hearthCv')") and vis(pg,"#hSnack") and pg.evaluate("!document.getElementById('hSnack').disabled"):
                click(pg,"#hSnack")
                if vis(pg,"[data-snack]"): click(pg,"[data-snack]"); visits+=1
                settle(pg)
            if vis(pg,"#hStory") and pg.evaluate("!document.getElementById('hStory').disabled"):
                click(pg,"#hStory")
                if vis(pg,"#storyIn"): pg.fill("#storyIn","A small story"); click(pg,"#storySave"); visits+=1
                settle(pg)
            if vis(pg,"#hCollect"): click(pg,"#hCollect"); settle(pg); collected+=1
            if vis(pg,"#hWander") and rng.random()<0.5:
                click(pg,"#hWander")
                opts=pg.evaluate("[...document.querySelectorAll('#modal [data-wgo]')].map(b=>b.dataset.wgo)")
                if opts:
                    rq=st(pg).get("request"); pick=str(rq["realm"]) if rq and str(rq["realm"]) in opts and rng.random()<0.7 else rng.choice(opts)
                    pg.evaluate("v=>document.querySelector('#modal [data-wgo=\"'+v+'\"]').click()",pick); pg.wait_for_timeout(250)
                wanders+=1 if st(pg).get("wander") else 0
            tabto(pg,"today")
        # consistency of the save
        s=st(pg); hist=s["history"]; ds=[h["date"] for h in hist]
        if len(ds)!=len(set(ds)) or ds!=sorted(ds): bad(k,"history out of order or doubled")
        done=sum(1 for h in hist if h["status"]=="done")
        if s["progress"]+5*(s["packs"]+s["packsOpened"])!=done: bad(k,f"pack progress mismatch done={done} progress={s['progress']} packs={s['packs']} opened={s['packsOpened']}")
        if len({c['id'] for c in s["cards"]})!=len(s["cards"]): bad(k,"duplicate card ids")
        if (day-start).days%15<2:
            for t in ("today","binder","chronicle","hearth","settings"):
                tabto(pg,t); txt=pg.inner_text("#view-"+t)
                if JUNK.search(txt): bad(k,f"junk text on {t}: "+JUNK.search(txt).group(0))
            tabto(pg,"chronicle")
            for sub in ("tales","journal","map"):
                pg.evaluate("s=>{const b=document.querySelector('[data-sub=\"'+s+'\"]');if(b)b.click();}",sub); pg.wait_for_timeout(300)
                txt=pg.inner_text("#view-chronicle")
                if JUNK.search(txt): bad(k,f"junk text on map/{sub}")
            tabto(pg,"today")
        if pg._errs: bad(k,"page error "+pg._errs[-1]); pg._errs.clear()
    final=st(pg)
    rec("Journey",f"{DAYS} days of real use (seed {SEED}) with no errors and a consistent save",not problems,problems[:4])
    rec("Journey","every day the calling was done, the mirror line appeared",played>0 and mirrors==played,(played,mirrors))
    rec("Journey","echoes appeared on anniversaries and opened their Second reading",echoes>=3,echoes)
    gapsE=[(b2-a2).days for a2,b2 in zip(echo_days,echo_days[1:])]
    rec("Journey","echoes stay occasional: never two within a week",all(g>=7 for g in gapsE) and echoes<=DAYS//7+1,(echoes,min(gapsE) if gapsE else None))
    rec("Journey","packs earned along the way all opened with five cards",packs_opened>=3,packs_opened)
    rec("Journey","Hearth visits, wanderers and curios all worked",visits>=10 and wanders>=3 and collected>=1,(visits,wanders,collected))
    rec("Journey","returning after a gap opens the sleeping Hearth first, and it can be woken",gaps==0 or (len(returned_to_hearth)>=1 and relights>=1),(gaps,len(returned_to_hearth),relights))
    print("summary",dict(days=DAYS,played=played,rests=rests,gaps=gaps,echoes=echoes,packs=packs_opened,visits=visits,wanders=wanders,collected=collected,journal=journal,cards=len(final["cards"]),by_fire=len((final.get("hearth") or {}).get("fseen") or []),requests_done=final.get("reqDone",0),keepsakes=len(final.get("keepsR") or [])))
    # back up and restore through the Settings screen
    tabto(pg,"settings"); click(pg,"#btnExport"); exp=pg.input_value("#expText"); settle(pg)
    pg.evaluate("k=>localStorage.removeItem(k)",KEY); pg.reload(); pg.wait_for_timeout(600)
    if vis(pg,"#titleGo"): click(pg,"#titleGo"); pg.wait_for_timeout(300)
    if vis(pg,"#ageGo"): pg.select_option("#ageM","6"); pg.select_option("#ageY","1995"); click(pg,"#ageGo")
    settle(pg); tabto(pg,"settings"); click(pg,"#btnRestore"); pg.fill("#resText",exp); click(pg,"#doRestore"); click(pg,"#doRestore"); pg.wait_for_timeout(600); settle(pg)
    after=st(pg)
    rec("Journey","a full backup restores every card, the journal and the history",len(after["cards"])==len(final["cards"]) and after["journal"]==final["journal"] and len(after["history"])==len(final["history"]),(len(after["cards"]),len(final["cards"])))
    rec("Journey","…with no page errors",not pg._errs,pg._errs[:1])
    b.close()
save_results(f"qa_journey{SEED}"); print(sum(r["ok"] for r in RES),"/",len(RES))
