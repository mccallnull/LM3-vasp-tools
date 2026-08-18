# qha_analysis/model/qha_point.py

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass
class QHAPoint:
    """
    QHA data at a single fixed volume.

    Parameters
    ----------
    volume : float
        Cell volume in Angstrom^3.

    static_energy : float
        Static electronic energy in eV.

    frequencies : Sequence[float]
        Phonon frequencies at this volume, in meV (so, strictily speaking, hbar*omega).
        Unit convention should be defined by the reader/model interface.
    """

    volume: float
    static_energy: float
    frequencies: Sequence[float]

    def __post_init__(self):
        self.volume = float(self.volume)
        self.static_energy = float(self.static_energy)
        self.frequencies = np.asarray(
            self.frequencies,
            dtype=float,
        )

    @property
    def n_modes(self) -> int:
        return len(self.frequencies)