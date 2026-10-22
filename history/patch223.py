# Forge 0.22.3: panels in the same pixel material as the rest of the world, and a small stage for the
# Forgeling on Today. CSS and a couple of attributes only. Reads base222.html, writes work.html.
import urllib.parse
src = open('base222.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# A 12x12 nine-slice pixel frame: stepped corners, outline, a lit top-left edge and a shaded bottom-right edge.
FRAME = ["..OOOOOOOO..",
         ".OHHHHHHHHO.",
         "OHGHHHHHHGSO",
         "OHHFFFFFFSSO",
         "OHFFFFFFFFSO",
         "OHFFFFFFFFSO",
         "OHFFFFFFFFSO",
         "OHFFFFFFFFSO",
         "OHSFFFFFFSSO",
         "OHGSSSSSSGSO",
         ".OSSSSSSSSO.",
         "..OOOOOOOO.."]
def runs_svg(rows,cols,extra=''):
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{len(rows[0])}" height="{len(rows)}" viewBox="0 0 {len(rows[0])} {len(rows)}" shape-rendering="crispEdges"{extra}>']
    for y,row in enumerate(rows):
        x=0
        while x<len(row):
            ch=row[x]
            if ch=='.': x+=1; continue
            e=x
            while e<len(row) and row[e]==ch: e+=1
            out.append(f'<rect x="{x}" y="{y}" width="{e-x}" height="1" fill="{cols[ch]}"/>'); x=e
    out.append('</svg>'); return ''.join(out)
def frame_svg(cols): return runs_svg(FRAME,cols)
def uri(svg): return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=' =:/,;<>') .replace('"', "'") + '")'
LIGHT = {'O':'#A99BDA','H':'#FFFFFF','F':'#FFFFFF','S':'#E4DDF5','G':'#E0A93A'}
DARK  = {'O':'#5A4E9A','H':'#3D366E','F':'#231F3D','S':'#191630','G':'#E8B04A'}
# A pixel pedestal for the Forgeling to stand on.
PED = ["....OOOOOOOOOOOOOOOO....",
       "..OOTTTTTTTTTTTTTTTTOO..",
       ".OTTTTTTTTTTTTTTTTTTTTO.",
       "OSSTTTTTTTTTTTTTTTTTTSSO",
       "OSSSSSSSSSSSSSSSSSSSSSSO",
       ".OSSSSSSSSSSSSSSSSSSSSO.",
       "..OOOOOOOOOOOOOOOOOOOO.."]
def ped_svg(cols): return runs_svg(PED,cols,' preserveAspectRatio="none"')
PL = {'O':'#B9AEDD','T':'#EDE8FA','S':'#D6CDEE'}
PD = {'O':'#0F0C22','T':'#4A4180','S':'#332C5E'}

DOTL='url("data:image/svg+xml,'+__import__('urllib.parse').parse.quote('<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" shape-rendering="crispEdges"><rect x="1" y="1" width="2" height="2" fill="#5B4A9E" fill-opacity=".045"/><rect x="5" y="5" width="2" height="2" fill="#5B4A9E" fill-opacity=".045"/></svg>',safe=' =:/,;<>').replace('"',"'")+'")'
DOTD=DOTL.replace('%235B4A9E','%23FFFFFF').replace('.045','.03')
rep(':root{', f':root{{--dotL:{DOTL};--dotD:{DOTD};--frameL:{uri(frame_svg(LIGHT))};--frameD:{uri(frame_svg(DARK))};--pedL:{uri(ped_svg(PL))};--pedD:{uri(ped_svg(PD))};', 1)
rep('/* Nav */', '''/* ---- 0.22.3: panels in pixel material ---- */
:root{--frame:var(--frameL);--ped:var(--pedL);--dot:var(--dotL);--glow:rgba(255,206,110,.42)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--frame:var(--frameD);--ped:var(--pedD);--dot:var(--dotD);--glow:rgba(255,180,100,.26)}}
:root[data-theme="dark"]{--frame:var(--frameD);--ped:var(--pedD);--dot:var(--dotD);--glow:rgba(255,180,100,.26)}
.panel-box,.group,.hero,.setblock{border:12px solid transparent !important;border-radius:0 !important;border-image:var(--frame) 4 / 12px / 0 stretch !important;background:var(--dot) 0 0/8px 8px repeat,var(--surface) !important;background-clip:padding-box !important;image-rendering:pixelated}
.panel-box{padding:6px 6px 4px !important}
.group{overflow:visible !important}
.group .rowl:first-child{border-top:0}
.hero{clip-path:none !important;padding:12px 8px 8px !important}
.herowrap{filter:none !important}
.hero:has(#btnShowToday),.hero:has(#btnTurn){background:var(--ped) center 192px/176px 22px no-repeat,radial-gradient(circle at 50% 104px,var(--glow) 0,transparent 128px),var(--dot) 0 0/8px 8px repeat,var(--surface) !important;background-clip:padding-box !important}
.hero #btnShowToday,.hero #btnTurn{margin-bottom:10px}
/* Nav */''')

rep('<title>Forge (prototype 0.22.2)</title>', '<title>Forge (prototype 0.22.3)</title>')
rep("const VERSION='prototype 0.22.2';", "const VERSION='prototype 0.22.3';")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
