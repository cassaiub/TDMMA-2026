# TDMMA 2026

Hands-on material for the workshop: the transient sky and alert brokers,
gravitational-wave follow-up, exoplanet transits, and a photometric pipeline
that takes raw telescope frames to a calibrated catalogue.

---

## 1. Installation

**One environment covers the whole workshop**, with two exceptions noted below.
Do this **before** the first session — the install pulls a few hundred megabytes.

You need **Python 3.10 or newer**. Check with `python3 --version`.

```bash
git clone https://github.com/cassaiub/TDMMA-2026.git
cd TDMMA-2026

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Then confirm it worked:

```bash
python -c "import numpy, pandas, matplotlib, scipy, sklearn, astropy, pyarrow, healpy, lightkurve; from alerce.core import Alerce; print('TDMMA environment OK')"
```

Start JupyterLab from the repository root and keep the virtual environment
activated in that terminal:

```bash
jupyter lab
```

### Windows: use WSL

There is no native-Windows path. `healpy`, which Day 2 needs for HEALPix sky
maps, publishes wheels for Linux and macOS only and does not build from source
on Windows. Day 4's photometry pipeline has the same constraint for a different
reason — its plate solver is not packaged for Windows either.

So install WSL once and treat it as your Linux machine for the whole workshop:

```powershell
wsl --install
```

Reboot when prompted, open **Ubuntu** from the Start menu, finish creating your
user, and then follow the Linux instructions above inside that shell. Your
Windows drives are visible under `/mnt/c`, but keep the repository inside the
Linux filesystem — it is considerably faster.

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
| `Day4/CASSA photometry/` | Clone [`cassaiub/observatory`](https://github.com/cassaiub/observatory), run `./install.sh`, then `conda activate cassa-photometry`. It needs an Astrometry.net plate solver, which pip cannot supply. Full instructions are in that session's participant handbook. |

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
