import re
def enc(txtpath,tblpath):
    T={}
    for l in open(tblpath,encoding='utf-8-sig').read().split('\n'):
        l=l.rstrip('\r')
        if '=' in l and not l.startswith('/'):
            k,v=l.split('=',1)
            if re.fullmatch(r'[0-9A-Fa-f]+',k) and len(k)%2==0 and v!='':
                T.setdefault(v,bytes.fromhex(k))
    longest=max(len(k) for k in T)
    out=bytearray(); started=False
    for l in open(txtpath,encoding='utf-8').read().split('\n'):
        l=l.rstrip('\r')
        if not started:
            if l.startswith('#JMP'): started=True
            continue
        if not l.strip(): continue
        i=0
        while i<len(l):
            for L in range(longest,0,-1):
                if l[i:i+L] in T: out+=T[l[i:i+L]]; i+=L; break
            else: raise Exception('unk '+repr(l[i:i+20]))
    return bytes(out)
