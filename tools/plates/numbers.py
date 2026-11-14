#!/usr/bin/env python3
"""Restore the original shaded (anti-aliased) 'No.' + digits 0-9 (16x16, 2bpp, JP tiles $C9..$F8) in
<lang>/Narrator/preset.bin at VRAM tile $320 (offset 0x2600). The earlier port had merged colours 1/2 into white.
usage: numbers.py <enUS|ptBR>"""
import sys,os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE=os.path.dirname(os.path.abspath(__file__))
l=sys.argv[1];f=os.path.join(ROOT,l,'Narrator','preset.bin')
d=bytearray(open(f,'rb').read());n=open(os.path.join(HERE,'num_jp.bin'),'rb').read()
assert len(n)==768
# swap colour indices 2<->3 so the shaded tone sits in index 3: the sound screen sets palette-3 colour 3 to the original
# greenish grey ($4EB4) while index 2 stays grey for the names/titles that share the palette
n=bytearray(n)
for t in range(48):
    for y in range(8):
        a=n[t*16+y*2];b=n[t*16+y*2+1]
        # pixel = a_bit | b_bit<<1 ; 2 -> 3 and 3 -> 2  == flip a where b set
        n[t*16+y*2]=a^b
n=bytes(n)
d[0x2600:0x2600+768]=n;open(f,'wb').write(d);print(l,'ok')
