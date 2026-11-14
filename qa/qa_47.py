from lib import *
import datetime
# 0.47: the rest of the journal. Hearth photo, letter, note, ink boxes and index; Forge sorted Ready / Still / Made;
# the close-up as a journal page; Settings bookplate; sheets in paper; and Today's tape clear of the date line.
AXE=open(S+'/qa/node_modules/axe-core/axe.min.js').read()
def axe(pg): pg.evaluate(AXE); return pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>v.id+':'+v.nodes[0].html.slice(0,80))}")
with sync_playwright() as p:
    b=p.chromium.launch()
    for hr in (11,22):
        ctx,pg=newpage(b); pg.clock.set_fixed_time(datetime.datetime(2026,10,22,hr,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
        tape=pg.evaluate("()=>{const c=document.querySelector('#view-today .herocard');if(!c)return null;const t=parseFloat(getComputedStyle(c,'::before').top),r=c.getBoundingClientRect(),d=document.getElementById('dateLabel').getBoundingClientRect();return [Math.round(r.top+t),Math.round(d.bottom)]}")
        tag="day" if hr==11 else "lamp"
        rec("Today",f"{tag}: the tape on today's find stays below the date line",tape and tape[0]>=tape[1],tape)
        s=st(pg); s["seen"]=99; c0=s["cards"][0]
        t0=datetime.date.fromisoformat(s["date"]); s["history"]=[{"date":(t0-datetime.timedelta(days=d)).isoformat(),"status":"done","v":0,"card":c0["id"],"note":"","allIn":False} for d in range(8,0,-1)]+s["history"]
        for i in range(3):
            c=json.loads(json.dumps(c0)); c.update(id=700+i,seed=5100+i*733); s["cards"].append(c)
        ids=[c["id"] for c in s["cards"]]; s["hearth"]["slots"]=ids[:2]; s["hearth"]["sleep"]=None; s["request"]={"cid":ids[0],"realm":2,"made":s["date"]}
        s["curios"]={"acorn":{"n":3,"cid":ids[0],"at":s["date"]},"flower":{"n":1,"cid":ids[0],"at":s["date"]}}
        setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
        tag="day" if hr==11 else "lamp"
        # Hearth
        tabto(pg,"hearth")
        h=pg.evaluate("""()=>{const w=getComputedStyle(document.querySelector('#view-hearth .hearthwrap')),a=getComputedStyle(document.querySelector('#view-hearth .act')),l=document.querySelector('#view-hearth .tale.new')||document.querySelector('#view-hearth .tale'),ix=[...document.querySelectorAll('#view-hearth .hmore .chip')].map(c=>Math.round(c.getBoundingClientRect().width)),hm=document.querySelector('#view-hearth .hmore').getBoundingClientRect().width;
          return {photo:w.borderRadius==='0px'&&w.paddingTop==='7px',box:a.borderRadius==='0px'&&a.borderTopStyle==='solid'&&a.backgroundColor==='rgba(0, 0, 0, 0)',letter:!!l&&getComputedStyle(l,'::before').borderRadius==='50%',index:ix.length>=3&&ix.every(x=>x>=hm-4)}}""")
        rec("Hearth",f"{tag}: the fire is a taped-in photo, the request a sealed letter, the actions ink boxes, the lists an index",all(h.values()),h)
        rec("Hearth",f"{tag}: the index rows are 44-point targets",pg.evaluate("[...document.querySelectorAll('#view-hearth .hmore .chip')].every(c=>c.getBoundingClientRect().height>=43.5)"))
        v=axe(pg); rec("A11y",f"{tag}: the Hearth has no accessibility violations",not v,v)
        # Forge: Ready, Still, Made
        pg.evaluate("document.getElementById('hForge').click()"); pg.wait_for_timeout(500)
        fo=pg.evaluate("()=>[...document.querySelectorAll('#modal .forgel li')].map(li=>li.classList.contains('fgsec')?'#'+li.textContent:li.className||'-')")
        heads=[x for x in fo if x.startswith('#')]
        first_can=fo.index('can') if 'can' in fo else -1
        rec("Forge",f"{tag}: what you can make comes first, under Ready to make, then Still to make",heads[:2]==["#Ready to make","#Still to make"] and 0<first_can<fo.index("#Still to make") and all(x!='can' for x in fo[fo.index("#Still to make"):]),fo[:6])
        rec("Forge",f"{tag}: the headings are not read as pieces",pg.evaluate("[...document.querySelectorAll('#modal .forgel li.fgsec')].every(li=>!li.querySelector('b,button'))"))
        v=axe(pg); rec("A11y",f"{tag}: the sorted Forge has no accessibility violations",not v,v)
        closemodals(pg)
        # the close-up
        tabto(pg,"binder"); pg.evaluate("document.querySelector('#view-binder [data-insp]').click()"); pg.wait_for_timeout(700)
        ci=pg.evaluate("()=>{const s=document.querySelector('.scrim'),o=document.querySelector('.scrim .ov'),cv=document.querySelector('.scrim .stageCv');return [s.classList.contains('jinsp'),getComputedStyle(o).backgroundImage.includes('gradient'),!cv||getComputedStyle(cv).display==='none',getComputedStyle(document.querySelector('.scrim .rv-title')).fontFamily]}")
        rec("Card",f"{tag}: a Forgeling opens on a journal page, its name handwritten, with no starfield",ci[0] and ci[1] and ci[2] and ci[3].startswith("Caveat"),ci)
        v=axe(pg); rec("A11y",f"{tag}: the close-up page has no accessibility violations",not v,v)
        pg.evaluate("document.getElementById('ovClose').click()"); pg.wait_for_timeout(300)
        # Settings bookplate
        tabto(pg,"settings",fold=True); t=pg.inner_text("#view-settings .jplate")
        rec("Settings",f"{tag}: Settings opens with the bookplate: when the journal began, days kept and Forgelings",t.startswith("This journal was started") and " kept · " in t and "Forgeling" in t,t)
        # a sheet: chips and fields
        pg.evaluate("()=>{document.querySelectorAll('#view-settings details').forEach(d=>d.open=true);document.getElementById('btnExport').click()}"); pg.wait_for_timeout(500)
        tx=pg.evaluate("()=>{const t=document.querySelector('#modal textarea');const s=getComputedStyle(t);return [s.borderRadius,s.backgroundColor]}")
        rec("Sheets",f"{tag}: text boxes in sheets are paper with ink edges",tx[0]=="0px" and tx[1] in ("rgb(255, 253, 246)","rgb(46, 40, 80)"),tx)
        closemodals(pg)
        if hr==11:
            s=st(pg); s["seen"]=40; setst(pg,s); pg.reload(); pg.wait_for_timeout(1200); w=mt(pg)
            rec("New","What's New opens with the latest notes (the whole journal has since rolled off; six kept since 0.83)",pg.locator("#modal .newlist li").count()>=6,w[:80])
        rec("All",f"{tag}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_47"); print(sum(r["ok"] for r in RES),"/",len(RES))
