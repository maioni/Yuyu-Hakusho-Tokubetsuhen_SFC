"""Equalize EN/PT title: same copyright block (EN layout) + same PRESS START glyph style (PT glyphs).
usage: python3 equalize.py [outdir]  (reads/writes <repo>/<lang>/Opening/title_*.bin unless outdir given)"""
import sys,struct,numpy as np
R='/home/claude/stoneboat65816/yuyu-hakusho-tokubetsuhen_sfc/'
sys.path.insert(0,R+'tools/title'); import titlelib as T
def load(L):
    d=R+L+'/Opening/'
    st=open(d+'title_set.bin','rb').read(); mp=open(d+'title_map.bin','rb').read()
    T.st=st; T.ENT=list(struct.unpack('<1024H',mp)); img=T.decode(); return st,list(T.ENT),img
def reencode(st,ENT,img,cellrows):
    cells=[r*32+c for r in cellrows for c in range(32)]; cs=set(cells)
    attrs={e>>10 for i,e in enumerate(ENT) if i in cs and (e&0x3ff)}
    print(' attrs in cells',attrs)
    outside=set(e&0x3ff for i,e in enumerate(ENT) if i not in cs and (e&0x3ff))
    new=list(ENT); tiles=bytearray(st); nt=len(st)//32
    pool=[t for t in range(1,nt) if t not in outside]; pi=0; asg={}
    for i in cells:
        y,x=divmod(i,32); a=img[y*8:y*8+8,x*8:x*8+8]
        if not a.any(): new[i]=0; continue
        e=T.enc4(a)
        if e in asg: new[i]=asg[e]; continue
        if pi<len(pool): tid=pool[pi]; pi+=1
        else: tid=len(tiles)//32
        if tid*32+32>len(tiles): tiles.extend(b'\0'*(tid*32+32-len(tiles)))
        tiles[tid*32:tid*32+32]=e; asg[e]=tid; new[i]=tid
    assert len(tiles)//32<=496
    return bytes(tiles),new
en=load('enUS'); pt=load('ptBR')
# PRESS START glyphs from PT
band=slice(229,244)
a=pt[2][band]; nz=(a!=0).any(0); segs=[];s=None
for x in range(256):
    if nz[x] and s is None:s=x
    if not nz[x] and s is not None:segs.append((s,x-1));s=None
assert len(segs)==14
def word(idx): return [a[:,s:e+1] for s,e in (segs[i] for i in idx)]
gap=segs[1][0]-segs[0][1]-1
def compose(glyphs,gaps):
    w=sum(g.shape[1] for g in glyphs)+sum(gaps); out=np.zeros((15,w),np.uint8); x=0
    for k,g in enumerate(glyphs):
        out[:,x:x+g.shape[1]]=np.where(g!=0,g,out[:,x:x+g.shape[1]]); x+=g.shape[1]+(gaps[k] if k<len(gaps) else 0)
    return out
wordgap=segs[9][0]-segs[8][1]-1
gl=word([0,1,2,3,4,9,10,11,12,13])
gaps=[segs[i+1][0]-segs[i][1]-1 for i in range(4)]+[wordgap]+[segs[i+1][0]-segs[i][1]-1 for i in range(9,13)]
ps=compose(gl,gaps); w=ps.shape[1]; print('PRESS START width',w)
# EN: replace PRESS START (rows 224-247)
img=en[2].copy(); img[224:248]=0
x0=int(round(128.5-w/2)); img[229:244,x0:x0+w]=ps
EN_st,EN_map=reencode(en[0],en[1],img,(28,29,30))
# PT: copy EN copyright block (rows 168-199), drop stray dot
img=pt[2].copy(); img[160:208]=0; img[160:208]=en[2][160:208]
# remove stray dot under subtitle
img[20:30,170:190]=0
PT_st,PT_map=reencode(pt[0],pt[1],img,(20,21,22,23,24,25,2,3))
out=sys.argv[1] if len(sys.argv)>1 else None
import os
for L,(s,m) in (('enUS',(EN_st,EN_map)),('ptBR',(PT_st,PT_map))):
    d=(out+'/'+L if out else R+L+'/Opening')+'/'
    os.makedirs(d,exist_ok=True)
    open(d+'title_set.bin','wb').write(s); open(d+'title_map.bin','wb').write(struct.pack('<1024H',*m))
    print(L,len(s)//32,'tiles')
