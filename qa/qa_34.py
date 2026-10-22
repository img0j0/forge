from lib import *
# 0.34.0: a favourite Forgeling on Today (after each day's new find), and campfire card backs. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def load(pg,s):
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def do_day(pg):
    tabto(pg,"today"); pg.tap("#btnTurnGo"); pg.wait_for_selector("#vBack",state="visible"); pg.tap("#vBack"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{const o=document.getElementById('vOk');o&&o.click()}"); pg.wait_for_timeout(300); pg.tap("#btnDone"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{const m=[...document.querySelectorAll('#modal [data-mood]')].find(b=>/mix/i.test(b.textContent));m&&m.click()}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{const c=document.getElementById('cover');c&&c.click()}"); pg.wait_for_selector("#rvSkip",state="visible",timeout=8000); pg.tap("#rvSkip"); pg.wait_for_timeout(1500)
    for _ in range(4):
        if not mt(pg): break
        pg.evaluate("()=>{const b=document.querySelector('#modal [data-close]')||document.getElementById('rvDone');b&&b.click()}"); pg.wait_for_timeout(500)
def hero(pg): return pg.inner_text("#view-today .hero")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    dev(pg,"week"); closemodals(pg); s=st(pg); fav=s["cards"][0]; fname=fav.get("nick") or fav["name"]
    # ---------- campfire backs ----------
    tabto(pg,"binder"); pg.evaluate(f"()=>{{const c=document.querySelector('#view-binder .card[data-cid=\"{fav['id']}\"]')||document.querySelector('#view-binder .card');c&&c.click()}}"); pg.wait_for_timeout(700)
    pg.evaluate("document.getElementById('inspFlip').click()"); pg.wait_for_timeout(900)
    cb=pg.evaluate("(()=>{const e=document.querySelector('#stage .cbk');const cs=getComputedStyle(e);return {bg:cs.backgroundImage.slice(0,60),emb:!!e.querySelector('.emb'),txt:e.innerText,info:!!e.querySelector('.binfo')}})()")
    rec("Back","every card back wears the campfire art",'svg' in cb["bg"] and cb["info"] and not cb["emb"],cb)
    rec("Back","the old FORGE wordmark is gone, the card's details remain","FORGE" not in cb["txt"] and ("Earned" in cb["txt"] or "Pulled" in cb["txt"]) and "No." in cb["txt"],cb["txt"][:120])
    bad+=["back: "+v for v in axe(pg)]
    # ---------- choosing a favourite ----------
    pg.evaluate("document.getElementById('inspFlip').click()"); pg.wait_for_timeout(400)
    cid_shown=pg.evaluate("+document.querySelector('#stage .card').dataset.cid"); fav=[c for c in st(pg)["cards"] if c["id"]==cid_shown][0]; fname=fav.get("nick") or fav["name"]
    rec("Pick","a card offers Show on Today",pg.locator("#inspHome").is_visible() and pg.inner_text("#inspHome")=="Show on Today")
    pg.tap("#inspHome"); pg.wait_for_timeout(300)
    rec("Pick","tapping it makes this Forgeling the one on Today",st(pg)["homeFav"]==fav["id"] and pg.get_attribute("#inspHome","aria-pressed")=="true" and "On Today" in pg.inner_text("#inspHome"))
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    # ---------- today's find first, then the favourite ----------
    do_day(pg); tabto(pg,"today"); h=hero(pg); find=[c for c in st(pg)["cards"] if c["id"]==st(pg)["todayCard"]][0]; findn=find.get("nick") or find["name"]
    rec("Today","today's new find shows first",f"{findn} joined your binder" in h and pg.locator("#btnShowToday").count()==1,h[:120])
    rec("Today","…with a one-tap way to bring the favourite back",pg.locator("#btnFavBack").count()==1 and f"Show {fname} here" in h)
    tabto(pg,"hearth"); tabto(pg,"today"); h=hero(pg)
    rec("Today","after leaving Today, the favourite keeps you company there",f"{fname} is keeping you company" in h and f"Today’s find, {findn}, is in your binder" in h and pg.locator("#btnShowFav").count()==1,h[:160])
    bad+=["today: "+v for v in axe(pg)]
    pg.tap("#btnSeeFind"); pg.wait_for_timeout(300)
    rec("Today","See today's find brings the find back",f"{findn} joined your binder" in hero(pg))
    pg.tap("#btnFavBack"); pg.wait_for_timeout(300)
    rec("Today","…and Show here returns to the favourite",f"{fname} is keeping you company" in hero(pg))
    pg.reload(); pg.wait_for_timeout(900); closemodals(pg); tabto(pg,"today")
    rec("Today","reopening the app the same day keeps the favourite",f"{fname} is keeping you company" in hero(pg))
    pg.tap("#btnShowFav"); pg.wait_for_timeout(600)
    rec("Today","tapping the favourite opens its card",ovm:=pg.evaluate("document.getElementById('modal').innerText.includes('Flip card')"))
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    # ---------- the next day ----------
    dev(pg,"next"); closemodals(pg); tabto(pg,"today")
    rec("Next day","a new day starts with today's card, as before",pg.locator("#btnTurnGo").count()==1 and "keeping you company" not in hero(pg))
    do_day(pg); tabto(pg,"today")
    rec("Next day","the new day's find shows first again",pg.locator("#btnShowToday").count()==1 and "joined your binder" in hero(pg))
    # ---------- rest days ----------
    dev(pg,"next"); closemodals(pg); tabto(pg,"today"); pg.tap("#btnTurnGo"); pg.wait_for_selector("#vBack",state="visible"); pg.tap("#vBack"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{const o=document.getElementById('vOk');o&&o.click()}"); pg.wait_for_timeout(300); pg.tap("#btnRest"); pg.wait_for_timeout(500); closemodals(pg)
    rec("Rest","on a rest day the favourite sits on Today",pg.locator("#view-today #btnShowFav").count()==1 and "Resting today" in hero(pg))
    # ---------- unpicking, and no favourite at all ----------
    s=st(pg); s["homeFav"]=None; load(pg,s); tabto(pg,"today")
    rec("None","with no favourite, Today is exactly as before",pg.locator("#btnShowFav,#btnFavBack,#btnSeeFind").count()==0)
    s=st(pg); s["homeFav"]=987654; load(pg,s); tabto(pg,"today")
    rec("None","a favourite that no longer exists is simply ignored",pg.locator("#btnShowFav,#btnFavBack").count()==0 and not pg._errs)
    s=st(pg); s["homeFav"]="x"; s["findSeen"]=5; load(pg,s); s=st(pg)
    rec("Damaged","broken favourite data is repaired","homeFav" not in s or s["homeFav"] is None or isinstance(s["homeFav"],int))
    rec("A11y","axe: zero violations on the card back and the favourite on Today",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_34"); print(sum(r["ok"] for r in RES),"/",len(RES))
