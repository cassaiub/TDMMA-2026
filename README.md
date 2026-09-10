# TDMMA 2026

Hands-on material for the workshop: the transient sky and alert brokers,
gravitational-wave follow-up, exoplanet transits, and a photometric pipeline
that takes raw telescope frames to a calibrated catalogue.

---

## 1. Installation

**One environment covers the whole workshop**, with two exceptions noted below.
Do this **before** the first session — the install pulls a few hundred megabytes.

You need **Python 3.10–3.13**. Check with `python3 --version`.

> Not 3.14 yet, if you can avoid it. Several scientific packages have not
> published wheels for it, so pip falls back to compiling them from source —
> which needs a C compiler and the Python development headers, and fails with a
> confusing `Python.h: No such file or directory` when they are missing. On
> 3.10–3.13 everything installs as a prebuilt wheel.

```bash
git clone https://github.com/cassaiub/TDMMA-2026.git
cd TDMMA-2026

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Then register this environment as a Jupyter kernel, so notebooks can find it:

```bash
python -m ipykernel install --user \
    --name tdmma-2026 --display-name "Python (TDMMA 2026)"
```

Finally, confirm it worked:

```bash
python check_env.py
```

### Starting JupyterLab, and picking the right kernel

```bash
source .venv/bin/activate      # every time you open a new terminal
jupyter lab
```

**Check the kernel name in the top-right corner of every notebook.** It should
say **`Python (TDMMA 2026)`**. If it says anything else — `Python 3
(ipykernel)`, `base`, a conda environment — click it and use
*Kernel → Change Kernel* to switch.

This is the single most common way the day goes wrong, and it looks like a
broken install rather than a wrong kernel:

> ```
> ModuleNotFoundError: No module named 'healpy'
> ```
>
> …in a notebook, on a machine where `pip install` clearly succeeded.

Installing the packages sets up your *environment*. It does not, by itself,
make Jupyter *use* that environment — particularly if you already had Anaconda
or another Jupyter on the machine, in which case `jupyter lab` may not even be
the one you just installed. Registering the kernel above is what connects the
two, and the name in the corner is how you confirm it.

To check from inside a notebook rather than by eye, run this in the first cell:

```python
%run ../check_env.py        # one ../ per directory below the repository root
```

It prints which Python the *kernel* is using, lists every package with its
version, and if something is missing tells you whether the problem is the
environment or the kernel — those have different fixes.

### Windows: use WSL

`healpy`, which Day 2 needs for HEALPix sky maps, publishes wheels for Linux and
macOS only and does not build from source on Windows. There is no way around
that, so **the workshop-wide environment needs WSL**:

```powershell
wsl --install
```

Reboot when prompted, open **Ubuntu** from the Start menu, finish creating your
user, and then follow the Linux instructions above inside that shell. Your
Windows drives are visible under `/mnt/c`, but keep the repository inside the
Linux filesystem — it is considerably faster.

> **Day 4's pipeline is the exception**: it installs and runs natively on
> Windows (`.\install.ps1`), because its plate solver publishes a Windows
> build. You will have WSL for Day 2 regardless, so either works — but if you
> only ever want to run the photometry pipeline, you do not need WSL at all.

### Network

Most notebooks run offline once installed. Three steps reach out:

| Step | What it fetches |
|---|---|
| Day 1, alert triage | live ZTF alerts from the ALeRCE broker |
| Day 3, exoplanets | a TESS light curve from MAST, cached in `~/.lightkurve/` |
| Days 1–2, observability | Astropy's observatory registry, cached after the first call |

Day 1 has an offline fallback if the broker is unreachable — see
[`Day1/README.md`](Day1/README.md).

### The two exceptions

These do **not** use the environment above:

| Session | How it installs |
|---|---|
| `Day3/Ground based follow up/` | See the handbook in that folder. |
| `Day4/CASSA photometry/` | Clone [`cassaiub/observatory`](https://github.com/cassaiub/observatory), then run `./install.sh` (Linux/macOS/WSL) or `.\install.ps1` (Windows) and `conda activate cassa-photometry`. It needs a plate-solver binary, which pip alone cannot supply — the installer handles it, and registers the Jupyter kernel. Full instructions are in that session's participant handbook. |

---

## 2. The workshop, day by day

### Day 1 — the transient sky, surveys and alert brokers

Four notebooks: compact-object physics (pulsar spin-down, Kerr ISCO, a TOV
neutron-star model), what powers a transient light curve (Arnett
<sup>56</sup>Ni decay, Malmquist bias), how a survey finds one (difference
imaging, then a real/bogus classifier), and the main practical — triaging live
ZTF alerts down to a single spectroscopic trigger.

Detail: [`Day1/README.md`](Day1/README.md).

### Day 2 — gravitational-wave follow-up

`Day2/GW_followup.ipynb`. Build a HEALPix probability sky map for a
gravitational-wave event, reduce it to 50% and 90% credible regions, tile those
regions with a telescope field of view, rank the tiles by contained probability,
and then check whether the best tile is actually observable from your site at
your observing time. The observatory and the event position are both meant to be
changed — put your own in.

Detail: [`Day2/README.md`](Day2/README.md).

### Day 3 — exoplanets, and ground-based follow-up

`Day3/Exoplanet_TESS.ipynb` downloads a real TESS light curve for TOI-700, flattens
out the systematics, runs a Box-Least-Squares periodogram to recover the transit
period, and phase-folds to measure the depth.

`Day3/Ground based follow up/` is a separate session with its own handbook.

Detail: [`Day3/README.md`](Day3/README.md).

### Day 4 — supernova cosmology, and a photometric pipeline

`Day4/SNCosmo.ipynb` generates a mock Type Ia sample, plots the Hubble diagram,
and fits Ω<sub>m</sub> by χ² minimisation against a flat ΛCDM model. Despite the
filename it needs nothing beyond NumPy and SciPy.

`Day4/CASSA photometry/` is the full reduction pipeline — raw frames to a
calibrated magnitude with an error budget carried the whole way. It installs
separately, and has its own handbook.

Detail: [`Day4/README.md`](Day4/README.md).
