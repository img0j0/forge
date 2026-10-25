# Forgelings 0.38.6: emblems and parchment. Each of the five games has its own pixel emblem (a dandelion, a fire,
# stacked stones, a snowflake, a lantern) instead of the same Forgeling five times. Snacks get pixel food, and the
# wander list marks each realm (dandelion, fire, wave, snowflake, moon; a spark for Anywhere). The notes under the
# map and the lower part of a realm page are on parchment, like a page of the map, and "Send ... to wander here" is
# the gold button it should be. Reads base385.html.
src = open('base385.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

rep("const FEELS=['easy','good','hard'];",
    "const FEELS=['easy','good','hard'];\n"
    "/* 0.38.6: emblems for games, realms and snacks */\n"
    "const ICON={dandelion:'..+.#..#.+../.#.######.#./..########../.####+#####./..########../.#.######.#./..+.#..#.+../.....#....../.....#....../....##....../...#.#....../.....#......',fire:'....#......./....##...#../...###..##../...####.##../..#+#######./..#+#######./.#+########./.#+#######../..########../...######.../.##########./.#+########.',stones:'....####..../...#+####.../....####..../............/..#######.../.#+#######../..#######.../............/.##########./#+##########/.##########.',wave:'..##....##../.#+##..#+##./##..####..##/............/..##....##../.#+##..#+##./##..####..##',snow:'.....#....../..#..#..#.../...#.#.#..../....###...../.#########../....###...../...#.#.#..../..#..#..#.../.....#......',lantern:'.....##...../....#..#..../..########../...#o++o#.../...#o++o#.../...#o++o#.../...#o++o#.../..########../....####....',spark:'.....##...../.....##...../....####..../...#+####.../############/############/...######.../....####..../.....##...../.....##.....',berries:'......###.../.....##...../..###..###../.#+###.#+##./.#####.####./..###..###../....###...../...#+###..../...#####..../....###.....',toast:'..########../.##########./############/#+##########/#+##########/.##########./.##########./.##########./.##########./.##########.',cookie:'...######.../..##o#####../.#+######o#./.#####o####./.#o########./.######o###./..##o#####../...######...',milk:'...######.../..#+#####.../..#+#####.#./..#######..#/..#+#####..#/..#######.#./..#######.../...#####....'};\n"
    "const GAMEI=[['dandelion','#FFE08A'],['fire','#FF9F43'],['stones','#9FB4C8'],['snow','#D6ECFA'],['lantern','#FFD36B']];\n"
    "const REALMI=[['dandelion','#FFE08A'],['fire','#FF9F43'],['wave','#8CC7F0'],['snow','#D6ECFA'],['','#C9B8FF']];\n"
    "const SNACKI=[['berries','#E0607E'],['toast','#E8B05A'],['cookie','#C98B4E'],['milk','#DCD6F7']];\n"
    "function iconSVG(a){return pixSVG(a[0]?ICON[a[0]]:SIGIL[8],a[1],'rowsig');}")
# games
rep('<button class="moodbtn" data-game="${ti}" data-cid="${c.id}"><img class="gpick" src="${spriteURL(c)}" alt=""><div>',
    '<button class="moodbtn" data-game="${ti}" data-cid="${c.id}">${iconSVG(GAMEI[ti])}<div>')
# snacks
rep('${SNACKS.map((s,i)=>`<button class="moodbtn" data-snack="${i}"><div><b>${s}</b></div></button>`).join(\'\')}',
    '${SNACKS.map((s,i)=>`<button class="moodbtn" data-snack="${i}">${iconSVG(SNACKI[i])}<div><b>${s}</b></div></button>`).join(\'\')}')
# wander realms
rep('return `<button class="moodbtn" data-wgo="${ti}"><div><b>${esc(rName(ti))}</b>',
    'return `<button class="moodbtn" data-wgo="${ti}">${iconSVG(REALMI[ti])}<div><b>${esc(rName(ti))}</b>')
rep('<button class="moodbtn" data-wgo="-1"><div><b>Anywhere</b>',
    '<button class="moodbtn" data-wgo="-1">${iconSVG([\'spark\',\'#C9B8FF\'])}<div><b>Anywhere</b>')
# realm page: the lower part on parchment, the wander button gold
rep("""  const mini=all.slice().sort((a,b)=>b.rarity-a.rarity||b.id-a.id).slice(0,6);""",
    """  const mini=all.slice().sort((a,b)=>b.rarity-a.rarity||b.id-a.id).slice(0,6);out+='<div class="parch realmnotes">';""")
rep("""`<button class="outline" data-wto="${ti}" style="margin-top:10px">Send""",
    """`<button class="primary" data-wto="${ti}">Send""")
rep("""  return out+`<div class="latest" style="margin-top:6px">${mini.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.nick||c.name)}">${cardHTML(c,{w:62,mini:true})}</button>`).join('')}</div>`;""",
    """  return out+`<div class="latest" style="margin-top:6px">${mini.map(c=>`<button data-insp="${c.id}" aria-label="Look at ${esc(c.nick||c.name)}">${cardHTML(c,{w:62,mini:true})}</button>`).join('')}</div></div>`;""")
# map notes
rep("""<div class="mapcap">${notes}${ev?'<h2 style="font-size:1.05rem;margin:12px 0 2px">Small marks in the margin</h2>'+ev:''}</div>`;""",
    """<div class="mapcap parch">${notes}${ev?'<h2 class="parchh">Small marks in the margin</h2>'+ev:''}</div>`;""")

PAPER_STEP = "polygon(0 4px,4px 4px,4px 0,calc(100% - 4px) 0,calc(100% - 4px) 4px,100% 4px,100% calc(100% - 4px),calc(100% - 4px) calc(100% - 4px),calc(100% - 4px) 100%,4px 100%,4px calc(100% - 4px),0 calc(100% - 4px))"
rep(".mapcap p{margin:6px 0}",
    ".mapcap p{margin:6px 0}\n"
    "/* 0.38.6: emblems in sheet rows, and parchment for the map's own notes */\n"
    ".moodbtn .rowsig{flex:none;width:40px;height:40px;image-rendering:pixelated;filter:drop-shadow(0 2px 0 rgba(10,6,28,.45))}\n"
    "html .parch{--ink:#2E2A47;--muted:#5E5878;--plum:#5B4A9E;--line:rgba(46,42,71,.22);color:#2E2A47;background:var(--paper) 0 0/32px 32px repeat,#FBF5E6;padding:12px 16px 14px;margin:12px 0 4px;clip-path:" + PAPER_STEP + ";box-shadow:inset 0 -4px 0 rgba(138,90,50,.18)}\n"
    "html .parch :is(p,li,b,span,small){color:inherit}html .parch .muted{color:#5E5878}\n"
    "html .parch .world{color:#5B3F94;border-left-color:#B49AE0}\n"
    "html .parch .parchh{font:400 22px/1 'VT323',monospace;color:#8A5A32;margin:12px 0 4px;letter-spacing:.02em}\n"
    ".realmnotes .primary{margin:4px 0 6px}")

# ---- room: the pixel grids are stored packed (2 bits a pixel, base64, first char = rows) and unpacked on load
import re as _re, base64 as _b64
PX='.#+o'
def pack(g):
    rows=g.split('/'); bits=[PX.index(ch) for r in rows for ch in r]; by=bytearray((len(bits)+3)//4)
    for i,v in enumerate(bits): by[i>>2]|=v<<((i&3)*2)
    return format(len(rows),'x')+_b64.b64encode(bytes(by)).decode().rstrip('=')
def packjs(m):
    return m.group(1)+'"'+pack(m.group(2))+'"'
m=_re.search(r'const SIGIL=\[(.*?)\];',src); arr=_re.findall(r'"([.#+o/]+)"',m.group(1))
src=src.replace(m.group(0),'const SIGIL=['+','.join('"'+pack(a)+'"' for a in arr)+'].map(unpk);',1)
m=_re.search(r'const FACE=\{(.*?)\};',src); body=_re.sub(r"'([.#+o/]{40,})'",lambda k:"unpk('"+pack(k.group(1))+"')",m.group(1))
src=src.replace(m.group(0),'const FACE={'+body+'};',1)
m=_re.search(r'const ICON=\{(.*?)\};',src); body=_re.sub(r"'([.#+o/]{40,})'",lambda k:"'"+pack(k.group(1))+"'",m.group(1))
src=src.replace(m.group(0),'const ICON=Object.fromEntries(Object.entries({'+body+'}).map(([k,v])=>[k,unpk(v)]));',1)
rep("const SIGIL=[", "function unpk(e){const h=parseInt(e[0],16),b=atob(e.slice(1)+'==='.slice((e.length-1)%4||3)),P='.#+o';let o='';for(let i=0;i<h*12;i++){o+=P[(b.charCodeAt(i>>2)>>((i&3)*2))&3];if(i%12===11&&i<h*12-1)o+='/';}return o;}\nconst SIGIL=[")
rep('<title>Forgelings (prototype 0.38.5)</title>', '<title>Forgelings (prototype 0.38.6)</title>')
rep("const VERSION='prototype 0.38.5'", "const VERSION='prototype 0.38.6'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
