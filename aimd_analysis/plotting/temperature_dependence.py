import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from typing import Tuple, List, Sequence, Optional

from ..model.md_profile import MDProfile
from . import style


def plot_temperature_dependence(
    profiles: List[MDProfile],
    target_temperatures: List[float],
    quantity: str,
    ax: Optional[Axes] = None,
    color: str = "tab:blue",
    label: str = "MD",
) -> Tuple[Figure, Axes]:
    """
    Plot average temperature against target temperature.

    Parameters
    ----------
    profiles : list[MDProfile]
    target_temperatures : list[float]
    quantity : str
    """

    means: List[float] = []
    stds: List[float] = []

    for profile in profiles:

        if quantity not in profile.stats:
            raise RuntimeError(
                "Statistics have not been computed."
            )

        means.append(profile.stats[quantity].mean)
        stds.append(profile.stats[quantity].std)

    means = np.asarray(means)
    stds = np.asarray(stds)
    target = np.asarray(target_temperatures)

    if ax is None:
        fig, ax = plt.subplots(
            figsize=(6, 6),
            constrained_layout=True,
        )
    else:
        fig = ax.figure

    ax.errorbar(
        target,
        means,
        yerr=stds,
        fmt="o",
        color=color,
        markersize=6,
        capsize=4,
        label=label,
    )

    #xmax = target.max() * 1.05

    #ax.set_xlim(0, xmax)
    #ax.set_ylim(0, xmax)

    ax.set_xlabel("Target temperature (K)")
    ax.set_ylabel(f"Average of {style.LABELS[quantity]}")

    return fig, ax

def add_temperature_reference(
    ax: Axes,
    x: Sequence[float],
    y: Sequence[float],
    linestyle: str = "--",
    color: str = "gray",
    linewidth: float = 1.5,
    label: Optional[str] = None,
) -> None:

    ax.plot(
        x,
        y,
        linestyle=linestyle,
        color=color,
        linewidth=linewidth,
        label=label,
    )

    ax.set_xlim(0, x.max())
    ax.set_ylim(0, x.max())
