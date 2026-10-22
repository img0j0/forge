from lib import *
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
import itertools
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(8000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
    s=st(pg); s["seen"]=18; setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
    import subprocess
    r=json.loads(subprocess.check_output(["node","cal.js"],cwd=S).decode())
    rec("Events","every day before the cutoff has exactly the same event as before",r["changedBefore"]==0,r)
    rec("Events","the same days have events (frequency unchanged)",r["nullMismatch"]==0)
    rec("Events","after the cutoff all twelve kinds appear",r["kindsAfter"]==list(range(12)),r["kindsAfter"])
    rec("Events","each realm has twelve entries, each with bright and Shade wording",r["counts"]==[12]*5 and r["pairsOk"],r["counts"])
    # 2. solo behaviours: every calling draws something visible, differs from empty hearth, no errors
    s=st(pg); b0=s["cards"][0]
    for v in range(12):
        c=json.loads(json.dumps(b0)); c["v"]=v; s["cards"]=[c]; s["hearth"]["slots"]=[c["id"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
        tabto(pg,"hearth"); pg.wait_for_timeout(300)
        frames=[]
        for k in range(5):
            pg.wait_for_timeout(1300)
            frames.append(pg.evaluate("()=>{const cv=document.querySelector('#view-hearth canvas');return cv?cv.toDataURL().length+':'+cv.toDataURL().slice(-400):'none';}"))
        rec("Alone",f"calling {v} ({['Clarity','Leverage','Depth','Velocity','Connection','Resilience','Play','Craft','Silence','Courage','Systems','Presence'][v]}) animates when alone, without errors",len(set(frames))>1 and "none" not in frames[0] and not pg._errs,pg._errs[:1])
    rec("Console","no page errors",not pg._errs,pg._errs[:2])
    b.close()
save_results("qa_15"); print(sum(r["ok"] for r in RES),"/",len(RES))
