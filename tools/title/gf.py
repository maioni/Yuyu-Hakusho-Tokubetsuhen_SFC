import sys,struct,numpy as np
sys.path.insert(0,'/tmp/enw')
import titlelib as T
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
R='/home/claude/stoneboat65816/yuyu-hakusho-tokubetsuhen_sfc/'
d=R+'enUS/Opening/'
st=open(d+'title_set.bin','rb').read();mp=open(d+'title_map.bin','rb').read();col=open(d+'title_col.bin','rb').read()
T.st=st;T.ENT=list(struct.unpack('<1024H',mp));T.col=col
img=T.decode();ENT=T.ENT
rows=slice(8,24)
sub=img[rows];ys,xs=np.nonzero(sub)
print('bbox',xs.min(),xs.max(),ys.min()+8,ys.max()+8)
cx=(xs.min()+xs.max())/2; ytop=ys.min()+8; ybot=ys.max()+8
img[rows]=0
SS=8;size=int(sys.argv[1]) if len(sys.argv)>1 else 12
f=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',size*SS)
im=Image.new('L',(256*SS,40*SS),0);dd=ImageDraw.Draw(im)
SP=1*SS
w=sum(dd.textlength(c,font=f)+SP for c in 'Ghost Files')-SP
x=cx*SS-w/2
for c in 'Ghost Files':
    dd.text((x,18*SS),c,font=f,fill=255,anchor='ls');x+=dd.textlength(c,font=f)+SP
a=np.array(im.resize((256,40),Image.BOX))
m=a>120
ys2,xs2=np.nonzero(m);print('glyph bbox',xs2.min(),xs2.max(),ys2.min(),ys2.max())
# place so glyph top-1 (outline) lands at ytop
dy=(ytop+1)-ys2.min()
full=np.zeros((256,256),bool)
full[dy:dy+40-0 if dy+40<=256 else 256,:][:min(40,256-dy)]=m[:min(40,256-dy)]
o=ndimage.binary_dilation(full,structure=np.ones((3,3)))&~full
img[o]=10;img[full]=1
cells=[r*32+c for r in (0,1,2,3) for c in range(32)];cs=set(cells)
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
T.st=bytes(tiles);T.ENT=new;chk=T.decode();print('mismatch',int((chk!=img).sum()),len(tiles)==len(st))
pal=np.array([tuple(((struct.unpack('<H',col[2*i:2*i+2])[0]>>s)&31)*8 for s in (0,5,10)) for i in range(16)],np.uint8)
Image.fromarray(pal[chk]).crop((80,0,176,28)).resize((960,280),Image.NEAREST).save('/tmp/cr/gf2.png')
if len(sys.argv)>2:
    open(d+'title_set.bin','wb').write(bytes(tiles));open(d+'title_map.bin','wb').write(struct.pack('<1024H',*new));print('written')
