# 0.50.1: sky lanterns lift off the lantern that finished the round and settle along the top in its colour;
# the fire, seeds and embers draw in front of the Forgeling, and by the fire it sits clear of the flames.
import sys
exec(open('qa_50.py').read().split('with sync_playwright() as p:')[0])
ZT="""sel=>{const pg=document.getElementById('pg'),m=pg.querySelector('.pgmate'),e=pg.querySelector(sel);if(!e)return null;const z=x=>+getComputedStyle(x).zIndex||0;return [z(e),z(m)]}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in [(320,568),(390,844)]:
        ctx,pg=newpage(b,w,h); pg.set_default_timeout(20000); pg.clock.install(time=datetime.datetime(2027,3,3,20,30)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); base=st(pg)
        # Keep the Fire
        ready(pg,card(base,1)); openg(pg,1); start(pg); pg.wait_for_timeout(300)
        g=pg.evaluate("()=>{const a=document.querySelector('#pg .pgmate').getBoundingClientRect(),f=document.querySelector('#pg .fire').getBoundingClientRect(),q=document.getElementById('pg').getBoundingClientRect();return [a.left-q.left,a.right,f.left]}")
        rec(f"Ember {w}","the Forgeling sits clear of the fire, inside the scene",g[0]>=0 and g[1]<=g[2],g)
        z=pg.evaluate(ZT,".fire"); rec(f"Ember {w}","the fire draws in front of the Forgeling",z[0]>z[1],z)
        wait_for(pg,"!!document.querySelector('#pg .emb')",3000); z=pg.evaluate(ZT,".emb"); rec(f"Ember {w}","embers draw in front of the Forgeling",z and z[0]>z[1],z)
        pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)
        # Dandelion Drift
        ready(pg,card(base,0)); openg(pg,0); start(pg); wait_for(pg,"!!document.querySelector('#pg .seed')",3000)
        z=pg.evaluate(ZT,".seed"); rec(f"Meadow {w}","seeds draw in front of the Forgeling",z and z[0]>z[1],z)
        hit=pg.evaluate("()=>{const m=document.querySelector('#pg .pgmate').getBoundingClientRect(),x=m.left+m.width/2,y=m.top+m.height/2,s=document.createElement('button');s.className='seed';s.style.cssText='left:'+(x-document.getElementById('pg').getBoundingClientRect().left-24)+'px;bottom:auto;top:'+(y-document.getElementById('pg').getBoundingClientRect().top-24)+'px';document.getElementById('pg').appendChild(s);const t=document.elementFromPoint(x,y);s.remove();return t===s}")
        rec(f"Meadow {w}","a seed passing over the Forgeling is still the thing you tap",hit)
        pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300)
        # Lantern Lights
        ready(pg,card(base,4)); openg(pg,4); pg.evaluate(WATCH); start(pg); last=[]
        for r in range(4):
            pg.wait_for_function("()=>document.getElementById('pgMsg').textContent==='Your turn.'&&window.__seq.length>0")
            sq=pg.evaluate("window.__seq.slice()"); pg.evaluate("window.__seq=[]"); last.append(sq[-1])
            for v in sq: pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",v); pg.wait_for_timeout(60)
        pg.wait_for_timeout(1900)
        S=pg.evaluate("()=>{const q=document.getElementById('pg').getBoundingClientRect(),m=document.getElementById('pgMsg').getBoundingClientRect();return {m:[m.left,m.right,m.bottom],L:[...document.querySelectorAll('#pg .skyl')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left-q.left),Math.round(r.top-q.top),getComputedStyle(e).backgroundColor]}),W:q.width}}")
        L=S["L"]; cols={'#FFD36B':'rgb(255, 211, 107)','#F29BB5':'rgb(242, 155, 181)','#A6D8F2':'rgb(166, 216, 242)','#B5DDB5':'rgb(181, 221, 181)'}
        order=['#FFD36B','#F29BB5','#A6D8F2','#B5DDB5']
        rec(f"Dusk {w}","each round settles one sky lantern, all on one line at the top",len(L)==4 and len({y for x,y,c in L})==1 and L[0][1]<20,L)
        rec(f"Dusk {w}","each takes the colour of the lantern that finished its round",[c for x,y,c in L]==[cols[order[i]] for i in last],(L,last))
        rec(f"Dusk {w}","they fill in from both edges, clear of the message and inside the scene",L[0][0]<S["W"]/2<L[1][0] and all(0<=x<=S["W"]-10 for x,y,c in L) and all(not(S["m"][0]-10<x+pg.evaluate("document.getElementById('pg').getBoundingClientRect().left")<S["m"][1]) for x,y,c in L),S)
        # reduced motion: they are simply there
        pg.emulate_media(reduced_motion="reduce")
        pg.wait_for_function("()=>document.getElementById('pgMsg').textContent==='Your turn.'&&window.__seq.length>0")
        sq=pg.evaluate("window.__seq.slice()"); pg.evaluate("window.__seq=[]")
        for v in sq: pg.evaluate("v=>document.querySelector('#pg [data-lant=\"'+v+'\"]').click()",v); pg.wait_for_timeout(60)
        pg.wait_for_timeout(150)
        rm=pg.evaluate("()=>{const e=[...document.querySelectorAll('#pg .skyl')].pop();return [getComputedStyle(e).animationName,getComputedStyle(e).transform]}")
        rec(f"Dusk {w}","with reduced motion a sky lantern appears in place, no flight",rm[0]=='none' and rm[1] in ('none',''),rm)
        rec(f"Dusk {w}","axe finds nothing",axe(pg)==[],axe(pg))
        pg.emulate_media(reduced_motion="no-preference")
        pg.evaluate("document.getElementById('pgSit').click()"); pg.wait_for_timeout(300); ctx.close()
    b.close()
save_results("qa_501"); print(sum(r["ok"] for r in RES),"/",len(RES))
