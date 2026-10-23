from lib import *
# 0.35.0: the Forge. Embers from done days (two on all-in days), spares as ingredients, a Forge panel at the Hearth,
# charms worn by the fire and badged on the card, the bell, the compass, Hearth pieces, signed pieces. Real taps.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
def load(pg,s):
    s["opens"]=s.get("opens",[])+[s["date"]]  # the dev clock skipped days; an open today keeps the fire from sleeping
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
def embers(pg): return pg.evaluate("()=>{const t=document.getElementById('hEmbers');return t?+t.textContent.split(' ')[0]:-1}")
def forge_sheet(pg):
    tabto(pg,"hearth")
    if not pg.locator("#hForge").count(): print("DEBUG no hForge; modal:",mt(pg)[:200],"| hearth:",pg.inner_text("#view-hearth")[:200])
    pg.tap("#hForge"); pg.wait_for_timeout(400); return mt(pg)
def do_day(pg,allin=False):
    tabto(pg,"today"); pg.tap("#btnTurnGo"); pg.wait_for_selector("#vBack",state="visible"); pg.tap("#vBack"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{const o=document.getElementById('vOk');o&&o.click()}"); pg.wait_for_timeout(300); pg.tap("#btnAll" if allin else "#btnDone"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{const m=[...document.querySelectorAll('#modal [data-mood]')].find(b=>/mix/i.test(b.textContent));m&&m.click()}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{const c=document.getElementById('cover');c&&c.click()}"); pg.wait_for_selector("#rvSkip",state="visible",timeout=8000)
    t=pg.inner_text("#modal"); pg.tap("#rvSkip"); pg.wait_for_timeout(1500)
    for _ in range(4):
        if not mt(pg): break
        pg.evaluate("()=>{const b=document.querySelector('#modal [data-close]')||document.getElementById('rvDone');b&&b.click()}"); pg.wait_for_timeout(500)
    return t
with sync_playwright() as p:
    b=p.chromium.launch(); bad=[]
    ctx,pg=newpage(b); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
    # ---------- embers from showing up ----------
    tabto(pg,"hearth")
    rec("Panel","the Forge panel sits at the Hearth, with the ember count and Open the Forge",pg.locator("#view-hearth #hForge").count()==1 and "The Forge" in pg.inner_text("#view-hearth .forgep") and embers(pg)==1,embers(pg))
    s=st(pg); rec("Panel","a fresh save carries the forge record",isinstance(s.get("forge"),dict) and s["forge"]["spent"]==0 and s["forge"]["made"]==[])
    dev(pg,"next"); closemodals(pg); t=do_day(pg); tabto(pg,"hearth")
    rec("Embers","a done day adds one ember, and the reveal says so","An ember for the Forge" in t and embers(pg)==2,(t[:80],embers(pg)))
    dev(pg,"next"); closemodals(pg); t=do_day(pg,allin=True); tabto(pg,"hearth")
    rec("Embers","an all-in day adds two","Two embers for the Forge" in t and embers(pg)==4,embers(pg))
    dev(pg,"next"); closemodals(pg); tabto(pg,"today"); pg.tap("#btnTurnGo"); pg.wait_for_selector("#vBack",state="visible"); pg.tap("#vBack"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{const o=document.getElementById('vOk');o&&o.click()}"); pg.wait_for_timeout(300); pg.tap("#btnRest"); pg.wait_for_timeout(500); closemodals(pg); tabto(pg,"hearth")
    rec("Embers","a rest day adds none and takes none",embers(pg)==4)
    dev(pg,"next"); dev(pg,"next"); closemodals(pg); tabto(pg,"hearth")
    rec("Embers","missed days cost nothing",embers(pg)==4)
    # ---------- the sheet: every recipe visible, nothing affordable without spares ----------
    t=forge_sheet(pg)
    names=["Charm of Meadow","Charm of Ember","Charm of Tide","Charm of Frost","Charm of Dusk","Wanderer’s bell","Compass","A copper kettle","An iron stand","Wind chimes"]
    rec("Sheet","all ten recipes are listed, each saying what it needs",all(n in t for n in names) and t.count("Needs ")==10 and "0 of 10 pieces made" in t,t[:200])
    rec("Sheet","with no spares, nothing can be made yet, and the reason is shown",pg.locator("#modal [data-fmake]").count()==0 and "You have 0" in t)
    rec("Sheet","the sheet says who signs the piece",re.search(r"Today that is \S",t) is not None)
    bad+=["forge sheet: "+v for v in axe(pg)]
    closemodals(pg)
    # ---------- spares (the prototype tool), then a charm ----------
    dev(pg,"spares"); closemodals(pg); s=st(pg); known=[ti for ti in range(5) if any(c["theme"]==ti for c in s["cards"])]
    rec("Spares","the tool gives two spares of each curio from realms on the map",all(v["n"]>=3 for v in s["curios"].values()) and len(s["curios"])==4*len(known),(len(s["curios"]),known))
    tabto(pg,"hearth"); pg.evaluate("()=>{const d=document.querySelector('#view-hearth details.more');d&&(d.open=true)}"); pg.wait_for_timeout(200)
    sh=pg.inner_text("#view-hearth .shelf")
    rec("Spares","the shelf shows no counts",not re.search(r"\d",sh),sh[:80])
    cid=list(s["curios"].keys())[0]; pg.tap(f"#view-hearth [data-cur='{cid}']"); pg.wait_for_timeout(400); t=mt(pg)
    rec("Spares","a curio's close-up says how many you have and how many are spare","You have 3, 2 spare" in t and "never your last one" in t,t[:160]); closemodals(pg)
    t=forge_sheet(pg); ti=known[0]; cname=names[ti]
    rec("Make","with spares and embers, that realm's charm, the bell, the kettle, the stand and the chimes can be made",pg.locator(f"#modal [data-fmake='charm{ti}']").count()==1 and pg.locator("#modal [data-fmake='bell']").count()==1 and pg.locator("#modal [data-fmake='kettle']").count()==1,t[:100])
    unk=[x for x in range(5) if x not in known][0]
    rec("Make","the compass can be made with 4 embers, but a charm of a realm not on the map cannot",pg.locator("#modal [data-fmake='compass']").count()==1 and pg.locator(f"#modal [data-fmake='charm{unk}']").count()==0)
    smith=st(pg)["hearth"]["slots"]; before=st(pg)
    pg.tap(f"#modal [data-fmake='charm{ti}']"); pg.wait_for_timeout(600); t=mt(pg); s=st(pg)
    rec("Make","making a charm shows the piece, signed by the helper and dated",cname in t and "Forged by " in t and "Made with " in t and "2 embers" in t,t[:200])
    rec("Make","it costs two embers and two spares from that realm, never a last copy",s["forge"]["spent"]==2 and s["forge"]["made"]==[f"charm{ti}"] and sum(before["curios"][k]["n"]-s["curios"][k]["n"] for k in s["curios"])==2 and all(v["n"]>=1 for v in s["curios"].values()),s["forge"])
    L=s["forge"]["log"][f"charm{ti}"]; rec("Make","the signature is kept in the save",L["by"] and L["at"]==s["date"] and len(L["used"])==2,L)
    bad+=["made: "+v for v in axe(pg)]
    rec("Charm","the helper can put the charm on straight away",pg.locator(f"#modal [data-equip='charm{ti}']").count()==1)
    pg.tap(f"#modal [data-equip='charm{ti}']"); pg.wait_for_timeout(600); s=st(pg); wearer=[c for c in s["cards"] if c["keep"]==f"charm{ti}"]
    rec("Charm","…and wears it by the fire",len(wearer)==1 and not pg._errs,pg._errs[:1])
    tabto(pg,"hearth"); kc=pg.evaluate(f"()=>{{const b=document.querySelector('#view-hearth [data-keep=\"charm{ti}\"]');return b?[b.textContent,b.getAttribute('aria-pressed')]:null}}")
    rec("Charm","the charm joins the keepsake chips, and is the one worn",kc and kc[0]==cname and kc[1]=="true",kc)
    rec("Charm","the Hearth message says who helped","Forged with " in pg.inner_text("#hmsg"))
    hv=pg.evaluate("()=>{const cv=document.getElementById('hearthCv'),x=cv.getContext('2d'),d=x.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<d.length;i+=4){if(Math.abs(d[i]-0x4F)<12&&Math.abs(d[i+1]-0xA3)<12&&Math.abs(d[i+2]-0x6A)<12)n++;if(Math.abs(d[i]-0xFF)<8&&Math.abs(d[i+1]-0x8A)<12&&Math.abs(d[i+2]-0x2E)<12)n++;if(Math.abs(d[i]-0x4F)<10&&Math.abs(d[i+1]-0x93)<10&&Math.abs(d[i+2]-0xC8)<10)n++;if(Math.abs(d[i]-0xBF)<8&&Math.abs(d[i+1]-0xE6)<8&&Math.abs(d[i+2]-0xFF)<8)n++;if(Math.abs(d[i]-0x9B)<10&&Math.abs(d[i+1]-0x7B)<10&&Math.abs(d[i+2]-0xD8)<10)n++;}return n}")
    rec("Charm","the pendant is drawn on the Hearth scene (realm-coloured pixels present)",hv>=6,hv)
    # the card: badge in the corner, art untouched
    tabto(pg,"binder"); w=wearer[0]; pg.evaluate(f"()=>{{const c=document.querySelector('#view-binder .card[data-cid=\"{w['id']}\"]');c&&c.click()}}"); pg.wait_for_timeout(700)
    cb=pg.evaluate("()=>{const e=document.querySelector('#stage .card .chb');if(!e)return null;const r=e.getBoundingClientRect(),a=e.closest('.art').getBoundingClientRect();return {alt:e.alt,right:a.right-r.right,bottom:a.bottom-r.bottom,w:r.width,h:r.height,k:document.querySelector('#stage .pcv').dataset.k}}")
    rec("Card","the card shows a small charm badge in the corner of the art",cb and cb["alt"]==f"Wearing the {cname}" and 0<=cb["right"]<12 and 0<=cb["bottom"]<12 and cb["w"]<40,cb)
    rec("Card","the card art itself is drawn without the pendant (the key carries no keep)",cb and cb["k"].endswith(f"-{w['theme']}-") or (cb and cb["k"].endswith(f"-{w['theme']}-f")),cb and cb["k"])
    bad+=["card: "+v for v in axe(pg)]
    pg.evaluate("()=>{const b=document.getElementById('ovClose');b&&b.click()}"); closemodals(pg)
    # ---------- the bell ----------
    s=st(pg); s["forge"]["spent"]=0; load(pg,s)
    t=forge_sheet(pg); pg.tap("#modal [data-fmake='bell']"); pg.wait_for_timeout(500); t=mt(pg)
    rec("Bell","the bell can be made (3 embers, 2 spares from anywhere)","Wanderer’s bell" in t and "Forged by" in t and st(pg)["forge"]["spent"]==3,t[:120]); closemodals(pg)
    tabto(pg,"hearth"); pg.tap("#hWander"); pg.wait_for_timeout(400); pg.evaluate("()=>{const b=document.querySelector('#modal [data-wgo=\"-1\"]');b&&b.click()}"); pg.wait_for_timeout(600)
    rec("Bell","with a wanderer out, Ring the bell is offered",pg.locator("#view-hearth #hBell").count()==1 and "out wandering" in pg.inner_text("#view-hearth"))
    pg.tap("#hBell"); pg.wait_for_timeout(900); s=st(pg)
    rec("Bell","ringing it brings the wanderer home now, once a day",s["forge"]["bell"]==s["date"] and pg.locator("#view-hearth #hCollect").count()==1 and pg.locator("#hBell").count()==0,(s["forge"]["bell"],s["date"]))
    pg.tap("#hCollect"); pg.wait_for_timeout(800); closemodals(pg); tabto(pg,"hearth"); pg.tap("#hWander"); pg.wait_for_timeout(400); pg.evaluate("()=>{const b=document.querySelector('#modal [data-wgo=\"-1\"]');b&&b.click()}"); pg.wait_for_timeout(600)
    rec("Bell","a second wander the same day says the bell has rung today",pg.locator("#hBell").count()==0 and "The bell has rung today" in pg.inner_text("#view-hearth"))
    dev(pg,"wander"); closemodals(pg); tabto(pg,"hearth"); pg.evaluate("()=>{const b=document.getElementById('hCollect');b&&b.click()}"); pg.wait_for_timeout(800); closemodals(pg)
    # ---------- the compass ----------
    s=st(pg); s["forge"]["spent"]=0; load(pg,s); t=forge_sheet(pg); pg.tap("#modal [data-fmake='compass']"); pg.wait_for_timeout(500); closemodals(pg); tabto(pg,"hearth")
    rec("Compass","once made, the Forge panel offers Ask the compass",pg.locator("#view-hearth #hCompass").count()==1)
    pg.tap("#hCompass"); pg.wait_for_timeout(400); line=pg.inner_text("#hCompLine"); s=st(pg)
    rec("Compass","the needle settles toward a realm with something unfound, with no counts","The needle settles toward" in line and s["forge"]["compTo"] in known and not re.search(r"\d",line),line)
    rec("Compass","it answers once a day, so the button is gone",pg.locator("#hCompass").count()==0)
    pg.tap("#hWander"); pg.wait_for_timeout(400); t=mt(pg)
    rec("Compass","the wander sheet marks that realm: The compass points here",t.count("The compass points here")==1,t[:200]); closemodals(pg)
    s=st(pg); s["forge"]["comp"]=""; s["explore"]={str(ti):4 for ti in known}
    load(pg,s); tabto(pg,"hearth")
    # all curios found in known realms? the spares tool gave every curio of known realms, and explore is full, so nothing is unfound
    pg.tap("#hCompass"); pg.wait_for_timeout(400); line=pg.inner_text("#hCompLine")
    rec("Compass","with nothing left unfound on the map, the needle spins and rests","Nothing on your map is left unfound" in line,line)
    # ---------- Hearth pieces, and the keep tally ----------
    for pid in ("kettle","stand","chimes"):
        dev(pg,"spares"); closemodals(pg)  # top up spares, so the run never depends on how many realms this save knows
        s=st(pg); s["forge"]["spent"]=0; load(pg,s)
        forge_sheet(pg); pg.tap(f"#modal [data-fmake='{pid}']"); pg.wait_for_timeout(500); closemodals(pg)
    s=st(pg); tabto(pg,"hearth")
    rec("Hearth","kettle, stand and chimes are made and listed as forged",all(x in s["forge"]["made"] for x in ("kettle","stand","chimes")) and "6 of 10 pieces made" in pg.inner_text("#view-hearth .forgep"))
    pm=pg.evaluate("async()=>{const cv=document.getElementById('hearthCv'),x=cv.getContext('2d');const px=(X,Y)=>Array.from(x.getImageData(X,Y,1,1).data).slice(0,3);const diff=(a,b)=>Math.max(...a.map((v,i)=>Math.abs(v-b[i])));let best=0,kettle=false;for(let s=0;s<8;s++){let legs=0;for(let y=55;y<=57;y++){if(diff(px(57,y),px(55,y))>12&&diff(px(71,y),px(73,y))>12)legs++;}best=Math.max(best,legs);const k=px(78,58);if(k[0]>k[1]&&k[1]>k[2]&&k[0]<240)kettle=true;await new Promise(r=>setTimeout(r,120));}return [best,kettle]}")
    rec("Hearth","the iron stand's legs and the copper kettle are drawn into the fire scene (sampled over a second, past the sparks)",pm[0]==3 and pm[1],pm)
    t=forge_sheet(pg)
    rec("Hearth","made pieces show their signature instead of a Make button",t.count("Forged by ")==6 and pg.locator("#modal [data-fmake]").count()<=4 and pg.locator("#modal [data-fmake='kettle'],#modal [data-fmake='bell'],#modal [data-fmake='compass']").count()==0,t.count("Forged by "))
    closemodals(pg); tabto(pg,"chronicle"); pg.evaluate("()=>{const b=document.querySelector('[data-sub=\"journal\"]');b&&b.click()}"); pg.wait_for_timeout(400); rb=pg.inner_text("#view-chronicle")
    rec("Ribbons","the ribbons list names First Forging and Smith","First Forging" in rb and "Smith" in rb)
    # ---------- older saves, damaged saves ----------
    s=st(pg); del s["forge"]; load(pg,s); s2=st(pg); tabto(pg,"hearth")
    rec("Migrate","a save without the Forge gets one, with embers for every day shown up so far",s2["forge"]["spent"]==0 and s2["forge"]["made"]==[] and embers(pg)==4,(s2["forge"],embers(pg)))
    s=st(pg); s["forge"]={"spent":-3,"made":["kettle","kettle",5],"log":"x","bell":3}; load(pg,s); s2=st(pg)
    rec("Damaged","broken forge data is repaired",s2["forge"]["spent"]==0 and s2["forge"]["made"]==["kettle"] and s2["forge"]["log"]=={} and s2["forge"]["bell"]=="" and not pg._errs,s2["forge"])
    rec("Copy","no screen calls the app plain Forge",not re.search(r"(?<![Tt]he )(?<![Ee]very )\bForge\b(?!ling|bound)",pg.inner_text("#view-hearth")+forge_sheet(pg)))
    closemodals(pg)
    rec("A11y","axe: zero violations on the Forge sheet, the made sheet and the badged card",not bad,bad[:3])
    rec("All","no page errors",not pg._errs,pg._errs[:1]); b.close()
save_results("qa_35"); print(sum(r["ok"] for r in RES),"/",len(RES))
