# 0.57.2: Japanese on Hunter's iPhone (November 12, screenshot of Today).
#   - Dates followed the phone's language, so a phone in English running the app in Japanese showed "Thu, Nov 12".
#     Every date now follows the app's language (LOC()); a card's saved date label reads in the app's language too.
#   - The companion's line ("Mordread nodded once...") was saved as English text when it was written. It is now
#     written from its template each time it is shown, in the app's language and with the name as it reads now.
#   - The How did it feel? labels (かんたん, いい感じ) ran into the circles: smaller in Japanese (i18n/build.mjs CSS).
import re,subprocess,os
S=open('base571.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.57.1'","const VERSION='prototype 0.57.2'")
rep("<title>Forgelings (prototype 0.57.1)</title>","<title>Forgelings (prototype 0.57.2)</title>")

# dates in the app's language
n=S.count("toLocaleDateString(undefined,"); assert n==4,n
S=S.replace("toLocaleDateString(undefined,","toLocaleDateString(LOC(),")
rep("toLocaleDateString()","toLocaleDateString(LOC())")
rep("const dateLabel=k=>","""/* 0.57.2: dates follow the app's language, not only the phone's */
function LOC(){return typeof LANG!=='undefined'&&LANG==='ja'?'ja-JP':undefined;}
const dateLabel=k=>""")
# a card's saved label reads in the app's language (the save keeps it as written)
rep("""  Object.defineProperty(c,'toJSON',{value:function(){const o=Object.assign({},this);o.name=v;return o;},enumerable:false,configurable:true});""",
"""  let dl=c.dateLabel;
  if(typeof c.date==='string'&&/^\\d{4}-\\d{2}-\\d{2}$/.test(c.date))Object.defineProperty(c,'dateLabel',{get:()=>dateLabel(c.date),set:x=>{dl=x;},enumerable:true,configurable:true});
  Object.defineProperty(c,'toJSON',{value:function(){const o=Object.assign({},this);o.name=v;o.dateLabel=dl;return o;},enumerable:false,configurable:true});""")

# the companion's line, written when shown
rep("""  const ow=todayOwnObj(),line=(ow?(ow.days.length<=1?'{n} saw you do \\u201C{o}\\u201D today, and thinks that is nice.':OWN_L[whash(dnum(state.date)*7+c.id)%OWN_L.length]).replace(/\\{o\\}/g,ow.text):L[whash(dnum(state.date)*31+c.id)%L.length]).replace(/\\{n\\}/g,n),after=bondLevel(c);
  state.comp={date:state.date,cid:c.id,line,up:after>before?after:0};""",
"""  const ow=todayOwnObj(),f=!!ow&&ow.days.length<=1,line=compLine(c,f),after=bondLevel(c);
  state.comp={date:state.date,cid:c.id,line,up:after>before?after:0,f};""")
rep("""function compHTML(){
  const p=state.comp;if(!p||p.date!==state.date)return '';const c=cardById(p.cid);if(!c)return '';const n=c.nick||c.name;
  return `<p class="comp"><b>${esc(p.line)}</b>""","""/* 0.57.2: the line is written from its template whenever it is shown (language and name as they are now) */
function compLine(c,first){
  const ow=todayOwnObj(),L=COMP_L[c.dark?1:0],n=c.nick||c.name;
  return (ow?(first?'{n} saw you do \\u201C{o}\\u201D today, and thinks that is nice.':OWN_L[whash(dnum(state.date)*7+c.id)%OWN_L.length]).replace(/\\{o\\}/g,ow.text):L[whash(dnum(state.date)*31+c.id)%L.length]).replace(/\\{n\\}/g,n);
}
function compHTML(){
  const p=state.comp;if(!p||p.date!==state.date)return '';const c=cardById(p.cid);if(!c)return '';const n=c.nick||c.name;
  const ow=todayOwnObj(),line=compLine(c,p.f!==undefined?!!p.f:!!ow&&ow.days.length<=1);
  return `<p class="comp"><b>${esc(line)}</b>""")

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk572.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk572.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
