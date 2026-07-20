"""
example_statistics_with_latparam.py

Example:
    - Read OUTCAR: only NPT!! (For NVT, lattice vectors are not read!!)
    - Print MD summary
    - Slice MD trajectory
    - Block-average MD trajectory
"""

from aimd_analysis.reader.outcar import read_outcar

from aimd_analysis.analysis.statistics import (
    compute_statistics,
    summary,
    slice_profile,
    block_average,
)

from aimd_analysis.analysis.geometry import compute_lattice_parameters

from pathlib import Path

base_dir = Path(__file__).resolve().parent

outcar= base_dir.parent / "tests" / "OUTCAR_npt"

# ==========================================================
# Read REPORT
# ==========================================================

profile = read_outcar(outcar)

# ==========================================================
# Raw MD profile
# ==========================================================

print()
print("=" * 60)
print("Raw MD profile")
print("=" * 60)

compute_lattice_parameters(profile)
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
