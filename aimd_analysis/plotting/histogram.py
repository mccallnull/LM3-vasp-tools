import matplotlib.pyplot as plt

from .style import (
    LABELS,
    DEFAULT_FIGSIZE,
    DEFAULT_ALPHA,
)


# Plot histogram of one quantity.
def plot_histogram(
    profile,
    quantity,

    # Figure
    ax=None,
    figsize=DEFAULT_FIGSIZE,

    # Histogram
    bins=30,
    density=False,

    # Style
    color=None,
    alpha=DEFAULT_ALPHA,
    label=None,

    # Axis
    grid=True,
    xlim=None,
    ylim=None,
):

    y = getattr(profile, quantity)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
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

    if grid:
        ax.grid(True)

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_xlabel(LABELS[quantity])

    if density:
        ax.set_ylabel("Density")
    else:
        ax.set_ylabel("Count")

    plt.tight_layout()

    return fig, ax
