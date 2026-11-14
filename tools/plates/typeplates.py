#!/usr/bin/env python3
"""Rebuild the 'Type 1' / 'Type 2' plates in <lang>/Narrator/square05_set.bin.
Frame, background bands and the big digit come from the original JP tiles (tools/plates/square05_set_jp.bin =
VRAM $4000..$47FF of the JP key-config screen). The digit is moved 2 px right and the word (EN 'Type', PT 'Tipo', same thin
1 px font, stretched 1.5x vertically) is spread over the free width so the whole group is centred in the box.
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
# 1 px glyphs (from the EN 'Type' plate); (first row, rows) ; row 0 = capital top
GL={'T':(0,["#####","..#..","..#..","..#..","..#..","..#.."]),
    'y':(1,["#..#","#..#","#..#",".###","...#","...#","###."]),
    'p':(1,["###.","#..#","#..#","#..#","###.","#...","#..."]),
    "e":(1,[".##.","#..#","####","#...",".###"]),
    'i':(0,["#",".","#","#","#","#"]),
    'o':(1,[".##.","#..#","#..#","#..#",".##."])}
SCALE=1.5
def stretch(first,rows):
    P=set()
    for r,row in enumerate(rows):
        a=int((first+r)*SCALE);b=int((first+r+1)*SCALE)
        for y in range(a,b):
            for x,ch in enumerate(row):
                if ch=='#':P.add((x,y))
    return P
def main(lang):
    jp=open(os.path.join(HERE,'square05_set_jp.bin'),'rb').read()
    f=os.path.join(ROOT,lang,'Narrator','square05_set.bin');out=bytearray(open(f,'rb').read())
    word='Type' if lang=='enUS' else 'Tipo'
    SH=2                                            # digit shift to the right
    for jc,oc,band in ((0,1,{'a':0xa,'9':9,'8':8}),(4,7,{'a':7,'9':6,'8':5})):
        J=comp(jp,jc);N=[row[:] for row in J]
        rows={1:'a',2:'a',3:'9',4:'9',5:'9',6:'8',7:'8',8:'8',9:'8',10:'9',11:'9',12:'9',13:'a',14:'a'}
        for y,k in rows.items():
            for x in range(1,31): N[y][x]=band[k]
        isband=lambda y,v:v in (band['a'],band['9'],band['8'])
        for y in range(1,15):                         # digit block x 22..27 -> shifted
            for x in range(22,28):
                if not isband(y,J[y][x]): N[y][x+SH]=J[y][x]
        # word: glyphs spread over white x 3..(21+SH-2) with equal gaps
        gl=[GL[c] for c in word];gp=[stretch(*g) for g in gl]
        gw=[max(x for x,_ in p)+1 for p in gp]
        x_start=2;x_end=21
        gap=(x_end-x_start+1-sum(gw))/(len(word)-1)
        x=float(x_start);W=set()
        for p,w in zip(gp,gw):
            for (px,py) in p:W.add((int(round(x))+px,py+3))
            x+=w+gap
        ymin=min(y for _,y in W);ymax=max(y for _,y in W)
        sy=1+(14-1-(ymax-ymin+2))//2+1-ymin          # centre vertically (outline rows inside 1..14)
        W={(x,y+sy) for x,y in W}
        for (x,y) in W:
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    if (x+dx,y+dy) not in W and 1<=y+dy<15 and 1<=x+dx<26: N[y+dy][x+dx]=1
        for (x,y) in W:N[y][x]=2
        uncomp(out,oc,N)
    open(f,'wb').write(out);print(lang,'ok')
if __name__=='__main__':main(sys.argv[1])
