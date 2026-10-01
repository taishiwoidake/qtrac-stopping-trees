from fractions import Fraction as F
from itertools import product
from collections import deque
import json

U = [
[1,0,1,0,0,2,0,0,0,0],
[0,1,0,0,2,0,1,0,0,0],
[0,0,1,0,1,1,0,0,1,0],
[0,2,0,2,0,0,0,0,0,0],
[0,0,2,1,1,0,0,0,0,0],
[2,0,0,1,0,1,0,0,0,0],
[0,0,0,0,0,0,3,1,0,0],
[1,0,0,0,0,0,0,3,0,0],
[0,0,0,0,0,0,0,0,3,1],
[0,1,0,0,0,0,0,0,0,3],
]
Z_EDGES = [(0,0),(1,1),(2,2),(6,7),(8,9)]
N=10

def zmat():
    z=[[0]*N for _ in range(N)]
    for i,j in Z_EDGES:z[i][j]=1
    return z
Z=zmat()
def rowsums(a):return [sum(r) for r in a]
def colsums(a):return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]
def leq(a,b):return all(a[i][j]<=b[i][j] for i in range(len(a)) for j in range(len(a[0])))
def twice(a):return [[2*x for x in r] for r in a]
def key(a):return tuple(tuple(r) for r in a)

def row_options(cap,low,d):
    supp=[j for j,x in enumerate(cap) if x or low[j]];out=[]
    def rec(k,rem,row):
        if k==len(supp):
            if rem==0:out.append(tuple(row))
            return
        j=supp[k];lo=low[j];hi=min(cap[j],rem)
        for v in range(lo,hi+1):
            row[j]=v;rec(k+1,rem-v,row)
        row[j]=0
    rec(0,d,[0]*len(cap));return out

def regular_matrices(cap,low,d):
    opts=[row_options(cap[i],low[i],d) for i in range(N)]
    def rec(i,chosen,col):
        if i==N:
            if all(x==d for x in col):yield [list(r) for r in chosen]
            return
        for row in opts[i]:
            nxt=[col[j]+row[j] for j in range(N)]
            if max(nxt)<=d:yield from rec(i+1,chosen+[row],nxt)
    yield from rec(0,[],[0]*N)

def has_degree(cap,low,d):return next(regular_matrices(cap,low,d),None)

def integer_certificate():
    h0s=list(regular_matrices(U,Z,3));assert len(h0s)==1
    h0=h0s[0];assert has_degree(U,Z,2) is None
    seen={key(h0):h0};q=deque([h0]);edge_count=0
    while q:
        h=q.popleft()
        assert has_degree(twice(h),Z,2) is None
        succ=list(regular_matrices(twice(h),Z,3));edge_count+=len(succ)
        for g in succ:
            if key(g) not in seen:seen[key(g)]=g;q.append(g)
    assert len(seen)==4 and edge_count==9
    assert leq(h0,twice(h0))
    return {'unique_degree3_entrance':h0,'reachable_degree3_states':len(seen),
            'degree3_edges':edge_count,'degree2_successors':0,'integer_optimum':'6'}

def Fm(rows):return [[F(x) for x in r] for r in rows]
H0R=Fm([
['1','0','1/2','0','0','2','0','0','0','0'],
['0','1','0','0','3/2','0','1','0','0','0'],
['0','0','1','0','1','1/2','0','0','1','0'],
['0','3/2','0','2','0','0','0','0','0','0'],
['0','0','2','1/2','1','0','0','0','0','0'],
['3/2','0','0','1','0','1','0','0','0','0'],
['0','0','0','0','0','0','5/2','1','0','0'],
['1','0','0','0','0','0','0','5/2','0','0'],
['0','0','0','0','0','0','0','0','5/2','1'],
['0','1','0','0','0','0','0','0','0','5/2'],
])
H1R=Fm([
['1','0','1','0','0','0','0','0','0','0'],
['0','1','0','0','0','0','1','0','0','0'],
['0','0','1','0','0','0','0','0','1','0'],
['0','0','0','2','0','0','0','0','0','0'],
['0','0','0','0','2','0','0','0','0','0'],
['0','0','0','0','0','2','0','0','0','0'],
['0','0','0','0','0','0','1','1','0','0'],
['1','0','0','0','0','0','0','1','0','0'],
['0','0','0','0','0','0','0','0','1','1'],
['0','1','0','0','0','0','0','0','0','1'],
])

def real_primal():
    UF=Fm(U);ZF=Fm(Z)
    assert rowsums(H0R)==[F(7,2)]*N and colsums(H0R)==[F(7,2)]*N
    assert rowsums(H1R)==[F(2)]*N and colsums(H1R)==[F(2)]*N
    assert leq(ZF,H0R) and leq(H0R,UF)
    assert leq(ZF,H1R) and leq(H1R,[[2*x for x in r] for r in H0R])
    cost=F(7,2)+F(2);assert cost==F(11,2)
    return {'d0':'7/2','d_q_q_ge_1':'2','cost':'11/2',
            'H0':[[str(x) for x in r] for r in H0R],
            'H1':[[str(x) for x in r] for r in H1R]}

SUPP=[(i,j) for i in range(N) for j in range(N) if U[i][j]>0]
VARS=[(q,i,j) for q in (0,1) for i,j in SUPP]+[('d',0),('d',1)]
VID={v:k for k,v in enumerate(VARS)}
def zero():return [F(0) for _ in VARS]
def add_scaled(dst,src,a):
    for i,x in enumerate(src):dst[i]+=a*x
def eq_vec(q,kind,index):
    v=zero()
    for i,j in SUPP:
        if (kind=='row' and i==index) or (kind=='col' and j==index):v[VID[(q,i,j)]]+=1
    v[VID[('d',q)]]-=1;return v
def nest_vec(e):
    i,j=e;v=zero();v[VID[(1,i,j)]]=1;v[VID[(0,i,j)]]=-2;return v
def unit(vname):
    v=zero();v[VID[vname]]=1;return v

EQ=[
((0,'row',3),2),((0,'row',4),2),((0,'row',5),2),((0,'row',7),2),((0,'row',9),2),
((0,'col',0),-2),((0,'col',1),-2),((0,'col',2),-2),((0,'col',3),-2),((0,'col',7),-2),((0,'col',9),-2),
((1,'row',1),-1),((1,'row',2),-1),((1,'row',4),-1),((1,'row',6),-1),((1,'row',8),-1),
((1,'col',2),1),((1,'col',4),1),((1,'col',6),1),((1,'col',8),1),
]
NEST=[((0,2),-1)]
LOW=[((0,0,0),2,1),((0,1,1),2,1),((0,2,2),2,1),((0,6,7),2,1),((0,8,9),2,1),
     ((1,1,1),1,1),((1,2,5),1,0),((1,4,3),1,0),((1,6,7),1,1),((1,8,9),1,1)]
UP=[((0,4,4),-2,1),((0,5,5),-2,1)]

def real_dual():
    rhs=zero()
    for (q,k,i),a in EQ:add_scaled(rhs,eq_vec(q,k,i),F(a))
    for e,a in NEST:add_scaled(rhs,nest_vec(e),F(a))
    bound=F(0)
    for v,a,lb in LOW:add_scaled(rhs,unit(v),F(a));bound+=F(a)*F(lb)
    for v,a,ub in UP:add_scaled(rhs,unit(v),F(a));bound+=F(a)*F(ub)
    target=zero();target[VID[('d',0)]]=2;target[VID[('d',1)]]=1
    assert rhs==target and bound==9
    assert all(a<=0 for _,a in NEST) and all(a>=0 for _,a,_ in LOW) and all(a<=0 for _,a,_ in UP)
    row8_support=[j for j,x in enumerate(U[7]) if x]
    assert row8_support==[0,7] and Z[0][0]==1 and Z[6][7]==1 and Z[7][0]==Z[7][7]==0
    return {'dual_bound_2d0_plus_d1':'9','tail_cut_dq_q_ge_1':'>=2','real_lower_bound':'11/2'}

def main():
    out={'integer':integer_certificate(),'real_primal':real_primal(),'real_dual':real_dual(),
         'integrality_gap':'1/2','C_infty_Z':'6','C_infty_R':'11/2'}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
