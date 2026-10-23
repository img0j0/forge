# Forgelings 0.35.2: Living Sky, finished on Today. Hunter saw 0.35.1 on his iPhone and Today still read like the old
# dark theme: the panels kept the purple pixel frame, and the card sat inside a box. Now, in Living Sky:
#  - every panel is dark glass with pixel-stepped corners and four gold rivets (no purple frame),
#  - Today's card stands on the sky, on its pedestal in firelight, with only the text and buttons in glass below it.
# Plain is untouched. Reads base351.html.
src = open('base351.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
RIV = lambda top, bot: (f"linear-gradient(#FFD36B,#FFD36B) left 8px top {top}/4px 4px no-repeat,linear-gradient(#FFD36B,#FFD36B) right 8px top {top}/4px 4px no-repeat,"
                        f"linear-gradient(#FFD36B,#FFD36B) left 8px bottom {bot}/4px 4px no-repeat,linear-gradient(#FFD36B,#FFD36B) right 8px bottom {bot}/4px 4px no-repeat")
CSS = """
/* ---- 0.35.2: glass panels with gold rivets; Today's card stands on the sky ---- */
html.ls .panel-box,html.ls .group,html.ls .hero,html.ls .setblock{border:0 !important;border-image:none !important;border-radius:0 !important;clip-path:var(--step) !important;background:%(R)s,var(--dot) 0 0/8px 8px repeat,var(--glass) !important}
html.ls .panel-box{padding:18px 18px 16px !important}
html.ls .group{padding:6px 4px !important}
html.ls .setblock{padding:20px 20px 18px !important}
html.ls .hero{padding:24px 16px 20px !important}
html.ls .hero:is(:has(#btnShowToday),:has(#btnTurn),:has(#btnShowFav)){clip-path:none !important;background:%(RH)s,var(--ped) center 204px/176px 22px no-repeat,radial-gradient(circle at 50%% 116px,var(--glow) 0,transparent 128px),linear-gradient(to bottom,transparent 0 232px,var(--glass) 232px) !important}
html.ls .hero:is(:has(#btnShowToday),:has(#btnTurn),:has(#btnShowFav)) h2{margin-top:16px}
""" % {'R': RIV('8px', '8px'), 'RH': RIV('240px', '8px')}
rep("</style>\n</head>", CSS + "</style>\n</head>")
rep('<title>Forgelings (prototype 0.35.1)</title>', '<title>Forgelings (prototype 0.35.2)</title>')
rep("const VERSION='prototype 0.35.1'", "const VERSION='prototype 0.35.2'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
