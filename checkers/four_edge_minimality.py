import json
from math import ceil

U=[
[1,0,0,0,1,1,0],
[0,1,0,0,1,0,1],
[0,0,1,0,0,1,1],
[0,0,0,1,0,1,1],
[1,1,0,0,1,0,0],
[1,0,1,1,0,0,0],
[0,1,1,1,0,0,0],
]

Z=[[0]*7 for _ in range(7)]
for i in range(4):
    Z[i][i]=1

H2=[
[1,0,0,0,0,1,0],
[0,1,0,0,0,0,1],
[0,0,1,0,0,1,0],
[0,0,0,1,0,0,1],
[0,0,0,0,2,0,0],
[1,0,1,0,0,0,0],
[0,1,0,1,0,0,0],
]

def rowsums(a): return [sum(r) for r in a]
def colsums(a): return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]
def leq(a,b): return all(a[i][j] <= b[i][j] for i in range(len(a)) for j in range(len(a[0])))

def cut_formula(U,Z):
    n=len(U)
    best=0
    witnesses=[]
    for mi in range(1<<n):
        I=[i for i in range(n) if mi>>i&1]
        for mj in range(1<<n):
            J=[j for j in range(n) if mj>>j&1]
            s=len(I)+len(J)-n
            if s<=0:
                continue
            Ic=[i for i in range(n) if i not in I]
            Jc=[j for j in range(n) if j not in J]
            z=sum(Z[i][j] for i in I for j in J)
            u=sum(U[i][j] for i in Ic for j in Jc)
            value=ceil((z-u)/s)
            if value>best:
                best=value
                witnesses=[(I,J,s,z,u)]
            elif value==best:
                witnesses.append((I,J,s,z,u))
    return best,witnesses

def scoped_lower_bound_arithmetic():
    # If kappa_Z(U)=3 and kappa_Z(2U)<=2, the same cut must satisfy
    # z-u >= 2s+1 and z-2u <= 2s, with 0<=z<=4 and s>=1.
    possible=[]
    for s in range(1,5):
        for z in range(5):
            for u in range(10):
                if z-u >= 2*s+1 and z-2*u <= 2*s:
                    possible.append((s,z,u))
    assert possible==[(1,4,1)]
    # For a four-edge partial matching, z=4 means I contains four
    # distinct required rows and J contains four distinct required columns.
    # Since s=|I|+|J|-n=1, n >= 4+4-1 = 7.
    return {
        "only_cut_parameters":[1,4,1],
        "interpretation":"s=1, Z(I,J)=4, U(I^c,J^c)=1",
        "partial_matching_forces_n_at_least":7
    }

def main():
    assert rowsums(U)==[3]*7 and colsums(U)==[3]*7
    assert rowsums(H2)==[2]*7 and colsums(H2)==[2]*7
    assert leq(Z,U)
    assert leq(Z,H2)
    assert leq(H2,[[2*x for x in r] for r in U])

    k1,w1=cut_formula(U,Z)
    k2,w2=cut_formula([[2*x for x in r] for r in U],Z)
    assert k1==3
    assert k2==2

    I=set(range(4));J=set(range(4))
    z=sum(Z[i][j] for i in I for j in J)
    u=sum(U[i][j] for i in range(4,7) for j in range(4,7))
    assert z==4 and u==1
    assert len(I)+len(J)-7==1

    report={
      "status":"PASS",
      "scope":"four required edges forming a partial matching",
      "lower_bound":scoped_lower_bound_arithmetic(),
      "seven_state_witness":{
        "U":U,
        "Z_edges_1_based":[[1,1],[2,2],[3,3],[4,4]],
        "H2":H2,
        "kappa_Z_U":k1,
        "kappa_Z_2U":k2,
        "sharp_cut":{"I":[1,2,3,4],"J":[1,2,3,4],"s":1,"z":4,"u":1}
      }
    }
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
