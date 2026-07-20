from pathlib import Path
import matplotlib.pyplot as plt

from aimd_analysis.reader.outcar import read_outcar
from aimd_analysis.plotting.profile import plot_profile
from aimd_analysis.analysis.statistics import (
    compute_statistics,
    slice_profile,
    block_average,
)

"""
example_overlay.py

Example:
    - Slice MD trajectory
    - Block-average MD trajectory
    - Overlay time profiles
"""

# ============================================================
# Read files
# ============================================================

base_dir = Path(__file__).resolve().parent

outfile = base_dir / "profile_overlay.png"
#outfile = base_dir / "profile_overlay_not_parent.png"

outcar = base_dir.parent / "tests" / "OUTCAR_npt"

profile = read_outcar(outcar)

# ============================================================
# Slice & Block-average
# ============================================================

profile_sliced = slice_profile(profile, start=20)

profile_block = block_average(
    profile_sliced,
    block_size=10,
)

compute_statistics(profile_sliced)
compute_statistics(profile_block)

fig, ax = plot_profile(
    profile_sliced,
    "Etot",
    color="C0",
    label="Raw MD",
    show_statistics=True,
    inset=True,
)

plot_profile(
    profile_block,
    "Etot",
    ax=ax,
    color="C1",
    label="Block average",
    time_reference="parent",
)

ax.legend()

fig.savefig(
    str(outfile),
    dpi=300,
)

print(f"Saved: {outfile}")

plt.close(fig)
