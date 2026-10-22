import json
from sprites import S, K, norm
out={}
for nm in S:
    pal,g=norm(nm)
    keys=sorted(pal)
    out[nm]=','.join(k+pal[k][1:] for k in keys)+'|'+''.join(g)
js='const CSPR='+json.dumps(out,separators=(',',':'))+';'
open('csprites.js','w').write(js); print(len(js))
