# 0.77 tucked-in test (12 checks): road postcard, season stamp, curio, letter, margin note, doodle on their day; Say more.
#   Run from a folder holding lived_store.json, dev root served at http://127.0.0.1:8772/ : python3 qa_tuck77.py work.html|app.html en|ja HH:MM
import sys,os,json,datetime as dt,copy
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;day=S['date']
def dnum(k): return (dt.date.fromisoformat(k)-dt.date(2026,1,1)).days
def clk(d,hh): ms=int(dt.datetime.fromisoformat(d+f'T{hh}:00-05:00').timestamp()*1000); return "(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
done=sorted({h['date'] for h in S['history'] if h['status']=='done'})
road=[g['d'] for g in S.get('pcGifts',[]) if g.get('t')==1 and g['d'] in done]
seas=[v for v in S['seasons'].values() if v in done]
cur=[v['at'] for v in S['curios'].values() if v.get('at') in done]
let=[L['d'] for L in S.get('letters',[]) if L['d'] in done]
note=[k for k in done if dnum(k)%3==0 and k in S.get('ask',{})]
dood=[k for k in done if dnum(k)%11==5]
print('candidates',len(road),len(seas),len(cur),len(let),len(note),len(dood))
cases=[('road',road[-1] if road else None,'#view-chronicle .bday .pcard.gift'),('season',seas[-1] if seas else None,'#view-chronicle .bseas'),('curio',cur[-1] if cur else None,'#view-chronicle .bcurio'),('letter',let[-1] if let else None,'#view-chronicle .bletter'),('note',note[-1] if note else None,'#view-chronicle .bnote'),('doodle',dood[-1] if dood else None,'#view-chronicle .bdood')]
ok=[];out=f's77/{LANG}_{HH[:2]}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,d)
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,390,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(clk(day,HH));pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg)
    pg.add_style_tag(content="#toast{display:none!important}")
    for name,k,sel in cases:
        if not k: chk(f'{name}: a day exists in the save',False);continue
        s2=copy.deepcopy(S);s2['bookAt']='d:'+k;setst(pg,s2);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG);pg.reload();pg.wait_for_timeout(1300);closemodals(pg)
        openmap(pg);pg.evaluate("document.querySelector('.tab[data-tab=book]').click()");pg.wait_for_timeout(300);pg.evaluate("document.querySelector('.tab[data-tab=book]').click()");pg.wait_for_timeout(500)
        chk(f'{name} on {k}',pg.locator(sel).count()>=1,pg.inner_text('#view-chronicle .bday').replace('\n',' / ')[:260]);pg.screenshot(path=f'{out}/{name}.png',full_page=False)
        if name=='letter':
            pg.evaluate("document.querySelector('#view-chronicle .bletter').click()");pg.wait_for_timeout(400);chk('letter opens from the page',pg.evaluate("!!document.querySelector('#modal .lpaper')"))
        if name=='note':
            pg.add_script_tag(content=AXE);v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk('axe on a spread with a margin note',not v,v)
        closemodals(pg)
    # Say more
    s2=copy.deepcopy(S);s2['journal'].pop(day,None);setst(pg,s2);pg.reload();pg.wait_for_timeout(1300);closemodals(pg);tabto(pg,'today')
    chk('Say more shows after the question when nothing is written',pg.evaluate("!!document.getElementById('askMore')"))
    pg.evaluate("document.getElementById('askMore').click()");pg.wait_for_timeout(400)
    chk('…and opens your words with the question and your answer above',pg.evaluate("!!document.querySelector('#modal .saylead')&&!!document.getElementById('jIn')"),pg.inner_text('#modal')[:200].replace('\n',' / '))
    pg.screenshot(path=f'{out}/saymore.png');pg.fill('#jIn','Quick walk after dinner.');pg.evaluate("document.getElementById('jSave').click()");pg.wait_for_timeout(500);closemodals(pg);tabto(pg,'today')
    chk('…and goes away once you have written',not pg.evaluate("!!document.getElementById('askMore')"))
    chk('no page errors',not pg._errs,pg._errs[:2]);b.close()
print(sum(ok),'/',len(ok))
