# 0.51: your Forgeling on Today, a binder that scrolls, a joined Map/Tales/Journal switch, toasts from the top.
exec(open('qa_50.py').read().split('with sync_playwright() as p:')[0])
TO="()=>{const t=document.getElementById('toast');t.textContent='New ribbon: Curio Shelf and 2 more';t.classList.add('medal','show')}"
def boot(b,w,hr=11,reduce=False):
    kw={'reduced_motion':'reduce'} if reduce else {}
    ctx,pg=newpage(b,w,844,**kw); pg.clock.install(time=datetime.datetime(2027,3,3,hr,10)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); return ctx,pg
def lit(pg,sel):  # the canvas has drawn something
    return pg.evaluate("s=>{const c=document.querySelector(s);if(!c)return 0;const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n}",sel)
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in (320,390):
    for hr,nm in ((11,'day'),(22,'night')):
      ctx,pg=boot(b,w,hr); dev(pg,'week'); closemodals(pg); tabto(pg,'today'); pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(500)
      L=f"{w} {nm}"
      def put(f):
        x=st(pg); f(x); setst(pg,x); pg.reload(); pg.wait_for_selector(".tabs"); closemodals(pg); tabto(pg,'today'); pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(500)
      if st(pg)['status']!='fresh': dev(pg,'next'); closemodals(pg); tabto(pg,'today'); pg.wait_for_timeout(400)
      ms=pg.locator("#view-today .matestrip")
      rec("Today",f"{L}: your Forgeling is at the top of Today, above today's card",ms.count()==1 and pg.evaluate("()=>{const m=document.querySelector('.matestrip'),h=document.querySelector('#view-today .herowrap');return m.getBoundingClientRect().bottom<=h.getBoundingClientRect().top+1}"))
      x=st(pg); names={c.get('nick') or c['name'] for c in x['cards'] if c['id'] in x['hearth']['slots']}
      t=pg.inner_text("#view-today .matestrip")
      rec("Today",f"{L}: it names one of your Hearth companions and says where they are",any(t.startswith(n+' is ') for n in names) and re.search(r"by the fire|asleep|wandering",t) is not None,(t[:120],names))
      rec("Today",f"{L}: their picture is drawn",lit(pg,"#view-today .matestrip canvas")>200)
      rec("Today",f"{L}: it is a 44-point target and nothing spills sideways",pg.evaluate("()=>{const r=document.querySelector('.matestrip').getBoundingClientRect();return r.height>=44&&r.right<=innerWidth&&document.documentElement.scrollWidth<=innerWidth}"))
      rec("Today",f"{L}: there is no second Hearth row",pg.locator("#view-today .group #btnHearth").count()==0)
      if w==390: v=axe(pg); rec("Today",f"{L}: axe finds nothing",not v,v)
      pg.evaluate("document.querySelector('.matestrip').click()"); pg.wait_for_timeout(400)
      rec("Today",f"{L}: tapping it opens the Hearth",not pg.evaluate("document.getElementById('view-hearth').hidden") and pg.evaluate("document.getElementById('view-today').hidden"))
      sid=st(pg)['hearth']['slots'][0]
      # done state: the hero already shows a Forgeling, so no photo
      put(lambda x:x.update(status='done'))
      rec("Today",f"{L}: once today is done the photo steps aside for the day's card",pg.locator("#view-today .matestrip").count()==0)
      # wandering
      now=pg.evaluate("Date.now()")
      put(lambda x:x.update(status='fresh',wander={'id':sid,'start':now,'ready':now+2*3600*1000,'seed':7,'notified':False,'realm':None}))
      t=pg.inner_text("#view-today .matestrip") if pg.locator("#view-today .matestrip").count() else ''
      rec("Today",f"{L}: a wandering Forgeling is shown out wandering, with when they're back","out wandering" in t and "Back in" in t,t[:120])
      put(lambda x:x['wander'].update(ready=now-1000,notified=True)); closemodals(pg); tabto(pg,'today'); pg.wait_for_timeout(300)
      t=pg.inner_text("#view-today .matestrip") if pg.locator("#view-today .matestrip").count() else ''
      rec("Today",f"{L}: ...and back from wandering when they return","back from wandering" in t and pg.evaluate("document.querySelector('.matestrip').classList.contains('ready')"),t[:120])
      # toast
      tabto(pg,'today'); pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(3700); pg.evaluate(TO); pg.wait_for_timeout(500)
      r=pg.evaluate("()=>{const t=document.getElementById('toast').getBoundingClientRect(),n=document.querySelector('.tabs').getBoundingClientRect(),h=document.querySelector('.matestrip').getBoundingClientRect();return {top:t.top,bottom:t.bottom,h:t.height,right:t.right,left:t.left,tabs:n.top,mate:h.top}}")
      rec("Toast",f"{L}: a toast drops in at the top, clear of the tab bar and of your Forgeling",r['top']>=0 and r['top']<40 and r['bottom']<r['mate'] and r['bottom']<r['tabs'],r)
      rec("Toast",f"{L}: it fits the screen{' on one line' if w==390 else ''}",r['left']>=0 and r['right']<=w and (w<390 or r['h']<56),r)
      ctx.close()
  # binder with many cards
  for w in (320,390):
    ctx,pg=boot(b,w)
    x=st(pg); n=len(x['cards']); m=max(c['id'] for c in x['cards'])
    for i in range(60):
      c=json.loads(json.dumps(x['cards'][i%n])); c['id']=m+1+i; c['fav']=False; x['cards'].append(c)
    setst(pg,x)
    pg.reload(); pg.wait_for_selector(".tabs"); closemodals(pg); tabto(pg,'binder'); pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(500)
    N=len(st(pg)['cards']); L=f"{w}"
    cnt=lambda: pg.evaluate("document.querySelectorAll('#view-binder .binder [data-insp]').length")
    rec("Binder",f"{L}: no more Previous/Next pages",pg.locator("#pgPrev").count()==0 and pg.locator("#view-binder .pager").count()==0)
    rec("Binder",f"{L}: the first 24 show, with a Show more button saying how many are left",cnt()==24 and f"({N-24} more)" in pg.inner_text("#pgNext"),(cnt(),N))
    pg.evaluate("document.getElementById('pgNext').scrollIntoView()"); pg.wait_for_timeout(800)
    rec("Binder",f"{L}: scrolling down loads more by itself",cnt()==48,cnt())
    y0=pg.evaluate("scrollY")
    rec("Binder",f"{L}: ...without jumping you back to the top",y0>300,y0)
    for _ in range(3):
      if pg.locator("#pgNext").count(): pg.evaluate("document.getElementById('pgNext').click()"); pg.wait_for_timeout(300)
    rec("Binder",f"{L}: every Forgeling can be reached and the button goes away at the end",cnt()==N and pg.locator("#pgNext").count()==0,(cnt(),N))
    em=pg.evaluate("()=>[...document.querySelectorAll('#view-binder .binder .empty')].map(e=>[e.className,getComputedStyle(e,'::after').content])")
    rec("Binder",f"{L}: empty slots only finish the last row, quietly",len(em)==(-N)%3 and all('quiet' in c and a in ('none','normal') for c,a in em),em)
    pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(200); pg.evaluate("document.getElementById('btnSort').click()"); pg.wait_for_timeout(500)
    rec("Binder",f"{L}: sorting starts again from the top 24",cnt()==24,cnt())
    rec("Binder",f"{L}: Filter and Sort are round pills, 44 points tall",pg.evaluate("()=>[...document.querySelectorAll('.bbar .pill')].every(b=>{const c=getComputedStyle(b);return parseFloat(c.borderTopLeftRadius)>=20&&b.getBoundingClientRect().height>=44})"))
    rec("Binder",f"{L}: the page never scrolls sideways",pg.evaluate("document.documentElement.scrollWidth<=innerWidth"))
    if w==390: v=axe(pg); rec("Binder",f"{L}: axe finds nothing",not v,v)
    ctx.close()
  # few cards: quiet slots finish a row of three
  ctx,pg=boot(b,390); tabto(pg,'binder'); pg.wait_for_timeout(300)
  n=len(st(pg)['cards']); e=pg.locator("#view-binder .binder .empty").count()
  rec("Binder","a small binder shows its cards and just enough quiet slots to finish the row",(n+e)%3==0 and e<=2 or (n==0 and e==3),(n,e))
  ctx.close()
  # switch
  for w,hr,red in ((320,11,False),(390,11,False),(390,22,False),(390,11,True)):
    ctx,pg=boot(b,w,hr,red); L=f"{w} {'night' if hr==22 else 'day'}{' reduced' if red else ''}"
    tabto(pg,'chronicle'); pg.wait_for_timeout(300)
    seg=pg.locator("#view-chronicle .seg")
    rec("Switch",f"{L}: Map and Tales are one joined switch (the Journal is the Book tab since 0.78)",seg.count()==1 and seg.locator("button").count()==2 and pg.evaluate("()=>{const b=[...document.querySelectorAll('.seg button')].map(x=>x.getBoundingClientRect());return Math.abs(b[0].top-b[1].top)<1&&b[1].left-b[0].right<2&&b.every(r=>r.height>=44)}"))
    for i,s in enumerate(['tales','map']):
      pg.evaluate(f"document.querySelector('.seg [data-sub={s}]').click()"); pg.wait_for_timeout(450)
      ok=pg.evaluate("s=>{const g=document.querySelector('.seg'),b=g.querySelector('[data-sub='+s+']'),m=new DOMMatrix(getComputedStyle(g,'::before').transform),gl=g.getBoundingClientRect().left+3+m.m41;return b.getAttribute('aria-pressed')==='true'&&Math.abs(gl-b.getBoundingClientRect().left)<3}",s)
      rec("Switch",f"{L}: the highlight sits under {s.title()}",ok)
    an=pg.evaluate("getComputedStyle(document.querySelector('.seg'),'::before').animationName")
    rec("Switch",f"{L}: the highlight {'stays still' if red else 'slides'}",(an=='none') if red else (an=='segsl'),an)
    cr=pg.evaluate("()=>[...document.querySelectorAll('.seg button')].map(b=>getComputedStyle(b).color)")
    if w==390: v=axe(pg); rec("Switch",f"{L}: axe finds nothing (contrast included)",not v,v)
    ctx.close()
  b.close()
save_results("qa_51")
