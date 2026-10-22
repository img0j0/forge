# Forge 0.28.1: the app is now called Forgelings (plain "Forge" is crowded in app stores and trademarks).
# "The Forge" stays as the name of the world inside the app (the Forge asks, every Forge, Forgebound).
# Adds the support email to the in-app privacy note. The save key (forge-app-v1) is unchanged so nothing is lost.
# Reads base28.html.
src = open('base28.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
EMAIL = 'forgelings.app@gmail.com'

rep('<title>Forge (prototype 0.28.0)</title>', '<title>Forgelings (prototype 0.28.1)</title>')
rep("const VERSION='prototype 0.28.0';", "const VERSION='prototype 0.28.1';")
rep('<meta name="apple-mobile-web-app-title" content="Forge">', '<meta name="apple-mobile-web-app-title" content="Forgelings">')
rep("else d.setAttribute('aria-label','Forge');}", "else d.setAttribute('aria-label','Forgelings');}")
rep('<h1 class="wordmark" id="dlgTitle">Forge</h1>', '<h1 class="wordmark" id="dlgTitle">Forgelings</h1>')
rep('/* Nav */', '#modal .tale a,#modal p a{color:var(--plum);text-decoration:underline;text-underline-offset:2px;overflow-wrap:anywhere}\n/* Nav */')
rep('.wordmark{font:600 64px/1 var(--display);', '.wordmark{font:600 clamp(40px,14.5vw,64px)/1 var(--display);')
rep('<h2>How is Forge treating you?</h2>', '<h2>How is Forgelings treating you?</h2>')
rep("'What do you wish Forge did?'", "'What do you wish Forgelings did?'")
rep('return `Forge pilot report (${VERSION})', 'return `Forgelings pilot report (${VERSION})')
rep('Everything you do in Forge stays on this device. Forge has no accounts and sends', 'Everything you do in Forgelings stays on this device. It has no accounts and sends')
rep('id="btnPrivacy">How Forge handles your data</button>', 'id="btnPrivacy">How Forgelings handles your data</button>')
rep('/* ================= Age screen (Forge is 13 and up) ================= */', '/* ================= Age screen (18 and up while testing) ================= */')
rep('We use this to set up Forge for you', 'We use this to set up Forgelings for you')
rep('<p class="rv-title">Forge is not available for you just yet</p><p class="rv-hint">While Forge is being tested',
    '<p class="rv-title">Forgelings is not available for you just yet</p><p class="rv-hint">While Forgelings is being tested')
rep("open Forge in your phone\\u2019s browser", "open Forgelings in your phone\\u2019s browser")
rep("title:'Forge backup'", "title:'Forgelings backup'")
rep("toast('That file is too big to be a Forge copy.')", "toast('That file is too big to be a Forgelings copy.')")
rep("'My Forge report'", "'My Forgelings report'")
rep('<b>Put Forge on your home screen</b>', '<b>Put Forgelings on your home screen</b>')
rep('name=`forge-backup-${k}.json`', 'name=`forgelings-backup-${k}.json`')

# in-app privacy note and terms
i = src.index('function privacyHTML(){'); j = src.index('/* ---- The realm games', i)
block = src[i:j]
for a, b in [('<h2>How Forge handles your data</h2>', '<h2>How Forgelings handles your data</h2>'),
             ('<b>What Forge keeps</b>', '<b>What Forgelings keeps</b>'),
             ('Forge has no accounts and no server of its own, so nobody else can see it, including the people who make Forge.',
              'Forgelings has no accounts and no server of its own, so nobody else can see it, including the people who make it.'),
             ('<b>What Forge never does</b>', '<b>What Forgelings never does</b>'),
             ('a message to the person testing Forge with you.', 'a message to the person testing Forgelings with you.'),
             ('<b>Where Forge is hosted</b>', '<b>Where Forgelings is hosted</b>'),
             ('Forge itself never receives them.', 'Forgelings itself never receives them.'),
             ('or remove Forge and clear', 'or remove Forgelings and clear'),
             ('While Forge is being tested, it is for adults 18 and up.', 'While Forgelings is being tested, it is for adults 18 and up.'),
             ('for example if Forge adds accounts', 'for example if Forgelings adds accounts'),
             ('<p class="muted small">Questions? Ask the person who shared Forge with you.</p>',
              f'<p class="muted small">Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>. The full policy is also at <a href="https://img0j0.github.io/forge/privacy.html" target="_blank" rel="noopener">img0j0.github.io/forge/privacy.html</a>.</p>'),
             ('<p>Forge is an early version shared for testing.', '<p>Forgelings is an early version shared for testing.'),
             ('to use Forge while it is being tested.', 'to use Forgelings while it is being tested.'),
             ('it may be used to improve Forge.', 'it may be used to improve Forgelings.'),
             ('<p>Forge is provided as it is,', '<p>Forgelings is provided as it is,'),
             ('the people who make Forge are not', 'the people who make Forgelings are not'),
             ('<p>Forge, the Forgelings and their stories belong to their creator.', '<p>Forgelings, the Forge and their stories belong to their creator.')]:
    assert block.count(a) == 1, a; block = block.replace(a, b)
block = block.replace("<div class=\"tale\"><b>The art and the world</b>", f"<div class=\"tale\"><b>Questions</b><p>Email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>.</p></div>\n  <div class=\"tale\"><b>The art and the world</b>", 1)
src = src[:i] + block + src[j:]
rep("const DOCS_DATE='October 16, 2026';", "const DOCS_DATE='October 20, 2026';")

# What's New
rep('const SEEN_V=32;', 'const SEEN_V=33;')
rep("""<ul class="newlist"><li><b>A Forgeling that notices.</b>""",
    """<ul class="newlist"><li><b>A new name: Forgelings.</b> The app is now called Forgelings, after the creatures at its heart. The Forge is still the world they come from, and nothing in your collection changes.</li>
    <li><b>A Forgeling that notices.</b>""")
import re as _re
_i=src.index('<ul class="newlist">'); _j=src.index('</ul>',_i)
_items=_re.findall(r'\s*<li>.*?</li>',src[_i+len('<ul class="newlist">'):_j],_re.S)
src=src[:_i]+'<ul class="newlist">'+''.join(_items[:10])+src[_j:]
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
