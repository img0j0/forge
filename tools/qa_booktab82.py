# 0.82 the Book tab is the book: opens at the ribbon in the tab (no sheet), no page count, Contents and Latest page,
#   the last five weeks as rows that open their pages, the back holds what sat beside the book, On this day and the echo
#   open the tab at that day, second reading only on the echo's day; 44 pt, no sideways scroll, axe.
#   Run from a folder holding lived_store.json, dev root served at http://127.0.0.1:8772/ : python3 qa_booktab82.py app.html en|ja HH:MM WIDTH
import sys,os,json,datetime as dt,copy,re
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]; W=int(sys.argv[4]) if len(sys.argv)>4 else 390
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;day=S['date']
ms=int(dt.datetime.fromisoformat(day+f'T{HH}:00-05:00').timestamp()*1000)
CLK="(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
ok=[];out=f's82b/{LANG}_{HH[:2]}_{W}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,str(d)[:200])
def at(pg): return pg.evaluate("()=>JSON.parse(localStorage.getItem('forge-app-v1')).bookAt")
def axe(pg):
    if not pg.evaluate("!!window.axe"):pg.add_script_tag(content=AXE)
    return pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))")
def small(pg,sel): return pg.evaluate("s=>[...document.querySelectorAll(s)].filter(b=>b.offsetParent).map(b=>b.getBoundingClientRect()).filter(r=>r.height<44||r.width<44).length",sel)
def wide(pg): return pg.evaluate("document.documentElement.scrollWidth>innerWidth+1")
d=dt.date.fromisoformat(day);mago=(d.replace(month=d.month-1) if d.month>1 else d.replace(year=d.year-1,month=12)).isoformat()
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,W,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(CLK);pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG)
    s=copy.deepcopy(S);s['bookAt']='d:2026-12-01';[L.update(read=True) for L in s.get('letters',[])];s['otd']=day
    setst(pg,s);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'book');pg.wait_for_timeout(400)
    chk('the Book tab is the book, open at the ribbon',pg.locator('#view-chronicle .jbook .bday').count()==1 and pg.locator('#modal:not([hidden])').count()==0 and at(pg)=='d:2026-12-01',at(pg))
    t=pg.inner_text('#view-chronicle');chk('no page count',not re.search(r'Page \d+ of|ページ中',t))
    chk('no echo, no second reading on a spread',pg.locator('#view-chronicle [data-kept]').count()==0)
    pg.screenshot(path=f'{out}/day.png',full_page=True)
    pg.click('#bkNext');pg.wait_for_timeout(300);a1=at(pg);pg.click('#bkPrev');pg.wait_for_timeout(300)
    chk('Back and Next turn pages in place',a1!='d:2026-12-01' and at(pg)=='d:2026-12-01',a1)
    pg.click('#bkLatest');pg.wait_for_timeout(300);chk('Latest page goes to the newest spread',at(pg)=='d:'+max(k for k in [h['date'] for h in S['history'] if h['status']=='done']),at(pg))
    chk('…and is disabled there',pg.evaluate("document.getElementById('bkLatest').disabled"))
    pg.click('#bkToc');pg.wait_for_timeout(300);chk('Contents',at(pg)=='t')
    rows=pg.locator('#view-chronicle .bkwk').count();chk('the last five weeks are rows in the contents',rows>=4,rows)
    chk('every contents row and book button is 44 pt',small(pg,'#view-chronicle .btrow, #view-chronicle .jbook button')==0,small(pg,'#view-chronicle .btrow, #view-chronicle .jbook button'))
    chk('no sideways scroll on the contents',not wide(pg));pg.screenshot(path=f'{out}/contents.png',full_page=True)
    v=axe(pg);chk('axe on the contents',not v,v)
    pg.locator('#view-chronicle .bkwk').first.click();pg.wait_for_timeout(300);chk('a week row opens its first page',(at(pg) or '').startswith('d:') and pg.locator('#view-chronicle .bday').count()==1,at(pg))
    # cover
    pg.evaluate("()=>{for(let i=0;i<300&&!document.getElementById('bkPrev').disabled;i++)document.getElementById('bkPrev').click()}");pg.wait_for_timeout(300)
    chk('the cover keeps the binding line',pg.locator('#view-chronicle .bcovnx').count()==1 and at(pg)=='c',at(pg));v=axe(pg);chk('axe on the cover',not v,v);pg.screenshot(path=f'{out}/cover.png')
    # back
    pg.evaluate("()=>{for(let i=0;i<400&&!document.getElementById('bkNext').disabled;i++)document.getElementById('bkNext').click()}");pg.wait_for_timeout(300)
    ids=pg.evaluate("[...document.querySelectorAll('#view-chronicle .bback button')].map(b=>b.id)")
    chk('the back holds what sat beside the book',all(x in ids for x in ['jWeek','jSeasons','jYear','jLines','bookLetters','bookRibbon']),ids)
    v=axe(pg);chk('axe on the back',not v,v);pg.screenshot(path=f'{out}/back.png',full_page=True)
    pg.click('#jSeasons');pg.wait_for_timeout(400);chk('Seasons opens from the back',pg.locator('#modal:not([hidden]) .seasons').count()==1);closemodals(pg)
    pg.click('#jWeek');pg.wait_for_timeout(400);chk('This week opens from the back',pg.locator('#modal:not([hidden])').count()==1);closemodals(pg)
    # keys and swipe
    pg.evaluate("document.getElementById('bkToc').click()");pg.wait_for_timeout(200);pg.keyboard.press('ArrowRight');pg.wait_for_timeout(300);chk('arrow keys turn pages',at(pg)!='t',at(pg))
    # On this day from Today opens the tab at that day
    s2=copy.deepcopy(S);s2.pop('otd',None);s2.pop('echo',None);s2['closed']=day;[L.update(read=True) for L in s2.get('letters',[])];setst(pg,s2);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'today')
    if pg.locator('#btnOtd').count():
        pg.click('#btnOtd');pg.wait_for_timeout(600)
        chk('On this day opens the Book tab at that day',pg.evaluate("document.querySelector('.tab[data-tab=book]').getAttribute('aria-current')")=='page' and at(pg)=='d:'+mago and pg.locator('#view-chronicle .bday').count()==1,at(pg))
    else: chk('On this day offered',False)
    # the echo: second reading shows on its day
    s3=copy.deepcopy(s2);s3['history']=[h for h in s3['history'] if h['date']!=mago];s3['journal'].pop(mago,None);(s3.get('ask') or {}).pop(mago,None);(s3.get('posts') or {}).pop(mago,None)
    setst(pg,s3);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'today')
    if pg.locator('#btnOtd').count():
        pg.click('#btnOtd');pg.wait_for_timeout(600);chk('the echo opens its day with the second reading',pg.locator('#view-chronicle .bday [data-kept]').count()==1)
        pg.screenshot(path=f'{out}/echo.png',full_page=True);v=axe(pg);chk('axe on the echo spread',not v,v)
    else: chk('echo offered',False)
    chk('no sideways scroll on a spread',not wide(pg))
    chk('no page errors',not pg._errs,pg._errs[:2]);b.close()
print(sum(ok),'/',len(ok))
