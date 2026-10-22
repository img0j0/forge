# Forge 0.24.1: soft music is on by default until the player turns it off. Reads base24.html, writes work.html.
src = open('base24.html', encoding='utf8').read()
def rep(old, new, count=1):
    global src
    n = src.count(old); assert n == count, f'{n} matches for {old[:70]!r}'
    src = src.replace(old, new)

# Settings chip: on unless the player has turned it off
rep('aria-pressed="${S.music===true}">Soft music ${S.music===true?\'on\':\'off\'}',
    'aria-pressed="${S.music!==false}">Soft music ${S.music!==false?\'on\':\'off\'}')
# The mixer and the start/stop check follow the same rule
rep('AU.mus.gain.setTargetAtTime(S.music===true?duck*.45:0,t,.6);', 'AU.mus.gain.setTargetAtTime(S.music!==false?duck*.45:0,t,.6);')
rep('const wantMus=sOn()&&state.settings.music===true;', 'const wantMus=sOn()&&state.settings.music!==false;')
# Toggle: from on (unset or true) to off, and back
rep("else if(b.id==='setMusic'){state.settings.music=!state.settings.music;", "else if(b.id==='setMusic'){state.settings.music=state.settings.music===false;")

rep('<title>Forge (prototype 0.24.0)</title>', '<title>Forge (prototype 0.24.1)</title>')
rep("const VERSION='prototype 0.24.0';", "const VERSION='prototype 0.24.1';")
open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
