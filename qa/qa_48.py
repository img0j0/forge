from lib import *
import datetime
# 0.48: ink and paper, moving. The pack is a sealed envelope; a new Forgeling is pencilled, inked, coloured and stamped,
# the same way for every rarity; kept cards drift into the Binder ribbon; embers roll up on the Hearth; the Forge stamps
# MADE; a new place is inked onto the map. A tap skips, Plain keeps the old look, and reduced motion keeps it all still.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def days(s,n):
    d=datetime.date.fromisoformat(s["startDate"]); have={h["date"] for h in s["history"]}; k=1
    while n>0:
        x=(d-datetime.timedelta(days=k)).isoformat(); k+=1
        if x in have: continue
        s["history"].append({"date":x,"status":"done","v":0}); n-=1
def load(pg,s): s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def click(pg,sel): pg.evaluate("s=>document.querySelector(s).click()",sel)
def start(b,hr=11,**kw):
    ctx,pg=newpage(b,**kw); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,hr,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); return ctx,pg
ANIM="(s)=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e);return c.animationName+' '+c.animationDuration+' '+c.animationDelay}"
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for hr in (11,22):
        tag="day" if hr==11 else "lamp"
        ctx,pg=start(b,hr)
        # ---------- the envelope ----------
        dev(pg,"pack"); pg.wait_for_timeout(400)
        env=pg.evaluate("()=>{const b=document.getElementById('packTear');return {env:!!b.querySelector('svg.jenv .e-seal'),old:!!b.querySelector('#pkg'),label:b.getAttribute('aria-label'),h:b.getBoundingClientRect().height,page:document.querySelector('#modal .scrim').classList.contains('jinsp')}}")
        hint=pg.inner_text("#modal .rv-hint")
        rec("Envelope",f"{tag}: the pack is a sealed envelope on a journal page",env["env"] and not env["old"] and env["page"] and hint=="Press the seal to open it",(env,hint))
        rec("Envelope",f"{tag}: it is a button named for what it does, 44 points or more",env["label"].startswith("An envelope holding 5") and env["h"]>=44,env)
        if hr==11: bad+=["envelope: "+v for v in axe(pg)]
        click(pg,"#packTear"); pg.wait_for_timeout(120)
        mid=pg.evaluate("()=>{const b=document.getElementById('packTear');return b&&b.classList.contains('opening')}")
        click(pg,"#packTear"); pg.wait_for_timeout(120)
        rec("Envelope",f"{tag}: pressing the seal opens it, and a second tap skips straight to the cards",mid and pg.locator("#modal #cover").count()==1 and "Card 1 of 5" in mt(pg),mt(pg)[:40])
        # ---------- the inked reveal, the same for all five ----------
        same=[];stamps=[];sparks=0
        for i in range(5):
            if i: click(pg,"#packNext"); pg.wait_for_timeout(250)
            click(pg,"#cover"); pg.wait_for_timeout(60)
            g=pg.evaluate(ANIM,"#stage .jghost"); s_=pg.evaluate(ANIM,"#stage .jrstamp")
            same.append((g,s_)); stamps.append(pg.evaluate("()=>{const s=document.querySelector('#stage .jrstamp b'),st=document.querySelector('#stage .stars');return [s&&s.textContent,st&&st.getAttribute('aria-label')]}"))
            if i==0:
                rec("Ink",f"{tag}: turning a card over pencils it in (a copy of the face, hidden from screen readers)",g is not None and g.startswith("jghost") and pg.evaluate("document.querySelector('#stage .jghost').getAttribute('aria-hidden')")=="true",g)
                pg.wait_for_timeout(1700)
                rec("Ink",f"{tag}: once coloured in, the pencil copy is gone and the stamp stays",pg.locator("#stage .jghost").count()==0 and pg.locator("#stage .jrstamp").count()==1)
                if hr==11: bad+=["reveal: "+v for v in axe(pg)]
            elif i==1:
                pg.tap("#stage .card"); pg.wait_for_timeout(60)
                rec("Ink",f"{tag}: a tap while it is being inked finishes it at once",pg.locator("#stage .jghost").count()==0 and pg.evaluate("document.querySelector('#stage .jrstamp').classList.contains('jnow')"))
                pg.wait_for_timeout(500)
            else: pg.wait_for_timeout(1700)
            sparks+=pg.locator("#stage .spark").count()
        rec("Ink",f"{tag}: every card is revealed with the same timing, whatever its rarity",all(x==same[0] for x in same) and same[0][0] is not None,same[0])
        rec("Ink",f"{tag}: the stamp names each card's own rarity",all(a and q and a==q.upper() for a,q in stamps),stamps)
        rec("Ink",f"{tag}: no rarity sparks in the journal (the stamp is the moment)",sparks==0,sparks)
        # ---------- into the binder: a pack ----------
        click(pg,"#packNext"); pg.wait_for_timeout(400); click(pg,"#packDone"); pg.wait_for_timeout(80)
        fly=pg.locator(".jfly").count(); pg.wait_for_timeout(700)
        plus=pg.evaluate("()=>{const p=document.querySelector('.jplus');return p&&p.textContent}"); dip=pg.evaluate("document.querySelector('.tab[data-tab=\"binder\"]').classList.contains('jdip')")
        rec("Binder",f"{tag}: the pack drifts into the Binder ribbon, which dips with +5",fly==1 and plus=="+5" and dip,(fly,plus,dip))
        pg.wait_for_timeout(1500)
        rec("Binder",f"{tag}: and it all tidies away",pg.locator(".jfly,.jplus").count()==0 and not pg.evaluate("document.querySelector('.tab[data-tab=\"binder\"]').classList.contains('jdip')"))
        # ---------- embers roll ----------
        tabto(pg,"hearth"); pg.wait_for_timeout(1500)
        s=st(pg); days(s,3); s["curios"]["acorn"]={"n":3,"cid":0,"at":s["date"]}; load(pg,s); tabto(pg,"hearth")
        r=pg.evaluate("()=>{const h=document.getElementById('hEmbers'),j=h.querySelector('.jroll');return {roll:!!j,add:j&&j.dataset.add,tc:h.textContent,it:h.innerText}}")
        rec("Embers",f"{tag}: new embers roll up on the Hearth with a +N",r["roll"] and r["add"]=="+3" and r["tc"]==r["it"] and re.fullmatch(r"\d+ embers?",r["tc"]) is not None,r)
        pg.wait_for_timeout(1600); tabto(pg,"today"); tabto(pg,"hearth")
        rec("Embers",f"{tag}: once seen, they do not roll again",pg.locator("#hEmbers .jroll").count()==0)
        # ---------- the Forge stamps it ----------
        pg.tap("#hForge"); pg.wait_for_timeout(500); mk=pg.locator("#modal [data-fmake]")
        if mk.count():
            mk.first.scroll_into_view_if_needed(); mk.first.tap(); pg.wait_for_timeout(800)
            j=pg.evaluate("()=>{const m=document.querySelector('#modal .jmade');return m&&{vis:getComputedStyle(m).display!=='none',t:m.innerText,ah:m.getAttribute('aria-hidden')}}")
            rec("Forge",f"{tag}: a finished piece is stamped MADE and signed",j and j["vis"] and j["t"].startswith("MADE") and "signed," in j["t"] and j["ah"]=="true",j)
            if hr==22: bad+=["made at night: "+v for v in axe(pg)]
        else: rec("Forge",f"{tag}: something to make",False)
        closemodals(pg)
        # ---------- a place is inked onto the map ----------
        tabto(pg,"chronicle"); pg.wait_for_timeout(1500)
        first=pg.locator(".mp-place.jnew").count()
        s=st(pg); ti=s["cards"][0]["theme"]; s["explore"]=s.get("explore") or {}; s["explore"][str(ti)]=(s["explore"].get(str(ti)) or 0)+1; load(pg,s); tabto(pg,"chronicle")
        n=pg.locator(".mp-place.jnew").count(); rg=pg.locator(".mp-ring").count()
        rec("Map",f"{tag}: a newly found place is inked onto the map (and nothing moves the first time you look)",first==0 and n==1 and rg==1,(first,n,rg))
        rec("All",f"{tag}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()

    # ---------- a daily find drifts into the binder (+1) ----------
    ctx,pg=newpage(b); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,11,30)); pg.goto(P); pg.wait_for_selector("#titleGo")
    pg.tap("#titleGo"); pg.wait_for_selector("#ageM",state="visible"); pg.select_option("#ageM","6"); pg.select_option("#ageY","1995"); pg.tap("#ageGo")
    pg.tap("#vBack"); pg.wait_for_selector("#vDoneNow",state="visible"); pg.tap("#vDoneNow"); pg.wait_for_selector("#cover",state="visible")
    rec("Reveal","the daily reveal opens on a journal page",pg.evaluate("document.querySelector('#modal .scrim').classList.contains('jinsp')"))
    pg.tap("#cover"); pg.wait_for_timeout(1700); pg.tap("#rvName"); pg.wait_for_timeout(500); pg.tap("#saveNames"); pg.wait_for_timeout(80)
    fly=pg.locator(".jfly").count(); pg.wait_for_timeout(650)
    rec("Binder","naming today's find sends it to the Binder ribbon with +1",fly==1 and pg.evaluate("()=>{const p=document.querySelector('.jplus');return p&&p.textContent}")=="+1")
    rec("All","daily: no page errors",not pg._errs,pg._errs[:2]); ctx.close()

    # ---------- Plain keeps the old pack and the sparks ----------
    ctx,pg=start(b); s=st(pg); s["settings"]["sky"]="plain"; load(pg,s)
    dev(pg,"pack"); pg.wait_for_timeout(400)
    rec("Plain","with the Plain page the pack is the old foil pack",pg.locator("#packTear svg.jenv").count()==0 and pg.locator("#packTear #pkg").count()==1 and "tear it open" in mt(pg))
    click(pg,"#packTear"); pg.wait_for_timeout(900); click(pg,"#cover"); pg.wait_for_timeout(80)
    rec("Plain","…and the reveal has no pencil copy or stamp",pg.locator("#stage .jghost,#stage .jrstamp").count()==0 and not pg.evaluate("document.querySelector('#modal .scrim').classList.contains('jinsp')"))
    rec("All","plain: no page errors",not pg._errs,pg._errs[:2]); ctx.close()

    # ---------- reduced motion: nothing moves, the stamp is simply there ----------
    ctx,pg=start(b,reduced_motion="reduce"); dev(pg,"pack"); pg.wait_for_timeout(400)
    click(pg,"#packTear"); pg.wait_for_timeout(750)
    rec("Motion","with reduced motion the envelope opens straight to the cards",pg.locator("#modal #cover").count()==1)
    click(pg,"#cover"); pg.wait_for_timeout(80)
    rec("Motion","…no pencil copy, and the stamp is already down",pg.locator("#stage .jghost").count()==0 and pg.evaluate("()=>{const s=document.querySelector('#stage .jrstamp');return !!s&&s.classList.contains('jnow')&&getComputedStyle(s).animationName==='none'}"))
    for i in range(4): click(pg,"#packNext"); pg.wait_for_timeout(200); click(pg,"#cover"); pg.wait_for_timeout(500)
    click(pg,"#packNext"); pg.wait_for_timeout(300); click(pg,"#packDone"); pg.wait_for_timeout(60)
    rec("Motion","…and nothing flies to the binder",pg.locator(".jfly,.jplus").count()==0)
    rec("All","reduced: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    rec("A11y","axe: the envelope, the inked reveal and the stamped Forge piece have no violations",not bad,bad[:4])
    b.close()
save_results("qa_48"); print(sum(r["ok"] for r in RES),"/",len(RES))
