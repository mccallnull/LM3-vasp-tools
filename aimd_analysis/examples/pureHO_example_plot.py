from pathlib import Path
import matplotlib.pyplot as plt

from aimd_analysis.reader.report_pureHO import read_report_pureHO
from aimd_analysis.reader.incar import read_incar
from aimd_analysis.plotting.profile import plot_profile
from aimd_analysis.analysis.statistics import (
    compute_statistics,
)


# ============================================================
# Read files
# ============================================================

base_dir = Path(__file__).resolve().parent

report = base_dir.parent / "tests" / "REPORT_pureHO"
incar = base_dir.parent / "tests" / "INCAR_pureHO"

profile = read_report_pureHO(report)
incar = read_incar(incar)

profile.dt = incar.potim

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
