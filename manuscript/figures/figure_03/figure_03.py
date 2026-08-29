from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTDIR = Path(__file__).resolve().parent


RELATIONSHIPS = [
    "mommy",
    "daddy",
    "mom",
    "dad",
    "girlfriend",
    "boyfriend",
    "wife",
    "husband",
]

CLAUDE = {
    "mommy":      [33.91, 12.47, 4.85, 4.28],
    "daddy":      [42.47,  8.77, 4.41, 4.01],
    "mom":        [61.84, 19.55, 2.85, 3.32],
    "dad":        [65.27, 14.83, 5.13, 4.40],
    "girlfriend": [113.86, 50.60, 7.10, 3.81],
    "boyfriend":  [110.53, 55.73, 8.70, 4.30],
    "wife":       [99.58, 41.50, 5.39, 3.01],
    "husband":    [87.31, 29.04, 4.34, 3.33],
}

GPT = {
    "mommy":      [10.62, 1.05, 1.00, 1.00],
    "daddy":      [20.62, 1.46, 1.00, 1.00],
    "mom":        [13.40, 1.00, 1.00, 1.00],
    "dad":        [15.65, 1.06, 1.00, 1.00],
    "girlfriend": [40.41, 6.05, 1.00, 1.00],
    "boyfriend":  [35.95, 7.89, 1.00, 1.00],
    "wife":       [19.64, 1.10, 1.00, 1.00],
    "husband":    [20.91, 1.31, 1.00, 1.00],
}


def draw_panel(ax, data, title):
    x = np.arange(1, 5)

    markers = ["o", "s", "^", "D", "v", "P", "X", "*"]
    linestyles = ["-", "-", "--", "--", "-.", "-.", ":", ":"]

    for i, relationship in enumerate(RELATIONSHIPS):
        ax.plot(
            x,
            data[relationship],
            marker=markers[i],
            linestyle=linestyles[i],
            linewidth=1.6,
            markersize=5.5,
            label=relationship,
        )

    ax.set_title(title, fontsize=11.5, fontweight="bold")
    ax.set_xlim(0.85, 4.15)
    ax.set_ylim(0, 120)

    ax.set_xticks(
        x,
        [
            "L1\nresponsive",
            "L2\nunresponsive",
            "L3\n+ abnormal\nbreathing",
            "L4\n+ barely\nbreathing",
        ],
    )

    ax.grid(axis="y", linewidth=0.6, alpha=0.35)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def main():
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(12.5, 6.5),
        sharey=True,
    )

    draw_panel(
        axes[0],
        CLAUDE,
        "A. Claude Sonnet 5",
    )

    draw_panel(
        axes[1],
        GPT,
        "B. GPT-5.6 Terra",
    )

    axes[0].set_ylabel(
        "Adjusted first EMS-directive word",
        fontsize=10.5,
        fontweight="bold",
    )


    axes[1].annotate(
        "L3/L4 raw saturation:\n1,920 / 1,920 at word 1",
        xy=(3.48, 1.0),
        xytext=(2.45, 23),
        arrowprops={
            "arrowstyle": "->",
            "linewidth": 0.9,
        },
        fontsize=8.5,
        ha="left",
    )

    handles, labels = axes[0].get_legend_handles_labels()

    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=4,
        frameon=False,
        fontsize=8.7,
        bbox_to_anchor=(0.5, 0.035),
    )

    fig.suptitle(
        "Study 3 relationship × emergency-evidence latency surfaces",
        fontsize=13.5,
        fontweight="bold",
        y=0.97,
    )

    fig.text(
        0.5,
        0.915,
        "Lower values indicate earlier EMS foregrounding",
        ha="center",
        fontsize=9.5,
        style="italic",
    )

    fig.text(
        0.5,
        0.008,
        r"Relationship × certainty interaction: Wald(21) = 1334.96, $p$ = 7.95 × 10$^{-270}$",
        ha="center",
        fontsize=8.8,
    )

    plt.subplots_adjust(
        left=0.085,
        right=0.98,
        top=0.84,
        bottom=0.24,
        wspace=0.12,
    )

    for suffix in ("svg", "pdf"):
        fig.savefig(
            OUTDIR / f"figure_03.{suffix}",
            bbox_inches="tight",
        )

    fig.savefig(
        OUTDIR / "figure_03.png",
        dpi=300,
        bbox_inches="tight",
    )

    print("Wrote:")
    for name in ("figure_03.svg", "figure_03.pdf", "figure_03.png"):
        print(f"  {OUTDIR / name}")


if __name__ == "__main__":
    main()
