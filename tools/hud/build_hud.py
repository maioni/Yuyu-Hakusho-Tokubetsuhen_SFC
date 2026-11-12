import sys,struct
from opt3 import *
def make(tr,outdir,cs=(43,128,213),gg=3):
    L,sp=build(tr,cs,gg)
    cols=sorted({x//8 for a,b in sp for x in range(a,b)})
    assert len(cols)<=16,len(cols)
    tiles=b''; row=[0x800]*32
    for k,c in enumerate(cols):
        px=L[:,c*8:c*8+8].copy(); px[px==0]=4
        tiles+=tile_bytes(px); row[c]=0x400|(143+k)
    blank=143+len(cols); tiles+=tile_bytes(np.full((8,8),4)); row=[0x400|blank if w==0x800 else w for w in row]
    tiles=tiles.ljust(17*32,b'\0')
    open(f'{outdir}/hud_tiles.bin','wb').write(tiles)
    open(f'{outdir}/hud_row.bin','wb').write(struct.pack('<32H',*row))
    return len(cols)
if __name__=='__main__':
    import os
    for d,tr,cs,gg in(('en',['Life','Spirit','Energy'],(43,128,212),3),('pt',['Vida','Espírito','Energia'],(43,128,212),1)):
        os.makedirs(f'b/{d}',exist_ok=True); print(d,make(tr,f'b/{d}',cs,gg))
