import matplotlib.pyplot as plt

import numpy as np

from mpl_toolkits.axes_grid1.inset_locator import inset_axes


LABELS = {
    "Epot": "Potential Energy (eV)",
    "Ekin": "Kinetic Energy (eV)",
    "Etot": "Total Energy (eV)",
    "T_md": "Temperature (K)",
}

# 한 개의 quantity를 시간에 따라 그림.
def plot_profile(
    profile,
    quantity,

    # Figure
    ax=None,
    figsize=(6, 4),

    # Line style
    color=None,
    linewidth=1.5,
    linestyle="-",
    alpha=1.0,
    label=None,

    # Axis
    grid=True,
    xlim=None,
    ylim=None,

    #bins=30,
):

    x = profile.elapsed_time
    y = getattr(profile, quantity)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    if grid:
        ax.grid(True)

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is None:
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

    ax.set_xlabel("Elapsed Time (fs)")
    ax.set_ylabel(LABELS[quantity])

    #axins = inset_axes(...)

    #axins.hist(y, bins=bins)

    #mean = np.mean(y)
    #std = np.std(y)

    #axins.text(...)

    plt.tight_layout()

    return fig, ax
