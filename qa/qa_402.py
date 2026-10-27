from lib import *
import subprocess, shutil, tempfile, re as _re
# 0.40.2: the audit fixes. Loops sleep when nothing moves, a new release is offered on return, backups keep this
# device's age answer and long text is trimmed, and nothing visible is lost.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE)
    return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
CNT="(()=>{window.__raf=0;const o=window.requestAnimationFrame;window.requestAnimationFrame=f=>{window.__raf++;return o(f)}})()"
def rate(pg,ms=2000):
    pg.wait_for_timeout(700); pg.evaluate("()=>window.__raf=0"); pg.wait_for_timeout(ms); return pg.evaluate("()=>window.__raf")*1000/ms
def pix(pg,sel): return pg.evaluate("(s)=>{const c=document.querySelector(s);return c?Array.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data.filter((v,i)=>i%16===0)).join(','):''}",sel)
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b); pg.add_init_script(CNT); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
    # loops
    tabto(pg,"settings",fold=True); r=rate(pg)
    rec("Loops","on Settings nothing animates, so the loops sleep (a few checks a second, not 120 frames)",r<8,round(r,1))
    tabto(pg,"chronicle"); r=rate(pg); rec("Loops","on the Map the loops sleep too",r<8,round(r,1))
    tabto(pg,"hearth"); a=pix(pg,"#hearthCv"); pg.wait_for_timeout(600); a2=pix(pg,"#hearthCv")
    rec("Loops","coming back to the Hearth, the fire moves again at once",a!=a2)
    tabto(pg,"binder"); sel="#view-binder canvas.pcv"; a=pix(pg,sel); pg.wait_for_timeout(500); a2=pix(pg,sel)
    rec("Loops","in the Binder the creatures still breathe",a!=a2)
    pg.evaluate("()=>document.querySelector('#view-binder .card').click()"); pg.wait_for_timeout(500); a=pix(pg,"#stage canvas.pcv"); pg.wait_for_timeout(500)
    rec("Loops","a card close-up still animates",a!=pix(pg,"#stage canvas.pcv")); closemodals(pg)
    tabto(pg,"settings",fold=True); pg.evaluate("()=>document.querySelector('.tab[data-tab=\"today\"]').click()"); pg.wait_for_timeout(150)
    sel="#view-today canvas.pcv"
    if pg.locator(sel).count():
        a=pix(pg,sel); pg.wait_for_timeout(400); rec("Loops","a sleeping loop wakes straight away on a tab change",a!=pix(pg,sel))
    # restore: age answer and long text
    s=st(pg); s["cards"][0]["nick"]="N"*100; s["cards"][0]["tale"]="T"*900; s["ageBand"]="teen"
    tabto(pg,"settings"); pg.evaluate("document.getElementById('btnRestore').click()"); pg.wait_for_timeout(300); pg.fill("#resText",json.dumps(s))
    pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(200); pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(700)
    s2=st(pg); c=s2["cards"][0]
    rec("Restore","a backup keeps this device's age answer",s2["ageBand"]=="adult",s2["ageBand"])
    rec("Restore","very long nicknames and tales from a file are trimmed",len(c["nick"])==24 and len(c["tale"])==200,(len(c["nick"]),len(c["tale"])))
    names=pg.evaluate("()=>{try{return JSON.parse(localStorage.getItem('forge-app-v1')).cards.map(c=>c.name.length)}catch(e){return[]}}")
    rec("All","no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    # reduced motion: both loops sleep everywhere
    ctx,pg=newpage(b,reduced_motion="reduce"); pg.add_init_script(CNT); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    tabto(pg,"hearth"); r=rate(pg); rec("Motion","with reduced motion nothing runs every frame, even at the Hearth",r<8,round(r,1)); ctx.close()
    # names: the longest generated name fits the 40-letter trim
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    for _ in range(3): dev(pg,"pack"); closemodals(pg)
    L=max(len(c["name"]) for c in st(pg)["cards"]); rec("Restore","generated names are well under the 40-letter trim",L<=30,L); ctx.close()
    # a new version is ready: served the way GitHub Pages serves it
    tmp=tempfile.mkdtemp(); shutil.copy(S+"/work.html",tmp+"/work.html")
    subprocess.run(["python3",S+"/pwa.py"],cwd=tmp,check=True,stdout=subprocess.DEVNULL); os.rename(tmp+"/pwa",tmp+"/forge")
    srv=subprocess.Popen(["python3","-m","http.server","8766"],cwd=tmp,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        time.sleep(1); U="http://localhost:8766/forge/"
        ctx,pg=newpage(b); pg.set_default_timeout(8000); pg.goto(U); pg.wait_for_selector("#titleGo")
        pg.wait_for_function("async()=>{const r=await navigator.serviceWorker.getRegistration();return !!(r&&r.active)}"); pg.wait_for_timeout(800)
        rec("Update","the first install shows no update note",pg.locator("#updBar").count()==0)
        pg.reload(); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
        pg.evaluate("()=>document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(1500)
        rec("Update","coming back with no new release shows nothing",pg.locator("#updBar").count()==0)
        sw=open(tmp+"/forge/sw.js").read(); open(tmp+"/forge/sw.js","w").write(_re.sub(r"forge-[0-9.]+","forge-9.9.9",sw))
        pg.evaluate("()=>document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(1500)
        rec("Update","…and the check waits half an hour between returns, so a second return right away finds nothing",pg.locator("#updBar").count()==0)
        pg.reload(); pg.wait_for_selector("#view-today",state="attached"); pg.wait_for_timeout(1500); closemodals(pg)
        rec("Update","opening the app fresh simply loads the new release, with no note",pg.locator("#updBar").count()==0)
        open(tmp+"/forge/sw.js","w").write(_re.sub(r"forge-[0-9.]+","forge-9.9.10",sw))
        pg.evaluate("()=>document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_selector("#updBar",timeout=8000)
        t=pg.inner_text("#updBar")
        rec("Update","a new release, found on return, is offered in a small note with Load it and Later","new version" in t and pg.locator("#updGo").count()==1 and pg.locator("#updLater").count()==1,t)
        sz=pg.evaluate("()=>[...document.querySelectorAll('#updBar button')].map(b=>{const r=b.getBoundingClientRect();return Math.min(r.width,r.height)})")
        rec("Update","its buttons are at least 44 points",min(sz)>=44,sz)
        bad+=["update note: "+v for v in axe(pg)]
        pg.tap("#updLater"); pg.wait_for_timeout(200); rec("Update","Later puts it away",pg.locator("#updBar").count()==0)
        pg.evaluate("()=>{window.__stay=1}")
        open(tmp+"/forge/sw.js","w").write(_re.sub(r"forge-[0-9.]+","forge-9.9.11",sw))
        pg.reload(); pg.wait_for_timeout(1200); closemodals(pg)
        pg.evaluate("()=>document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_selector("#updBar",timeout=8000)
        pg.tap("#updGo"); pg.wait_for_timeout(1500)
        rec("Update","Load it reloads into the new release, keeping your Forgelings",pg.evaluate("()=>window.__stay")is None and pg.locator("#updBar").count()==0 and len(st(pg)["cards"])>=1)
        rec("All","served copy: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    finally:
        srv.terminate(); shutil.rmtree(tmp,ignore_errors=True)
    rec("A11y","axe: zero violations on the update note",not bad,bad[:3])
    b.close()
save_results("qa_402"); print(sum(r["ok"] for r in RES),"/",len(RES))
