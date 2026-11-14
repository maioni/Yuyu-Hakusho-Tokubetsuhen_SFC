#!/usr/bin/env python3
"""Shaded A/B/X/Y icons, 2nd pass: the translated 15-colour palette lacked the JP dark yellow (01f2) and dark green (1e00).
1) merge the three near-identical dark greys (idx 9,10,14) into idx 9 (294a) in every tile of config_set;
2) palette idx 10 := 01f2 (dark yellow), idx 14 := 1e00 (dark green);
3) rebuild the 16 icon tiles from the JP VRAM tiles with exact/nearest colour mapping (tiles are rewritten in place, extra ones appended).
usage: icons3.py <lang dir> <jp.vram>"""
import sys,struct
L,vramf=sys.argv[1:3];R=L+'/Narrator/'
JP=[int(x,16) for x in "0000,1908,7fff,6739,4e73,6147,48e5,01f2,02d9,4d02,75a4,1012,1c1d,1824,1e00,3300".split(',')]
cs=bytearray(open(R+'config_set.bin','rb').read());cm=list(struct.unpack('<1024H',open(R+'config_map.bin','rb').read()))
col=list(struct.unpack('<15H',open(R+'config_col.bin','rb').read()))
def dec(b):return [[((b[y*2]>>(7-x))&1)|(((b[y*2+1]>>(7-x))&1)<<1)|(((b[16+y*2]>>(7-x))&1)<<2)|(((b[16+y*2+1]>>(7-x))&1)<<3) for x in range(8)] for y in range(8)]
def enc(t):
    o=bytearray(32)
    for y in range(8):
        for p in range(4):
            v=0
            for x in range(8): v|=((t[y][x]>>p)&1)<<(7-x)
            o[y*2+(p&1)+(16 if p>1 else 0)]=v
    return bytes(o)
icon=lambda i:(i//32 in list(range(7,15))+list(range(19,27))) and (i%32 in (1,2,21,22))
if col[9-1]!=0x294a or True:
    # only apply the palette change once
    if col[10-1]!=0x01f2:
        for n in range(len(cs)//32):
            t=dec(cs[n*32:n*32+32])
            if any(v in (10,14) for r in t for v in r):
                cs[n*32:n*32+32]=enc([[9 if v in (10,14) else v for v in r] for r in t])
        col[9-1]=0x294a;col[10-1]=0x01f2;col[14-1]=0x1e00
rgb=lambda w:tuple(((w>>s)&31)*255//31 for s in (0,5,10))
en=[0]+col
conv={i:min(range(1,16),key=lambda j:sum((a-b)**2 for a,b in zip(rgb(JP[i]),rgb(en[j])))) for i in range(1,16)}
print('conv',conv)
jv=open(vramf,'rb').read();jm=struct.unpack('<1024H',jv[0x3800:0x4000])
def jtile(w):
    t=dec(jv[(w&0x3ff)*32:(w&0x3ff)*32+32])
    if w&0x4000:t=[r[::-1] for r in t]
    if w&0x8000:t=t[::-1]
    return t
owner={}                         # existing tile idx -> bytes assigned this run
n=len(cs)//32;appended=0
for r in list(range(7,15))+list(range(19,27)):
    for c in (1,2,21,22):
        i=r*32+c;e=enc([[conv[v] if v else 0 for v in row] for row in jtile(jm[i])])
        cur=cm[i]&0x3ff
        if cur in owner and owner[cur]!=e:                    # collision: append a new tile
            cs+=e;cm[i]=(cm[i]&0xfc00)|n;n+=1;appended+=1
        else:
            cs[cur*32:cur*32+32]=e;owner[cur]=e
print('tiles',n,'appended',appended,'DMA $%X'%(n*32))
open(R+'config_set.bin','wb').write(cs);open(R+'config_map.bin','wb').write(struct.pack('<1024H',*cm))
open(R+'config_col.bin','wb').write(struct.pack('<15H',*col))
