"""
geometry.py
Geometry analysis for VASP AIMD trajectories.
Current features
----------------
- Compute lattice parameters from lattice vectors
    * a
    * b
    * c
    * alpha
    * beta
    * gamma
"""

import numpy as np
from typing import Tuple

from ..model.md_profile import MDProfile

# ==========================================================
# Lattice parameters
# ==========================================================

def compute_lattice_parameters(profile: MDProfile) -> None:
    """
    Compute lattice parameters from lattice vectors.
    Results are stored directly into the MDProfile object.
    """

    if profile.lat_vecs is None:
        return

    if len(profile.lat_vecs) == 0:
        return

    a, b, c = _compute_lengths(profile.lat_vecs)
    alpha, beta, gamma = _compute_angles(profile.lat_vecs)

    profile.lat_a = a
    profile.lat_b = b
    profile.lat_c = c

    profile.lat_alp = alpha
    profile.lat_bet = beta
    profile.lat_gam = gamma


def _compute_lengths(lat_vecs: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    a = np.linalg.norm(lat_vecs[:, 0, :], axis=1)
    b = np.linalg.norm(lat_vecs[:, 1, :], axis=1)
    c = np.linalg.norm(lat_vecs[:, 2, :], axis=1)

    return a, b, c


def _compute_angles(lat_vecs: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    a_vec = lat_vecs[:, 0, :]
    b_vec = lat_vecs[:, 1, :]
    c_vec = lat_vecs[:, 2, :]

    a, b, c = _compute_lengths(lat_vecs)

    alpha = _angle(b_vec, c_vec, b, c)
    beta  = _angle(a_vec, c_vec, a, c)
    gamma = _angle(a_vec, b_vec, a, b)

    return alpha, beta, gamma


def _angle(
    v1: np.ndarray,
    v2: np.ndarray,
    norm1: np.ndarray,
    norm2: np.ndarray,
) -> np.ndarray:

    cos_theta = np.sum(v1 * v2, axis=1) / (norm1 * norm2)

    # numerical safety
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    return np.degrees(np.arccos(cos_theta))
