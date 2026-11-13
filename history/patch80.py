# 0.80: quieter counts (look-back and progress design doc, decisions 2 and 4; Hunter, November 13: "Let's go with the
#   recommendations").
#   - Ribbons are retired: no medal grid in the book, no "New ribbon" toasts. `state.ribbons` is still kept (silently), so
#     nothing anyone earned is lost, and the four backdrops still unlock from the same goals. A backdrop that unlocks says
#     so once ("A new backdrop for your Hearth: Glade."); a locked one says how it opens, in words, not "ribbon: …".
#   - Bond visits keep their daily limit, but the counter is gone: no "Visits left today: 2 of 3" on the Hearth or in
#     the games sheet, no "3 visits left today" on Today. When they are used up, the line says so plainly, as before.
import re,subprocess,os
S=open('base79.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.79.0'","const VERSION='prototype 0.80.0'")
rep("<title>Forgelings (prototype 0.79.0)</title>","<title>Forgelings (prototype 0.80.0)</title>")
# --- ribbons retired ---
rep("""+calendarHTML()+ribbonsHTML();""","""+calendarHTML();""")
rep("""const BACKDROPS=[{id:'glade',name:'Glade',ribbon:'week'},{id:'snow',name:'Snowfall',ribbon:'bond3'},{id:'cave',name:'Cinder Cave',ribbon:'tales'},{id:'gilded',name:'Gilded Night',ribbon:'legend'}];""",
"""const BACKDROPS=[{id:'glade',name:'Glade',ribbon:'week',lock:'Glade opens after 7 days of showing up',got:'A new backdrop for your Hearth: Glade.'},{id:'snow',name:'Snowfall',ribbon:'bond3',lock:'Snowfall opens when a Forgeling reaches bond 3',got:'A new backdrop for your Hearth: Snowfall.'},{id:'cave',name:'Cinder Cave',ribbon:'tales',lock:'Cinder Cave opens after 5 tales',got:'A new backdrop for your Hearth: Cinder Cave.'},{id:'gilded',name:'Gilded Night',ribbon:'legend',lock:'Gilded Night opens when you find a Legend',got:'A new backdrop for your Hearth: Gilded Night.'}];""")
rep("""const ok=!b.id||unl.includes(b.ribbon),rb=b.ribbon?RIBBONS.find(r=>r.id===b.ribbon).name:'';return `<button class="chip" data-bd="${b.id}" ${ok?'':'disabled style="opacity:.45"'} aria-pressed="${(state.hearth.bd||'')===b.id}">${b.name}${ok?'':' (ribbon: '+rb+')'}</button>`;""",
"""const ok=!b.id||unl.includes(b.ribbon);return `<button class="chip" data-bd="${b.id}" ${ok?'':'disabled style="opacity:.45"'} aria-pressed="${(state.hearth.bd||'')===b.id}">${ok?b.name:b.lock}</button>`;""",2)
rep("""if(add.length){state.ribbons=state.ribbons.concat(add);save();const r=RIBBONS.find(x=>x.id===add[0]);ribbonMsg=add.length>1?`New ribbon: ${r.name}, and ${add.length-1} more`:`New ribbon: ${r.name}`;""",
"""if(add.length){state.ribbons=state.ribbons.concat(add);save();const bd=BACKDROPS.find(x=>add.includes(x.ribbon));if(bd)ribbonMsg=bd.got;""")
# --- the visits counter goes; the limit stays ---
rep("""(hv>0?`${hv} ${hv===1?'visit':'visits'} left today.`:'Your companions are here for company.')""","""(hv>0?'':'Your companions are here for company.')""")
rep("""left?`Visits left today: ${left} of 3. Play any of the five games.`:""","""left?'Time together grows your bond. Play any of the five games.':""")
rep("""${left?`Visits left today: ${left} of 3. A round grows the bond of the Forgeling who plays.`:""","""${left?'A round grows the bond of the Forgeling who plays.':""")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk80.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk80.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
