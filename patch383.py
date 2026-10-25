# Forgelings 0.38.3: Settings folds. Fourteen open blocks become seven folding sections, ordered by use, each
# showing its current choice on the folded row. Your cards starts open while you have not set anything. Erase moves
# to the very bottom. Every control keeps its id and data attribute. Reads base382.html.
src = open('base382.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---- the new Settings body: everything from the first block up to the feedback blocks
a = src.index('  $(\'#view-settings\').innerHTML=`\n    <div class="setblock"><b>Forgeling mood</b>')
b = src.index('    <details class="dev"><summary>Prototype tools</summary>')
old = src[a:b]
assert old.count('setblock') == 10, old.count('setblock')

def grab(start, end):
    i = old.index(start); j = old.index(end, i) + len(end); return old[i:j]
mood_chips = grab('<div class="chips" role="group" aria-label="Forgeling mood">', "</button>`).join('')}</div>")
sound_body = grab('<div class="chips"><button class="chip" id="setSound"', "Soft music needs the standard method.</p>':''}")
comfort_chips = grab('<div class="chips"><button class="chip" id="setReduce"', 'Whispers and tales ${S.lore!==false?\'on\':\'off\'}</button></div>')
look_rest = grab('<div class="lbl2">Appearance</div>', "</button>`).join('')}</div></div>")[:-len('</div>')]
cards_body = old[old.index('<p class="muted small">What do you want more of?'):old.index('    ${remindHTML()}')].rstrip()
assert cards_body.endswith('</div>`:\'\'}</div>'), cards_body[-60:]
cards_body = cards_body[:-len('</div>')]
nums = grab('<div class="numgrid">', '<span>packs opened</span></div></div>')
odds = '<button class="pill" id="btnOdds">See the odds</button>'
priv_p = grab('<p class="muted small">Everything you do in Forgelings stays on this device.', 'only that you are an adult.</p>')
priv_btns = '<div class="chips"><button class="pill" id="btnPrivacy">How Forgelings handles your data</button><button class="pill" id="btnTerms">Terms of use</button></div>'
age = grab('<p class="small">Age setting:', "'Not set'}</b></p>")
backup = '<div class="chips"><button class="pill" id="btnExport">Save a copy</button><button class="pill" id="btnRestore">Restore a copy</button></div>'
report_btn = grab('<button class="pill" id="btnReport">', 'Copy my report\'}</button>')
for s in (odds, priv_btns, backup):
    assert s in old, s

new = ("  if(!setOpen)setOpen=new Set(state.want.length||state.owns.length?[]:['cards']);\n"
"  const ML={cute:'Cute only',mix:'A mix',dark:'Dark only'},SK={auto:'Follows your day',day:'Always day',night:'Always night',plain:'Plain'},TH={light:'Light',dark:'Dark'};\n"
"  $('#view-settings').innerHTML=`\n"
"    ${setSec('cards','Your cards',(state.want.length?state.want.map(i=>WANTS[i].n).join(', '):'Nothing picked yet')+(state.owns.length?' \\u00B7 '+state.owns.length+' of your own':''),`" + cards_body + "`,'yourCards')}\n"
"    ${setSec('sound','Sound',S.sound===false?'Off':['On',S.music!==false?'soft music':'no music',(S.vol||'normal')+' volume'].join(' \\u00B7 '),`<p class=\"muted small\">Soft pixel-style sounds, all made on your device.</p>\n      " + sound_body + "`)}\n"
"    ${setSec('look','Look and feel',[ML[S.mood]||'A mix',SK[S.sky||'auto'],TH[S.theme],S.reduce?'less motion':''].filter(Boolean).join(' \\u00B7 '),`<div class=\"lbl2\">Forgeling mood</div><p class=\"muted small\">Which Forgelings you find from now on. The ones you already have stay.</p>" + mood_chips + "<div class=\"lbl2\">Comfort</div>" + comfort_chips + look_rest + "`)}\n"
"    ${remindHTML()}\n"
"    ${setSec('coll','Your collection',state.cards.length+' Forgeling'+(state.cards.length===1?'':'s')+' \\u00B7 save or restore a copy',`" + nums + "<div class=\"lbl2\">Backup</div><p class=\"muted small\">Your collection lives on this device. Save a copy so you can move it or restore it.</p>" + backup + "`)}\n"
"    ${setSec('about','About',`Fair odds, privacy and terms`,`<div class=\"lbl2\">Fair odds</div><p class=\"muted small\">Packs are earned, never sold. Check the odds yourself.</p>" + odds + "<div class=\"lbl2\">Privacy</div>" + priv_p + priv_btns + age + "`)}\n"
"    ${STORE?'':setSec('feedback','Feedback','A few quick questions, and your report',`<p class=\"muted small\">Answer as many as you like, whenever you like.</p>${feedbackHTML()}<div class=\"lbl2\">My report</div><p class=\"muted small\">A short summary, plus anything you wrote above, that you can send to whoever is gathering feedback.</p>" + report_btn + "`)}\n"
"    ${installTipHTML()}\n"
"    <div class=\"erase\"><button class=\"pill\" id=\"btnErase\">Erase everything on this device</button></div>\n"
"    ${STORE?'':`")
src = src[:a] + new + src[b:]
# the dev tools were inside the feedback template literal before; keep the same closing
rep("""      <button class="tool" data-tool="reset"><b>Start over</b><span>Erases this prototype's progress.</span></button></div></details>`}""",
    """      <button class="tool" data-tool="reset"><b>Start over</b><span>Erases this prototype's progress.</span></button></div></details>`}""")

# ---- the section helper and the remembered open state
rep('function renderSettings(){',
    "let setOpen=null;\n"
    "function setSec(id,title,sum,body,el){const o=setOpen&&setOpen.has(id);return `<details class=\"setblock setsec\" data-sec=\"${id}\"${el?` id=\"${el}\"`:''}${o?' open':''}><summary><span class=\"sst\"><b>${title}</b><small class=\"ssum\">${sum}</small></span></summary><div class=\"setin\">${body}</div></details>`;}\n"
    'function renderSettings(){')
rep("$('#view-settings').addEventListener('click',e=>{",
    "$('#view-settings').addEventListener('toggle',e=>{const d=e.target;if(!d.matches||!d.matches('details.setsec'))return;if(!setOpen)setOpen=new Set();if(d.open)setOpen.add(d.dataset.sec);else setOpen.delete(d.dataset.sec);},true);\n"
    "$('#view-settings').addEventListener('click',e=>{")
# the feedback prompt opens its section
rep("else if(b.id==='fbGo'){closeModal();tab='settings';render();",
    "else if(b.id==='fbGo'){closeModal();tab='settings';if(!setOpen)setOpen=new Set();setOpen.add('feedback');render();")

# ---- reminders (iPhone app) become a section
rep("""  return `<div class="setblock"><b>Reminders</b><p class="muted small">""",
    """  return setSec('remind','Reminders',S.nudge?'Each day at '+S.nudge:'Off',`<p class="muted small">""")
rep("""Haptics ${S.haptics!==false?'on':'off'}</button></div></div>`;""",
    """Haptics ${S.haptics!==false?'on':'off'}</button></div>`);""")

# ---- styles
rep('.setblock .muted{margin:2px 0 8px}',
    '.setblock .muted{margin:2px 0 8px}\n'
    '.setsec{padding:0 16px}.setsec>summary{min-height:60px;display:flex;align-items:center;gap:12px;cursor:pointer;list-style:none;padding:10px 0}\n'
    '.setsec>summary::-webkit-details-marker{display:none}\n'
    ".setsec>summary::after{content:'+';margin-left:auto;flex:none;width:24px;text-align:center;font:400 30px/1 'VT323',monospace;color:var(--plum)}\n"
    ".setsec[open]>summary::after{content:'\\2013'}\n"
    '.setsec>summary:focus-visible{outline:none;box-shadow:inset 0 0 0 3px var(--plum)}\n'
    '.sst{display:flex;flex-direction:column;min-width:0;gap:2px}.ssum{color:var(--muted);font-size:13px;line-height:1.35}\n'
    '.setsec[open]>summary{border-bottom:1px solid var(--line);margin-bottom:6px}.setin{padding-bottom:14px}.setin>.lbl2:first-child{margin-top:6px}\n'
    '.erase{text-align:center;margin:18px 0 4px}')
rep('html.ls .setblock{padding:20px 20px 18px !important}',
    'html.ls .setblock{padding:20px 20px 18px !important}html.ls .setsec{padding:8px 20px !important}')

rep('<title>Forgelings (prototype 0.38.2)</title>', '<title>Forgelings (prototype 0.38.3)</title>')
rep("const VERSION='prototype 0.38.2'", "const VERSION='prototype 0.38.3'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
