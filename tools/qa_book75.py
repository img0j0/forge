# 0.75 book test (21 checks). Run from a folder holding lived_store.json (tools/lived_save.py) with the dev root served at
#   http://127.0.0.1:8772/ : python3 qa_book75.py work.html|app.html en|ja HH:MM WIDTH. Screenshots go to ./b75/.
import sys,os,json,datetime as dt
sys.path.insert(0,'/home/claude/forge/qa'); B=sys.argv[1] if len(sys.argv)>1 else 'work.html'; os.environ['FORGE_HTML']='http://127.0.0.1:8772/'+B
LANG=sys.argv[2] if len(sys.argv)>2 else 'en'; HH=sys.argv[3] if len(sys.argv)>3 else '16:00'; W=int(sys.argv[4]) if len(sys.argv)>4 else 390
from lib import *
AXE=open('/home/claude/forge/qa/node_modules/axe-core/axe.min.js').read()
S=json.load(open('lived_store.json'));S['seen']=999;S.pop('bookAt',None);day=S['date']
ms=int(dt.datetime.fromisoformat(day+f'T{HH}:00-05:00').timestamp()*1000)
CLK="(()=>{const R=Date;const off=%d-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%ms
ok=[];out=f'b75/{LANG}_{HH[:2]}_{W}';os.makedirs(out,exist_ok=True)
def chk(n,c,d=''): ok.append(c); print('PASS' if c else 'FAIL',n,d)
with sync_playwright() as p:
    b=p.chromium.launch();ctx,pg=newpage(b,W,844,timezone_id='America/New_York',device_scale_factor=2,reduced_motion='no-preference')
    pg.add_init_script(CLK);pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);setst(pg,S);pg.evaluate("l=>localStorage.setItem('forge-lang',l)",LANG);pg.reload();pg.wait_for_timeout(1500);closemodals(pg)
    pg.add_style_tag(content="#toast{display:none!important}")
    def snap(n): pg.wait_for_timeout(450); pg.screenshot(path=f'{out}/{n}.png')
    def txt(): return pg.inner_text('#modal .zbox')
    openmap(pg);pg.evaluate("document.querySelector('[data-sub=journal]').click()");pg.wait_for_timeout(400)
    chk('Journal has Open your book',pg.evaluate("!!document.getElementById('bookOpen')"))
    chk('Monthly books button gone',not pg.evaluate("!!document.getElementById('bookZines')"))
    pg.evaluate("document.getElementById('bookOpen').click()");pg.wait_for_timeout(500)
    chk('first open shows the contents',pg.evaluate("!!document.querySelector('#modal .btoc')"));snap('1-contents')
    rows=pg.evaluate("[...document.querySelectorAll('[data-bkgo]')].map(b=>b.innerText.replace(/\\n/g,' | '))");print(rows)
    chk('five chapters listed',len(rows)==5,len(rows))
    chk('current month still being written','still being written' in rows[0] or 'まだ書きかけ' in rows[0])
    pg.evaluate("document.querySelectorAll('[data-bkgo]')[1].click()");pg.wait_for_timeout(500)
    t=txt();print('chapter:',t.replace('\n',' | '));chk('chapter title page',pg.evaluate("!!document.querySelector('#modal .bch')"));snap('2-chapter')
    pg.evaluate("document.getElementById('bkNext').click()");pg.wait_for_timeout(500)
    chk('next is a day spread',pg.evaluate("!!document.querySelector('#modal .bday .bprint img')"));snap('3-day')
    # a day with a postcard and words
    k=[d for d in sorted(S['posts']) if (S['journal'].get(d) or {}).get('text')][-1]
    pg.evaluate("k=>{const i=1;}",k)
    pg.evaluate("document.getElementById('bkToc').click()");pg.wait_for_timeout(400)
    pg.evaluate("document.querySelectorAll('[data-bkgo]')[0].click()");pg.wait_for_timeout(400)
    for i in range(60):
        if pg.evaluate("!!document.querySelector('#modal .bday .pcard')&&!!document.querySelector('#modal .bday .mine')"): break
        pg.evaluate("document.getElementById('bkNext').click()");pg.wait_for_timeout(120)
    chk('a spread with postcard and your words',pg.evaluate("!!document.querySelector('#modal .bday .pcard')&&!!document.querySelector('#modal .bday .mine')"));snap('4-day-full')
    chk('turn animation runs (motion on)',pg.evaluate("!!document.querySelector('#modal .zpage.bkf,#modal .zpage.bkb')"))
    at=pg.evaluate("JSON.parse(localStorage.getItem('forge-app-v1')).bookAt");print('ribbon',at)
    closemodals(pg);pg.evaluate("document.getElementById('bookOpen').click()");pg.wait_for_timeout(400)
    chk('reopens where you left off',pg.evaluate("JSON.parse(localStorage.getItem('forge-app-v1')).bookAt")==at and pg.evaluate("!!document.querySelector('#modal .bday')"),at)
    before=pg.inner_text('#modal .znav + *') if False else pg.evaluate("document.querySelector('#modal .muted.small.center').innerText")
    pg.keyboard.press('ArrowRight');pg.wait_for_timeout(300);a1=pg.evaluate("document.querySelector('#modal .muted.small.center').innerText")
    chk('arrow key turns',a1!=before,(before,a1))
    bx=pg.evaluate("(()=>{const r=document.querySelector('#modal .zbox').getBoundingClientRect();return [r.x+r.width*0.8,r.y+r.height/2]})()")
    pg.mouse.move(bx[0],bx[1]);pg.mouse.down();pg.mouse.move(bx[0]-150,bx[1]+5,steps=6);pg.mouse.up();pg.wait_for_timeout(300)
    a2=pg.evaluate("document.querySelector('#modal .muted.small.center').innerText");chk('swipe turns',a2!=a1,(a1,a2))
    # walk to a chapter end and the back
    pg.evaluate("document.getElementById('bkToc').click()");pg.wait_for_timeout(300)
    n=pg.evaluate("+document.querySelector('#modal .muted.small.center').innerText.match(/\\d+/g).at(-1)")
    pg.evaluate("document.querySelectorAll('[data-bkgo]')[0].click()");pg.wait_for_timeout(300)
    for i in range(80):
        if pg.evaluate("!!document.querySelector('#modal .zback')"): break
        pg.evaluate("document.getElementById('bkNext').click()");pg.wait_for_timeout(60)
    chk('chapter ends with its month page',pg.evaluate("!!document.querySelector('#modal .zback [data-bkpic]')"));snap('5-end')
    pg.evaluate("document.getElementById('bkNext').click()");pg.wait_for_timeout(300)
    chk('then the back of the book',pg.evaluate("!!document.querySelector('#modal .bback #jYear')"));snap('6-back')
    chk('last page: Next disabled',pg.evaluate("document.getElementById('bkNext').disabled"))
    # cover
    pg.evaluate("(()=>{for(let i=0;i<300;i++){const b=document.getElementById('bkPrev');if(!b||b.disabled)break;b.click();}})()");pg.wait_for_timeout(300)
    chk('first page is the cover',pg.evaluate("!!document.querySelector('#modal .bcov')"));snap('0-cover')
    # axe on cover, contents, chapter, day
    pg.add_script_tag(content=AXE);vio=[]
    for step in ['cover','toc','ch','day']:
        if step=='toc': pg.evaluate("document.getElementById('bkToc').click()")
        if step=='ch': pg.evaluate("document.querySelectorAll('[data-bkgo]')[0].click()")
        if step=='day': pg.evaluate("document.getElementById('bkNext').click()")
        pg.wait_for_timeout(500)
        r=pg.evaluate("axe.run(document.getElementById('modal'),{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))");vio+=r
    chk('axe: zero violations on the book pages',not vio,vio)
    ov=pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1&&[...document.querySelectorAll('#modal .zpage *')].every(e=>e.getBoundingClientRect().right<=innerWidth+1)")
    chk('nothing runs off the screen',ov)
    small=pg.evaluate("[...document.querySelectorAll('#modal button')].filter(b=>b.offsetParent&&b.getBoundingClientRect().height<44).map(b=>b.innerText.slice(0,20))");chk('buttons at least 44 pt',not small,small)
    closemodals(pg)
    # Today's "is bound" row opens the chapter
    chk('no page errors',not pg._errs,pg._errs[:3])
    b.close()
    # reduced motion
    b=p.chromium.launch();ctx,pg=newpage(b,W,844,timezone_id='America/New_York',reduced_motion='reduce')
    pg.add_init_script(CLK);pg.goto(P);pg.wait_for_selector('#titleGo');first_card(pg);closemodals(pg);setst(pg,S);pg.reload();pg.wait_for_timeout(1200);closemodals(pg)
    openmap(pg);pg.evaluate("document.querySelector('[data-sub=journal]').click()");pg.wait_for_timeout(300);pg.evaluate("document.getElementById('bookOpen').click()");pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('bkNext').click()");pg.wait_for_timeout(300)
    chk('reduced motion: no turn animation',pg.evaluate("document.getAnimations().filter(a=>a.animationName&&a.animationName.startsWith('bkIn')).length")==0)
    b.close()
print(sum(ok),'/',len(ok))
