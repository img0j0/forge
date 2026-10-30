const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
(async()=>{
const source=fs.readFileSync('work.html','utf8');const nodes=new Map();let blocked=true,stored='',backups=0;const daily={};
const element=()=>({style:{},children:[],setAttribute(){},appendChild(x){this.children.push(x)},remove(){nodes.delete(this.id)}});
const ctx={Set,JSON,Promise,document:{getElementById:id=>nodes.get(id),createElement:element,body:{prepend:x=>nodes.set(x.id,x)}},localStorage:{setItem(k,v){if(blocked)throw Error('quota');if(k===ctx.KEY)stored=v;else daily[k]=v},removeItem(k){delete daily[k]}},state:{_sv:0,cards:[{id:1,snackKnown:true,firstFind:{id:'key',at:'2026-10-26'}}]},sleepRun:null,KEY:'forge-app-v1',nset(){},nflush(){},remindSoon(){},openExport(){backups++}};
vm.createContext(ctx);vm.runInContext(source.slice(source.indexOf('const saveProblems='),source.indexOf('function rollover()')),ctx);
ctx.save();assert(nodes.has('saveWarning'));assert.equal(ctx.state.cards.length,1);nodes.get('saveWarning').children[1].onclick();assert.equal(backups,1);
ctx.save();assert.equal(nodes.size,1);blocked=false;nodes.get('saveWarning').children[2].onclick();assert.equal(nodes.size,0);assert.equal(JSON.parse(stored).cards[0].firstFind.id,'key');
ctx.saveProblem('native',true);ctx.save();assert(nodes.has('saveWarning'));ctx.saveProblem('native',false);assert.equal(nodes.size,0);
console.log('PASS storage failure warning, backup action, retry, memory preservation, independent native error');
blocked=true;assert.equal(ctx.save(),false,'a failed save reports false');blocked=false;assert.equal(ctx.save(),true,'a kept save reports true');
ctx.state.date='2026-10-30';vm.runInContext('dailyAt=null',ctx);ctx.save();assert(daily['forge-app-v1-daily'],'first save of the day keeps a safety copy');
vm.runInContext('tabAway=true',ctx);stored='';assert.equal(ctx.save(),false);assert.equal(stored,'','another tab in charge: nothing written');
vm.runInContext('tabAway=false;loadBad={raw:"x"}',ctx);assert.equal(ctx.save(),false);assert.equal(stored,'','unreadable save waiting: nothing written');vm.runInContext('loadBad=null',ctx);
console.log('PASS save reports success, keeps a daily safety copy, and writes nothing while another tab is in charge or a save is unreadable');
const CUR=(fs.readFileSync('pwa/sw.js','utf8').match(/const V='(forge-[0-9.]+)'/)||[])[1];assert(CUR,'cache name not found in pwa/sw.js');
const events={},deleted=[],writes=[];let response=new Response('new'),cached=new Response('old');
const sw={URL,Response,Promise,setTimeout,clearTimeout,location:{origin:'https://example.test'},self:{registration:{scope:'https://example.test/forge/'},addEventListener:(n,f)=>events[n]=f,clients:{claim:async()=>{}},skipWaiting:async()=>{}},fetch:async()=>response,caches:{keys:async()=>['forge-0.1.0','forge-0.2.0',CUR,'another-app','forge-unrelated'],delete:async k=>deleted.push(k),open:async()=>({put:async(k,v)=>writes.push(await v.text()),addAll:async()=>{}}),match:async()=>cached.clone()}};
vm.createContext(sw);vm.runInContext(fs.readFileSync('pwa/sw.js','utf8'),sw);
let activation;events.activate({waitUntil:p=>activation=p});await activation;assert.deepEqual(deleted,['forge-0.1.0','forge-0.2.0']);
async function navigate(url){let result,background;events.fetch({request:{method:'GET',url,mode:'navigate'},respondWith:p=>result=p,waitUntil:p=>background=p});const r=await result;await background;return r.text();}
assert.equal(await navigate('https://example.test/forge/'),'new');assert.deepEqual(writes,['new']);response=new Response('error',{status:503});assert.equal(await navigate('https://example.test/forge/'),'old');sw.fetch=async()=>{throw Error('offline')};assert.equal(await navigate('https://example.test/forge/index.html'),'old');
console.log('PASS scoped cache cleanup, network update, cache-write lifetime, HTTP-error and offline fallback');
})().catch(e=>{console.error(e);process.exitCode=1});
