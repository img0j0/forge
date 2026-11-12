# 0.54.0: creature variety (Hunter, November 12: "Ok let's continue" after the quality review named "the Forgelings
#   look too alike" as the biggest gap). New finds are the second generation (card field gen:2). They draw from new
#   bodies (pear, drop, loaf, blob, noodle, mushroom; Shade: imp, slink, tower), poses (arms up, waving, hugging,
#   tucked; Shade: raised claws, none), faces (happy, sparkle, bean, wink, line; fang, o, wavy, flat, tongue;
#   Shade: many eyes, void, stitch, tusks) and small touches (two-tone ears and tail, nose, mask, cheek fluff,
#   socks, patch, veins), plus a little jitter in where the eyes sit. Everything found before keeps its look: the
#   first generation is drawn by the same code with the same random stream (creatures/same.py compares 1,200
#   sprites). Gift and statue links carry w:2 so a friend sees the same Forgeling. Art source: creatures/.
import re,subprocess,os
S=open('base53.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
H='creatures/'
rep("const VERSION='prototype 0.53.0'","const VERSION='prototype 0.54.0'")
rep("<title>Forgelings (prototype 0.53.0)</title>","<title>Forgelings (prototype 0.54.0)</title>")
def swap(name,new):
    global S
    i=S.find('function '+name+'('); j=S.find('\n}',i)+2; assert i>0 and S.count('function '+name+'(')==1; S=S[:i]+new.rstrip('\n')+S[j:]
swap('genSpec',open(H+'genSpec.js').read())
swap('buildSprite',open(H+'cute2.js').read()+'\n'+open(H+'buildSprite.js').read())

# new finds are the second generation; the cache key, the save check and the links know it
rep("bond:0,keep:'',fire:[],allIn:!!o.allIn,source:o.source||'daily',own:o.own||''};","bond:0,keep:'',fire:[],allIn:!!o.allIn,source:o.source||'daily',own:o.own||'',gen:2};")
rep("const ckey=c=>c.seed+'-'+","const ckey=c=>(c.gen===2?'g2-':'')+c.seed+'-'+")
rep("c.rarity=int(c.rarity,0,4,0);c.dark=!!c.dark;","c.rarity=int(c.rarity,0,4,0);c.dark=!!c.dark;if(c.gen!==2)delete c.gen;")
rep("e:c.seed>>>0,k:c.v};if(fr)g.f=fr.id;","e:c.seed>>>0,k:c.v};if(c.gen===2)g.w=2;if(fr)g.f=fr.id;")
rep("k:o.k,m:(o.m||'').trim()};if(o.f!==undefined)","k:o.k,m:(o.m||'').trim()};if(o.w===2)out.w=2;if(o.f!==undefined)")
rep("const giftSender=g=>({id:-1,seed:g.e,rarity:g.r,dark:!!g.d,theme:g.t,v:g.k,keep:'',bond:0,name:g.n,nick:''});",
    "const giftSender=g=>({id:-1,seed:g.e,rarity:g.r,dark:!!g.d,theme:g.t,v:g.k,keep:'',bond:0,name:g.n,nick:'',...(g.w===2?{gen:2}:{})});")
rep("return {v:1,e:o.e,t:o.t,d:o.d,r:o.r,k:o.k,n:o.n.trim(),a:o.a,p};","return {v:1,e:o.e,t:o.t,d:o.d,r:o.r,k:o.k,n:o.n.trim(),a:o.a,p,...(o.w===2?{w:2}:{})};")
rep("name:s.n,nick:'',statue:{at:s.a,keep:s.p}});","name:s.n,nick:'',statue:{at:s.a,keep:s.p},...(s.w===2?{gen:2}:{})});")
rep("n,a:c.statue.at,p:c.statue.keep||''};","n,a:c.statue.at,p:c.statue.keep||'',...(c.gen===2?{w:2}:{})};")

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk54.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk54.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
