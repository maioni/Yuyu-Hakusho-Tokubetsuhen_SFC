#!/usr/bin/env python3
"""Menu plates (main menu: Free Battle / Options; settings menu: Difficulty / Sound / Buttons): rebuild the label strip.
Same idea as modes.py: the strip (interior of the dark label bar) keeps the original game's own pixels (read from the JP
screenshots in ref/jp_main.png, ref/jp_set.png) wherever the Japanese lettering does not cover them; the pixels under the
lettering come from the clean (text-free) reference squares (ref/14..18, 2x, area-averaged and snapped to the plate's
real sprite palette).  Then the label is drawn with the pixel font (tools/font/bigfont2.py): white, 1 px dark outline,
base of the letters on the bottom row of the strip.  Accents (Ã Õ Ç ...) are drawn on top/below, over the bar lines.
Tile maps (screen cell -> sheet tile) were measured in the emulator: ref/menu_tilemaps.json ([sq, tile] per 8x8 cell).
usage: menus.py <enUS|ptBR>"""
import sys,os,json,unicodedata
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0,HERE);sys.path.insert(0,os.path.join(ROOT,'tools','font'))
from rank import gt,pt
from PIL import Image,ImageFilter
import bigfont2 as bf
bf.YS=0.97;bf.BRUSH2=False
REF=os.path.join(HERE,'ref')
TM=json.load(open(os.path.join(REF,'menu_tilemaps.json')))
PAL=json.load(open(os.path.join(REF,'menu_pal.json')))
JPI={'main':Image.open(os.path.join(REF,'jp_main.png')).convert('RGB'),'set':Image.open(os.path.join(REF,'jp_set.png')).convert('RGB'),'stage':Image.open(os.path.join(REF,'jp_stage.png')).convert('RGB')}
def c15(v):
    r,g,b=v&31,(v>>5)&31,(v>>10)&31;return ((r<<3)|(r>>2),(g<<3)|(g>>2),(b<<3)|(b>>2))
# name: (screen, plate origin, size, sheet, clean ref, strip rect x0,y0,w,h, font (xscap,capair,gap), {lang:text})
PLATES={
 'free':('main',(16,88),(96,80),'01','14_menu_batalha_livre_sem_texto.png',(8,63,80,11),(0.56,1,1),{'enUS':'FREE BATTLE','ptBR':'COMBATE LIVRE'}),
 'opt': ('main',(144,88),(96,80),'00','15_menu_configuracoes_sem_texto.png',(8,63,80,11),(0.56,1,1),{'enUS':'OPTIONS','ptBR':'OPÇÕES'}),
 'diff':('set',(24,96),(64,64),'02','16_config_dificuldade_sem_texto.png',(8,47,48,11),(0.42,0,0),{'enUS':'DIFFICULTY','ptBR':'DIFICULDADE'}),
 'snd': ('set',(96,96),(64,64),'03','17_config_som_sem_texto.png',(8,47,48,11),(0.7,1,1),{'enUS':'SOUND','ptBR':'SOM'}),
 'btn': ('set',(168,96),(64,64),'04','18_config_controles_sem_texto.png',(8,47,48,11),(0.56,1,1),{'enUS':'BUTTONS','ptBR':'BOTÕES'}),

 'forest':('stage',(32,80),(64,64),'11','23_estagio_floresta_sem_texto.png',(8,47,48,11),(0.62,1,1),{'enUS':'FOREST','ptBR':'FLORESTA'}),
 'dome':  ('stage',(160,80),(64,64),'11','24_estagio_domo_trevas_sem_texto.png',(8,47,48,11),(0.7,1,1),{'enUS':'DOME','ptBR':'DOMO'}),
 'hill':  ('stage',(32,152),(64,64),'12','25_estagio_colina_decapitacao_sem_texto.png',(8,47,48,11),(0.7,1,1),{'enUS':'HILL','ptBR':'COLINA'}),
 'dim':   ('stage',(160,152),(64,64),'12','26_estagio_fenda_dimensional_sem_texto.png',(8,47,48,11),(0.5,1,1),{'enUS':'DIMENSION','ptBR':'DIMENSÃO'}),
}
TXTIDX={'free':(1,2,3),'opt':(1,2,3,4)}   # palette indices the Japanese lettering uses (free: index 4 is the plate grey)
ACC={'~':[(0,1),(1,0),(2,0),(3,1)],'´':[(0,1),(1,0)],'`':[(0,0),(1,1)],'^':[(0,1),(1,0),(2,1)]}
BASE={'Ã':('A','~'),'Õ':('O','~'),'É':('E','´'),'Ê':('E','^'),'Á':('A','´'),'Â':('A','^'),'Í':('I','´'),'Ó':('O','´'),'Ô':('O','^'),'Ú':('U','´'),'À':('A','`'),'Ç':('C','ç')}
FULL=True       # rebuild the whole plate from the clean reference (like modes.py)
GAPV=1
def layout(text,extra=0):
    """pixels of the text, x from 0, y from the top of the capitals (accents negative / cedilla below); returns (set, width, baseline)"""
    out=set();x=0;prev=None;base=0;L=[c for c in text if c!=' '];n=len(L);li=0
    for ch in text:
        if ch==' ':x+=4;prev=None;continue
        b,a=BASE.get(ch,(ch,None))
        P,w=bf.raster(b)
        if prev is not None: x+=bf.CAPAIR if True else 0
        for (px,py) in P:out.add((x+px,py))
        base=max(base,max(py for _,py in P))
        if a:
            cx=x+w//2
            if a=='ç':out.add((cx,base+1))
            else:
                ap=ACC[a];ax=cx-2
                for (dx,dy) in ap:out.add((ax+dx,dy-2))
        x+=w+GAPV
        if n>1 and extra>0 and (li+1)*extra//(n-1)>li*extra//(n-1):x+=1      # spread spare pixels evenly between letters
        li+=1
        prev=ch
    return out,x-GAPV,base
def pal_bank(scr,x0,y0,w,h):
    """sprite palette bank whose colours explain the plate's pixels on the JP screenshot best (tolerant colour match)"""
    im=JPI[scr].crop((x0,y0,x0+w,y0+h));cols=list(im.getdata());best=None
    for k,b in enumerate(PAL[scr]):
        pc=[c15(v) for v in b[1:]]
        m=sum(1 for c in cols if not any(max(abs(a-d) for a,d in zip(c,q))<=4 for q in pc))
        if best is None or m<best[0]:best=(m,k)
    return PAL[scr][best[1]]
def nearest(pal,c):
    return min(range(1,16),key=lambda i:sum((a-b)**2 for a,b in zip(pal[i],c)))
def build(name,lang):
    scr,(px0,py0),(pw,ph),sq,rf,(sx,sy,sw,sh),(xs,air,gap),texts=PLATES[name]
    pal=[c15(v) for v in pal_bank(scr,px0,py0,pw,ph)]
    jp=JPI[scr].load()
    ref=Image.open(os.path.join(REF,rf)).convert('RGB').filter(ImageFilter.MedianFilter(3)).resize((pw,ph),Image.BOX)
    rp=ref.load()
    G={}
    if FULL:                            # whole plate from the clean reference: exact sampling of the 2x image, snapped to the palette
        rimg=Image.open(os.path.join(REF,rf)).convert('RGB');rq=rimg.load()
        for Y in range(ph):
            for x in range(pw):
                G[(x,Y-sy)]=nearest(pal,rq[2*x+1,2*Y+1])
    for y in range(0 if FULL else sh):                # interior: the original game's pixels (palette indices)
        for x in range(sx,sx+sw):G[(x,y)]=nearest(pal,jp[px0+x,py0+sy+y])
    # replace the pixels under the Japanese lettering (white / dark outline colours) with the clean reference
    if not FULL:
        TXI=TXTIDX.get(name,(1,2,3,4));TXT=[pal[i] for i in TXI]
        def istxt(c):return any(max(abs(a-b) for a,b in zip(c,t))<=3 for t in TXT)
        from collections import Counter
        cnt=Counter(jp[px0+x,py0+sy+y] for y in range(sh) for x in range(sx,sx+sw) if not istxt(jp[px0+x,py0+sy+y]))
        bg=sorted({nearest(pal,c) for c,n in cnt.items() if n>=3})      # indices of the strip's real background colours
        for y in range(sh):
            for x in range(sx,sx+sw):
                jc=jp[px0+x,py0+sy+y]
                if istxt(jc):
                    c=rp[x,sy+y];G[(x,y)]=min(bg,key=lambda i:sum((a-b)**2 for a,b in zip(pal[i],c)))
    global GAPV
    chain=[(xs,air,gap),(0.62,1,1),(0.56,1,1),(0.5,1,1),(0.42,1,1),(0.5,0,1),(0.42,0,1),(0.42,0,0)]
    for (xs,air,gap) in chain:          # first font setting that fits the strip
        GAPV=gap;bf.XSCAP=xs;bf.CAPAIR=air
        if layout(texts[lang])[1]<=sw-4:break
    P,w,base=layout(texts[lang]);
    ex=max(0,min(sw-4-w,len(texts[lang])-1))
    if ex:P,w,base=layout(texts[lang],ex)
    if w>sw:print('WARNING %s %s text %d > strip %d'%(name,lang,w,sw))
    ox=sx+(sw-w)//2;oy=sh-1-base
    S={(ox+x,oy+y) for x,y in P}
    for (x,y) in S:
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                X,Y=x+dx,y+dy
                if (X,Y) not in S and sx<=X<sx+sw and -2<=Y<=sh:G[(X,Y)]=1
    for (x,y) in S:
        if sx<=x<sx+sw and -2<=y<=sh:G[(x,y)]=2
    return sq,G,(px0,py0)
def write(lang):
    for name in PLATES:
        sq,G,_=build(name,lang)
        f=os.path.join(ROOT,lang,'Narrator','square%s_set.bin'%sq);s=bytearray(open(f,'rb').read())
        key=name;pw,ph=PLATES[name][2];sy=PLATES[name][5][1]
        cells={};owner={}
        for ty,row in enumerate(TM[key]):          # mirrored (flipped) cells reuse a tile: only the first cell may write it
            for tx,m in enumerate(row):
                if m is not None and m[1] not in owner:owner[m[1]]=(tx,ty)
        for (x,y),v in sorted(G.items()):
            Y=sy+y
            if not(0<=Y<len(TM[key])*8 and 0<=x<len(TM[key][0])*8):continue
            m=TM[key][Y//8][x//8]
            if m is None or owner.get(m[1])!=(x//8,Y//8):continue
            t=m[1]
            if t not in cells:cells[t]=gt(s,t)
            cells[t][Y%8][x%8]=v
        for t,c in cells.items():pt(s,t,c)
        open(f,'wb').write(s);print(lang,name,PLATES[name][7][lang])
if __name__=='__main__':write(sys.argv[1])
