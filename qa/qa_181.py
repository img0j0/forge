from lib import *
# 0.18.1: the living sky. 0.46: the field journal replaced the drawn sky; the same setting now chooses the page (paper by day,
# lamplit at dusk, night or Dark), so these checks read the page instead of the sky's colour.
FAKE="""(()=>{const R=Date;let off=+(localStorage.getItem('__off')||sessionStorage.getItem('__off')||0);window.__setOff=v=>{off=v;sessionStorage.setItem('__off',String(v));localStorage.setItem('__off',String(v));};window.__real=()=>R.now();
class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"""
# 0.35.1 (Living Sky): the Light sky is now vivid (SKYV), so its top colours changed.
TOP={("light","dawn"):"day",("light","day"):"day",("light","dusk"):"lamp",("light","night"):"lamp",
     ("dark","dawn"):"lamp",("dark","day"):"lamp",("dark","dusk"):"lamp",("dark","night"):"lamp"}
def hexrgb(h): return h
def top(pg): return pg.evaluate("()=>document.documentElement.getAttribute('data-page')")
def setclock(pg,iso):
    ms=pg.evaluate("(s)=>new Date(s).getTime()-window.__real()",iso); pg.evaluate("(v)=>window.__setOff(v)",ms)
def mk(b,scheme):
    ctx,pg=newpage(b,390,844,color_scheme=scheme,timezone_id="America/New_York"); pg.add_init_script(FAKE); pg.set_default_timeout(7000); return ctx,pg
with sync_playwright() as p:
    b=p.chromium.launch()
    for scheme in ("light","dark"):
        ctx,pg=mk(b,scheme); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
        for ph,hh in (("dawn","06:10"),("day","12:00"),("dusk","18:30"),("night","22:30")):
            setclock(pg,"2026-12-10T"+hh+":00"); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
            got=top(pg); rec("Sky",f"{scheme}: at {hh} the sky is {ph}",got==hexrgb(TOP[(scheme,ph)]),(got,TOP[(scheme,ph)]))
        v=pg.evaluate("()=>[getComputedStyle(document.body).backgroundColor,document.getElementById('skyCv').hidden]")
        rec("Sky",f"{scheme}: the journal sits on the desk, and the old sky is not drawn",v[0] in ("rgb(59, 42, 34)","rgb(20, 15, 12)") and v[1],v)
        rec("Sky",f"{scheme}: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    # settings
    ctx,pg=mk(b,"light"); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    setclock(pg,"2026-12-10T22:30:00"); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    rec("Setting","a fresh save defaults to following your day",st(pg)["settings"].get("sky")=="auto",st(pg)["settings"].get("sky"))
    tabto(pg,"settings"); t=pg.inner_text("#view-settings")
    rec("Setting","Settings offers the four page choices",all(x in t for x in ("Follows your day","Always day","Always lamplit","Plain")))
    pg.evaluate("document.querySelector('[data-setsky=\"day\"]').click()"); pg.wait_for_timeout(300)
    rec("Setting","Always day shows the day sky at night, straight away",top(pg)==hexrgb(TOP[("light","day")]) and st(pg)["settings"]["sky"]=="day",top(pg))
    rec("Setting","…and the chip shows as chosen",pg.evaluate("document.querySelector('[data-setsky=\"day\"]').getAttribute('aria-pressed')")=="true")
    pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    rec("Setting","…and it is remembered after reopening",top(pg)==hexrgb(TOP[("light","day")]))
    setclock(pg,"2026-12-10T12:00:00"); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"settings")
    pg.evaluate("document.querySelector('[data-setsky=\"night\"]').click()"); pg.wait_for_timeout(300)
    rec("Setting","Always lamplit shows the lamplit page at noon",top(pg)==hexrgb(TOP[("light","night")]),top(pg))
    pg.evaluate("document.querySelector('[data-setsky=\"plain\"]').click()"); pg.wait_for_timeout(300)
    bg=pg.evaluate("getComputedStyle(document.body).backgroundColor")
    rec("Setting","Plain hides the sky and shows the plain background",top(pg) is None and bg=="rgb(241, 237, 248)",bg)
    pg.evaluate("document.querySelector('[data-settheme=\"dark\"]').click()"); pg.wait_for_timeout(300)
    rec("Setting","…Plain stays plain when switching to dark",top(pg) is None)
    pg.evaluate("document.querySelector('[data-setsky=\"auto\"]').click()"); pg.wait_for_timeout(300)
    rec("Setting","choosing Dark appearance with a living sky gives the dark sky",top(pg)==hexrgb(TOP[("dark","day")]),top(pg))
    pg.evaluate("document.querySelector('[data-settheme=\"light\"]').click()"); pg.wait_for_timeout(300)
    rec("Setting","…and switching back to Light redraws it light",top(pg)==hexrgb(TOP[("light","day")]),top(pg))
    # the day turning while the app is open
    setclock(pg,"2026-12-10T16:59:30"); pg.reload(); pg.wait_for_timeout(700); closemodals(pg); a=top(pg)
    setclock(pg,"2026-12-10T17:01:00"); pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(300)
    rec("Live","coming back to the app after 5pm turns day into dusk without a reload",a==hexrgb(TOP[("light","day")]) and top(pg)==hexrgb(TOP[("light","dusk")]),(a,top(pg)))
    pg.set_viewport_size({"width":844,"height":390}); pg.wait_for_timeout(500)
    rec("Live","turning the phone sideways keeps the page centred with no sideways scroll",pg.evaluate("()=>document.documentElement.scrollWidth<=innerWidth&&document.querySelector('.app').getBoundingClientRect().width<=460"))
    pg.set_viewport_size({"width":390,"height":844}); pg.wait_for_timeout(300)
    # damaged settings
    for bad in ("bogus",5,None,{"x":1}):
        s=st(pg); s["settings"]["sky"]=bad; setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
        rec("Damaged",f"a damaged sky setting ({bad!r}) is repaired to following your day",st(pg)["settings"].get("sky")=="auto" and top(pg) is not None and not pg._errs,pg._errs[:1])
    s=st(pg); del s["settings"]["sky"]; setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
    rec("Damaged","an older save with no sky setting gets the living sky",st(pg)["settings"].get("sky")=="auto" and top(pg) is not None)
    # reduced motion: the sky never animates, so nothing to stop; check it does not redraw on its own while hidden
    rec("All","no page errors",not pg._errs,pg._errs[:2])
    ctx.close(); b.close()
save_results("qa_181"); print(sum(r["ok"] for r in RES),"/",len(RES))
