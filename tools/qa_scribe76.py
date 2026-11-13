# 0.76 Scribe test (12 checks): prints every chapter the Scribe writes. Run from a folder holding lived_store.json with the dev
#   root served at http://127.0.0.1:8772/ : python3 qa_scribe76.py work.html|app.html en|ja HH:MM. Screenshots go to ./s76/.
import sys,os,json,datetime as dt
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;S.pop('bookAt',None);day=S['date']
def clk(d,hh): ms=int(dt.datetime.fromisoformat(d+f'T{hh}:00-05:00').timestamp()*1000); return "(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
ok=[];out=f's76/{LANG}_{HH[:2]}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,d)
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,390,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(clk(day,HH));pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);setst(pg,S);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG);pg.reload();pg.wait_for_timeout(1500);closemodals(pg)
    pg.add_style_tag(content="#toast{display:none!important}")
    openmap(pg);pg.evaluate("document.querySelector('[data-sub=journal]').click()");pg.wait_for_timeout(400)
    pg.evaluate("document.getElementById('bookOpen').click()");pg.wait_for_timeout(400)
    n=pg.evaluate("document.querySelectorAll('[data-bkgo]').length")
    for i in range(n):
        pg.evaluate("i=>document.querySelectorAll('[data-bkgo]')[i].click()",i);pg.wait_for_timeout(350)
        t=pg.inner_text('#modal .bch');print('-----',t.replace('\n',' / ')[:900])
        chk(f'chapter {i}: the Scribe wrote at least 3 sentences',pg.evaluate("document.querySelector('#modal .bch .scribe .world').innerText.split(/[.。]/).filter(x=>x.trim()).length")>=3)
        pg.screenshot(path=f'{out}/ch{i}.png');pg.evaluate("document.getElementById('bkToc').click()");pg.wait_for_timeout(250)
    pg.add_script_tag(content=AXE)
    v=pg.evaluate("(async()=>{document.querySelectorAll('[data-bkgo]')[0].click();await new Promise(r=>setTimeout(r,400));const r=await axe.run(document.getElementById('modal'),{runOnly:['wcag2a','wcag2aa']});return r.violations.map(v=>v.id)})()");chk('axe on a chapter page',not v,v)
    closemodals(pg)
    pg.evaluate("document.getElementById('jMonth').click()");pg.wait_for_timeout(400);t=pg.inner_text('#modal');print('MONTH:',t.replace('\n',' / ')[:600]);pg.screenshot(path=f'{out}/month.png')
    chk('month in words is the Scribe, no counts',pg.evaluate("!!document.querySelector('#modal .scribe')") and 'lines in your book' not in t and '14 days' not in t)
    closemodals(pg);pg.evaluate("document.getElementById('jWeek').click()");pg.wait_for_timeout(400);t=pg.inner_text('#modal');print('WEEK:',t.replace('\n',' / ')[:500]);pg.screenshot(path=f'{out}/week.png')
    chk('week is the Scribe, chips gone',pg.evaluate("!!document.querySelector('#modal .scribe')&&!document.querySelector('#modal .stat-chip')"))
    chk('no page errors',not pg._errs,pg._errs[:2]);b.close()
    # Sunday evening: the save's own day is Sunday Dec 20, done
    import copy;S2=copy.deepcopy(S);c=S2['cards'][-1]
    S2['history'].append({'date':'2026-12-20','status':'done','v':S2.get('todayV',0),'card':c['id'],'note':'','allIn':False});S2['date']='2026-12-20';S2['status']='done';S2['todayCard']=c['id']
    b=p.chromium.launch();ctx,pg=newpage(b,390,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(clk('2026-12-20','21:15'));pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);setst(pg,S2);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG);pg.reload();pg.wait_for_timeout(1500);closemodals(pg)
    tabto(pg,'today');has=pg.evaluate("!!document.getElementById('btnClose')");chk('Sunday: Close the day offered',has)
    if has:
        pg.evaluate("document.getElementById('btnClose').click()");pg.wait_for_timeout(500);t=pg.inner_text('#modal');print('SUNDAY:',t.replace('\n',' / ')[:700]);pg.screenshot(path=f'{out}/sunday.png')
        chk('Sunday: the week read back before goodnight',pg.evaluate("!!document.querySelector('#modal .weekback .scribe')"))
    chk('no page errors (Sunday)',not pg._errs,pg._errs[:2]);b.close()
print(sum(ok),'/',len(ok))
