# 0.53.0: polish from the quality review (Hunter, November 12).
#   1. The Hearth: what you can do sits right under the fire; the request, the companion row and the extras follow.
#   2. Today: less to read. The line under "Today's card is waiting" repeated the button; "rest days never reset this"
#      shows in the first week only.
#   3. Type: handwriting for headings only (the Binder's count line becomes plain text); Fredoka is kept for the
#      Forgelings name itself, and buttons and labels use Nunito Sans with the rest of the text. The typewriter stamp
#      (dates) and the card print stay: they are part of the journal and the cards.
#   4. The ribbons are quieter: only the open page's ribbon is in full colour.
#   5. One tap turns today's card over (the first card still asks for its own tap, as a small lesson).
import re,subprocess,os
S=open('base52.html').read()
def rep(old,new,n=1):
    global S
    c=S.count(old); assert c==n,(c,n,old[:90]); S=S.replace(old,new)
rep("const VERSION='prototype 0.52.0'","const VERSION='prototype 0.53.0'")
rep("<title>Forgelings (prototype 0.52.0)</title>","<title>Forgelings (prototype 0.53.0)</title>")

# ---- 1. the Hearth: actions first
OLD_H="""    ${reqHTML()}${away?'':mEchoHTML(c)}
    ${cs.length>1?`<div class="chips hwho" role="group" aria-label="Companions">${cs.map((x,i)=>`<button class="chip" data-hslot="${i}" aria-pressed="${i===hf.sel}">${esc(x.nick||x.name)}</button>`).join('')}</div>`:''}
    <div class="group hcompg"><button class="rowl" id="hComp"><span class="rt"><b>${esc(n)}</b><span class="rs">${BOND_NAMES[lv-1]}, bond ${lv} of 5${c.statue?' · has a statue':''}</span><span class="bondbar" aria-hidden="true"><i style="width:${pct}%"></i></span></span><span class="chev" aria-hidden="true">›</span></button></div>
    <div class="actions hgrid">"""
assert S.count(OLD_H)==1
i=S.index(OLD_H); j=S.index('</p>${notes}',i)+len('</p>${notes}')
block=S[i:j]
head,grid=block.split('    <div class="actions hgrid">',1)
grid='    <div class="actions hgrid">'+grid
S=S[:i]+grid.replace('${notes}','')+'\n'+head.rstrip('\n')+'${notes}'+S[j:]

# ---- 2. Today: less to read
rep("""<h2>Today's card is waiting</h2><p class="muted">Turn it over to see today's small thing.</p><button class="primary" id="btnTurnGo">""",
    """<h2>Today's card is waiting</h2><button class="primary" id="btnTurnGo">""")
rep("""more ${5-state.progress===1?'day':'days'} to go. Rest days and missed days never reset this.`""",
    """more ${5-state.progress===1?'day':'days'} to go.${dayN()<=7?' Rest days and missed days never reset this.':''}`""")

# ---- 5. one tap turns the card
rep("if(b.id==='btnTurn'||b.id==='btnTurnGo'||b.id==='btnCard')openVector();",
    "if(b.id==='btnTurn'||b.id==='btnTurnGo'||b.id==='btnCard'){const fr=state.status==='fresh'&&state.onboarded;openVector();if(fr)setTimeout(flipVector,REDUCE?0:260);}")

# ---- 3 and 4: type and ribbons (end of the last stylesheet, so they win)
CSS="""
/* 0.53: handwriting for headings, one text face for the rest; Fredoka is the name on the cover */
:root{--display:'Nunito Sans',system-ui,-apple-system,'Segoe UI',sans-serif}
.wordmark{font-family:'Fredoka','Trebuchet MS',system-ui,sans-serif}
html.jr .app .summary{font:400 16px/1.45 var(--body);color:var(--ink)}
/* 0.53: quiet ribbons; the open page keeps its colour */
html.jr .tab:not([aria-current="page"]){color:#EADFCB}
html.jr .tab[data-tab="today"]:not([aria-current="page"]){background:#7A5A27 !important}
html.jr .tab[data-tab="hearth"]:not([aria-current="page"]){background:#642D2D !important}
html.jr .tab[data-tab="binder"]:not([aria-current="page"]){background:#363E4A !important}
html.jr .tab[data-tab="chronicle"]:not([aria-current="page"]){background:#36432F !important}
html.jr .tab[data-tab="settings"]:not([aria-current="page"]){background:#473651 !important}
</style>"""
k=S.rindex('</style>'); S=S[:k]+CSS+S[k+len('</style>'):]

out=os.environ.get('OUT','work.html'); open(out,'w').write(S)
js=re.findall(r'<script>([\s\S]*?)</script>',S); open('/tmp/chk53.js','w').write('\n;\n'.join(js))
r=subprocess.run(['node','--check','/tmp/chk53.js'],capture_output=True,text=True); print('node --check',r.returncode,r.stderr[:600],'->',out)
