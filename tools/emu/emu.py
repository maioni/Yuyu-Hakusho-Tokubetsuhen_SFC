import ctypes as C,sys
from PIL import Image
import numpy as np
L=C.CDLL('/tmp/s9x/libretro/snes9x_libretro.so')
class GI(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
VID=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUD=C.CFUNCTYPE(None,C.c_int16,C.c_int16)
ABT=C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
IP=C.CFUNCTYPE(None)
IS=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
state={'fb':None,'fmt':2,'btn':0}
keep=[]
def env(cmd,data):
    if cmd==10: state['fmt']=C.cast(data,C.POINTER(C.c_int)).contents.value;return True
    if cmd==3: C.cast(data,C.POINTER(C.c_bool)).contents.value=True;return True
    if cmd in(9,31):
        p=C.cast(data,C.POINTER(C.c_char_p));p.contents=C.c_char_p(b'/tmp/emu');keep.append(p);return True
    return False
def vid(d,w,h,pitch):
    if not d:return
    state['w'],state['h']=w,h
    if state['fmt']==1:
        a=np.frombuffer(C.string_at(d,pitch*h),np.uint8).reshape(h,pitch)[:,:w*4].reshape(h,w,4)[:,:,[2,1,0]]
    else:
        a=np.frombuffer(C.string_at(d,pitch*h),np.uint16).reshape(h,pitch//2)[:,:w]
        a=np.stack([((a>>11)&31)*255//31,((a>>5)&63)*255//63,(a&31)*255//31],-1).astype(np.uint8)
    state['fb']=a
envc=ENV(env);vidc=VID(vid);audc=AUD(lambda l,r:None)
abc=ABT(lambda d,n:n);ipc=IP(lambda:None)
def inp(port,dev,idx,id_):
    return 1 if (port==0 and dev==1 and (state['btn']>>id_)&1) else 0
isc=IS(inp)
L.retro_set_environment(envc);L.retro_set_video_refresh(vidc);L.retro_set_audio_sample(audc)
L.retro_set_audio_sample_batch(abc);L.retro_set_input_poll(ipc);L.retro_set_input_state(isc)
L.retro_init()
def load(path):
    d=open(path,'rb').read();buf=C.create_string_buffer(d,len(d));keep.append(buf)
    gi=GI(path.encode(),C.cast(buf,C.c_void_p),len(d),None)
    assert L.retro_load_game(C.byref(gi))
L.retro_get_memory_data.restype=C.c_void_p
L.retro_get_memory_size.restype=C.c_size_t
def run(n,btn=0):
    state['btn']=btn
    for _ in range(n):L.retro_run()
def shot(f):Image.fromarray(state['fb']).save(f)
def mem(i):
    p=L.retro_get_memory_data(i);s=L.retro_get_memory_size(i);return C.string_at(p,s) if p else b''
B=dict(B=0,Y=1,SEL=2,START=3,UP=4,DOWN=5,LEFT=6,RIGHT=7,A=8,X=9)
def press(name,n=6,gap=30):
    run(n,1<<B[name]);run(gap,0)
