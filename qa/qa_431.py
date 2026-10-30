from lib import *
# 0.43.1: safe saves. One tab at a time; an unreadable save gets a recovery sheet (safety copy, restore, copy, start over);
# a save missing its settings is repaired; Restore respects a failed save; the statue viewer rests under reduced motion.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg):
    pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
BROKEN='{"v":1,"cards":[{"id":1,"bro'
def raw(pg,k=KEY): return pg.evaluate("k=>localStorage.getItem(k)",k)
def toast(pg): return pg.evaluate("document.getElementById('toast').textContent")
def size(pg,sel): return pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.width,r.height]}",sel)
RAF="()=>{if(window.__rafw)return;window.__rafw=1;window.__raf=0;const o=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=f=>{window.__raf++;return o(f)};}"
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader'])
    # ---------- two tabs ----------
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"holo"); closemodals(pg)
    pg.reload(); pg.wait_for_timeout(900)
    rec("Tabs","reloading one tab never trips the guard",pg.locator("#tabAway").count()==0)
    pg2=ctx.new_page(); pg2._errs=[]; pg2.on("pageerror",lambda e:pg2._errs.append(str(e))); pg2.goto(P); pg2.wait_for_timeout(1200)
    rec("Tabs","opening a second tab steps the first one aside",pg.locator("#tabAway").count()==1 and pg2.locator("#tabAway").count()==0)
    rec("Tabs","the stepped-aside tab says why, calmly","Forgelings is open somewhere else" in pg.inner_text("#tabAway") and "nothing gets written over" in pg.inner_text("#tabAway"))
    rec("Tabs","…and the app behind it can't be used",pg.evaluate("document.querySelector('.app').inert&&document.querySelector('.tabs').inert"))
    w,h=size(pg,"#tabHere"); rec("Tabs","Use it here is a 44-point target and has focus",w>=44 and h>=44 and pg.evaluate("document.activeElement.id")=="tabHere",(w,h))
    v=axe(pg); rec("A11y","the tab notice has no accessibility violations",not v,v)
    sv=st(pg)["_sv"]; pg2.evaluate("document.querySelector('.tab[data-tab=\"hearth\"]').click()"); pg2.wait_for_timeout(300)
    pg.tap("#tabHere"); pg.wait_for_timeout(1400)
    rec("Tabs","Use it here takes over: this tab is live and the other steps aside",pg.locator("#tabAway").count()==0 and pg2.locator("#tabAway").count()==1)
    rec("Tabs","…and it picks up the latest save",pg.evaluate("k=>JSON.parse(localStorage.getItem(k))._sv",KEY)>=sv)
    rec("All","no page errors in either tab",not pg._errs and not pg2._errs,(pg._errs+pg2._errs)[:2])
    pg2.close()
    good=st(pg); n=len(good["cards"])
    # ---------- unreadable save, with a safety copy ----------
    rec("Daily","a safety copy is kept",raw(pg,KEY+"-daily") is not None and len(json.loads(raw(pg,KEY+"-daily"))["cards"])==n)
    pg.evaluate("([k,b])=>localStorage.setItem(k,b)",[KEY,BROKEN]); pg.reload(); pg.wait_for_timeout(1500)
    t=mt(pg)
    rec("Recover","an unreadable save opens the recovery sheet, not the title","could not read your saved collection" in t and "Nothing has been deleted" in t and pg.locator("#titleGo").count()==0,t[:200])
    rec("Recover","it offers the safety copy, with its date and how many Forgelings","A safety copy from" in t and f"with {n} Forgeling" in t and pg.locator("#recUse").count()==1)
    rec("Recover","the unreadable save is untouched and also kept aside",raw(pg)==BROKEN and raw(pg,KEY+"-recovery")==BROKEN)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300); pg.mouse.click(10,10); pg.wait_for_timeout(300)
    rec("Recover","it can't be brushed away by accident","could not read" in mt(pg))
    v=axe(pg); rec("A11y","the recovery sheet has no accessibility violations",not v,v)
    small=pg.evaluate("()=>[...document.querySelectorAll('#modal button')].filter(b=>{const r=b.getBoundingClientRect();return r.width<44||r.height<44}).map(b=>b.id)")
    rec("Recover","every button is at least 44 points",not small,small)
    pg.tap("#recUse"); pg.wait_for_timeout(1500)
    rec("Recover","Use the safety copy brings the collection back",len(st(pg)["cards"])==n and "could not read" not in mt(pg))
    # ---------- unreadable save, no safety copy: restore a backup ----------
    pg.evaluate("([k,b])=>{localStorage.removeItem(k+'-daily');localStorage.setItem(k,b)}",[KEY,BROKEN]); pg.reload(); pg.wait_for_timeout(1500)
    rec("Recover","without a safety copy, Restore a backup leads",pg.locator("#recUse").count()==0 and pg.locator("#recRestore.primary").count()==1)
    pg.tap("#recRestore"); pg.wait_for_timeout(400)
    rec("Recover","the restore sheet has Back, not Cancel",pg.locator("#modal #recBack").count()==1 and pg.locator("#modal [data-close]").count()==0)
    pg.tap("#recBack"); pg.wait_for_timeout(400); rec("Recover","Back returns to the recovery sheet","could not read" in mt(pg))
    pg.tap("#recRestore"); pg.wait_for_timeout(400); pg.fill("#resText",json.dumps(good)); pg.tap("#doRestore"); pg.tap("#doRestore"); pg.wait_for_timeout(900)
    rec("Recover","restoring a backup from there brings the collection back",len(st(pg)["cards"])==n and toast(pg)=="Restored." and pg.evaluate("document.getElementById('modal').hidden"),toast(pg))
    # ---------- start over ----------
    pg.evaluate("([k,b])=>{localStorage.removeItem(k+'-daily');localStorage.setItem(k,b)}",[KEY,BROKEN]); pg.reload(); pg.wait_for_timeout(1500)
    pg.tap("#recCopy"); pg.wait_for_timeout(400)
    clip=pg.evaluate("navigator.clipboard.readText()")
    rec("Recover","Copy the unreadable save copies it exactly",clip==BROKEN,clip[:40])
    pg.tap("#recFresh"); pg.wait_for_timeout(200); rec("Recover","Start over asks twice","Tap again" in pg.inner_text("#recFresh"))
    pg.tap("#recFresh"); pg.wait_for_timeout(900)
    rec("Recover","…then opens the title, keeping the unreadable save aside",pg.locator("#titleGo").count()==1 and raw(pg,KEY+"-recovery")==BROKEN)
    ctx.close()
    # ---------- a save missing its settings is repaired ----------
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo")
    s=json.loads(json.dumps(good)); del s["settings"]; setst(pg,s); pg.reload(); pg.wait_for_timeout(1500)
    rec("Repair","a save missing its settings opens with every Forgeling and says it was mended",len(st(pg)["cards"])==n and isinstance(st(pg).get("settings"),dict) and "small repair" in toast(pg),toast(pg))
    # ---------- Restore waits for a good save ----------
    closemodals(pg); tabto(pg,"settings"); pg.evaluate("document.getElementById('btnRestore').click()"); pg.wait_for_timeout(400)
    one=json.loads(json.dumps(good)); one["cards"]=one["cards"][:1]; pg.fill("#resText",json.dumps(one))
    pg.evaluate("k=>{const o=Storage.prototype.setItem;window.__si=o;Storage.prototype.setItem=function(a,b){if(a===k)throw new Error('quota');return o.call(this,a,b)}}",KEY)
    pg.tap("#doRestore"); pg.tap("#doRestore"); pg.wait_for_timeout(600)
    t=toast(pg); pg.evaluate("()=>{Storage.prototype.setItem=window.__si}")
    rec("Restore","if the device can't keep the restored copy, nothing changes and it says so","could not keep the restored copy" in t and len(st(pg)["cards"])==n,t)
    closemodals(pg); tabto(pg,"binder"); rec("Restore","…and the app still shows the whole collection",pg.evaluate("document.querySelectorAll('#view-binder .card').length")==n,n)
    rec("All","no page errors",not pg._errs,pg._errs[:2])
    ctx.close()
    # ---------- statue viewer under reduced motion ----------
    for rm in ("reduce","no-preference"):
        ctx,pg=newpage(b,reduced_motion=rm); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); dev(pg,"week"); closemodals(pg)
        s=st(pg); hid=s["hearth"]["slots"][0]; c=[x for x in s["cards"] if x["id"]==hid][0]; c["bond"]=25; c["statue"]={"at":s["date"],"keep":""}
        s["opens"]=s.get("opens",[])+[s["date"]]; setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
        hsheet(pg,"comp"); pg.evaluate(RAF); pg.evaluate("i=>document.querySelector('#modal .stline [data-statue=\"'+i+'\"]').click()",hid); pg.wait_for_timeout(1200)
        pg.evaluate("window.__raf=0"); pg.wait_for_timeout(2000); n0=pg.evaluate("window.__raf")
        if rm=="reduce":
            rec("Statue","with reduced motion the statue is drawn once and rests",n0<=12,n0)
            box=pg.locator("#stCv").bounding_box(); before=pg.evaluate("document.getElementById('stCv').toDataURL()")
            pg.mouse.move(box["x"]+box["width"]/2,box["y"]+box["height"]/2); pg.mouse.down(); pg.mouse.move(box["x"]+box["width"]/2+80,box["y"]+box["height"]/2,steps=6); pg.mouse.up(); pg.wait_for_timeout(400)
            rec("Statue","…and turning it by hand still redraws it",pg.evaluate("document.getElementById('stCv').toDataURL()")!=before)
        else:
            rec("Statue","without reduced motion it keeps turning",n0>=40,n0)
        rec("All",f"no page errors ({rm})",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_431"); print(sum(r["ok"] for r in RES),"/",len(RES))
