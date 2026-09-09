# Day 4 — Supernova Cosmology and the Photometric Pipeline

Two sessions. In the morning, what a sample of Type Ia supernovae tells you about
the universe. In the afternoon, the full reduction that produces one such
measurement from raw telescope frames — with an error bar you can defend.

> **Setup:** `SNCosmo.ipynb` uses the workshop-wide environment — install once
> from the repository root, see the [main README](../README.md). The photometry
> pipeline installs separately; see
> [`CASSA photometry/README.md`](CASSA%20photometry/README.md).

> When `SNCosmo.ipynb` opens, check the kernel name in the top-right corner
> reads **`Python (TDMMA 2026)`**. If it does not, *Kernel -> Change Kernel*.
> The photometry notebooks use their own environment instead --- that folder's
> README says which.

---

```
Day4/
├── SNCosmo.ipynb
└── CASSA photometry/
    ├── TDMMA-2026-CASSA-Photometry_slide.pdf
    ├── TDMMA-2026-CASSA-Photometry_participant-handbook.pdf
    ├── notebooks/     00 to 04, run in order
    └── raw/           empty — your night goes here
```

## `SNCosmo.ipynb` — measuring Ω<sub>m</sub> from a Hubble diagram

Despite the filename this needs no extra package — NumPy and SciPy only.

1. **Mock a sample.** 50 Type Ia supernovae, redshifts from 0.01 to 1.0, with
   distance moduli drawn from a fiducial flat ΛCDM cosmology
   (H₀ = 70, Ω<sub>m</sub> = 0.3, Ω<sub>Λ</sub> = 0.7) plus realistic scatter.
   Luminosity distance comes from numerically integrating
   1/√(Ω<sub>m</sub>(1+z)³ + Ω<sub>Λ</sub>).
2. **Plot the Hubble diagram.** Distance modulus against redshift, with error
   bars, and theoretical curves overlaid. At low redshift every cosmology agrees;
   the curves only separate past z ≈ 0.3, which is exactly why the 1998
   measurement needed distant supernovae.
3. **Fit.** Minimise χ² over Ω<sub>m</sub>, holding the universe flat so
   Ω<sub>Λ</sub> = 1 − Ω<sub>m</sub>. Recover the input value, and see how tightly
   50 supernovae constrain it.

### Things worth trying

- Set `num_sne` to 10, then 500. How does the uncertainty on Ω<sub>m</sub> scale?
- Restrict `z_data` to below 0.2 and refit. The constraint should collapse —
  low-redshift supernovae measure H₀, not the matter density.
- Drop the flatness assumption and fit Ω<sub>m</sub> and Ω<sub>Λ</sub>
  independently. They are degenerate along a diagonal, which is why supernovae
  alone do not pin down either one.

## `CASSA photometry/` — the reduction pipeline

The afternoon session: a lecture, then five notebooks that take a night of raw
frames from the observatory's acquisition software to a calibrated catalogue —
instrument signature removal, stacking and plate solving, source detection and a
zero point, carrying an error and a data-quality plane the whole way. You finish
by reporting the magnitude of one assigned star with an honest uncertainty.

**This session installs separately.** Plate solving needs a compiled binary
that pip alone cannot supply, so the pipeline has its own installer rather than
living in the workshop-wide environment. One command handles it — the installer
tries three solver backends and uses the first your platform can run. Windows
participants use WSL, the same WSL setup Day 2 already requires.

Read [`CASSA photometry/README.md`](CASSA%20photometry/README.md) first, then the
participant handbook PDF in that folder, which walks through installation on all
three platforms and the tasks notebook by notebook.
