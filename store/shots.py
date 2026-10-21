import sys; sys.path.insert(0,'/home/claude/qa-src/forge-qa/qa')
import os
os.environ["FORGE_HTML"]="file:///home/claude/forgelings-app/www/index.html"
from lib import *
exec(open("/home/claude/qa-src/forge-qa/qa/qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
O='/tmp/claude-0/-home-claude/bd938e2e-992b-518b-b60c-27f2cca7a96c/scratchpad/raw/'; os.makedirs(O,exist_ok=True)
scheme=sys.argv[1] if len(sys.argv)>1 else "light"
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={"width":440,"height":956},device_scale_factor=3,has_touch=True,is_mobile=True,color_scheme=scheme,reduced_motion="reduce")
    pg=ctx.new_page(); pg._errs=[]; pg.on("pageerror",lambda e:pg._errs.append(str(e)))
    pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    base=st(pg)
    s=build(base,[6,4,3,6,2],(0,1),"mix"); s["seen"]=99
    names=["Wobble","Pip","Moss","Ember","Bramblet","Tuck","Fen","Cinder","Ash","Marlo","Kip","Sprig","Nim","Juniper","Rook","Lumen","Tansy","Quill","Hob","Wren","Sorrel"]
    import random; R=random.Random(7)
    for i,c in enumerate(s["cards"]): c["seed"]=R.randrange(1,2**31); c["v"]=R.randrange(12); c["wi"]=R.randrange(1000); c["name"]=names[i%len(names)]; c["rarity"]=[1,2,0,3,1,0,2,4,1,0,2,1,3,0,1,2,0,1,2,1,0][i%21]; c["bond"]=[9,16,4,26,3][i%5]
    ids=[c["id"] for c in s["cards"]]; s["hearth"]["slots"]=[ids[0],ids[6],ids[10]]
    for k in ["acorn","flower","mushroom","feather","leaf","spark","snow","moon","bell","shell","crystal"]: s["curios"][k]={"n":1,"cid":ids[0],"at":s["date"]}
    s["hearth"]["curio"]="mushroom"; s["explore"]={"0":4,"1":3,"2":1,"3":4,"4":1}
    import datetime as _d
    s["startDate"]=(_d.date.fromisoformat(s["date"])-_d.timedelta(days=20)).isoformat()
    s["opens"]=s.get("opens",[]); s["wander"]=None
    s["todayCard"]=ids[7]; s["status"]="done"; s["comp"]={"date":s["date"],"cid":ids[0],"line":"Wobble did a small happy hop by the fire.","up":0,"seen":1}
    setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); closemodals(pg)
    pg.add_style_tag(content="#toast{display:none!important}")
    def snap(n): pg.evaluate("document.activeElement&&document.activeElement.blur&&document.activeElement.blur()"); pg.wait_for_timeout(700); pg.screenshot(path=f"{O}{n}-{scheme}.png")
    tabto(pg,"today"); pg.evaluate("window.scrollTo(0,0)"); snap("1-today")
    tabto(pg,"hearth"); pg.evaluate("window.scrollTo(0,0)"); snap("2-hearth")
    pg.evaluate("()=>{document.querySelectorAll('#view-hearth details.more').forEach(d=>{if(/Curio shelf/.test(d.querySelector('summary').textContent))d.open=true})}"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('.shelf').scrollIntoView({block:'center'})"); snap("5-shelf")
    tabto(pg,"binder"); pg.evaluate("window.scrollTo(0,0)"); snap("3-binder")
    pg.evaluate("()=>{const c=document.querySelectorAll('#view-binder .card')[3];c&&c.click()}"); pg.wait_for_timeout(900); snap("3b-card")
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    openmap(pg); pg.evaluate("window.scrollTo(0,0)"); snap("4-map")
    tabto(pg,"hearth"); pg.evaluate("window.scrollTo(0,0)"); pg.evaluate("document.getElementById('hPlay').click()"); pg.wait_for_timeout(500); snap("6-games")
    print(pg._errs); b.close()
