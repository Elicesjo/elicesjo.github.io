import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

projects = [
    {
        "slug": "sql-requetes",
        "title": "SQL\nRequêtes BDD",
        "icon": "🗄️",
        "color": "#2980B9",
        "accent": "#1A5276",
        "elements": "sql",
    },
    {
        "slug": "sante-publique",
        "title": "Santé Publique\nPython",
        "icon": "🌍",
        "color": "#27AE60",
        "accent": "#1E8449",
        "elements": "map",
    },
    {
        "slug": "immo-sql",
        "title": "BDD Immobilier\nSQL",
        "icon": "🏠",
        "color": "#8E44AD",
        "accent": "#6C3483",
        "elements": "erd",
    },
    {
        "slug": "ecommerce-python",
        "title": "E-commerce\nPython",
        "icon": "🛒",
        "color": "#E67E22",
        "accent": "#CA6F1E",
        "elements": "bar",
    },
    {
        "slug": "powerbi-dashboard",
        "title": "Dashboard\nPower BI",
        "icon": "📊",
        "color": "#E74C3C",
        "accent": "#C0392B",
        "elements": "kpi",
    },
]

base = Path("/home/elicesjo/GitHub/elicesjo.github.io/projets")

for p in projects:
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor(p["color"])
    ax.set_facecolor(p["color"])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.add_patch(mpatches.FancyBboxPatch((0.3, 0.3), 9.4, 5.4, boxstyle="round,pad=0.1",
                                          facecolor=p["accent"], alpha=0.3, linewidth=0))

    if p["elements"] == "bar":
        heights = [2, 3.5, 2.8, 4.2, 1.8, 3.1]
        xs = np.linspace(1.5, 8.5, 6)
        for x, h in zip(xs, heights):
            ax.add_patch(mpatches.Rectangle((x - 0.35, 0.6), 0.7, h * 0.8,
                                             facecolor="white", alpha=0.5))
    elif p["elements"] == "kpi":
        for i, (val, lbl) in enumerate([("87%", "KPI 1"), ("2.4M", "KPI 2"), ("↑12%", "KPI 3")]):
            x = 1.5 + i * 3
            ax.add_patch(mpatches.FancyBboxPatch((x - 0.9, 1.2), 1.8, 2.5,
                                                  boxstyle="round,pad=0.1",
                                                  facecolor="white", alpha=0.25))
            ax.text(x, 2.8, val, ha="center", va="center", fontsize=14,
                    fontweight="bold", color="white")
            ax.text(x, 1.8, lbl, ha="center", va="center", fontsize=8, color="white", alpha=0.8)
    elif p["elements"] == "sql":
        for i in range(3):
            y = 4.2 - i * 1.4
            ax.add_patch(mpatches.FancyBboxPatch((1.0, y - 0.4), 3.5, 0.8,
                                                  boxstyle="round,pad=0.1",
                                                  facecolor="white", alpha=0.25))
            ax.add_patch(mpatches.FancyBboxPatch((5.5, y - 0.4), 3.5, 0.8,
                                                  boxstyle="round,pad=0.1",
                                                  facecolor="white", alpha=0.25))
            ax.annotate("", xy=(5.4, y), xytext=(4.6, y),
                        arrowprops=dict(arrowstyle="->", color="white", lw=1.5))
    elif p["elements"] == "map":
        theta = np.linspace(0, 2 * np.pi, 100)
        ax.fill(5 + 3.5 * np.cos(theta), 3 + 1.8 * np.sin(theta),
                color="white", alpha=0.15)
        np.random.seed(42)
        for _ in range(20):
            x = np.random.uniform(2, 8)
            y = np.random.uniform(1.5, 4.5)
            c = np.random.choice(["white", "#F0E68C", "#FF6B6B"], p=[0.5, 0.3, 0.2])
            ax.scatter(x, y, s=40, color=c, alpha=0.7, zorder=5)
    elif p["elements"] == "erd":
        for i, (x, y, label) in enumerate([(2.5, 4.2, "COMMUNE"), (7.5, 4.2, "BIEN"),
                                            (2.5, 1.8, "REGION"), (7.5, 1.8, "TRANSACTION")]):
            ax.add_patch(mpatches.FancyBboxPatch((x - 1.2, y - 0.45), 2.4, 0.9,
                                                  boxstyle="round,pad=0.05",
                                                  facecolor="white", alpha=0.3))
            ax.text(x, y, label, ha="center", va="center", fontsize=7,
                    fontweight="bold", color="white")
        for (x1, y1), (x2, y2) in [((2.5, 3.75), (2.5, 2.25)),
                                     ((3.7, 4.2), (6.3, 4.2)),
                                     ((7.5, 3.75), (7.5, 2.25))]:
            ax.plot([x1, x2], [y1, y2], color="white", lw=1.5, alpha=0.6)

    ax.text(5, 5.4, p["title"], ha="center", va="center", fontsize=14,
            fontweight="bold", color="white",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=p["accent"], alpha=0.5, linewidth=0))

    out = base / p["slug"] / "thumbnail.png"
    plt.tight_layout(pad=0)
    plt.savefig(out, dpi=120, bbox_inches="tight", facecolor=p["color"])
    plt.close()
    print(f"Created {out}")
