from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from ..analysis.convergence import (
    moving_average,
    running_average,
)
from ..model.md_profile import MDProfile
from . import style


def add_running_average(
    ax: Axes,
    profile: MDProfile,
    quantity: str,
    moving_window: Optional[int] = None,
    label: Optional[str] = None,
    color: Optional[str] = None,
    linewidth: float = 2.0,
    show_mean: bool = True,
) -> None:
    """
    Plot running average (and optional moving average)
    for a selected MD quantity.

    Parameters
    ----------
    ax
        Target matplotlib axes.
    profile
        MD profile object.
    quantity
        Quantity to plot.
    moving_window
        Window size for moving average.
    label
        Legend label.
    color
        Line color.
    linewidth
        Base line width.
    """

    time, running = running_average(
        profile,
        quantity,
    )

    ax.plot(
        time,
        running,
        label=label,
        color=color,
        linewidth=linewidth,
        linestyle=style.DEFAULT_LINESTYLE,
        alpha=style.DEFAULT_ALPHA,
    )

    if moving_window is not None:

        time_move, moving = moving_average(
            profile,
            quantity,
            moving_window,
        )

        ax.plot(
            time_move,
            moving,
            label=None,
            color=color,
            linewidth=style.MOVING_LINEWIDTH_SCALE * linewidth,
            linestyle=style.MOVING_LINESTYLE,
            alpha=style.MOVING_ALPHA,
        )

    if show_mean:
        ax.axhline(
            profile.stats[quantity].mean,
            color=style.MEAN_LINECOLOR,
            linestyle=style.MEAN_LINESTYLE,
            linewidth=style.MEAN_LINEWIDTH,
            alpha=style.MEAN_LINEALPHA,
        )
