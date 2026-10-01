from math import ceil, log2
import json, random

def rowsums(a):return [sum(r) for r in a]
def colsums(a):return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]
def leq(a,b):return all(a[i][j]<=b[i][j] for i in range(len(a)) for j in range(len(a[0])))
def support_subset(a,b):return all(a[i][j]==0 or b[i][j]>0 for i in range(len(a)) for j in range(len(a)))
def regular(a):
    r=rowsums(a);c=colsums(a)
    return len(set(r+c))==1
def perfect_matching_support(a):
    n=len(a)
    def rec(i,used,out):
        if i==n:return tuple(out)
        for j in range(n):
            if a[i][j]>0 and j not in used:
                z=rec(i+1,used|{j},out+[j])
                if z is not None:return z
        return None
    p=rec(0,set(),[]);assert p is not None
    P=[[0]*n for _ in range(n)]
    for i,j in enumerate(p):P[i][j]=1
    return P
def balanced_half(S):
    n=len(S);B=[[x//2 for x in row] for row in S]
    odd={(i,j) for i in range(n) for j in range(n) if S[i][j]%2}
    assert all(sum((i,j) in odd for j in range(n))%2==0 for i in range(n))
    assert all(sum((i,j) in odd for i in range(n))%2==0 for j in range(n))
    adj={('r',i):[] for i in range(n)}|{('c',j):[] for j in range(n)}
    for i,j in odd:
        adj[('r',i)].append(('c',j));adj[('c',j)].append(('r',i))
    unused={frozenset((('r',i),('c',j))) for i,j in odd};up=set()
    while unused:
        e=next(iter(unused));u,v=tuple(e);start=u;cur=u;trail=[]
        while True:
            candidates=[w for w in adj[cur] if frozenset((cur,w)) in unused]
            if not candidates:break
            w=candidates[0];unused.remove(frozenset((cur,w)));trail.append((cur,w));cur=w
            if cur==start:break
        assert cur==start and len(trail)%2==0
        for t,(u,v) in enumerate(trail):
            if t%2==0:
                rr=u if u[0]=='r' else v;cc=v if v[0]=='c' else u
                up.add((rr[1],cc[1]))
    for i,j in up:B[i][j]+=1
    d=rowsums(S)[0]//2
    assert rowsums(B)==[d]*n and colsums(B)==[d]*n
    return B
def reach(A,K,Z):
    n=len(A);d=rowsums(A)[0];k=rowsums(K)[0]
    assert d>k and regular(A) and regular(K)
    assert rowsums(A)==[d]*n and colsums(A)==[d]*n
    assert rowsums(K)==[k]*n and colsums(K)==[k]*n
    assert leq(Z,A) and leq(Z,K) and support_subset(K,A)
    if d<=2:
        assert leq(K,[[2*x for x in r] for r in A]);return [A,K]
    P=perfect_matching_support(A)
    R=[[K[i][j]+(d-k)*P[i][j] for j in range(n)] for i in range(n)]
    assert rowsums(R)==[d]*n and colsums(R)==[d]*n and leq(Z,R) and support_subset(R,A)
    seq=[R];t=ceil(log2(d-1))
    for _ in range(t):
        S=[[A[i][j]+R[i][j] for j in range(n)] for i in range(n)]
        Rn=balanced_half(S)
        assert leq(Z,Rn) and support_subset(Rn,A)
        assert leq(R,[[2*x for x in r] for r in Rn])
        R=Rn;seq.append(R)
    assert leq(seq[-1],[[2*x for x in r] for r in A])
    chain=[A]+list(reversed(seq[1:]))+[K]
    for X,Y in zip(chain,chain[1:]):assert leq(Y,[[2*x for x in r] for r in X])
    assert len(chain)-1==1+t
    return chain
def pmatrix(p):
    n=len(p);a=[[0]*n for _ in range(n)]
    for i,j in enumerate(p):a[i][j]+=1
    return a
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sum_mats(ms):
    a=[[0]*len(ms[0]) for _ in range(len(ms[0]))]
    for m in ms:a=add(a,m)
    return a
def main():
    random.seed(7);fixtures=[]
    for n in range(3,8):
        for d in range(2,8):
            k=max(1,d//2)
            perms=[random.sample(range(n),n) for _ in range(d)]
            A=sum_mats([pmatrix(p) for p in perms]);K=sum_mats([pmatrix(p) for p in perms[:k]])
            Z=[[0]*n for _ in range(n)]
            for i in range(min(n,k+1)):
                j=next(j for j,x in enumerate(K[i]) if x);Z[i][j]=1
            chain=reach(A,K,Z);L=1+ceil(log2(d-1))
            assert len(chain)-1<=L
            fixtures.append({'n':n,'d':d,'k':k,'links':len(chain)-1,'bound':L})
    formulas=[]
    for r in range(2,100):
        B=2*r-1;h=ceil(log2(B-1))
        M=sum(1+ceil(log2(d-1)) for d in range(2,B+1))
        closed=(h+1)*(B-1)-2**h+1
        assert M==closed;formulas.append({'r':r,'B':B,'M':M})
    print(json.dumps({'status':'PASS','reachability_fixtures':fixtures,'finite_layer_formulas':formulas},indent=2))
if __name__=='__main__':main()
