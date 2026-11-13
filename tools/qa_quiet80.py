# 0.80 quieter counts: no ribbon grid or ribbon toast, backdrops unlock in words, no visits counter anywhere; axe.
#   Run from a folder holding lived_store.json, dev root served at http://127.0.0.1:8772/ : python3 qa_quiet80.py app.html en|ja HH:MM
import sys,os,json,datetime as dt,copy,re
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;day=S['date']
ms=int(dt.datetime.fromisoformat(day+f'T{HH}:00-05:00').timestamp()*1000)
CLK="(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
ok=[];out=f's80/{LANG}_{HH[:2]}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,str(d)[:200])
BAD=re.compile(r'visits? left|Visits left|of 3\.|New ribbon|ribbon:|Ribbons|あと\d回|3回中|新しいリボン|リボン：')
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,390,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(CLK);pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG)
    s=copy.deepcopy(S);s['hearth']['visits']={'date':day,'used':1};setst(pg,s);pg.reload();pg.wait_for_timeout(1300);closemodals(pg)
    seen={}
    for t in ['today','hearth','binder','chronicle','book','settings']:
        tabto(pg,t);pg.wait_for_timeout(300);seen[t]=pg.inner_text('#app') if pg.locator('#app').count() else pg.inner_text('body')
    bad=[t for t,x in seen.items() if BAD.search(x)];chk('no visits counter or ribbon wording on any tab',not bad,[(t,BAD.search(seen[t]).group(0)) for t in bad])
    tabto(pg,'book');chk('no ribbon medals in the book',pg.locator('.medals,.ribp').count()==0)
    tabto(pg,'hearth');pg.evaluate("document.getElementById('hPlay')&&document.getElementById('hPlay').click()");pg.wait_for_timeout(500)
    g=pg.inner_text('#modal') if pg.locator('#modal:not([hidden])').count() else '';chk('games sheet: no counter',g and not BAD.search(g),g[:160].replace('\n',' / '))
    pg.screenshot(path=f'{out}/games.png');closemodals(pg)
    # backdrops: lock them all, open the chooser, read the words
    s2=copy.deepcopy(s);s2['cards']=[c for c in s2['cards']][:3];s2['history']=s2['history'][-3:];s2['ribbons']=[]
    for c in s2['cards']: c['bond']=0;c['rarity']=min(c.get('rarity',0),1);c.pop('tale',None)
    setst(pg,s2);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'hearth')
    pg.evaluate("document.getElementById('hKeeps')&&document.getElementById('hKeeps').click()");pg.wait_for_timeout(500)
    locks=pg.evaluate("[...document.querySelectorAll('#modal [data-bd]')].filter(x=>x.disabled).map(x=>x.innerText)")
    chk('locked backdrops say how they open, in words',len(locks)>=3 and all(('opens' in l) or ('ひらきます' in l) for l in locks),locks)
    pg.screenshot(path=f'{out}/backdrops.png');pg.add_script_tag(content=AXE)
    v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk('axe on the backdrop sheet',not v,v);closemodals(pg)
    # earning a backdrop: one plain line, no medal
    s3=copy.deepcopy(S);s3['ribbons']=[r for r in (S.get('ribbons') or []) if r!='week'];setst(pg,s3);pg.reload();pg.wait_for_timeout(2500);closemodals(pg);pg.wait_for_timeout(900)
    tt=pg.evaluate("document.getElementById('toast').textContent");med=pg.evaluate("document.getElementById('toast').classList.contains('medal')")
    chk('earning Glade says so plainly',('Glade' in tt or '木もれ日' in tt) and not med,tt)
    s4=copy.deepcopy(S);s4['ribbons']=[r for r in (S.get('ribbons') or []) if r!='collector'];setst(pg,s4);pg.reload();pg.wait_for_timeout(2500);closemodals(pg);pg.wait_for_timeout(900)
    tt=pg.evaluate("document.getElementById('toast').textContent");chk('other goals pass quietly',not BAD.search(tt or ''),tt)
    st=pg.evaluate("()=>JSON.parse(localStorage.getItem('forge-app-v1')).ribbons");chk('…and are still kept in the save',isinstance(st,list) and 'collector' in st)
    for t in ['today','hearth','book']:
        tabto(pg,t);pg.add_script_tag(content=AXE);v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk(f'axe on {t}',not v,v)
    pg.screenshot(path=f'{out}/book.png')
    chk('no page errors',not pg._errs,pg._errs[:2]);b.close()
print(sum(ok),'/',len(ok))
