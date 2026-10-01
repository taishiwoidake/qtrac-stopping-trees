# Four-Edge Partial-Matching Minimality Theorem

## Statement

Let \(U\) be a nonnegative integer regular \(n\times n\) capacity matrix and let \(Z\le U\) be a 0–1 matrix consisting of exactly four required edges, with all four rows distinct and all four columns distinct.

Define

\[
\kappa_Z(U)
=
\min\{k:\ \exists\text{ integer }k\text{-regular }H,\ Z\le H\le U\}.
\]

If

\[
\kappa_Z(U)=3,
\qquad
\kappa_Z(2U)=2,
\]

then

\[
\boxed{n\ge7}.
\]

The bound is sharp: an explicit seven-state example exists.

## Cut characterization

For row set \(I\) and column set \(J\), put

\[
s=|I|+|J|-n.
\]

For \(s>0\), let \(Z(I,J)\) denote the total required mass in \(I\times J\) and \(U(I^c,J^c)\) the capacity in the complementary block.

The regular lower/upper-capacity feasibility problem has the exact cut formula

\[
\kappa_Z(U)
=
\max_{I,J:\ s>0}
\left\lceil
\frac{Z(I,J)-U(I^c,J^c)}{s}
\right\rceil.
\]

This is the max-flow/min-cut condition for the residual matrix \(H-Z\). Necessity also follows directly from

\[
H(I,J)-H(I^c,J^c)=ks
\]

for every \(k\)-regular \(H\).

## Seven-state lower bound

Assume \(\kappa_Z(U)=3\). Then some cut with \(s>0\) satisfies

\[
Z(I,J)-U(I^c,J^c)\ge2s+1.
\]

Write

\[
z=Z(I,J),\qquad u=U(I^c,J^c).
\]

Because \(Z\) contains only four edges, \(z\le4\).

Since \(\kappa_Z(2U)=2\), the same cut must satisfy

\[
z-2u\le2s.
\]

Thus

\[
z-u\ge2s+1,
\qquad
z-2u\le2s,
\qquad
0\le z\le4.
\]

The only integer possibility is

\[
\boxed{s=1,\qquad z=4,\qquad u=1}.
\]

Since all four required edges lie in \(I\times J\) and form a partial matching, \(I\) contains at least four distinct required rows and \(J\) contains at least four distinct required columns. Hence

\[
|I|\ge4,\qquad |J|\ge4.
\]

But \(s=1\) gives

\[
n=|I|+|J|-1\ge4+4-1=7.
\]

Therefore no admissible instance with at most six states can exhibit this partial-matching \(3\to2\) capacity-dilation transition.

## Sharp seven-state witness

Take

\[
Z=E_{11}+E_{22}+E_{33}+E_{44}
\]

and

\[
U=
\begin{pmatrix}
1&0&0&0&1&1&0\\
0&1&0&0&1&0&1\\
0&0&1&0&0&1&1\\
0&0&0&1&0&1&1\\
1&1&0&0&1&0&0\\
1&0&1&1&0&0&0\\
0&1&1&1&0&0&0
\end{pmatrix}.
\]

Then \(U\) is 3-regular. For

\[
I=J=\{1,2,3,4\},
\]

we have \(s=1\), \(Z(I,J)=4\), and \(U(I^c,J^c)=1\), so the cut formula gives \(\kappa_Z(U)\ge3\). Since \(U\) itself is a degree-three feasible cover,

\[
\kappa_Z(U)=3.
\]

For \(2U\), the explicit degree-two cover

\[
H_2=
\begin{pmatrix}
1&0&0&0&0&1&0\\
0&1&0&0&0&0&1\\
0&0&1&0&0&1&0\\
0&0&0&1&0&0&1\\
0&0&0&0&2&0&0\\
1&0&1&0&0&0&0\\
0&1&0&1&0&0&0
\end{pmatrix}
\]

satisfies

\[
Z\le H_2\le2U.
\]

The same cut gives the lower bound two, hence

\[
\kappa_Z(2U)=2.
\]

Therefore seven states are both necessary and sufficient in the four-edge partial-matching model.

## Scope

The partial-matching hypothesis is essential to this state-count lower bound. This theorem does not claim seven-state minimality for an arbitrary four-edge required mask with repeated rows or columns.

## Verification

The file `checkers/tail/four_edge_minimality.py` verifies the explicit witness, evaluates the cut formula exactly, and checks the finite arithmetic implication that forces \((s,z,u)=(1,4,1)\).