from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


OUTDIR = Path(__file__).resolve().parent


def add_panel(ax, x, y, w, h, study, role, design, question, result, footer):
    # Main panel
    panel = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        linewidth=1.25,
        edgecolor="0.25",
        facecolor="0.97",
    )
    ax.add_patch(panel)

    # Study label
    ax.text(
        x + 0.04 * w, y + 0.91 * h,
        study,
        ha="left", va="top",
        fontsize=11, fontweight="bold",
    )

    # Conceptual role
    ax.text(
        x + 0.04 * w, y + 0.82 * h,
        role.upper(),
        ha="left", va="top",
        fontsize=9, fontweight="bold",
        color="0.35",
    )

    # Design shorthand
    ax.text(
        x + 0.04 * w, y + 0.68 * h,
        design,
        ha="left", va="top",
        fontsize=8.5,
        linespacing=1.25,
    )

    # Divider
    ax.plot(
        [x + 0.04 * w, x + 0.96 * w],
        [y + 0.57 * h, y + 0.57 * h],
        linewidth=0.8,
        color="0.75",
    )

    # Question
    ax.text(
        x + 0.04 * w, y + 0.51 * h,
        "QUESTION",
        ha="left", va="top",
        fontsize=7.5, fontweight="bold",
        color="0.4",
    )
    ax.text(
        x + 0.04 * w, y + 0.44 * h,
        question,
        ha="left", va="top",
        fontsize=8.7,
        linespacing=1.25,
    )

    # Result
    ax.text(
        x + 0.04 * w, y + 0.28 * h,
        "RESULT",
        ha="left", va="top",
        fontsize=7.5, fontweight="bold",
        color="0.4",
    )
    ax.text(
        x + 0.04 * w, y + 0.21 * h,
        result,
        ha="left", va="top",
        fontsize=8.7,
        fontweight="bold",
        linespacing=1.25,
    )

    # Footer
    ax.text(
        x + 0.04 * w, y + 0.035 * h,
        footer,
        ha="left", va="bottom",
        fontsize=7.3,
        color="0.35",
    )


def main():
    fig, ax = plt.subplots(figsize=(12.5, 4.9))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Geometry
    y = 0.10
    h = 0.80
    w = 0.275

    x1 = 0.035
    x2 = 0.3625
    x3 = 0.690

    add_panel(
        ax, x1, y, w, h,
        study="STUDY 1",
        role="Discovery",
        design=(
            "4 relationship cues × emergency absent/present\n"
            "mommy · mom · girlfriend · wife"
        ),
        question=(
            "Does relationship wording alter\n"
            "emergency guidance?"
        ),
        result=(
            "EMS inclusion reaches ceiling under\n"
            "unresponsiveness; foregrounding\n"
            "differences are discovered beneath it."
        ),
        footer="2 models · 3 systems · 60 reps/cell · N = 2,880",
    )

    add_panel(
        ax, x2, y, w, h,
        study="STUDY 2",
        role="Replication & decomposition",
        design=(
            "8 matched referents × emergency absent/present\n"
            "4 female/male role pairs"
        ),
        question=(
            "Does EMS latency replicate, and is it\n"
            "a uniform sex-coded effect?"
        ),
        result=(
            "Latency replicates strongly;\n"
            "matched contrasts differ by\n"
            "relational role."
        ),
        footer="2 models · 3 systems · 60 reps/cell · N = 5,760",
    )

    add_panel(
        ax, x3, y, w, h,
        study="STUDY 3",
        role="Boundary condition",
        design=(
            "8 matched referents × 4 evidence levels\n"
            "× 2 prompt variants"
        ),
        question=(
            "Does stronger emergency evidence\n"
            "constrain the relationship effect?"
        ),
        result=(
            "Relationship-conditioned differences\n"
            "contract as evidence becomes decisive;\n"
            "model trajectories differ."
        ),
        footer="2 models · 3 systems · 40 reps/cell · N = 15,360",
    )

    # Progression arrows
    for xa, xb in [(x1 + w, x2), (x2 + w, x3)]:
        arrow = FancyArrowPatch(
            (xa + 0.008, 0.50),
            (xb - 0.008, 0.50),
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.4,
            color="0.35",
        )
        ax.add_patch(arrow)

    fig.suptitle(
        "Progressive design of the three-study research program",
        fontsize=13,
        fontweight="bold",
        y=0.98,
    )

    fig.text(
        0.5, 0.025,
        "Discovery → prospective replication and decomposition → manipulated boundary-condition test",
        ha="center", va="bottom",
        fontsize=8.5,
        color="0.35",
    )

    plt.subplots_adjust(left=0.01, right=0.99, top=0.91, bottom=0.08)

    fig.savefig(
        OUTDIR / "figure_01.svg",
        bbox_inches="tight",
    )
    fig.savefig(
        OUTDIR / "figure_01.pdf",
        bbox_inches="tight",
    )
    fig.savefig(
        OUTDIR / "figure_01.png",
        dpi=300,
        bbox_inches="tight",
    )

    print("Wrote:")
    for name in ("figure_01.svg", "figure_01.pdf", "figure_01.png"):
        print(f"  {OUTDIR / name}")


if __name__ == "__main__":
    main()
