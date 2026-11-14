// Print the source text of top-level function/const declarations named on the command line.
// Usage: node tools/fnrange.mjs file.html name1 name2 ...   (uses acorn from i18n/node_modules)
import fs from 'fs';import {createRequire} from 'module';const require=createRequire(import.meta.url);
const acorn=require('../i18n/node_modules/acorn');
const [file,...names]=process.argv.slice(2),html=fs.readFileSync(file,'utf8'),out={};
const re=/<script>([\s\S]*?)<\/script>/g;let m;
while((m=re.exec(html))){const base=m.index+'<script>'.length;let ast;try{ast=acorn.parse(m[1],{ecmaVersion:'latest',sourceType:'script',allowReturnOutsideFunction:true});}catch(e){continue;}
  const walk=(body)=>{for(const n of body){
    if(n.type==='FunctionDeclaration'&&names.includes(n.id.name))out[n.id.name]=html.slice(base+n.start,base+n.end);
    if(n.type==='VariableDeclaration'&&n.declarations.length===1&&names.includes(n.declarations[0].id.name))out[n.declarations[0].id.name]=html.slice(base+n.start,base+n.end);
    if(n.type==='ExpressionStatement'&&n.expression.type==='CallExpression'){const c=n.expression.callee;const fb=c.body||(c.expression&&c.expression.body);if(fb&&fb.body)walk(fb.body);}
    if(n.type==='BlockStatement')walk(n.body);}};
  walk(ast.body);}
console.log(JSON.stringify(out));
