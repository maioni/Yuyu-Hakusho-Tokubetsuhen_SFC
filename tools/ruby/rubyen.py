import re,json,sys
B='/home/claude/stoneboat65816/yuyu-hakusho-tokubetsuhen_sfc/'
ROM=open('/tmp/bt/v09c.smc','rb').read()
W=list(ROM[0x201000:0x201000+240])+[4,4]+[8]*14
FUR=ROM[0x200000+0x10F0:0x200000+0x10F0+256*32]
tbl={}
import os
for l in open(B+os.environ.get('RTBL','enUS/Yuyu_PTBR.tbl'),encoding='utf-8').read().split('\n'):
    if '=' in l and not l.startswith('/'):
        k,v=l.split('=',1)
        if len(k)==4 or len(k)==2: tbl[v]=int(k[:2],16)
longest=max(len(k) for k in tbl)
def tokens(s):
    out=[];i=0
    while i<len(s):
        if s.startswith('<end>',i): out.append('<end>');i+=5;continue
        if s[i]=='<':
            j=s.index('>',i);out.append(s[i:j+1]);i=j+1;continue
        for L in range(longest,0,-1):
            if s[i:i+L] in tbl: out.append(s[i:i+L]);i+=L;break
        else: raise Exception('unk '+repr(s[i:]))
    return out
def ink_tiles(code):
    g=FUR[code*32:code*32+32];mx=-1
    for t in range(4):
        for r in range(8):
            b=g[t*8+r]
            for x in range(8):
                if b>>(7-x)&1: mx=max(mx,t*8+x)
    return 0 if mx<0 else (mx+1+7)//8
def place(line,pieces,span=None,dense=False):
    """line: EN text; pieces: list of codes; span: substring where pieces are spread (default: quote/name content).
    returns new line, info"""
    toks=tokens(line)
    # char-level text (excluding tags)
    plain=''.join(t for t in toks if not t.startswith('<'))
    # compute x (px) at each token index
    xs=[];x=0
    for t in toks:
        xs.append(x)
        if t.startswith('<'): continue
        x+=W[tbl[t]]
    total=x
    # locate span in token indices
    idxs=[i for i,t in enumerate(toks) if not t.startswith('<')]
    s_chars=''.join(toks[i] for i in idxs)
    if span is None:
        # default: content after 「 or leading spaces, to before trailing punctuation
        qs=[p for p in (s_chars.find('「'),s_chars.find('『')) if p>=0]
        st=min(qs)+1 if qs else (len(s_chars)-len(s_chars.lstrip(' ')))
        en=len(s_chars.rstrip('」』!~.-'))
        # speaker prefix like "Underground Bomb 「" handled by explicit span
    else:
        st=s_chars.find(span)
        assert st>=0,(line,span)
        en=st+len(span)
    # map char positions to token index
    i_start=idxs[st]; i_end=idxs[en-1]+1 if en>0 else i_start
    x0=xs[i_start]; x1=xs[i_end-1]+W[tbl[toks[i_end-1]]] if i_end>i_start else x0
    k=len(pieces)
    ns=[max(ink_tiles(c),1) for c in pieces]
    spanTiles=max((x1-x0)/8,1)
    # target tile offsets (in tiles) relative to d20 at span start
    d0=(x0>>3)+1
    out=[];pi=0;nextfree=0;x=0;layout=[]
    for ti,t in enumerate(toks):
        if not t.startswith('<') and ti>=i_start and pi<k:
            d20=(x>>3)+1
            target=d0+(sum(ns[:pi]) if dense else int(round(pi*max(spanTiles/k,0))))
            if d20>=max(nextfree,target):
                c=pieces[pi]; out.append('<$%02X><$20>'%c); layout.append((c,d20,ns[pi])); nextfree=d20+ns[pi]; pi+=1
        out.append(t)
        if not t.startswith('<'): x+=W[tbl[t]]
    # leftover pieces: pad spaces before <end>
    endpos=len(out)-1 if out and out[-1]=='<end>' else len(out)
    tail=[]
    while pi<k:
        d20=(x>>3)+1
        if d20>=nextfree:
            c=pieces[pi]; tail.append('<$%02X><$20>'%c); layout.append((c,d20,ns[pi])); nextfree=d20+ns[pi]; pi+=1
        else:
            tail.append(' '); x+=W[tbl[' ']]
    out[endpos:endpos]=tail
    return ''.join(out),layout,x
