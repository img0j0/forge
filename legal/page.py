# Builds Forge's public pages (privacy, terms, support) for the website and App Store Connect.
# Run from /home/claude/forge: python3 legal/page.py  -> writes legal/out/*.html, copied into pwa/ by pwa.py's caller.
import os
DATE = 'October 20, 2026'
CONTACT = os.environ.get('FORGE_CONTACT', 'forgelings.app@gmail.com')  # set to the support email before App Store submission
OUT = os.path.join(os.path.dirname(__file__), 'out'); os.makedirs(OUT, exist_ok=True)

CSS = '''
:root{--bg:#F4F0E8;--card:#FFFFFF;--ink:#2E2A47;--muted:#5E5873;--line:#D9D2F5;--accent:#5B4A9E;--gold:#E2B04A}
@media (prefers-color-scheme: dark){:root{--bg:#1C1930;--card:#262241;--ink:#F1EEFF;--muted:#B9B2D6;--line:#3D3762;--accent:#C7B8FF;--gold:#FFD36B}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:680px;margin:0 auto;padding:28px 16px 48px}
header{display:flex;align-items:center;gap:12px;margin-bottom:8px}
header img{width:44px;height:44px;border-radius:10px}
header a{color:var(--ink);text-decoration:none;font-weight:700;font-size:20px}
h1{font-size:28px;line-height:1.2;margin:18px 0 4px}
.date{color:var(--muted);font-size:14px;margin:0 0 20px}
section{background:var(--card);border:1.5px solid var(--line);border-radius:14px;padding:14px 16px;margin:12px 0}
h2{font-size:18px;margin:0 0 6px}
p{margin:0 0 8px}p:last-child{margin-bottom:0}
ul{margin:4px 0 0;padding-left:20px}
a{color:var(--accent)}
nav{margin-top:28px;padding-top:14px;border-top:1.5px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 18px;font-size:15px}
nav a{display:inline-block;padding:10px 0}
.lead{font-size:18px}
'''

def contact_line(prefix='Questions or requests'):
    if CONTACT:
        return f'<p>{prefix}: email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>'
    return '<p>Questions or requests: see the <a href="support.html">support page</a>.</p>'

def page(fn, title, desc, body):
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Forgelings</title><meta name="description" content="{desc}">
<link rel="icon" href="icon-192.png"><style>{CSS}</style></head>
<body><main>
<header><img src="icon-192.png" alt=""><a href="./">Forgelings</a></header>
<h1>{title}</h1><p class="date">Last updated {DATE}</p>
{body}
<nav aria-label="Forgelings pages"><a href="./">Open Forgelings</a><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms of use</a><a href="support.html">Support</a></nav>
</main></body></html>'''
    open(os.path.join(OUT, fn), 'w', encoding='utf8').write(html)

page('privacy.html', 'Privacy policy', 'How Forgelings handles your data: it all stays on your device.', f'''
<p class="lead">Short version: Forgelings collects nothing. Everything you do in the app stays on your device, and nobody else can see it, including the people who make Forgelings.</p>
<section><h2>What Forgelings keeps, and where</h2>
<p>Forgelings keeps your Forgelings, the days you showed up or rested, anything you write (names, tales, margin notes and feedback answers), your settings, and the fact that you are an adult. Your birth date is never kept.</p>
<p>All of it is stored only on your device: in your browser for the web version, or inside the app on your phone for the app version. Forgelings has no accounts and no server of its own.</p></section>
<section><h2>What Forgelings never does</h2>
<ul><li>No tracking, no analytics and no advertising.</li><li>No selling, renting or sharing of any information.</li><li>No third-party code that collects data.</li><li>Nothing about you leaves your device unless you choose to send it.</li></ul></section>
<section><h2>When you choose to share</h2>
<p>Some features create something you can send yourself: a share picture of a Forgeling, a backup file of your collection, a text report, or a gift or statue link for a friend. These go only where you put them, for example a message or your own files. Forgelings does not receive a copy.</p>
<p>A gift link holds only the curio you are giving, your Forgeling's name and look, and your note if you add one. A statue link holds only what a statue is built from: its look, its name and the day it was cast. That part of a link comes after a # sign, which browsers never send to the website, so not even the host sees it.</p></section>
<section><h2>Hosting</h2>
<p>The web version of Forgelings is delivered by GitHub Pages. Like any website, GitHub receives basic technical details such as your IP address when it delivers the page, under <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a>. Forgelings itself never receives them. If you install Forgelings from an app store, that store's own privacy policy covers the download.</p></section>
<section><h2>Keeping or deleting your data</h2>
<p>Because your data is only on your device, you are in control of it. To delete everything, use "Erase everything on this device" in the app's Settings, or delete the app (or clear this site's data in your browser). There is no other copy anywhere, so there is nothing for anyone to delete on a server.</p></section>
<section><h2>Age</h2><p>While Forgelings is being tested, it is for adults 18 and up. It is not directed at children.</p></section>
<section><h2>Changes</h2><p>If Forgelings ever changes how it handles data, for example by adding accounts or backups to a server, this policy will be updated first, and you will see the change in the app before anything new happens.</p></section>
<section><h2>Contact</h2>{contact_line()}</section>
''')

page('terms.html', 'Terms of use', 'The terms for using Forgelings, in plain English.', f'''
<section><h2>An early version</h2><p>Forgelings is an early version shared for testing. It is free, it may change, and things may occasionally break. Save a copy of your collection from Settings now and then so you never lose your Forgelings.</p></section>
<section><h2>For adults</h2><p>You need to be 18 or older to use Forgelings while it is being tested.</p></section>
<section><h2>Nothing to buy</h2><p>Forgelings, packs, curios and keepsakes cannot be bought or sold and have no value outside the app. The odds for packs are shown in the app.</p></section>
<section><h2>Small things, your judgment</h2><p>Daily callings are gentle suggestions, not medical, mental health or professional advice. Only do what is safe and right for you, and skip anything that is not. Rest days are always fine.</p></section>
<section><h2>Your words are yours</h2><p>Anything you write in Forgelings stays yours and stays on your device. If you send feedback, it may be used to improve Forgelings.</p></section>
<section><h2>As it is</h2><p>Forgelings is provided as it is, without promises that it will always work or keep your data. To the extent the law allows, the people who make Forgelings are not responsible for losses from using it.</p></section>
<section><h2>The art and the world</h2><p>Forgelings, the Forge and their stories belong to their creator. Please do not copy them into other products.</p></section>
<section><h2>App stores</h2><p>If you get Forgelings from an app store, that store's standard terms for apps also apply, and these terms add to them.</p></section>
<section><h2>Contact</h2>{contact_line('Questions')}</section>
''')

support_contact = (f'<p>Email <a href="mailto:{CONTACT}">{CONTACT}</a>. A person reads every message.</p>' if CONTACT
                   else '<p>If someone shared Forgelings with you, reach out to them directly. A public support address is coming soon.</p>')
page('support.html', 'Support', 'Help with Forgelings.', f'''
<section><h2>Get in touch</h2>{support_contact}</section>
<section><h2>Common questions</h2>
<p><b>Will I lose my Forgelings if I miss a day?</b> Never. Missed days and rest days don't reset anything.</p>
<p><b>How do I move my collection to a new phone?</b> In Settings, under Backup, save a copy. On the new phone, use Restore and choose that file.</p>
<p><b>Something looks wrong after an update.</b> Close Forgelings completely and open it again. On iPhone, swipe it away in the app switcher first.</p>
<p><b>How do I delete everything?</b> Settings, then "Erase everything on this device". Forgelings keeps no copy anywhere else.</p></section>
''')
print('wrote', sorted(os.listdir(OUT)))
