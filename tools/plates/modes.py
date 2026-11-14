#!/usr/bin/env python3
"""Mode plates (Solo / Team / Tournament / Championship): redraw the label strip.
1. the strip is rebuilt from the clean (text-free) reference squares in tools/plates/ref/ (area-averaged to the game's
   pixels and snapped to each plate's real sprite palette, no new colours),
2. the label is drawn on top with the compact variant of the big pixel font (tools/font/bigfont2.py), white with a
   1 px dark outline, centred.
Plates are sprite sheets (square06..09_set.bin, 16 tiles wide); screen pixel (x,y) of a plate maps to tile T[ty][tx]
(measured in the emulator).  usage: modes.py <enUS|ptBR>"""
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0,HERE);sys.path.insert(0,os.path.join(ROOT,'tools','font'))
from rank import gt,pt
from PIL import Image,ImageFilter
import bigfont2 as bf
bf.YS=0.97;bf.XSCAP=0.62;bf.BRUSH2=False;bf.CAPAIR=1
# tile id for each 8x8 cell of the 92x60 plate (12 cols x 8 rows)
T=[list(range(r*16,r*16+12)) for r in range(4)]+[[12,13,14,15,44,45,46,47,64,65,66,67],[28,29,30,31,60,61,62,63,80,81,82,83],list(range(68,80)),list(range(84,96))]
def c15(v):
    r,g,b=v&31,(v>>5)&31,(v>>10)&31;return ((r<<3)|(r>>2),(g<<3)|(g>>2),(b<<3)|(b>>2))
SPAL=[[0x7E9F,0x18A4,0x7FFF,0x6739,0x4E73,0x52FC,0x3E58,0x29B4,0x1D0B,0x3A3E,0x217F,0x08BF,0x61C6,0x2F19,0x2A54,0x02B5],
      [0x7EDF,0x18A4,0x7FFF,0x6739,0x4E73,0x52FC,0x3E58,0x29B4,0x7F4C,0x7241,0x4458,0x2854,0x5BFF,0x2F19,0x2A54,0x0000],
      [0x7EDF,0x18A4,0x7FFF,0x6739,0x4E73,0x52FC,0x3E58,0x29B4,0x6B93,0x56AD,0x356F,0x30A9,0x61C6,0x2F19,0x2A54,0x0000],
      [0x0000,0x18A4,0x7FFF,0x6739,0x4E73,0x52FC,0x3E58,0x29B4,0x1D0B,0x5527,0x48A4,0x0ABF,0x1DFB,0x3719,0x2A54,0x0000]]
# name: (clean square, plate pal, sq file, plate bbox x0,y0 on screen, strip rect (x0,y0,w,h), texts)
PLATES={'solo': ('19_modo_duelo_1v1_sem_texto.png',0,'07',(18,82),(24,125),{'enUS':'SOLO FIGHT','ptBR':'COMBATE SOLO'}),
        'team': ('20_modo_equipes_sem_texto.png',1,'09',(146,82),(152,125),{'enUS':'TEAM FIGHT','ptBR':'EQUIPE'}),
        'tour': ('21_modo_torneio_sem_texto.png',2,'08',(18,82),(24,125),{'enUS':'TOURNAMENT','ptBR':'TORNEIO'}),
        'champ':('22_modo_todos_contra_todos_sem_texto.png',3,'06',(146,82),(152,125),{'enUS':'CHAMPIONSHIP','ptBR':'CAMPEONATO'})}
OUTL=70;SOFT=0;DARK=0
PW,PH,SW,SH=92,60,80,15       # strip window: 2 rows of top bar + 11 interior rows + 2 rows of bottom bar
IN0,IN1=2,12                   # interior rows inside the window
YOFF=2      # measured: tile row Y of the T map shows at screen y = plate y + 80 (not +82)
def strip(fn,pk,jp=None,spos=None):
    im=Image.open(os.path.join(HERE,'ref',fn)).convert('RGB')
    px=im.load();w,h=im.size
    xs=[x for y in range(h) for x in range(w) if min(px[x,y])>200];ys=[y for y in range(h) for x in range(w) if min(px[x,y])>200]
    cx0,cy0,cx1,cy1=min(xs),min(ys),max(xs),max(ys)
    sx=(cx1-cx0)/float(PW-1);sy=(cy1-cy0)/float(PH-1)
    im=im.filter(ImageFilter.MedianFilter(3))
    if SOFT:im=im.filter(ImageFilter.GaussianBlur(SOFT))
    if DARK:im=Image.blend(im,Image.new('RGB',im.size,(33,41,49)),DARK)   # shade the art so the label reads clearly     # soft version of the art behind the label (no hard shapes under the letters)
    ox,oy=6,43      # strip rect origin inside the plate (screen 24,127 / plate 18,82)
    box=(cx0+ox*sx,cy0+oy*sy,cx0+(ox+SW)*sx,cy0+(oy+SH)*sy)
    sm=im.resize((SW,SH),Image.BOX,box=box)
    pal=[c15(v) for v in SPAL[pk]];G=[[0]*SW for _ in range(SH)]
    for y in range(SH):
        for x in range(SW):
            c=sm.getpixel((x,y))
            G[y][x]=min(range(1,15),key=lambda i:sum((a-b)**2 for a,b in zip(pal[i],c)))
    if jp is not None:      # keep the original game's own pixels wherever the Japanese lettering does not cover them
        pj=jp.load();TXT={(255,255,255),(32,40,49),(156,157,156),(205,206,205),(197,149,123)}
        ex={c:i for i,c in enumerate(pal) if i}
        for y in range(SH):
            for x in range(SW):
                c=pj[spos[0]+x,spos[1]+y]
                if c in TXT or c not in ex:continue
                G[y][x]=ex[c]
    return G
def label(G,text,pk):
    P,w=bf.pixels(text)
    x0=(SW-w)//2;y0=IN1+1-(max(y for _,y in P)+1)    # base of the letters on the bottom row of the strip, like the original
    S={(x0+x,y0+y) for x,y in P}
    for (x,y) in S:
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                X,Y=x+dx,y+dy
                if (X,Y) not in S and 0<=X<SW and 0<=Y<SH:
                    r,g,b=c15(SPAL[pk][G[Y][X]]) if G[Y][X] else (0,0,0)
                    if (0.3*r+0.59*g+0.11*b)>OUTL:G[Y][X]=1      # outline only where the art behind is light, so the artwork stays visible
    for (x,y) in S:
        if 0<=x<SW and 0<=y<SH:G[y][x]=2
def fullplate(fn,pk):
    """whole 92x60 plate from the clean reference: exact (nearest) sampling of the 2x image, snapped to the plate's palette"""
    im=Image.open(os.path.join(HERE,'ref',fn)).convert('RGB');px=im.load();w,h=im.size
    xs=[x for y in range(h) for x in range(w) if min(px[x,y])>200];ys=[y for y in range(h) for x in range(w) if min(px[x,y])>200]
    cx0,cy0=min(xs),min(ys)
    pal=[c15(v) for v in SPAL[pk]];F=[]
    for y in range(PH):
        F.append([min(range(1,15),key=lambda i:sum((a-b)**2 for a,b in zip(pal[i],px[cx0+2*x+1,cy0+2*y+1]))) for x in range(PW)])
    return F
XOFF=2      # the clean reference's white frame is at plate x=2 (the game's 2 px highlight ring is outside it)
import json
HL=json.load(open(os.path.join(HERE,'ref','mode_hl15.json')))    # per plate: 64x96 mask of the original's palette-index-15 pixels
def write_full(s,F,pk):
    """F (92x60, from the clean ref) goes to tile space at (XOFF,YOFF); then the original's idx-15 pixels (the yellow
    highlight ring + the strip frame, recoloured by the game when the plate is selected) are restored exactly"""
    TS=[[0]*96 for _ in range(64)]
    for ty,row in enumerate(T):
        for tx,t in enumerate(row):
            g=gt(s,t)
            for y in range(8):
                for x in range(8):TS[ty*8+y][tx*8+x]=g[y][x]
    for y in range(PH):
        for x in range(PW):TS[y+YOFF][x+XOFF]=F[y][x]
    for y in range(64):
        for x in range(96):
            if HL[pk][y][x]=='1':TS[y][x]=15
    for ty,row in enumerate(T):
        for tx,t in enumerate(row):
            pt(s,t,[[TS[ty*8+y][tx*8+x] for x in range(8)] for y in range(8)])
def write(s,G,ox,oy,sx,sy):
    cells={}
    for y in range(SH):
        for x in range(SW):
            X=sx+x-ox;Y=sy+y-oy+YOFF;t=T[Y//8][X//8]
            if t not in cells:cells[t]=gt(s,t)
            cells[t][Y%8][X%8]=G[y][x]
    for t,c in cells.items():pt(s,t,c)
JP=Image.open(os.path.join(HERE,'ref','jp_modes.png')).convert('RGB')
SY={'solo':127,'team':127,'tour':199,'champ':199}
FULL=True      # rebuild the whole plate from the clean reference
FLAT=None   # {'solo':11,...} would give flat bands
SOFT=float(os.environ.get('SOFT','0'));DARK=float(os.environ.get('DARK','0'))
def main(lang):
    for n,(fn,pk,sq,(ox,oy),(sx,sy),texts) in PLATES.items():
        f=os.path.join(ROOT,lang,'Narrator','square%s_set.bin'%sq);s=bytearray(open(f,'rb').read())
        if FULL:
            F=fullplate(fn,pk)
            Gs=[row[6:86] for row in F[43:58]]
            if not os.environ.get('NOTEXT'):label(Gs,texts[lang],pk)
            for yy in range(15):F[43+yy][6:86]=Gs[yy]
            write_full(s,F,n);open(f,'wb').write(s);print(lang,n,texts[lang],'(full plate)');continue
        G=strip(fn,pk)
        if FLAT:G=[[FLAT[n]]*SW for _ in range(SH)]      # flat band (palette index of the plate's own colour), like the menu plates
        if not os.environ.get('NOTEXT'):label(G,texts[lang],pk)
        write(s,G,ox,oy,sx,sy)
        open(f,'wb').write(s);print(lang,n,texts[lang])
if __name__=='__main__':main(sys.argv[1])
