# 0.72: richer card backs, still Hunter's "Leather journal" (cardback.py, picked November 1): the same 40 x 56 grid,
#   the same wax seal and mark, now with tooled leather (a faint diamond lattice, lit from the top left), a bevelled
#   gold frame with corner flourishes and studs, shaded ribbons, and a shadow under the seal.
#   P = the back you tap to turn a Forgeling over (reveal, packs, choosing today's card): ribbons tied both ways.
#   T = the backs that carry words (today's card, a card's Moment side): seal high, the lower half kept quiet.
#   packed() gives the CSS-ready SVG, as before.
import math,random,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from cardback import SEAL,SP,W,H,blank,put
def packed(G):
    # 0.73: half the size of cardback.packed (qa_301 keeps pixel art under 9,000 characters): each colour is one
    # stroked path of horizontal runs, the first run on a row placed absolutely and the rest relatively.
    by={}
    for y,row in enumerate(G):
        x=0
        while x<W:
            c=row[x];s0=x
            while x<W and row[x]==c:x+=1
            by.setdefault(c,{}).setdefault(y,[]).append((s0,x-s0))
    bg=max(by,key=lambda c:sum(len(v) for v in by[c].values()))
    out=[]
    for c,rows in by.items():
        if c==bg:continue
        d=[]
        for y,runs in rows.items():
            px=None
            for (x0,n) in runs:
                d.append(f"M{x0} {y}.5h{n}" if px is None else f"m{x0-px} 0h{n}");px=x0+n
        out.append(f"<path stroke='{c}' d='{''.join(d)}'/>")
    svg=f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 56' shape-rendering='crispEdges' preserveAspectRatio='none'><rect width='40' height='56' fill='{bg}'/>{''.join(out)}</svg>"
    return svg.replace('#','%23')
L0,L,L1,L2,TOOL,TOOLHI='#3E1C1D','#5A2C2A','#62322F','#6E3A33','#4A2223','#704033'
EDGE,G0,G,G1,G2,ST='#24100F','#9A6A1A','#E0A82E','#FFD36B','#FFF1C9','#C9A15A'
def leather(G_,R,lattice_rows):
    for y in range(H):
        for x in range(W):
            c=L
            if (x*7+y*13)%11==0:c=L1
            if y in lattice_rows:
                d1,d2=(x+y)%8,(x-y)%8
                if d1==0 or d2==0:c=TOOL
                elif d1==1 or d2==7:c=TOOLHI if R.random()<.6 else L1
            elif (x+y)%8==0 or (x-y)%8==0:c='#532829'
            G_[y][x]=c
    for y in range(2,H-2):
        for x in range(2,W-2):
            if min(x-2,y-2,W-3-x,H-3-y)<1 and G_[y][x]!=TOOL:G_[y][x]=L0
def frame(G_):
    for y in range(H):
        for x in range(W):
            if x<2 or y<2 or x>=W-2 or y>=H-2:G_[y][x]=EDGE
    for x in range(2,W-2):G_[2][x]=G1;G_[H-3][x]=G0
    for y in range(2,H-2):G_[y][2]=G1;G_[y][W-3]=G0
    G_[2][W-3]=G;G_[H-3][2]=G
    for x in range(5,W-5):
        if (x//2)%2==0:G_[4][x]=ST;G_[H-5][x]=ST
    for y in range(5,H-5):
        if (y//2)%2==0:G_[y][4]=ST;G_[y][W-5]=ST
    F=['GGg','G..','g..']
    for sx,sy in ((1,1),(-1,1),(1,-1),(-1,-1)):
        ox=3 if sx>0 else W-4;oy=3 if sy>0 else H-4
        for j,row in enumerate(F):
            for i,ch in enumerate(row):
                if ch!='.':G_[oy+j*sy][ox+i*sx]={'G':G1,'g':G0}[ch]
        G_[oy+sy*2][ox+sx*2]=G2
    for (x,y) in ((W//2-1,2),(W//2,2),(W//2-1,H-3),(W//2,H-3)):G_[y][x]=G2
    for (x,y) in ((2,H//2-1),(2,H//2),(W-3,H//2-1),(W-3,H//2)):G_[y][x]=G2
def vrib(G_,y0,y1,tail=False):
    for y in range(y0,y1):
        for i,c in enumerate((G0,G,G1,G0)):
            x=18+i
            if tail and y>=y1-2 and i in (1,2):continue
            if tail and y==y1-1 and i in (0,3):continue
            G_[y][x]=c
        if y%5==0 and not (tail and y>=y1-2):G_[y][20]=G2
def hrib(G_,yc):
    for x in range(3,W-3):
        for i,c in enumerate((G0,G,G1,G0)):G_[yc-2+i][x]=c
        if x%5==0:G_[yc][x]=G2
def seal(G_,x0,y0):
    for j,row in enumerate(SEAL):
        for i,ch in enumerate(row):
            if ch!='.':
                yy,xx=y0+j+1,x0+i+1
                if 0<=yy<H and 0<=xx<W and G_[yy][xx] not in (G0,G,G1,G2):G_[yy][xx]=EDGE if (i+j)%2 else L0
    put(G_,SEAL,SP,x0,y0)
    for (dx,dy) in ((5,6),(6,5),(4,7)):G_[y0+dy][x0+dx]='#F08A90'
def P():
    G_=blank(L);leather(G_,random.Random(3),range(0,H));frame(G_);vrib(G_,3,H-3);hrib(G_,27);seal(G_,8,16);return G_
def T():
    G_=blank(L);leather(G_,random.Random(5),range(0,30));frame(G_);vrib(G_,3,31,tail=True);seal(G_,8,4);return G_
BACKS={'P':P(),'T':T()}
if __name__=='__main__':
    here=os.path.dirname(os.path.abspath(__file__))
    for k,v in BACKS.items():
        s=packed(v);open(os.path.join(here,f'cb72{k}.css.txt'),'w').write(s)
        open(os.path.join(here,f'cb72{k}.svg'),'w').write(s.replace('%23','#'))
        print(k,len(s))
