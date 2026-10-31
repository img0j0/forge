from lib import *
# 0.45: relics and gifts. A realm relic is forged from a spare of each of the realm's four curios and 8 embers; it sits on
# a shelf by the fire and adds a closing line to the realm's old tale. Forged charms and Shade curios can be gifted.
import base64, datetime
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def dec(code): return json.loads(base64.urlsafe_b64decode(code+"="*(-len(code)%4)))
def goto_hash(pg,h):
    base=P.split("#")[0]; pg.goto("about:blank"); pg.goto(base+h); pg.wait_for_timeout(3000)
REALM={0:"acorn flower feather mushroom",1:"leaf spark bone crystal",2:"shell pebble rain coin",3:"snow moon bell glimmer",4:"key candle thread map",
       5:"thorn seed nest rosehip",6:"cinder obsidian ring ash",7:"bottle pearl anchor seaglass",8:"mitten stillstone icicle snowglass",9:"letter inkpot locket mirror"}
def rich(s,spare=2,days=30,lantern=True,made=()):
    c0=s["cards"][0]; cards=[]
    for i in range(6):
        c=json.loads(json.dumps(c0)); c.update(id=500+i,seed=4000+i*331,theme=i%5,dark=False); cards.append(c)
    cards[0]["nick"]="Pip"; s["cards"]=cards; s["hearth"]["slots"]=[500,501]; s["seen"]=99
    t=datetime.date.fromisoformat(s["date"]); s["history"]=[{"date":(t-datetime.timedelta(days=d)).isoformat(),"status":"done","v":0,"card":500,"note":"","allIn":False} for d in range(days,0,-1)]
    s["curios"]={k:{"n":spare,"cid":500,"at":s["date"]} for ks in REALM.values() for k in ks.split()}
    s["explore"]={str(i):4 for i in range(10)}; s["forge"]={"spent":0,"made":(["xlantern"] if lantern else [])+list(made),"log":{},"bell":"","comp":"","compTo":-1}
    return s
def load(pg,s): setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def forge(pg): closemodals(pg); tabto(pg,"hearth"); pg.evaluate("document.getElementById('hForge').click()"); pg.wait_for_timeout(450)
def hearthpx(pg): return pg.evaluate("document.getElementById('hearthCv').toDataURL()")
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # ---------- the recipe is visible, and says what it needs ----------
    s=rich(json.loads(json.dumps(base)),spare=1,lantern=False); load(pg,s); forge(pg); m=mt(pg)
    rec("Recipe","the Forge lists the five bright relics, with what each needs",all(f"Relic of {n}" in m for n in ["Meadow","Ember","Tide","Frost","Dusk"]) and "Needs a spare of each of Meadow’s four curios and 8 embers (you have spares of 0 of 4" in m,m[-400:])
    rec("Recipe","Shade relics wait for the lantern","Relic of Bramble" not in m)
    rec("Recipe","without the spares there is no Make button",pg.locator("[data-fmake='relic0']").count()==0)
    # ---------- forging a relic ----------
    s=rich(json.loads(json.dumps(base))); load(pg,s); before=hearthpx(pg); forge(pg); m=mt(pg)
    rec("Recipe","with the lantern, all ten relics are listed",all(f"Relic of {n}" in m for n in ["Meadow","Bramble","Void"]))
    v=axe(pg); rec("A11y","the Forge with relics has no accessibility violations",not v,v)
    rec("Make","with a spare of each Meadow curio and 8 embers, Make it appears",pg.locator("[data-fmake='relic0']").count()==1)
    pg.click("[data-fmake='relic0']"); pg.wait_for_timeout(700); m=mt(pg); s2=st(pg)
    rec("Make","the relic is forged and signed","Relic of Meadow" in m and "Forged by Pip" in m and "relic0" in s2["forge"]["made"],m[:200])
    rec("Make","it used exactly one of each Meadow curio and 8 embers, never the last copy",all(s2["curios"][k]["n"]==1 for k in REALM[0].split()) and s2["forge"]["spent"]==8 and all(s2["curios"][k]["n"]==2 for k in REALM[1].split()))
    rec("Make","the sheet says it sits by the fire and the tale has a closing line","on the shelf by the fire" in m and "closing line" in m)
    sm=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.getBoundingClientRect().height<44).map(b=>b.textContent.trim())"); rec("A11y","its buttons are 44-point targets",not sm,sm)
    pg.click("#modal [data-otale='0']"); pg.wait_for_timeout(500); m=mt(pg)
    rec("Tale","Read the closing line opens the tale at its last page, with the relic's line after the ending","Page 4 of 4" in m and "Somewhere a hill is glad someone stayed for the view" in m and m.find("It still grows at its own speed")<m.find("Somewhere a hill"),m[-300:])
    v=axe(pg); rec("A11y","the tale with its closing line has no accessibility violations",not v,v)
    closemodals(pg); tabto(pg,"hearth"); pg.wait_for_timeout(500); after=hearthpx(pg)
    rec("Hearth","the relic shows by the fire",before!=after)
    pg.evaluate("()=>{const x=document.createElement('button');x.dataset.realmopen=0;document.body.appendChild(x);x.click();x.remove()}"); pg.wait_for_timeout(500)
    rec("Map","the realm page says its relic is by your fire","Its relic is by your fire." in pg.inner_text(".realmpage"))
    # a second relic, from the other side
    forge(pg); pg.click("[data-fmake='relic5']"); pg.wait_for_timeout(700); closemodals(pg); s3=st(pg)
    rec("Make","a Shade relic forges the same way","relic5" in s3["forge"]["made"] and s3["forge"]["spent"]==16)
    forge(pg); rec("Make","a forged relic says who made it and stays made","Forged by Pip" in mt(pg) and pg.locator("[data-fmake='relic0']").count()==0)
    hsheet(pg,"keeps"); rec("Keep","relics are not offered as something a Forgeling wears","Relic" not in mt(pg),mt(pg)[:200])
    closemodals(pg)
    # ---------- sending a charm ----------
    s=rich(json.loads(json.dumps(base)),made=("charm1","ward2")); load(pg,s); forge(pg)
    rec("Gift","the Forge offers to send a charm you made",pg.locator("#fgGift").count()==1)
    pg.click("#fgGift"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Gift","the gift sheet has curios from both sides and the charms you forged","Send a gift to a friend" in m and pg.locator("#modal [data-gcur='charm1']").count()==1 and pg.locator("#modal [data-gcur='ward2']").count()==1 and pg.locator("#modal [data-gcur='thorn']").count()==1,m[:160])
    rec("Gift","a charm you forged is chosen first when you come from the Forge",pg.get_attribute("#modal [data-gcur='charm1']","aria-pressed")=="true")
    v=axe(pg); rec("A11y","the gift sheet has no accessibility violations",not v,v)
    pg.click("#giftGo"); pg.wait_for_timeout(700); clip=pg.evaluate("navigator.clipboard.readText()")
    mm=re.search(r"#gift=([A-Za-z0-9_-]+)",clip); code=mm.group(1) if mm else ""; g=dec(code) if code else {}
    rec("Gift","the message says it was forged, and the link carries the charm",("forged a charm of Ember" in clip) and g.get("v")==2 and g.get("f")=="charm1" and "c" not in g,(clip[:90],g))
    rec("Gift","you keep yours","charm1" in st(pg)["forge"]["made"])
    # a Shade curio
    hsheet(pg,"shelf"); pg.click("#hGift"); pg.wait_for_timeout(300); pg.click("#modal [data-gcur='thorn']"); pg.click("#giftGo"); pg.wait_for_timeout(700)
    clip2=pg.evaluate("navigator.clipboard.readText()"); code2=re.search(r"#gift=([A-Za-z0-9_-]+)",clip2).group(1); g2=dec(code2)
    rec("Gift","a Shade curio travels as a v2 link",g2.get("v")==2 and g2.get("c")=="thorn",g2)
    hsheet(pg,"shelf"); pg.click("#hGift"); pg.wait_for_timeout(300); pg.click("#modal [data-gcur='acorn']"); pg.click("#giftGo"); pg.wait_for_timeout(700)
    g3=dec(re.search(r"#gift=([A-Za-z0-9_-]+)",pg.evaluate("navigator.clipboard.readText()")).group(1))
    rec("Gift","a bright curio still travels as v1, so older copies open it",g3.get("v")==1 and g3.get("c")=="acorn",g3)
    ctx.close()
    # ---------- the friend ----------
    cB,B=newpage(b); B.goto(P); B.wait_for_selector("#titleGo"); first_card(B); closemodals(B); sB=st(B); sB["seen"]=99; sB["curios"]={}; load(B,sB)
    goto_hash(B,"#gift="+code); m=mt(B)
    rec("Receive","the friend sees the forged charm, who made it, and that anyone can wear it","Pip sent you something" in m and "Charm of Ember" in m and "Forged by Pip" in m and "can wear it" in m,m[:220])
    v=axe(B); rec("A11y","receiving a charm has no accessibility violations",not v,v)
    B.click("#giftKeep"); B.wait_for_timeout(600); m=mt(B); sB=st(B)
    rec("Receive","keeping it puts the charm in their Forge as a gift","charm1" in sB["forge"]["made"] and sB["forge"]["log"]["charm1"].get("gift")==1 and "Keepsakes" in m,m[:160])
    closemodals(B); forge(B); rec("Receive","their Forge says it was a gift from Pip","A gift from Pip" in mt(B))
    closemodals(B); goto_hash(B,"#gift="+code); rec("Receive","the same link opens once","Already opened" in mt(B) and "in your Forge" in mt(B)); closemodals(B)
    goto_hash(B,"#gift="+code2); B.click("#giftKeep"); B.wait_for_timeout(500); rec("Receive","a Shade curio arrives on the shelf","thorn" in st(B)["curios"]); closemodals(B)
    # tampered v2 links
    def enc(o): return base64.urlsafe_b64encode(json.dumps(o).encode()).decode().rstrip("=")
    for label,o in [("both curio and charm",dict(g,c="acorn",g="aaaaaa111111")),("a relic",dict(g,f="relic0",g="bbbbbb222222")),("a made-up charm",dict(g,f="charm9",g="cccccc333333")),("an unknown version",dict(g,v=3,g="dddddd444444"))]:
        goto_hash(B,"#gift="+enc(o)); t=B.evaluate("document.getElementById('toast').textContent")
        rec("Links",f"a link with {label} is refused politely",not mt(B) and "broken" in t,(mt(B)[:60],t))
    rec("All","no page errors",not B._errs,B._errs[:2]); cB.close()
    b.close()
save_results("qa_45"); print(sum(r["ok"] for r in RES),"/",len(RES))
