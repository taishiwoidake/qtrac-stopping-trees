# Exact Integer/Real Integrality Gap

For the ten-state partial-matching lift \(U',Z'\), define a legal nested sequence by

\[
Z'\le H_0\le U',
\qquad
Z'\le H_q,
\qquad
H_{q+1}\le2H_q,
\]

with every \(H_q\) regular of degree \(d_q\).

The infinite discounted cost is

\[
C_\infty
=
\sum_{q\ge0}2^{-q}d_q.
\]

The repository contains an exact certificate of

\[
\boxed{
C_\infty^{\mathbb Z}=6,
\qquad
C_\infty^{\mathbb R}=\frac{11}{2}.
}
\]

Hence the exact integrality gap is

\[
\frac12.
\]

## Integer optimum

The checker exhaustively enumerates the integer degree-three entrance states under \(U'\) and \(Z'\).

There is one degree-three entrance state.

Under the nesting transition \(H'\le2H\), the reachable degree-three state graph closes after four states and nine directed transitions. None of those four states admits a degree-two successor covering \(Z'\).

Therefore an integer chain starting at degree three cannot drop directly to degree two while it remains in the degree-three sector.

If a chain ever uses degree at least four before dropping, the discounted increase exactly cancels the maximum possible later saving relative to the constant degree-three chain. Thus every integer chain has cost at least six.

The constant degree-three chain is legal and has cost

\[
3\sum_{q\ge0}2^{-q}=6.
\]

Therefore

\[
C_\infty^{\mathbb Z}=6.
\]

## Real upper bound

The checker contains explicit rational regular matrices \(H_0^{\mathbb R}\) and \(H_1^{\mathbb R}\) with

\[
\deg H_0^{\mathbb R}=\frac72,
\qquad
\deg H_1^{\mathbb R}=2,
\]

\[
Z'\le H_0^{\mathbb R}\le U',
\qquad
Z'\le H_1^{\mathbb R}\le2H_0^{\mathbb R}.
\]

Taking

\[
H_q^{\mathbb R}=H_1^{\mathbb R}
\qquad(q\ge1)
\]

gives

\[
C_\infty^{\mathbb R}
\le
\frac72
+
2\sum_{q\ge1}2^{-q}
=
\frac{11}{2}.
\]

## Real lower bound

The checker verifies an exact finite LP dual certificate for

\[
2d_0+d_1\ge9.
\]

The certificate is an integer linear combination of:

- row-regularity equalities;
- column-regularity equalities;
- one nesting inequality;
- active lower bounds;
- active upper-capacity bounds.

No floating-point optimization is used to validate the certificate.

A separate cut gives

\[
d_q\ge2
\qquad(q\ge1).
\]

Indeed, row 8 of \(U'\) is supported only on columns 1 and 8, while those two columns contain two required \(Z'\)-entries outside row 8. Regularity therefore gives

\[
2d_q\ge d_q+2.
\]

Consequently,

\[
\begin{aligned}
C_\infty^{\mathbb R}
&=
d_0+\frac12d_1+\sum_{q\ge2}2^{-q}d_q\\
&\ge
\frac12(2d_0+d_1)
+
\sum_{q\ge2}2^{-q}\,2\\
&\ge
\frac92+1
=
\frac{11}{2}.
\end{aligned}
\]

Together with the explicit real chain,

\[
C_\infty^{\mathbb R}=\frac{11}{2}.
\]

## Verification

Run

\[
\texttt{python -O checkers/integrality_gap.py}.
\]

The checker uses only Python's standard library and exact rational/integer arithmetic.
