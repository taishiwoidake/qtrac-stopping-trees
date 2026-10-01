# Publication Theorem Map — nested-regular-covers-v1

**Working title:** *Nested Regular Covers and Stopping Trees: Finite Stabilization, Sharp Thresholds, and Integrality Gaps*

This file defines the theorem boundary of the first public QTRAC publication unit. It is intentionally narrower than the Tail research line.

## Core theorem set

### Theorem A — Finite-layer stabilization

Canonical claim: `QTRAC-TAIL-004`.

For deficit size (r=|Z|\ge2), the infinite nested optimization admits an optimal representative that becomes constant within

\[
M_r
=
\sum_{d=2}^{2r-1}
\left(1+\left\lceil\log_2(d-1)\right\rceil\right)
=
O(r\log r).
\]

**Analytic proof:** `papers/tail/FINITE_LAYER_THEOREM.md`.

**Computational scope:** `checkers/tail/reachability_rounding.py` checks the constructive rounding mechanism on exact integer fixtures and verifies the closed-form layer count. It does not formally verify the universal analytic proof.

### Theorem B — Sharp four-edge partial-matching threshold

Canonical claim: `QTRAC-TAIL-011`.

For four required edges with pairwise distinct rows and columns,

\[
\kappa_Z(U)=3,
\qquad
\kappa_Z(2U)=2
\]

implies

\[
n\ge7,
\]

and the bound is sharp.

**Analytic proof:** `papers/tail/FOUR_EDGE_MINIMALITY.md`.

**Finite evidence:** `checkers/tail/four_edge_minimality.py` and `certificates/tail/four_edge_minimality.json`.

### Theorem C — Exact integer/real integrality gap

Canonical claim: `QTRAC-TAIL-009`.

For the frozen ten-state partial-matching lift,

\[
C_\infty^{\mathbb Z}=6,
\qquad
C_\infty^{\mathbb R}=\frac{11}{2}.
\]

The exact gap is (1/2).

**Proof and certificate explanation:** `papers/tail/INTEGRALITY_GAP.md`.

**Finite evidence:** the integer reachable-state graph, an explicit real primal chain, and an exact rational LP-dual identity are checked by `checkers/tail/integrality_gap.py`.

### Theorem D — Complete stopping-tree realization

Canonical claim: `QTRAC-TAIL-010`.

For the corrected five-edge six-state family,

\[
\mathbb E T_\ell
=
\frac{29}{8}
-
\frac38,2^{-\ell},
\]

and the limiting infinite tree realizes (A_\infty) with

\[
\mathbb E T_\infty=\frac{29}{8}.
\]

**Proof and certificate explanation:** `papers/tail/STOPPING_TREE.md`.

**Finite evidence:** `checkers/tail/stopping_tree.py` and `certificates/tail/stopping_tree.json`.

## Deliberately excluded from publication v1

The following are not part of this frozen publication unit merely because they belong to the broader Tail line:

- the generic four-edge witness outside the partial-matching theorem;
- the (r\le3) simultaneous-optimality result;
- the six-state capacity-drop development history;
- the ten-state lift as a standalone theorem;
- the open four-edge connector problem;
- QTRAC-COMP and the Vol.3 complexity line;
- the general Ximeste・Maluna line;
- Arithmetic Power-Lift;
- Closed Control and Exact Return.

Some excluded results may appear as background or motivation in the eventual paper, but they are not exported as theorem-facing public artifacts in v1.

## Verification language

The public package must distinguish analytic proof from computational evidence.

The intended public statement is:

> The verification command independently checks all finite certificates and computational claims shipped with this publication snapshot. Analytic proofs are contained in the paper and are not formally verified by these scripts.

The public package must not claim that the Python checker formally verifies the general theorems.
