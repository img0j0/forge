# 0.83: tidy up (Hunter, November 13: asked whether anything else needed fixing, then "Let's do it. Let's optimize").
#   - What's New is current again (SEEN_V 56). The notes were from about 0.50, so nobody updating heard about choosing
#     a card, the question, the book and its tab, the Scribe, letters and seasons, or the quieter Today.
#   - Code nothing reaches any more is removed: the old Journal summary (journeyHTML, bookHTML, calendarHTML), the
#     ribbon grid (ribbonsHTML), the echo block (echoHTML), the old-page sheet (openOldPage) and the monthly-books
#     sheet (zinesHTML and its #bookZines handler). Their Japanese goes with them.
#   - The book's This week tile shows the week in one row.
#   - The echo's On this day line waits until the day's card is done (as the echo did before 0.79).
import re,subprocess,os,json
S=open('base822.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
def drop_fns(names):
    """remove top-level declarations by name; their exact text comes from a real parse (tools/fnrange.mjs)"""
    global S
    open('/tmp/drop83.html','w').write(S)
    R=json.loads(subprocess.run(['node','tools/fnrange.mjs','/tmp/drop83.html',*names],capture_output=True,text=True).stdout)
    assert set(R)==set(names),(set(names)-set(R))
    for n,t in R.items():
        assert S.count(t)==1,n; S=S.replace(t+'\n',t,1).replace(t,'',1)
rep("const VERSION='prototype 0.82.2'","const VERSION='prototype 0.83.0'")
rep("<title>Forgelings (prototype 0.82.2)</title>","<title>Forgelings (prototype 0.83.0)</title>")
rep("const SEEN_V=55;","const SEEN_V=56;")
# --- What's New ---
m=re.search(r'<ul class="newlist">.*?\n    </ul>',S,re.S); assert m
S=S.replace(m.group(0),'''<ul class="newlist"><li><b>Your book.</b> The Book tab is your book: a chapter for every month, a page for every day, with the Forgeling you found taped in and your words in your own hand. It opens where your ribbon is. Close it from any page.</li><li><b>The Scribe writes the chapters.</b> Each month's first page tells the story of that month, and on Sunday evenings Close the day reads the week back to you.</li><li><b>Keepsakes on their day.</b> Postcards, curios, season stamps and letters are tucked into the page of the day they came, and sometimes your Forgeling writes in the margin.</li><li><b>Choose your card.</b> Each day, turn over three cards and choose the one you want. You can keep one for later.</li><li><b>One question a day.</b> After your card, your Forgeling asks one small question. Your answer is written into the day's page, and it leans where your Forgeling wanders next.</li><li><b>A quieter Today.</b> One look back a day, opening your book. Ribbons and counters are gone, and the Forge keeps its own count.</li>
    </ul>''')
# --- unused code ---
drop_fns(['journeyHTML','bookHTML','calendarHTML','ribbonsHTML','echoHTML','openOldPage','zinesHTML'])
rep("""  if(e.target.closest('#bookZines')){openSheet(zinesHTML());return;}\n""","")
for f in ['journeyHTML','bookHTML','calendarHTML','ribbonsHTML','echoHTML','openOldPage','zinesHTML']:
    assert not re.search(r'\b'+f+r'\b',S),f
# --- the echo line waits until the day's card is done, as the echo always did (qa_17) ---
rep("else if(!o&&state.otd!==todayKey()&&state.cards.length){const e=echoToday();","else if(!o&&state.otd!==todayKey()&&state.cards.length&&(state.status==='done'||state.status==='rest')){const e=echoToday();")
# --- This week tile in one row ---
rep(".bkb .bki .wkd{display:grid;grid-template-columns:repeat(4,7px);gap:2px}",".bkb .bki .wkd{display:grid;grid-template-columns:repeat(7,4px);gap:1px}")
rep(".bkb .bki .wkd i{width:7px;height:7px;border:1.2px solid #B9AE96;border-radius:1px}",".bkb .bki .wkd i{width:4px;height:12px;border:1px solid #B9AE96;border-radius:1px}")
out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk83.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk83.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out,len(S))
