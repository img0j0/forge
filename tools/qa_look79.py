# 0.79 look-back test: one look-back line on Today; On this day and the echo open the book; second reading on the spread;
#   This week gone from Today, Latest finds kept; axe.
#   Run from a folder holding lived_store.json, dev root served at http://127.0.0.1:8772/ : python3 qa_look79.py app.html en|ja HH:MM
import sys,os,json,datetime as dt,copy
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;day=S['date']
def ms(hh): return int(dt.datetime.fromisoformat(day+f'T{hh}:00-05:00').timestamp()*1000)
CLK="(()=>{const R=Date;let t=+(localStorage.getItem('qa-clock')||0);if(!t)return;const off=t-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"
LB=['btnClose','btnLetter','btnYear','btnZine','btnOtd']
ok=[];out=f's79/{LANG}_{HH[:2]}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,str(d)[:200])
def lbs(pg): return pg.evaluate("ids=>ids.filter(i=>document.getElementById(i))",LB)
d=dt.date.fromisoformat(day);mago=(d.replace(month=d.month-1) if d.month>1 else d.replace(year=d.year-1,month=12)).isoformat()
def load(pg,s,hh):
    pg.evaluate("m=>localStorage.setItem('qa-clock',m)",ms(hh));setst(pg,s);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'today')
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,390,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(CLK);pg.goto(P);pg.evaluate("m=>localStorage.setItem('qa-clock',m)",ms(HH));pg.reload();pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG)
    s=copy.deepcopy(S);s.pop('otd',None);s.pop('echo',None);s['closed']=None;load(pg,s,HH);pg.add_style_tag(content="#toast{display:none!important}")
    shown=lbs(pg);chk('at most one look-back line on Today',len(shown)<=1,shown)
    if HH>='19':chk('in the evening it is Close the day',shown==['btnClose'],shown)
    t=pg.inner_text('#view-today');chk('This week is gone from Today, Latest finds stays',pg.locator('#view-today .dots').count()==0 and pg.locator('#view-today .latest').count()==1)
    pg.screenshot(path=f'{out}/today.png',full_page=True)
    # On this day at noon: the page from a month ago opens in the book
    s=copy.deepcopy(S);s.pop('otd',None);s.pop('echo',None);[L.update(read=True) for L in s.get('letters',[])];load(pg,s,'12:00')
    has=pg.locator('#btnOtd').count()==1;chk('noon: On this day offered (a page from a month ago exists)',has,lbs(pg))
    if has:
        pg.click('#btnOtd');pg.wait_for_timeout(600)
        chk('…and opens the book at that day',pg.locator('#view-chronicle .jbook .bday').count()==1 and pg.evaluate("()=>JSON.parse(localStorage.getItem('forge-app-v1')).bookAt")=='d:'+mago,pg.evaluate("()=>JSON.parse(localStorage.getItem('forge-app-v1')).bookAt"))
        closemodals(pg);chk('…once a day',pg.locator('#btnOtd').count()==0)
    # the echo: no page a month ago, so the Forgeling found two weeks ago comes back
    s=copy.deepcopy(S);s.pop('otd',None);s.pop('echo',None);[L.update(read=True) for L in s.get('letters',[])]
    s['history']=[h for h in s['history'] if h['date']!=mago];s['journal'].pop(mago,None);(s.get('ask') or {}).pop(mago,None);(s.get('posts') or {}).pop(mago,None)
    load(pg,s,'12:00');ttl=pg.evaluate("()=>{const b=document.getElementById('btnOtd');return b?b.querySelector('b').innerText:''}")
    chk('echo: the row names when it was found',bool(ttl) and pg.locator('.echo').count()==0,ttl)
    if ttl:
        pg.screenshot(path=f'{out}/echo_row.png');pg.click('#btnOtd');pg.wait_for_timeout(600)
        sp=pg.locator('#view-chronicle .jbook .bday').count()==1;chk('…opens that day in the book',sp)
        chk('…where the second reading is one tap away',pg.locator('#view-chronicle .bday [data-kept]').count()==1)
        pg.screenshot(path=f'{out}/echo_book.png');pg.add_script_tag(content=AXE)
        v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk('axe on the spread',not v,v)
        h=pg.evaluate("(()=>{const r=document.querySelector('#view-chronicle .bday [data-kept]').getBoundingClientRect();return r.height})()");chk('second reading is 44 pt',h>=44,h)
        pg.click('#view-chronicle .bday [data-kept]');pg.wait_for_timeout(500);chk('…and opens it',pg.locator('#keptBack').count()==1);closemodals(pg)
    tabto(pg,'today');pg.add_script_tag(content=AXE)
    v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk('axe on Today',not v,v)
    chk('no page errors',not pg._errs,pg._errs[:2]);b.close()
print(sum(ok),'/',len(ok))
