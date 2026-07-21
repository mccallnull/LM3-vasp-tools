"""
example_statistics.py

Example:
    - Read REPORT and INCAR
    - Print MD summary
    - Slice MD trajectory
    - Block-average MD trajectory
"""

from aimd_analysis.reader.report_pureHO import read_report_pureHO
from aimd_analysis.reader.incar import read_incar

from aimd_analysis.analysis.statistics import (
    compute_statistics,
    summary,
    slice_profile,
    block_average,
)

from pathlib import Path

base_dir = Path(__file__).resolve().parent

report = base_dir.parent / "tests" / "REPORT_pureHO"
incar = base_dir.parent / "tests" / "INCAR_pureHO"

# ==========================================================
# Read REPORT / INCAR
# ==========================================================

profile = read_report_pureHO(report)

incar = read_incar(incar)
profile.dt = incar.potim
profile.stride = incar.ml_outblock
profile.first_step = incar.ml_outblock


# ==========================================================
# Raw MD profile
# ==========================================================

print()
print("=" * 60)
print("Raw MD profile")
print("=" * 60)

compute_statistics(profile)
summary(profile, verbose=True)


# ==========================================================
# Slice profile
# ==========================================================

profile_sliced = slice_profile(
    profile,
    start=20,
)

print()
print("=" * 60)
print("Sliced MD profile")
print("=" * 60)

compute_statistics(profile_sliced)
summary(profile_sliced, verbose=True)


# ==========================================================
# Block averaged profile
# ==========================================================

profile_block = block_average(
    profile_sliced,
    block_size=10,
)

print()
print("=" * 60)
print("Block averaged MD profile")
print("=" * 60)

compute_statistics(profile_block)
summary(profile_block, verbose=True)
