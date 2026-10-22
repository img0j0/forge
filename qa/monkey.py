from lib import *
import random,sys
exec(open("qa_map.py").read().split("JUNK=")[0].split("from lib import *")[1])
SEED=int(sys.argv[1]) if len(sys.argv)>1 else 1
SEL="button:not([disabled]),[role=button],[data-insp],.tab,.chip,.fchip,input,select,summary,svg .mphit"
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg=newpage(b); pg.set_default_timeout(3000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg); base=st(pg)
    # give the monkey a lively save: several cards of varied calling/realm/rarity, a pack, journal
    s=json.loads(json.dumps(base)); b0=s["cards"][0]; rnd=random.Random(SEED); s["cards"]=[]
    for i in range(14):
        c=json.loads(json.dumps(b0)); c.update({"id":100+i,"seed":9000+i*7717,"v":i%12,"theme":i%5,"dark":i%3==0,"rarity":[0,0,1,2,0,3,1,4][i%8]}); s["cards"].append(c)
    s["nextId"]=500; s["packs"]=1; s["seen"]=18; s["hearth"]["slots"]=[100,101]; setst(pg,s); pg.reload(); pg.wait_for_timeout(700); closemodals(pg)
    rnd=random.Random(SEED); n=0; fails=[]
    tools=["next","pack","wander","world","together","sleep","preview","mappreview","agecard","quiet","holo","skip10"]
    for step in range(260):
        try:
            r=rnd.random()
            if r<.07: dev(pg,rnd.choice(tools))
            elif r<.12: tabto(pg,rnd.choice(["today","hearth","binder","chronicle","settings"]))
            else:
                els=pg.query_selector_all(SEL)
                vis=[e for e in els if e.is_visible()]
                if not vis: closemodals(pg); continue
                e=rnd.choice(vis); tag=e.evaluate("e=>(e.id||e.dataset.tool||e.textContent||'').trim().slice(0,30)")
                if "Start over" in tag or tag=="reset" or "Erase" in tag or "Restore" in tag or "Import" in tag: continue
                if e.evaluate("e=>e.tagName==='INPUT'&&e.type!=='checkbox'&&e.type!=='radio'"):
                    e.fill(rnd.choice(["hello","x"*30,"<b>x</b>","\"';--","😀 ok",""]))
                elif e.evaluate("e=>e.tagName==='SELECT'"):
                    opts=e.evaluate("e=>[...e.options].map(o=>o.value)"); e.select_option(rnd.choice(opts))
                else: e.click(timeout=1500,force=True)
            n+=1
            if pg._errs: fails.append((step,pg._errs[:1])); pg._errs.clear()
        except Exception as ex:
            msg=str(ex)[:90]
            if "Timeout" in msg or "detached" in msg or "not attached" in msg or "outside" in msg or "intercept" in msg or "navigat" in msg: 
                try: closemodals(pg)
                except Exception: pass
                continue
            fails.append((step,msg))
    s2=st(pg); ok=isinstance(s2,dict) and isinstance(s2.get("cards"),list)
    rec("Monkey",f"seed {SEED}: {n} random actions, no page errors",not fails,fails[:2])
    rec("Monkey",f"seed {SEED}: the save is still valid and loads cleanly afterwards",ok and bool(pg.reload() or True) and not pg._errs,"")
    pg.wait_for_timeout(500); rec("Monkey",f"seed {SEED}: still renders after reload",pg.locator('.tab').count()==5 and not pg._errs,pg._errs[:1])
    b.close()
print(sum(r["ok"] for r in RES),"/",len(RES))
