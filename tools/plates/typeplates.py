#!/usr/bin/env python3
"""Rebuild the 'Type 1' / 'Type 2' plates in <lang>/Narrator/square05_set.bin.
Frame, background bands and the big digits come from the original JP tiles (tools/plates/square05_set_jp.bin =
VRAM $4000..$47FF of the JP key-config screen); only the kana (x<22) is replaced by the previous
hand-drawn word (pixels of colour 1/2 kept from the existing file, everything else dropped, which removes stray pixels).
Plates live at tile cols 1..4 (Type 1) and 7..10 (Type 2), rows 0..1, in the EN/PT sheet (JP: cols 0..3 / 4..7).
usage: typeplates.py <enUS|ptBR>"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from rank import gt,pt
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(os.path.dirname(HERE))
def comp(s,c0,r0=0):
    C=[[0]*32 for _ in range(16)]
    for ty in range(2):
        for tx in range(4):
            t=gt(s,(r0+ty)*16+c0+tx)
            for y in range(8):
                for x in range(8): C[ty*8+y][tx*8+x]=t[y][x]
    return C
def uncomp(s,c0,C,r0=0):
    for ty in range(2):
        for tx in range(4):
            pt(s,(r0+ty)*16+c0+tx,[[C[ty*8+y][tx*8+x] for x in range(8)] for y in range(8)])
import menus as M
M.bf.YS=0.88
TX={'enUS':'TYPE','ptBR':'TIPO'}
def draw(t,Wd=21,Hd=14):
    """label in the condensed-caps pixel font, centred in the x1..21 / y1..14 area (same font as the other plates)"""
    for (xs,air,gap) in [(0.7,1,1),(0.62,1,1),(0.56,1,1),(0.5,1,1),(0.42,1,1),(0.42,0,0)]:
        M.GAPV=gap;M.bf.XSCAP=xs;M.bf.CAPAIR=air
        if M.layout(t)[1]<=Wd-2:break
    P,w,base=M.layout(t)
    ys=[y for _,y in P];ox=1+(Wd-w)//2;oy=1+(Hd-(max(ys)-min(ys)+1))//2-min(ys)
    return {(ox+x,oy+y) for x,y in P}
def main(lang):
    jp=open(os.path.join(HERE,'square05_set_jp.bin'),'rb').read()
    f=os.path.join(ROOT,lang,'Narrator','square05_set.bin');out=bytearray(open(f,'rb').read())
    for jc,oc,band in ((0,1,{'a':0xa,'9':9,'8':8}),(4,7,{'a':7,'9':6,'8':5})):
        J=comp(jp,jc);O=comp(out,oc)
        N=[row[:] for row in J]
        rows={1:'a',2:'a',3:'9',4:'9',5:'9',6:'8',7:'8',8:'8',9:'8',10:'9',11:'9',12:'9',13:'a',14:'a'}
        for y,k in rows.items():
            for x in range(1,22): N[y][x]=band[k]
        W=draw(TX[lang])
        for (x,y) in W:
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    if (x+dx,y+dy) not in W and 1<=y+dy<15 and 1<=x+dx<22: N[y+dy][x+dx]=1
        for (x,y) in W: N[y][x]=2
        uncomp(out,oc,N)
    open(f,'wb').write(out);print(lang,'ok')
if __name__=='__main__':main(sys.argv[1])
