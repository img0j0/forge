from lib import *
# 0.43.1: appearance references. Ten fixed-seed cards (every rarity, light and dark, all five realms) and one statue are
# drawn with reduced motion and compared with the images in qa/ref/. A release that changes the art on purpose
# regenerates them with REF_UPDATE=1 (and says so in the handoff); any other change to how a card looks fails here.
from PIL import Image, ImageChops
import io
REF=S+"/qa/ref"; UPD=os.environ.get("REF_UPDATE")=="1"; os.makedirs(REF,exist_ok=True)
T={"id":1,"seed":0,"v":0,"dark":False,"rarity":0,"theme":0,"name":"Ketly","stats":[42,46,57],"serial":581,"date":"2026-10-30","kh":12,"dayN":1,"dateLabel":"Fri, Oct 30","note":"","nick":"","tale":"","wi":113,"bond":0,"keep":"","fire":[],"allIn":False,"source":"daily","own":"","era":4,"gossip":""}
SEEDS=[634733212,136756196,11,222,3333,44444,555555,6666666,77777777,888888888]
NAMES=["Ketly","Thulwraith","Bramblet","Oxwick","Pell","Sorrowmere","Tindle","Quillon","Marrow","Juniper"]
def cards():
    out=[]
    for i,sd in enumerate(SEEDS):
        c=dict(T); c.update(id=i+1,seed=sd,v=(i*5)%12,dark=i%2==1,rarity=i%5,theme=i%5,name=NAMES[i],stats=[30+i*5,40+i*3,50+i*2],serial=100+i,wi=sd%1000); out.append(c)
    return out
def diff(a,b):
    if a.size!=b.size: return 1.0
    d=ImageChops.difference(a.convert("RGB"),b.convert("RGB")).convert("L").point(lambda x:255 if x>24 else 0)
    return sum(1 for v in d.getdata() if v)/(a.size[0]*a.size[1])
def check(name,png):
    img=Image.open(io.BytesIO(png)); path=f"{REF}/{name}.png"
    if UPD or not os.path.exists(path):
        img.save(path); rec("Ref",f"{name}: reference written",True); return
    d=diff(img,Image.open(path))
    if d>=0.005 and os.environ.get("REF_OUT"): img.save(os.environ["REF_OUT"]+f"/{name}_now.png")
    rec("Ref",f"{name} looks the same as its reference",d<0.005,f"{d*100:.2f}% of pixels differ")
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader'])
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); s["cards"]=cards(); s["nextId"]=11; s["todayCard"]=None; s["hearth"]["slots"]=[1]; s["opens"]=s.get("opens",[])+[s["date"]]
    setst(pg,s)
    # the shine and sparkles follow the clock, so the page runs on a paused clock and is stepped by hand
    pg.clock.install(time=datetime.datetime(2026,10,30,12,0,0)); pg.reload(); pg.clock.pause_at(datetime.datetime(2026,10,30,12,0,5)); pg.clock.run_for(3000); closemodals(pg); pg.clock.run_for(1000)
    for i in range(1,11):
        tabto(pg,"binder"); pg.clock.run_for(500)
        pg.evaluate("i=>{const v=document.getElementById('view-binder'),x=document.createElement('button');x.dataset.insp=i;v.appendChild(x);x.click();x.remove()}",i); pg.clock.run_for(1500)
        check(f"card{i:02d}",pg.locator("#modal .card").first.screenshot(animations="disabled"))
        pg.evaluate("()=>{const b=document.querySelector('#modal [data-close]');if(b)b.click();}"); pg.clock.run_for(800)
    s=st(pg); s["cards"][0]["bond"]=25; s["cards"][0]["statue"]={"at":s["date"],"keep":""}; setst(pg,s); pg.reload(); pg.clock.run_for(3000); closemodals(pg); pg.clock.run_for(800)
    hsheet(pg,"comp"); pg.clock.run_for(500); pg.evaluate("()=>document.querySelector('#modal .stline [data-statue=\"1\"]').click()"); pg.clock.run_for(1500)
    check("statue01",pg.locator("#stCv").screenshot())
    rec("All","no page errors",not pg._errs,pg._errs[:2])
    b.close()
save_results("qa_ref"); print(sum(r["ok"] for r in RES),"/",len(RES))
