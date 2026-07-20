from pathlib import Path
import matplotlib.pyplot as plt

from aimd_analysis.reader.outcar import read_outcar
from aimd_analysis.plotting.profile import plot_profile
from aimd_analysis.analysis.statistics import (
    compute_statistics,
)


# ============================================================
# Read files
# ============================================================

base_dir = Path(__file__).resolve().parent

outcar = base_dir.parent / "tests" / "OUTCAR_npt"

profile = read_outcar(outcar)

compute_statistics(profile)

# ============================================================
# Plot
# ============================================================

fig, ax = plot_profile(
    profile,
    quantity="Etot",
    color="tab:red",
    linewidth=2,
    linestyle="--",
    inset=True,
    show_statistics=True,
)

plt.show()
