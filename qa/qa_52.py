from lib import *
import base64, gzip
# 0.52: the iCloud copy (iPhone app), Android back button, backup and edge wording, and Android screen edges.
# The native app is played by a fake window.Capacitor injected before the page loads: Preferences and CloudSave keep
# their data in sessionStorage so it survives reloads; a new browser context is a new phone.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});return r.violations.map(v=>v.id+':'+v.nodes.length)}")
MOCK=r"""
(cfg=>{
  const ss=(k,d)=>{try{const v=sessionStorage.getItem(k);return v===null?d:JSON.parse(v);}catch(e){return d;}};
  const put=(k,v)=>{try{sessionStorage.setItem(k,JSON.stringify(v));}catch(e){}};
  if(sessionStorage.getItem('__seeded')!=='1'){put('__cloud',cfg.cloud||{});put('__prefs',cfg.prefs||{});
    if(cfg.local)for(const k in cfg.local)localStorage.setItem(k,cfg.local[k]);sessionStorage.setItem('__seeded','1');}
  window.__log=[];window.__lis={};
  const noop=new Proxy({},{get:(t,k)=>k==='then'?undefined:(()=>Promise.resolve({}))});
  const P={
    Preferences:{get:async({key})=>({value:ss('__prefs',{})[key]??null}),set:async({key,value})=>{const p=ss('__prefs',{});p[key]=value;put('__prefs',p);},remove:async({key})=>{const p=ss('__prefs',{});delete p[key];put('__prefs',p);}},
    Haptics:noop,LocalNotifications:noop,Share:noop,Filesystem:noop,
    App:{addListener:(e,f)=>{window.__lis[e]=f;return Promise.resolve({remove(){}});},minimizeApp:async()=>{window.__log.push('minimize');}}
  };
  if(cfg.icloud)P.CloudSave={
    status:async()=>({available:cfg.avail!==false}),
    get:async({key})=>{const c=ss('__cloud',{});return key in c?{value:c[key]}:{};},
    set:async({key,value})=>{const c=ss('__cloud',{});c[key]=value;put('__cloud',c);window.__log.push('set');},
    remove:async({key})=>{const c=ss('__cloud',{});delete c[key];put('__cloud',c);window.__log.push('remove');},
    addListener:(e,f)=>{window.__lis['cloud:'+e]=f;return Promise.resolve({remove(){}});}
  };
  window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>cfg.platform,Plugins:P};
})(%s);
"""
def phone(b,platform='ios',icloud=True,cloud=None,local=None,avail=True,w=390,h=844):
    ctx,pg=newpage(b,w,h); cfg={"platform":platform,"icloud":icloud,"cloud":cloud or {},"local":local or {},"avail":avail}
    ctx.add_init_script(MOCK%json.dumps(cfg)); pg.clock.install(time=datetime.datetime(2026,11,11,12,0)); return ctx,pg
def cloud(pg): return pg.evaluate("JSON.parse(sessionStorage.getItem('__cloud')||'{}')")
def unz(v):
    if v.startswith('j1:'): return json.loads(v[3:])
    return json.loads(gzip.decompress(base64.b64decode(v[4:])).decode())
def gz(o): return 'gz1:'+base64.b64encode(gzip.compress(json.dumps(o).encode())).decode()
def boot(pg):
    pg.goto(P); pg.wait_for_timeout(900)
def tick(pg,ms=5000): pg.clock.run_for(ms); pg.wait_for_timeout(400)
def settings(pg):
    tabto(pg,"settings"); pg.wait_for_timeout(200)
def errs(pg,label): rec("All",f"{label}: no page errors",not pg._errs,pg._errs[:3])

with sync_playwright() as p:
    b=p.chromium.launch()
    # ---- A. iPhone, empty iCloud: playing keeps a compressed copy there
    ctx,pg=phone(b); boot(pg); first_card(pg); closemodals(pg); tick(pg)
    c=cloud(pg); loc=st(pg)
    rec("iCloud","a save reaches iCloud a few seconds later, compressed",KEY in c and c[KEY].startswith('gz1:'),list(c)[:3])
    sv=unz(c[KEY]) if KEY in c else {}
    rec("iCloud","the iCloud copy is the same journal as the phone (jid, cards, save count)",sv.get('jid')==loc.get('jid') and len(sv.get('cards',[]))==len(loc['cards'])==1 and sv.get('_sv')==loc.get('_sv'),(sv.get('jid'),loc.get('jid')))
    rec("iCloud","every journal now has a journal id",isinstance(loc.get('jid'),str) and len(loc['jid'])>=6,loc.get('jid'))
    rec("iCloud","the copy is small (a first day under 3 KB)",len(c.get(KEY,''))<3000,len(c.get(KEY,'')))
    settings(pg); line=pg.inner_text("#cloudLine") if pg.locator("#cloudLine").count() else ""
    rec("Settings","Backup shows the iCloud copy and when it was last saved","own iCloud" in line and "Last saved just now" in line,line)
    rec("Settings","the iCloud button offers to turn it off",pg.inner_text("#btnCloud")=="Turn off the iCloud copy")
    rec("Settings","Erase says it clears iCloud too",pg.inner_text("#btnErase")=="Erase everything here and in iCloud")
    priv=pg.inner_text("#view-settings")
    rec("Privacy","the Settings privacy note mentions the iCloud copy","copy in your own iCloud" in priv and "can never see it" in priv)
    v=axe(pg); rec("A11y","Settings with the iCloud section has no accessibility violations",not v,v)
    bt=pg.locator("#btnCloud").bounding_box(); rec("A11y","the iCloud button is at least 44 points tall",bt and bt["height"]>=44,bt)
    pg.evaluate("document.getElementById('btnPrivacy').click()"); pg.wait_for_timeout(300); t=mt(pg)
    rec("Privacy","the full privacy note says where the iCloud copy lives and how to remove it","your own iCloud" in t and "only you can reach" in t and "removes it from iCloud" in t,t[:200])
    closemodals(pg); pg.screenshot(path=S+"/qa/shots/qa52_settings.png",full_page=False)
    gzv=c.get(KEY); first=loc
    errs(pg,"iPhone first day"); ctx.close()

    # ---- B. a new iPhone with an empty app: the journal comes back from iCloud, no age gate, no questions
    ctx,pg=phone(b,cloud={KEY:gzv}); boot(pg)
    l2=st(pg)
    rec("New phone","a new iPhone brings the journal back from iCloud",l2 and l2.get('jid')==first['jid'] and len(l2['cards'])==1,l2 and l2.get('jid'))
    rec("New phone","it opens straight onto Today (no age gate, no welcome)",pg.locator("#view-today").is_visible() and pg.locator("#ageM").count()==0 and not mt(pg),mt(pg)[:80])
    rec("New phone","the Forgeling found on the old phone is on the new one",pg.evaluate("document.querySelectorAll('#view-today canvas').length")>0)
    errs(pg,"new phone"); ctx.close()

    # ---- C. same journal: the newer save wins quietly, either way round
    newer=dict(first); newer['_sv']=first['_sv']+50; newer['cards']=first['cards']+[dict(first['cards'][0],id=first['cards'][0]['id']+1,name='Cloudborn')]
    ctx,pg=phone(b,cloud={KEY:gz(newer)},local={KEY:json.dumps(first)}); boot(pg)
    rec("Same journal","a newer iCloud save (same journal) replaces an older phone save quietly",len(st(pg)['cards'])==2 and not mt(pg),len(st(pg)['cards']))
    ctx.close()
    older=dict(first); older['_sv']=1
    ctx,pg=phone(b,cloud={KEY:gz(older)},local={KEY:json.dumps(newer)}); boot(pg); tick(pg)
    rec("Same journal","an older iCloud save never replaces a newer phone save",len(st(pg)['cards'])==2)
    rec("Same journal","the phone's newer save is sent up to iCloud",unz(cloud(pg)[KEY])['_sv']>=newer['_sv'],unz(cloud(pg)[KEY]).get('_sv'))
    # a change from iCloud while the app is open (another device): a newer save of the same journal is brought in
    newest=dict(newer); newest['_sv']=newer['_sv']+500; newest['cards']=newer['cards']+[dict(first['cards'][0],id=first['cards'][0]['id']+2,name='Latecomer')]
    pg.evaluate("v=>{const c=JSON.parse(sessionStorage.getItem('__cloud'));c['forge-app-v1']=v;sessionStorage.setItem('__cloud',JSON.stringify(c));}",gz(newest))
    with pg.expect_navigation(timeout=8000): pg.evaluate("window.__lis['cloud:change']({keys:['forge-app-v1'],reason:0})"); pg.clock.run_for(1000)
    pg.wait_for_timeout(900)
    rec("Same journal","a newer save arriving from iCloud while open is brought in",len(st(pg)['cards'])==3,len(st(pg)['cards']))
    errs(pg,"same journal"); ctx.close()

    # ---- D. two different journals: never swapped silently; the player chooses
    other=dict(newer); other['jid']='otherjournal1'; other['_sv']=9999; other['date']='2026-10-30'
    ctx,pg=phone(b,cloud={KEY:gz(other)},local={KEY:json.dumps(first)}); boot(pg); pg.clock.run_for(2000); pg.wait_for_timeout(500); t=mt(pg)
    rec("Two journals","a different journal in iCloud is offered, not swapped in",len(st(pg)['cards'])==1 and "A journal in your iCloud" in t and "2 Forgelings" in t and "1 Forgeling" in t,t[:220])
    rec("Two journals","the offer says when the iCloud journal was last opened","October 30, 2026" in t)
    tick(pg); rec("Two journals","nothing is sent to iCloud while the choice is open",unz(cloud(pg)[KEY])['jid']=='otherjournal1')
    v=axe(pg); rec("A11y","the choice sheet has no accessibility violations",not v,v)
    bb=[pg.locator(x).bounding_box()["height"] for x in ("#cloudUse","#cloudKeep","#cloudCopy")]; rec("A11y","its three buttons are at least 44 points tall",min(bb)>=44,bb)
    pg.screenshot(path=S+"/qa/shots/qa52_offer.png")
    pg.evaluate("document.getElementById('cloudKeep').click()"); tick(pg)
    rec("Two journals","Keep this phone's journal makes it the iCloud journal",unz(cloud(pg)[KEY])['jid']==first['jid'] and len(st(pg)['cards'])==1)
    ctx.close()
    ctx,pg=phone(b,cloud={KEY:gz(other)},local={KEY:json.dumps(first)}); boot(pg); pg.clock.run_for(2000); pg.wait_for_timeout(500)
    with pg.expect_navigation(timeout=8000): pg.evaluate("document.getElementById('cloudUse').click()"); pg.clock.run_for(1000)
    pg.wait_for_timeout(900); l=st(pg)
    rec("Two journals","Use the iCloud journal brings it in",l['jid']=='otherjournal1' and len(l['cards'])==2,l.get('jid'))
    rep_=pg.evaluate("JSON.parse(localStorage.getItem('forge-app-v1-replaced')||'null')")
    rec("Two journals","the phone's own journal is kept aside on the device, not thrown away",rep_ and rep_.get('jid')==first['jid'])
    rec("Two journals","no offer after choosing",not mt(pg))
    errs(pg,"two journals"); ctx.close()

    # ---- E. turning it off removes the iCloud copy; on again sends it back; erase clears iCloud
    ctx,pg=phone(b,cloud={KEY:gzv},local={KEY:json.dumps(first)}); boot(pg); settings(pg)
    pg.evaluate("document.getElementById('btnCloud').click()"); pg.wait_for_timeout(300); settings(pg)
    rec("Off","turning the iCloud copy off removes it from iCloud",KEY not in cloud(pg))
    rec("Off","Settings says it is off and offers to turn it on",pg.inner_text("#cloudLine").startswith("Off.") and pg.inner_text("#btnCloud")=="Keep a copy in iCloud")
    rec("Off","Erase goes back to this device only",pg.inner_text("#btnErase")=="Erase everything on this device")
    pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('forge-app-v1'));s.name='x';localStorage.setItem('forge-app-v1',JSON.stringify(s));}")
    tabto(pg,"today"); tick(pg); rec("Off","while off, nothing is sent to iCloud",KEY not in cloud(pg))
    pg.reload(); pg.wait_for_timeout(900); rec("Off","staying off survives a restart",KEY not in cloud(pg) and len(st(pg)['cards'])==1)
    settings(pg); pg.evaluate("document.getElementById('btnCloud').click()"); tick(pg)
    rec("On","turning it back on sends a copy straight away",KEY in cloud(pg))
    settings(pg); pg.evaluate("document.getElementById('btnErase').click()"); pg.evaluate("document.getElementById('btnErase').click()"); pg.wait_for_timeout(400)
    rec("Erase","Erase everything clears the iCloud copy",KEY not in cloud(pg))
    pg.reload(); pg.wait_for_timeout(1000)
    rec("Erase","after erasing, nothing comes back from iCloud (a fresh start)",pg.locator("#titleGo").count()>0 or pg.locator("#ageM").count()>0)
    errs(pg,"off, on, erase"); ctx.close()

    # ---- F. not signed in to iCloud: it says so, and nothing is sent
    ctx,pg=phone(b,avail=False,local={KEY:json.dumps(first)}); boot(pg); tick(pg); settings(pg)
    rec("Signed out","with no iCloud account it asks you to sign in","Sign in to iCloud" in pg.inner_text("#cloudLine"),pg.inner_text("#cloudLine"))
    rec("Signed out","and nothing is sent","set" not in pg.evaluate("window.__log"))
    errs(pg,"signed out"); ctx.close()

    # ---- G. Android: back button, Android backup wording, screen edges
    ctx,pg=phone(b,platform='android',icloud=False,local={KEY:json.dumps(first)}); boot(pg); settings(pg)
    t=pg.inner_text("#view-settings")
    rec("Android","Settings explains Android's own backup, and shows no iCloud controls","Android keeps a copy of Forgelings" in t and pg.locator("#btnCloud").count()==0)
    rec("Android","the privacy note mentions Android's backup","in Android’s own backup if that is on" in t)
    pg.evaluate("document.getElementById('btnPrivacy').click()"); pg.wait_for_timeout(300)
    rec("Android","the full privacy note describes Android's backup","Android also keeps a copy" in mt(pg))
    rec("Back","Android back button is handled by the app","backButton" in pg.evaluate("Object.keys(window.__lis)"))
    pg.evaluate("window.__lis.backButton()"); pg.wait_for_timeout(400)
    rec("Back","back closes an open sheet",pg.evaluate("document.getElementById('modal').hidden"))
    pg.evaluate("window.__lis.backButton()"); pg.wait_for_timeout(400)
    rec("Back","back from Settings goes to Today",pg.locator("#view-today").is_visible())
    pg.evaluate("window.__lis.backButton()"); pg.wait_for_timeout(200)
    rec("Back","back on Today leaves the app (to the background, nothing lost)",pg.evaluate("window.__log").count('minimize')==1)
    nav="document.querySelector('.tabs')"
    b0=pg.evaluate(f"parseFloat(getComputedStyle({nav}).paddingBottom)")
    pg.evaluate("document.documentElement.style.setProperty('--safe-area-inset-bottom','24px');document.documentElement.style.setProperty('--safe-area-inset-top','30px')"); pg.wait_for_timeout(100)
    b1=pg.evaluate(f"parseFloat(getComputedStyle({nav}).paddingBottom)")
    rec("Edges","the tab bar clears Android's gesture bar",abs((b1-b0)-24)<0.6,(b0,b1))
    tp=pg.evaluate("parseFloat(getComputedStyle(document.documentElement).paddingTop)")
    rec("Edges","the page clears Android's status bar",tp>=30,tp)
    v=axe(pg); rec("A11y","Android Settings has no accessibility violations",not v,v)
    errs(pg,"Android"); ctx.close()

    # ---- H. the website is unchanged: no iCloud, no Android wording
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); settings(pg)
    t=pg.inner_text("#view-settings")
    rec("Web","the website shows no iCloud or Android backup controls",pg.locator("#btnCloud").count()==0 and "Android" not in t and "iCloud" not in t)
    rec("Web","its privacy note still says only this device","Everything you do in Forgelings stays on this device. It has no accounts" in t)
    pg.evaluate("document.getElementById('btnPrivacy').click()"); pg.wait_for_timeout(300)
    rec("Web","the full privacy note is unchanged for the website","Only on this device, in this browser." in mt(pg) and "There is no other copy anywhere." in mt(pg))
    errs(pg,"website"); ctx.close()
    b.close()
ok=sum(r["ok"] for r in RES); print(f"{ok} / {len(RES)}")
json.dump(RES,open(S+"/qa/qa_52.json","w"),indent=1)
