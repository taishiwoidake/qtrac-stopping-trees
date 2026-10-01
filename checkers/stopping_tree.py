from fractions import Fraction as F
import json

U=[
[1,0,1,0,0,2],
[1,1,0,0,2,0],
[0,1,1,0,1,1],
[0,2,0,2,0,0],
[0,0,2,1,1,0],
[2,0,0,1,0,1],
]
P_COLS=[3,5,6,2,4,1]
N=6
J=[[1]*N for _ in range(N)]

P=[[0]*N for _ in range(N)]
for i,j in enumerate(P_COLS):
    P[i][j-1]=1
H=[[U[i][j]-P[i][j] for j in range(N)] for i in range(N)]

G=[[0]*N for _ in range(N)]
for i,j in [(1,2),(2,3),(2,4),(3,1),(3,5),(4,1),(5,2)]:
    G[i-1][j-1]+=1
for i,j in [(1,1),(2,1),(2,2),(3,2),(3,3),(4,4),(5,5)]:
    G[i-1][j-1]-=1

B=[[2*J[i][j]+U[i][j] for j in range(N)] for i in range(N)]

def rowsums(a): return [sum(r) for r in a]
def colsums(a): return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]
def leq(a,b): return all(a[i][j] <= b[i][j] for i in range(len(a)) for j in range(len(a[0])))
def twice(a): return [[2*x for x in r] for r in a]
def zero(): return [[0]*N for _ in range(N)]

NEG={(i,j) for i in range(N) for j in range(N) if G[i][j]<0}

def cumulative_N(t,ell):
    s=4+ell
    if t<=2: return zero()
    if t==3: return [r[:] for r in J]
    if t<s:
        q=2**(t-4)
        return [[q*B[i][j]-H[i][j] for j in range(N)] for i in range(N)]
    if t==s:
        q=2**ell
        return [[q*B[i][j]+G[i][j] for j in range(N)] for i in range(N)]
    raise ValueError("t exceeds terminal depth")

def floor_capacity(t,ell):
    s=4+ell
    out=[]
    for i in range(N):
        row=[]
        for j in range(N):
            x=F(2**t,16)*B[i][j] + F(2**t,2**s)*G[i][j]
            row.append(x.numerator//x.denominator)
        out.append(row)
    return out

def finite_certificate(ell):
    s=4+ell
    previous=None
    degrees=[]
    stopping_degrees=[]
    for t in range(s+1):
        nt=cumulative_N(t,ell)
        cap=floor_capacity(t,ell)
        assert min(x for r in nt for x in r)>=0
        assert leq(nt,cap)
        rs=rowsums(nt); cs=colsums(nt)
        assert len(set(rs+cs))==1
        degrees.append(rs[0])
        if previous is not None:
            assert leq(twice(previous),nt)
            xt=[[nt[i][j]-2*previous[i][j] for j in range(N)] for i in range(N)]
            assert min(x for r in xt for x in r)>=0
            assert len(set(rowsums(xt)+colsums(xt)))==1
            stopping_degrees.append(rowsums(xt)[0])
        previous=nt

    terminal=[[2**ell*B[i][j]+G[i][j] for j in range(N)] for i in range(N)]
    assert cumulative_N(s,ell)==terminal
    assert rowsums(terminal)==[2**s]*N and colsums(terminal)==[2**s]*N

    expected=sum(F(1)-F(degrees[t],2**t) for t in range(s))
    closed=F(29,8)-F(3,8)*F(1,2**ell)
    assert expected==closed
    return {
        "ell":ell,
        "terminal_depth":s,
        "expected_cost":str(expected),
        "cumulative_degrees":degrees,
        "new_stopping_degrees":stopping_degrees
    }

def symbolic_all_ell_certificate():
    assert rowsums(U)==[4]*N and colsums(U)==[4]*N
    assert rowsums(P)==[1]*N and colsums(P)==[1]*N
    assert rowsums(H)==[3]*N and colsums(H)==[3]*N
    assert min(x for r in H for x in r)>=0
    assert rowsums(G)==[0]*N and colsums(G)==[0]*N
    assert rowsums(B)==[16]*N and colsums(B)==[16]*N
    assert all(H[i][j]>=1 for i,j in NEG)
    assert min(U[i][j]+G[i][j] for i in range(N) for j in range(N))>=0
    assert min(2*H[i][j]+G[i][j] for i in range(N) for j in range(N))>=0
    assert leq(J,floor_capacity(3,0))
    return {
        "H_covers_negative_support":True,
        "U_plus_G_nonnegative":True,
        "twoH_plus_G_nonnegative":True,
        "t3_capacity_worst_case":True,
        "all_ell_proof_conditions":"PASS"
    }

def infinite_certificate(max_depth=40):
    previous=None
    degrees=[]
    for t in range(max_depth+1):
        if t<=2: nt=zero()
        elif t==3: nt=[r[:] for r in J]
        else:
            q=2**(t-4)
            nt=[[q*B[i][j]-H[i][j] for j in range(N)] for i in range(N)]
        assert min(x for r in nt for x in r)>=0
        assert len(set(rowsums(nt)+colsums(nt)))==1
        if previous is not None:
            assert leq(twice(previous),nt)
        previous=nt
        degrees.append(rowsums(nt)[0])
    for t in range(4,max_depth+1):
        assert 2**t-degrees[t]==3
    partial=sum(F(1)-F(degrees[t],2**t) for t in range(max_depth+1))
    tail=F(3,2**max_depth)
    assert partial+tail==F(29,8)
    return {
        "checked_depth":max_depth,
        "surviving_degree_for_t_ge_4":3,
        "exact_expected_cost":"29/8",
        "normalized_limit":"A_infty",
        "entrywise_error_formula":"H / 2^t"
    }

def main():
    report={
        "status":"PASS",
        "symbolic_all_ell":symbolic_all_ell_certificate(),
        "finite_samples":[finite_certificate(ell) for ell in range(33)],
        "infinite_tree":infinite_certificate()
    }
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
