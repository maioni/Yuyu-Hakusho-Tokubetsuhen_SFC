import sys;sys.path.insert(0,'.')
from bigfont import *
from PIL import Image,ImageDraw
BG=(33,41,49);W_=(255,255,255);OL=(0,0,0)
def strip(text,w=96,h=20,bg=BG):
    P,Wd=pixels(text);im=Image.new('RGB',(w,h),bg)
    x0=(w-Wd)//2;y0=3
    for (x,y) in P:
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                im.putpixel((x0+x+dx,y0+y+dy),OL)
    for (x,y) in P: im.putpixel((x0+x,y0+y),W_)
    return im,Wd
PT=['1P vs COM','1P vs 2P','Combate Livre','Combate Solo','Dificuldade','Som','Botões','Opções','Continuar','Desistir','Esquiva','Nível']
EN=['Free Battle','Solo Battle','Difficulty','Sound','Buttons','Options','Continue','Give Up','Dodge','Parry','High guard','Class']
def sheet(lst,title,fn):
    cols=3;cw=96*3+10;rows=(len(lst)+cols-1)//cols
    out=Image.new('RGB',(cols*cw+10,rows*(20*3+22)+30),(20,20,20));d=ImageDraw.Draw(out);d.text((10,6),title,fill=(255,255,0))
    for i,t in enumerate(lst):
        im,w=strip(t);x=10+(i%cols)*cw;y=26+(i//cols)*(20*3+22)
        out.paste(im.resize((96*3,60),Image.NEAREST),(x,y));d.text((x,y+62),'%s  (%d px)'%(t,w),fill=(200,200,200))
    out.save(fn);return out.size
print(sheet(PT,'Fonte propria - textos PT-BR','/tmp/own_pt.png'),sheet(EN,'Fonte propria - textos EN','/tmp/own_en.png'))
