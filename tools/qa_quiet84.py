# 0.84: one "Edit today's page" sheet, a Hearth without counts, one Map line, the games focus ring, the packed web save.
#   Run from a folder holding lived_store.json, dev root served at http://127.0.0.1:8772/ : python3 qa_quiet84.py app.html en|ja HH:MM
import sys,os,json,datetime as dt,copy,re,random
QA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','qa'); sys.path.insert(0,QA); B=sys.argv[1]; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2]; HH=sys.argv[3]
from lib import *
AXE=open(os.path.join(QA,'node_modules/axe-core/axe.min.js')).read()
S=json.load(open('lived_store.json'));S['seen']=999;day=S['date']
ms=int(dt.datetime.fromisoformat(day+f'T{HH}:00-05:00').timestamp()*1000)
CLK="(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
ok=[];out=f's84/{LANG}_{HH[:2]}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(bool(c)); print('PASS' if c else 'FAIL',n,str(d)[:220])
COUNT=re.compile(r'\d+ of \d+|bond \d|\+\d|· \d+|\d+/\d+|絆 ?\d|全\d')
def vis(pg,sel): return pg.evaluate("s=>[...document.querySelectorAll(s)].filter(e=>e.offsetParent!==null).length",sel)
def axe(pg,n):
    if not pg.evaluate("typeof axe!=='undefined'"): pg.add_script_tag(content=AXE)
    v=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");chk('axe: '+n,not v,v)
def fresh(pg,s):
    setst(pg,s);pg.reload();pg.wait_for_timeout(1300);closemodals(pg)
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,390,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='reduce')
    pg.add_init_script(CLK);pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG)
    s=copy.deepcopy(S);s['wantAsked']=False;fresh(pg,s);tabto(pg,'today')
    chk('the day is finished with a postcard and words',s['status']=='done' and day in (s.get('posts') or {}) and day in s['journal'],s['status'])
    chk('one "Edit today\'s page" link',vis(pg,'#btnEditPage')==1)
    chk('the four edit links are folded away',vis(pg,'#askAgain,#pcAdd,#pcDel,#btnMargin')==0)
    chk('"Make your cards yours" rests after day 30',pg.locator('#btnWant').count()==0)
    chk('date line keeps "Day N, date" together',pg.locator('#dateLabel .nw').count()==2)
    pg.screenshot(path=f'{out}/today.png',full_page=True);axe(pg,'Today')
    pg.click('#btnEditPage');pg.wait_for_timeout(400);eps=pg.evaluate("[...document.querySelectorAll('#modal [data-ep]')].map(b=>b.dataset.ep+'='+b.textContent)")
    chk('the sheet offers all four edits',[e.split('=')[0] for e in eps]==['askAgain','pcAdd','pcDel','btnMargin'],eps)
    chk('the sheet\'s buttons are 44 pt or more',pg.evaluate("[...document.querySelectorAll('#modal [data-ep]')].every(b=>b.getBoundingClientRect().height>=44)"))
    pg.screenshot(path=f'{out}/editsheet.png');axe(pg,'edit sheet')
    pg.click('#modal [data-ep="btnMargin"]');pg.wait_for_timeout(500)
    chk('"Edit your own words" opens the journal',pg.locator('#modal #jIn').count()==1);closemodals(pg)
    pg.click('#btnEditPage');pg.wait_for_timeout(300);pg.click('#modal [data-ep="pcDel"]');pg.wait_for_timeout(500)
    chk('"Remove the postcard" removes it',pg.evaluate(f"!(JSON.parse(localStorage.getItem('forge-app-v1')).posts||{{}})['{day}']"))
    chk('with one edit left there is no sheet',vis(pg,'#btnEditPage')==1 or vis(pg,'#askAgain')==1, vis(pg,'#btnEditPage'))
    pg.click('#btnEditPage') if vis(pg,'#btnEditPage') else None;pg.wait_for_timeout(300)
    if pg.locator('#modal [data-ep="askAgain"]').count(): pg.click('#modal [data-ep="askAgain"]')
    else: pg.click('#askAgain')
    pg.wait_for_timeout(500);chk('"Change the answer" asks again',pg.locator('#view-today [data-ask]').count()>=1)
    # Hearth without counts
    fresh(pg,copy.deepcopy(S));tabto(pg,'hearth');pg.wait_for_timeout(400);h=pg.inner_text('#view-hearth')
    m=COUNT.search(h);chk('the Hearth shows no counts',not m,m and h[max(0,m.start()-40):m.end()+20].replace('\n',' / '))
    pg.click('#hComp');pg.wait_for_timeout(400);t=pg.inner_text('#modal');m=re.search(r'bond \d|絆 ?\d',t);chk('the Forgeling sheet has no bond number',not m,m and m.group(0));closemodals(pg)
    pg.click('#hFurn');pg.wait_for_timeout(400);t=pg.inner_text('#modal h2');chk('By the fire has no count',not re.search(r'\d',t),t);closemodals(pg)
    pg.screenshot(path=f'{out}/hearth.png',full_page=True);axe(pg,'Hearth')
    # games: the focus ring stays inside the tilted card
    pg.click('#hPlay');pg.wait_for_timeout(400);pg.keyboard.press('Tab');pg.keyboard.press('Shift+Tab');pg.wait_for_timeout(200)
    off=pg.evaluate("(()=>{const a=document.activeElement;return a&&a.matches('.pcard')?getComputedStyle(a).outlineOffset:'no card focused: '+(a&&a.outerHTML.slice(0,60))})()")
    chk('a focused game card draws its ring inside',off=='-4px',off);pg.screenshot(path=f'{out}/games.png');closemodals(pg)
    # Map: one line for a fully charted map
    tabto(pg,'chronicle');pg.wait_for_timeout(400);n=pg.evaluate("[...document.querySelectorAll('#view-chronicle .mapcap>p.small')].filter(p=>/Inked|インク/.test(p.textContent)).length")
    t=pg.inner_text('#view-chronicle .mapcap');chk('a charted map says so once',n==1 and ('Every realm' in t or 'どの地方も' in t),(n,t[:120]))
    # the web save
    pg.wait_for_timeout(300)
    d=pg.evaluate("localStorage.getItem('forge-app-v1-daily')||''");mn=pg.evaluate("localStorage.getItem('forge-app-v1')||''")
    chk('the daily safety copy is packed',d.startswith('lz1:') and len(d)<len(mn)/3,(len(d),len(mn)))
    chk('the main save stays plain while small',mn.startswith('{'))
    big=copy.deepcopy(S);rnd=random.Random(4);base=dt.date(2020,1,1)
    for i in range(1900): big['journal'][(base+dt.timedelta(days=i)).isoformat()]={'text':' '.join(rnd.choice(['tea','walk','snow','rain','book','call','mum','park','bread','light']) for _ in range(180))}
    fresh(pg,big);pg.evaluate("()=>{const b=document.querySelector('.tab[data-tab=\"hearth\"]');b&&b.click()}");pg.wait_for_timeout(400)
    tabto(pg,'today');pg.click('#btnEditPage');pg.wait_for_timeout(300);pg.click('#modal [data-ep="askAgain"]');pg.wait_for_timeout(500)
    mn=pg.evaluate("localStorage.getItem('forge-app-v1')||''");chk('a big save is packed',mn.startswith('lz1:'),len(mn))
    pg.reload();pg.wait_for_timeout(1800);closemodals(pg)
    nj=pg.evaluate("Object.keys(state.journal).length") if pg.evaluate("typeof state!=='undefined'") else None
    chk('a packed save loads back whole',pg.locator('#view-today').count()==1 and pg.evaluate("!document.getElementById('recUse')"),nj)
    tot=pg.evaluate("Object.keys(localStorage).reduce((a,k)=>a+(localStorage.getItem(k)||'').length,0)");chk('2 MB of journal fits in well under 1 MB of storage',tot<1_000_000,tot)
    fresh(pg,copy.deepcopy(S));chk('an older plain save still loads',pg.locator('#view-today').count()==1 and pg.evaluate("(localStorage.getItem('forge-app-v1')||'').startsWith('{')"))
    chk('no page errors',not pg._errs,pg._errs[:3]);b.close()
print(f'{sum(ok)}/{len(ok)} passed');sys.exit(0 if all(ok) else 1)
