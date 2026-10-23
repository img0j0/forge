# Forgelings 0.35.4: the margin moves off Today (Hunter: "In the margin" felt out of place on the home page).
# Today is now the card, the find and your favourite. Once the day's card is done (or on a rest day), one quiet link
# under the find, "Add a line to your journal" ("Edit today's line" once written), opens the same Forge prompt in a
# small sheet. Lines still go to the Journal and still feed margin echoes at the Hearth. Reads base353.html.
src = open('base353.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
i = src.index("  const jr=state.journal[state.date],reflect=s!=='fresh'?"); j = src.index("\n", i)
src = src[:i] + "  const jr=state.journal[state.date];if(s==='done'||s==='rest')hero+=`<button class=\"ghost marginlink\" id=\"btnMargin\">${jr?'Edit today’s line':'Add a line to your journal'}</button>`;const reflect='';" + src[j:]
rep("function saveJournal(text){", r'''function openMargin(){
  const V=VECTORS[state.todayV],jr=state.journal[state.date];
  openSheet(`<h2>In the margin</h2><p class="muted"><i>The Forge asks:</i> ${esc(V.question)}</p>
    <label class="field" style="margin-top:10px"><span>Write one line. It stays on this device, in your Journal.</span><input id="jIn" maxlength="200" value="${esc(jr?jr.text:'')}" placeholder="Whatever comes to mind" autocomplete="off"></label>
    <div class="stack"><button class="primary" id="jSave">Save</button></div>
    <div class="row" style="justify-content:center"><button class="ghost" data-close>Not now</button></div>`);
  setTimeout(()=>{const i=$('#jIn');if(i)i.focus({preventScroll:true});},60);
}
function saveJournal(text){''')
# the sheet's Save lives in the modal's own click handler
rep("  else if(b.id==='giftKeep')giftKeep();", "  else if(b.id==='giftKeep')giftKeep();\n  else if(b.id==='jSave'){saveJournal(($('#jIn')||{}).value||'');closeModal();renderToday();renderChronicle();checkRibbons();toast('Saved to your Journal. It stays on this device.');}")
rep("  else if(b.id==='btnShowToday')inspect(state.todayCard);", "  else if(b.id==='btnShowToday')inspect(state.todayCard);\n  else if(b.id==='btnMargin')openMargin();")
rep('/* Nav */', '.hero .marginlink{margin-top:2px}\n/* Nav */')
rep('<title>Forgelings (prototype 0.35.3)</title>', '<title>Forgelings (prototype 0.35.4)</title>')
rep("const VERSION='prototype 0.35.3'", "const VERSION='prototype 0.35.4'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
