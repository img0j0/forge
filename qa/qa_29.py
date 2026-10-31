from lib import *
# 0.29.0: gift links. A curio travels to a friend inside a link; played with real taps on both phones.
import base64, urllib.parse
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
def load(pg,s):
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def openshelf(pg):
    hsheet(pg,"shelf"); pg.wait_for_timeout(200)
def enc(o): return base64.urlsafe_b64encode(json.dumps(o).encode()).decode().rstrip("=")
def dec(code): return json.loads(base64.urlsafe_b64decode(code+"="*(-len(code)%4)))
def goto_hash(pg,h):
    base=P.split("#")[0]; pg.goto("about:blank"); pg.goto(base+h); pg.wait_for_timeout(3000)
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    # ---------- the sender ----------
    cA,A=newpage(b); A.goto(P); A.wait_for_selector("#titleGo"); first_card(A); closemodals(A); base=st(A)
    s=build(base,[2,0,0,0,0]); s["seen"]=99; ids=[c["id"] for c in s["cards"]]; s["hearth"]["slots"]=ids; s["curios"]={"acorn":{"n":1,"cid":ids[0],"at":s["date"]},"mushroom":{"n":2,"cid":ids[0],"at":s["date"]}}
    s["cards"][1]["nick"]="Pip"; load(A,s); openshelf(A)
    rec("Send","the curio shelf has a send-a-gift button",A.locator("#hGift").is_visible())
    A.tap("#hGift"); A.wait_for_timeout(400); m=mt(A)
    rec("Send","the sheet offers who sends it, your curios, and an optional note","Send a gift to a friend" in m and A.locator("[data-gsw]").count()==2 and A.locator("[data-gcur]").count()==2 and A.locator("#giftNote").count()==1,m[:200])
    rec("Send","it says plainly what the link holds","holds only the gift" in m)
    small=A.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.getBoundingClientRect().height<44).map(b=>b.textContent.trim().slice(0,20))")
    rec("Send","every choice is easy to tap",not small,small)
    bad+=["send: "+v for v in axe(A)]
    A.tap(f"[data-gsw='{ids[1]}']"); A.tap("[data-gcur='mushroom']"); A.fill("#giftNote","This one glows. <b>hi</b>")
    A.tap("#giftGo"); A.wait_for_timeout(700)
    clip=A.evaluate("navigator.clipboard.readText()")
    mm=re.search(r"#gift=([A-Za-z0-9_-]+)",clip); code=mm.group(1) if mm else ""
    rec("Send","sending copies a friendly message with a gift link","Pip found a moonlit mushroom and wants you to have it" in clip and clip.startswith("Pip") and "https://img0j0.github.io/forge/#gift=" in clip,clip[:160])
    g=dec(code) if code else {}
    rec("Send","the link holds only the gift, the sender's name and look, the note and two random ids",set(g)=={"v","g","s","c","n","t","d","r","e","k","m"} and g["c"]=="mushroom" and g["n"]=="Pip" and g["m"]=="This one glows. <b>hi</b>",g)
    sA=st(A); rec("Send","you keep your curio, and the send is counted",sA["curios"]["mushroom"]["n"]==2 and sA.get("giftsSent")==1 and isinstance(sA.get("sid"),str))
    A.wait_for_timeout(1200); rec("Send","the Kind Gesture ribbon is earned","gift1" in (st(A).get("ribbons") or {}) or "gift1" in json.dumps(st(A).get("ribbons")),str(st(A).get("ribbons"))[:120])
    # opening your own link
    goto_hash(A,"#gift="+code); m=mt(A)
    rec("Self","opening your own gift link just says it is yours","This is your own gift" in m and st(A)["curios"]["mushroom"]["n"]==2,m[:100])
    rec("Self","the gift part of the address is cleared after reading",A.evaluate("location.hash")=="")
    closemodals(A)
    # ---------- a friend who already plays ----------
    cB,B=newpage(b); B.goto(P); B.wait_for_selector("#titleGo"); first_card(B); closemodals(B); sB=st(B); sB["seen"]=99; sB["curios"]={}; load(B,sB)
    goto_hash(B,"#gift="+code); m=mt(B)
    rec("Receive","the friend sees who sent it, what it is, and the note","Pip sent you something" in m and "Moonlit mushroom" in m and "This one glows. <b>hi</b>" in m,m[:200])
    rec("Receive","the note is shown as plain text, never as markup",B.locator("#modal .giftnote b").count()==0)
    rec("Receive","the sender's Forgeling is drawn",B.evaluate("(()=>{const i=document.querySelector('#modal .gfrom img');return !!i&&i.src.startsWith('data:image')})()"))
    bad+=["receive: "+v for v in axe(B)]
    B.tap("#giftKeep"); B.wait_for_timeout(600); m=mt(B); sB=st(B)
    rec("Receive","keeping it puts the curio on the shelf and shows its tale page","mushroom" in sB["curios"] and "on your shelf" in m and "A page of an old" in m,m[:200])
    rec("Receive","the gift is remembered so it opens once",len(sB.get("giftsGot",[]))==1)
    closemodals(B); B.wait_for_timeout(1200)
    rec("Receive","the Well Loved ribbon is earned","giftgot" in json.dumps(st(B).get("ribbons")))
    goto_hash(B,"#gift="+code); m=mt(B)
    rec("Receive","opening the same link again doesn't give a second copy","Already opened" in m and st(B)["curios"]["mushroom"]["n"]==1,m[:100])
    closemodals(B)
    # broken and tampered links
    for label,h in [("garbage","#gift=notreallyagiftatall"),("bad curio","#gift="+enc(dict(g,c="dragon",g="zzzzzz123456"))),("script name","#gift="+enc(dict(g,n="<img src=x onerror=alert(1)>"*2,g="yyyyyy123456")))]:
        goto_hash(B,h); t=B.evaluate("document.getElementById('toast').textContent")
        rec("Links",f"a {label} link is refused politely",not mt(B) and "broken" in t and B.evaluate("location.hash")=="" and not B.evaluate("localStorage.getItem('forge-gift-in')"),(mt(B)[:60],t))
    # ---------- someone new ----------
    cC,C=newpage(b); C.goto(P.split("#")[0]+"#gift="+code); C.wait_for_selector("#titleGo"); C.wait_for_timeout(500)
    rec("New player","the title screen says a gift is waiting",C.locator("#titleGift").is_visible() and "Pip sent you a gift" in C.inner_text("#titleGift"))
    bad+=["title: "+v for v in axe(C)]
    C.tap("#titleGo"); C.wait_for_selector("#ageM",state="visible"); C.select_option("#ageM","6"); C.select_option("#ageY","1995"); C.tap("#ageGo")
    C.tap("#vBack"); C.wait_for_selector("#vDoneNow",state="visible"); C.tap("#vDoneNow"); C.wait_for_selector("#cover",state="visible"); C.tap("#cover")
    C.wait_for_selector("#rvSkip",state="visible"); C.tap("#rvSkip")
    C.wait_for_selector("#fdHearth",state="visible",timeout=8000)
    rec("New player","the gift waits until after the first Forgeling and the first-day note","That’s your first day" in mt(C))
    C.evaluate("document.querySelector('#modal [data-close]').click()")
    C.wait_for_selector("#giftKeep",state="visible",timeout=6000); C.tap("#giftKeep"); C.wait_for_timeout(500)
    rec("New player","then it opens and goes on the shelf","mushroom" in st(C)["curios"])
    # a visitor who is turned away keeps nothing
    cD,D=newpage(b); D.goto(P.split("#")[0]+"#gift="+code); D.wait_for_selector("#titleGo"); D.tap("#titleGo"); D.wait_for_selector("#ageM",state="visible")
    D.select_option("#ageM","6"); D.select_option("#ageY",str(__import__("datetime").date.today().year-15)); D.tap("#ageGo"); D.wait_for_timeout(600)
    rec("Age","a visitor under 18 is turned away and the gift is not kept",not D.evaluate("localStorage.getItem('forge-gift-in')") and "not available" in mt(D))
    # damaged saves
    sB=st(B); sB.update({"sid":"<x>","giftsGot":"oops","giftsSent":-3}); load(B,sB); sB=st(B)
    rec("Damaged","broken gift data in a save is repaired","sid" not in sB and sB["giftsGot"]==[] and sB["giftsSent"]==0 and not B._errs,(sB.get("sid"),sB.get("giftsGot"),sB.get("giftsSent")))
    # privacy note
    tabto(B,"settings"); B.evaluate("document.getElementById('btnPrivacy').click()"); B.wait_for_timeout(300)
    rec("Privacy","the privacy note explains gift links","gift link holds only the curio" in mt(B).lower() or "A gift link holds only the curio" in mt(B))
    closemodals(B)
    # dark theme a11y on the gift sheets
    cE,E=newpage(b,color_scheme="dark"); E.goto(P); E.wait_for_selector("#titleGo"); first_card(E); closemodals(E); sE=st(E); sE["seen"]=99; load(E,sE)
    goto_hash(E,"#gift="+code); bad+=["dark receive: "+v for v in axe(E)]
    rec("A11y","axe: zero violations on the send sheet, the gift, and the title note (light), and the gift (dark)",not bad,bad[:3])
    for nm,pg in (("sender",A),("friend",B),("new",C),("dark",E)): rec("All",f"{nm}: no page errors",not pg._errs,pg._errs[:1])
    b.close()
save_results("qa_29"); print(sum(r["ok"] for r in RES),"/",len(RES))
