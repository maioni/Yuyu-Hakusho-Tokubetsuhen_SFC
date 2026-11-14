#!/usr/bin/env python3
"""Team-order screen: the First/Mid/Last (Ponta/Meio/Fim) boxes (Narrator/preset2.bin, 32x16 sprites) and the Cancel portrait
(Narrator/square13_set.bin, 32x32 sprite cell used twice).  Condensed-caps pixel font, tall like the Japanese kanji.
The Cancel cell: the original hides part of the character behind the label; the hidden rows (20..28) are repainted
(hair on the sides, pale-pink dress in the middle) and the label is drawn over it with a dark outline.
usage: order.py <enUS|ptBR>"""
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
import menus as M
from rank import gt,pt
from PIL import Image
ROOT=M.ROOT
TX={'enUS':{'First':'FIRST','Mid':'MID','Last':'LAST','Cancel':'CANCEL'},'ptBR':{'First':'PONTA','Mid':'MEIO','Last':'FIM','Cancel':'CANCELAR'}}
BOX={'First':([32,33,34,35],[48,49,50,51]),'Mid':([36,37,38,39],[52,53,54,55]),'Last':([40,41,42,43],[56,57,58,59])}
CAN=[[72,73,74,75],[88,89,90,91],[76,77,78,79],[92,93,94,95]]
def label(t,W,y0,y1,out,fg,maxw,ys=0.88):
    """pixel set of the label (+outline) fitted in width maxw, vertically centred in rows y0..y1"""
    M.bf.YS=ys
    for (xs,air,gap) in [(0.7,1,1),(0.62,1,1),(0.56,1,1),(0.5,1,1),(0.42,1,1),(0.5,0,1),(0.42,0,1),(0.42,0,0),(0.35,0,0),(0.3,0,0)]:
        M.GAPV=gap;M.bf.XSCAP=xs;M.bf.CAPAIR=air
        if M.layout(t)[1]<=maxw:break
    P,w,base=M.layout(t)
    ex=max(0,min(maxw-w,len(t)-1))
    if ex:P,w,base=M.layout(t,ex)
    ysx=[y for _,y in P];h=max(ysx)-min(ysx)+1
    ox=(W-w)//2;oy=y0+(y1-y0+1-h)//2-min(ysx)
    S={(ox+x,oy+y) for x,y in P}
    return S
TINY={'C':['XXX','X..','X..','X..','X..','X..','XXX'],'A':['.X.','X.X','X.X','XXX','X.X','X.X','X.X'],
      'N':['X.X','XXX','XXX','XXX','XXX','X.X','X.X'],'E':['XXX','X..','X..','XX.','X..','X..','XXX'],
      'L':['X..','X..','X..','X..','X..','X..','XXX'],'R':['XX.','X.X','X.X','XX.','X.X','X.X','X.X']}
def tiny(t):
    """3x7 caps, 1 px gap (none between L and A), returns pixel set from (0,0) and width"""
    S=set();x=0;prev=None
    for ch in t:
        if prev is not None and not (prev=='L' and ch=='A'):x+=1
        for y,row in enumerate(TINY[ch]):
            for dx,c in enumerate(row):
                if c=='X':S.add((x+dx,y))
        x+=3;prev=ch
    return S,x
def box(name,lang):
    W,H=32,16;C=[[0]*W for _ in range(H)]
    grad={1:7,2:5,3:5,4:5,5:5,6:6,7:6,8:6,9:6,10:7,11:7,12:7,13:7,14:7}
    for y in range(H):
        for x in range(W):
            if y==0:C[y][x]=2 if x==0 else 8
            elif y==H-1:C[y][x]=8 if x==0 else 9
            elif x==0:C[y][x]=8
            elif x==W-1:C[y][x]=9
            else:C[y][x]=grad[y]
    S=label(TX[lang][name],W,1,14,1,2,W-6)
    for (x,y) in S:
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                X,Y=x+dx,y+dy
                if (X,Y) not in S and 1<=X<W-1 and 1<=Y<H-1:C[Y][X]=1
    for (x,y) in S:
        if 1<=x<W-1 and 1<=y<H-1:C[y][x]=2
    return C
def jpcell():
    """cell pixels as the Japanese game shows them (from ref/jp_cancel.bin: 32x32 palette indices)"""
    d=open(os.path.join(M.REF,'jp_cancel.txt')).read().split()
    return [[int(c,16) for c in r] for r in d]
def cellpal():
    """sprite palette of the Cancel cell: idx -> rgb, measured from ref/jp_order.png (JP screenshot) and the idx map ref/jp_cancel.txt"""
    from collections import Counter
    im=Image.open(os.path.join(M.REF,'jp_order.png')).convert('RGB');J=jpcell();cnt={}
    for y in range(32):
        for x in range(32):
            cnt.setdefault(J[y][x],Counter())[im.getpixel((64+x,160+y))]+=1
    return {i:c.most_common(1)[0][0] for i,c in cnt.items() if i!=0}
def refcell():
    im=Image.open(os.path.join(M.REF,'27_ordem_equipe_sem_texto.png')).convert('RGB')
    P=cellpal();R=[[0]*32 for _ in range(32)]
    for y in range(32):
        for x in range(32):
            px=[im.getpixel((256+4*x+i,640+4*y+j)) for i in range(4) for j in range(4)]
            c=tuple(sum(q[k] for q in px)//16 for k in range(3))
            R[y][x]=min(P,key=lambda i:sum((a-b)**2 for a,b in zip(P[i],c)))
    from collections import Counter
    for _ in range(2):                    # 3x3 majority filter: the reference is blurry, this removes the speckle
        N=[r[:] for r in R]
        for y in range(1,31):
            for x in range(1,31):
                cn=Counter(R[y+j][x+i] for j in(-1,0,1) for i in(-1,0,1));v,n=cn.most_common(1)[0]
                if n>=4:N[y][x]=v
        R=N
    return R
def cancel(lang):
    s=open(os.path.join(ROOT,lang,'Narrator','square13_set.bin'),'rb').read()
    C=[[0]*32 for _ in range(32)]
    for r,row in enumerate(CAN):
        for c,t in enumerate(row):
            T=gt(s,t)
            for y in range(8):
                for x in range(8):C[r*8+y][c*8+x]=T[y][x]
    # repaint the hidden band (rows 20..28) from the clean reference screen (ref/27_ordem_equipe_sem_texto.png, 4x):
    # 4x4 block average snapped to the cell's sprite palette (colours measured on the game screenshots)
    R=refcell()
    for y in range(20,29):
        for x in range(1,31):C[y][x]=R[y][x]
    if lang=='ptBR':
        S0,w=tiny(TX[lang]['Cancel']);S={(1+(30-w)//2+x,21+y) for x,y in S0}
    else:S=label(TX[lang]['Cancel'],32,21,28,4,4,29,ys=0.62)
    for (x,y) in S:                               # dark outline, then white letters
        for dx,dy in((1,0),(0,1),(1,1),(-1,0),(0,-1),(-1,-1),(1,-1),(-1,1)):
            X,Y=x+dx,y+dy
            if (X,Y) not in S and 1<=X<31 and 1<=Y<31:C[Y][X]=4
    for (x,y) in S:                               # white letters; light-grey (idx 2) shading on the lower edge, like the original
        if 1<=x<31 and 1<=y<31:C[y][x]=2 if ((x,y+1) not in S and (x+y)%2==0) else 1
    return C
def main(lang):
    f=os.path.join(ROOT,lang,'Narrator','preset2.bin');s=bytearray(open(f,'rb').read())
    for n,(a,b) in BOX.items():
        C=box(n,lang)
        for r,row in enumerate((a,b)):
            for c,t in enumerate(row):
                pt(s,t,[[C[r*8+y][c*8+x] for x in range(8)] for y in range(8)])
    open(f,'wb').write(s)
    f=os.path.join(ROOT,lang,'Narrator','square13_set.bin');s=bytearray(open(f,'rb').read())
    C=cancel(lang)
    for r,row in enumerate(CAN):
        for c,t in enumerate(row):
            pt(s,t,[[C[r*8+y][c*8+x] for x in range(8)] for y in range(8)])
    open(f,'wb').write(s);print(lang,'order plates written')
if __name__=='__main__':main(sys.argv[1])
