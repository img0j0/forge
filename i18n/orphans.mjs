// List (or with --rm, remove) Japanese entries that match nothing in the given HTML; same rule as scan.mjs's warning.
// Usage: node orphans.mjs ../work.html [--rm]
import fs from 'fs';import {units,staticText} from './units.mjs';
const [file,flag]=process.argv.slice(2),html=fs.readFileSync(file,'utf8'),U=units(html),live=new Set();
for(const u of U)live.add(u.word?u.key+'@'+u.area:u.key);for(const k of staticText(html))live.add(k);
let n=0;for(const f of fs.readdirSync('ja').filter(f=>f.endsWith('.json'))){const d=JSON.parse(fs.readFileSync('ja/'+f));let c=0;
  for(const k of Object.keys(d))if(!live.has(k)&&!live.has(k.replace(/@\w+$/,''))){console.log(f,JSON.stringify(k).slice(0,110));if(flag==='--rm'){delete d[k];c++;}n++;}
  if(c)fs.writeFileSync('ja/'+f,JSON.stringify(d,null,1));}
console.log(n,'orphans',flag==='--rm'?'removed':'');
