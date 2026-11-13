#!/usr/bin/env python3
"""Redraw the PT-BR 'Livre' plate (ptBR/Narrator/square01_set.bin) as 'Combate Livre'.
Plate tiles are 16x16 blocks at TN (see composite()). Colour 1 = dark outline, 2 = white, 3 = plate grey."""
import sys
def load(f): return bytearray(open(f,'rb').read())
def gt(s,n):
    off=n*32;t=[[0]*8 for _ in range(8)]
    for y in range(8):
        b=[s[off+y*2],s[off+y*2+1],s[off+16+y*2],s[off+16+y*2+1]]
        for x in range(8): t[y][x]=sum(((b[p]>>(7-x))&1)<<p for p in range(4))
    return t
def pt(s,n,t):
    off=n*32
    for y in range(8):
        b=[0,0,0,0]
        for x in range(8):
            for p in range(4): b[p]|=((t[y][x]>>p)&1)<<(7-x)
        s[off+y*2],s[off+y*2+1],s[off+16+y*2],s[off+16+y*2+1]=b
TN=[72,74,76,78,104,106]
def comp(s):
    C=[[0]*96 for _ in range(16)]
    for si,tn in enumerate(TN):
        for dy in range(2):
            for dx in range(2):
                t=gt(s,tn+dy*16+dx)
                for y in range(8):
                    for x in range(8): C[dy*8+y][si*16+dx*8+x]=t[y][x]
    return C
def uncomp(s,C):
    for si,tn in enumerate(TN):
        for dy in range(2):
            for dx in range(2):
                pt(s,tn+dy*16+dx,[[C[dy*8+y][si*16+dx*8+x] for x in range(8)] for y in range(8)])
# glyphs: rows listed top->bottom, 'O' = white. Caps are 7 rows (0..6), lower case x-height 5 (rows 2..6)
G={
'C':[".OOO.","O...O","O....","O....","O....","O...O",".OOO."],
'L':["O...","O...","O...","O...","O...","O...","OOOO"],
'o':[None,None,".OO.","O..O","O..O","O..O",".OO."],
'm':[None,None,"OOOO.","O.O.O","O.O.O","O.O.O","O.O.O"],
'b':["O...","O...","OOO.","O..O","O..O","O..O","OOO."],
'a':[None,None,".OO.","...O",".OOO","O..O",".OOO"],
't':[None,".O.","OOO",".O.",".O.",".O.",".OO"],
'e':[None,None,".OO.","O..O","OOOO","O...",".OOO"],
'i':["O",None,"O","O","O","O","O"],
'v':[None,None,"O.O","O.O","O.O","O.O",".O."],
'r':[None,None,"OOO","O..","O..","O..","O.."],
}
def layout(text,gap=1,space=3):
    cols=[];x=0
    for ch in text:
        if ch==' ': x+=space;continue
        g=G[ch];w=max(len(r) for r in g if r)
        cols.append((x,g,w)); x+=w+gap
    return cols,x-gap
def main(f):
    s=load(f);C=comp(s)
    # clear old text (colours 1/2) in x 30..66, rows 0..8
    for y in range(0,9):
        for x in range(30,66):
            if C[y][x] in (1,2): C[y][x]=3
    cols,W=layout("Combate Livre")
    x0=10+(80-(W+2))//2+1          # centre in grey bar (x 10..89), +1 for outline
    y0=1                            # caps rows 1..7, outline rows 0 and 8
    white=set()
    for x,g,w in cols:
        for r,row in enumerate(g):
            if not row: continue
            for c,ch in enumerate(row):
                if ch=='O': white.add((x0+x+c,y0+r))
    for (x,y) in white:
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if (x+dx,y+dy) not in white and 0<=y+dy<16: C[y+dy][x+dx]=1
    for (x,y) in white: C[y][x]=2
    uncomp(s,C);open(f,'wb').write(s)
    print('text width',W,'x0',x0)
main(sys.argv[1])
