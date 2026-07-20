from aimd_analysis.reader.outcar import read_outcar

from pathlib import Path

base_dir = Path(__file__).resolve().parent

outcar = base_dir.parent / "tests" / "OUTCAR_npt"

# ==========================================================
# Read REPORT / INCAR
# ==========================================================

profile = read_outcar(outcar)

print(profile.step)
