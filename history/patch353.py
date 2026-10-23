# Forgelings 0.35.3: a polish pass after a full visual audit of every screen at night and by day (Hunter asked for
# nothing to look unfinished).
#  - Glass is a touch denser (.94), so the sun, moon and stars no longer ghost through panels as smudges.
#  - The night moon is a real crescent. Its cut-out was centred on the moon itself, which left a broken ring.
#  - Full-screen overlays (a card up close, the reveal) re-declare the light ink, so muted lines stay readable when
#    the sky outside is in day ink. ("A second reading opens in…" was nearly invisible by day.)
#  - The pack's wordmark was falling back to a plain font (an unquoted 'Press Start 2P' in SVG). It now reads
#    FORGELINGS in the pixel font, and so does the share picture (naming rule: the app is Forgelings).
#  - The Forge sheet: larger piece icons, the charm line said once instead of five times, tidier "needs" lines.
#  - The Hearth line after forging keeps a piece's proper name ("Forged with Pip: Charm of Meadow.").
# Reads base352.html.
src = open('base352.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep("--glass:rgba(20,15,48,.9)", "--glass:rgba(20,15,48,.94)")
rep("html.ls :is(.panel-box,.group,.hero,.setblock,.sheet,.tabs,.binder,.mapwrap){", "html.ls :is(.panel-box,.group,.hero,.setblock,.sheet,.tabs,.binder,.mapwrap,.ov){")
rep("html.ls .hmsg{font:400 22px/1.1 var(--px2);", "html.ls .hmsg{font:400 20px/1.15 var(--px2);")
# the moon
rep("if(P.orb){const cx=W-15,cy=Math.round(H*.17),R=ph==='day'?5:4;for(let y=-R;y<=R;y++)for(let x=-R;x<=R;x++)if(x*x+y*y<=R*R+1)put(cx+x,cy+y,P.orb);if(ph==='night')for(let y=-R;y<=R;y++)for(let x=-R;x<=R;x++)if((x+2)*(x+2)+(y-1)*(y-1)<=R*R-2)put(cx+x+2,cy+y-1,P.s[0]);}",
    "if(P.orb){const cx=W-15,cy=Math.round(H*.17),R=5;for(let y=-R;y<=R;y++)for(let x=-R;x<=R;x++)if(x*x+y*y<=R*R+1&&!(ph==='night'&&(x-2)*(x-2)+(y+1)*(y+1)<=R*R-4))put(cx+x,cy+y,P.orb);}")
# the pack and the share picture
rep('<text x="80" y="172" text-anchor="middle" font-family="Press Start 2P,monospace" font-size="15" fill="#fff">FORGE</text>',
    '<text x="80" y="172" text-anchor="middle" font-family="\'Press Start 2P\',monospace" font-size="11" fill="#fff">FORGELINGS</text>')
rep('<text x="80" y="196" text-anchor="middle" font-family="VT323,monospace"', '<text x="80" y="196" text-anchor="middle" font-family="\'VT323\',monospace"')
rep('aria-label="FORGE 5 pixel Forgelings. Tear open the pack"', 'aria-label="FORGELINGS 5 pixel Forgelings. Tear open the pack"')
rep("""x.font='22px "Press Start 2P", monospace';x.fillText('FORGE',W/2,H-72);""", """x.font='18px "Press Start 2P", monospace';x.fillText('FORGELINGS',W/2,H-72);""")
# the Forge sheet
rep("what:'A charm any Forgeling can wear. It shows by the fire and in the corner of the card.'},", "what:''},", 5)
rep("function fgCan(r){", "const FG_KIND={Keepsake:'Charms can be worn by any Forgeling, by the fire and on its card.'};\nfunction fgCan(r){")
rep("function fgNeeds(r){const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?THEMES[r.ti].name+' ':'';\n  return `Needs ${r.sp} ${rn}${r.sp===1?'spare':'spares'} and ${r.emb} embers. You have ${sp} ${rn}${sp===1?'spare':'spares'} and ${e} ${e===1?'ember':'embers'}.`;}",
    "function fgNeeds(r){const sp=spareTotal(r.ti),e=embers(),rn=r.ti!==undefined?THEMES[r.ti].name+' ':'';\n  return `Needs ${r.sp} ${rn}${r.sp===1?'spare':'spares'} and ${r.emb} embers (you have ${sp} and ${e}).`;}")
rep("<span class=\"fi\" aria-hidden=\"true\">${fgImg(r.id,20)}</span><span><b>${esc(r.name)}</b><small>${r.kind}. ${esc(r.what)}</small>",
    "<span class=\"fi\" aria-hidden=\"true\">${fgImg(r.id,30)}</span><span><b>${esc(r.name)}</b><small>${r.what?r.kind+'. '+esc(r.what):r.kind}</small>")
rep("""<ul class="furn forgel">${rows}</ul>""", """<p class="muted small" style="margin-top:6px">${esc(FG_KIND.Keepsake)}</p><ul class="furn forgel">${rows}</ul>""")
rep("ul.forgel li .fi{width:28px;height:34px;background:none}", "ul.forgel li .fi{width:34px;height:42px;background:none;display:grid;place-items:center}\nul.forgel li .fi .cimg{width:32px;height:40px}")
rep("hf.msg=`Forged with ${s.nick||s.name}: ${r.name.toLowerCase()}.`;", "hf.msg=`Forged with ${s.nick||s.name}: ${/^An? /.test(r.name)?r.name[0].toLowerCase()+r.name.slice(1):r.name}.`;")

rep('<title>Forgelings (prototype 0.35.2)</title>', '<title>Forgelings (prototype 0.35.3)</title>')
rep("const VERSION='prototype 0.35.2'", "const VERSION='prototype 0.35.3'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
