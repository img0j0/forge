# 0.81 the Forge keeps its own count: no ember line on the reveal or the Hearth button; "Something is ready" only when a
#   piece can be made; the Forge sheet keeps embers and spares, no "pieces made"; axe.
#   Run from a folder holding lived_store.json, dev root served at http://127.0.0.1:8772/ : python3 qa_forge81.py app.html en|ja HH:MM
import sys,os,json,datetime as dt,copy,re
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;day=S['date']
ms=int(dt.datetime.fromisoformat(day+f'T{HH}:00-05:00').timestamp()*1000)
CLK="(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
ok=[];out=f's81/{LANG}_{HH[:2]}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,str(d)[:220])
EMB=re.compile(r'\bembers?\b|残り火')
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,390,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(CLK);pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG)
    # no spares: nothing ready, no count on the button
    s=copy.deepcopy(S)
    for k,v in s['curios'].items(): v['n']=1
    setst(pg,s);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'hearth')
    t=pg.inner_text('#hForge');chk('Hearth Forge button: no ember count',not EMB.search(t) and not re.search(r'\d',t),t)
    chk('…and nothing ready says nothing',pg.locator('#hForge small').count()==0,t)
    # spares: something ready
    s2=copy.deepcopy(S)
    for k,v in s2['curios'].items(): v['n']=4
    setst(pg,s2);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'hearth')
    t=pg.inner_text('#hForge');chk('with spares it says something is ready',('Something is ready' in t) or ('作れるもの' in t),t)
    pg.screenshot(path=f'{out}/hearth.png')
    pg.click('#hForge');pg.wait_for_timeout(500);m=pg.inner_text('#modal')
    chk('Forge sheet keeps embers and spares in one line, no pieces-made count',bool(EMB.search(m)) and 'pieces made' not in m and '点中' not in m,m[:160].replace('\n',' / '))
    pg.screenshot(path=f'{out}/forge.png');pg.add_script_tag(content=AXE)
    v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk('axe on the Forge sheet',not v,v);closemodals(pg)
    # the reveal: today's card, turned and done
    s3=copy.deepcopy(S);s3['status']='revealed';s3['todayCard']=None;s3['history']=[h for h in s3['history'] if h['date']!=day];s3['journal'].pop(day,None)
    setst(pg,s3);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'today')
    if pg.locator('#btnDone').count():
        pg.click('#btnDone');pg.wait_for_timeout(2500)
        pg.evaluate("document.querySelector('#stage .card, #stage')&&document.querySelector('#stage').click()");pg.wait_for_timeout(2500)
        r=pg.inner_text('#overlay') if pg.locator('#overlay').count() else pg.inner_text('body')
        chk('the reveal has no ember line',pg.locator('#rvEmber').count()==0 and 'for the Forge' not in r and '鍛冶場で使える' not in r)
        pg.screenshot(path=f'{out}/reveal.png')
    else: chk('reached the reveal',False,'no I did it button')
    chk('no page errors',not pg._errs,pg._errs[:2]);b.close()
print(sum(ok),'/',len(ok))
