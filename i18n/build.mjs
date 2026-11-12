// node build.mjs ../work.html ../app.html
// Makes the shipped app from the English build: every unit with a Japanese entry in ja/*.json becomes
//   (LJ?JA[id]:'English')                    for a string
//   (LJ?Lt(id,[a,b]):`English ${a} ${b}`)    for a template ({0}, {1}... in the Japanese, in any order)
// and the Japanese text is embedded once, as JSON, read only when the app runs in Japanese.
// It refuses entries that would break the page (placeholders or markup that differ from the English) and text that the
// code also compares or looks up (translating it would change behaviour), and lists them.
import fs from 'fs';import * as acorn from 'acorn';import * as walk from 'acorn-walk';import {units,scripts,staticText} from './units.mjs';
const [,,IN='../work.html',OUT='../app.html']=process.argv;
const html=fs.readFileSync(IN,'utf8');
const ja={};for(const f of fs.readdirSync('ja').filter(f=>f.endsWith('.json')).sort()){const o=JSON.parse(fs.readFileSync('ja/'+f));for(const k in o)if(o[k]!=='')ja[k]=o[k];}

// text the code compares, switches on or uses as a key: never translated
const fixed=new Set();
for(const s of scripts(html)){const ast=acorn.parse(s.src,{ecmaVersion:'latest',sourceType:'script'});
  const lit=n=>{if(n&&n.type==='Literal'&&typeof n.value==='string')fixed.add(n.value);};
  walk.full(ast,n=>{if(n.type==='BinaryExpression'&&/^(===|!==|==|!=)$/.test(n.operator)){lit(n.left);lit(n.right);}
    if(n.type==='SwitchCase')lit(n.test);if(n.type==='Property'&&n.key)lit(n.key);
    if(n.type==='MemberExpression'&&n.computed)lit(n.property);
    if(n.type==='CallExpression'&&n.callee.type==='MemberExpression'&&/^(includes|indexOf)$/.test(n.callee.property.name||''))n.arguments.forEach(lit);});}

// checks: same placeholders, same markup (tags, attribute names and non-text attribute values)
const ph=s=>(s.match(/\{\d+\}/g)||[]).sort().join(',');
const TXT_ATTR=/^(aria-label|title|alt|placeholder|aria-description|data-tip)$/;
const tags=s=>(s.match(/<\/?[a-zA-Z][^>]*>/g)||[]).map(t=>t.replace(/\s([\w-]+)="([^"]*)"/g,(m,a,v)=>' '+a+(TXT_ATTR.test(a)?'=…':'="'+v+'"'))).sort().join('');
const problems=[];
const U=units(html),byScript={};let id=0;const JA=[],idOf=new Map();
for(const u of U){const t=u.word?ja[u.key+'@'+u.area]:ja[u.key];if(t===undefined)continue;
  if(!u.word&&fixed.has(u.key)){problems.push(['compared or used as a key; left in English',u.key]);continue;}
  if(ph(t)!==ph(u.key)){problems.push(['placeholders differ',u.key,t]);continue;}
  if(tags(t)!==tags(u.key)){problems.push(['markup differs',u.key,t]);continue;}
  if(/\$\{|`/.test(t)&&!/\$\{|`/.test(u.key)){problems.push(['backtick or ${ in the Japanese',u.key,t]);continue;}
  const ik=u.word?u.key+'@'+u.area:u.key;   // a single word can differ by area ('Calm' a stat, 'Calm' a wish)
  if(!idOf.has(ik)){idOf.set(ik,id++);JA.push(t);}
  u.id=idOf.get(ik);(byScript[u.si]=byScript[u.si]||[]).push(u);}

const STATIC={};for(const k of staticText(html))if(ja[k]!==undefined)STATIC[k]=ja[k];
// rewrite each script: outermost units first; a template's expressions keep their own (nested) rewrites
function rewrite(src,list){list.sort((a,b)=>a.start-b.start||b.end-a.end);
  const render=(s,e,except)=>{let out='',p=s;for(const u of list){if(u===except||u.start<p||u.end>e||u.start<s)continue;
      out+=src.slice(p,u.start)+unit(u);p=u.end;}return out+src.slice(p,e);};
  const unit=u=>{if(u.kind==='s')return `(LJ?JA[${u.id}]:${src.slice(u.start,u.end)})`;
    const ex=u.exprs.map(([a,b])=>render(a,b));return `(LJ?Lt(${u.id},[${ex.join(',')}]):${render(u.start,u.end,u)})`;};
  return render(0,src.length);}
const S=scripts(html);let out='',p=0;
S.forEach((s,i)=>{out+=html.slice(p,s.at)+(byScript[i]?rewrite(s.src,byScript[i]):s.src);p=s.at+s.src.length;});
out+=html.slice(p);

// runtime: the language (saved choice, else the phone's), the Japanese text, and the template filler
const RUNTIME=`/* i18n (build.mjs): LJ is true when the app runs in Japanese; JA[id] is a Japanese unit; Lt fills {0}, {1}... */
const LANG=(()=>{try{const s=localStorage.getItem('forge-lang');if(s==='ja'||s==='en')return s;}catch(e){}return /^ja\\b/i.test(navigator.language||'')?'ja':'en';})();
const JA=LANG==='ja'?(()=>{try{return JSON.parse(document.getElementById('jaText').textContent);}catch(e){return null;}})():null,LJ=!!JA;
const Lt=(id,v)=>JA[id].replace(/\\{(\\d+)\\}/g,(m,n)=>String(v[+n]));
if(LJ){document.documentElement.lang='ja';const ST=${JSON.stringify(STATIC)};
  const fix=()=>{document.querySelectorAll('body *:not(script):not(style)').forEach(el=>{const a=el.getAttribute('aria-label');if(a&&ST[a])el.setAttribute('aria-label',ST[a]);
    el.childNodes.forEach(t=>{if(t.nodeType===3){const k=t.nodeValue.trim();if(k&&ST[k])t.nodeValue=t.nodeValue.replace(k,ST[k]);}});});};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fix);else fix();}
`;
const first=out.indexOf('<script>');
out=out.slice(0,first)+'<script type="application/json" id="jaText">'+JSON.stringify(JA).replace(/</g,'\\u003c')+'</script>\n<script>'+RUNTIME+out.slice(first+8);
// Japanese type: Latin letters keep their faces; kana and kanji fall to the phone's rounded or plain gothic
const JPL="local('HiraMaruProN-W4'),local('Hiragino Maru Gothic ProN W4'),local('Hiragino Maru Gothic ProN'),local('NotoSansCJKjp-Medium'),local('Noto Sans CJK JP Medium'),local('NotoSansJP-Medium'),local('Noto Sans JP'),local('YuGothic-Medium'),local('Meiryo')";
// the handwriting face is small for its size, so Japanese beside it is drawn smaller (JPHand); body text a touch smaller
const CSS=`<style id="jaType">@font-face{font-family:'JPHand';src:${JPL};size-adjust:76%}@font-face{font-family:'JPText';src:${JPL};size-adjust:93%}
html[lang=ja]{--jp:'JPText','Hiragino Maru Gothic ProN','Hiragino Sans','Noto Sans JP','Noto Sans CJK JP','Yu Gothic','Meiryo',sans-serif;
--body:'Nunito Sans',var(--jp);--display:'Nunito Sans',var(--jp)}
html.jr[lang=ja],html[lang=ja]{--hand:'Caveat','JPHand',var(--jp)}
html[lang=ja] body{line-break:strict;word-break:normal;overflow-wrap:anywhere}
html[lang=ja] #dateLabel{font-size:.88em}html[lang=ja] .scrim.jcov .tagline,html[lang=ja] .tagline{font-size:20px;line-height:1.35}html[lang=ja] .stat{grid-template-columns:4.1em 1fr 1.7em}html[lang=ja] .stat>span:first-child{white-space:nowrap;font-size:.92em}html[lang=ja] .odds td{white-space:nowrap}html[lang=ja] .odds th{font-size:11px;word-break:keep-all}
</style>`;
out=out.replace('</head>',CSS+'\n</head>');
fs.writeFileSync(OUT,out);
fs.writeFileSync('problems.json',JSON.stringify(problems,null,1));
console.log(`${OUT}: ${JA.length} Japanese units in use (${(Buffer.byteLength(JSON.stringify(JA))/1024).toFixed(0)} KB), ${problems.length} refused (problems.json), ${(out.length/1024).toFixed(0)} KB`);
