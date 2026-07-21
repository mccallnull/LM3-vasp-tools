from aimd_analysis.analysis.convergence import (
    running_average,
    moving_average,
)
from . import style


def plot_running_average(
    ax,
    profile,
    quantity,
    *,
    moving_window=None,
    label=None,
    color=None,
    linewidth=2,
):
    """
    Plot running average.

    Parameters
    ----------
    ax
        Matplotlib axes.

    profile
        MD profile.

    quantity
        Quantity name.

    label
        Legend label.

    color
        Line color.

    linewidth
        Line width.
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
            linewidth=0.8 * linewidth,
            linestyle="--",
            alpha=0.9,
        )

    ax.axhline(
        running[-1],
        color=style.MEAN_LINECOLOR,
        linestyle=style.MEAN_LINESTYLE,
        linewidth=style.MEAN_LINEWIDTH,
        alpha=style.MEAN_LINEALPHA,
    )

    ax.set_xlabel("Elapsed Time (fs)")
    ax.set_ylabel(f"Running Average\n{style.LABELS[quantity]}")

    return ax
