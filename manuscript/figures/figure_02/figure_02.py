from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTDIR = Path(__file__).resolve().parent


def main():
    labels = [
        "daddy − mommy",
        "dad − mom",
        "boyfriend − girlfriend",
        "husband − wife",
    ]

    estimates = np.array([
        4.2528,
        1.9111,
        -0.6778,
        -3.2500,
    ])

    ci_low = np.array([
        3.0678,
        0.2725,
        -3.6178,
        -5.2917,
    ])

    ci_high = np.array([
        5.4377,
        3.5498,
        2.2622,
        -1.2083,
    ])

    lower_err = estimates - ci_low
    upper_err = ci_high - estimates

    y = np.arange(len(labels))[::-1]

    fig, ax = plt.subplots(figsize=(10.5, 6.0))

    # Reference line
    ax.axvline(0, linewidth=1.0, color="0.25")

    # Confidence intervals + point estimates
    ax.errorbar(
        estimates,
        y,
        xerr=np.vstack([lower_err, upper_err]),
        fmt="o",
        markersize=6,
        capsize=4,
        linewidth=1.25,
        color="black",
    )

    # Row labels
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)

    # Symmetric axis
    ax.set_xlim(-6.3, 6.3)
    ax.set_xticks(np.arange(-6, 7, 2))

    ax.set_xlabel(
        "Male-coded − female-coded difference in first EMS-directive word",
        fontsize=10,
        fontweight="bold",
        labelpad=12,
    )

    # Light horizontal guides
    ax.grid(axis="y", linewidth=0.6, color="0.88")
    ax.grid(axis="x", linewidth=0.5, color="0.90", linestyle=":")

    # Clean frame
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    # Right-side estimate labels
    text_x = 6.55
    for yi, est, lo, hi in zip(y, estimates, ci_low, ci_high):
        ax.text(
            text_x,
            yi,
            f"{est:+.4f} [{lo:.4f}, {hi:.4f}]",
            va="center",
            ha="left",
            fontsize=8.7,
            clip_on=False,
        )

    ax.text(
        text_x,
        y[0] + 0.55,
        "Estimate [95% CI]",
        va="bottom",
        ha="left",
        fontsize=9,
        fontweight="bold",
        clip_on=False,
    )

    fig.suptitle(
        "Study 2 matched-role EMS-latency contrasts",
        fontsize=13,
        fontweight="bold",
        y=0.97,
    )

    fig.text(
        0.125,
        0.895,
        "Outcome: first EMS-directive word (lower = earlier EMS foregrounding)",
        fontsize=9.5,
        style="italic",
    )

    fig.text(
        0.125,
        0.085,
        "Adjusted for model and system-prompt condition",
        fontsize=8.8,
    )

    fig.text(
        0.125,
        0.050,
        r"Role × gendered-referent interaction: Wald(3) = 42.48, $p$ = 3.17 × 10$^{-9}$",
        fontsize=8.8,
    )

    plt.subplots_adjust(
        left=0.25,
        right=0.76,
        top=0.82,
        bottom=0.20,
    )

    for suffix in ("svg", "pdf"):
        fig.savefig(
            OUTDIR / f"figure_02.{suffix}",
            bbox_inches="tight",
        )

    fig.savefig(
        OUTDIR / "figure_02.png",
        dpi=300,
        bbox_inches="tight",
    )

    print("Wrote:")
    for name in ("figure_02.svg", "figure_02.pdf", "figure_02.png"):
        print(f"  {OUTDIR / name}")


if __name__ == "__main__":
    main()
