#!/usr/bin/env python3
"""The game overwrites BG tile $5F (VRAM $0BE0) on the key-config screen (original JP leaves it unused).
Move any use of tile $5F in config_set/config_map to a new tile appended at the end (idx = count).
usage: fix5f.py <enUS|ptBR>   (then DMA length in code.asm must be count*32)"""
import sys,os,struct
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L=sys.argv[1];d=ROOT+'/'+L+'/Narrator/'
cs=bytearray(open(d+'config_set.bin','rb').read());m=bytearray(open(d+'config_map.bin','rb').read())
n=len(cs)//32;refs=0;new=n
for i in range(len(m)//2):
    w=struct.unpack_from('<H',m,i*2)[0]
    if (w&0x3ff)==0x5f:
        struct.pack_into('<H',m,i*2,(w&~0x3ff)|new);refs+=1
if refs:
    cs+=cs[0x5f*32:0x5f*32+32]
    open(d+'config_set.bin','wb').write(cs);open(d+'config_map.bin','wb').write(m)
print(L,'refs',refs,'tiles now',len(cs)//32,hex(len(cs)))
