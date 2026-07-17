import matplotlib.pyplot as plt
from typing import Dict, Optional, Any

from ..model.md_profile import MDProfile
from . import style


# Plot histogram of one quantity.
def plot_histogram(
    profile: MDProfile,
    quantity: str,

    # Figure
    ax=None,
    figsize=style.DEFAULT_FIGSIZE,

    # Histogram
    bins: int = 30,
    density: bool = False,

    # Style
    color=None,
    alpha=style.DEFAULT_ALPHA,
    label=None,

    # Axis
    grid: bool = True,
    xlim=None,
    ylim=None,

    # Is inset?
    inset: bool  =False,

    # Include statistics?
    show_statistics: bool = False,

    # Details for style
    mean_kwargs: Optional[Dict[str, Any]] = None,
    textbox_kwargs: Optional[Dict[str, Any]] = None,
) -> tuple:

    if not profile.stats:
        raise RuntimeError(
            "Statistics have not been computed. "
            "Call compute_statistics(profile) first."
        )

    # Setup histogram
    y = getattr(profile, quantity)

    if ax is None:
        fig, ax = plt.subplots(
            figsize=figsize,
            constrained_layout=True
        )
    else:
        fig = ax.figure

    ax.hist(
        y,
        bins=bins,
        density=density,
        color=color,
        alpha=alpha,
        label=label,
    )

    # Setup mean vertical line
    stats = profile.stats[quantity]

    default_mean_kwargs = dict(
        color=style.MEAN_LINECOLOR,
        linestyle=style.MEAN_LINESTYLE,
        linewidth=style.MEAN_LINEWIDTH,
        alpha=style.MEAN_LINEALPHA,
    )

    if mean_kwargs is not None:
        default_mean_kwargs.update(mean_kwargs)

    ax.axvline(
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

    ax.set_xlabel(style.LABELS[quantity])

    if density:
        ax.set_ylabel("Density")
    else:
        ax.set_ylabel("Count")

    if inset:
        ax.set_xlabel("")
        ax.set_ylabel("")

        ax.tick_params(
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False,
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
