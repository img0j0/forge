from lib import *
import datetime
# 0.48.5: the phone's date moving back a day or two (travel west after midnight, a clock changed by hand) holds the
# day: a finished day stays finished, the card can't be earned twice, no day is logged twice. A bigger jump back still
# follows the phone. Ordinary days still roll over, and missed days are still logged once each.
def snap(pg):
    s=st(pg); ds=[h["date"] for h in s["history"]]
    return {"date":s["date"],"status":s["status"],"cards":len(s["cards"]),"dup":len(ds)-len(set(ds)),"today":s.get("todayCard")}
def go(pg,y,m,d,h=10):
    pg.clock.set_system_time(datetime.datetime(y,m,d,h,0)); pg.reload(); pg.wait_for_timeout(1100); closemodals(pg); return snap(pg)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b)
    pg.clock.install(time=datetime.datetime(2026,11,5,10,0)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    s0=snap(pg); rec("Clock","day 1 is done with one Forgeling",s0["status"]=="done" and s0["cards"]==1,s0)
    s1=go(pg,2026,11,4); rec("Clock","the date moving back a day keeps the finished day: still done, no new card on offer",s1["date"]=="2026-11-05" and s1["status"]=="done" and s1["today"]==s0["today"],s1)
    s1b=go(pg,2026,11,3,23); rec("Clock","two days back still holds the day",s1b["date"]=="2026-11-05" and s1b["status"]=="done",s1b)
    tabto(pg,"hearth"); v0=pg.inner_text("#view-hearth"); import re as _re; vl=lambda t:(_re.search(r"Visits left today: (\d)",t) or [None,None])[1]
    pg.evaluate("document.getElementById('hSnack').click()"); pg.wait_for_timeout(400)
    try: pg.locator("#modal [data-snack]").first.click(); pg.wait_for_timeout(500)
    except Exception: pass
    closemodals(pg); tabto(pg,"hearth"); used=vl(pg.inner_text("#view-hearth"))
    go(pg,2026,11,4); tabto(pg,"hearth"); after=vl(pg.inner_text("#view-hearth"))
    rec("Clock","moving the date back does not give back Hearth visits",used is not None and after==used,(vl(v0),used,after))
    s2=go(pg,2026,11,5); rec("Clock","back to the real date: still done, nothing logged twice",s2["date"]=="2026-11-05" and s2["status"]=="done" and s2["dup"]==0,s2)
    s3=go(pg,2026,11,6); rec("Clock","the next real day rolls over as usual",s3["date"]=="2026-11-06" and s3["status"]=="fresh" and s3["dup"]==0,s3)
    s4=go(pg,2026,11,9); h=st(pg)["history"]; miss=[x["date"] for x in h if x["status"]=="skipped"]
    rec("Clock","missed days are still logged once each",s4["date"]=="2026-11-09" and s4["dup"]==0 and miss==["2026-11-06","2026-11-07","2026-11-08"],(s4,miss))
    s5=go(pg,2026,9,1); rec("Clock","a big jump back (a clock set wrong) still follows the phone",s5["date"]=="2026-09-01",s5)
    rec("All","no page errors",not pg._errs,pg._errs[:2]); b.close()
save_results("qa_485"); print(sum(r["ok"] for r in RES),"/",len(RES))
