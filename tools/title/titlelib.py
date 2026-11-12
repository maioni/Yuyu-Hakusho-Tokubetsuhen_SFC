import struct,numpy as np
from PIL import Image
G='/tmp/enbuild/gfx/Opening/'
st=open(G+'title_set.bin','rb').read(); mp=open(G+'title_map.bin','rb').read(); col=open(G+'title_col.bin','rb').read()
PAL=[]
for i in range(16):
    v=struct.unpack('<H',col[2*i:2*i+2])[0]; PAL.append(((v&31)*8,((v>>5)&31)*8,((v>>10)&31)*8))
def tile4(d):
    a=np.zeros((8,8),np.uint8)
    for y in range(8):
        b0,b1,b2,b3=d[2*y],d[2*y+1],d[16+2*y],d[16+2*y+1]
        for x in range(8):
            s=7-x; a[y,x]=((b0>>s)&1)|(((b1>>s)&1)<<1)|(((b2>>s)&1)<<2)|(((b3>>s)&1)<<3)
    return a
def enc4(a):
    o=bytearray(32)
    for y in range(8):
        for x in range(8):
            v=int(a[y,x]); s=7-x
            o[2*y]|=(v&1)<<s; o[2*y+1]|=((v>>1)&1)<<s; o[16+2*y]|=((v>>2)&1)<<s; o[16+2*y+1]|=((v>>3)&1)<<s
    return bytes(o)
ENT=list(struct.unpack('<1024H',mp))
def decode():
    img=np.zeros((256,256),np.uint8)
    for i,e in enumerate(ENT):
        t=tile4(st[(e&0x3ff)*32:(e&0x3ff)*32+32])
        if e&0x4000: t=t[:,::-1]
        if e&0x8000: t=t[::-1]
        y,x=divmod(i,32); img[y*8:y*8+8,x*8:x*8+8]=t
    return img
def rgb(img): return np.array(PAL,np.uint8)[img]
