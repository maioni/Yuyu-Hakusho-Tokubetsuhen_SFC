import os,sys,re
lang=sys.argv[1]
os.environ['RTBL']='enUS/Yuyu_PTBR.tbl' if lang=='en' else 'ptBR/Yuyu_PTBR.tbl'
src=open('rubyen.py').read().split('def place')[0]
src=src.replace("/tmp/bt/v09c.smc",'/tmp/hud/b/'+('en_f13.smc' if lang=='en' else 'pt_f11.smc'))
exec(src)
B2=B+('enUS/battle_text_enUS.txt' if lang=='en' else 'ptBR/battle_text_PTBR.txt')
def tileink(c):
    g=FUR[c*32:c*32+32];return [any(g[t*8:t*8+8]) for t in range(4)]
tot=0
for n,l in enumerate(open(B2,encoding='utf-8').read().split('\n'),1):
    if l.startswith('//') or not re.search(r'<\$[0-9A-F]{2}><\$20>',l): continue
    try: toks=tokens(l)
    except Exception: print(n,"UNTOKENIZABLE",l[:40]); continue
    x=0;prev=0;pcs=[];k=0
    while k<len(toks):
        t=toks[k]
        if t.startswith('<$') and k+1<len(toks) and toks[k+1]=='<$20>' and t!='<$20>':
            pcs.append((int(t[2:4],16),(prev>>3)+1));k+=2;continue
        if t.startswith('<'): k+=1;continue
        prev=x;x+=W[tbl[t]];k+=1
    lost=[]
    for i,(c,a) in enumerate(pcs):
        ink=tileink(c)
        for j,(c2,b) in enumerate(pcs[i+1:],i+1):
            for t in range(4):
                if ink[t] and b<=a+t<b+4: lost.append((hex(c),t))
    if lost:
        tot+=1;plain=''.join(t for t in toks if not t.startswith('<'))
        print(n,'LOST',lost,'|',plain.strip()[:60])
print(lang,'lines with lost ink',tot)
