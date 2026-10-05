import matplotlib.pyplot as plt


def plot_smile(strikes, ivs, spot, expiry, ticker="SPY", outfile="vol_smile.png"):
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)

    ax.plot(strikes, ivs * 100, color="#1f5e8c", linewidth=2,
            marker="o", markersize=4, markerfacecolor="white",
            markeredgewidth=1.2, zorder=3)

    ax.axvline(spot, color="#8a8f98", linewidth=1, linestyle="--", zorder=2)
    ax.annotate(f"spot {spot:,.2f}", xy=(spot, ax.get_ylim()[1]),
                xytext=(5, -12), textcoords="offset points",
                color="#55606e", fontsize=9, va="top")

    ax.set_title(f"{ticker} implied volatility by strike — {expiry} expiry",
                 fontsize=12, pad=12)
    ax.set_xlabel("Strike")
    ax.set_ylabel("Implied volatility (%)")

    ax.grid(True, color="#e3e7ec", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(outfile)
    return outfile