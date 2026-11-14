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
d[0x2600:0x2600+768]=n;open(f,'wb').write(d);print(l,'ok')
