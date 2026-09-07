#!/usr/bin/env python3
"""Check that this Python can run the TDMMA 2026 notebooks.

Run it two ways, because they test different things:

    python check_env.py                  # in the terminal: is the venv right?
    %run /path/to/check_env.py           # in a notebook cell: is the KERNEL right?

The second one is the one that catches the usual problem. Installing the
packages fixes your virtual environment; it does not, on its own, make
JupyterLab *use* that environment. A notebook can happily run on some other
Python that has none of them.

Deliberately written for old Python and with no imports beyond the standard
library, so that it reports a wrong interpreter instead of crashing on one.
"""

import sys

# (import name, pip name, which sessions need it)
PACKAGES = [
    ("numpy",        "numpy",        "all"),
    ("pandas",       "pandas",       "Day 1"),
    ("matplotlib",   "matplotlib",   "all"),
    ("scipy",        "scipy",        "Days 1, 4"),
    ("astropy",      "astropy",      "Days 1, 2, 3"),
    ("sklearn",      "scikit-learn", "Day 1"),
    ("alerce",       "alerce",       "Day 1"),
    ("pyarrow",      "pyarrow",      "Day 1"),
    ("healpy",       "healpy",       "Day 2"),
    ("lightkurve",   "lightkurve",   "Day 3"),
    ("ipykernel",    "ipykernel",    "kernel registration"),
]

KERNEL_NAME = "tdmma-2026"
DISPLAY_NAME = "Python (TDMMA 2026)"


def in_notebook():
    """True when running inside a Jupyter kernel rather than a terminal."""
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"
    except Exception:
        return False


def version_of(module):
    for attr in ("__version__", "version", "VERSION"):
        value = getattr(module, attr, None)
        if isinstance(value, str):
            return value
    return "?"


def main():
    notebook = in_notebook()
    where = "notebook kernel" if notebook else "terminal"

    print("=" * 68)
    print("TDMMA 2026 -- environment check (%s)" % where)
    print("=" * 68)
    print("python     %s" % sys.version.split()[0])
    print("executable %s" % sys.executable)
    print()

    if sys.version_info < (3, 10):
        print("[!] Python %d.%d is too old. The workshop needs 3.10 or newer,"
              % (sys.version_info[0], sys.version_info[1]))
        print("    because healpy 1.20 requires it.")
        print()

    missing = []
    widest = max(len(name) for name, _, _ in PACKAGES)

    for import_name, pip_name, needed_by in PACKAGES:
        try:
            module = __import__(import_name)
        except Exception:
            missing.append((pip_name, needed_by))
            print("  [ -- ] %-*s  MISSING     (%s)" % (widest, import_name, needed_by))
        else:
            print("  [ ok ] %-*s  %-10s  (%s)"
                  % (widest, import_name, version_of(module), needed_by))

    print()
    if not missing:
        print("All packages present. This %s can run every notebook." % where)
        if not notebook:
            print()
            print("That covers the terminal. Now run the same check inside a")
            print("notebook -- put this in the first cell of any notebook:")
            print()
            print("    %run ../check_env.py        # adjust the path as needed")
            print()
            print("If it fails there but passed here, the kernel is wrong, not")
            print("the environment.")
        print("=" * 68)
        return 0

    print("Missing: " + ", ".join(pip for pip, _ in missing))
    print()

    if notebook:
        print("This notebook is NOT running on the workshop environment.")
        print()
        print("The packages may well be installed -- just not in the Python this")
        print("kernel is using, which is the one printed above. Fix it by pointing")
        print("the notebook at the right kernel:")
        print()
        print("  1. In the terminal, with the environment activated, run:")
        print()
        print("         python -m ipykernel install --user \\")
        print("             --name %s --display-name \"%s\"" % (KERNEL_NAME, DISPLAY_NAME))
        print()
        print("  2. Reload the JupyterLab tab.")
        print("  3. Kernel -> Change Kernel -> \"%s\"." % DISPLAY_NAME)
        print("  4. Re-run this cell.")
    else:
        print("Install them into this environment:")
        print()
        print("    pip install -r requirements.txt")
        print()
        print("If that was already done, check the prompt shows (.venv) -- the")
        print("environment has to be activated in *this* shell.")

    print("=" * 68)
    return 1


if __name__ == "__main__":
    status = main()
    # `%run` inside a notebook also sets __name__ to "__main__", and calling
    # sys.exit() there raises SystemExit, which Jupyter renders as a traceback --
    # a crash on top of the report the participant is supposed to read. Only the
    # terminal gets an exit code.
    if not in_notebook():
        sys.exit(status)
else:
    main()
