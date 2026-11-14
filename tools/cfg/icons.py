#!/usr/bin/env python3
"""Recolour the key-config A/B/X/Y icons so they look like the JP original.
usage: icons.py <lang dir> <lang screenshot of key-config> <JP screenshot of key-config>
Each icon is a 2x2-tile block (cols 1-2 / 21-22, rows 7-14 / 19-26). For every icon pixel the palette index whose
*rendered* colour (measured on the translated screenshot) is closest to the JP screenshot colour is chosen; every icon
instance gets its own 4 tiles appended to config_set.bin (tile count grows; code DMA length must follow)."""
import sys,struct
import numpy as np
from PIL import Image
L,shot,jp=sys.argv[1:4]
R=L+'/Narrator/'
cs=bytearray(open(R+'config_set.bin','rb').read());cm=list(struct.unpack('<1024H',open(R+'config_map.bin','rb').read()))
S=np.array(Image.open(shot).convert('RGB')).astype(int);J=np.array(Image.open(jp).convert('RGB')).astype(int)
def tile(n):
    b=cs[n*32:n*32+32]
    return np.array([[((b[y*2]>>(7-x))&1)|(((b[y*2+1]>>(7-x))&1)<<1)|(((b[16+y*2]>>(7-x))&1)<<2)|(((b[16+y*2+1]>>(7-x))&1)<<3) for x in range(8)] for y in range(8)])
def enc(t):
    o=bytearray(32)
    for y in range(8):
        for p in range(4):
            v=0
            for x in range(8): v|=((int(t[y][x])>>p)&1)<<(7-x)
            o[y*2+(p&1)+(16 if p>1 else 0)]=v
    return bytes(o)
cells=[(r,c) for r in list(range(7,15))+list(range(19,27)) for c in (1,2,21,22)]
# idx -> rendered colour (median over icon pixels of the translated screenshot)
samples={}
for r,c in cells:
    w=cm[r*32+c];t=tile(w&0x3ff)
    for y in range(8):
        for x in range(8):
            v=t[y][x]
            if v: samples.setdefault(v,[]).append(S[r*8+y,c*8+x])
col={v:np.median(np.array(a),0) for v,a in samples.items()}
print('idx colours',{v:tuple(int(k) for k in c) for v,c in sorted(col.items())})
ntiles=len(cs)//32;made=0
for r in range(7,27,2):
    for c0 in (1,21):
        if r in (15,17): continue
        new={}
        for dr in (0,1):
            for dc in (0,1):
                rr,cc=r+dr,c0+dc
                w=cm[rr*32+cc];t=tile(w&0x3ff)
                nt=t.copy()
                for y in range(8):
                    for x in range(8):
                        if t[y][x]==0: continue
                        j=J[rr*8+y,cc*8+x]
                        best=min(col,key=lambda v:((col[v]-j)**2).sum())
                        nt[y][x]=best
                cs+=enc(nt);cm[rr*32+cc]=(w&0xfc00)|ntiles;ntiles+=1;made+=1
print('new tiles',made,'total',ntiles)
assert ntiles<=448
open(R+'config_set.bin','wb').write(cs);open(R+'config_map.bin','wb').write(struct.pack('<1024H',*cm))
print('DMA length = $%X'%(ntiles*32))
