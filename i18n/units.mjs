// Finds the translatable units in the English build: string literals and whole template literals (expressions become
// {0}, {1}...), skipping object keys, comparisons, switch cases and code-ish text. Shared by scan.mjs and build.mjs.
import * as acorn from 'acorn';import * as walk from 'acorn-walk';
export function scripts(html){const out=[];const re=/<script>([\s\S]*?)<\/script>/g;let m;while((m=re.exec(html)))out.push({src:m[1],at:m.index+8});return out;}
const strip=s=>s.replace(/\{\d+\}/g,' ').replace(/<[^>]*>/g,' ').replace(/&[#a-z0-9]+;/gi,' ');
const CODEY=/^(?:[\w.#\[\]=:,'"()\s-]*|.*(?:\d+px|rgba?\(|#[0-9a-f]{3,6}\b|data:|base64|https?:|[{};]\s*$).*)$/i;
// text the rules above would miss (punctuation only, or numbers): translated anyway
const FORCE=new Set(['<p class="small"><b>{0}.</b> {1} {2}{3}</p>','<p class="small"><b>{0}, {1}.</b> {2}.</p>','+1 to +3','\u2606 Favorite','\u2605 Favorited',' · Favorite','{0}. {1}','A mix','SMTWTFS','{0} to {1}','{0} asks: {1}','A {0} day.']);
export function isHuman(key){if(FORCE.has(key))return true;const t=(strip(key)+' '+[...key.matchAll(/(?:aria-label|alt|title|placeholder)="([^"]*)"/g)].map(m=>m[1].replace(/\{\d+\}/g,' ')).join(' ')).trim();if(!t)return false;
  if(/\.{4,}|\|/.test(t))return false;
  const ok=(t.match(/[A-Za-z ,.'’!?;:—–()-]/g)||[]).length/t.length;if(ok<.75)return false;
  if((/[A-Za-z]{2,}[ ,.!?'’:;—–-]+[A-Za-z]/.test(t)||/^[A-Z] [a-z]{3,}/.test(t))&&!/\d+px|font-|rgba?\(|var\(--|^\s*[.#][\w-]+\s*\{/.test(t))return true;   // a phrase
  if(/\{\d+\}/.test(key)&&/(^|[\s,.])[A-Za-z]{4,}([\s,.]|$)/.test(t)&&!/[(){};=<>]/.test(t))return true;                     // a template sentence around placeholders
  if(/\{\d+\}/.test(key)&&/^[A-Z][a-z]{2,}[\s,.:]*$/.test(t.replace(/[\s,.:·]+/g,' ').trim()+' '))return true;                       // 'Day {0}, {1}': one word around placeholders
  if(/^[A-Z][a-z’']+[.!?]?$/.test(t)||/^[A-Z][a-z]+ ?[a-z]*[.!?…]?$/.test(t))return 'word';                                       // a capitalised single word
  return false;}
export function units(html){const res=[];
  scripts(html).forEach((s,si)=>{const fnAt=[];for(const m of s.src.matchAll(/\n(?:function\s+(\w+)|const\s+(\w+)\s*=|let\s+(\w+)\s*=)/g))fnAt.push([m.index,m[1]||m[2]||m[3]]);
    const areaOf=p=>{let a='top';for(const [i,n] of fnAt){if(i>p)break;a=n;}return a;};const ast=acorn.parse(s.src,{ecmaVersion:'latest',sourceType:'script'});
    const skip=new Set();
    walk.full(ast,n=>{
      if(n.type==='Property'&&n.key)skip.add(n.key);
      if(n.type==='BinaryExpression'&&/^(===|!==|==|!=|in)$/.test(n.operator)){skip.add(n.left);skip.add(n.right);}
      if(n.type==='SwitchCase'&&n.test)skip.add(n.test);
      if(n.type==='TaggedTemplateExpression')skip.add(n.quasi);
      if(n.type==='CallExpression'){const c=n.callee,nm=c.type==='MemberExpression'?(c.property.name||''):(c.name||'');
        if(/^(querySelector(All)?|getElementById|getItem|setItem|removeItem|matches|closest|addEventListener|removeEventListener|setAttribute|getAttribute|toggle|add|remove|contains|test|replace|split|indexOf|includes|startsWith|endsWith|RegExp|measureText|createElement|postMessage|register)$/.test(nm))n.arguments.forEach(a=>skip.add(a));}
      if(n.type==='AssignmentExpression'&&n.left.type==='MemberExpression'&&/^(font|fillStyle|strokeStyle|className|id|textBaseline|textAlign|cssText|href|src|type)$/.test(n.left.property.name||''))skip.add(n.right);
      if(n.type==='MemberExpression'&&n.computed)skip.add(n.property);
      if(n.type==='ImportExpression'||n.type==='NewExpression'&&n.callee.name==='RegExp')n.arguments&&n.arguments.forEach(a=>skip.add(a));
    });
    const plural=new Set();
    walk.full(ast,n=>{if(n.type==='ConditionalExpression'&&[n.consequent,n.alternate].every(x=>x.type==='Literal'&&typeof x.value==='string'&&/^[a-z][a-z ’']{1,20}$/.test(x.value))){plural.add(n.consequent);plural.add(n.alternate);}});
    const at=res.length;
    walk.full(ast,n=>{
      if(skip.has(n))return;
      if(plural.has(n)){res.push({si,start:n.start,end:n.end,kind:'s',key:n.value,word:true});return;}
      if(n.type==='Literal'&&typeof n.value==='string'){const h=isHuman(n.value);if(h)res.push({si,start:n.start,end:n.end,kind:'s',key:n.value,word:h==='word'});}
      if(n.type==='TemplateLiteral'){const key=n.quasis.map((q,i)=>q.value.cooked+(i<n.expressions.length?'{'+i+'}':'')).join('');
        if(/\{\d+\}/.test(n.quasis.map(q=>q.value.cooked).join(''))) {/* literal braces in text: leave alone */}
        const h=isHuman(key);if(h)res.push({si,start:n.start,end:n.end,kind:'t',key,n:n.expressions.length,word:h==='word',exprs:n.expressions.map(e=>[e.start,e.end])});}
    });
    for(let k=at;k<res.length;k++)res[k].area=areaOf(res[k].start);});
  return res;}

// text in the page's own markup (outside scripts): text between tags and aria-label values
export function staticText(html){const b=html.slice(html.indexOf('<body')).replace(/<script[\s\S]*?<\/script>/g,'').replace(/<style[\s\S]*?<\/style>/g,'');
  const out=new Set();for(const m of b.matchAll(/>([^<>]+)</g)){const t=m[1].trim();if(/[A-Za-z]{2}/.test(t))out.add(t);}
  for(const m of b.matchAll(/aria-label="([^"]+)"/g))out.add(m[1]);return [...out];}
