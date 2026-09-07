# Day 1 — The Transient Sky, Surveys and Alert Brokers

From the physics of what explodes, to how a survey finds it, to pulling a real
alert out of a live broker and asking a telescope to observe it tonight.

---

## 1. Installation

Day 1 uses the workshop-wide environment — **one environment covers every day**
except the two sessions that install separately (Day 3's ground-based follow-up
and Day 4's photometry pipeline).

Do this **before** the session, not during it. You need **Python 3.10 or newer**.

```bash
git clone https://github.com/cassaiub/TDMMA-2026.git
cd TDMMA-2026

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

On **Windows**, do all of this inside WSL — Day 2 needs `healpy`, which has no
Windows build. The root [`README.md`](../README.md) has the one-time WSL setup.

Then check it worked:

```bash
python -c "import numpy, pandas, matplotlib, scipy, sklearn, astropy, pyarrow; from alerce.core import Alerce; print('Day 1 environment OK')"
```

If that raises `ModuleNotFoundError`, the install did not finish — re-run
`pip install -r requirements.txt` and read the error rather than scrolling past
it.

### Start JupyterLab

```bash
jupyter lab
```

Leave the virtual environment activated in that terminal. Everything below runs
inside JupyterLab.

### What Day 1 uses from that environment

| Package | Needed for |
|---|---|
| `jupyterlab` | running the notebooks at all; also supplies IPython |
| `numpy`, `pandas`, `matplotlib` | every notebook |
| `scipy` | TOV integration, and PSF matching for difference imaging |
| `astropy` | coordinates, times and the observability window |
| `alerce`, `requests` | querying the ALeRCE alert broker |
| `pyarrow` | reading the offline alert dataset (Parquet) |
| `scikit-learn` | the real/bogus classifier in the survey notebook |

### Network

Two steps reach the internet:

- **ALeRCE broker queries** in the alert-triage notebook.
- **`EarthLocation.of_site('ctio')`**, which downloads Astropy's observatory
  registry the first time and caches it afterwards.

If the connection is unreliable on the day, the alert session has an offline
path — see the note under `Alert_Brokers/` below.

---

## 2. The day's hands-on

Four notebooks. The three at the top level are self-contained and can be run in
any order; `Alert_Brokers/` is the main practical session and comes last.

```
Day1/
├── Compact_Object_Physics.ipynb
├── EM_TransintSky.ipynb
├── Modern_Survey_Astronomy.ipynb
└── Alert_Brokers/
    ├── notebooks/01_Alert_Triage_Master.ipynb
    ├── modules/observability.py
    ├── data/reference_alerts.parquet
    └── generate_failsafe.py
```

### `Compact_Object_Physics.ipynb` — what is left behind

The numerical suite for compact objects. Pulsar spin-down: surface dipole
magnetic field and characteristic age from a measured period and period
derivative. Kerr black holes: the ISCO radius and the radiative efficiency of a
thin accretion disc, from a non-spinning hole to the Thorne limit. And a
Tolman–Oppenheimer–Volkoff integration — hydrostatic equilibrium in general
relativity — giving a neutron star's mass and radius from its central density.

### `EM_TransintSky.ipynb` — why transients look the way they do

The Arnett model: energy deposited by the radioactive decay chain
<sup>56</sup>Ni → <sup>56</sup>Co, which is what powers a Type Ia light curve.
Change the nickel mass and watch the peak move. Then Malmquist bias — how the
accessible survey volume scales with absolute magnitude at a Rubin-like limiting
depth, and why a magnitude-limited survey sees a biased sample of the universe.

### `Modern_Survey_Astronomy.ipynb` — how a survey finds them

Difference imaging, end to end on simulated data. Build a science and a
reference image with different seeing, derive the PSF-matching kernel that makes
the reference match the science frame, subtract, and see the transient appear in
the residual.

Then the problem every survey actually has: the difference image is full of
artefacts. A random-forest classifier is trained to separate real detections from
bogus ones, and scored with a confusion matrix.

### `Alert_Brokers/` — the main session

`notebooks/01_Alert_Triage_Master.ipynb`. ZTF and Rubin produce millions of optical
alerts a night. You have **one 30-minute spectroscopic slot** on the Las Cumbres
Observatory 2-metre at Cerro Tololo, and you have to decide what to point it at.

1. **Broker ingestion** — query ALeRCE for recent candidates.
2. **Filtering and light-curve morphology** — apply the three triage rules
   (baseline, outburst symmetry, colour cooling) that separate a young Type Ia
   from an AGN or cataclysmic variable the classifier got wrong.
3. **Cross-catalogue association** — check your candidate against the archives.
   A long photometric history means it is not new, and the trigger is wasted.
4. **Observability** — is the target actually above the horizon at Cerro Tololo,
   at an airmass you can work at?
5. **Payload submission** — build the observation request and submit it to a mock
   LCO Observation Portal, which validates your coordinates, exposure time,
   airmass constraint and instrument configuration, and tells you exactly which
   one you got wrong.

**Run it from its own directory**, so that the notebook can find
`modules/observability.py` and `data/`:

```bash
cd Alert_Brokers/notebooks
jupyter lab 01_Alert_Triage_Master.ipynb
```

**If the broker is unreachable**, set `USE_LIVE_API = False` near the top of the
notebook. It then reads `data/reference_alerts.parquet` instead, and the whole
session works offline. To rebuild that file:

```bash
cd Alert_Brokers
python generate_failsafe.py
```

It fetches live objects if it can, and falls back to a synthetic dataset if it
cannot — either way the notebook has something to work with.
