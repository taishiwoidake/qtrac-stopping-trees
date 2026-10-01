# Finite-Layer Tail Stabilization Theorem

Let \(Z\) be a required-edge mask with

\[
r=|Z|\ge2.
\]

Let \(U\) be an integer regular capacity matrix. A legal tail sequence is a sequence of integer regular matrices \(H_q\) satisfying

\[
Z\le H_0\le U,
\qquad
Z\le H_{q+1}\le2H_q.
\]

Write

\[
d_q=\deg H_q
\]

and use the discounted tail cost

\[
C_\infty(\boldsymbol H)
=
\sum_{q\ge0}2^{-q}d_q.
\]

Then an optimal sequence has an optimal representative that becomes constant after a number of layers depending only on \(r\), not on the ambient state count.

## 1. Degree trimming

Set

\[
B=2r-1.
\]

Suppose a legal state \(W\ge Z\) has degree at least \(2r\).

Because \(W\) is an integer regular bipartite multigraph, it decomposes into permutation matrices. For each of the \(r\) required edges, select one permutation in the decomposition containing that edge. After removing duplicates, their sum \(R\) satisfies

\[
Z\le R\le W,
\qquad
\deg R\le r.
\]

Replacing \(W\) and its entire future by the constant tail \(R,R,\ldots\) is legal.

From the layer containing \(W\), the replacement costs at most

\[
2\deg R\le2r,
\]

whereas the current layer \(W\) alone costs at least \(2r\) in the same local normalization.

Thus a degree \(\ge2r\) is never necessary in an optimal representative. Hence

\[
\boxed{\deg H_q\le B=2r-1.}
\]

## 2. Reachability lemma

Let \(A\) be integer \(d\)-regular and \(K\) integer \(k\)-regular with

\[
d>k,
\qquad
Z\le A,K,
\qquad
\operatorname{supp}K\subseteq\operatorname{supp}A.
\]

Define

\[
L(d)=1+\left\lceil\log_2(d-1)\right\rceil.
\]

Then \(K\) can be reached from \(A\) by a legal chain with at most \(L(d)\) transitions, while every intermediate matrix before \(K\) has degree \(d\).

### Construction

Choose a permutation matrix \(P\le A\) and define

\[
R_0=K+(d-k)P.
\]

Then \(R_0\) is \(d\)-regular, contains \(Z\), and has support inside \(\operatorname{supp}A\).

Given \(R_s\), form

\[
S_s=A+R_s.
\]

Every row and column sum of \(S_s\) equals \(2d\). Start with the entrywise floor

\[
\left\lfloor\frac{S_s}{2}\right\rfloor.
\]

The positions where \(S_s\) is odd form a bipartite graph of even degree at every row and column vertex. Decompose that odd-support graph into even cycles and, on every cycle, alternately round one edge up and the next down.

This produces an integer \(d\)-regular matrix \(R_{s+1}\) with

\[
R_{s+1,ij}
\in
\left\{
\left\lfloor\frac{A_{ij}+R_{s,ij}}2\right\rfloor,
\left\lceil\frac{A_{ij}+R_{s,ij}}2\right\rceil
\right\}.
\]

Because \(A,R_s\ge Z\), the rounding preserves

\[
R_{s+1}\ge Z.
\]

Because \(\operatorname{supp}R_s\subseteq\operatorname{supp}A\), support remains inside \(\operatorname{supp}A\).

Moreover,

\[
R_s\le2R_{s+1}.
\]

The positive entrywise excess above \(A\) contracts by at least a factor two up to rounding:

\[
\max_{ij}(R_{s+1,ij}-A_{ij})_+
\le
\left\lceil
\frac12
\max_{ij}(R_{s,ij}-A_{ij})_+
\right\rceil.
\]

Since every positive support entry of \(A\) is at least one and \(R_{0,ij}\le d\), the initial excess is at most \(d-1\).

After

\[
t=\left\lceil\log_2(d-1)\right\rceil
\]

rounds,

\[
R_t\le2A.
\]

The legal chain is therefore

\[
A,\ R_t,\ R_{t-1},\ldots,R_1,\ K.
\]

The first transition is legal because \(R_t\le2A\). The reversed rounded transitions are legal because \(R_s\le2R_{s+1}\). The last transition is legal because

\[
K\le R_0\le2R_1.
\]

Thus the number of transitions is at most

\[
1+t=L(d).
\]

For \(d=2\), the direct transition gives the same bound.

## 3. Removing long plateaus and degree increases

Along a legal chain, supports can only shrink.

Take a state \(A\) of degree \(d\) and the first later state \(K\) whose degree is strictly smaller than \(d\). Any states between them have degree at least \(d\).

The reachability lemma replaces that segment by at most \(L(d)\) degree-\(d\) links followed by \(K\).

This replacement cannot increase discounted cost. If \(V_K\) denotes the continuation value beginning at \(K\), then keeping \(K\) forever is feasible, so

\[
V_K\le2k<2d.
\]

Waiting \(s\) degree-\(d\) layers before entering the same continuation costs

\[
W_s
=
d\sum_{j=0}^{s-1}2^{-j}
+
2^{-s}V_K
=
2d+2^{-s}(V_K-2d),
\]

which is increasing in \(s\).

Hence an optimal representative may be chosen so that every strict degree drop occurs within \(L(d)\) layers of the preceding running-minimum degree.

## 4. Uniform finite-layer bound

There are no relevant degrees above

\[
B=2r-1.
\]

Summing the worst-case delay for every possible strict degree drop gives

\[
\boxed{
M_r
=
\sum_{d=2}^{B}
\left(
1+\left\lceil\log_2(d-1)\right\rceil
\right).
}
\]

Let

\[
h_r=
\left\lceil\log_2(B-1)\right\rceil.
\]

The sum has the exact closed form

\[
\boxed{
M_r
=
(h_r+1)(B-1)-2^{h_r}+1.
}
\]

Therefore

\[
\boxed{M_r=O(r\log r).}
\]

An optimal infinite tail can be chosen to become constant by layer \(M_r\).

Consequently the infinite optimization reduces to a finite optimization over the first \(M_r\) layers plus one terminal regular matrix.

## Verification code

The file checkers/tail/reachability_rounding.py implements the Eulerian odd-support rounding construction on exact integer fixtures and verifies the closed form for \(M_r\) for \(2\le r<100\).

The code is supplementary. The universal statement is the analytic argument above.
