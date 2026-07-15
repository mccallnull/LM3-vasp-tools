import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from .style import (
    LABELS,
    DEFAULT_FIGSIZE,
    DEFAULT_LINEWIDTH,
    DEFAULT_LINESTYLE,
    DEFAULT_ALPHA,
)

from .histogram import plot_histogram


# 한 개의 quantity를 시간에 따라 그림.
def plot_profile(
    profile,
    quantity,

    # Figure
    ax=None,
    figsize=DEFAULT_FIGSIZE,

    # Line style
    color=None,
    linewidth=DEFAULT_LINEWIDTH,
    linestyle=DEFAULT_LINESTYLE,
    alpha=DEFAULT_ALPHA,
    label=None,

    # Axis
    grid=True,
    xlim=None,
    ylim=None,

    # Include histogram?
    inset=False,
):

    x = profile.elapsed_time
    y = getattr(profile, quantity)

    if ax is None:
        fig, ax = plt.subplots(
            figsize=figsize,
            constrained_layout=True
        )
    else:
        fig = ax.figure

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.plot(
        x,
        y,
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        alpha=alpha,
        label=label,
    )

    if grid:
        ax.grid(True)

    ax.set_xlabel("Elapsed Time (fs)")
    ax.set_ylabel(LABELS[quantity])

    # plotting histogram --> 나중에 True/False로 켜고 끄기 가능하도록 구현.
    if inset:
        axins = inset_axes(
            ax,
            width="35%",
            height="35%",
            loc="upper left"
        )

        plot_histogram(
            profile,
            quantity,
            ax=axins,
            grid=False,
            inset=inset,
        )

    #mean = np.mean(y)
    #std = np.std(y)

    #axins.text(...)

    return fig, ax
