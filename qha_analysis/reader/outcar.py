# qha_analysis/reader/outcar.py

from pathlib import Path
from typing import List, Sequence

from ..model.qha_point import QHAPoint
from ..model.qha_model import QHAModel


def read_qha_point(path: str) -> QHAPoint:
    """
    Read a QHA point from a VASP phonon OUTCAR.

    The following quantities are extracted:

    - Cell volume in Angstrom^3
    - Static energy (first TOTEN) in eV
    - Phonon energies (hbar*omega) in meV

    Parameters
    ----------
    path : str
        Path to the VASP OUTCAR file.

    Returns
    -------
    QHAPoint
        QHA data at the fixed volume.
    """

    path = Path(path)

    volume = None
    static_energy = None
    frequencies: List[float] = []

    with path.open("r") as f:
        for line in f:

            # Cell volume
            if "volume of cell" in line:
                volume = float(line.split(":")[-1].strip())

            # Static energy:
            # first TOTEN corresponds to the undisplaced configuration
            if static_energy is None and "free  energy   TOTEN" in line:
                static_energy = float(line.split("=")[1].split()[0])

            # Phonon modes
            # Examples:
            #  1 f   = ... 63.512575 meV
            # 190 f/i = ...  0.002479 meV
            if (" f  =" in line or " f/i=" in line) and "meV" in line:
                tokens = line.split()
                mev_index = tokens.index("meV")
                frequency = float(tokens[mev_index - 1])

                # Preserve the sign of imaginary modes
                if "f/i" in line:
                    frequency = -frequency

                frequencies.append(frequency)

    if volume is None:
        raise ValueError(
            f"Cell volume was not found in {path}"
        )

    if static_energy is None:
        raise ValueError(
            f"Static energy (first TOTEN) was not found in {path}"
        )

    if not frequencies:
        raise ValueError(
            f"Phonon frequencies were not found in {path}"
        )

    return QHAPoint(
        volume=volume,
        static_energy=static_energy,
        frequencies=frequencies,
    )

def read_qha_model(paths: Sequence[str]) -> QHAModel:
    """
    Read multiple VASP phonon OUTCAR files
    and construct a QHAModel.

    Parameters
    ----------
    paths : Sequence[str]
        Paths to VASP phonon OUTCAR files.

    Returns
    -------
    QHAModel
        QHA data collected over multiple volumes.
    """

    points = [
        read_qha_point(path)
        for path in paths
    ]

    return QHAModel(points=points)