#!/usr/bin/env python3
"""Rebuild <lang>/Narrator/rank_set.bin (computer-level plates S/A/B) from the original JP tiles
(tools/plates/rank_set_jp.bin = VRAM $6000..$67FF of the JP game) and replace the kanji tab with a
narrow tab of the same style, so the letters' legs are not covered (the old wide band cut the 'A').
usage: rank.py <enUS|ptBR> [text]   (default text: Rank for enUS, Nivel for ptBR)"""
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(os.path.dirname(HERE))
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
def comp(s,c0,r0):
    C=[[0]*32 for _ in range(16)]
    for ty in range(2):
        for tx in range(4):
            t=gt(s,(r0+ty)*16+c0+tx)
            for y in range(8):
                for x in range(8): C[ty*8+y][tx*8+x]=t[y][x]
    return C
def uncomp(s,c0,r0,C):
    for ty in range(2):
        for tx in range(4):
            pt(s,(r0+ty)*16+c0+tx,[[C[ty*8+y][tx*8+x] for x in range(8)] for y in range(8)])
# 3-wide pixel font, caps 5 rows, lowercase 4 rows (rows 1..4), accent in row 0
F={
'R':["OO.","O.O","OO.","O.O","O.O"],
'N':["O.O","OOO","OOO","O.O","O.O"],
'a':[None,".OO","O.O","O.O",".OO"],
'n':[None,"OO.","O.O","O.O","O.O"],
'k':["O..","O..","O.O","OO.","O.O"],
'e':[None,".OO","OOO","O..",".OO"],
'v':[None,"O.O","O.O","O.O",".O."],
'l':["O","O","O","O","O"],
'i':[None,"O","O","O","O"],
'í':[".O","O.","O.","O.","O."],
}
def text_cols(txt):
    out=[];x=0
    for ch in txt:
        g=F[ch];w=max(len(r) for r in g if r);out.append((x,g));x+=w+1
    return out,x-1
def tab(C,txt):
    cols,W=text_cols(txt)
    wi=max(16,W+1)                      # interior width
    xl=int(15.5-wi/2.0+0.5)-1           # left border column; interior xl+1..xl+wi (centred on x=15.5)
    xl=max(xl,4)
    xr=xl+wi
    for y in range(5,16):
        for x in range(xl,xr+2):
            C[y][x]=0
    for x in range(xl+1,xr+1): C[5][x]=0xd
    for y in range(6,14):
        C[y][xl]=0xe
        for x in range(xl+1,xr+1): C[y][x]=0xe
    C[6][xl]=0xd
    for x in range(xl,xr+2): C[14][x]=0xe; C[15][x]=1
    C[12][xr+1]=0xd
    x0=xl+1+(wi-W)//2;y0=7
    for x,g in cols:
        for r,row in enumerate(g):
            if not row: continue
            for c,ch in enumerate(row):
                if ch=='O': C[y0+r][x0+x+c]=2
    return xl,xr
def main(lang,txt):
    jp=bytearray(open(os.path.join(HERE,'rank_set_jp.bin'),'rb').read())
    f=os.path.join(ROOT,lang,'Narrator','rank_set.bin')
    out=bytearray(open(f,'rb').read())
    for c0,r0 in ((4,0),(12,0),(4,2)):
        C=comp(jp,c0,r0)
        tab(C,txt)
        uncomp(out,c0,r0,C)
    open(f,'wb').write(out);print(lang,txt,'ok')
if __name__=='__main__':
    lang=sys.argv[1];main(lang,sys.argv[2] if len(sys.argv)>2 else ('Rank' if lang=='enUS' else 'Nível'))
