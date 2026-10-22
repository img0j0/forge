from lib import *
import subprocess
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
src=open(S+"/work.html").read()
ev=src[src.index("const EVENTS=["):src.index("const WEPOCH")]
evs=[m for m in re.findall(r"'((?:[^'\\]|\\.)*)'",ev)]
longest=sorted(evs,key=len,reverse=True)[:6]
eras=re.findall(r"\{n:'([^']+)'",src[src.index("const ERAS=["):src.index("];",src.index("const ERAS=["))])
era_long=max(range(len(eras)),key=lambda i:len(eras[i]))
def gossip(t,gap=12): return "Found during the weeks when "+t+"."
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,568),(360,640),(390,844)]:
        ctx,pg=newpage(b,W,H); pg.set_default_timeout(7000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        worst=[]
        for i,t in enumerate(longest):
            for dark in (False,True):
                s=json.loads(json.dumps(base)); c=s["cards"][0]; c.update({"gossip":gossip(t),"era":era_long,"nick":"M"*16,"tale":"W"*120,"dark":dark,"allIn":True,"source":"pack","dateLabel":"Wed, Sep 30"}); s["seen"]=18; s["settings"]["mood"]="dark" if dark else "cute"
                s["cards"][0]["date"]="2026-09-29"
                setst(pg,s); pg.reload(); pg.wait_for_timeout(500); closemodals(pg)
                tabto(pg,"binder"); pg.evaluate("()=>document.querySelector('[data-insp]').click()"); pg.wait_for_timeout(350)
                pg.evaluate("()=>document.getElementById('inspFlip').click()"); pg.wait_for_timeout(600)
                m=pg.evaluate("()=>{const e=document.querySelector('#modal .cbk');if(!e)return null;const r=e.getBoundingClientRect(),ch=[...e.children].filter(x=>getComputedStyle(x).display!=='none');const last=ch[ch.length-1].getBoundingClientRect(),first=ch[0].getBoundingClientRect();return {sh:e.scrollHeight,ch:e.clientHeight,over:e.scrollHeight-e.clientHeight,top:Math.round(first.top-r.top),bot:Math.round(r.bottom-last.bottom),clipX:e.scrollWidth>e.clientWidth}}")
                worst.append((m["over"] if m else 999,m["clipX"] if m else True,i,dark,m))
                pg.evaluate("()=>document.getElementById('ovClose').click()"); pg.wait_for_timeout(200)
        mo=max(w[0] for w in worst); cx=any(w[1] for w in worst)
        rec("Fit",f"{W}px: worst case card back (16-char name, 120-char tale, longest new event, longest era, pack, all-in) needs no scrolling",mo<=1 and not cx,[w for w in worst if w[0]>1][:2] or mo)
        ctx.close()
    b.close()
save_results("qa_fit"); print(sum(r["ok"] for r in RES),"/",len(RES))
