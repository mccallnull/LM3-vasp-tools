"""
example_statistics.py

Example:
    - Read REPORT and INCAR
    - Print MD summary
    - Slice MD trajectory
    - Block-average MD trajectory
"""

from io.report_pureHO import read_report_pureHO
from io.incar import read_incar

from analysis.statistics import (
    summary,
    slice_profile,
    block_average,
)


# ==========================================================
# Read REPORT / INCAR
# ==========================================================

profile = read_report_pureHO("../tests/REPORT")

incar = read_incar("../tests/INCAR")
profile.dt = incar.POTIM


# ==========================================================
# Raw MD profile
# ==========================================================

print()
print("=" * 60)
print("Raw MD profile")
print("=" * 60)

summary(profile)


# ==========================================================
# Slice profile
# ==========================================================

profile_sliced = slice_profile(
    profile,
    start=10000,
)

print()
print("=" * 60)
print("Sliced MD profile")
print("=" * 60)

summary(profile_sliced)


# ==========================================================
# Block averaged profile
# ==========================================================

profile_block = block_average(
    profile_sliced,
    block_size=100,
)

print()
print("=" * 60)
print("Block averaged MD profile")
print("=" * 60)

summary(profile_block)