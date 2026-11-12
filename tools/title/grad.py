import sys,struct,numpy as np
sys.path.insert(0,'/tmp/enw')
import titlelib as T
from PIL import Image
R='/home/claude/stoneboat65816/yuyu-hakusho-tokubetsuhen_sfc/'
d=R+'enUS/Opening/'
st=open(d+'title_set.bin','rb').read();mp=open(d+'title_map.bin','rb').read();col=open(d+'title_col.bin','rb').read()
T.st=st;T.ENT=list(struct.unpack('<1024H',mp));T.col=col
img=T.decode();ENT=T.ENT
M={104:1,105:1,106:12,107:12,108:11,109:11,110:15,111:13,112:13}
FILL={1,11,12,13,15}
n=0
for y,v in M.items():
    for x in range(56,199):
        if img[y,x] in FILL and img[y,x]!=v: img[y,x]=v;n+=1
print('changed',n)
cells=[r*32+c for r in (12,13,14) for c in range(32)];cs=set(cells)
outside=set(e&0x3ff for i,e in enumerate(ENT) if i not in cs and (e&0x3ff))
new=list(ENT);tiles=bytearray(st);nt=len(st)//32
pool=[t for t in range(1,nt) if t not in outside];pi=0;asg={}
for i in cells:
    y,x=divmod(i,32);t=img[y*8:y*8+8,x*8:x*8+8]
    if not t.any(): new[i]=0;continue
    e=T.enc4(t)
    if e in asg:new[i]=asg[e];continue
    if pi<len(pool):tid=pool[pi];pi+=1
    else:tid=len(tiles)//32
    if tid*32+32>len(tiles):tiles.extend(b'\0'*(tid*32+32-len(tiles)))
    tiles[tid*32:tid*32+32]=e;asg[e]=tid;new[i]=tid
assert len(tiles)//32<=496
T.st=bytes(tiles);T.ENT=new;chk=T.decode();print('mismatch',int((chk!=img).sum()),len(tiles)//32, len(tiles)==len(st))
open(d+'title_set.bin','wb').write(bytes(tiles));open(d+'title_map.bin','wb').write(struct.pack('<1024H',*new))
pal=np.array([tuple(((struct.unpack('<H',col[2*i:2*i+2])[0]>>s)&31)*8 for s in (0,5,10)) for i in range(16)],np.uint8)
Image.fromarray(pal[chk]).crop((40,90,216,130)).resize((704,160),Image.NEAREST).save('/tmp/cr/se_new.png')
