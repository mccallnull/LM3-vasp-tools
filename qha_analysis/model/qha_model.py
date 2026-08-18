# qha_analysis/model/qha_model.py

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .qha_point import QHAPoint


@dataclass
class QHAModel:
    """
    Collection of QHA data evaluated at different volumes.
    """

    points: Sequence[QHAPoint]

    def __post_init__(self):
        self.points = sorted(
            self.points,
            key=lambda point: point.volume,
        )

    @property
    def volumes(self) -> np.ndarray:
        return np.asarray(
            [point.volume for point in self.points],
            dtype=float,
        )

    @property
    def static_energies(self) -> np.ndarray:
        return np.asarray(
            [point.static_energy for point in self.points],
            dtype=float,
        )

    @property
    def n_volumes(self) -> int:
        return len(self.points)