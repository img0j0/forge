const fs=require('fs');
function load(f){const s=fs.readFileSync(f,'utf8');
 const wh=s.match(/(?:const whash=|function whash)[^\n]*\n/)[0];
 const ev=s.slice(s.indexOf('const EVENTS=['),s.indexOf('const WEPOCH'));
 const we=s.match(/(?:const EV2=287;[^\n]*\n)?function worldEvent[^\n]*\n/)[0];
 const code=wh+ev+we+';module.exports={worldEvent,EVENTS}';
 const m={exports:{}};new Function('module',code)(m);return m.exports;}
const A=load('base14.html'),B=load('work.html');
let diff=0,nulls=0,hi=new Set(),n=0;
for(let d=0;d<700;d++){const a=A.worldEvent(d),b=B.worldEvent(d);
 if((a===null)!==(b===null))nulls++;
 if(d<287&&JSON.stringify(a)!==JSON.stringify(b))diff++;
 if(d>=287&&b)hi.add(b.kind);}
console.log(JSON.stringify({changedBefore:diff,nullMismatch:nulls,kindsAfter:[...hi].sort((x,y)=>x-y),counts:B.EVENTS.map(r=>r.length),pairsOk:B.EVENTS.every(r=>r.every(e=>e.length===2&&e[0]&&e[1]))}));
