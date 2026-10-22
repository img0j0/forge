let seed=777;const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
const weighted=W=>{const t=W.reduce((a,b)=>a+b,0);let r=rnd()*t;for(let i=0;i<W.length;i++){if(r<W[i])return i;r-=W[i];}return 0;};
function run(O,PITYW,allInShare,years=3000){let since=0,cnt=[0,0,0,0,0],maxGap=0,gap=0,n=0;
 const roll=W=>{if(since>=14)W=PITYW;const r=weighted(W);since=r>=2?0:since+1;cnt[r]++;n++;gap=r>=2?0:gap+1;maxGap=Math.max(maxGap,gap);};
 for(let d=0;d<years*365;d++){roll(rnd()<allInShare?O.allIn:O.daily);if(d%5===4){for(let i=0;i<4;i++)roll(O.pack);roll(O.packLast);}}
 return {perYear:cnt.map(c=>+(c/years).toFixed(1)),pct:cnt.map(c=>+(100*c/n).toFixed(2)),maxGap};}
const cur={daily:[55,27,12,5,1],allIn:[42,30,18,8,2],pack:[55,27,12,5,1],packLast:[0,45,35,16,4]};
const nw={daily:[55.7,27,12,5,0.3],allIn:[43.5,30,18,8,0.5],pack:[55.7,27,12,5,0.3],packLast:[0,47,37,15.4,0.6]};
console.log('current, never all in',JSON.stringify(run(cur,[0,0,70,24,6],0)));
console.log('new, never all in    ',JSON.stringify(run(nw,[0,0,74,25.5,0.5],0)));
console.log('new, all in daily    ',JSON.stringify(run(nw,[0,0,74,25.5,0.5],1)));
