// node scan.mjs ../work.html : lists translatable units by area, and which have no Japanese yet (i18n/todo/*.json).
import fs from 'fs';import {units,scripts,staticText} from './units.mjs';
const html=fs.readFileSync(process.argv[2]||'../work.html','utf8'),U=units(html),S=scripts(html);
const ja={};for(const f of fs.readdirSync('ja').filter(f=>f.endsWith('.json')))Object.assign(ja,JSON.parse(fs.readFileSync('ja/'+f)));
const area=u=>{const b=S[u.si].src.slice(0,u.start);const m=[...b.matchAll(/\n(?:function\s+(\w+)|const\s+(\w+)\s*=|let\s+(\w+)\s*=)/g)].pop();return m?(m[1]||m[2]||m[3]):'top';};
const by={};let have=0;const keys=new Set();
for(const u of U){const k=u.word?u.key+'@'+u.area:u.key;if(keys.has(k))continue;keys.add(k);if(ja[k]!==undefined||(!u.word&&ja[u.key]!==undefined)){have++;continue;}(by[u.area]=by[u.area]||{})[k]='';}
fs.rmSync('todo',{recursive:true,force:true});fs.mkdirSync('todo');
for(const [a,o] of Object.entries(by))fs.writeFileSync('todo/'+a+'.json',JSON.stringify(o,null,1));
{const st={};for(const k of staticText(html)){if(keys.has(k))continue;keys.add(k);if(ja[k]!==undefined){have++;continue;}st[k]='';}if(Object.keys(st).length)by['page']=st;}
const left=[...keys].length-have,words=Object.values(by).flatMap(o=>Object.keys(o)).reduce((n,k)=>n+k.replace(/<[^>]*>|\{\d+\}/g,' ').split(/\s+/).filter(w=>/[A-Za-z]/.test(w)).length,0);
console.log(`${U.length} units, ${keys.size} distinct; translated ${have}; to do ${left} (${words} words) in ${Object.keys(by).length} areas`);

// 0.59: warn about Japanese that no longer matches anything (an English template changed) and untranslated markup
{const live=new Set();for(const u of U)live.add(u.word?u.key+'@'+u.area:u.key);for(const k of staticText(html))live.add(k);
 const orphan=Object.keys(ja).filter(k=>!live.has(k)&&!live.has(k.replace(/@\w+$/,'')));
 const SKIPA=new Set(['renderSettings','pilotReport','runTool']);
 const mark=Object.entries(by).filter(([a])=>!SKIPA.has(a)).flatMap(([a,o])=>Object.keys(o).filter(k=>/<[a-z]/.test(k)&&/[A-Za-z]{3,} [A-Za-z]{3,}/.test(k.replace(/<[^>]*>/g,' '))).map(k=>a));
 if(orphan.length)console.log(`${orphan.length} Japanese entries match nothing now (an English text changed?): node -e to list, e.g. ${JSON.stringify(orphan[0]).slice(0,120)}`);
 if(mark.length)console.log(`untranslated markup in: ${[...new Set(mark)].join(', ')}`);}
