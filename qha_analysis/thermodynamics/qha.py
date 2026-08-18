# qha_analysis/thermodynamics/qha.py

import numpy as np

from ..model.qha_model import QHAModel
from .vibrational import (
    vibrational_internal_energy,
    vibrational_free_energy,
    internal_energy,
    free_energy,
)


def vibrational_internal_energies(
    model: QHAModel,
    temperature: float,
    zero_threshold: float = 0.01,
) -> np.ndarray:
    return np.asarray([
        vibrational_internal_energy(
            point,
            temperature,
            zero_threshold,
        )
        for point in model.points
    ])


def vibrational_free_energies(
    model: QHAModel,
    temperature: float,
    zero_threshold: float = 0.01,
) -> np.ndarray:
    return np.asarray([
        vibrational_free_energy(
            point,
            temperature,
            zero_threshold,
        )
        for point in model.points
    ])


def internal_energies(
    model: QHAModel,
    temperature: float,
    zero_threshold: float = 0.01,
) -> np.ndarray:
    return np.asarray([
        internal_energy(
            point,
            temperature,
            zero_threshold,
        )
        for point in model.points
    ])


def free_energies(
    model: QHAModel,
    temperature: float,
    zero_threshold: float = 0.01,
) -> np.ndarray:
    return np.asarray([
        free_energy(
            point,
            temperature,
            zero_threshold,
        )
        for point in model.points
    ])