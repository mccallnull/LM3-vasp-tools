from pathlib import Path
import matplotlib.pyplot as plt

from aimd_analysis.reader.report_pureHO import read_report_pureHO
from aimd_analysis.reader.incar import read_incar
from aimd_analysis.plotting.profile import plot_profile


# ============================================================
# Read files
# ============================================================

base_dir = Path(__file__).resolve().parent

outfile = base_dir / "profile.png"

report = base_dir.parent / "tests" / "REPORT"
incar = base_dir.parent / "tests" / "INCAR"

profile = read_report_pureHO(report)
incar = read_incar(incar)

profile.dt = incar.potim


# ============================================================
# Plot
# ============================================================

fig, ax = plot_profile(
    profile,
    quantity="Etot",
)

ax.set_title("Total Energy")

fig.tight_layout()

fig.savefig(
    str(outfile),
    dpi=300,
)

print(f"Saved: {outfile}")

plt.close(fig)
