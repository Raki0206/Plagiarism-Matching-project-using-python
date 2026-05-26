import matplotlib
matplotlib.use("Agg")   # headless rendering
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os, glob, csv
from collections import defaultdict

# ── Colour palette (one per algorithm) ───────────────────────
COLORS = {
    "Naive":       "#E74C3C",
    "KMP":         "#2ECC71",
    "Rabin-Karp":  "#3498DB",
    "Boyer-Moore": "#F39C12",
}

# ── Embedded benchmark data (mirrors the compiled run) ───────
# Format: (pattern, algo, occurrences, comparisons, time_us)
BENCH_DATA = [
    # pattern: "the"
    ("the",                          "Naive",       12, 1394, 4.61),
    ("the",                          "KMP",         12, 1256, 4.97),
    ("the",                          "Rabin-Karp",  12, 1292, 6.63),
    ("the",                          "Boyer-Moore", 12,  489, 3.45),
    # pattern: "pattern"
    ("pattern",                      "Naive",        9, 1331, 3.78),
    ("pattern",                      "KMP",          9, 1256, 4.06),
    ("pattern",                      "Rabin-Karp",   9, 1318, 6.71),
    ("pattern",                      "Boyer-Moore",  9,  289, 2.23),
    # pattern: "plagiarism"
    ("plagiarism",                   "Naive",        8, 1346, 3.69),
    ("plagiarism",                   "KMP",          8, 1256, 3.88),
    ("plagiarism",                   "Rabin-Karp",   8, 1335, 7.03),
    ("plagiarism",                   "Boyer-Moore",  8,  242, 2.16),
    # pattern: "matching algorithms"
    ("matching algorithms",          "Naive",        4, 1412, 3.98),
    ("matching algorithms",          "KMP",          4, 1256, 4.24),
    ("matching algorithms",          "Rabin-Karp",   4, 1323, 6.91),
    ("matching algorithms",          "Boyer-Moore",  4,  205, 1.30),
    # pattern: "Knuth-Morris-Pratt algorithm"
    ("Knuth-Morris-Pratt algorithm", "Naive",        1, 1265, 2.89),
    ("Knuth-Morris-Pratt algorithm", "KMP",          1, 1256, 3.49),
    ("Knuth-Morris-Pratt algorithm", "Rabin-Karp",   1, 1270, 6.42),
    ("Knuth-Morris-Pratt algorithm", "Boyer-Moore",  1,  174, 0.98),
    # pattern: "pattern matching algorithms are"
    ("pattern matching algorithms are", "Naive",     1, 1439, 3.37),
    ("pattern matching algorithms are", "KMP",       1, 1256, 3.67),
    ("pattern matching algorithms are", "Rabin-Karp",1, 1275, 6.47),
    ("pattern matching algorithms are", "Boyer-Moore",1, 154, 1.00),
]

ALGOS    = ["Naive", "KMP", "Rabin-Karp", "Boyer-Moore"]
PATTERNS = list(dict.fromkeys(r[0] for r in BENCH_DATA))   # preserve order

def get_metric(metric_idx):
    """Return dict[pattern][algo] = value. metric_idx: 3=comparisons, 4=time."""
    d = defaultdict(dict)
    for row in BENCH_DATA:
        pat, algo, *vals = row
        d[pat][algo] = vals[metric_idx - 2]   # offset: row is (pat,algo,occ,cmp,t)
    return d


# ─────────────────────────────────────────────────────────────
# FIG 1 – Grouped bar chart: Execution Time per Pattern
# ─────────────────────────────────────────────────────────────
def fig_execution_time_grouped():
    time_data = get_metric(4)
    x = np.arange(len(PATTERNS))
    width = 0.18
    offsets = np.linspace(-1.5 * width, 1.5 * width, 4)

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    for i, algo in enumerate(ALGOS):
        vals = [time_data[p].get(algo, 0) for p in PATTERNS]
        bars = ax.bar(x + offsets[i], vals, width,
                      label=algo, color=COLORS[algo], alpha=0.9,
                      edgecolor="white", linewidth=0.4)
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:.1f}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom",
                        fontsize=7, color="white")

    labels = [p if len(p) <= 14 else p[:12] + "…" for p in PATTERNS]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right", color="white", fontsize=9)
    ax.set_ylabel("Execution Time (µs)", color="white", fontsize=11)
    ax.set_title("Execution Time per Pattern  –  All Algorithms",
                 color="white", fontsize=13, pad=12, fontweight="bold")
    ax.legend(facecolor="#1E293B", edgecolor="gray", labelcolor="white",
              fontsize=9)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#334155")
    ax.yaxis.grid(True, color="#334155", linewidth=0.5)
    fig.tight_layout()
    fig.savefig("output/fig1_execution_time_grouped.png", dpi=150,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  Saved: fig1_execution_time_grouped.png")


# ─────────────────────────────────────────────────────────────
# FIG 2 – Grouped bar chart: Comparisons per Pattern
# ─────────────────────────────────────────────────────────────
def fig_comparisons_grouped():
    cmp_data = get_metric(3)
    x = np.arange(len(PATTERNS))
    width = 0.18
    offsets = np.linspace(-1.5 * width, 1.5 * width, 4)

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    for i, algo in enumerate(ALGOS):
        vals = [cmp_data[p].get(algo, 0) for p in PATTERNS]
        bars = ax.bar(x + offsets[i], vals, width,
                      label=algo, color=COLORS[algo], alpha=0.9,
                      edgecolor="white", linewidth=0.4)
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{int(h)}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom",
                        fontsize=7, color="white")

    labels = [p if len(p) <= 14 else p[:12] + "…" for p in PATTERNS]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right", color="white", fontsize=9)
    ax.set_ylabel("Number of Comparisons", color="white", fontsize=11)
    ax.set_title("Character Comparisons per Pattern  –  All Algorithms",
                 color="white", fontsize=13, pad=12, fontweight="bold")
    ax.legend(facecolor="#1E293B", edgecolor="gray", labelcolor="white",
              fontsize=9)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#334155")
    ax.yaxis.grid(True, color="#334155", linewidth=0.5)
    fig.tight_layout()
    fig.savefig("output/fig2_comparisons_grouped.png", dpi=150,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  Saved: fig2_comparisons_grouped.png")


# ─────────────────────────────────────────────────────────────
# FIG 3 – Line chart: Execution Time vs Pattern Length
# ─────────────────────────────────────────────────────────────
def fig_time_vs_pattern_length():
    lengths = [len(p) for p in PATTERNS]
    time_data = get_metric(4)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    for algo in ALGOS:
        vals = [time_data[p].get(algo, 0) for p in PATTERNS]
        ax.plot(lengths, vals, marker="o", label=algo,
                color=COLORS[algo], linewidth=2, markersize=7)
        for x, y in zip(lengths, vals):
            ax.annotate(f"{y:.1f}", (x, y),
                        textcoords="offset points", xytext=(4, 4),
                        fontsize=8, color=COLORS[algo])

    ax.set_xlabel("Pattern Length (characters)", color="white", fontsize=11)
    ax.set_ylabel("Execution Time (µs)",         color="white", fontsize=11)
    ax.set_title("Execution Time vs Pattern Length",
                 color="white", fontsize=13, pad=12, fontweight="bold")
    ax.legend(facecolor="#1E293B", edgecolor="gray", labelcolor="white")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#334155")
    ax.yaxis.grid(True, color="#334155", linewidth=0.5)
    fig.tight_layout()
    fig.savefig("output/fig3_time_vs_pattern_length.png", dpi=150,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  Saved: fig3_time_vs_pattern_length.png")


# ─────────────────────────────────────────────────────────────
# FIG 4 – Radar / Spider chart: Overall performance
# ─────────────────────────────────────────────────────────────
def fig_radar():
    # Metrics: [Avg Speed, Avg Comparisons(inv), Worst-Case, Impl Simplicity]
    # All normalised 0–1 (higher = better)
    scores = {
        "Naive":       [0.55, 0.20, 0.30, 1.00],
        "KMP":         [0.80, 0.85, 1.00, 0.70],
        "Rabin-Karp":  [0.60, 0.80, 0.60, 0.75],
        "Boyer-Moore": [1.00, 1.00, 0.60, 0.55],
    }
    categories = ["Avg Speed", "Few Comparisons",
                  "Worst-Case\nGuarantee", "Impl. Simplicity"]
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8),
                           subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    for algo, vals in scores.items():
        v = vals + vals[:1]
        ax.plot(angles, v, color=COLORS[algo], linewidth=2, label=algo)
        ax.fill(angles, v, color=COLORS[algo], alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color="white", fontsize=10)
    ax.set_yticklabels([])
    ax.spines["polar"].set_color("#334155")
    ax.grid(color="#334155", linewidth=0.8)
    ax.set_title("Algorithm Quality Radar\n(higher = better)",
                 color="white", fontsize=13, pad=20, fontweight="bold")
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15),
              facecolor="#1E293B", edgecolor="gray", labelcolor="white")
    fig.tight_layout()
    fig.savefig("output/fig4_radar.png", dpi=150,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  Saved: fig4_radar.png")


# ─────────────────────────────────────────────────────────────
# FIG 5 – Stacked bar: Average comparisons breakdown
# ─────────────────────────────────────────────────────────────
def fig_avg_comparisons_bar():
    cmp_data = get_metric(3)
    avgs = {algo: np.mean([cmp_data[p].get(algo, 0) for p in PATTERNS])
            for algo in ALGOS}

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    bars = ax.barh(list(avgs.keys()),
                   list(avgs.values()),
                   color=[COLORS[a] for a in avgs],
                   edgecolor="white", linewidth=0.5,
                   height=0.5)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 10, bar.get_y() + bar.get_height() / 2,
                f"{int(w)}", va="center", color="white", fontsize=10)

    ax.set_xlabel("Average Comparisons", color="white", fontsize=11)
    ax.set_title("Average Comparisons across All Patterns",
                 color="white", fontsize=13, pad=12, fontweight="bold")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#334155")
    ax.xaxis.grid(True, color="#334155", linewidth=0.5)
    fig.tight_layout()
    fig.savefig("output/fig5_avg_comparisons.png", dpi=150,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  Saved: fig5_avg_comparisons.png")


# ─────────────────────────────────────────────────────────────
# FIG 6 – Time complexity growth curves (theoretical)
# ─────────────────────────────────────────────────────────────
def fig_theoretical_complexity():
    n = np.linspace(100, 100_000, 500)
    m = 20   # fixed pattern length

    curves = {
        "Naive  O(n·m)":         n * m,
        "KMP    O(n+m)":         n + m,
        "Rabin-Karp O(n+m)avg":  n + m,
        "Boyer-Moore O(n/m)best":n / m,
    }
    style = ["-", "--", "-.", ":"]
    colors_theory = list(COLORS.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    for (label, y), ls, c in zip(curves.items(), style, colors_theory):
        ax.plot(n, y, linestyle=ls, color=c, linewidth=2, label=label)

    ax.set_xlabel("Text Length n (characters)", color="white", fontsize=11)
    ax.set_ylabel("Operations",                  color="white", fontsize=11)
    ax.set_title(f"Theoretical Time Complexity (m = {m})",
                 color="white", fontsize=13, pad=12, fontweight="bold")
    ax.legend(facecolor="#1E293B", edgecolor="gray", labelcolor="white",
              fontsize=9)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#334155")
    ax.yaxis.grid(True, color="#334155", linewidth=0.5)
    fig.tight_layout()
    fig.savefig("output/fig6_theoretical_complexity.png", dpi=150,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("  Saved: fig6_theoretical_complexity.png")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    print("\n  Generating visualisation charts...\n")
    fig_execution_time_grouped()
    fig_comparisons_grouped()
    fig_time_vs_pattern_length()
    fig_radar()
    fig_avg_comparisons_bar()
    fig_theoretical_complexity()
    print("\n  All 6 charts saved to output/\n")
