# Day 4 — CASSA photometry pipeline

From raw pixels off the telescope to a calibrated catalog, with an error budget
carried the whole way. One lecture, then a hands-on reduction of a full night's
data in the CASSA 8-inch's own configuration.

| File | What it is |
|---|---|
| `TDMMA-2026-CASSA-Photometry_slide.pdf` | The lecture (21 slides). |
| `TDMMA-2026-CASSA-Photometry_participant-handbook.pdf` | **Read this first.** Installation, where the data goes, and the tasks notebook by notebook. |
| `notebooks/` | The hands-on session, `00` to `04`. Run them in order. |
| `raw/` | Empty — for your **own** night. The session's dataset (NGC 7331, 77 frames) comes with the observatory clone. |

## Before the session

The handbook has the full instructions; this is the shape of them.

The pipeline itself is a separate package, so there are two things to fetch:
conda (if you have none), then the pipeline. It installs natively on **Linux,
macOS and Windows**.

**1. Miniforge**, if you do not already have conda or miniconda.

```bash
# Linux / macOS -- the installer name is built from your own machine, so this
# is the same pair of commands on Intel and ARM alike.
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

On **Windows**, download the Miniforge installer from
[conda-forge.org/download](https://conda-forge.org/download/) and run it, or
skip this step if you already have Miniconda or Anaconda.

**2. The pipeline.**

```bash
# Linux / macOS
git clone https://github.com/cassaiub/observatory.git
cd observatory/photometric_pipeline
./install.sh
conda activate cassa-photometry
cassa-doctor        # must pass before the session starts
```

```powershell
# Windows
git clone https://github.com/cassaiub/observatory.git
cd observatory\photometric_pipeline
.\install.ps1
cassa-doctor        # must pass before the session starts
```

`install.ps1` does the same things as `install.sh`. WSL works too if you already
have it for Day 2 — it is real x86-64 Linux, so use the Linux commands inside
it, and `.\install.ps1 -Wsl` prints the setup steps.

`cassa-doctor` is the check that matters. Run it the day before, not in the
first ten minutes of the session.

The installer registers the Jupyter kernel for you. If you need to do it by
hand:

```bash
python -m ipykernel install --user \
    --name cassa-photometry --display-name "Python (CASSA photometry)"
```

When a notebook opens, check the kernel name in the top-right corner reads
**`Python (CASSA photometry)`**; if not, *Kernel -> Change Kernel*. A notebook
running on the wrong kernel reports `ModuleNotFoundError: No module named
'cassa_photometry'`, which looks like a failed install but is not one.

Note this is a **different** environment from the workshop-wide one used by the
other sessions --- this pipeline needs a plate-solver binary that pip alone
cannot supply.

### Which plate solver you get, and why it does not matter

`install.sh` tries three backends and uses the first that installs: **ASTAP** (a
sub-megabyte binary that runs on every platform, ARM included), then
Astrometry.net's `solve-field`, then an in-process Python solver.
`cassa-doctor` tells you which one you have.

**Your results do not depend on the answer.** The one thing ASTAP does not
report --- the astrometric residual `ASTRMS`, which Phase 3 uses to size its
catalog cross-match --- the pipeline measures for itself, so every backend
produces it. If your neighbour has a different solver, your catalogs are still
comparable.

There is also **nothing to download in advance**. Plate solving matches your
stars against a sky catalog, and those catalogs are large (859 MB for ASTAP,
~34 GB for Astrometry.net). You need neither: the pipeline reads your frame's
pointing and field size and fetches only the pieces that field needs --- about
6 MB for ASTAP --- caching them under `~/.cache/cassa-photometry/`.

## The data

**A night comes with the pipeline.** When you clone `cassaiub/observatory` for
the install, you also get `photometric_pipeline/workshop/raw/` — one real night,
77 frames, 155 MB:

```
raw/20230822/
├── Bias/               10 frames,  0 s
├── Dark/               10 frames, 60 s
├── Flat/               43 frames,  3 s   (B 18, R 15, V 10)
└── Light/NGC7331/      14 frames, 60 s   (B 5, R 5, V 4)
```

NGC 7331, observed 2023-08-23 on an iTelescope **CDK700** with an **Andor
DU934P** CCD, 1024×1024. Real data, and the exercises are keyed to it — the
expected answers in the notebooks come from a reference reduction of exactly
these frames.

Two things about this night you will meet, and should:

- **The header's plate scale is wrong** — `SECPIX` says 0.4″/px against a truth
  of 0.5905″/px, a 32% error. The pipeline solves anyway and tells you.
- **There is no gain or read noise in the header**, so phase 1 assumes
  1.0 e⁻/ADU and 10 e⁻ and says so for every frame. Every uncertainty
  downstream is an estimate rather than a measurement. That warning is the
  pipeline being honest.

### Bringing your own night instead

Put it in this folder's `raw/`, exactly as the acquisition software wrote it,
and point the notebooks at it with `RAW_DIR`. Do not rename or reorganise
anything: the pipeline reads the tree recursively and sorts frames by their
`IMAGETYP`, `FILTER` and `EXPTIME` **headers**, never by folder name — so a flat
directory works too, and so does any other layout.

This folder's `raw/` and `work/` are both git-ignored: a night is a few hundred
MB and the reduction it produces is larger again, so nothing you generate here
gets committed. The shipped night lives in the observatory repository instead.

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
plate solver, no zero point, a health check that says STOP, macOS quarantining
the ASTAP binary. Work through that before asking; it names the cause for each.

`cassa-doctor` prints the state of the whole install in one screen. Bring that
output rather than a description. Two solver backends showing as unavailable is
**normal** — you only need one; the line that matters is `solver: in use`.
