# Forge 0.17.1: echoes at most once a week, daily cards only; relighting the Hearth survives closing the app mid-wake.
# Applies count-asserted replacements to base17.html (0.17.0) and writes work.html.
src = open('base17.html', encoding='utf8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:80]!r}'
    src = src.replace(old, new)

rep('<title>Forge (prototype 0.17.0)</title>', '<title>Forge (prototype 0.17.1)</title>')
rep("const VERSION='prototype 0.17.0';", "const VERSION='prototype 0.17.1';")

# ---- save(): while the fire is being relit, the saved copy already counts as awake ----
rep("function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){}}",
    "function save(){try{let s=state;if(sleepRun&&s&&s.hearth&&s.hearth.sleep)s=Object.assign({},s,{hearth:Object.assign({},s.hearth,{sleep:null})});localStorage.setItem(KEY,JSON.stringify(s));}catch(e){}}")
# welcomes are counted when the fire is relit, not when the animation ends
rep("  sleepRun={t0:performance.now(),woke:{},msg:'The fire catches, warm and golden.'};\n  hearthPoke();renderHearth();",
    "  sleepRun={t0:performance.now(),woke:{},msg:'The fire catches, warm and golden.'};\n  hh.welcomes=(hh.welcomes||0)+1;save();\n  hearthPoke();renderHearth();")
rep("  const hh=state.hearth;hh.sleep=null;hh.welcomes=(hh.welcomes||0)+1;save();",
    "  const hh=state.hearth;hh.sleep=null;save();")

# ---- damaged saves: a malformed echo record is dropped ----
rep("  if(s.wander&&(typeof s.wander!=='object'",
    "  if(s.echo!==undefined&&s.echo!==null&&(typeof s.echo!=='object'||typeof s.echo.date!=='string'||!Number.isFinite(s.echo.id)||typeof s.echo.lab!=='string'))s.echo=null;\n  if(s.wander&&(typeof s.wander!=='object'")

# ---- echoes: daily cards only, and at most one every seven days ----
rep("    if(!c||typeof c.date!=='string'||c.date>=k)continue;",
    "    if(!c||c.source!=='daily'||typeof c.date!=='string'||c.date>=k)continue;")
rep("/* One echo at most per day: the oldest card whose anniversary is today, preferring the daily card over pack finds. */",
    "/* The oldest daily card whose anniversary is today. Pack finds are not tied to a day's calling, so they do not echo. */")
rep('''function echoHTML(){
  const e=echoFor(todayKey());if(!e)return '';
  const c=e.c,''',
'''const ECHO_GAP=7;
/* Decided once per day and remembered, so the line is stable all day; after one appears, the next waits at least a week. */
function echoToday(){
  const k=todayKey(),E=state.echo;
  if(E&&E.date===k){const c=cardById(E.id);return c?{c,lab:E.lab}:null;}
  if(E&&!(dayDiff(E.date,k)>=ECHO_GAP))return null;
  const e=echoFor(k);if(!e)return null;
  state.echo={date:k,id:e.c.id,lab:e.lab};save();return e;
}
function echoHTML(){
  const e=echoToday();if(!e)return '';
  const c=e.c,''')
rep("it may appear under today's card so you can read that day again.",
    "it may now and then appear under today's card so you can read that day again. Never more than once a week.")

open('work.html', 'w', encoding='utf8').write(src)
print('patched OK', len(src))
