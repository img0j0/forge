from lib import *
# 0.27.1: gaps from the full walkthrough. One realm name everywhere; no nudge promise; first-day note points to the
# Hearth; copy fixes. Played with real taps.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
REALMS={"Meadow","Ember","Tide","Frost","Dusk","Bramble","Inferno","Abyss","Wraith","Void"}
def fresh_load(pg,s):
    setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)
def vis(pg): return pg.evaluate("document.querySelector('.app').innerText")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,390,844); pg.goto(P); pg.wait_for_selector("#titleGo")
    # ---------- the first day, as a new player ----------
    pg.tap("#titleGo"); pg.wait_for_selector("#ageM",state="visible"); pg.select_option("#ageM","6"); pg.select_option("#ageY","1995"); pg.tap("#ageGo")
    pg.tap("#vBack"); pg.wait_for_selector("#vDoneNow",state="visible"); pg.tap("#vDoneNow"); pg.wait_for_selector("#cover",state="visible"); pg.tap("#cover")
    pg.wait_for_selector("#rvSkip",state="visible"); pg.tap("#rvSkip"); pg.wait_for_selector("#fdHearth",state="visible",timeout=8000)
    m=mt(pg); nm=st(pg)["cards"][0]["name"]
    rec("First day","the first-day note says who joined and suggests a first wander",nm in m and "send "+nm+" out to wander" in m and "20 minutes" in m,m[:240])
    rec("First day","…and makes no nudge promise","nudge" not in m.lower() and "Nothing is sent" not in m and pg.locator("#modal [data-time]").count()==0)
    small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.getBoundingClientRect().height<44).map(b=>b.textContent)")
    rec("First day","its buttons are easy to tap",not small,small)
    pg.tap("#fdHearth"); pg.wait_for_timeout(600)
    rec("First day","Go to the Hearth closes the note and opens the Hearth",not mt(pg) and pg.evaluate("document.querySelector('.tab[data-tab=\"hearth\"]').getAttribute('aria-current')")=="page" and pg.locator("#hWander").is_visible(),pg.evaluate("document.querySelector('.tab[aria-current]')?.dataset.tab"))
    # ---------- copy ----------
    seen=[]
    for t in ["today","hearth","binder","chronicle","settings"]:
        tabto(pg,t); seen.append(vis(pg))
    tabto(pg,"chronicle")
    for sub in ["tales","journal"]:
        pg.evaluate(f"()=>document.querySelector('[data-sub=\"{sub}\"]').click()"); pg.wait_for_timeout(300); seen.append(vis(pg))
    pg.evaluate("document.getElementById('jWeek').click()"); pg.wait_for_timeout(300); seen.append(mt(pg)); closemodals(pg)  # 0.43: This week opens as a sheet
    allt="\n".join(seen)
    rec("Copy","no player text says Chronicle","Chronicle" not in allt,[l for l in allt.split("\n") if "Chronicle" in l][:3])
    rec("Copy","no Morning nudge setting and no 'Prototype only' notes","Morning nudge" not in allt and "Prototype only" not in allt and pg.locator("[data-setnudge]").count()==0)
    rec("Copy","the lore switch is called Whispers and tales","Whispers and tales on" in allt)
    rec("Copy","the journal on day 1 says 'You showed up today.'","You showed up today." in allt and "of the last 1 day" not in allt)
    tales=seen[5]
    rec("Copy","with no curios yet, the Tales tab says how to find pages once, not five times",tales.count("Send a Forgeling")==0 and tales.count("Your first wander starts at the Hearth.")==1 and tales.count("0 of 4 pages")==5,tales[:300])
    rec("Copy","no undefined, NaN or null on any tab",not JUNK.search(allt),JUNK.findall(allt)[:3])
    # ---------- one name per realm ----------
    base=st(pg)
    for mood in ("mix","dark","cute"):
        s=build(base,[1,0,0,0,0],(0,),mood); s["wander"]=None; s["curios"]={}; s["explore"]={}; s["seen"]=99
        s["hearth"]["visits"]={"date":s["date"],"used":0}; fresh_load(pg,s); openmap(pg)
        mapn=[l for l in mapinfo(pg)["labels"] if l in REALMS]
        tabto(pg,"hearth"); pg.tap("#hWander"); pg.wait_for_timeout(400)
        sheet=pg.evaluate("[...document.querySelectorAll('#modal [data-wgo] b')].map(b=>b.textContent)")
        pg.tap("#modal [data-wgo='0']"); pg.wait_for_timeout(500); hmsg=pg.inner_text("#view-hearth")
        s2=st(pg); s2["wander"]["ready"]=0; fresh_load(pg,s2); tabto(pg,"hearth")
        pg.evaluate("()=>{const b=[...document.querySelectorAll('#view-hearth button')].find(b=>/welcome|see what/i.test(b.textContent));b&&b.click()}"); pg.wait_for_timeout(900)
        ret=mt(pg); bare=pg.evaluate("()=>{const m=document.getElementById('modal').cloneNode(true);m.querySelectorAll('.world,h2').forEach(e=>e.remove());return m.innerText}")
        names_in_ret={w for w in re.findall(r"[A-Z][a-z]+",bare) if w in REALMS}
        closemodals(pg); tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"tales\"]').click()"); pg.wait_for_timeout(300)
        tl=pg.inner_text("#view-chronicle"); first_tale=re.search(r"(\w+)\. \d of 4 pages",tl)
        n0=mapn[0] if mapn else None
        rec("Names",f"{mood}: map, wander sheet, Hearth, return, tale and place all use one name ({n0})",
            n0 and sheet[0]==n0 and f"toward {n0}" in hmsg+pg.evaluate("document.getElementById('toast').textContent") or (n0 and sheet[0]==n0 and n0 in hmsg),(mapn,sheet,hmsg[:120]))
        rec("Names",f"{mood}: the return sheet names only that realm",names_in_ret=={n0} and f"Back from {n0}" in ret and f"map of {n0}" in ret and f"old {n0} tale" in ret,(names_in_ret,ret[:300]))
        rec("Names",f"{mood}: the Tales tab names the tale's realm the same way",first_tale and first_tale.group(1)==n0,first_tale and first_tale.group(0))
    # ---------- the return toast doesn't sit on an open sheet ----------
    s3=st(pg); s3["wander"]={"id":s3["cards"][0]["id"],"start":0,"ready":pg.evaluate("Date.now()")+2000,"realm":0}; fresh_load(pg,s3); tabto(pg,"settings")
    pg.tap("#btnOdds"); pg.wait_for_timeout(300)
    toasts=[]
    for _ in range(115): pg.wait_for_timeout(200); toasts.append(pg.evaluate("document.getElementById('toast').classList.contains('show')?document.getElementById('toast').textContent:''"))
    rec("Toast","no 'back from wandering' toast over an open sheet",mt(pg) and not any("back from wandering" in t for t in toasts) and st(pg)["wander"].get("notified")==True,toasts)
    closemodals(pg)
    # ---------- accessibility of the first-day note ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        c2,p2=newpage(b,390,844,color_scheme=scheme); p2.goto(P); p2.wait_for_selector("#titleGo")
        p2.tap("#titleGo"); p2.wait_for_selector("#ageM",state="visible"); p2.select_option("#ageM","6"); p2.select_option("#ageY","1995"); p2.tap("#ageGo")
        p2.tap("#vBack"); p2.wait_for_selector("#vDoneNow",state="visible"); p2.tap("#vDoneNow"); p2.wait_for_selector("#cover",state="visible"); p2.tap("#cover")
        p2.wait_for_selector("#rvSkip",state="visible"); p2.tap("#rvSkip"); p2.wait_for_selector("#fdHearth",state="visible",timeout=8000)
        p2.wait_for_function("document.getAnimations().filter(a=>a.playState==='running'&&a.effect&&a.effect.getComputedTiming().iterations!==Infinity).length===0",timeout=5000)
        p2.evaluate(AXE); bad+=[f"{scheme}: {v}" for v in p2.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")]
        rec("All",f"{scheme}: no page errors",not p2._errs,p2._errs[:1]); c2.close()
    rec("A11y","axe: zero violations on the first-day note, light and dark",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_271"); print(sum(r["ok"] for r in RES),"/",len(RES))
