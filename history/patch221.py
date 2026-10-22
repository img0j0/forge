# Forge 0.22.1: ready to install. Reads base22.html, writes work.html.
# The same file runs everywhere; a hosted "release" copy (made by pwa.py) adds a marker that switches on
# the offline helper, hides the prototype tools and shows how to add Forge to the home screen.
src = open('base22.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# The fonts are built into the file now, so nothing is loaded from anywhere.
rep("This prototype has no accounts and sends nothing to a server, apart from loading fonts from Google Fonts.",
    "Forge has no accounts and sends nothing anywhere: no server, no tracking, no ads.")

rep('/* Nav */', '''html.release details.dev{display:none}
.installtip{background:var(--chip);border-radius:14px;padding:10px 12px;margin-top:8px}
/* Nav */''')

REL_JS = r'''
/* ---- The installed app. A hosted copy carries <meta name="forge-build" content="release">. ---- */
const RELEASE=!!document.querySelector('meta[name="forge-build"][content="release"]');
const STANDALONE=()=>!!((window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone);
if(RELEASE){document.documentElement.classList.add('release');
  if('serviceWorker' in navigator&&/^https?:$/.test(location.protocol))window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{});});
  try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist().catch(()=>{});}catch(e){}}
function installTipHTML(){
  if(!RELEASE||STANDALONE())return '';
  const ios=/iPhone|iPad|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  return `<div class="setblock"><b>Put Forge on your home screen</b><p class="muted small">It opens like an app, full screen, and works offline.</p><p class="installtip small">${ios?'In Safari, tap the Share button, then <b>Add to Home Screen</b>.':'In Chrome, open the menu and tap <b>Install app</b> or <b>Add to Home screen</b>.'}</p></div>`;
}
function shareOrCopy(txt,done,title){
  if(navigator.share&&(RELEASE||STANDALONE())){navigator.share({title,text:txt}).catch(err=>{if(!err||err.name!=='AbortError')copyText(txt,done);});return;}
  copyText(txt,done);
}
'''
rep('/* ================= Start ================= */', REL_JS + '\n/* ================= Start ================= */')
rep("""    <div class="setblock"><b>Fair odds</b>""", """    ${installTipHTML()}
    <div class="setblock"><b>Fair odds</b>""")
rep("  else if(b.id==='btnReport')copyText(pilotReport(),'Report copied.');",
    "  else if(b.id==='btnReport')shareOrCopy(pilotReport(),'Report copied.','My Forge report');")
rep("""<button class="pill" id="btnReport">Copy my report</button>""",
    """<button class="pill" id="btnReport">${navigator.share&&(RELEASE||STANDALONE())?'Send my report':'Copy my report'}</button>""")

rep('<title>Forge (prototype 0.22.0)</title>', '<title>Forge (prototype 0.22.1)</title>')
rep("const VERSION='prototype 0.22.0';", "const VERSION='prototype 0.22.1';")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
