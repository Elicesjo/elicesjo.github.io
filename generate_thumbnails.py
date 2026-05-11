import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

BASE = Path("/home/elicesjo/GitHub/elicesjo.github.io/projets")

PROJECTS = [
    {
        "slug": "sql-requetes",
        "title": "Requêtes SQL",
        "subtitle": "Analyse des ventes — Marchand de vin",
        "color1": "#6B6BA8",
        "color2": "#4A4A7A",
    },
    {
        "slug": "sante-publique",
        "title": "Santé Publique",
        "subtitle": "Étude sous-nutrition mondiale — FAO",
        "color1": "#D47070",
        "color2": "#A85050",
    },
    {
        "slug": "immo-sql",
        "title": "Base de données\nImmobilière",
        "subtitle": "Modélisation SQL — Données DVF",
        "color1": "#6B94C0",
        "color2": "#4A72A0",
    },
    {
        "slug": "ecommerce-python",
        "title": "E-commerce",
        "subtitle": "Optimisation & audit données — Python",
        "color1": "#70A87A",
        "color2": "#4A7A54",
    },
    {
        "slug": "powerbi-dashboard",
        "title": "Dashboard Power BI",
        "subtitle": "Indicateurs santé entreprise — DAX",
        "color1": "#C09B50",
        "color2": "#9A7530",
    },
    {
        "slug": "socio-demo-dbt",
        "title": "Socio-démographie",
        "subtitle": "Profils apprenants OpenClassrooms — dbt",
        "color1": "#9B78C0",
        "color2": "#7050A0",
    },
    {
        "slug": "ecommerce-lapage",
        "title": "Analyse E-commerce\nLapage",
        "subtitle": "Segmentation clients & statistiques",
        "color1": "#5090B0",
        "color2": "#306A90",
    },
]


def make_thumbnail(slug, title, subtitle, color1, color2):
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor=color1)
    ax.set_facecolor(color1)
    ax.axis("off")

    # Gradient effect via rectangles
    n = 60
    for i in range(n):
        t = i / n
        r1, g1, b1 = [int(color1[j:j+2], 16) / 255 for j in (1, 3, 5)]
        r2, g2, b2 = [int(color2[j:j+2], 16) / 255 for j in (1, 3, 5)]
        r = r1 + (r2 - r1) * t
        g = g1 + (g2 - g1) * t
        b = b1 + (b2 - b1) * t
        ax.add_patch(plt.Rectangle((0, i / n), 1, 1 / n,
                                    transform=ax.transAxes,
                                    color=(r, g, b), linewidth=0))

    # Subtle decorative circle
    circle = plt.Circle((0.85, 0.5), 0.38, transform=ax.transAxes,
                         color="white", alpha=0.05, linewidth=0)
    ax.add_patch(circle)
    circle2 = plt.Circle((0.88, 0.15), 0.22, transform=ax.transAxes,
                          color="white", alpha=0.05, linewidth=0)
    ax.add_patch(circle2)

    # Title
    ax.text(0.08, 0.62, title,
            transform=ax.transAxes,
            fontsize=28, fontweight="bold", color="white",
            va="center", ha="left",
            fontfamily="DejaVu Sans",
            linespacing=1.3)

    # Subtitle
    ax.text(0.08, 0.25, subtitle,
            transform=ax.transAxes,
            fontsize=13, color="white", alpha=0.82,
            va="center", ha="left",
            fontfamily="DejaVu Sans")

    # Thin accent line
    ax.add_patch(plt.Rectangle((0.08, 0.42), 0.06, 0.004,
                                transform=ax.transAxes,
                                color="white", alpha=0.6, linewidth=0))

    out = BASE / slug / "thumbnail.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=color1, pad_inches=0)
    plt.close(fig)
    print(f"  → {slug}/thumbnail.png")


for p in PROJECTS:
    make_thumbnail(**p)

print("\nTous les thumbnails générés.")
