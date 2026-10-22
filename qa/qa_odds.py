from lib import *
import subprocess
src=open(S+"/work.html").read()
js=r'''
const fs=require('fs');const s=fs.readFileSync(process.argv[2],'utf8');
const cut=(a,b)=>s.slice(s.indexOf(a),s.indexOf(b,s.indexOf(a)));
const g=re=>s.match(re)[0];
const code=g(/const ODDS=\{[^\n]*\n/)+g(/const PITY=\d+;/)+g(/function weighted\(W\)\{[^\n]*\n/)+g(/function rollRarity\(W\)\{[\s\S]*?\n\}\n/);
let seed=2024;Math.random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
const state={pity:{since:0}};
const mod=new Function('state',code+';return {ODDS,PITY,rollRarity};')(state);
const {ODDS,PITY,rollRarity}=mod;
const Y=3000,cnt=[0,0,0,0,0];let n=0,gap=0,maxGap=0;
const roll=W=>{const r=rollRarity(W);cnt[r]++;n++;gap=r>=2?0:gap+1;maxGap=Math.max(maxGap,gap);};
for(let d=0;d<Y*365;d++){roll(ODDS.daily);if(d%5===4){for(let i=0;i<4;i++)roll(ODDS.pack);roll(ODDS.packLast);}}
console.log(JSON.stringify({ODDS,PITY,perYear:cnt.map(c=>c/Y),maxGap,sums:Object.values(ODDS).map(a=>a.reduce((x,y)=>x+y,0))}));
'''
open(S+"/odds_real.js","w").write(js)
r=json.loads(subprocess.check_output(["node",S+"/odds_real.js",S+"/work.html"]).decode())
rec("Odds","every published pull table sums to exactly 100%",all(abs(x-100)<1e-9 for x in r["sums"]),r["sums"])
rec("Odds","real rarity code: Legendaries per year for a player who opens every day and every pack is 1.5 to 4",1.5<=r["perYear"][4]<=4,round(r["perYear"][4],2))
rec("Odds","real code: the safety net holds, never more than 14 in a row without a Rare or better",r["maxGap"]<=14,r["maxGap"])
pw=re.search(r"if\(state\.pity\.since>=PITY\)W=\[([^\]]*)\]",src).group(1).split(","); pw=[float(x) for x in pw]
rec("Odds","the guaranteed pull after the safety net cannot be a Common or Uncommon, and sums to 100",pw[0]==0 and pw[1]==0 and abs(sum(pw)-100)<1e-9,pw)
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,568),(390,844)]:
        ctx,pg=newpage(b,W,H); pg.set_default_timeout(6000); pg.goto(P); pg.wait_for_selector("#ageGo, #titleGo"); first_card(pg); closemodals(pg)
        s0=st(pg); s0["seen"]=18; setst(pg,s0); pg.reload(); pg.wait_for_timeout(600); closemodals(pg)
        tabto(pg,"settings"); pg.evaluate("()=>{const b=[...document.querySelectorAll('#view-settings button')].find(x=>/odds/i.test(x.textContent));b&&b.click()}"); pg.wait_for_timeout(400)
        t=mt(pg); rows=pg.evaluate("()=>[...document.querySelectorAll('#modal table.odds tbody tr')].map(r=>[...r.cells].map(c=>c.textContent))")
        exp={"Daily":r["ODDS"]["daily"],"All in":r["ODDS"]["allIn"],"Pack":r["ODDS"]["pack"],"Last in pack":r["ODDS"]["packLast"]}
        okrows=all([float(x.rstrip('%')) for x in row[1:]]==exp[row[0]] for row in rows) and len(rows)==4
        rec("Odds",f"{W}px: the Fair odds sheet shows exactly the odds the code uses",okrows,rows[0] if rows else t[:80])
        ov=pg.evaluate("()=>{const t=document.querySelector('#modal table.odds');const s=t.closest('[role=dialog]');return t.scrollWidth<=s.clientWidth+1}")
        rec("Odds",f"{W}px: the odds table fits without sideways scrolling",ov)
        rec("Odds",f"{W}px: the sheet shows the safety net text with a live count","away right now" in t,"")
        ctx.close()
    b.close()
save_results("qa_odds"); print(sum(r["ok"] for r in RES),"/",len(RES))
