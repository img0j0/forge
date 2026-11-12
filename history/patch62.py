# 0.62: the native widget and the wandering countdown (Hunter, November 12: "Please prioritize and execute the
#   additions"; the fifth). In the iPhone and Android apps the web app now tells the home-screen widget who to show
#   (the Forgeling at the fire, or the one out wandering), what to say (today's card waiting or done, resting, out
#   wandering, back) and, while a Forgeling wanders, when it is back. It also starts the wandering countdown: a Live
#   Activity on the iPhone's Lock Screen and Dynamic Island, an ongoing countdown notification on Android. The words
#   are sent already translated. The website is unchanged: it has no widget.
import re,subprocess,os
S=open('base611.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.61.1'","const VERSION='prototype 0.62.0'")
rep("<title>Forgelings (prototype 0.61.1)</title>","<title>Forgelings (prototype 0.62.0)</title>")

rep("/* ================= 0.60: your year in Forgelings ================= */","""/* ================= 0.62: the native widget and the wandering countdown ================= */
const wplug=()=>NATIVE&&PL.Widget?PL.Widget:null;
let wLast='',wAct=0;
function widgetSync(){
  const W=wplug();if(!W||!state||!state.cards.length)return;
  try{
    const w=state.wander,wc=w?cardById(w.id):null,out=!!(w&&wc&&Date.now()<w.ready);
    const c=out?wc:(mateNow()||homeFav()||state.cards[state.cards.length-1]);if(!c)return;
    const n=c.nick||c.name,wn=wc?(wc.nick||wc.name):'';
    const line=state.status==='done'?`${n} is by the fire. Today's card is done.`:state.status==='rest'?`Resting today. ${n} is keeping the fire warm.`:`Today's card is waiting, and so is ${n}.`;
    const snap={name:n,line,fresh:`Today's card is waiting, and so is ${n}.`,wline:wc?`${wn} is out wandering`:'',back:wc?`${wn} is back from wandering`:'',day:todayKey(),until:w&&wc?w.ready:0};
    const key=JSON.stringify(snap)+'|'+ckey(c);
    if(key!==wLast){wLast=key;const u=spriteURL(c);if(u)snap.png=u.split(',')[1];W.update(snap).catch(()=>{});}
    if(out&&wAct!==w.start){wAct=w.start;W.wanderStart({name:wn,until:w.ready,title:`${wn} is out wandering`,back:`${wn} is back from wandering`,channel:'Wandering'}).catch(()=>{});}
    else if(!out&&wAct!==-1){wAct=-1;W.wanderEnd({back:wc?`${wn} is back from wandering`:''}).catch(()=>{});}
  }catch(e){}
}
document.addEventListener('visibilitychange',()=>{if(document.hidden)widgetSync();});
/* ================= 0.60: your year in Forgelings ================= */""")
# kept in step with Today (renderToday runs after every change that matters), and when the app goes to the background
m=re.search(r"\nfunction renderToday\(\)\{\n",S);assert m
S=S[:m.end()]+"  setTimeout(widgetSync,0);\n"+S[m.end():]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk62.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk62.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
