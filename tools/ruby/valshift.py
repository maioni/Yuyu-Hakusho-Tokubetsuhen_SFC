"""Validate ruby piece overlap for every name width shift (0..7 px). usage: valshift.py en|pt"""
import os,re,sys
lang=sys.argv[1]
R='/home/claude/stoneboat65816/yuyu-hakusho-tokubetsuhen_sfc/';os.chdir(R)
os.environ['RTBL']='enUS/Yuyu_PTBR.tbl' if lang=='en' else 'ptBR/Yuyu_PTBR.tbl'
rom={'en':'/tmp/hud/b/en_final4.smc','pt':'/tmp/hud/b/pt_final2.smc'}[lang]
src=open('tools/ruby/rubyen.py').read().split('def place')[0].replace("/tmp/bt/v09c.smc",rom)
exec(src)
txt='enUS/battle_text_enUS.txt' if lang=='en' else 'ptBR/battle_text_PTBR.txt'
def ink(c):
    g=FUR[c*32:c*32+32];m=[any(g[t*8:t*8+8]) for t in range(4)];return m
bad=0;tot=0
for n,l in enumerate(open(txt,encoding='utf-8').read().split('\n'),1):
    if l.startswith('//') or l.startswith('#') or not l.strip() or not re.search(r'<\$[0-9A-F]{2}><\$20>',l):continue
    try: toks=tokens(l)
    except Exception as e: print('untok',n);continue
    tot+=1
    worst=None
    for sh in range(8):
        x=0;prev=0;pcs=[];k=0
        while k<len(toks):
            t=toks[k]
            if t.startswith('<$') and k+1<len(toks) and toks[k+1]=='<$20>' and t!='<$20>':
                pcs.append((int(t[2:4],16),(prev>>3)+1));k+=2;continue
            if t.startswith('<'):
                if t.startswith('<name'): x+=sh
                k+=1;continue
            prev=x;x+=W[tbl[t]];k+=1
        lost=[]
        for i,(c,a) in enumerate(pcs):
            im=ink(c)
            for c2,b in pcs[i+1:]:
                for t in range(4):
                    if im[t] and b<=a+t<b+4: lost.append((hex(c),t))
        if lost and (worst is None): worst=(sh,lost)
        if '<name' not in l: break
    if worst:
        bad+=1;print(n,'shift',worst[0],'LOST',worst[1],'|',''.join(t for t in toks if not t.startswith('<')).strip()[:50])
print(lang,'lines',tot,'with lost ink',bad)
