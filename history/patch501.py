# 0.50.1: fixes from Hunter's first play-through of 0.50 (November 8).
#   Lantern Lights: the sky lanterns for each finished round appeared at random spots. Each one now lifts off the
#     lantern that finished the round, in its colour, and settles in the sky along the top, filling in from both edges (clear of the Watch / Your turn line), one per round.
#   Keep the Fire and Dandelion Drift: the Forgeling sat in front of the fire and of rising seeds and embers. The fire,
#     seeds and embers now draw in front of the Forgeling, and in Keep the Fire it sits clear of the fire on narrow phones.
import re,subprocess,os
S=open('base50.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.50.0'","const VERSION='prototype 0.50.1'")
rep("<title>Forgelings (prototype 0.50.0)</title>","<title>Forgelings (prototype 0.50.1)</title>")

# ---------- sky lanterns: lift off the lantern that finished the round, settle in a row ----------
rep("""const skyL=()=>{if(sky>=12)return;sky++;const e=document.createElement('i');e.className='skyl';e.setAttribute('aria-hidden','true');e.style.left=(8+Math.random()*80)+'%';e.style.setProperty('--up',-Math.round(area.clientHeight*(.18+Math.random()*.3))+'px');area.appendChild(e);};""",
"""const skyL=i=>{if(sky>=12)return;const k=sky++,W=area.clientWidth,j=k>>1,x=Math.round((k&1?W*(1-(j+.5)*.055):W*(j+.5)*.055)-5),y=8,p=gPos(L[i]),e=document.createElement('i');e.className='skyl';e.setAttribute('aria-hidden','true');
    e.style.left=x+'px';e.style.top=y+'px';e.style.setProperty('--lc',cols[i]);e.style.setProperty('--fx',Math.round(p[0]-5-x)+'px');e.style.setProperty('--fy',Math.round(p[1]-6-y)+'px');area.appendChild(e);};""")
rep("gFloat(p[0],p[1],seq.length+'!');skyL();","gFloat(p[0],p[1],seq.length+'!');skyL(i);")
rep(".skyl{position:absolute;bottom:42%;width:10px;height:13px;background:#FFB04A;clip-path:polygon(20% 0,80% 0,100% 30%,90% 100%,10% 100%,0 30%);pointer-events:none;z-index:0;animation:skyl 3s ease-out forwards}",
    ".skyl{position:absolute;width:10px;height:13px;background:var(--lc,#FFB04A);box-shadow:0 0 8px 2px var(--lc,#FFB04A);clip-path:polygon(20% 0,80% 0,100% 30%,90% 100%,10% 100%,0 30%);pointer-events:none;z-index:0;opacity:.9;animation:skyl 1.6s cubic-bezier(.3,.7,.4,1) both}")
rep("@keyframes skyl{from{transform:translateY(0);opacity:.2}to{transform:translateY(var(--up));opacity:.9}}",
    "@keyframes skyl{from{transform:translate(var(--fx),var(--fy)) scale(2.2);opacity:.3}to{transform:none;opacity:.9}}")
rep(".skyl{animation:none;transform:translateY(var(--up));opacity:.9}",".skyl{animation:none}",2)

# ---------- the Forgeling sits behind the fire, the seeds and the embers ----------
rep(".seed.puff{width:64px;height:64px;z-index:2}",".seed.puff{width:64px;height:64px;z-index:4}")
rep(".seed.gold{z-index:1}",".seed.gold{z-index:3}")
CSS="""
/* 0.50.1: play pieces draw in front of the Forgeling; by the fire it sits clear of the flames */
.pg .seed,.pg .emb{z-index:2}
.pg .seed.gold{z-index:3}
.pg .seed.puff{z-index:4}
.pg-ember .fire{z-index:2}
.pg-ember .pgmate{left:max(2px,calc(50% - 138px))}
"""
i=S.index("</style>",S.index("</style>")+1); S=S[:i]+CSS+S[i:]
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk501.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk501.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
