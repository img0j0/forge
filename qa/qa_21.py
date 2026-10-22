from lib import *
# 0.21.0: first impressions. The title scene and the age rules behind it, the home-screen icon,
# the first-day close, ribbon notes that wait their turn, the arrival and the greeting.
import datetime, base64
FAKE="""(()=>{const R=Date;let off=+(localStorage.getItem('__off')||0);window.__setOff=v=>{off=v;localStorage.setItem('__off',String(v));};window.__real=()=>R.now();
class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"""
def mk(b,w=390,h=844,scheme="light",reduce=None):
    kw=dict(color_scheme=scheme,timezone_id="America/New_York")
    if reduce: kw["reduced_motion"]="reduce"
    ctx,pg=newpage(b,w,h,**kw); pg.add_init_script(FAKE); pg.set_default_timeout(7000); return ctx,pg
def at(pg,hhmm):
    ms=pg.evaluate("(s)=>new Date(s).getTime()-window.__real()","2026-10-16T"+hhmm+":00"); pg.evaluate("(v)=>window.__setOff(v)",ms)
PX="()=>{const c=document.getElementById('titleCv');if(!c)return -1;const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n}"
def age(pg,m,y):
    pg.select_option("#ageM",str(m)); pg.select_option("#ageY",str(y)); pg.tap("#ageGo"); pg.wait_for_timeout(500)
with sync_playwright() as p:
    b=p.chromium.launch()
    # ---------- the title scene ----------
    ctx,pg=mk(b); pg.goto(P); at(pg,"12:00"); pg.reload(); pg.wait_for_selector("#titleGo")
    t=pg.inner_text("#modal")
    rec("Title","a new player first sees the Forgelings title, a tagline and Begin, not a form","Forgelings" in t and "One small thing a day" in t and pg.locator("#ageM").count()==0 and pg.is_visible("#titleGo"),t[:90])
    rec("Title","the scene is drawn",pg.evaluate(PX)>1000,pg.evaluate(PX))
    rec("Title","the dialog is named Forgelings for screen readers",pg.evaluate("()=>{const d=document.querySelector('#modal [role=dialog]');const id=d.getAttribute('aria-labelledby');return id?document.getElementById(id).textContent:d.getAttribute('aria-label')}")=="Forgelings")
    rec("Title","at noon on a light phone the scene is the day sky with dark lettering",pg.evaluate("document.querySelector('.scrim').classList.contains('lite')"))
    at(pg,"22:30"); pg.reload(); pg.wait_for_selector("#titleGo")
    rec("Title","at night it is the night sky with light lettering",not pg.evaluate("document.querySelector('.scrim').classList.contains('lite')"))
    pg.tap("#titleGo"); pg.wait_for_timeout(500); t=pg.inner_text("#modal")
    rec("Title","Begin brings up the same age question, inside the scene","Before we begin" in t and "we do not keep your birth date" in t and pg.is_visible("#ageM") and pg.locator("#titleCv").count()==1,t[-200:])
    rec("Title","…the month field gets focus and the scene lifts to make room",pg.evaluate("document.activeElement&&document.activeElement.id")=="ageM" and pg.evaluate("document.querySelector('.scrim').classList.contains('asking')"))
    pg.tap("#ageGo"); pg.wait_for_timeout(300)
    rec("Age","Continue with nothing chosen asks for a month and year and stays put","choose a month and a year" in pg.inner_text("#toast") and pg.is_visible("#ageM"))
    age(pg,6,1995); s=st(pg)
    rec("Age","an adult goes on to their first card, and the scene is gone",s["ageBand"]=="adult" and pg.locator("#titleCv").count()==0 and "Today's card" in mt(pg),mt(pg)[:60])
    rec("All","no page errors on the way in",not pg._errs,pg._errs[:2]); ctx.close()
    yr=datetime.date.today().year
    ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.tap("#titleGo"); pg.wait_for_timeout(300); age(pg,1,yr-15)
    rec("Age","while Forge is in testing, a 15-year-old sees the not-yet screen","not available for you" in mt(pg) and "adults only" in mt(pg),mt(pg)[:90]); ctx.close()
    ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.tap("#titleGo"); pg.wait_for_timeout(300); age(pg,1,yr-19)
    rec("Age","a 19-year-old is let in as an adult",st(pg)["ageBand"]=="adult"); ctx.close()
    ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.tap("#titleGo"); pg.wait_for_timeout(300); age(pg,12,yr-18)
    rec("Age","someone whose 18th birthday month has not finished yet is treated as 17 (we lean younger)","not available for you" in mt(pg),mt(pg)[:60]); ctx.close()
    ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.tap("#titleGo"); pg.wait_for_timeout(300); age(pg,3,yr-10)
    blocked=pg.evaluate("[localStorage.getItem('forge-age-block'),localStorage.getItem('forge-app-v1')]")
    rec("Age","a 10-year-old sees the not-yet screen and nothing about them is saved","not available for you" in mt(pg) and blocked[0] and blocked[1] is None,blocked)
    pg.reload(); pg.wait_for_timeout(800)
    rec("Age","…and reopening still shows the not-yet screen, not the title",("not available for you" in mt(pg)) and pg.locator("#titleGo").count()==0 and not pg._errs,pg._errs[:1]); ctx.close()
    # small, sideways and reduced motion
    for (w,h,label) in ((320,568,"a small phone"),(844,390,"a phone turned sideways")):
        ctx,pg=mk(b,w,h); pg.goto(P); pg.wait_for_selector("#titleGo")
        bb=pg.locator("#titleGo").bounding_box(); ok1=bb and bb["y"]+bb["height"]<=h and bb["x"]>=0 and bb["x"]+bb["width"]<=w
        pg.tap("#titleGo"); pg.wait_for_timeout(500); pg.locator("#ageGo").scroll_into_view_if_needed(); cb=pg.locator("#ageGo").bounding_box()
        ok2=cb and cb["y"]>=0 and cb["y"]+cb["height"]<=h
        hs=pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
        rec("Title",f"on {label} ({w}x{h}) Begin and Continue are on screen with no sideways scrolling",ok1 and ok2 and not hs,(bb,cb,hs)); ctx.close()
    ctx,pg=mk(b,reduce=True); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.wait_for_timeout(300)
    a=pg.evaluate(PX); pg.wait_for_timeout(600); same=pg.evaluate("()=>{const c=document.getElementById('titleCv');return c.toDataURL()}")==pg.evaluate("()=>document.getElementById('titleCv').toDataURL()")
    rec("Title","with reduced motion the scene is drawn and holds still",a>1000 and same); ctx.close()
    # ---------- the icon ----------
    ctx,pg=mk(b); pg.goto(P); pg.wait_for_selector("#titleGo")
    ic=pg.evaluate("""async()=>{const l=document.querySelector('link[rel=apple-touch-icon]');if(!l)return null;const im=new Image();im.src=l.href;await im.decode();return [im.naturalWidth,im.naturalHeight]}""")
    fav=pg.evaluate("""async()=>{const l=document.querySelector('link[rel=icon]');if(!l)return null;const im=new Image();im.src=l.href;await im.decode();return im.naturalWidth}""")
    tc=pg.evaluate("[...document.querySelectorAll('meta[name=theme-color]')].map(m=>m.content+'|'+m.media)")
    rec("Icon","a 180-pixel home-screen icon and a small browser icon are built in",ic==[180,180] and fav==64,(ic,fav))
    rec("Icon","the phone's bar colour follows light and dark",len(tc)==2 and any("dark" in x for x in tc),tc)
    rec("Icon","the home-screen name is Forgelings",pg.evaluate("document.querySelector('meta[name=apple-mobile-web-app-title]').content")=="Forgelings")
    ctx.close()
    # ---------- the first minute ----------
    ctx,pg=mk(b); pg.goto(P); at(pg,"19:00"); pg.reload(); pg.wait_for_selector("#titleGo")
    pg.tap("#titleGo"); pg.wait_for_selector("#ageM",state="visible"); age(pg,6,1995)
    pg.tap("#vBack"); pg.wait_for_selector("#vDoneNow",state="visible"); pg.tap("#vDoneNow"); pg.wait_for_selector("#cover",state="visible")
    toasts=[]
    pg.tap("#cover");
    for _ in range(8): pg.wait_for_timeout(250); toasts.append(pg.evaluate("document.getElementById('toast').classList.contains('show')?document.getElementById('toast').textContent:''"))
    rec("First day","no ribbon note pops up over the reveal",not any("ribbon" in x for x in toasts),toasts)
    pg.wait_for_selector("#rvSkip",state="visible"); pg.tap("#rvSkip")
    over=[]
    for _ in range(9): pg.wait_for_timeout(200); over.append(pg.evaluate("document.getElementById('toast').classList.contains('show')?document.getElementById('toast').textContent:''"))
    rec("First day","no ribbon note pops up over the first-day note either",not any("ribbon" in x for x in over),over)
    m=mt(pg)
    nm=st(pg)["cards"][0]["name"]
    rec("First day","the first day closes with one note: who joined, what happens tomorrow, and something to try now","That’s your first day" in m and nm in m and "A new card arrives tomorrow" in m and "wander" in m and pg.locator("#modal #fdHearth").count()==1 and pg.locator("#modal [data-time]").count()==0,m[:200])
    seen=[]
    pg.evaluate("document.querySelector('#modal [data-close]').click()")
    for _ in range(10): pg.wait_for_timeout(200); seen.append(pg.inner_text("#toast") if pg.evaluate("document.getElementById('toast').classList.contains('show')") else "")
    rec("First day","…and the First Spark ribbon note comes after it, once nothing else is on screen",any("New ribbon: First Spark" in x for x in seen),seen)
    # ---------- the greeting and the arrival ----------
    lbl=pg.inner_text("#dateLabel")
    rec("Greeting","Today greets you for the time of day, before the day count",lbl.startswith("Good evening · Day 1,"),lbl)
    tabto(pg,"binder")
    rec("Greeting","other tabs show just the day",pg.inner_text("#dateLabel").startswith("Day 1,"),pg.inner_text("#dateLabel"))
    tabto(pg,"today")
    for hh,g in (("07:30","Good morning"),("14:00","Good afternoon"),("23:30","Hello, night owl")):
        at(pg,hh); pg.reload(); pg.wait_for_timeout(500); closemodals(pg)
        rec("Greeting",f"at {hh} it says {g}",pg.inner_text("#dateLabel").startswith(g),pg.inner_text("#dateLabel"))
    at(pg,"14:00"); pg.reload(); pg.wait_for_timeout(150)
    a1=pg.evaluate("document.body.classList.contains('arrive')"); pg.wait_for_timeout(1500); a2=pg.evaluate("document.body.classList.contains('arrive')")
    rec("Arrival","opening the app plays the gentle arrival once, then settles",a1 and not a2,(a1,a2))
    pg.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))}")
    at(pg,"14:20"); pg.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))}"); pg.wait_for_timeout(100)
    rec("Arrival","coming back after a while plays it again",pg.evaluate("document.body.classList.contains('arrive')"))
    pg.wait_for_timeout(1500)
    pg.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))}")
    at(pg,"14:22"); pg.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))}"); pg.wait_for_timeout(100)
    rec("Arrival","…but not after a quick glance away",not pg.evaluate("document.body.classList.contains('arrive')"))
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    ctx,pg=mk(b,reduce=True); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); pg.reload(); pg.wait_for_timeout(150)
    rec("Arrival","with reduced motion there is no arrival animation",not pg.evaluate("document.body.classList.contains('arrive')")); ctx.close()
    # ---------- accessibility ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        for hh in ("12:00","22:30"):
            ctx,pg=mk(b,scheme=scheme); pg.goto(P); at(pg,hh); pg.reload(); pg.wait_for_selector("#titleGo")
            for where in ("title","age"):
                if where=="age": pg.tap("#titleGo"); pg.wait_for_timeout(500)
                pg.wait_for_function("document.getAnimations().filter(a=>a.playState==='running'&&a.effect&&a.effect.getComputedTiming().iterations!==Infinity).length===0",timeout=5000)
                pg.evaluate(AXE); v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
                bad+=[f"{scheme}/{hh}/{where}: {x}" for x in v]
            ctx.close()
    rec("A11y","axe: zero violations on the title and the age question, day and night, light and dark",not bad,bad[:3])
    b.close()
save_results("qa_21"); print(sum(r["ok"] for r in RES),"/",len(RES))
