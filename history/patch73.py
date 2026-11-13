# 0.73.0: a calmer first week (Hunter, November 12, the launch-readiness plan: "a new player's first week").
#   From playing days 1 to 7 as a new person:
#   - "This week" spread its days across the whole width, so on day 2 Tuesday sat at the far right, where Sunday
#     goes. The days now sit in seven fixed columns, in order.
#   - Day 1 after the first card was crowded (the question, the postcard offer, your own words, "Make your cards
#     yours", the season, the next pack, the Hearth, a ribbon and the first-day sheet). The postcard offer now
#     starts on your third page (or whenever a postcard already exists), and "Make your cards yours" on day 2.
#   - Once a season's stamp is pressed, its row shows that day only, not every day until the season ends.
#   And from the full test run: the build works from any folder (pwa.py), the card backs are packed smaller, and the
#   Scribe's arrival is no longer hidden by the 60-page letter.
import re,subprocess,os,sys
sys.path.insert(0,'art');import cardback72
S=open('base721.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.72.1'","const VERSION='prototype 0.73.0'")
rep("<title>Forgelings (prototype 0.72.1)</title>","<title>Forgelings (prototype 0.73.0)</title>")
rep("if(s==='done')hero+=askHTML()+pcHTML();","if(s==='done')hero+=askHTML()+((state.posts||{})[state.date]||entryDays().size>=3?pcHTML():'');")
rep("  if(!state.wantAsked&&state.cards.length&&state.status!=='fresh')rows.unshift(","  if(!state.wantAsked&&state.cards.length&&state.status!=='fresh'&&entryDays().size>=2)rows.unshift(")
rep("  {const n=seasonNow();if(n&&state.cards.length){const got=state.seasons&&state.seasons[seasonKey(n)];\n    rows.unshift(",
    "  {const n=seasonNow();if(n&&state.cards.length){const got=state.seasons&&state.seasons[seasonKey(n)];\n    if(!got||got===state.date)rows.unshift(")
# from the full test run (qa_38): at 60 pages the Scribe arrives and the 60-page letter is written at the same moment;
#   the letter's notice by the fire replaced the Scribe's arrival. A letter no longer replaces a notice already there
#   (it still waits on Today).
rep("hf.msg=`${m.nick||m.name} has left you a letter by the fire.`;save();}","if(!hf.msg)hf.msg=`${m.nick||m.name} has left you a letter by the fire.`;save();}")
# the card backs, packed half as small (qa_301: no pixel art over 9,000 characters)
for k in 'TP':
    m=re.search(r'--cb'+k+r':url\("data:image/svg\+xml,(.*?)"\)',S);assert m
    S=S[:m.start(1)]+cardback72.packed(cardback72.BACKS[k])+S[m.end(1):]
css="""
/* 0.73: this week's days in seven fixed columns */
.weekbox .dots{display:grid;grid-template-columns:repeat(7,34px);justify-content:space-between;gap:4px}
/* qa_fit: a long unbroken word in a tale wraps under the card instead of spilling off the side */
.inspback,.inspback *{overflow-wrap:anywhere}
"""
i=S.rindex("</style>",0,S.index("<body")); S=S[:i]+css+S[i:]
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk73.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk73.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
