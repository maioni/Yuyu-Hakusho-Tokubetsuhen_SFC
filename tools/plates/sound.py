#!/usr/bin/env python3
"""Fix the sound-settings plates (Mode/Track/Voice/Stereo/Mono) in <lang>/Narrator/square10_set.bin:
full 1 px white border (EN/PT lost the right edge) and the label centred in the plate.
Layout (16x16 sprites, sheet 16 tiles wide, VRAM $2000): Mode cols0-3 r0, Track 4-7 r0, Voice 8-11 r0,
Stereo cols12-15 r0 + cols0-1 r2, Mono cols2-7 r2.   usage: sound.py <enUS|ptBR>"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from rank import gt,pt
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PL={'Mode':[(0,0),(1,0),(2,0),(3,0)],'Track':[(4,0),(5,0),(6,0),(7,0)],'Voice':[(8,0),(9,0),(10,0),(11,0)],
    'Stereo':[(12,0),(13,0),(14,0),(15,0),(0,2),(1,2)],'Mono':[(2,2),(3,2),(4,2),(5,2),(6,2),(7,2)]}
def get(s,cells):
    W=len(cells)*8;C=[[0]*W for _ in range(16)]
    for i,(c,r) in enumerate(cells):
        for ty in range(2):
            t=gt(s,(r+ty)*16+c)
            for y in range(8):
                for x in range(8):C[ty*8+y][i*8+x]=t[y][x]
    return C
def put(s,cells,C):
    for i,(c,r) in enumerate(cells):
        for ty in range(2):
            pt(s,(r+ty)*16+c,[[C[ty*8+y][i*8+x] for x in range(8)] for y in range(8)])
def fix(C,dy):
    W=len(C[0]);fill=C[7][1]
    # fill colour = most common interior value
    from collections import Counter
    fill=Counter(C[y][x] for y in range(1,15) for x in range(1,W-1)).most_common(1)[0][0]
    px={(x,y):C[y][x] for y in range(1,15) for x in range(1,W-1) if C[y][x]!=fill}
    xs=[x for x,_ in px];x0,x1=min(xs),max(xs)
    dx=int((1+W-2)/2-(x0+x1)/2+0.5) if False else round(((1+W-2)-(x0+x1))/2-1e-9)
    N=[[2]*W for _ in range(16)]
    for y in range(1,15):
        for x in range(1,W-1):N[y][x]=fill
    for (x,y),v in px.items():N[y+dy][x+dx]=v
    for y in range(16):N[y][0]=N[y][W-1]=2
    return N,(x0,x1,dx)
def main(lang,dy):
    f=os.path.join(ROOT,lang,'Narrator','square10_set.bin');s=bytearray(open(f,'rb').read())
    for n,cells in PL.items():
        C=get(s,cells);N,info=fix(C,dy);put(s,cells,N);print(lang,n,info)
    open(f,'wb').write(s)
if __name__=='__main__':main(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 1)
