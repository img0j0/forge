from lib import *
# 0.25.2: Play opens a chooser where any Forgeling by the fire can play any of the five games. (Was 0.25.1's
# realm-locked chooser.) Played with real taps.
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
TITLES=["Dandelion Drift","Keep the Fire","Skipping Stones","Snowflake Catch","Lantern Lights"]
def ready(pg,s):
    pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click();const d=document.getElementById('pgDone');if(d)d.click()}"); pg.wait_for_timeout(200)
    setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg); tabto(pg,"hearth")
def rows(pg): return pg.evaluate("[...document.querySelectorAll('#modal [data-game]')].map(e=>[e.querySelector('b').textContent,+e.dataset.game,+e.dataset.cid,e.innerText])")
def who(pg): return pg.evaluate("[...document.querySelectorAll('#modal [data-gwho]')].map(e=>[+e.dataset.gwho,e.getAttribute('aria-pressed')])")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b,390,844); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # Only Frost Forgelings: three of them, two by the fire
    s=build(base,[0,0,0,3,0]); s["seen"]=99; cs=s["cards"]; A,B,C=cs[0],cs[1],cs[2]
    A["stats"]=[20,30,90]; B["stats"]=[90,40,20]; B["dark"]=True
    s["hearth"]["slots"]=[A["id"],B["id"]]; s["hearth"]["visits"]={"date":s["date"],"used":0}; s["games"]={"best":{"tide":7},"played":0,"curioDay":""}
    ready(pg,s)
    rec("Hearth","the Hearth says Play opens any of the five games","Play any of the five games" in pg.inner_text("#view-hearth"))
    pg.tap("#hPlay"); pg.wait_for_timeout(400); r=rows(pg)
    rec("Chooser","with Forgelings from only one realm, all five games are open",len(r)==5 and sorted(x[0].replace("Home","") for x in r)==sorted(TITLES) and pg.locator("#modal .gwait").count()==0,[x[0] for x in r])
    rec("Chooser","the selected Forgeling's own realm game is first, marked Home, and has focus",r[0][1]==3 and "Home" in r[0][0] and sum("Home" in x[0] for x in r)==1 and pg.evaluate("document.activeElement.dataset.game")=="3")
    rec("Chooser","every game is played by the selected Forgeling, and shows the best score",all(x[2]==A["id"] for x in r) and "Best: 7 skips" in [x for x in r if x[1]==2][0][3])
    w=who(pg); rec("Who","you can choose who plays from the Forgelings by the fire",w==[[A["id"],"true"],[B["id"],"false"]],w)
    small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.getBoundingClientRect().height<44).map(b=>b.textContent.slice(0,20))")
    rec("Chooser","every choice is easy to tap",not small,small)
    pg.tap(f"#modal [data-gwho='{B['id']}']"); pg.wait_for_timeout(300); r=rows(pg); w=who(pg)
    rec("Who","tapping another Forgeling switches who plays every game",all(x[2]==B["id"] for x in r) and w[1][1]=="true" and w[0][1]=="false",w)
    # a Frost Forgeling plays Dandelion Drift, with its own stats and, being dark, that game's twist
    pg.tap("#modal [data-game='0']"); pg.wait_for_timeout(400); rd=pg.inner_text("#pgReady")
    rec("Play","a Frost Forgeling can play Dandelion Drift",pg.locator("#pgReady").count()==1 and "Dandelion Drift" in mt(pg))
    rec("Play","…its Start card uses its own stats and the game's twist (Bramble for Dandelion Drift)","Dread 40:" in rd and "Bramble twist:" in rd,rd[:200])
    pg.tap("#pgGo"); pg.wait_for_timeout(200); pg.tap("#pgSit"); pg.wait_for_timeout(400); s2=st(pg)
    bB=[c for c in s2["cards"] if c["id"]==B["id"]][0]; bA=[c for c in s2["cards"] if c["id"]==A["id"]][0]
    rec("Play","the visit counts and the bond goes to the Forgeling who played",s2["hearth"]["visits"]["used"]==1 and bB["bond"]==1 and bA["bond"]==0,(s2["hearth"]["visits"],bA["bond"],bB["bond"]))
    # traits follow the player: A (Calm 90) gets wider calm water in Skipping Stones than B (Calm 20)
    def calm(cid):
        s3=st(pg); s3["hearth"]["visits"]={"date":s3["date"],"used":0}; ready(pg,s3); pg.tap("#hPlay"); pg.wait_for_timeout(300)
        if pg.locator(f"#modal [data-gwho='{cid}']").count(): pg.tap(f"#modal [data-gwho='{cid}']"); pg.wait_for_timeout(250)
        pg.tap("#modal [data-game='2']"); pg.wait_for_timeout(300); pg.tap("#pgGo"); pg.wait_for_timeout(200)
        wd=pg.evaluate("document.getElementById('pgCalm').getBoundingClientRect().width"); closemodals(pg); pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click()}"); pg.wait_for_timeout(300); return wd
    wa,wb=calm(A["id"]),calm(B["id"])
    rec("Play","traits follow whoever plays: high Calm widens the calm water for any Forgeling",wa>wb*1.15,(round(wa),round(wb)))
    # Play again keeps the chosen game
    s3=st(pg); s3["hearth"]["visits"]={"date":s3["date"],"used":3}; ready(pg,s3); pg.tap("#hPlay"); pg.wait_for_timeout(300)
    rec("Free","with visits used up, the chooser says the games are just for fun","just for fun" in mt(pg))
    pg.tap("#modal [data-game='3']"); pg.wait_for_timeout(300); pg.tap("#pgGo")
    pg.wait_for_function("!!document.getElementById('pgAgain')",timeout=30000); pg.tap("#pgAgain"); pg.wait_for_timeout(300)
    rec("Free","Play again replays the same game you chose","Snowflake Catch" in mt(pg) and pg.locator("#pgReady").count()==1)
    closemodals(pg); pg.evaluate("()=>{const b=document.getElementById('pgSit');if(b)b.click()}"); pg.wait_for_timeout(300)
    # a wandering Forgeling can't be chosen
    s4=st(pg); s4["wander"]={"id":A["id"],"start":0,"ready":9e15,"realm":3}; s4["hearth"]["visits"]={"date":s4["date"],"used":0}; ready(pg,s4)
    pg.evaluate(f"()=>{{const b=document.querySelector('[data-hslot=\"1\"]');if(b)b.click()}}"); pg.wait_for_timeout(200); pg.tap("#hPlay"); pg.wait_for_timeout(300)
    rec("Who","a Forgeling out wandering is not offered",all(x[0]!=A["id"] for x in who(pg)) and all(x[2]==B["id"] for x in rows(pg)),(who(pg),rows(pg)[:1]))
    closemodals(pg)
    # accessibility, light and dark
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); bad=[]
    for scheme in ("light","dark"):
        c2,p2=newpage(b,430,932,color_scheme=scheme); p2.goto(P); p2.wait_for_selector("#titleGo"); first_card(p2); closemodals(p2)
        setst(p2,s); p2.reload(); p2.wait_for_timeout(800); closemodals(p2); tabto(p2,"hearth"); p2.tap("#hPlay"); p2.wait_for_timeout(500)
        p2.wait_for_function("document.getAnimations().filter(a=>a.playState==='running'&&a.effect&&a.effect.getComputedTiming().iterations!==Infinity).length===0",timeout=5000)
        p2.evaluate(AXE); bad+=[f"{scheme}: {v}" for v in p2.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")]
        rec("All",f"{scheme}: no page errors",not p2._errs,p2._errs[:1]); c2.close()
    rec("A11y","axe: zero violations on the game chooser, light and dark",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_251"); print(sum(r["ok"] for r in RES),"/",len(RES))
