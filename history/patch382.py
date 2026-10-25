# Forgelings 0.38.2: chips that sit straight on the sky (Filter and Sort in the Binder, Map / Tales / Journal) were
# see-through, so the moon or sun could show through them (Hunter saw the moon over Sort). On the sky they are now
# solid: night glass by night, pale paper by day. Inside panels nothing changes. Reads base381.html.
src = open('base381.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)
rep('html.ls :is(.chip,.fchip,.pill){border:0;border-radius:0;clip-path:var(--step);background:var(--chip)}',
    'html.ls :is(.chip,.fchip,.pill){border:0;border-radius:0;clip-path:var(--step);background:linear-gradient(var(--chip),var(--chip)),var(--chipbase,transparent)}\n'
    'html:root.ls{--chipbase:rgba(20,15,48,.94)}html:root.ls[data-skyink="dark"]{--chipbase:#EEF3F8}\n'
    'html.ls :is(.panel-box,.group,.hero,.setblock,.sheet,.tabs,.binder,.mapwrap,.ov,.calling,.rib,.chron,.realm,.otale,.mecho){--chipbase:transparent}')
rep('<title>Forgelings (prototype 0.38.1)</title>', '<title>Forgelings (prototype 0.38.2)</title>')
rep("const VERSION='prototype 0.38.1'", "const VERSION='prototype 0.38.2'")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src.encode()))
