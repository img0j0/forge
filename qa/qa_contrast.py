from lib import *
# 0.44.2: text contrast on every screen, by day and by night, in light and dark themes (axe skips text on translucent
# backgrounds, which is how the "See <realm> in 3D" button went unread at night). Computes each visible text's colour
# against the composited background it actually sits on, including gradient fills; 4.5:1, or 3:1 for large text.
SCAN=r"""()=>{
 const P=c=>{const m=c.match(/[\d.]+/g);return m?m.map(Number).concat(m.length<4?[1]:[]):[0,0,0,0]};
 const L=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])};
 const over=(top,bot)=>{const a=top[3];return [top[0]*a+bot[0]*(1-a),top[1]*a+bot[1]*(1-a),top[2]*a+bot[2]*(1-a),1]};
 const bgOf=e=>{const layers=[];let p=e;while(p&&p.nodeType===1){const s=getComputedStyle(p);let c=P(s.backgroundColor);if(c[3]===0&&s.backgroundImage.includes('gradient')){const gs=s.backgroundImage.split(/,\s*(?=(?:linear|radial|repeating)-gradient)/);const last=gs[gs.length-1];const cs=last.match(/rgba?\([^)]*\)/g);if(cs)c=P(cs[cs.length-1]);}if(s.backgroundImage.includes('url(')&&c[3]<1)return null;if(c[3]>0)layers.push(c);if(c[3]>=1)break;p=p.parentElement}
   let b=layers.length&&layers[layers.length-1][3]>=1?layers.pop():P(getComputedStyle(document.documentElement).getPropertyValue('--bg')||'rgb(255,255,255)');if(b[3]<1)b=[b[0],b[1],b[2],1];for(let i=layers.length-1;i>=0;i--)b=over(layers[i],b);return b};
 const out=[];const scope=document.getElementById('modal').hidden?document.body:document.getElementById('modal');
 for(const e of scope.querySelectorAll('button,a,.chip,[role=button],summary,label,p,span,b,small,h2,h3,li')){
  const r=e.getBoundingClientRect();if(!r.width||e.closest('[hidden],details.dev,.sr')||e.closest('details:not([open])')&&!e.closest('summary'))continue;
  const own=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());if(!own)continue;const s=getComputedStyle(e);if(s.visibility==='hidden'||+s.opacity===0)continue;
  const bg=bgOf(e);if(!bg)continue;const fg=over(P(s.color),bg);const a=L(fg),b=L(bg);const cr=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  const big=parseFloat(s.fontSize)>=24||(parseFloat(s.fontSize)>=18.6&&+s.fontWeight>=700);if(cr<(big?3:4.5)&&!e.disabled&&e.getAttribute('aria-disabled')!=='true')out.push(cr.toFixed(2)+' '+e.tagName+(e.id?'#'+e.id:'')+' "'+(e.textContent||'').trim().slice(0,30)+'"')}
 return [...new Set(out)].slice(0,12)}"""

def setup(pg,theme):
    s=st(pg); c0=s["cards"][0]; cards=[]
    for i in range(20):
        c=json.loads(json.dumps(c0)); c.update(id=400+i,seed=9000+i*613,theme=i%10 if i<10 else i%5,dark=i>=5 and i<10,rarity=i%5); cards.append(c)
    s["cards"]=cards; s["explore"]={str(i):4 for i in range(10)}; s["forge"]["made"]=list(set(s["forge"].get("made",[])+["xlantern"])); s["settings"]["theme"]=theme
    setst(pg,s); pg.reload(); pg.wait_for_timeout(900); closemodals(pg)
CLK="(h)=>{}"
with sync_playwright() as p:
    b=p.chromium.launch()
    for hr in ("13:30","22:00"):
        for theme in ("light","dark"):
            ctx,pg=newpage(b,390,844,timezone_id="America/New_York")
            pg.add_init_script("(()=>{const R=Date;const t=new R();const want=new R(t.getFullYear(),t.getMonth(),t.getDate(),%d,%d).getTime();const off=want-R.now();class D extends R{constructor(...a){if(a.length)super(...a);else super(R.now()+off);}static now(){return R.now()+off;}}window.Date=D;})()"%tuple(map(int,hr.split(":"))))
            pg.goto(P); pg.wait_for_selector("#titleGo"); first_card(pg); closemodals(pg); setup(pg,theme)
            bad={}
            for t in ["today","hearth","binder","settings","chronicle"]:
                tabto(pg,t); closemodals(pg); r=pg.evaluate(SCAN)
                if r: bad[t]=r
            for sub in ["tales","journal"]:
                tabto(pg,"chronicle"); pg.evaluate("s=>{const b=document.querySelector('[data-sub=\"'+s+'\"]');if(b)b.click()}",sub); pg.wait_for_timeout(300); r=pg.evaluate(SCAN)
                if r: bad[sub]=r
            for ti in range(10):
                pg.evaluate("ti=>{const x=document.createElement('button');x.dataset.realmopen=ti;document.body.appendChild(x);x.click();x.remove()}",ti); pg.wait_for_timeout(350); r=pg.evaluate(SCAN)
                if r: bad["realm%d"%ti]=r
            for hid in ["hShelf","hFurn","hKeeps","hComp","hForge","hChange","hPlay","hSnack","hStory","hWander"]:
                closemodals(pg); tabto(pg,"hearth")
                if pg.evaluate("i=>{const e=document.getElementById(i);if(!e)return false;e.click();return true}",hid):
                    pg.wait_for_timeout(400); r=pg.evaluate(SCAN)
                    if r: bad[hid]=r
            closemodals(pg)
            rec("Contrast",f"{hr} {theme}: every text on every screen, realm page and Hearth sheet reads at 4.5:1 (3:1 large)",not bad,bad)
            rec("All",f"{hr} {theme}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_contrast"); print(sum(r["ok"] for r in RES),"/",len(RES))
