# Forge 0.22.2: adults only during testing, a plain-English privacy note and terms in Settings,
# and a visible way to erase everything. Reads base221.html, writes work.html.
src = open('base221.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# ---------- 18 and up while Forge is being tested ----------
rep("const KEY='forge-app-v1',BLOCK='forge-age-block';", "const KEY='forge-app-v1',BLOCK='forge-age-block',MIN_AGE=18;")
rep("  if(a<13){try{localStorage.setItem(BLOCK,String(Date.now()));", "  if(a<MIN_AGE){try{localStorage.setItem(BLOCK,String(Date.now()));")
rep("""  openOverlay(`<p class="rv-title">Forge is not available for you just yet</p><p class="rv-hint">Thanks for being honest with us. We did not save any details about you. Come back when you are older.</p>`,false);""",
    """  openOverlay(`<p class="rv-title">Forge is not available for you just yet</p><p class="rv-hint">While Forge is being tested, it is for adults only. Thanks for being honest with us. We did not save any details about you.</p>`,false);""")

# ---------- Privacy and terms, in plain words ----------
rep("""    <div class="setblock"><b>Privacy</b><p class="muted small">Everything you do in Forge stays on this device. Forge has no accounts and sends nothing anywhere: no server, no tracking, no ads. Your birth date is not stored, only whether you are a teen or an adult.</p>""",
    """    <div class="setblock"><b>Privacy</b><p class="muted small">Everything you do in Forge stays on this device. Forge has no accounts and sends nothing anywhere: no server, no tracking, no ads. Your birth date is not stored, only that you are an adult.</p>
      <div class="chips"><button class="pill" id="btnPrivacy">How Forge handles your data</button><button class="pill" id="btnTerms">Terms of use</button></div>
      <button class="pill" id="btnErase" style="margin-top:8px">Erase everything on this device</button>""")
DOCS_JS = r'''
/* ---- Privacy note and terms of use: plain English, kept short, matching exactly what Forge does. ---- */
const DOCS_DATE='October 16, 2026';
function privacyHTML(){
  return `<h2>How Forge handles your data</h2><p class="muted small">Last updated ${DOCS_DATE}</p>
  <div class="tale"><b>What Forge keeps</b><p>Your Forgelings, the days you showed up or rested, anything you write (names, tales, margin notes and feedback answers), your settings, and the fact that you are an adult. Your birth date is never kept.</p></div>
  <div class="tale"><b>Where it is kept</b><p>Only on this device, in this browser. Forge has no accounts and no server of its own, so nobody else can see it, including the people who make Forge.</p></div>
  <div class="tale"><b>What Forge never does</b><p>No tracking, no analytics, no ads, no selling or sharing of anything. Nothing about you leaves this device unless you choose to send it.</p></div>
  <div class="tale"><b>When you choose to share</b><p>"Save a copy" and "Send my report" create text that goes only where you put it, for example a message to the person testing Forge with you.</p></div>
  <div class="tale"><b>Where Forge is hosted</b><p>The app is delivered by GitHub Pages. Like any website, GitHub receives basic technical details such as your IP address when it delivers the app, under GitHub's own privacy statement. Forge itself never receives them.</p></div>
  <div class="tale"><b>Deleting everything</b><p>Use "Erase everything on this device" in Settings, or remove Forge and clear this site's data in your browser. There is no other copy anywhere.</p></div>
  <div class="tale"><b>Age</b><p>While Forge is being tested, it is for adults 18 and up.</p></div>
  <div class="tale"><b>Changes</b><p>If this ever changes, for example if Forge adds accounts, this note will be updated first, and you will see it in the app before anything new happens.</p></div>
  <p class="muted small">Questions? Ask the person who shared Forge with you.</p>
  <div class="stack"><button class="primary" data-close>Done</button></div>`;
}
function termsHTML(){
  return `<h2>Terms of use</h2><p class="muted small">Last updated ${DOCS_DATE}</p>
  <div class="tale"><b>A test version</b><p>Forge is an early version shared for testing. It is free, it may change, and things may occasionally break. Save a copy from Settings now and then so you never lose your Forgelings.</p></div>
  <div class="tale"><b>For adults</b><p>You need to be 18 or older to use Forge while it is being tested.</p></div>
  <div class="tale"><b>Nothing to buy</b><p>Forgelings, packs, curios and keepsakes cannot be bought or sold and have no value outside the app.</p></div>
  <div class="tale"><b>Small things, your judgment</b><p>Daily callings are gentle suggestions, not medical, mental health or professional advice. Only do what is safe and right for you, and skip anything that is not. Rest days are always fine.</p></div>
  <div class="tale"><b>Your words are yours</b><p>Anything you write stays yours. If you send feedback, it may be used to improve Forge.</p></div>
  <div class="tale"><b>As it is</b><p>Forge is provided as it is, without promises that it will always work or keep your data. To the extent the law allows, the people who make Forge are not responsible for losses from using it.</p></div>
  <div class="tale"><b>The art and the world</b><p>Forge, the Forgelings and their stories belong to their creator. Please do not copy them into other products.</p></div>
  <div class="stack"><button class="primary" data-close>Done</button></div>`;
}
'''
rep('/* ================= Start ================= */', DOCS_JS + '\n/* ================= Start ================= */')
rep("  else if(b.id==='btnReport')shareOrCopy(", """  else if(b.id==='btnPrivacy')openSheet(privacyHTML());
  else if(b.id==='btnTerms')openSheet(termsHTML());
  else if(b.id==='btnErase'){
    if(b.dataset.armed!=='1'){b.dataset.armed='1';b.textContent='Tap again to erase everything. This cannot be undone.';return;}
    try{localStorage.removeItem(KEY);localStorage.removeItem(KEY+'-recovery');localStorage.removeItem(QSEEN);}catch(e){}
    state=migrate(fresh());bf={type:'all',mood:'all',sort:'new',page:0};tab='today';applySettings();render();openAgeGate();
  }
  else if(b.id==='btnReport')shareOrCopy(""")
# The first screen mentions them, quietly
rep("""<p class="tsmall">No account. Everything stays on this phone.</p>""",
    """<p class="tsmall">No account. Everything stays on this phone. For adults 18 and up.</p>""")

# The Ember charm was hard to see on some Forgelings: make the pendant a little larger.
rep("stamp(g,15,cy,['o..o','.oo.','.ya.','.aa.'],false);", "stamp(g,14,cy,['.o..o.','..oo..','.oyyo.','.oyao.','..oo..'],false);")
rep('<title>Forge (prototype 0.22.1)</title>', '<title>Forge (prototype 0.22.2)</title>')
rep("const VERSION='prototype 0.22.1';", "const VERSION='prototype 0.22.2';")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
