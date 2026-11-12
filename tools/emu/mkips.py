import sys
base=open(sys.argv[1],'rb').read();new=open(sys.argv[2],'rb').read()
out=bytearray(b'PATCH')
def rec(off,data):
    global out
    while data:
        if off==0x454F46:  # evita confundir com EOF
            off-=1;data=base_byte(off)+data
        n=min(len(data),0xFFFF)
        # RLE
        out+=off.to_bytes(3,'big')+n.to_bytes(2,'big')+data[:n]
        off+=n;data=data[n:]
def base_byte(o):return new[o:o+1]
i=0;L=len(new);n=len(base)
while i<L:
    if i<n and new[i]==base[i]:i+=1;continue
    j=i
    while j<L and (j>=n or new[j]!=base[j]):
        j+=1
        # junta se a proxima igualdade for curta
        k=j
        while k<L and k<n and new[k]==base[k] and k-j<8:k+=1
        if k<L and k-j<8 and k<n and k!=j and not (k>=n):
            j=k
    rec(i,new[i:j]);i=j
out+=b'EOF'
open(sys.argv[3],'wb').write(out);print(len(out))
