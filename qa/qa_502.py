# 0.50.2: the update note ("Load it") and toasts are easy to read by day and by night.
exec(open('qa_50.py').read().split('with sync_playwright() as p:')[0])
MK="""()=>{const b=document.createElement('div');b.id='updBar';b.className='updbar';b.setAttribute('role','status');b.innerHTML='<span>A new version of Forgelings is ready.</span><button type="button" id="updGo">Load it</button><button type="button" class="later" id="updLater">Later</button>';document.body.appendChild(b);const t=document.getElementById('toast');t.textContent='Saved.';t.classList.add('show')}"""
CR="""()=>{const rgb=s=>s.match(/[\\d.]+/g).map(Number);const L=c=>{const [r,g,b]=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
 const cr=(a,b)=>{const x=L(rgb(a)),y=L(rgb(b));return +((Math.max(x,y)+.05)/(Math.min(x,y)+.05)).toFixed(2)};const cs=e=>getComputedStyle(document.querySelector(e));
 const bar=cs('#updBar'),go=cs('#updGo'),la=cs('#updLater'),to=cs('#toast');const pageBg=getComputedStyle(document.querySelector('.app')||document.body).backgroundColor;
 return {msg:cr(bar.color,bar.backgroundColor),go:cr(go.color,go.backgroundColor),goVsBar:cr(go.backgroundColor,bar.backgroundColor),later:cr(la.color,bar.backgroundColor),toast:cr(to.color,to.backgroundColor),
  h:document.getElementById('updGo').getBoundingClientRect().height}}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for hr,nm in [(11,'Day'),(22,'Night')]:
    for w in (320,390):
      ctx,pg=newpage(b,w,844); pg.clock.install(time=datetime.datetime(2027,3,3,hr,10)); pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg)
      pg.evaluate(MK); pg.wait_for_timeout(500); c=pg.evaluate(CR)
      rec(nm,f"{w}: the update message reads clearly (4.5:1 or better)",c['msg']>=4.5,c)
      rec(nm,f"{w}: Load it reads clearly and stands out from the note",c['go']>=4.5 and c['goVsBar']>=3,c)
      rec(nm,f"{w}: Later reads clearly",c['later']>=4.5,c)
      rec(nm,f"{w}: a toast reads clearly",c['toast']>=4.5,c)
      rec(nm,f"{w}: Load it is at least 44 points tall",c['h']>=44,c['h'])
      if w==390:
        v=axe(pg); rec(nm,"axe finds nothing",not v,v)
        pg.screenshot(path=f'shots/qa502_{nm.lower()}.png')
      ctx.close()
  b.close()
save_results("qa_502")
