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
def main(lang):
    jp=open(os.path.join(HERE,'square05_set_jp.bin'),'rb').read()
    f=os.path.join(ROOT,lang,'Narrator','square05_set.bin');out=bytearray(open(f,'rb').read())
    for jc,oc,band in ((0,1,{'a':0xa,'9':9,'8':8}),(4,7,{'a':7,'9':6,'8':5})):
        J=comp(jp,jc);O=comp(out,oc)
        N=[row[:] for row in J]
        rows={1:'a',2:'a',3:'9',4:'9',5:'9',6:'8',7:'8',8:'8',9:'8',10:'9',11:'9',12:'9',13:'a',14:'a'}
        for y,k in rows.items():
            for x in range(1,22): N[y][x]=band[k]
        for y in range(1,15):
            for x in range(1,22):
                if O[y][x] in (1,2): N[y][x]=O[y][x]
        uncomp(out,oc,N)
    open(f,'wb').write(out);print(lang,'ok')
if __name__=='__main__':main(sys.argv[1])
