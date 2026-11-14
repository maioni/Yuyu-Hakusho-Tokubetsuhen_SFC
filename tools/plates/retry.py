#!/usr/bin/env python3
"""Retry screen ("Want to try one more time?"): the Continue / Give Up plates, 48x16 = 3 sprites of 16x16 each, in
<lang>/Narrator/square14_set.bin (16 tiles per row): Continue (78,79,94,95)(96,97,112,113)(98,99,114,115),
Give Up (100,101,116,117)(102,103,118,119)(104,105,120,121).  Plate = border idx 10 (palette makes it yellow when selected),
vertical purple gradient (7,6,5,6,7) and the label in the condensed-caps pixel font (white idx 2, dark outline idx 1).
usage: retry.py <enUS|ptBR>"""
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
import menus as M, order as O
from rank import pt
ROOT=M.ROOT
TX={'enUS':{'cont':'CONTINUE','give':'GIVE UP'},'ptBR':{'cont':'CONTINUAR','give':'DESISTIR'}}
SP={'cont':[(78,79,94,95),(96,97,112,113),(98,99,114,115)],'give':[(100,101,116,117),(102,103,118,119),(104,105,120,121)]}
GR={1:7,2:7,3:6,4:6,5:6,6:5,7:5,8:5,9:5,10:6,11:6,12:6,13:7,14:7}
def plate(name,lang):
    W,H=48,16;C=[[0]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            C[y][x]=10 if (y in(0,H-1) or x in(0,W-1)) else GR[y]
    S=O.label(TX[lang][name],W,1,14,1,2,W-8)
    for (x,y) in S:
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                X,Y=x+dx,y+dy
                if (X,Y) not in S and 1<=X<W-1 and 1<=Y<H-1:C[Y][X]=1
    for (x,y) in S:
        if 1<=x<W-1 and 1<=y<H-1:C[y][x]=2
    return C
def main(lang):
    f=os.path.join(ROOT,lang,'Narrator','square14_set.bin');s=bytearray(open(f,'rb').read())
    for n in SP:
        C=plate(n,lang)
        for k,(a,b,c,d) in enumerate(SP[n]):
            for t,(ox,oy) in zip((a,b,c,d),((0,0),(8,0),(0,8),(8,8))):
                pt(s,t,[[C[oy+y][16*k+ox+x] for x in range(8)] for y in range(8)])
    open(f,'wb').write(s);print(lang,'retry plates written')
if __name__=='__main__':main(sys.argv[1])
