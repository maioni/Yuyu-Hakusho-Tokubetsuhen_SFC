import os,sys,re
lang=sys.argv[1]; write=len(sys.argv)>2
os.environ['RTBL']='enUS/Yuyu_PTBR.tbl' if lang=='en' else 'ptBR/Yuyu_PTBR.tbl'
src=open('rubyen.py').read().split('def place')[0]
src=src.replace("/tmp/bt/v09c.smc",'/tmp/hud/b/'+('en_f13.smc' if lang=='en' else 'pt_f11.smc'))
exec(src)
P=B+('enUS/battle_text_enUS.txt' if lang=='en' else 'ptBR/battle_text_PTBR.txt')
lines=open(P,encoding='utf-8').read().split('\n')
def span(c):
    g=FUR[c*32:c*32+32];m=0
    for t in range(4):
        if any(g[t*8:t*8+8]): m=t+1
    return max(m,1)
def layout(toks):
    x=0;prev=0;out={}
    for k,t in enumerate(toks):
        if t.startswith('<$') and t!='<$20>' and k+1<len(toks) and toks[k+1]=='<$20>': out[k]=(prev>>3)+1; continue
        if t.startswith('<'): continue
        prev=x;x+=W[tbl[t]]
    return out
changed=0;bad=0
for n,l in enumerate(lines):
    if l.startswith('//') or not re.search(r'<\$[0-9A-F]{2}><\$20>',l): continue
    try: toks=tokens(l)
    except Exception: continue
    for _ in range(40):
        lay=layout(toks);pk=sorted(lay);moved=False
        for a,b in zip(pk,pk[1:]):
            ca=int(toks[a][2:4],16)
            if lay[a]+span(ca)>lay[b]:
                # move piece b (2 tokens) right past next text char
                j=b+2
                while j<len(toks) and toks[j].startswith('<'): 
                    if toks[j]=='<end>': j=None;break
                    j+=1
                if j is None or j>=len(toks): bad+=1;toks=tokens(l);print('STUCK',n+1);moved=False;break
                toks[b:j+1]=toks[b+2:j+1]+toks[b:b+2]
                moved=True;break
        if not moved: break
    new=''.join(toks)
    if new!=l:
        changed+=1;lines[n]=new
        if changed<=60: print(n+1,l.strip()[:75],'\n   ->',new.strip()[:75])
print(lang,'changed',changed,'stuck',bad)
if write: open(P,'w',encoding='utf-8').write('\n'.join(lines))
