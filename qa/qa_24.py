from lib import *
# 0.24.0: share a Forgeling picture, the backup nudge and file save/restore, calling variety, your own small thing.
import datetime, base64
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
JUNK=re.compile(r"undefined|NaN|\[object|\bnull\b|Infinity")
SRC=open(P.replace("file://","")).read() if P.startswith("file://") else open(S+"/work.html").read()
TASKS=re.findall(r"task:`([^`]*)`",SRC)
ALT=[re.findall(r"`([^`]*)`",row) for row in re.findall(r"\n \[(`.*?`)\]",SRC.split("const TASK_ALT=[")[1].split("function taskFor")[0])]
PHR=[[TASKS[i]]+ALT[i] for i in range(12)]
def ready(pg,s): setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def D(s,n): return (datetime.date.fromisoformat(s["date"])-datetime.timedelta(days=n)).isoformat()
def grown(base,cards=(2,2,2,1,1),age=12):
    s=build(base,list(cards)); s["seen"]=99; s["startDate"]=D(s,age); s["backup"]={"at":"","ask":""}; s["own"]={"text":"","days":[]}; return s
SHARE_STUB="""()=>{window.__shared=[];navigator.canShare=()=>true;navigator.share=d=>{window.__shared.push({title:d.title,files:(d.files||[]).map(f=>[f.name,f.type,f.size])});return Promise.resolve();};}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b,390,844,accept_downloads=True); pg.set_default_timeout(8000); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    _v=re.search(r"const VERSION='prototype (\d+)\.(\d+)",pg.content()); rec("Version","the app is 0.24 or later",_v and (int(_v.group(1)),int(_v.group(2)))>=(0,24))
    rec("Variety","every calling has at least 4 phrasings, all different",len(PHR)==12 and all(len(x)>=4 and len(set(x))==len(x) for x in PHR),[len(x) for x in PHR])

    # ---------- share ----------
    s=grown(base); s["cards"][1]["nick"]="Pip"; s["cards"][2]["source"]="pack"; s["cards"][3]["rarity"]=4; ready(pg,s)
    cid=s["cards"][1]["id"]; tabto(pg,"binder"); pg.evaluate("id=>document.querySelector('#view-binder [data-insp=\"'+id+'\"]').click()",cid); pg.wait_for_timeout(600)
    h=pg.evaluate("()=>{const b=document.getElementById('inspShare');return b?Math.round(b.getBoundingClientRect().height):0}")
    rec("Share","a Forgeling's card has a Share button, easy to tap",h>=44,h)
    pg.evaluate("document.getElementById('inspShare').click()"); pg.wait_for_selector("#shareImg")
    info=pg.evaluate("""async()=>{const im=document.getElementById('shareImg');await im.decode();const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);
      const px=(a,b)=>Array.from(x.getImageData(a,b,1,1).data).slice(0,3);const art=new Set();for(let i=0;i<40;i++){const p=px(80+i*14,90+i*10);art.add(p.join(','));}
      return {w:im.naturalWidth,h:im.naturalHeight,src:im.src.slice(0,22),alt:im.alt,rivet:px(30,30),bg:px(100,850),art:art.size}}""")
    rec("Share","the picture is a 720×960 PNG made on the phone",info["w"]==720 and info["h"]==960 and info["src"]=="data:image/png;base64,",info)
    rec("Share","it shows the Forgeling's art (many colours), gold corner rivets and the night background",info["art"]>=6 and info["rivet"]==[226,176,74] and info["bg"][2]>info["bg"][1],info)
    rec("Share","the picture has a description for screen readers",info["alt"].startswith("A picture card of Pip") and "Meadow" in info["alt"],info["alt"])
    m=mt(pg); rec("Share","it says nothing is uploaded","nothing is uploaded" in m and not JUNK.search(m),m[:140])
    with pg.expect_download() as dl: pg.evaluate("document.getElementById('shDo').click()")
    rec("Share","without a share sheet, Save picture downloads it as a PNG named after the Forgeling",dl.value.suggested_filename=="Pip.png" and pg.inner_text("#shDo")=="Save picture",dl.value.suggested_filename)
    pg.evaluate("document.getElementById('shBack').click()"); pg.wait_for_timeout(500)
    rec("Share","Back returns to the card",pg.locator("#inspShare").count()==1 and pg.locator("#shareImg").count()==0)
    pg.evaluate(SHARE_STUB); pg.evaluate("document.getElementById('inspShare').click()"); pg.wait_for_selector("#shareImg"); pg.wait_for_timeout(200)
    lab=pg.inner_text("#shDo"); pg.evaluate("document.getElementById('shDo').click()"); pg.wait_for_timeout(400); sh=pg.evaluate("window.__shared")
    rec("Share","with a share sheet, Share sends the PNG file through it",lab=="Share" and sh and sh[0]["files"][0][0]=="Pip.png" and sh[0]["files"][0][1]=="image/png" and sh[0]["files"][0][2]>5000,(lab,sh))
    pg.evaluate("()=>{navigator.share=()=>Promise.reject(Object.assign(new Error('no'),{name:'NotAllowedError'}));}")
    with pg.expect_download() as dl: pg.evaluate("document.getElementById('shDo').click()")
    rec("Share","if the share sheet fails, it falls back to saving the picture",dl.value.suggested_filename=="Pip.png")
    pg.evaluate("()=>{navigator.share=()=>Promise.reject(Object.assign(new Error('x'),{name:'AbortError'}));}"); n0=len(pg._errs)
    got=[]; pg.on("download",lambda d:got.append(d)); pg.evaluate("document.getElementById('shDo').click()"); pg.wait_for_timeout(600)
    rec("Share","cancelling the share sheet does nothing else",not got and len(pg._errs)==n0)
    closemodals(pg); pg.evaluate("()=>{const c=document.getElementById('ovClose');if(c)c.click()}")
    for i in (2,3):
        tabto(pg,"binder"); pg.evaluate("id=>document.querySelector('#view-binder [data-insp=\"'+id+'\"]').click()",s["cards"][i]["id"]); pg.wait_for_timeout(400)
        pg.evaluate("document.getElementById('inspShare').click()"); pg.wait_for_selector("#shareImg"); pg.wait_for_timeout(200)
        rec("Share",f"pack and legendary Forgelings share too ({['','','pack','legend'][i]})",pg.evaluate("document.getElementById('shareImg').naturalWidth")==720 and not pg._errs,pg._errs[:1])
        closemodals(pg); pg.evaluate("()=>{const c=document.getElementById('ovClose');if(c)c.click()}")

    # ---------- backup nudge ----------
    ready(pg,grown(base,(1,1,1,1,0)))
    rec("Backup","no nudge with fewer than 5 Forgelings",pg.locator("#btnBackup").count()==0)
    ready(pg,grown(base,age=4))
    rec("Backup","no nudge in the first week",pg.locator("#btnBackup").count()==0)
    s=grown(base); ready(pg,s)
    rec("Backup","from day 7 with 5+ Forgelings, Today offers to save a copy",pg.locator("#btnBackup").count()==1 and "Save a copy" in pg.inner_text("#btnBackup"))
    rec("Backup","the nudge is the last row, after the Hearth and Map",pg.evaluate("()=>{const r=[...document.querySelectorAll('#view-today .group .rowl')];return r[r.length-1].id}")=="btnBackup")
    pg.evaluate("document.getElementById('btnBackup').click()"); pg.wait_for_timeout(400); m=mt(pg)
    rec("Backup","it explains why, gently","only on this phone" in m and pg.locator("#saveFile").count()==1 and pg.locator("#backupLater").count()==1,m[:120])
    with pg.expect_download() as dl: pg.evaluate("document.getElementById('saveFile').click()")
    f=dl.value; data=json.loads(open(f.path()).read()); pg.wait_for_timeout(400)
    rec("Backup","Save a copy downloads a dated .json file holding the whole collection",f.suggested_filename==f"forgelings-backup-{s['date']}.json" and len(data["cards"])==len(s["cards"]) and data["v"]==1,f.suggested_filename)
    rec("Backup","saving records the date and the nudge goes away",st(pg)["backup"]["at"]==s["date"] and pg.locator("#btnBackup").count()==0 and pg.evaluate("document.getElementById('modal').hidden"))
    BK=f.path()
    s2=st(pg); s2["backup"]={"at":D(s2,29),"ask":""}; ready(pg,s2)
    rec("Backup","no nudge within a month of the last copy",pg.locator("#btnBackup").count()==0)
    s2["backup"]={"at":D(s2,30),"ask":""}; ready(pg,s2)
    rec("Backup","a month after the last copy, it asks again",pg.locator("#btnBackup").count()==1)
    pg.evaluate("document.getElementById('btnBackup').click()"); pg.wait_for_timeout(300); pg.evaluate("document.getElementById('backupLater').click()"); pg.wait_for_timeout(400)
    rec("Backup","Remind me next month hides it for a month",st(pg)["backup"]["ask"]==s2["date"] and pg.locator("#btnBackup").count()==0)
    s2=st(pg); s2["backup"]={"at":D(s2,90),"ask":D(s2,30)}; ready(pg,s2)
    rec("Backup","…and a month later it comes back",pg.locator("#btnBackup").count()==1)
    pg.evaluate(SHARE_STUB); pg.evaluate("document.getElementById('btnBackup').click()"); pg.wait_for_timeout(300); pg.evaluate("document.getElementById('saveFile').click()"); pg.wait_for_timeout(500); sh=pg.evaluate("window.__shared")
    rec("Backup","with a share sheet, the copy goes through it as a JSON file",sh and sh[0]["files"][0][0].startswith("forgelings-backup-") and sh[0]["files"][0][1]=="application/json" and st(pg)["backup"]["at"]==s2["date"],sh)
    # settings
    pg.reload(); pg.wait_for_timeout(700); closemodals(pg); tabto(pg,"settings"); pg.evaluate("document.getElementById('btnExport').click()"); pg.wait_for_timeout(300)
    rec("Backup","Settings > Save a copy offers a file first, and the text second",pg.locator("#saveFile").count()==1 and pg.locator("#expText").count()==1 and pg.inner_text("#saveFile")=="Save as a file")
    s3=st(pg); s3["backup"]={"at":"","ask":""}; setst(pg,s3); pg.evaluate("document.getElementById('copyExp').click()"); pg.wait_for_timeout(300)
    rec("Backup","copying the text also counts as a backup",st(pg)["backup"]["at"]==s3["date"])
    closemodals(pg)
    # restore from a file
    cur=st(pg); cur["cards"]=cur["cards"][:2]; cur["backup"]={"at":"","ask":""}; ready(pg,cur); tabto(pg,"settings")
    pg.evaluate("document.getElementById('btnRestore').click()"); pg.wait_for_timeout(300)
    hh=pg.evaluate("Math.round(document.querySelector('.filepick').getBoundingClientRect().height)")
    rec("Restore","Restore has a Choose a saved file button, easy to tap",hh>=44,hh)
    pg.set_input_files("#resFile",BK); pg.wait_for_timeout(600)
    rec("Restore","choosing a file fills in the copy",len(pg.input_value("#resText"))>500 and pg.evaluate("document.activeElement.id")=="doRestore")
    pg.evaluate("document.getElementById('doRestore').click()"); pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(800)
    rec("Restore","…and Restore brings the saved collection back",len(st(pg)["cards"])==len(s["cards"]) and not pg._errs,(len(st(pg)["cards"]),pg._errs[:1]))
    tabto(pg,"settings"); pg.evaluate("document.getElementById('btnRestore').click()"); pg.wait_for_timeout(300)
    bad=S+"/qa/_bad.json"; open(bad,"w").write('{"hello":1}'); n=len(st(pg)["cards"])
    pg.set_input_files("#resFile",bad); pg.wait_for_timeout(500); pg.evaluate("document.getElementById('doRestore').click()"); pg.evaluate("document.getElementById('doRestore').click()"); pg.wait_for_timeout(500)
    rec("Restore","a file that isn't a Forge copy changes nothing",len(st(pg)["cards"])==n and "does not look like a saved copy" in pg.inner_text("#toast"),pg.inner_text("#toast"))
    os.remove(bad); closemodals(pg)

    # ---------- calling variety ----------
    seen=set(); bad=[]
    for i in range(14):
        day=datetime.date(2026,11,1)+datetime.timedelta(days=i*3); k=day.isoformat()
        c2,p2=newpage(b); p2.clock.set_fixed_time(datetime.datetime(day.year,day.month,day.day,10,0)); p2.goto(P); p2.wait_for_timeout(300)
        ss=grown(base); ss["date"]=k; ss["startDate"]=(day-datetime.timedelta(days=10)).isoformat(); ss["history"]=[]; ss["todayV"]=i%12; ss["status"]="revealed"; ss["seen"]=99
        setst(p2,ss); p2.reload(); p2.wait_for_timeout(700); closemodals(p2)
        hero=p2.inner_text("#view-today .taskface p"); p2.evaluate("document.getElementById('btnCard').click()"); p2.wait_for_timeout(500)
        front=p2.evaluate("()=>{const p=[...document.querySelectorAll('.vbody p')].find(x=>x.innerText.startsWith(\"Today's small thing\"));return p?p.innerText.replace(\"Today's small thing\",'').trim():''}")
        if hero not in PHR[i%12] or front!=hero: bad.append((k,i%12,hero,front))
        if i%12==0 or True: seen.add((i%12,hero))
        c2.close()
    rec("Variety","the card front and Today show the same phrasing, always one of that calling's",not bad,bad[:2])
    c2,p2=newpage(b); p2.goto(P); p2.wait_for_timeout(300); texts=set()
    for i in range(10):
        day=datetime.date(2026,12,1)+datetime.timedelta(days=i); p2.clock.set_fixed_time(datetime.datetime(day.year,day.month,day.day,10,0))
        ss=grown(base); ss["date"]=day.isoformat(); ss["startDate"]=(day-datetime.timedelta(days=10)).isoformat(); ss["history"]=[]; ss["todayV"]=4; ss["status"]="revealed"
        setst(p2,ss); p2.reload(); p2.wait_for_timeout(500); closemodals(p2); texts.add(p2.inner_text("#view-today .taskface p"))
    rec("Variety","over ten days the same calling is asked in at least 3 different ways",len(texts)>=3,texts); c2.close()

    # ---------- your own small things: since 0.36 they live on the card (qa_36). The Journal still marks their days ----------
    s=grown(base); s["history"]=[{"date":D(s,i),"status":"done","v":i%12} for i in range(1,11)]; s["owns"]=[{"id":1,"text":"Drink a glass of water","k":-1,"days":[D(s,i) for i in (0,1,3,5,40)]}]; ready(pg,s)
    rec("Own","Today has no separate tick row any more (own small things come up on the card)",pg.locator("#btnOwn").count()==0)
    tabto(pg,"chronicle"); pg.evaluate("()=>{const b=document.querySelector('#view-chronicle [data-sub=\"journal\"]');if(b)b.click()}"); pg.wait_for_timeout(500)
    own=pg.evaluate("[...document.querySelectorAll('.cal .c.own')].map(c=>c.getAttribute('aria-label'))"); txt=pg.inner_text("#view-chronicle")
    rec("Own","the Journal calendar marks the days you did one (within five weeks)",len(own)==4 and all("your own small thing done" in a for a in own),own)
    rec("Own","…and says how many",("You did your own small thing on 4 of these days" in txt) and "your own small thing" in pg.inner_text(".calkey"),[l for l in txt.split("\n") if "own small" in l])
    # damaged
    for bad in ("x",None,[1],{"text":5,"days":"no"},{"text":"ok","days":["2026-01-01","2026-01-01","nope",7]}):
        s=st(pg); s["own"]=bad; s["backup"]=bad; ready(pg,s); o=st(pg)["own"]; bk=st(pg)["backup"]
        rec("Damaged",f"damaged own/backup records ({bad!r}) are repaired",isinstance(o,dict) and isinstance(o["text"],str) and isinstance(o["days"],list) and all(re.match(r"^\d{4}-\d{2}-\d{2}$",d) for d in o["days"]) and len(o["days"])==len(set(o["days"])) and set(bk)=={"at","ask"} and not pg._errs,(o,bk,pg._errs[:1]))
    s=st(pg); del s["own"]; del s["backup"]; ready(pg,s)
    rec("Damaged","an older save without these fields picks them up",st(pg)["own"]=={"text":"","days":[]} and st(pg)["backup"]=={"at":"","ask":""})
    # what's new
    s=st(pg); s["seen"]=27; ready(pg,s); pg.wait_for_timeout(300)
    s=st(pg); s["seen"]=27; setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); m=mt(pg)
    rec("New","What is new opens for an older save, newest first, and keeps the list short",bool(m) and "What is new" in m and pg.locator("#modal .newlist li").count()<=8 and st(pg)["seen"]>=28,m[:100].replace("\n"," | "))
    rec("All","no page errors",not pg._errs,pg._errs[:2]); ctx.close()

    # ---------- layout and accessibility ----------
    AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read(); badv=[]
    def axe(pg,where):
        pg.evaluate(AXE); v=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
        badv.extend(f"{where}: {x}" for x in v)
    for scheme in ("light","dark"):
        for w in (320,430):
            ctx,pg=newpage(b,w,700 if w==320 else 932,color_scheme=scheme); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
            s=grown(base); s["own"]={"text":"Drink a glass of water","days":[]}; ready(pg,s); pg.wait_for_function("!document.body.classList.contains('arrive')")
            hs=lambda:pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
            small=pg.evaluate("[...document.querySelectorAll('#btnOwn,#btnBackup')].map(b=>Math.round(b.getBoundingClientRect().height)).filter(h=>h<44)")
            rec("Layout",f"{scheme} {w}px: Today with your own thing and the backup row fits, and both are easy to tap",not hs() and not small,small)
            if w==430: axe(pg,f"{scheme} Today")
            tabto(pg,"binder"); pg.evaluate("()=>document.querySelector('#view-binder [data-insp]').click()"); pg.wait_for_timeout(600)
            tops=pg.evaluate("[...new Set([...document.querySelectorAll('#inspFav,#modal [data-tale],#inspShare,#ovClose')].map(b=>Math.round(b.getBoundingClientRect().top)))].length")
            rec("Layout",f"{scheme} {w}px: Favorite, Story, Share and Close sit on one line",tops==1,tops)
            pg.evaluate("document.getElementById('inspShare').click()"); pg.wait_for_selector("#shareImg"); pg.wait_for_timeout(300)
            iw=pg.evaluate("Math.round(document.getElementById('shareImg').getBoundingClientRect().width)")
            rec("Layout",f"{scheme} {w}px: the share preview fits the screen",not hs() and 0<iw<=w-24,iw)
            if w==430: pg.wait_for_function("!document.body.classList.contains('arrive')"); axe(pg,f"{scheme} share")
            closemodals(pg); pg.evaluate("()=>{const c=document.getElementById('shBack');if(c)c.click()}"); pg.wait_for_timeout(300); closemodals(pg); pg.evaluate("()=>{const c=document.getElementById('ovClose');if(c)c.click()}")
            tabto(pg,"settings"); rec("Layout",f"{scheme} {w}px: Settings fits",not hs())
            if w==430:
                axe(pg,f"{scheme} settings"); pg.evaluate("document.getElementById('btnRestore').click()"); pg.wait_for_timeout(400); axe(pg,f"{scheme} restore"); closemodals(pg)
                pg.evaluate("document.getElementById('btnExport').click()"); pg.wait_for_timeout(400); axe(pg,f"{scheme} export"); closemodals(pg)
                tabto(pg,"today"); pg.evaluate("document.getElementById('btnBackup').click()"); pg.wait_for_timeout(400); axe(pg,f"{scheme} nudge"); closemodals(pg)
            rec("All",f"{scheme} {w}px: no page errors",not pg._errs,pg._errs[:1]); ctx.close()
    rec("A11y","axe: zero violations on Today, the share picture, Settings, Restore, Save a copy and the nudge, light and dark",not badv,badv[:4])
    b.close()
save_results("qa_24"); print(sum(r["ok"] for r in RES),"/",len(RES))
