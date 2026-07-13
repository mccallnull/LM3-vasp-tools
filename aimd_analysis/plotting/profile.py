def plot_profile(
    profile,
    quantity,
    bins=30,
    figsize=(8, 5),
):

    x = profile.elapsed_time
    y = getattr(profile, quantity)

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(x, y)

    ax.set_xlabel("Elapsed Time (fs)")
    ax.set_ylabel(LABELS[quantity])

    axins = inset_axes(...)

    axins.hist(y, bins=bins)

    mean = np.mean(y)
    std = np.std(y)

    axins.text(...)

    plt.tight_layout()

    return fig, ax