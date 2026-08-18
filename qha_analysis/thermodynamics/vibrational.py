# qha_analysis/thermodynamics/vibrational.py

import numpy as np

from ..model.qha_point import QHAPoint


KB_EV_K = 8.617333262e-5


def vibrational_internal_energy(
    point: QHAPoint,
    temperature: float,
    zero_threshold: float = 0.01,
) -> float:
    """
    Calculate the vibrational internal energy at a given temperature.

    Parameters
    ----------
    point : QHAPoint
        QHA data at a fixed volume.

    temperature : float
        Temperature in K.

    zero_threshold : float, optional
        Phonon energies with |hbar*omega| below this value
        are treated as zero modes and excluded.
        Unit: meV.

    Returns
    -------
    float
        Vibrational internal energy in eV.
    """

    eps = _active_phonon_energies(point, zero_threshold)
    eps = eps * 1.0e-3  # meV -> eV

    # Zero-temperature limit
    if temperature == 0.0:
        return 0.5 * np.sum(eps)

    kBT = KB_EV_K * temperature

    return np.sum(
        0.5 * eps
        + eps / np.expm1(eps / kBT)
    )


def vibrational_free_energy(
    point: QHAPoint,
    temperature: float,
    zero_threshold: float = 0.01,
) -> float:
    """
    Calculate the vibrational Helmholtz free energy
    at a given temperature.

    Returns
    -------
    float
        Vibrational Helmholtz free energy in eV.
    """

    eps = _active_phonon_energies(point, zero_threshold)
    eps = eps * 1.0e-3  # meV -> eV

    # Zero-temperature limit: F_vib = ZPE
    if temperature == 0.0:
        return 0.5 * np.sum(eps)

    kBT = KB_EV_K * temperature

    return np.sum(
        0.5 * eps
        + kBT * np.log(-np.expm1(-eps / kBT))
    )


def _active_phonon_energies(
    point: QHAPoint,
    zero_threshold: float,
) -> np.ndarray:
    """
    Return non-zero real phonon energies in meV.
    """

    eps = np.asarray(point.frequencies, dtype=float)

    # Remove translational / numerical zero modes
    mask = np.abs(eps) >= zero_threshold
    eps = eps[mask]

    # Remaining imaginary modes indicate an unstable structure
    if np.any(eps < 0.0):
        imaginary = eps[eps < 0.0]

        raise ValueError(
            "Imaginary phonon modes found above zero threshold: "
            f"{imaginary} meV"
        )

    return eps


def internal_energy(
    point: QHAPoint,
    temperature: float,
    zero_threshold: float = 0.01,
) -> float:
    """
    Total internal energy:

        U(T,V) = E_static(V) + U_vib(T,V)
    """

    return (
        point.static_energy
        + vibrational_internal_energy(
            point,
            temperature,
            zero_threshold,
        )
    )


def free_energy(
    point: QHAPoint,
    temperature: float,
    zero_threshold: float = 0.01,
) -> float:
    """
    Total Helmholtz free energy:

        F(T,V) = E_static(V) + F_vib(T,V)
    """

    return (
        point.static_energy
        + vibrational_free_energy(
            point,
            temperature,
            zero_threshold,
        )
    )