import pickle, numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'/tmp/emu')
import lzp
GN,GT=pickle.load(open('/tmp/bt/fonts2.pkl','rb'))
def _g(rows,w):
    a=np.zeros((16,w),bool)
    for r,s in rows:
        for c,ch in enumerate(s): a[r,c]=ch=='#'
    return a
GT['í']=_g([(6,'.#'),(7,'#.'),(9,'#.'),(10,'#.'),(11,'#.'),(12,'#.')],2)
GT['p']=_g([(8,'###.'),(9,'#..#'),(10,'#..#'),(11,'#..#'),(12,'###.'),(13,'#...')],4)
GT['g']=_g([(8,'.###'),(9,'#..#'),(10,'#..#'),(11,'#..#'),(12,'.###'),(13,'###.')],4)
GT['y']=_g([(8,'#..#'),(9,'#..#'),(10,'#..#'),(11,'.###'),(12,'...#'),(13,'###.')],4)
GT['q']=_g([(8,'.###'),(9,'#..#'),(10,'#..#'),(11,'#..#'),(12,'.###'),(13,'...#')],4)
GT['P']=_g([(6,'####.'),(7,'#...#'),(8,'#...#'),(9,'####.'),(10,'#....'),(11,'#....'),(12,'#....')],5)
FP='/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
def kan(ch):
    F=ImageFont.truetype(FP,8); m=Image.new('L',(16,16),0); d=ImageDraw.Draw(m); d.fontmode='1'; d.text((2,2),ch,font=F,fill=255)
    bb=m.getbbox(); return np.array(m.crop((bb[0],bb[1],bb[2],bb[1]+8)))>0
REI=["########","#.#..#.#",".######.",".#.##.#.",".######.",".######.","########"]
K={'体':kan('体'),'力':kan('力'),'気':kan('気'),'霊':np.array([[c=='#' for c in r] for r in REI])}
def word(t):
    cols=[]
    for ch in t:
        if ch==' ': cols.append(np.zeros((16,3),bool)); continue
        cols.append(GT[ch]); cols.append(np.zeros((16,1),bool))
    return np.hstack(cols[:-1])
def line(tr,W=256,gg=4,gb=12):
    L=np.zeros((8,W),np.uint8)
    groups=[(tr[0],'体力','Tairyoku',1),(tr[1],'気','Touki',2),(tr[2],'霊','Reiryoku',3)]
    def gw(g): return word(g[0]).shape[1]+gg+sum(K[k].shape[1] for k in g[1])+(len(g[1])-1)+gg+word(g[2]).shape[1]
    tot=sum(gw(g) for g in groups)+gb*2
    x=(W-tot)//2
    def put_word(t,x,c):
        g=word(t)
        for r in range(6,14):      # GT rows 6..13 -> tile rows 0..7
            for cc in range(g.shape[1]):
                if g[r,cc]: L[r-6,x+cc]=c
        return g.shape[1]
    for t,k,o,c in groups:
        x+=put_word(t,x,c)+gg
        for j,ch in enumerate(k):
            g=K[ch]
            for r in range(g.shape[0]):
                for cc in range(g.shape[1]):
                    if g[r,cc]: L[r,x+cc]=c
            x+=g.shape[1]+(1 if j<len(k)-1 else 0)
        x+=gg
        x+=put_word(o,x,c)+gb
    return L,tot
def tile_bytes(px):  # px 8x8 indices 0..15
    out=bytearray(32)
    for r in range(8):
        for p in range(4):
            b=0
            for c in range(8): b|=((int(px[r,c])>>p)&1)<<(7-c)
            out[ (p//2)*16 + r*2 + (p%2) ]=b
    return bytes(out)
