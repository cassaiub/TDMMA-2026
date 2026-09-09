# Day 2 — Gravitational-Wave Follow-Up

A gravitational-wave detection does not tell you where to point. It gives you a
probability distribution smeared across hundreds or thousands of square degrees,
and a few hours before the counterpart fades. This session is the work of turning
that into a pointing list.

> **Setup is workshop-wide.** Install once from the repository root — see the
> [main README](../README.md). Windows participants need WSL for this day:
> `healpy` publishes no Windows build.

> When a notebook opens, check the kernel name in the top-right corner reads
> **`Python (TDMMA 2026)`**. If it does not, *Kernel -> Change Kernel*.

---

## `Exoplanet_TESS.ipynb` — recovering a transit from real TESS data

Not simulated data: this notebook pulls a genuine light curve out of the archive
and finds a real planet in it.

1. **Download.** `lightkurve` queries MAST for **TOI-700** (TIC 150428135),
   sector 1, and downloads the light curve. The target is a multi-planet system
   around an M dwarf, one of whose planets is Earth-sized and in the habitable
   zone.
2. **Detrend.** Flatten out the instrumental systematics and stellar variability
   that would otherwise swamp a transit. A transit is a fraction of a percent
   deep; almost everything else in the raw light curve is larger than the signal.
3. **Search.** A Box-Least-Squares periodogram over 10,000 trial periods from 0.5
   to 15 days, with transit durations from 0.05 to 0.25 days. BLS fits a box —
   flat, then a dip, then flat — because that is what a transit is, and it beats
   a Fourier method that is looking for sinusoids.
4. **Fold and measure.** Phase-fold on the recovered period, bin the result, and
   read the transit depth. Depth gives you the planet-to-star radius ratio:
   δ ≈ (R<sub>p</sub>/R<sub>*</sub>)².

**Network is needed on the first run** — the light curve comes from MAST. It is
then cached under `~/.lightkurve/`, so a second run works offline. If the venue
connection is slow, run the download cell once before the session.

### Things worth trying

- Change `sector=1` to another sector and see whether the same period comes back.
  It should. If it does not, you have found a systematic rather than a planet.
- Widen the period grid. The BLS will happily report a "best" period for pure
  noise, so the question is always whether the peak stands above the rest of the
  periodogram, not whether a peak exists.
- Try a target with no known planet and confirm you find nothing convincing.