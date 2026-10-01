# Theorem Map — technical-v1

This file maps the public theorem labels to their analytic proofs and finite verification artifacts.

## Theorem A — Finite-layer stabilization

For deficit size \(r=|Z|\ge2\),

```math
M_r=
\sum_{d=2}^{2r-1}
\left(1+\left\lceil\log_2(d-1)\right\rceil\right)
=
O(r\log r).
```

**Analytic proof:** `paper/proofs/finite_layer.md`.

**Finite verification:** `checkers/reachability_rounding.py`.

The checker verifies the constructive rounding mechanism on exact integer fixtures and the closed-form layer count. It does not formally verify the universal analytic theorem.

## Theorem B — Sharp four-edge partial-matching threshold

For four required edges with pairwise distinct rows and columns,

```math
\kappa_Z(U)=3,
\qquad
\kappa_Z(2U)=2
```

implies

```math
n\ge7,
```

and the bound is sharp.

**Analytic proof:** `paper/proofs/four_edge_minimality.md`.

**Finite verification:** `checkers/four_edge_minimality.py` and `certificates/four_edge_minimality.json`.

## Theorem C — Exact integer/real integrality gap

For the frozen ten-state partial-matching instance,

```math
C_\infty^{\mathbb Z}=6,
\qquad
C_\infty^{\mathbb R}=\frac{11}{2}.
```

The exact gap is \(\frac12\).

**Proof and certificate explanation:** `paper/proofs/integrality_gap.md`.

**Finite verification:** `checkers/integrality_gap.py` checks the integer reachable-state graph, the explicit real primal chain, and the exact rational LP-dual identity.

## Theorem D — Complete stopping-tree realization

For the six-state dyadic family,

```math
\mathbb E T_\ell
=
\frac{29}{8}
-
\frac38\,2^{-\ell},
\qquad
\mathbb E T_\infty
=
\frac{29}{8}.
```

**Proof and certificate explanation:** `paper/proofs/stopping_tree.md`.

**Finite verification:** `checkers/stopping_tree.py` and `certificates/stopping_tree.json`.

## Verification scope

`python verify.py` independently checks the public snapshot integrity, privacy boundary, frozen PDF hash when present, and the finite certificates and computational claims shipped with this publication snapshot.

The analytic proofs are contained in the paper and proof notes and are not formally verified by the Python checkers.
