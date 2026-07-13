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
    summary,
    slice_profile,
    block_average,
)

from pathlib import Path

EXAMPLE_DIR = Path(__file__).resolve().parent
TEST_DIR = EXAMPLE_DIR.parent / "tests"

report_file = TEST_DIR / "REPORT"
incar_file = TEST_DIR / "INCAR"

# ==========================================================
# Read REPORT / INCAR
# ==========================================================

profile = read_report_pureHO(report_file)

incar = read_incar(incar_file)
profile.dt = incar.potim


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
    start=20,
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
    block_size=10,
)

print()
print("=" * 60)
print("Block averaged MD profile")
print("=" * 60)

summary(profile_block)