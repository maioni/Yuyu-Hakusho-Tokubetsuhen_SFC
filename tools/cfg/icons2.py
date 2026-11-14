#!/usr/bin/env python3
"""Restore the original JP key-config A/B/X/Y icon tiles (shaded) in <lang>/Narrator/config_set.bin + config_map.bin.
JP tiles/map come from a VRAM dump of the JP ROM on that screen (vram at $0000 tiles, map at $3800) and its palette 7;
every JP colour is mapped to the nearest colour of the translated config_col.bin palette.
usage: icons2.py <lang dir> <jp.vram> <jp palette words, 16 hex comma separated>"""
import sys,struct
L,vramf,pal=sys.argv[1:4]
R=L+'/Narrator/'
jv=open(vramf,'rb').read();jp=[int(x,16) for x in pal.split(',')]
cs=bytearray(open(R+'config_set.bin','rb').read());cm=list(struct.unpack('<1024H',open(R+'config_map.bin','rb').read()))
col=open(R+'config_col.bin','rb').read();en=[0]+list(struct.unpack('<15H',col))
rgb=lambda w:tuple(((w>>s)&31)*255//31 for s in (0,5,10))
conv={}
for i in range(1,16):
    c=rgb(jp[i]);conv[i]=min(range(1,16),key=lambda j:sum((a-b)**2 for a,b in zip(c,rgb(en[j]))))
print('idx map',conv)
jm=struct.unpack('<1024H',jv[0x3800:0x4000])
def jtile(n):
    b=jv[n*32:n*32+32]
    return [[((b[y*2]>>(7-x))&1)|(((b[y*2+1]>>(7-x))&1)<<1)|(((b[16+y*2]>>(7-x))&1)<<2)|(((b[16+y*2+1]>>(7-x))&1)<<3) for x in range(8)] for y in range(8)]
def enc(t):
    o=bytearray(32)
    for y in range(8):
        for p in range(4):
            v=0
            for x in range(8): v|=((t[y][x]>>p)&1)<<(7-x)
            o[y*2+(p&1)+(16 if p>1 else 0)]=v
    return bytes(o)
have={bytes(cs[i*32:i*32+32]):i for i in range(len(cs)//32)}
n=len(cs)//32;added=0
for r in list(range(7,15))+list(range(19,27)):
    for c in (1,2,21,22):
        w=jm[r*32+c]
        # JP map uses the same cell layout; icon cells only
        t=jtile(w&0x3ff)
        if w&0x4000: t=[row[::-1] for row in t]
        if w&0x8000: t=t[::-1]
        nt=[[conv[v] if v else 0 for v in row] for row in t]
        e=enc(nt)
        if e not in have:
            cs+=e;have[e]=n;n+=1;added+=1
        cm[r*32+c]=(cm[r*32+c]&0xfc00)|have[e]
print('added',added,'tiles',n,'DMA $%X'%(n*32));assert n<=448
open(R+'config_set.bin','wb').write(cs);open(R+'config_map.bin','wb').write(struct.pack('<1024H',*cm))
