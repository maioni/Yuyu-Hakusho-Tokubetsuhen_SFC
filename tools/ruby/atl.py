import re,sys
sys.path.insert(0,'/tmp/ru')
from rubyen import tokens,tbl,B
def tblfull(path):
    t={}
    for l in open(path,encoding='utf-8').read().split('\n'):
        l=l.rstrip('\r')
        if '=' in l and not l.startswith('/'):
            k,v=l.split('=',1)
            if len(k) in(2,4): t[v]=bytes.fromhex(k if len(k)==4 else k+'00')
    return t
def insert(rom,path,tblpath):
    T=tblfull(tblpath); longest=max(len(k) for k in T)
    rom=bytearray(rom)
    pos=None;pend=[];base=None
    for l in open(path,encoding='utf-8').read().split('\n'):
        l=l.rstrip('\r')
        m=re.match(r'#JMP\(\$([0-9A-Fa-f]+)\)',l)
        if m: pos=int(m.group(1),16);base=base or pos;continue
        m=re.match(r'#WRITE\(Ptr, \$([0-9A-Fa-f]+)\)',l)
        if m: pend.append(int(m.group(1),16));continue
        if not l.strip() or l.startswith('//') or l.startswith('#'): continue
        out=bytearray();i=0
        while i<len(l):
            if l[i]=='<' and l[i+1]=='$': out.append(int(l[i+2:i+4],16));i+=5;continue
            for L in range(longest,0,-1):
                if l[i:i+L] in T: out+=T[l[i:i+L]];i+=L;break
            else: raise Exception('unk '+repr(l[i:]))
        for a in pend:
            v=(pos-0x310000)&0xFFFF; rom[a:a+2]=v.to_bytes(2,'little')
        pend=[]
        rom[pos:pos+len(out)]=out; pos+=len(out)
    return bytes(rom),pos
if __name__=='__main__':
    R=open('/tmp/bt/v09c.smc','rb').read()
    out,end=insert(R,B+'enUS/battle_text_enUS.txt',B+'enUS/Yuyu_PTBR.tbl')
    print(hex(end), out==R, sum(1 for a,b in zip(out,R) if a!=b))
