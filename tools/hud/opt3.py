from hudlib import *
def group(tr,k,c,gg=3):
    # kanji first then translation
    w=word(tr); kw=sum(K[ch].shape[1] for ch in k)+(len(k)-1)
    return kw+gg+w.shape[1]
def build(tr,centers,gg=3):
    L=np.zeros((8,256),np.uint8); spans=[]
    for (t,k,c),cx in zip(zip(tr,['体力','気','霊'],[1,2,3]),centers):
        w=group(t,k,c,gg); x=cx-w//2; x0=x
        for j,ch in enumerate(k):
            g=K[ch]
            for r in range(8):
                for cc in range(g.shape[1]):
                    if r<g.shape[0] and g[r,cc]: L[r,x+cc]=c
            x+=g.shape[1]+(1 if j<len(k)-1 else 0)
        x+=gg-(0)
        g=word(t)
        for r in range(6,14):
            for cc in range(g.shape[1]):
                if g[r,cc]: L[r-6,x+cc]=c
        spans.append((x0,x0+w))
    return L,spans
if __name__=='__main__':
    for name,tr in [('EN',['Life','Spirit','Energy']),('PT',['Vida','Espírito','Energia'])]:
        for cs in [(43,128,213),(48,128,208)]:
            L,sp=build(tr,cs)
            cols=sorted({x//8 for a,b in sp for x in range(a,b)})
            print(name,cs,sp,len(cols))
