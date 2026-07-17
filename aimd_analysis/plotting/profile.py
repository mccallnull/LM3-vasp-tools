import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from typing import Dict, Optional, Any

from ..model.md_profile import MDProfile
from . import style
from .histogram import plot_histogram


# 한 개의 quantity를 시간에 따라 그림.
def plot_profile(
    profile: MDProfile,
    quantity: str,

    # Figure
    ax=None,
    figsize=style.DEFAULT_FIGSIZE,

    # Line style
    color=None,
    linewidth=style.DEFAULT_LINEWIDTH,
    linestyle=style.DEFAULT_LINESTYLE,
    alpha=style.DEFAULT_ALPHA,
    label=None,

    # Axis
    grid: bool = True,
    xlim=None,
    ylim=None,

    # Include histogram?
    inset: bool = False,

    # Include statistics?
    show_statistics: bool = False,

    # Time reference?
    time_reference: str = "elapsed",

    # Details for style
    mean_kwargs: Optional[Dict[str, Any]] = None,
    textbox_kwargs: Optional[Dict[str, Any]] = None,
) -> tuple:

    if not profile.stats:
        raise RuntimeError(
            "Statistics have not been computed. "
            "Call compute_statistics(profile) first."
        )

    # Setip profile plot
    if time_reference == "absolute":
        x = profile.time
    elif time_reference == "elapsed":
        x = profile.elapsed_time
    elif time_reference == "parent":
        if profile.parent is None:
            raise RuntimeError(
                "This profile has no parent."
            )
        x = profile.parent_time
    else:
        raise ValueError(
            f"Unknown time_reference: {time_reference!r}. "
            "Choose from 'absolute', 'elapsed', or 'parent'."
        )

    y = getattr(profile, quantity)

    if ax is None:
        fig, ax = plt.subplots(
            figsize=figsize,
            constrained_layout=True
        )
    else:
        fig = ax.figure



    ax.plot(
        x,
        y,
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        alpha=alpha,
        label=label,
    )

    # Setup mean horizontal line
    stats = profile.stats[quantity]

    default_mean_kwargs = dict(
        color=style.MEAN_LINECOLOR,
        linestyle=style.MEAN_LINESTYLE,
        linewidth=style.MEAN_LINEWIDTH,
        alpha=style.MEAN_LINEALPHA,
    )

    if mean_kwargs is not None:
        default_mean_kwargs.update(mean_kwargs)

    ax.axhline(
        stats.mean,
        **default_mean_kwargs,
    )

    # Setup axes and grids
    if grid:
        ax.grid(True)

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_xlabel("Time (fs)")
    ax.set_ylabel(style.LABELS[quantity])

    # Setup inset histogram
    if inset:
        axins = inset_axes(
            ax,
            width="35%",
            height="35%",
            loc="lower right"
        )

        plot_histogram(
            profile,
            quantity,
            ax=axins,
            grid=False,
            inset=inset,
        )

    # Setup statistics textbox
    if show_statistics:
        text = (
            f"{'Mean':<5}: {stats.mean:10.6f}\n"
            f"{'Std':<5}: {stats.std:10.6f}"
        )

        default_textbox_kwargs = dict(
            facecolor=style.TEXTBOX_FACECOLOR,
            edgecolor=style.TEXTBOX_EDGECOLOR,
            alpha=style.TEXTBOX_ALPHA,
            boxstyle=f"square,pad={style.TEXTBOX_PAD}",
        )

        if textbox_kwargs is not None:
            default_textbox_kwargs.update(textbox_kwargs)

        ax.text(
            style.TEXTBOX_X,
            style.TEXTBOX_Y,
            text,

            transform=ax.transAxes,

            ha="left",
            va="top",

            bbox = default_textbox_kwargs,

            fontsize=style.TEXTBOX_FONTSIZE,
        )

    return fig, ax
