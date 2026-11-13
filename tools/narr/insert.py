#!/usr/bin/env python3
"""Linux stand-in for Narrator/Insert.exe (Atlas subset): encode nameNN.txt / narratorNN.txt to .bin.
usage: insert.py <Narrator dir>   (writes every *.bin that has a matching *.txt)"""
import re,sys,glob,os
def load_tbl(p):
    t={}
    for l in open(p,encoding='utf-8-sig').read().split('\n'):
        l=l.rstrip('\r')
        if '=' in l:
            k,v=l.split('=',1)
            if v=='' : continue
            t.setdefault(v,bytes.fromhex(k))
    return t
def enc(txt,t):
    body=txt.split('#JMP',1)[1]; body=body.split('\n',1)[1]
    body=re.sub(r'\r','',body)
    out=bytearray();keys=sorted(t,key=len,reverse=True);i=0
    while i<len(body):
        c=body[i]
        if c=='\n': i+=1;continue
        m=re.match(r'<\$([0-9A-Fa-f]{2})>',body[i:])
        if m: out.append(int(m.group(1),16));i+=m.end();continue
        for k in keys:
            if body.startswith(k,i): out+=t[k];i+=len(k);break
        else: raise SystemExit('no tbl entry for %r near %r'%(c,body[i:i+20]))
    return bytes(out)
d=sys.argv[1]
for f in sorted(glob.glob(d+'/*.txt')):
    s=open(f,encoding='utf-8-sig').read()
    if '#JMP' not in s: continue
    tb=re.search(r'#ADDTBL\("([^"]+)"',s).group(1)
    b=enc(s,load_tbl(os.path.join(d,tb)))
    open(f[:-4]+'.bin','wb').write(b)
