# Day 2 — Gravitational-Wave Follow-Up

A gravitational-wave detection does not tell you where to point. It gives you a
probability distribution smeared across hundreds or thousands of square degrees,
and a few hours before the counterpart fades. This session is the work of turning
that into a pointing list.

> **Setup is workshop-wide.** Install once from the repository root — see the
> [main README](../README.md). Windows participants need WSL for this day:
> `healpy` publishes no Windows build.

---

```
Day2/
└── GW_followup.ipynb
```

## `GW_followup.ipynb` — from a sky map to a pointing list

Five steps, run top to bottom.

1. **Build the sky map.** A mock HEALPix probability density at `nside = 64`, a
   Gaussian on the sphere centred on the event position. HEALPix divides the sky
   into equal-area pixels, which is what makes the probability arithmetic that
   follows honest.
2. **Credible regions.** Sort pixels by probability, take the cumulative sum, and
   cut at 50% and 90%. Multiply the pixel count by the area per pixel and you
   have the localisation area in square degrees — the number that decides whether
   follow-up is feasible at all.
3. **Tiling.** Lay a grid of telescope fields (2° × 2° by default) over the
   region and integrate the probability inside each one.
4. **Ranking.** Sort the tiles by contained probability. The top three are where
   you point first, and the printout tells you what fraction of the total
   probability each one buys.
5. **Observability.** Convert the best tile to altitude and azimuth for your site
   at your observing time, and accept it only above 30° altitude. A tile holding
   most of the probability is worthless if it is below your horizon.

## Make it yours

Three things in the notebook are placeholders, and the exercise is to replace
them:

| Change | Where | Default |
|---|---|---|
| Event position | `center_ra`, `center_dec` in step 1 | RA 180°, Dec −30° |
| Observatory | `EarthLocation(...)` in step 5 | Palomar (33.356°N, 116.863°W, 1706 m) |
| Observing time | `obs_time` in step 5 | 2026-09-08 04:00 UTC |

Set the site to **Dhaka** and the time to **now**, then re-run from step 4. The
same event that was comfortably observable from California may be unobservable
from Bangladesh at that hour — which is the whole argument for a globally
distributed follow-up network.

If you move the event position, remember to move the tile grid with it:
`tile_ras` and `tile_decs` in step 3 are hard-coded to bracket the default
position.

## Notes

- Everything here runs offline once installed. Astropy may fetch its Earth
  orientation data on the first coordinate transform, which is cached afterwards.
- `healpy` needs Linux or macOS. On Windows, run the whole workshop inside WSL.
