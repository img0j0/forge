from lib import *
import datetime as _d
# 0.38.0: The Scribe (60 lines in total), its reading by the fire, Hearth lines about your own small things, ribbon.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); pg.wait_for_function("()=>document.getAnimations().every(a=>a.playState!=='running'||a.effect&&a.effect.getTiming().iterations===Infinity)",timeout=8000)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def load(pg,s):
    s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def lines(s,n,start=8):
    base=_d.date.fromisoformat(s["date"]); return {(base-_d.timedelta(days=start+i*2)).isoformat():{"v":i%12,"text":f"old line {i}"} for i in range(n)}
def scribe_px(pg):  # count pixels of the Scribe's quill ink on the Hearth canvas
    return pg.evaluate("()=>{const cv=document.getElementById('hearthCv');if(!cv)return -1;const d=cv.getContext('2d').getImageData(108,30,20,30).data;let n=0;for(let i=0;i<d.length;i+=4){if(Math.abs(d[i]-0x5A)<30&&Math.abs(d[i+1]-0x3F)<30&&Math.abs(d[i+2]-0xC0)<40)n++;}return n}")
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    s=st(pg); s["journal"]=lines(s,58); load(pg,s); tabto(pg,"hearth"); pg.wait_for_timeout(600)
    rec("Before","with 58 lines there is no Scribe yet",scribe_px(pg)==0 and "Scribe" not in pg.inner_text("#hmsg"))
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400)
    rec("Before","the book promises someone will come at 60","At 60, someone will come to the fire to read with you." in pg.inner_text("#view-chronicle"))
    # the 59th and 60th lines: the arrival
    s=st(pg); s["journal"]=lines(s,59); s["status"]="done"; load(pg,s); tabto(pg,"today")
    pg.evaluate("document.getElementById('btnMargin').click()"); pg.wait_for_timeout(300); pg.fill("#jIn","The sixtieth line."); pg.evaluate("document.getElementById('jSave').click()"); pg.wait_for_timeout(900)
    rec("Arrive","the sixtieth line brings the Scribe, with a toast","The Scribe has come" in pg.inner_text("#toast"))
    tabto(pg,"hearth"); pg.wait_for_timeout(700)
    rec("Arrive","the Hearth says someone new has come to the fire","Someone new has come to the fire" in pg.inner_text("#hmsg"),pg.inner_text("#hmsg"))
    rec("Look","the Scribe is drawn by the fire, with its ink-dipped quill",scribe_px(pg)>=2,scribe_px(pg))
    bad+=["hearth: "+v for v in axe(pg)]
    # the reading, once a day
    dev(pg,"next"); closemodals(pg); s=st(pg); s["opens"]+=[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
    import re as _re
    tabto(pg,"hearth"); pg.wait_for_timeout(500); m=pg.inner_text("#hmsg")
    rec("Read","once a day the Scribe opens your book and reads an older line",m.startswith("The Scribe opens your book.") and "old line" in m and bool(_re.search(r"\d+ days ago",m)),m)
    s=st(pg); rec("Read","…and remembers it has read today",s.get("scribeDay")==s["date"])
    tabto(pg,"today"); tabto(pg,"hearth"); m2=pg.inner_text("#hmsg")
    rec("Read","it does not read again the same day","Scribe opens your book" not in m2 or m2==m)
    tabto(pg,"chronicle"); pg.evaluate("()=>document.querySelector('[data-sub=\"journal\"]').click()"); pg.wait_for_timeout(400)
    rec("Book","the book says the Scribe sits by your fire","The Scribe sits by your fire" in pg.inner_text("#view-chronicle"))
    rec("Ribbon","the ribbon The Scribe is earned","The Scribe" in pg.inner_text("#view-chronicle") and "scribe" in (st(pg).get("ribbons") or []))
    # removing lines never takes it away? lines are totals: removing the 60th line drops below 60, so it leaves gently
    # (totals only grow in normal use; this checks nothing breaks)
    s=st(pg); s["journal"]=lines(s,10); load(pg,s); tabto(pg,"hearth"); pg.wait_for_timeout(500)
    rec("Edge","with fewer than 60 lines (edited away) nothing breaks and it is not drawn",scribe_px(pg)==0 and not pg._errs)
    # Hearth lines about your own things
    s=st(pg); s["owns"]=[{"id":1,"text":"Text Mom","k":2,"days":[]}]; s["todayOwn"]=1; s["status"]="revealed"; s["todayCard"]=None; load(pg,s); tabto(pg,"today")
    pg.evaluate("document.getElementById('btnDone').click()"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const c=document.getElementById('cover');c&&c.click()}"); pg.wait_for_timeout(400); pg.evaluate("()=>{const b=document.getElementById('rvSkip');b&&b.click()}"); pg.wait_for_timeout(600); closemodals(pg)
    s=st(pg); line=(s.get("comp") or {}).get("line","")
    rec("Own","on a day you do one of your own things, the Forgeling who notices says so","“Text Mom”" in line and "today" in line,line)
    dev(pg,"next"); closemodals(pg); s=st(pg); s["todayOwn"]=1; s["status"]="revealed"; s["todayCard"]=None; load(pg,s); tabto(pg,"today")
    pg.evaluate("document.getElementById('btnDone').click()"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const c=document.getElementById('cover');c&&c.click()}"); pg.wait_for_timeout(400); pg.evaluate("()=>{const b=document.getElementById('rvSkip');b&&b.click()}"); pg.wait_for_timeout(600); closemodals(pg)
    line2=(st(pg).get("comp") or {}).get("line","")
    rec("Own","…and the next time it notices you did it again","“Text Mom”" in line2 and line2!=line,line2)
    s=st(pg); s["scribeDay"]=5; load(pg,s); rec("Damaged","a broken reading date is repaired","scribeDay" not in st(pg) and not pg._errs)
    rec("A11y","axe: zero violations on the Hearth with the Scribe",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_38"); print(sum(r["ok"] for r in RES),"/",len(RES))
