import sys;sys.path.insert(0,'/tmp/emu')
from emu import *
import numpy as np
load(sys.argv[1]);run(300)
for k in range(400):
    if k%3==0: press('A',6,0)
    run(80)
    a=state['fb'].astype(int)
    y=((a[100:135,:,0]>200)&(a[100:135,:,1]>180)&(a[100:135,:,2]<90)).sum()
    if y>250 and k>100:
        run(60);shot(sys.argv[2]);open(sys.argv[2]+'.vr','wb').write(mem(3));print('k',k);break
