"""
Trajectory convergence analysis.
Provides running statistics and convergence diagnostics.
"""

from __future__ import annotations

import numpy as np

from aimd_analysis.model.md_profile import MDProfile


def _get_quantity(
    profile: MDProfile,
    quantity: str,
) -> np.ndarray:

    data = getattr(profile, quantity)

    if data is None:
        raise ValueError(f"{quantity} is not available.")

    return data


def running_average(
    profile: MDProfile,
    quantity: str,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculate running average of a trajectory quantity.

    Parameters
    ----------
    profile
        MD profile.
    quantity
        Quantity name (e.g. "T_md", "Etot", "Epot").

    Returns
    -------
    time : ndarray
        Elapsed simulation time.
    running : ndarray
        Running average.
    """

    data = _get_quantity(profile, quantity)

    running = np.cumsum(data) / np.arange(1, len(data) + 1)

    return profile.elapsed_time, running

def moving_average(
    profile: MDProfile,
    quantity: str,
    window: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the centered moving average of a trajectory quantity.

    Parameters
    ----------
    profile : MDProfile
        Molecular dynamics trajectory.
    quantity : str
        Quantity name.
    window : int
        Moving window size (number of frames).

    Returns
    -------
    time : ndarray
        Elapsed time corresponding to the center of each window.
    moving : ndarray
        Moving average.
    """

    if window < 1:
        raise ValueError("window must be >= 1.")

    data = _get_quantity(profile, quantity)

    if window > len(data):
        raise ValueError("window is larger than the trajectory.")

    if window % 2 == 0:
        raise ValueError("window must be an odd integer.")

    kernel = np.ones(window) / window

    moving = np.convolve(
        data,
        kernel,
        mode="valid",
    )

    start = window // 2
    stop = start + len(moving)

    time = profile.elapsed_time[start:stop]

    return time, moving
