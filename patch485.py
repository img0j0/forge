# 0.48.5: review fixes (Hunter asked for a pass for enhancements and bugs, November 5).
# The phone's date moving back a day or two (flying west after midnight, a clock changed by hand) no longer rolls the
# journal back: the day you finished stays finished, the card cannot be earned twice, and no day is logged twice.
# A larger jump back still follows the phone, so a clock set to the wrong year by mistake does not freeze the journal.
# todayKey() itself holds, so Hearth visits and every other per-day count follow the journal's day too.
import re,subprocess
S=open('base484.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.48.4'","const VERSION='prototype 0.48.5'")
rep("<title>Forgelings (prototype 0.48.4)</title>","<title>Forgelings (prototype 0.48.5)</title>")
rep("const todayKey=()=>dkey(nowDate());",
    "const todayKey=()=>{const k=dkey(nowDate());return state&&state.date&&k<state.date&&dayDiff(k,state.date)<=2?state.date:k;}; /* 0.48.5: a day or two back (travel, a clock change) holds the journal's day */")
open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk485.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk485.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
