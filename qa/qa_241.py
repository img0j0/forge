from lib import *
# 0.24.1: soft music is on by default until the player turns it off.
HOOK="""(()=>{window.__mus=0;const P=(window.AudioContext||window.webkitAudioContext).prototype,o=P.createDelay;P.createDelay=function(){window.__mus++;return o.apply(this,arguments);};})();"""
def chip(pg): tabto(pg,"settings"); return pg.get_attribute("#setMusic","aria-pressed"),pg.inner_text("#setMusic")
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    ctx,pg=newpage(b); pg.add_init_script(HOOK); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); pg.wait_for_timeout(800)
    rec("Music","a new player starts with soft music on in Settings",chip(pg)==("true","Soft music on"),chip(pg))
    rec("Music","…and the music really starts once they've tapped",pg.evaluate("window.__mus")>=1,pg.evaluate("window.__mus"))
    rec("Music","nothing is written until they choose",st(pg)["settings"].get("music") is None,st(pg)["settings"].get("music"))
    pg.evaluate("document.getElementById('setMusic').click()"); pg.wait_for_timeout(300)
    rec("Music","one tap turns it off and remembers that",chip(pg)==("false","Soft music off") and st(pg)["settings"]["music"] is False)
    pg.reload(); pg.wait_for_timeout(800); closemodals(pg); n0=pg.evaluate("window.__mus"); pg.tap("body"); pg.wait_for_timeout(600)
    rec("Music","after reopening, it stays off",chip(pg)[0]=="false" and pg.evaluate("window.__mus")==n0==0,(chip(pg),pg.evaluate("window.__mus")))
    pg.evaluate("document.getElementById('setMusic').click()"); pg.wait_for_timeout(500)
    rec("Music","another tap turns it back on, and it plays",chip(pg)==("true","Soft music on") and st(pg)["settings"]["music"] is True and pg.evaluate("window.__mus")>=1)
    s=st(pg); s["settings"].pop("music",None); setst(pg,s); pg.reload(); pg.wait_for_timeout(800); closemodals(pg)
    rec("Music","a save from before 0.24.1 that never touched music now has it on",chip(pg)[0]=="true")
    s=st(pg); s["settings"]["sound"]=False; s["settings"].pop("music",None); setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg); pg.tap("body"); pg.wait_for_timeout(600)
    rec("Music","with all sound off, no music plays",pg.evaluate("window.__mus")==0,pg.evaluate("window.__mus"))
    rec("All","no page errors",not pg._errs,pg._errs[:1]); ctx.close(); b.close()
save_results("qa_241"); print(sum(r["ok"] for r in RES),"/",len(RES))
