"""02_tool_frequencies.py

Response distribution of all 19 digital tools (Supplement S2), the median
share of "unclear what this is" across the 18 comparison tools, and Figure 1.

Reads analytical_sample.csv (written by 01_prepare_sample.py).
Writes data/aggregated/s2_tool_frequencies.csv, results/figure1.pdf, results/figure1.png.

Run from the repository root:  python code/02_tool_frequencies.py
"""
import importlib.util
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prep", ROOT / "code" / "01_prepare_sample.py")
prep = importlib.util.module_from_spec(spec); spec.loader.exec_module(prep)
TOOL_LABELS, CDSS_ITEM = prep.TOOL_LABELS, prep.CDSS_ITEM

LEVELS = ["daily", "weekly", "monthly", "less_often", "would_like", "unclear"]
COLLAPSED = {"daily": "daily_weekly", "weekly": "daily_weekly",
             "monthly": "monthly_less", "less_often": "monthly_less",
             "would_like": "would_like", "unclear": "unclear"}
FOOTNOTE_TOOLS = {15, 16}   # marked with an asterisk in Figure 1 (see figure legend)


def main() -> None:
    d = pd.read_csv(ROOT / "analytical_sample.csv")

    rows = []
    for k in range(1, 20):
        v = d[f"tool_{k:02d}"].dropna()
        n = len(v)
        counts = v.value_counts()
        row = {"item": k, "tool": TOOL_LABELS[k], "n": n}
        for lv in LEVELS:
            row[lv] = int(counts.get(lv, 0))
        for lv in LEVELS:
            row[f"{lv}_pct"] = round(row[lv] / n * 100, 1)
        c4 = v.map(COLLAPSED).value_counts()
        for cc in ["daily_weekly", "monthly_less", "would_like", "unclear"]:
            row[f"{cc}_collapsed"] = int(c4.get(cc, 0))
        rows.append(row)
    S2 = pd.DataFrame(rows)
    S2.to_csv(ROOT / "data" / "aggregated" / "s2_tool_frequencies.csv", index=False)

    cdss = S2[S2["item"] == CDSS_ITEM].iloc[0]
    others = S2[S2["item"] != CDSS_ITEM]
    median_unclear = others["unclear_pct"].median()

    # checks against the manuscript
    assert cdss["n"] == 361
    assert (cdss["daily_weekly_collapsed"], cdss["monthly_less_collapsed"],
            cdss["would_like_collapsed"], cdss["unclear_collapsed"]) == (43, 89, 80, 149)
    assert round(cdss["unclear_pct"]) == 41 and round(cdss["would_like_pct"]) == 22
    assert round(median_unclear) == 8
    # CDSS has the highest share of "unclear what this is" among the 19 tools
    assert S2.loc[S2["unclear_pct"].idxmax(), "item"] == CDSS_ITEM
    exceed = S2[S2["unclear"] > S2["would_like"]]
    print("tools with 'unclear' > 'would like': " + "; ".join(
        f"{r['tool']} ({r['unclear_pct']:.1f}% vs {r['would_like_pct']:.1f}%)" for _, r in exceed.iterrows()))

    print(f"CDSS (n = {cdss['n']}): daily/weekly {cdss['daily_weekly_collapsed']}, monthly/less {cdss['monthly_less_collapsed']}, "
          f"would like {cdss['would_like_collapsed']} ({cdss['would_like_pct']:.0f}%), unclear {cdss['unclear_collapsed']} ({cdss['unclear_pct']:.0f}%)")
    print(f"median 'unclear' across the 18 other tools: {median_unclear:.1f}%")
    print("S2 written: data/aggregated/s2_tool_frequencies.csv")

    figure1(S2, median_unclear)


def figure1(S2: pd.DataFrame, median_unclear: float) -> None:
    """Dumbbell chart: 'unclear what this is' (filled) and 'would like to, but not
    available' (open) for all 19 tools, sorted by the former; dashed line at the
    median of the 18 comparison tools; the CDSS item highlighted."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5})
    s = S2.sort_values("unclear_pct", ascending=True).reset_index(drop=True)
    y = np.arange(len(s))
    grey, accent = "#8a8a8a", "#1f5fbf"

    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.axvline(median_unclear, color="#bbbbbb", linestyle=(0, (3, 3)), linewidth=0.9, zorder=1)
    for i, r in s.iterrows():
        is_cdss = r["item"] == CDSS_ITEM
        col = accent if is_cdss else grey
        lo, hi = sorted([r["unclear_pct"], r["would_like_pct"]])
        ax.plot([lo, hi], [i, i], color=col, linewidth=1.0, zorder=2)
        ax.plot(r["unclear_pct"], i, "o", color=col, markersize=5.2, zorder=3)
        ax.plot(r["would_like_pct"], i, "o", markerfacecolor="white", markeredgecolor=col,
                markeredgewidth=1.0, markersize=5.2, zorder=3)
        if is_cdss:
            ax.annotate(f"{r['unclear_pct']:.0f}%", (r["unclear_pct"], i), xytext=(5, 0),
                        textcoords="offset points", va="center", fontweight="bold", color=accent)
            ax.annotate(f"{r['would_like_pct']:.0f}%", (r["would_like_pct"], i), xytext=(-5, 0),
                        textcoords="offset points", va="center", ha="right", fontweight="bold", color=accent)

    labels = [f"{r['tool']}*" if r["item"] in FOOTNOTE_TOOLS else r["tool"] for _, r in s.iterrows()]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    for lab, (_, r) in zip(ax.get_yticklabels(), s.iterrows()):
        if r["item"] == CDSS_ITEM:
            lab.set_fontweight("bold")
    ax.set_xlim(0, 50)
    ax.set_xticks([0, 10, 20, 30, 40, 50])
    ax.set_xticklabels([f"{t}%" for t in [0, 10, 20, 30, 40, 50]])
    ax.set_xlabel("Share of respondents")
    ax.set_ylim(-0.7, len(s) - 0.3)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=2, color="#999999")
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#999999")
    ax.grid(axis="x", color="#eeeeee", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)

    h1 = plt.Line2D([], [], color=grey, marker="o", linestyle="", markersize=5.2, label="“unclear what this is”")
    h2 = plt.Line2D([], [], color=grey, marker="o", linestyle="", markersize=5.2, markerfacecolor="white",
                    label="“would like to, but not available”")
    ax.legend(handles=[h1, h2], loc="center right", frameon=False, handletextpad=0.4, borderaxespad=0.2)

    fig.tight_layout(pad=0.4)
    fig.savefig(ROOT / "results" / "figure1.pdf")
    fig.savefig(ROOT / "results" / "figure1.png", dpi=300)
    print("Figure 1 written: results/figure1.pdf, results/figure1.png")


if __name__ == "__main__":
    main()
