import sys,os,json,datetime as dt,copy
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]; W=int(sys.argv[4])
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;day=S['date']
ms=int(dt.datetime.fromisoformat(day+f'T{HH}:00-05:00').timestamp()*1000)
CLK="(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
ok=[];out=f's78/{LANG}_{HH[:2]}_{W}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,d)
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,W,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(CLK);pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);setst(pg,S);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG);pg.reload();pg.wait_for_timeout(1500);closemodals(pg)
    pg.add_style_tag(content="#toast{display:none!important}")
    tabs=pg.evaluate("[...document.querySelectorAll('.tab')].filter(t=>!t.hidden).map(t=>{const r=t.getBoundingClientRect();return [t.innerText.trim(),Math.round(r.width),Math.round(r.height),t.scrollWidth<=t.clientWidth+1]})");print(tabs)
    chk('six tabs, each at least 44 pt and labels fit',len(tabs)==6 and all(w>=44 and h>=44 and fit for _,w,h,fit in tabs),tabs)
    pg.evaluate("document.querySelector('.tab[data-tab=book]').click()");pg.wait_for_timeout(500)
    chk('Book tab opens the journal',pg.evaluate("!!document.getElementById('bookOpen')&&!document.querySelector('#view-chronicle .chips.seg')"))
    chk('title says Your book',pg.inner_text('#title') in ('Your book','あなたの本'),pg.inner_text('#title'))
    pg.screenshot(path=f'{out}/book.png')
    pg.evaluate("document.querySelector('.tab[data-tab=chronicle]').click()");pg.wait_for_timeout(500)
    segs=pg.evaluate("[...document.querySelectorAll('#view-chronicle .chips.seg .chip')].map(b=>b.dataset.sub)")
    chk('Map tab has Map and Tales only',segs==['map','tales'],segs);pg.screenshot(path=f'{out}/map.png')
    pg.add_script_tag(content=AXE)
    for t in ['book','chronicle']:
        pg.evaluate("t=>document.querySelector('.tab[data-tab='+t+']').click()",t);pg.wait_for_timeout(500)
        v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk(f'axe on {t}',not v,v)
    # one voice
    s2=copy.deepcopy(S);s2['journal'].pop(day,None);setst(pg,s2);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'today')
    pg.evaluate("document.getElementById('askMore').click()");pg.wait_for_timeout(400);m=pg.inner_text('#modal')
    chk('your words sheet: the companion asks, the Forge does not',pg.evaluate("document.querySelectorAll('#modal .saylead').length")==1 and 'The Forge asks' not in m and '鍛冶場からの問い' not in m,m[:220].replace('\n',' / '))
    pg.screenshot(path=f'{out}/words.png')
    chk('no page errors',not pg._errs,pg._errs[:2]);b.close()
print(sum(ok),'/',len(ok))
