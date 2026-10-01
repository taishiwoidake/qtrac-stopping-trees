# Nested Regular Covers and Stopping Trees

Reproducibility package for the frozen technical preprint:

**Nested Regular Covers and Stopping Trees: Finite Stabilization, Sharp Thresholds, and Integrality Gaps**

[Read the technical-v1 PDF](paper/preprint_v1.pdf)

## What is proved?

The publication unit contains four theorem-facing results.

**Theorem A — finite-layer stabilization.**

```math
M_r=
\sum_{d=2}^{2r-1}
\left(1+\left\lceil\log_2(d-1)\right\rceil\right)
=O(r\log r).
```

**Theorem B — sharp four-edge partial-matching threshold.**

A local transition

```math
\kappa_Z(U)=3,
\qquad
\kappa_Z(2U)=2
```

requires at least seven states in the four-edge partial-matching model, and the bound is sharp.

**Theorem C — exact integer/real integrality gap.**

```math
C_\infty^{\mathbb Z}=6,
\qquad
C_\infty^{\mathbb R}=\frac{11}{2}.
```

**Theorem D — complete stopping-tree realization.**

```math
\mathbb E T_\ell
=
\frac{29}{8}-\frac38\,2^{-\ell},
\qquad
\mathbb E T_\infty=\frac{29}{8}.
```

The analytic manuscript is in `paper/preprint_v1.tex`; the bibliography is in `paper/references.bib`.
The frozen PDF is committed at `paper/preprint_v1.pdf`.

## Verify the finite evidence

Run:

```bash
python verify.py
```

Expected summary:

```text
[PASS] snapshot integrity
[PASS] publication metadata consistency
[PASS] privacy boundary
[PASS] frozen PDF hash
[PASS] Theorem A finite construction checks
[PASS] Theorem B finite certificate
[PASS] Theorem C exact primal/dual certificate
[PASS] Theorem D stopping-tree certificate
All finite certificates and computational claims passed.
```

The command checks the public snapshot metadata, privacy boundary, frozen PDF hash when the PDF is present, and the finite certificates and computational claims shipped with this publication snapshot.

It does **not** formally verify the analytic proofs of the general theorems.

## Repository map

- `paper/preprint_v1.pdf` — frozen technical-v1 PDF.
- `paper/preprint_v1.tex` — integrated analytic manuscript.
- `paper/proofs/` — theorem-facing proof notes.
- `checkers/` — exact finite verification programs.
- `certificates/` — machine-readable certificate manifests.
- `THEOREM_MAP.md` — public claim-to-evidence scope.
- `SOURCE_MANIFEST.json` — public artifact manifest with SHA-256 digests.
- `PUBLICATION_LOCK.json` — generated snapshot lock.
- `.github/workflows/verify.yml` — finite-evidence and integrity CI.
- `.github/workflows/build-paper.yml` — read-only reproducible PDF build and frozen-hash check.

## Reproducibility scope

The theorem-facing verification code uses Python's standard library and exact integer/rational arithmetic.

The PDF build is checked for byte-for-byte reproducibility. CI rebuilds it twice from clean generated state, compares the two outputs, and verifies that the result matches the frozen PDF and SHA-256 recorded in `RELEASE.json`.

## Version

Paper version: **technical-v1**.

This repository is a frozen publication snapshot. Research-workspace provenance and unpublished research lines are deliberately excluded from the public metadata.

## Citation and license

Citation metadata and licensing are kept separate from the mathematical verification package and are finalized at publication time.
