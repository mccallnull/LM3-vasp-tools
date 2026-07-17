from pathlib import Path
import matplotlib.pyplot as plt

from aimd_analysis.reader.report_pureHO import read_report_pureHO
from aimd_analysis.reader.incar import read_incar
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

outfile = base_dir / "pureHO_profile_overlay.png"
#outfile = base_dir / "pureHO_profile_overlay_not_parent.png"

report = base_dir.parent / "tests" / "REPORT_pureHO"
incar = base_dir.parent / "tests" / "INCAR_pureHO"

profile = read_report_pureHO(report)
incar = read_incar(incar)

profile.dt = incar.potim

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
