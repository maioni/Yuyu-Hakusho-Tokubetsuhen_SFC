"""PT-BR version of rewrite.py. Regenerate broken PT ruby (romaji) pieces + make piece placement robust to <name> width.
Run from repo root:  python3 tools/ruby/rewrite.py   (needs /tmp/sim/blobs.pkl = letter atlas from the ROM glyph table)
Writes ptBR/Font/ruby_extra.bin (extended to code $FF) and ptBR/battle_text_PTBR.txt."""
import os,re,sys,pickle,numpy as np
R='/home/claude/stoneboat65816/yuyu-hakusho-tokubetsuhen_sfc/'; os.chdir(R)
os.environ['RTBL']='ptBR/Yuyu_PTBR.tbl'
sys.path.insert(0,R+'tools/ruby')
src=open('tools/ruby/rubyen.py').read().split('def place')[0].replace("/tmp/bt/v09c.smc",'/tmp/hud/b/pt_final.smc')
exec(src)
# ---------- font from atlas ----------
BL=pickle.load(open('/tmp/sim/blobs.pkl','rb'))
names='a i e o k h u n ō s y S t K p ū R m J d r g l b G B z D T Y c E W M j v f N F O Z -'.split()
F={}
for i,n in enumerate(names): F[n]=BL[i][0].copy()
P=np.array([[1,1,1,1,1,1,0],[0,1,0,0,0,0,1],[0,1,0,0,0,0,1],[0,1,1,1,1,1,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[1,1,1,0,0,0,0],[0,0,0,0,0,0,0]],np.uint8)
F['P']=P
def render(text):
    cols=[]
    for ch in text:
        if ch==' ': cols.append(np.zeros((8,3),np.uint8)); continue
        cols.append(F[ch]); cols.append(np.zeros((8,1),np.uint8))
    a=np.concatenate(cols,1)
    # trim trailing blank
    nz=np.where(a.any(0))[0]; return a[:,:nz[-1]+1]
def chunks(text):
    words=text.split(' ');out=[];cur=''
    for w in words:
        t=(cur+' '+w) if cur else w
        if render(t).shape[1]<=32: cur=t
        else:
            if cur: out.append(cur)
            if render(w).shape[1]<=32: cur=w
            else:
                cur=''
                for ch in w:
                    if render(cur+ch).shape[1]<=32: cur+=ch
                    else: out.append(cur);cur=ch
    if cur: out.append(cur)
    return out
def enc(a):
    g=np.zeros((8,32),np.uint8); g[:,:a.shape[1]]=a; o=bytearray(32)
    for r in range(8):
        v=0
        for i in range(32): v=(v<<1)|int(g[r,i])
        for t,b in enumerate(v.to_bytes(4,'big')): o[t*8+r]=b
    return bytes(o)
# ---------- glyph table ----------
EX=bytearray(open('ptBR/Font/ruby_extra.bin','rb').read())
if len(EX)<(0x100-0x76)*32: EX+=bytes((0x100-0x76)*32-len(EX))
text=open('ptBR/battle_text_PTBR.txt',encoding='utf-8').read()
REW=(200,212,380,422,452,506,554,800,962,1040,1220,1430,1593,1671,974,992,1016)
_L=text.split('\n')
used=set()
for _n,_l in enumerate(_L,1):
    if _n in REW or _l.startswith('//') or _l.startswith('#'): continue
    used|=set(int(x,16) for x in re.findall(r'<\$([0-9A-F]{2})><\$20>',_l))
free=[c for c in range(0x76,0x100) if c not in used]
alloc={}
def piece(s):
    """allocate (or reuse) a glyph code for chunk text s"""
    if s in alloc: return alloc[s]
    c=free.pop(0); EX[(c-0x76)*32:(c-0x76)*32+32]=enc(render(s)); alloc[s]=(c,(render(s).shape[1]+7)//8); return alloc[s]
def ruby(s):
    ch=s if isinstance(s,list) else chunks(s)
    for c in ch: assert render(c).shape[1]<=32,(c,render(c).shape[1])
    return [piece(c) for c in ch]
# ---------- placement ----------
def strip(line):
    return re.sub(r'<\$[0-9A-F]{2}><\$20>','',line)
def place(line,pcs,start_text=None,start_idx=None,verbose=False):
    base=strip(line); toks=tokens(base)
    plain=[i for i,t in enumerate(toks) if not t.startswith('<')]
    ptext=''.join(toks[i] for i in plain)
    if start_idx is None:
        k=ptext.find(start_text); assert k>=0,(line,start_text); start_idx=k
    # x start of each plain char, var flag (after <name..>)
    xs={};x=0;var=False;varflag={}
    for i,t in enumerate(toks):
        if t.startswith('<'):
            if t.startswith('<name'): var=True
            continue
        xs[i]=x;varflag[i]=var;x+=W[tbl[t]]
    ins=[];j=0;prev=None  # prev=(x,ink)
    pi=start_idx
    while j<len(pcs):
        if pi>=len(plain):
            # extend with spaces before <end>
            toks.insert(len(toks)-1 if toks[-1]=='<end>' else len(toks),' ')
            plain=[i for i,t in enumerate(toks) if not t.startswith('<')]
            x=0;var=False;xs={};varflag={}
            for i,t in enumerate(toks):
                if t.startswith('<'):
                    if t.startswith('<name'): var=True
                    continue
                xs[i]=x;varflag[i]=var;x+=W[tbl[t]]
            ins=[(a if a<len(toks) else a,b) for a,b in ins]
            continue
        ti=plain[pi]; # candidate anchor = char BEFORE which the piece goes, i.e. prev char is plain[pi-1]
        if pi==0: ax=0;av=False
        else: ax=xs[plain[pi-1]];av=varflag[plain[pi-1]]
        ok=True
        if prev is not None:
            D=ax-prev[0]
            if av or prev[2]: ok=(D//8)>=prev[1]
            else: ok=((ax>>3)+1)>=((prev[0]>>3)+1)+prev[1]
        if ok:
            c,ink=pcs[j]; ins.append((ti,'<$%02X><$20>'%c)); prev=(ax,ink,av); j+=1
        pi+=1
    out=[];m=dict()
    for ti,s in ins: m.setdefault(ti,[]).append(s)
    for i,t in enumerate(toks):
        if i in m: out+=m[i]
        out.append(t)
    # pieces whose insertion index == len(toks)
    return ''.join(out)
def pieces_of(line):
    return [int(x,16) for x in re.findall(r'<\$([0-9A-F]{2})><\$20>',line)]
L=text.split('\n')
def ln(n): return L[n-1]
rew={ # PT line numbers
 200:('uchi keshi','Os dois'),
 212:('uchi keshi','teve'),
 380:(['kū','kan',' kiri',' sai','ta'],'O espaço'),
 422:(['kara','da',' sō'],'Erva'),
 452:(['kara','da',' naka',' sō'],'A erva'),
 506:(['zan','zō'],'imagem'),
 554:(['kai','giri'],'Corte'),
 800:(['kaze',' aya','tsuri',' uki',' aga','tta'],'Jin'),
 962:(['shi',' hai',' sha',' ki',' rai'],'Mina'),
 1040:(['shi',' no',' mai'],'Dança'),
 1220:('Gi tai','Forma'),
 1430:(['mi',' kan','ja'],'atendo'),
 1593:(['Res','shū',' ōzan','kya','ku'],'Chute'),
 1671:(['fuyō','ka',' ma','kai',' sho','ku','bu','tsu'],'Planta'),
 974:(['Pine','apple'],'Granada'),
 992:(['Tra','ce','Eye'],'Bomba'),
 1016:(['Tra','ce','Eye'],'Bomba'),
}
done=set()
for n,(s,st) in rew.items():
    new=place(ln(n),ruby(s),start_text=st); L[n-1]=new; done.add(n)
    print(n,new)
# robust repair of remaining <name> lines
nrep=0
for n,l in enumerate(L,1):
    if l.startswith('//') or l.startswith('#') or not l.strip() or n in done: continue
    pc=pieces_of(l)
    if not pc or '<name' not in l: continue
    toks=tokens(l); 
    # index of first plain char before which first piece sits
    m=re.search(r'<\$[0-9A-F]{2}><\$20>',l)
    before=strip(l[:m.start()]); bt=tokens(before) if before else []
    sidx=sum(1 for t in bt if not t.startswith('<'))
    # only needed if a piece lies after <name>
    if not re.search(r'<name2?>[^<]*(<\$[0-9A-F]{2}><\$20>)',l) and '<name' in l[m.start():] is False: pass
    pcs=[(c,ink_tiles(c) or 1) for c in pc]
    try: new=place(l,pcs,start_idx=sidx)
    except Exception as e: print('skip',n,e); continue
    if new!=l: L[n-1]=new; nrep+=1
print('repaired name-lines',nrep)
open('ptBR/battle_text_PTBR.txt','w',encoding='utf-8').write('\n'.join(L))
open('ptBR/Font/ruby_extra.bin','wb').write(bytes(EX))
print('free left',len(free),'alloc',len(alloc))
