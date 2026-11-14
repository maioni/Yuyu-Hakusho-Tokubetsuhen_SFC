import sys;sys.path.insert(0,'.')
from bigfont import pixels
from PIL import Image,ImageDraw
src=Image.open('/mnt/user-data/attachments/080b782e-618e-5293-a63c-47ec41af85d4/c200ea63-image.png').convert('RGB')
new=src.copy()
def band(x0,x1,col,text,y_caps=151):
    for y in range(149,163):
        for x in range(x0,x1): new.putpixel((x,y),col)
    P,W=pixels(text);cx=(x0+x1)//2;ox=cx-W//2
    for (x,y) in P:
        for dy in(-1,0,1):
            for dx in(-1,0,1):new.putpixel((ox+x+dx,y_caps+y+dy),(0,0,0))
    for (x,y) in P:new.putpixel((ox+x,y_caps+y),(255,255,255))
band(26,102,(33,41,49),'1P vs COM')
band(154,231,(90,66,57),'1P vs 2P')
# dark top line like original right plate
for x in range(154,231):new.putpixel((x,149),(33,41,49));new.putpixel((x,150),(33,41,49))
out=Image.new('RGB',(2*512+30,448+2*140+90),(20,20,20));d=ImageDraw.Draw(out)
d.text((10,6),'ATUAL',fill=(255,255,0));d.text((542,6),'FONTE NOVA (maquete: faixa de fundo simulada)',fill=(255,255,0))
out.paste(src.resize((512,448),Image.NEAREST),(10,22));out.paste(new.resize((512,448),Image.NEAREST),(542,22))
y=22+448+14
for i,(a,b) in enumerate(((14,114),(142,242))):
    pass
for k,(box) in enumerate(((14,144,114,168),(142,144,242,168))):
    w=box[2]-box[0]
    out.paste(src.crop(box).resize((w*5,120),Image.NEAREST),(10+k*(w*5+0)+ (0 if k==0 else 0),y)) if False else None
# strips: current vs new, stacked, for left and right
yy=y
for k,box in enumerate(((14,144,114,168),(142,144,242,168))):
    w=box[2]-box[0]
    out.paste(src.crop(box).resize((w*5,120),Image.NEAREST),(10+k*(w*5+20),yy))
    out.paste(new.crop(box).resize((w*5,120),Image.NEAREST),(10+k*(w*5+20),yy+130))
out=out.crop((0,0,out.width,yy+260))
out.save('/tmp/mock_cmp.png');print(out.size)
