# 0.47: the rest of the field journal, and the fixes from a review of every 0.46 screen and sheet by day and lamplight.
# Hearth: the scene is a taped-in photo, a request is a sealed letter, the pocket note is torn paper, the actions are
# hand-drawn boxes, the shelf/fire/keepsakes/who-sits are an index. Map: your lines and realm headers are written on the
# page. Sheets: options are ink boxes, chips paper tabs, fields paper. The Forge sorts Ready to make, Still to make,
# Made. A Forgeling close up is a journal page with its print taped in. Settings opens with the journal's bookplate.
# Fix: Today's tape no longer crosses the date line.
import re,subprocess
S=open('base46.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)

rep("const VERSION='prototype 0.46.0'","const VERSION='prototype 0.47.0'")
rep("<title>Forgelings (prototype 0.46.0)</title>","<title>Forgelings (prototype 0.47.0)</title>")
rep("const SEEN_V=51;","const SEEN_V=52;")

# the close-up is a page in the journal
rep("""  attachTilt($('#stage'));hydrate(modal);$('#ovClose').focus({preventScroll:true});""",
    """  {const sc=modal.querySelector('.scrim');if(sc)sc.classList.toggle('jinsp',lsOn());}
  attachTilt($('#stage'));hydrate(modal);$('#ovClose').focus({preventScroll:true});""")

# the Forge: what you can make first, then what is still to make, then what is made
rep("""  const rows=L.map(r=>{const ok=fgMade(r.id),can=fgCan(r),L=f.log[r.id];
    return `<li class=""",
"""  const rk=r=>fgMade(r.id)?2:fgCan(r)?0:1,LS=L.slice().sort((a,b)=>rk(a)-rk(b));let lastRk=-1;
  const rows=LS.map(r=>{const ok=fgMade(r.id),can=fgCan(r),L=f.log[r.id],hd=rk(r)!==lastRk?(lastRk=rk(r),`<li class="fgh">${['Ready to make','Still to make','Made'][lastRk]}</li>`):'';
    return hd+`<li class=""")

# Settings: the bookplate inside the cover
rep("""$('#view-settings').innerHTML=`
""","""$('#view-settings').innerHTML=`<div class="jplate"><span class="k">This journal was started</span><b>${esc(dateLabel(state.startDate))}</b><span>${dayN()} ${dayN()===1?'day':'days'} kept · ${state.cards.length} ${state.cards.length===1?'Forgeling':'Forgelings'}</span></div>
""")

CSS=open('/home/claude/forge/journal47.css').read()
i=S.index("</style>",S.index("</style>")+1)
S=S[:i]+"\n"+CSS+"\n"+S[i:]

rep("""<ul class="newlist"><li><b>A field journal.</b>""","""<ul class="newlist"><li><b>The whole journal.</b> The Hearth is a taped-in photo with letters and notes beside it, the Forge lists what you can make first, a Forgeling opens on its own page, and Settings begins inside the cover. Every sheet is written on the same paper.</li><li><b>A field journal.</b>""")
m=re.search(r'<ul class="newlist">(.*?)</ul>',S,re.S); items=re.findall(r'<li>.*?</li>',m.group(1),re.S)
assert len(items)==9,len(items); rep(items[-1],"")

open('work.html','w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk47.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk47.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600])
