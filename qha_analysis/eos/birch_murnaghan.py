from dataclasses import dataclass

import numpy as np
from scipy.optimize import curve_fit


@dataclass
class BirchMurnaghanFit:
    """
    Result of a third-order Birch-Murnaghan EOS fit.
    """

    e0: float
    v0: float
    b0: float
    b0_prime: float

    def energy(self, volume):
        """
        Evaluate the fitted EOS at given volume(s).
        """
        return birch_murnaghan(
            volume,
            self.e0,
            self.v0,
            self.b0,
            self.b0_prime,
        )


def birch_murnaghan(
    volume,
    e0,
    v0,
    b0,
    b0_prime,
):
    """
    Third-order Birch-Murnaghan equation of state.

    Parameters
    ----------
    volume : float or array-like
        Volume in Angstrom^3.
    e0 : float
        Minimum energy in eV.
    v0 : float
        Equilibrium volume in Angstrom^3.
    b0 : float
        Bulk modulus in eV / Angstrom^3.
    b0_prime : float
        Pressure derivative of the bulk modulus.

    Returns
    -------
    float or ndarray
        Energy in eV.
    """

    eta = (v0 / volume) ** (2.0 / 3.0)

    return (
        e0
        + 9.0 * v0 * b0 / 16.0
        * (
            (eta - 1.0) ** 3 * b0_prime
            + (eta - 1.0) ** 2 * (6.0 - 4.0 * eta)
        )
    )


def fit_birch_murnaghan(
    volumes,
    energies,
) -> BirchMurnaghanFit:
    """
    Fit energy-volume data to a third-order
    Birch-Murnaghan equation of state.
    """

    volumes = np.asarray(volumes, dtype=float)
    energies = np.asarray(energies, dtype=float)

    i_min = np.argmin(energies)

    e0_guess = energies[i_min]
    v0_guess = volumes[i_min]

    # Reasonable initial guesses
    b0_guess = 0.5          # eV / Angstrom^3
    b0_prime_guess = 4.0

    popt, _ = curve_fit(
        birch_murnaghan,
        volumes,
        energies,
        p0=[
            e0_guess,
            v0_guess,
            b0_guess,
            b0_prime_guess,
        ],
        maxfev=10000,
    )

    return BirchMurnaghanFit(
        e0=popt[0],
        v0=popt[1],
        b0=popt[2],
        b0_prime=popt[3],
    )