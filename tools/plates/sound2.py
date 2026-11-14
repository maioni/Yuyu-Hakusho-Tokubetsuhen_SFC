#!/usr/bin/env python3
"""Sound-settings plates (Mode/Track/Voice/Stereo/Mono) in <lang>/Narrator/square10_set.bin, rebuilt from scratch:
empty plate (1 px white border, flat fill colour of the plate) + label drawn with the condensed-caps pixel font
(white, 1 px dark outline), centred.  usage: sound2.py <enUS|ptBR> [preview.png]"""
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
import menus as M, sound as S
from rank import gt,pt
ROOT=M.ROOT
FILL={'Mode':5,'Track':6,'Voice':7,'Stereo':8,'Mono':9}
TX={'enUS':{'Mode':'MODE','Track':'TRACK','Voice':'VOICE','Stereo':'STEREO','Mono':'MONO'},
    'ptBR':{'Mode':'MODO','Track':'FAIXA','Voice':'VOZ','Stereo':'ESTÉREO','Mono':'MONO'}}
M.bf.YS=0.88
def plate(name,lang):
    W=len(S.PL[name])*8;H=16;f=FILL[name]
    C=[[f]*W for _ in range(H)]
    for x in range(W):C[0][x]=C[H-1][x]=2
    for y in range(H):C[y][0]=C[y][W-1]=2
    t=TX[lang][name]
    for (xs,air,gap) in [(0.7,1,1),(0.62,1,1),(0.56,1,1),(0.5,1,1),(0.42,1,1),(0.42,0,0)]:
        M.GAPV=gap;M.bf.XSCAP=xs;M.bf.CAPAIR=air
        if M.layout(t)[1]<=W-6:break
    P,w,base=M.layout(t)
    ex=max(0,min(W-6-w,len(t)-1))
    if ex:P,w,base=M.layout(t,ex)
    ys=[y for _,y in P];ox=(W-w)//2;oy=1+(H-2-(max(ys)-min(ys)+1))//2-min(ys)
    Sx={(ox+x,oy+y) for x,y in P}
    for (x,y) in Sx:
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                X,Y=x+dx,y+dy
                if (X,Y) not in Sx and 1<=X<W-1 and 1<=Y<H-1:C[Y][X]=1
    for (x,y) in Sx:
        if 1<=x<W-1 and 1<=y<H-1:C[y][x]=2
    return C
def main(lang,prev=None):
    f=os.path.join(ROOT,lang,'Narrator','square10_set.bin');s=bytearray(open(f,'rb').read())
    for n,cells in S.PL.items():
        S.put(s,cells,plate(n,lang))
    open(f,'wb').write(s);print(lang,'sound plates written')
if __name__=='__main__':main(sys.argv[1])
