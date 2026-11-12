import sys,struct,numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,'/tmp/cr'); from font import render
R='/home/claude/stoneboat65816/yuyu-hakusho-tokubetsuhen_sfc/'
sys.path.insert(0,'/tmp/enw')
import titlelib as T
TXT={'enUS':'V0.9 EN-US 2026 MAIONI / SNIPERDMAA - STONEBOAT 2017-2025',
     'ptBR':'V7.0 PT-BR 2026 MAIONI / SNIPERDMAA - STONEBOAT 2017-2025'}
OUT=sys.argv[1] if len(sys.argv)>1 else '/tmp/cr/out/'
import os
for L in TXT:
    d=R+L+'/Opening/'
    st=open(d+'title_set.bin','rb').read(); mp=open(d+'title_map.bin','rb').read(); col=open(d+'title_col.bin','rb').read()
    T.st=st; T.ENT=list(struct.unpack('<1024H',mp)); T.col=col
    img=T.decode()
    ENT=T.ENT
    img[200:224]=0
    m5=render(TXT[L]); w=m5.shape[1]; x0=(256-w)//2; y0=209
    m=np.zeros((256,256),bool); m[y0:y0+5,x0:x0+w]=m5
    o=ndimage.binary_dilation(m,structure=np.ones((3,3)))&~m
    img[o]=2; img[m]=14
    cells=[r*32+c for r in (25,26,27) for c in range(32)]
    cs=set(cells)
    outside=set(e&0x3ff for i,e in enumerate(ENT) if i not in cs and (e&0x3ff))
    new=list(ENT); tiles=bytearray(st); nt=len(st)//32
    pool=[t for t in range(1,nt) if t not in outside]
    pi=0; asg={}
    for i in cells:
        y,x=divmod(i,32); a=img[y*8:y*8+8,x*8:x*8+8]
        if not a.any(): new[i]=0; continue
        e=T.enc4(a)
        if e in asg: new[i]=asg[e]; continue
        if pi<len(pool): tid=pool[pi]; pi+=1
        else: tid=len(tiles)//32
        if tid*32+32>len(tiles): tiles.extend(b'\0'*(tid*32+32-len(tiles)))
        tiles[tid*32:tid*32+32]=e; asg[e]=tid; new[i]=tid
    print(L,'width',w,'tiles',len(tiles)//32)
    assert len(tiles)//32<=496
    T.st=bytes(tiles); T.ENT=new
    chk=T.decode(); print('mismatch',int((chk!=img).sum()))
    os.makedirs(OUT+L,exist_ok=True)
    open(OUT+L+'/title_set.bin','wb').write(bytes(tiles)); open(OUT+L+'/title_map.bin','wb').write(struct.pack('<1024H',*new)); open(OUT+L+'/title_col.bin','wb').write(col)
    pal=np.array([tuple(((struct.unpack('<H',col[2*i:2*i+2])[0]>>s)&31)*8 for s in (0,5,10)) for i in range(16)],np.uint8); rgb=pal[chk]
    rgb[chk==0]=(20,60,40)
    Image.fromarray(rgb).crop((0,184,256,256)).resize((768,216),Image.NEAREST).save(OUT+L+'_prev.png')
