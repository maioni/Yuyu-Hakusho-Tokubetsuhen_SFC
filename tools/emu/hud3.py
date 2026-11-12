import sys;sys.path.insert(0,'/tmp/emu')
from emu import *
rom=sys.argv[1]
load(rom);run(400)
for i in range(5):
    press('START',6,200);run(200)
press('A',6,120);run(200);press('A',6,120);run(200);press('A',6,120);run(200)
press('A',6,120);run(100)
for _ in range(3): press('A',6,150);run(150)
run(900)
L.retro_serialize_size.restype=C.c_size_t
n=L.retro_serialize_size();buf=C.create_string_buffer(n)
assert L.retro_serialize(buf,n)
open('/tmp/emu/state_fight.bin','wb').write(buf.raw)
shot('/tmp/emu/hud_a.png')
open('/tmp/emu/vram_fight.bin','wb').write(mem(3))
print(n)
