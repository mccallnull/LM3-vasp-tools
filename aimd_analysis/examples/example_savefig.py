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

outfile = base_dir / "profile.png"

outcar = base_dir.parent / "tests" / "OUTCAR_npt"

profile = read_outcar(outcar)

compute_statistics(profile)

# ============================================================
# Plot
# ============================================================

fig, ax = plot_profile(
    profile,
    quantity="Etot",
)

ax.set_title("Total Energy")

fig.savefig(
    str(outfile),
    dpi=300,
)

print(f"Saved: {outfile}")

plt.close(fig)
