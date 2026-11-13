"""Extend the blue header lines (y+2 and y+7 of the header tile row) up to the title text on the
key-config screen, like the JP original. usage: hdrlines.py enUS|ptBR  (reads/writes Narrator/config_set.bin + config_map.bin)"""
import struct,sys
L=sys.argv[1]
P=L+'/Narrator/'
setb=bytearray(open(P+'config_set.bin','rb').read())
mapw=list(struct.unpack('<1024H',open(P+'config_map.bin','rb').read()))
LINE=0xC
def rd(t):
    b=setb[t*32:t*32+32];a=[[0]*8 for _ in range(8)]
    for y in range(8):
        for x in range(8): a[y][x]=sum(((b[y*2+o]>>(7-x))&1)<<p for p,o in enumerate((0,1,16,17)))
    return a
def wr(t,a):
    b=bytearray(32)
    for y in range(8):
        for x in range(8):
            v=a[y][x]
            for p,o in enumerate((0,1,16,17)):
                if (v>>p)&1: b[y*2+o]|=1<<(7-x)
    setb[t*32:t*32+32]=b
# pass 1: blank cells inside header runs -> line tile 0xEE (full lines on rows 2 and 7)
LT=0xEE
lt=rd(LT);assert all(v==LINE for v in lt[2]) and all(v==LINE for v in lt[7]) and not any(any(r) for i,r in enumerate(lt) if i not in (2,7)),'0xEE is not the pure line tile'
runs=[(r,c0,c1) for r in (5,17) for c0,c1 in ((1,10),(21,30))]
mods={}
for r,s,e in runs:
    if e-s<6: continue
    # find which cells are blank in the run
    for c in range(s,e+1):
        if not mapw[r*32+c]:
            pal=mapw[r*32+s]&0xFC00
            mapw[r*32+c]=pal|LT
    # text columns per cell (use top tile r and bottom tile r+1)
    for c in range(s,e+1):
        top=mapw[r*32+c]&0x3FF;bot=mapw[(r+1)*32+c]&0x3FF
        if top==LT: continue
        a=rd(top);b=rd(bot) if bot else [[0]*8 for _ in range(8)]
        txt=[any(a[y][x] in (3,4) for y in range(8)) or any(b[y][x] in (3,4) for y in range(4)) for x in range(8)]
        key=top
        lo=2 if c==s else 0; hi=6 if c==e else 8
        for yy in (2,7):
            for x in range(lo,hi):
                if a[yy][x]==0 and not txt[x]:
                    mods.setdefault(key,set()).add((yy,x))
for t,pix in mods.items():
    a=rd(t)
    for yy,x in pix: a[yy][x]=LINE
    wr(t,a)
open(P+'config_set.bin','wb').write(setb)
open(P+'config_map.bin','wb').write(struct.pack('<1024H',*mapw))
print(L,'runs',runs,'tiles modified',len(mods))
