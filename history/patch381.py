# Forgelings 0.38.1: a chosen realm lights up along its own outline (Hunter: tapping a realm drew a box that didn't
# match its shape). The box was the browser's focus rectangle around the tap target. Now:
#  - the chosen realm gets a gold ink line along its real edge (wobbled by the same pen filter as the map's ink),
#    with a soft gold glow under it that breathes twice when you choose it (still with reduced motion),
#  - the browser's focus box is gone; keyboard focus draws a dashed line along the realm's own edge instead.
# Reads base38.html.
src = open('base38.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
rep('    if(sel)g+=`<path d="${d}" class="mp-st mp-sel" fill="none" stroke-width="2.4" stroke-dasharray="2 5" transform="translate(0 0)"/>`;',
    '    if(sel)g+=`<g class="mp-selg" aria-hidden="true"><path d="${d}" class="mp-selglow" fill="none" stroke-width="7" stroke-linejoin="round" filter="url(#mpGlow)"/><path d="${d}" class="mp-gold mp-sel" fill="none" stroke-width="2.2" stroke-linejoin="round" filter="url(#mpInk)"/></g>`;')
rep('<defs><filter id="mpBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1"/></filter>',
    '<defs><filter id="mpBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1"/></filter><filter id="mpGlow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>')
rep('.mphit{cursor:pointer;-webkit-tap-highlight-color:transparent}.mphit:focus-visible{outline:3px solid var(--plum);outline-offset:2px}\n.mp-sel{stroke:var(--plum)}',
    '.mphit{cursor:pointer;-webkit-tap-highlight-color:transparent;outline:none}.mphit:focus{outline:none}.mphit:focus-visible{outline:none;stroke:var(--plum);stroke-width:1.8;stroke-dasharray:4 3}\n.mp-selglow{stroke:#FFD36B;opacity:.55}\nhtml:not(.reduce) .mp-selglow{animation:mpBreath 1.5s ease-in-out 2}\n@keyframes mpBreath{0%,100%{opacity:.55}50%{opacity:.9}}')
rep('<title>Forgelings (prototype 0.38.0)</title>', '<title>Forgelings (prototype 0.38.1)</title>')
rep("const VERSION='prototype 0.38.0'", "const VERSION='prototype 0.38.1'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
