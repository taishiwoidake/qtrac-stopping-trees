# Complete Stopping-Tree Certificate

This file gives an exact cumulative stopping-tree certificate for the corrected five-edge six-state construction.

Let

\[
A_\infty=\frac{2J_6+U}{16},
\qquad
B:=16A_\infty=2J_6+U.
\]

Let \(P\) be the permutation with row-columns \((3,5,6,2,4,1)\), and put \(H=U-P\). Then \(H\) is 3-regular and contains the negative support of the corrected perturbation \(\widehat G\).

For \(\ell\ge0\), define

\[
A_{4+\ell}=A_\infty+2^{-(4+\ell)}\widehat G,
\qquad s=4+\ell.
\]

## Finite stopping tree

Define cumulative stopped-branch matrices by

\[
N_0=N_1=N_2=0,\qquad N_3=J_6.
\]

For \(4\le t<s\), set

\[
N_t=2^tA_\infty-H=2^{t-4}B-H.
\]

At terminal depth \(s\), set

\[
N_s=2^sA_s=2^{s-4}B+\widehat G.
\]

These matrices are integer regular, satisfy the exact capacity inequalities \(N_t\le\lfloor2^tA_s\rfloor\), and obey the nesting relation

\[
N_{t+1}\ge2N_t.
\]

The nontrivial increments reduce to

\[
N_4-2N_3=P,
\]

for a nonterminal level four,

\[
N_{t+1}-2N_t=H
\]

between intermediate levels, and

\[
N_s-2N_{s-1}=\widehat G+2H\ge0
\]

at termination. For \(\ell=0\), the direct terminal increment is \(U+\widehat G\ge0\).

## Degrees and expected cost

The cumulative degree is

\[
\deg N_t=
\begin{cases}
0,&t=0,1,2,\\
6,&t=3,\\
2^t-3,&4\le t<s,\\
2^s,&t=s.
\end{cases}
\]

Therefore the exact expected fair-bit cost is

\[
3+\left(1-\frac68\right)+\sum_{t=4}^{s-1}\frac{3}{2^t}
=
\boxed{\frac{29}{8}-\frac38\,2^{-\ell}}.
\]

## Infinite limiting tree

For \(A_\infty\), use the same first four levels and, for every \(t\ge4\),

\[
N_t=2^tA_\infty-H.
\]

Then

\[
N_{t+1}-2N_t=H\ge0,
\qquad
\frac{N_t}{2^t}=A_\infty-\frac{H}{2^t}\to A_\infty.
\]

The surviving mass at every \(t\ge4\) is exactly \(3/2^t\). Hence

\[
\boxed{\mathbb E T_\infty=\frac{29}{8}}.
\]

## Verification

The repository checker `checkers/stopping_tree.py` verifies the symbolic local conditions that imply the construction for every \(\ell\ge0\), checks finite instances \(0\le\ell\le32\), and verifies the exact infinite-tail identity.

Existence of an actual permutation-valued stopping tree from the cumulative integer matrices follows from the exact integer nesting criterion recorded in the stopping/nesting line.