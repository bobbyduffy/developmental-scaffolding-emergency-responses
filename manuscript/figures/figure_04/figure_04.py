from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTDIR = Path(__file__).resolve().parent


LABELS = [
    "L1",
    "L2",
    "L3",
    "L4",
    "L1",
    "L2",
    "L3",
    "L4",
]

# Extra gap between Claude and GPT.
Y = np.array([7.0, 6.0, 5.0, 4.0, 2.5, 1.5, 0.5, -0.5])

PRESENCE = np.array([
    53.33,
    1.25,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
    0.00,
])

WITHIN10 = np.array([
    15.56,
    62.92,
    27.50,
    5.00,
    59.17,
    36.25,
    0.00,
    0.00,
])

LATENCY = np.array([
    79.96,
    46.97,
    5.85,
    1.39,
    29.79,
    6.89,
    0.00,
    0.00,
])


def draw_panel(ax, values, title, xmax, unit):
    bars = ax.barh(
        Y,
        values,
        height=0.58,
    )

    ax.set_xlim(0, xmax)
    ax.set_yticks(Y)
    ax.set_yticklabels([])

    ax.set_title(
        title,
        fontsize=11,
        fontweight="bold",
        pad=12,
    )

    ax.grid(
        axis="x",
        linewidth=0.6,
        alpha=0.30,
    )
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.tick_params(
        axis="y",
        length=0,
    )

    if unit == "pp":
        ax.set_xlabel(
            "Relationship spread (percentage points)",
            fontsize=8.5,
        )
    else:
        ax.set_xlabel(
            "Relationship spread (words)",
            fontsize=8.5,
        )

    for bar, value in zip(bars, values):
        # Keep zeroes visible as explicit numeric observations.
        if value == 0:
            x = 0.8
            ha = "left"
        else:
            x = min(value + xmax * 0.025, xmax * 0.97)
            ha = "left"

        ax.text(
            x,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            va="center",
            ha=ha,
            fontsize=9,
            fontweight="bold",
        )


def main():
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(12.0, 6.7),
        sharey=True,
    )

    draw_panel(
        axes[0],
        PRESENCE,
        "EMS presence\nspread",
        65,
        "pp",
    )

    draw_panel(
        axes[1],
        WITHIN10,
        "EMS ≤10 words\nspread",
        65,
        "pp",
    )

    draw_panel(
        axes[2],
        LATENCY,
        "EMS latency\nspread",
        85,
        "words",
    )

    # Categorical level labels.
    axes[0].set_yticks(Y)
    axes[0].set_yticklabels(
        LABELS,
        fontsize=10,
    )
    axes[0].tick_params(
        axis="y",
        pad=8,
    )

    # Group labels.
    axes[0].text(
        -13.5,
        5.5,
        "Claude",
        ha="right",
        va="center",
        fontsize=10.5,
        fontweight="bold",
        clip_on=False,
    )

    axes[0].text(
        -13.5,
        1.0,
        "GPT",
        ha="right",
        va="center",
        fontsize=10.5,
        fontweight="bold",
        clip_on=False,
    )

    fig.suptitle(
        "Study 3 relationship-conditioned spread across mechanical emergency endpoints",
        fontsize=13,
        fontweight="bold",
        y=0.97,
    )

    fig.text(
        0.5,
        0.915,
        "Bars show max − min adjusted relationship estimates within each model × evidence level",
        ha="center",
        fontsize=9,
        style="italic",
    )

    fig.text(
        0.5,
        0.055,
        "Presence and ≤10-word panels share a percentage-point scale; latency uses a separate word scale.",
        ha="center",
        fontsize=8.5,
    )

    fig.text(
        0.5,
        0.022,
        "EMS ≤10-word and latency spreads are conditional on EMS presence.",
        ha="center",
        fontsize=8.5,
        fontweight="bold",
    )

    plt.subplots_adjust(
        left=0.19,
        right=0.97,
        top=0.82,
        bottom=0.15,
        wspace=0.32,
    )

    for suffix in ("svg", "pdf"):
        fig.savefig(
            OUTDIR / f"figure_04.{suffix}",
            bbox_inches="tight",
        )

    fig.savefig(
        OUTDIR / "figure_04.png",
        dpi=300,
        bbox_inches="tight",
    )

    print("Wrote:")
    for name in ("figure_04.svg", "figure_04.pdf", "figure_04.png"):
        print(f"  {OUTDIR / name}")


if __name__ == "__main__":
    main()
