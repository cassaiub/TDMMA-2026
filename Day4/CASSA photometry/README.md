# Day 4 — CASSA photometry pipeline

From raw pixels off the telescope to a calibrated catalog, with an error budget
carried the whole way. One lecture, then a hands-on reduction of a full night's
data in the CASSA 8-inch's own configuration.

| File | What it is |
|---|---|
| `TDMMA-2026-CASSA-Photometry_slide.pdf` | The lecture (21 slides). |
| `TDMMA-2026-CASSA-Photometry_participant-handbook.pdf` | **Read this first.** Installation, where the data goes, and the tasks notebook by notebook. |
| `notebooks/` | The hands-on session, `00` to `04`. Run them in order. |
| `raw/` | Empty — this is where your night goes. |

## Before the session

The handbook has the full instructions; this is the shape of them.

The pipeline itself is a separate package, so there are two things to fetch:

```bash
# 1. Miniforge, if you do not already have conda.
#    On Windows, do all of this inside WSL -- there is no plate solver for
#    native Windows, and without one there is no zero point.
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

# 2. The pipeline.
git clone https://github.com/cassaiub/observatory.git
cd observatory/photometric_pipeline
./install.sh
conda activate cassa-photometry
cassa-doctor        # must pass before the session starts
```

`cassa-doctor` is the check that matters. Run it the day before, not in the
first ten minutes of the session.

## The data

Put your night in `raw/`, exactly as the acquisition software wrote it:

```
raw/20260903/BIAS/untargeted/    ...fits
raw/20260903/DARK/untargeted/    ...fits
raw/20260903/FLAT/untargeted/    ...fits
raw/20260903/LIGHT/m22/          ...fits
```

Do not rename or reorganise anything. The pipeline reads the tree recursively
and sorts frames by their `IMAGETYP`, `FILTER` and `EXPTIME` **headers**, never
by folder name — so a flat directory works too, and so does any other layout.

`raw/` and `work/` are both git-ignored: a night is a few hundred MB, and the
reduction it produces is larger again. Nothing you generate here gets committed.

## The notebooks

Start JupyterLab in the `cassa-photometry` environment and work through them in
order. `00` and `01` only read; `02` to `04` each consume the previous
notebook's output.

| Notebook | What you do |
|---|---|
| `00_setup` | Confirm the environment, the package and the dataset are all found. |
| `01_raw_frame_health` | Health-check the bias, dark, flat and light frames. Ends in a go / no-go verdict — **do not skip it.** |
| `02_phase1_calibration` | Run the instrument signature removal. 2 exercises. |
| `03_phase2_integration` | Align, stack and plate-solve. 2 exercises. |
| `04_phase3_photometry` | Detect, measure, and tie to a zero point. 2 exercises, the last being your own assigned star. |

Each exercise is part-written: fill in the lines marked `TODO`, and the worked
solution around them shows what the answer is for. Six exercises in total.

## What you hand in

One line, from the last exercise of notebook `04`: which star you were assigned,
its magnitude with an uncertainty, and which half of the error budget dominates.
The handbook's last page has the format.

## If something breaks

The handbook's final section covers the failures that actually happen — no
plate solver, no zero point, a health check that says STOP. Work through that
before asking; it names the cause for each.
