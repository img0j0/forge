from lib import *
import base64
# 0.41.1: statue links. Share a cast statue as a link; a friend's browser rebuilds it in 3D from the link alone,
# display only. A new visitor can look before the 18+ check. Hostile links are refused or shown safely. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
DRAWN="()=>{const c=document.getElementById('stCv');if(!c||!c.width||c.hidden)return [0,0];const t=document.createElement('canvas');t.width=64;t.height=64;const x=t.getContext('2d');x.drawImage(c,0,0,64,64);const d=x.getImageData(0,0,64,64).data;let n=0,sat=0;for(let i=0;i<d.length;i+=4)if(d[i+3]>0){n++;const mx=Math.max(d[i],d[i+1],d[i+2]),mn=Math.min(d[i],d[i+1],d[i+2]);if(mx-mn>40)sat++;}return [n,sat];}"
def load(pg,s): s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def enc(o): return base64.urlsafe_b64encode(json.dumps(o,separators=(",",":")).encode()).decode().rstrip("=")
def link(o): return P+"#statue="+enc(o)
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader'])
    # ---------- the owner shares a statue ----------
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); c=s["cards"][0]; c["bond"]=30; c["keep"]="scarf"; c["statue"]={"at":s["date"],"keep":"scarf"}; c["nick"]="Pip"; hid=c["id"]; load(pg,s)
    tabto(pg,"hearth"); pg.tap(f"#view-hearth .stline [data-statue='{hid}']"); pg.wait_for_timeout(1200)
    rec("Share","the statue viewer has a Share a link button",pg.locator("#stLink").count()==1 and pg.locator("#stLink").is_visible())
    pg.tap("#stLink"); pg.wait_for_timeout(600)
    clip=pg.evaluate("navigator.clipboard.readText()")
    m=re.search(r"(https://\S+#statue=([A-Za-z0-9_-]+))",clip or "")
    rec("Share","the link goes to the live site and names the Forgeling",bool(m) and m.group(1).startswith("https://img0j0.github.io/forge/") and "Pip" in clip,clip[:160])
    raw=m.group(2); data=json.loads(base64.urlsafe_b64decode(raw+"="*(-len(raw)%4)))
    rec("Privacy","the link holds only what the statue is built from",set(data)=={"v","e","t","d","r","k","n","a","p"} and data["n"]=="Pip" and data["p"]=="scarf" and data["e"]==c["seed"],sorted(data))
    rec("Share","the report counts statue links sent",st(pg).get("statueLinks")==1)
    pg.tap("#ovClose"); pg.wait_for_timeout(500)
    before=st(pg); n0=len(before["cards"]); cur0=json.dumps(before["curios"],sort_keys=True)
    # ---------- the owner opens someone else's link: shown, nothing added ----------
    other=dict(data,n="Bramblet",e=12345,t=0,d=1,r=4,k=3,p="")
    pg.evaluate("(h)=>{location.hash=h}","statue="+enc(other)); pg.wait_for_timeout(1800)
    t=mt(pg) if pg.locator("#modal .stview").count() else ""
    rec("Open","a player opening a statue link sees the friend's statue in 3D","Bramblet" in t and "A friend’s statue" in t and "Legend" in t and "Bramble" in t,t[:120])
    d=pg.evaluate(DRAWN); rec("Open","…drawn in full colour",d[0]>200 and d[1]>d[0]*.1,d)
    rec("Open","…with no Get button for someone who already plays",pg.locator("#stGet").count()==0)
    rec("Open","…and the link is cleared from the address bar",pg.evaluate("location.hash")=="")
    pg.wait_for_timeout(400); bad+=["owner view: "+v for v in axe(pg)]
    pg.tap("#ovClose"); pg.wait_for_timeout(500); after=st(pg)
    rec("Display only","nothing was added: same cards, same curios, no new statue",len(after["cards"])==n0 and json.dumps(after["curios"],sort_keys=True)==cur0 and sum(1 for x in after["cards"] if x.get("statue"))==1)
    rec("All","no page errors for the owner",not pg._errs,pg._errs[:2]); ctx.close()
    # ---------- a new visitor ----------
    ctx,pg=newpage(b); pg.goto(link(data)); pg.wait_for_timeout(2500)
    t=mt(pg)
    rec("Visitor","a new visitor sees the statue before anything else","Pip" in t and pg.locator("#stCv").count()==1 and pg.locator("#ageM").count()==0,t[:120])
    d=pg.evaluate(DRAWN); rec("Visitor","…drawn in 3D",d[0]>200,d)
    rec("Visitor","…with a short line about the game and a Get Forgelings button","calm daily-habit game" in t and pg.locator("#stGet").is_visible())
    small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.offsetParent&&b.getBoundingClientRect().height<44).map(b=>b.textContent)")
    rec("Visitor","every button is a 44-point target",not small,small)
    pg.wait_for_timeout(300); bad+=["visitor: "+v for v in axe(pg)]
    rec("Visitor","nothing is saved for a visitor who is only looking",(st(pg) or {}).get("ageBand") in (None,) and not (st(pg) or {}).get("cards"))
    pg.tap("#stGet"); pg.wait_for_timeout(900)
    rec("Visitor","Get Forgelings goes on to the title and the 18+ check",pg.locator("#titleGo").count()==1 and pg.locator("#titleGo").is_visible())
    first_card(pg); closemodals(pg); s=st(pg)
    rec("Visitor","the visitor can then start as usual, with nothing from the link in their save",len(s["cards"])==1 and s["cards"][0]["seed"]!=data["e"] and not s["cards"][0].get("statue"))
    rec("All","no page errors for the visitor",not pg._errs,pg._errs[:2]); ctx.close()
    ctx,pg=newpage(b); pg.goto(link(data)); pg.wait_for_timeout(2000); pg.tap("#ovClose"); pg.wait_for_timeout(900)
    rec("Visitor","Just looking also returns to the title",pg.locator("#titleGo").count()==1 and pg.locator("#titleGo").is_visible()); ctx.close()
    # ---------- hostile and broken links ----------
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    evil=dict(data,n="<img src=x onerror=window.__pwn=1>")
    pg.evaluate("(h)=>{location.hash=h}","statue="+enc(evil)); pg.wait_for_timeout(1800)
    rec("Hostile","a name with markup is shown as text and never runs",not pg.evaluate("window.__pwn||0"),pg.evaluate("window.__pwn||0"))
    rec("Hostile","…and no image element was injected",pg.evaluate("document.querySelectorAll('#modal img[src=\"x\"]').length")==0)
    closemodals(pg)
    for nm,o in [("out-of-range realm",dict(data,t=9)),("unknown keepsake",dict(data,p="crown-of-everything")),("too-long name",dict(data,n="N"*40)),("bad date",dict(data,a="tomorrow"))]:
        pg.evaluate("(h)=>{location.hash=h}","statue="+enc(o)); pg.wait_for_timeout(1500)
        rec("Broken",f"a link with an {nm} is refused with a gentle note",pg.locator("#modal .stview").count()==0 and "statue link looks broken" in pg.inner_text("#toast"),pg.inner_text("#toast")[:80])
        pg.wait_for_timeout(2600)
    pg.evaluate("()=>{location.hash='statue=@@@not-base64@@@'}"); pg.wait_for_timeout(1200)
    rec("Broken","garbage after #statue= is ignored without errors",pg.locator("#modal .stview").count()==0 and not pg._errs,pg._errs[:1])
    rec("A11y","zero accessibility violations on the friend's statue (player and visitor)",not bad,bad[:4])
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    # reduced motion: still draws, turntable off
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.goto(link(data)); pg.wait_for_timeout(2200)
    rec("Motion","with reduced motion the statue still draws and the turntable starts off",pg.evaluate(DRAWN)[0]>200 and pg.get_attribute("#stTurn","aria-pressed")=="false")
    ctx.close()
save_results("qa_411")
