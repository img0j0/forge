# The card back you tap to turn a Forgeling over (0.48.3, Hunter picked option 3, "Leather journal", on November 1, 2026):
# stitched leather, a gold ribbon, and the seal mark in pixels. Draws a 40 x 56 pixel grid; packed() is the CSS-ready SVG.
import math
W,H=40,56
def blank(c): return [[c]*W for _ in range(H)]
def seal_px(n=23):
    c=(n-1)/2; g=[['.']*n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            dx,dy=x-c,y-c; d=math.hypot(dx,dy); a=math.degrees(math.atan2(dy,dx))%360
            R=10.8+0.6*math.sin(math.radians(a)*5+1)+0.35*math.sin(math.radians(a)*9)
            if d>R: continue
            ch='R'
            if 8.2<=d<9.3: ch='r'
            if d>R-1.1 and 10<a<120: ch='D'
            if R-1.9<d<=R-0.6 and 200<a<265: ch='H'
            g[y][x]=ch
    E=[".....C.....","....CC.....","....CCC.C..","...CCCCCC..","...CCRCCC..","...CRRRCC..","...CCRRCC..","....CCCC...","...........","CCC.....CCC","CCCCC.CCCCC","CCCCCDCCCCC",".CCCCDCCCC."]
    for j,row in enumerate(E):
        for i,ch in enumerate(row):
            if ch!='.': g[4+j][6+i]=ch
    return g
SEAL=seal_px()
SP={'R':'#B3283A','r':'#8A1C2C','D':'#7A1626','H':'#D8505F','C':'#F6DCC8'}
def put(G,grid,pal,x0,y0):
    for j,row in enumerate(grid):
        for i,ch in enumerate(row):
            if ch!='.' and 0<=y0+j<H and 0<=x0+i<W: G[y0+j][x0+i]=pal[ch]
def frame(G,edge,dash,corner):
    for y in range(H):
        for x in range(W):
            if x<2 or y<2 or x>=W-2 or y>=H-2: G[y][x]=edge
    for x in range(3,W-3):
        if (x//2)%2==0: G[3][x]=dash; G[H-4][x]=dash
    for y in range(3,H-3):
        if (y//2)%2==0: G[y][3]=dash; G[y][W-4]=dash
    for (x,y) in [(3,3),(W-4,3),(3,H-4),(W-4,H-4)]: G[y][x]=corner
def plus(G,col,bg):
    for cy in range(8,H-6,6):
        for cx in range(7+(3 if (cy//6)%2 else 0),W-5,6):
            for (dx,dy) in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                if G[cy+dy][cx+dx]==bg: G[cy+dy][cx+dx]=col
def halo(G,col,bg,r=13.5):
    for y in range(H):
        for x in range(W):
            if math.hypot(x-19,(y-27)*1.0)<r and G[y][x] in bg: G[y][x]=col
def svg(G):
    out=[]
    for y,row in enumerate(G):
        x=0
        while x<W:
            c=row[x]; s=x
            while x<W and row[x]==c: x+=1
            out.append(f"<rect x='{s}' y='{y}' width='{x-s}' height='1' fill='{c}'/>")
    return "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 56' shape-rendering='crispEdges' preserveAspectRatio='none'>"+''.join(out)+"</svg>"
def purple():
    bg='#4C3D90'; G=blank(bg); plus(G,'#5E4796',bg); halo(G,'#57468F',[bg,'#5E4796']); frame(G,'#2A2160','#E9B949','#FFF1C9'); put(G,SEAL,SP,8,16); return G
def amber():
    bg='#E39A45'; G=blank(bg); plus(G,'#EDB060',bg); halo(G,'#F2BE6C',[bg,'#EDB060']); frame(G,'#8A4A1A','#FFF1C9','#FFFFFF'); put(G,SEAL,SP,8,16); return G
def leather():
    bg='#5A2C2A'; G=blank(bg)
    for y in range(H):
        for x in range(W):
            if (x*7+y*13)%11==0: G[y][x]='#62322F'
    for y in range(2,H-2):
        for x in (18,19,20,21): G[y][x]='#E0A82E' if x in (19,20) else '#B9851E'
    frame(G,'#2E1614','#C9A15A','#E9C77A'); put(G,SEAL,SP,8,16); return G
def night():
    bg='#2E2758'; G=blank(bg)
    import random; R=random.Random(4)
    for _ in range(26):
        x,y=R.randrange(5,W-5),R.randrange(5,H-5)
        G[y][x]=R.choice(['#6B5FB0','#8C80D0','#FFD36B'])
    halo(G,'#3A3170',[bg,'#6B5FB0','#8C80D0'],14.5); halo(G,'#463C82',[ '#3A3170'],12)
    frame(G,'#1A1536','#E9B949','#FFF1C9'); put(G,SEAL,SP,8,16); return G
BACKS={'purple':purple(),'amber':amber(),'leather':leather(),'night':night()}
SVGS={k:svg(v) for k,v in BACKS.items()}

def packed(G):
    by={}
    for y,row in enumerate(G):
        x=0
        while x<W:
            c=row[x]; s0=x
            while x<W and row[x]==c: x+=1
            by.setdefault(c,[]).append(f"M{s0} {y}h{x-s0}v1h-{x-s0}z")
    bg=max(by,key=lambda c:len(by[c]))
    body=''.join(f"<path fill='{c}' d='{''.join(v)}'/>" for c,v in by.items() if c!=bg)
    svg=f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 56' shape-rendering='crispEdges' preserveAspectRatio='none'><rect width='40' height='56' fill='{bg}'/>{body}</svg>"
    return svg.replace('#','%23')
if __name__=='__main__':
    print(len(packed(BACKS['leather'])))
