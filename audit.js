const fs=require('fs');const s=fs.readFileSync('work.html','utf8');
const out={};
out.bytes=s.length;
out.emdash=(s.match(/—/g)||[]).length; out.endash=(s.match(/–/g)||[]).length;
out.todo=(s.match(/TODO|FIXME|XXX/g)||[]).length;
out.consoleLog=(s.match(/console\.log/g)||[]).length;
out.externalUrls=[...new Set((s.match(/https?:\/\/[^\s"'<>)]+/g)||[]))].filter(u=>!u.startsWith('http://www.w3.org'));
// static id dupes in the html shell (before <script>)
const shell=s.slice(0,s.indexOf('<script>')); const ids=[...shell.matchAll(/\sid="([^"$]+)"/g)].map(m=>m[1]); out.dupStaticIds=ids.filter((x,i)=>ids.indexOf(x)!==i);
// events/lines lint
const ev=s.slice(s.indexOf('const EVENTS=['),s.indexOf('const WEPOCH'));
const strs=[...ev.matchAll(/'((?:[^'\\]|\\.)*)'/g)].map(m=>m[1]);
out.eventStrings=strs.length; out.eventLint=strs.filter(t=>/  |^\s|\s$|[A-Z]/.test(t.slice(0,1))||/[.!?]$/.test(t)||t.length>110).slice(0,10);
out.longest=strs.sort((a,b)=>b.length-a.length).slice(0,3).map(t=>[t.length,t]);
// odds
const odds=eval('('+s.match(/const ODDS=(\{[^;]*\});/)[1]+')'); const PITY=+s.match(/const PITY=(\d+)/)[1];
out.oddsSum=Object.fromEntries(Object.entries(odds).map(([k,v])=>[k,v.reduce((a,b)=>a+b,0)]));
let seed=12345;const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
const weighted=W=>{const t=W.reduce((a,b)=>a+b,0);let r=rnd()*t;for(let i=0;i<W.length;i++){r-=W[i];if(r<0)return i;}return W.length-1;};
function sim(years,model){let since=0,cnt=[0,0,0,0,0],maxGap=0,gap=0,total=0;
 const roll=W=>{if(since>=PITY)W=[0,0,70,24,6];const r=weighted(W);since=r>=2?0:since+1;cnt[r]++;total++;gap=r>=2?0:gap+1;maxGap=Math.max(maxGap,gap);return r;};
 for(let d=0;d<years*365;d++){roll(odds.daily);if(model==='pack'&&d%5===4){for(let i=0;i<4;i++)roll(odds.pack);roll(odds.packLast);}}
 return {total,perYear:cnt.map(c=>+(c/years).toFixed(1)),maxGap};}
out.sim_daily_only=sim(2000,'daily'); out.sim_with_packs=sim(2000,'pack');
console.log(JSON.stringify(out,null,1));
