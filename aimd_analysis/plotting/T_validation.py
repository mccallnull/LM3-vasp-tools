import matplotlib.pyplot as plt
import numpy as np

from ..model.md_profile import MDProfile


def plot_temperature_validation(
    profiles,
    target_temperatures,
    outfile="temperature_validation.png",
):
    """
    Plot average temperature against target temperature.

    Parameters
    ----------
    profiles : list[MDProfile]
    target_temperatures : list[float]
    """

    means = []
    stds = []

    for profile in profiles:

        if not profile.stats:
            raise RuntimeError(
                "Statistics have not been computed."
            )

        means.append(profile.stats["T_md"].mean)
        stds.append(profile.stats["T_md"].std)

    means = np.asarray(means)
    stds = np.asarray(stds)
    target = np.asarray(target_temperatures)

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.errorbar(
        target,
        means,
        yerr=stds,
        fmt="o",
        color="tab:blue",
        markersize=6,
        capsize=4,
        label="QTB",
    )

    xmax = target.max() * 1.05

    ax.plot(
        [0, xmax],
        [0, xmax],
        "--",
        color="gray",
        linewidth=1.5,
        label="Ideal",
    )

    ax.set_xlim(0, xmax)
    ax.set_ylim(0, xmax)

    ax.set_xlabel("Target temperature (K)")
    ax.set_ylabel("Average temperature (K)")

    ax.legend()

    fig.tight_layout()
    fig.savefig(outfile, dpi=300)

    return fig
