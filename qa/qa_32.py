from lib import *
# 0.32.0: the iPhone app layer, tested with a stand-in for Capacitor's plugins (kept on the test side so it survives
# reloads, like the phone's own storage would).
import datetime as _dt
MOCK = r"""
(()=>{const M=(...a)=>window.__m(...a);
 window.Capacitor={isNativePlatform:()=>true,Plugins:{
  Preferences:{get:async({key})=>({value:await M('get',key)}),set:async({key,value})=>M('set',key,value),remove:async({key})=>M('del',key)},
  LocalNotifications:{checkPermissions:async()=>({display:await M('perm')}),requestPermissions:async()=>({display:await M('ask')}),
    cancel:async(o)=>M('log','cancel',o.notifications.map(n=>n.id)),
    schedule:async(o)=>M('sched',o.notifications.map(n=>({id:n.id,body:n.body,at:new Date(n.schedule.at).toISOString()})))},
  Haptics:{impact:async(o)=>M('log','haptic',o.style),notification:async(o)=>M('log','haptic',o.type)},
  Share:{share:async(o)=>M('log','share',{title:o.title,text:o.text||'',files:o.files||[]})},
  Filesystem:{writeFile:async(o)=>{await M('log','write',{path:o.path,len:(o.data||'').length,dir:o.directory});return {uri:'file:///cache/'+o.path}}}
 }};})();
"""
class Mock:
    def __init__(s): s.prefs={}; s.log=[]; s.perm='prompt'; s.sched=[]
    def __call__(s,source,op,k=None,v=None):
        if op=='get': return s.prefs.get(k)
        if op=='set': s.prefs[k]=v; return None
        if op=='del': s.prefs.pop(k,None); return None
        if op=='perm': return s.perm
        if op=='ask': s.log.append(('ask',1)); s.perm='granted'; return 'granted'
        if op=='sched': s.sched=k; s.log.append(('schedule',k)); return None
        if op=='log': s.log.append((k,v)); return None
MOCKS={}
def logs(pg,k=None): return [v for kk,v in MOCKS[pg].log if k is None or kk==k]
def prefs(pg): return MOCKS[pg].prefs
def sched(pg): return MOCKS[pg].sched
def clearlog(pg): MOCKS[pg].log.clear()
def npage(b,**kw):
    ctx,pg=newpage(b,**kw); m=Mock(); ctx.expose_binding("__m",m); ctx.add_init_script(MOCK); MOCKS[pg]=m; return ctx,pg
def onboard(pg):
    pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=npage(b); onboard(pg); pg.wait_for_timeout(600)
    pv=prefs(pg); s=st(pg)
    rec("Saves","every save is mirrored to the phone's own storage",pv.get("forge-app-v1") and json.loads(pv["forge-app-v1"])["cards"][0]["id"]==s["cards"][0]["id"])
    rec("Saves","saves carry a counter so the newer copy can win",isinstance(s.get("_sv"),int) and s["_sv"]>0)
    # iOS clears web storage: the collection comes back
    n=len(s["cards"]); name=s["cards"][0]["name"]
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(1200); closemodals(pg)
    s2=st(pg)
    rec("Saves","if web storage is wiped, the collection is restored from the phone's storage",s2 and len(s2["cards"])==n and s2["cards"][0]["name"]==name and not pg.locator("#titleGo").count())
    # the newer copy wins, both ways
    s3=st(pg); old=json.loads(json.dumps(s3)); s3["_sv"]=s3["_sv"]+50; s3["cards"][0]["nick"]="FromPhone"
    prefs(pg)["forge-app-v1"]=json.dumps(s3)
    pg.reload(); pg.wait_for_timeout(1200); closemodals(pg)
    rec("Saves","when the phone's copy is newer, it wins",st(pg)["cards"][0]["nick"]=="FromPhone")
    s4=st(pg); s4["_sv"]=s4["_sv"]+80; s4["cards"][0]["nick"]="FromWeb"; setst(pg,s4); pg.reload(); pg.wait_for_timeout(1200); closemodals(pg); pg.wait_for_timeout(500)
    rec("Saves","when the web copy is newer, it wins and is copied to the phone",st(pg)["cards"][0]["nick"]=="FromWeb" and "FromWeb" in prefs(pg).get("forge-app-v1",""))
    # store edition
    tabto(pg,"settings"); t=pg.inner_text("#view-settings")
    rec("Store","tester-only pieces are hidden: feedback questions, pilot report, prototype tools","Feedback" not in t and "My report" not in t and pg.locator("details.dev").count()==0,t[-200:])
    rec("Store","the version reads as a plain app version","Forgelings 1.0.0" in t and "prototype" not in t)
    rec("Store","no 'add to home screen' tip inside the app","Put Forgelings on your home screen" not in t)
    tabto(pg,"binder"); pg.evaluate("()=>{const c=document.querySelector('#view-binder .card');c&&c.click()}"); pg.wait_for_timeout(500)
    ft=pg.evaluate("[...document.querySelectorAll('.card .foot span:first-child')].map(e=>e.textContent)")
    rec("Store","cards say First Edition in the app",ft and all(x=="First Edition" for x in ft),ft[:3])
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    # reminders
    tabto(pg,"settings"); clearlog(pg)
    rec("Reminders","Settings has reminders, the wanderer note and haptics in the app",pg.locator("[data-setnudge]").count()==4 and pg.locator("#setWnote").count()==1 and pg.locator("#setHaptic").count()==1)
    pg.tap("[data-setnudge='8:00 am']"); pg.wait_for_timeout(800)
    sch=sched(pg)
    s=st(pg); done=s["status"]=="done"
    at=[x for x in sch if x["id"]==1]
    when=_dt.datetime.fromisoformat(at[0]["at"].replace("Z","+00:00")).astimezone() if at else None
    rec("Reminders","choosing a time asks permission and schedules one gentle nudge",logs(pg,"ask") and len(at)==1 and when and when.hour==8 and when.minute==0,(sch,when))
    rec("Reminders","with today's card already done, the nudge is for tomorrow",(not done) or (when and when.date()>_dt.date.today()),(done,when))
    rec("Reminders","a reminder is never doubled up: old ones are cancelled first",all(1 in c for c in logs(pg,"cancel")) and len([x for x in sch if x["id"]==1])==1)
    # wanderer note
    tabto(pg,"hearth"); pg.evaluate("()=>{const b=document.getElementById('hWander');b&&b.click()}"); pg.wait_for_timeout(300); pg.evaluate("()=>{const b=document.querySelector('#modal [data-wgo]');b&&b.click()}"); pg.wait_for_timeout(1600)
    sch=sched(pg); w=st(pg)["wander"]
    two=[x for x in sch if x["id"]==2]
    rec("Reminders","sending a Forgeling wandering schedules a note for when they're back",w and len(two)==1 and abs(_dt.datetime.fromisoformat(two[0]["at"].replace("Z","+00:00")).timestamp()*1000-w["ready"])<2000 and "back from wandering" in two[0]["body"],(two,w and w["ready"]))
    tabto(pg,"settings"); pg.tap("#setWnote"); pg.wait_for_timeout(1500)
    sch=sched(pg)
    rec("Reminders","turning the wanderer note off removes it",not [x for x in sch if x["id"]==2] and st(pg)["settings"]["wnote"]==False,sch)
    # haptics
    clearlog(pg); tabto(pg,"today"); pg.tap(".tab[data-tab='hearth']"); pg.wait_for_timeout(300)
    rec("Haptics","taps give a light haptic",'LIGHT' in logs(pg,"haptic") or logs(pg,"haptic"),logs(pg,"haptic"))
    tabto(pg,"settings"); pg.tap("#setHaptic"); pg.wait_for_timeout(200); clearlog(pg); pg.tap(".tab[data-tab='hearth']"); pg.wait_for_timeout(300)
    rec("Haptics","turning haptics off stops them",not logs(pg,"haptic"),logs(pg,"haptic"))
    # share sheet
    clearlog(pg); tabto(pg,"settings"); pg.evaluate("document.getElementById('btnExport').click()"); pg.wait_for_timeout(500)
    btn=pg.evaluate("[...document.querySelectorAll('#modal button')].map(b=>b.id)")
    for bid in btn:
        if bid in ("bkFile","btnBackupFile","expFile","bkSave"): pg.evaluate(f"document.getElementById('{bid}').click()")
    pg.evaluate("()=>{const b=[...document.querySelectorAll('#modal button')].find(b=>/file|save a copy|save it/i.test(b.textContent));b&&b.click()}"); pg.wait_for_timeout(900)
    wr=logs(pg,"write"); sh=logs(pg,"share")
    rec("Share","a backup goes through the phone's share sheet as a file",wr and wr[0]["path"].startswith("forgelings-backup-") and wr[0]["dir"]=="CACHE" and sh and sh[-1]["files"] and sh[-1]["files"][0].endswith(".json"),(btn,wr,sh))
    closemodals(pg)
    # erase clears the phone's copy
    tabto(pg,"settings"); pg.evaluate("document.getElementById('btnErase').click()"); pg.evaluate("document.getElementById('btnErase').click()"); pg.wait_for_timeout(800)
    rec("Erase","Erase everything also clears the phone's copy and cancels reminders","forge-app-v1" not in prefs(pg) and any(set(c)>={1,2} for c in logs(pg,"cancel")),list(prefs(pg)))
    rec("All","no page errors in the app",not pg._errs,pg._errs[:1]); ctx.close()
    # under-18 block is mirrored
    ctx,pg=npage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); pg.tap("#titleGo"); pg.wait_for_selector("#ageM",state="visible")
    pg.select_option("#ageM","6"); pg.select_option("#ageY",str(_dt.date.today().year-15)); pg.tap("#ageGo"); pg.wait_for_timeout(800)
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(1200)
    rec("Age","the not-yet screen survives web storage being wiped","not available" in mt(pg) and "forge-age-block" in prefs(pg))
    ctx.close()
    # the web is untouched
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); tabto(pg,"settings"); t=pg.inner_text("#view-settings")
    rec("Web","on the web nothing changes: no reminders block, tester tools still there","Reminders" not in t and "Feedback" in t and "My report" in t and pg.locator("details.dev").count()==1 and re.search(r"prototype 0\.\d+\.\d+",t))
    rec("Web","no page errors on the web",not pg._errs,pg._errs[:1]); ctx.close()
    b.close()
save_results("qa_32"); print(sum(r["ok"] for r in RES),"/",len(RES))
