import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Ellipse
import matplotlib.colors as mcolors
import os
import warnings

warnings.filterwarnings("ignore")

np.random.seed(42)

BG = "#0D0D0D"
TEXT = "#E8E8F8"
MUTED = "#9090B0"
SPINE = "#1E1E2E"
PRIMARY = "#9B9BD4"
SECONDARY = "#E89090"
TERTIARY = "#8BAED4"
QUATERNARY = "#8BC4A8"
ORANGE = "#F4A261"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "text.color": TEXT,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.grid": True,
    "grid.color": SPINE,
    "grid.alpha": 0.5,
    "axes.grid.axis": "y",
    "font.family": "DejaVu Sans",
    "figure.dpi": 100,
})


def style_ax(ax, xlabel=None, ylabel=None, title=None):
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_color(SPINE)
        spine.set_alpha(0.4)
    ax.tick_params(colors=MUTED, labelsize=8)
    if xlabel:
        ax.set_xlabel(xlabel, color=MUTED, fontsize=8)
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED, fontsize=8)
    if title:
        ax.set_title(title, color=TEXT, fontsize=10, fontweight="bold", pad=8)


# ─────────────────────────────────────────────────────────────────────────────
# 1. RFM Customer Segmentation
# ─────────────────────────────────────────────────────────────────────────────
def make_rfm():
    fig = plt.figure(figsize=(12, 6.5), facecolor=BG)
    gs = gridspec.GridSpec(2, 2, figure=fig, width_ratios=[1, 1],
                           hspace=0.45, wspace=0.35)
    ax_scatter = fig.add_subplot(gs[:, 0])
    ax_bar = fig.add_subplot(gs[0, 1])
    ax_kpi = fig.add_subplot(gs[1, 1])

    segments = {
        "Champions": {"color": PRIMARY,    "center": (4.5, 4.5), "n": 30},
        "Loyal":     {"color": QUATERNARY, "center": (3.5, 4.0), "n": 35},
        "At Risk":   {"color": SECONDARY,  "center": (2.0, 2.5), "n": 35},
        "Lost":      {"color": TERTIARY,   "center": (1.0, 1.5), "n": 25},
        "Promising": {"color": ORANGE,     "center": (3.8, 2.0), "n": 25},
    }

    for seg, props in segments.items():
        cx, cy = props["center"]
        n = props["n"]
        x = np.clip(np.random.normal(cx, 0.4, n), 1, 5)
        y = np.clip(np.random.normal(cy, 0.4, n), 1, 5)
        sizes = np.random.uniform(30, 300, n)
        ax_scatter.scatter(x, y, s=sizes, color=props["color"], alpha=0.75,
                           edgecolors="none", label=seg)
        ax_scatter.annotate(seg, (cx, cy), fontsize=8, color=props["color"],
                            fontweight="bold", ha="center",
                            bbox=dict(boxstyle="round,pad=0.2", facecolor=BG,
                                      edgecolor=props["color"], alpha=0.7, linewidth=0.8))

    style_ax(ax_scatter, xlabel="Score Récence (1–5)",
             ylabel="Score Fréquence (1–5)",
             title="Scatter RFM — Segments clients")
    ax_scatter.set_xlim(0.5, 5.5)
    ax_scatter.set_ylim(0.5, 5.5)
    ax_scatter.grid(axis="both", color=SPINE, alpha=0.4)

    seg_names = list(segments.keys())
    seg_counts = [30, 35, 35, 25, 25]
    seg_colors = [segments[s]["color"] for s in seg_names]
    bars = ax_bar.barh(seg_names, seg_counts, color=seg_colors, height=0.6, alpha=0.9)
    for bar, count in zip(bars, seg_counts):
        ax_bar.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                    str(count), va="center", ha="left", color=MUTED, fontsize=8)
    style_ax(ax_bar, title="Répartition des segments")
    ax_bar.grid(axis="x", color=SPINE, alpha=0.4)
    ax_bar.grid(axis="y", alpha=0)
    ax_bar.set_xlim(0, 45)

    ax_kpi.set_facecolor(BG)
    ax_kpi.axis("off")
    kpis = [("2 543", "clients"), ("5", "segments"), ("3.2", "score moyen")]
    colors = [PRIMARY, QUATERNARY, TERTIARY]
    for i, (val, label) in enumerate(kpis):
        x_pos = 0.15 + i * 0.33
        rect = FancyBboxPatch((x_pos - 0.12, 0.1), 0.24, 0.8,
                              boxstyle="round,pad=0.03",
                              facecolor=SPINE, edgecolor=colors[i],
                              linewidth=1.2, transform=ax_kpi.transAxes)
        ax_kpi.add_patch(rect)
        ax_kpi.text(x_pos, 0.62, val, ha="center", va="center",
                    fontsize=20, fontweight="bold", color=colors[i],
                    transform=ax_kpi.transAxes)
        ax_kpi.text(x_pos, 0.3, label, ha="center", va="center",
                    fontsize=9, color=MUTED, transform=ax_kpi.transAxes)

    fig.suptitle("Segmentation RFM — Lapage E-commerce",
                 color=TEXT, fontsize=14, fontweight="bold", y=0.98)
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/ecommerce-lapage/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("1/8 RFM done")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Data Quality Audit
# ─────────────────────────────────────────────────────────────────────────────
def make_data_quality():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6.5), facecolor=BG)

    cols = ["product_id", "price", "category", "stock",
            "description", "supplier", "weight", "margin"]
    missing = [0, 2.1, 0, 18.3, 41.2, 7.8, 12.5, 34.7]
    bar_colors = []
    for v in missing:
        if v < 5:
            bar_colors.append(QUATERNARY)
        elif v <= 20:
            bar_colors.append(ORANGE)
        else:
            bar_colors.append(SECONDARY)

    bars = ax1.barh(cols, missing, color=bar_colors, height=0.6, alpha=0.9)
    for bar, val in zip(bars, missing):
        ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{val}%", va="center", color=MUTED, fontsize=8)
    ax1.axvline(20, color=SECONDARY, linestyle="--", linewidth=1.2, alpha=0.8)
    ax1.text(20.5, 7.2, "seuil 20%", color=SECONDARY, fontsize=7.5)
    style_ax(ax1, xlabel="% valeurs manquantes",
             title="Taux de valeurs manquantes")
    ax1.set_xlim(0, 50)
    ax1.grid(axis="x", color=SPINE, alpha=0.4)
    ax1.grid(axis="y", alpha=0)

    anom_types = ["Doublons", "Prix négatifs", "Stock < 0", "Refs manquantes"]
    detected = [127, 43, 89, 234]
    fixed = [127, 43, 89, 198]
    x = np.arange(len(anom_types))
    width = 0.35
    ax2.bar(x - width / 2, detected, width, label="Détectés",
            color=SECONDARY, alpha=0.9)
    ax2.bar(x + width / 2, fixed, width, label="Corrigés",
            color=QUATERNARY, alpha=0.9)
    for i, (d, f) in enumerate(zip(detected, fixed)):
        ax2.text(i - width / 2, d + 3, str(d), ha="center",
                 color=MUTED, fontsize=7.5)
        ax2.text(i + width / 2, f + 3, str(f), ha="center",
                 color=MUTED, fontsize=7.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(anom_types, fontsize=8)
    ax2.legend(facecolor=BG, edgecolor=SPINE, labelcolor=MUTED, fontsize=8)
    style_ax(ax2, title="Anomalies détectées & corrigées")

    fig.suptitle("Audit qualité données — Bottleneck",
                 color=TEXT, fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/ecommerce-python/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("2/8 Data Quality done")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Real estate SQL
# ─────────────────────────────────────────────────────────────────────────────
def make_immo():
    fig = plt.figure(figsize=(12, 6.5), facecolor=BG)
    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[3, 2],
                           wspace=0.35)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    n_paris = 120
    n_idf = 180
    s_paris = np.random.uniform(20, 80, n_paris)
    p_paris = 8000 + 6000 * (1 - (s_paris - 20) / 60) + np.random.normal(0, 800, n_paris)
    s_idf = np.random.uniform(40, 200, n_idf)
    p_idf = 4000 + 2000 * (1 - (s_idf - 40) / 160) + np.random.normal(0, 400, n_idf)

    ax1.scatter(s_paris, p_paris, color=PRIMARY, alpha=0.5, s=18,
                edgecolors="none", label="Paris intra-muros")
    ax1.scatter(s_idf, p_idf, color=TERTIARY, alpha=0.45, s=14,
                edgecolors="none", label="Île-de-France")

    for s_arr, p_arr, col in [(s_paris, p_paris, PRIMARY), (s_idf, p_idf, TERTIARY)]:
        m, b = np.polyfit(s_arr, p_arr, 1)
        x_line = np.linspace(s_arr.min(), s_arr.max(), 100)
        ax1.plot(x_line, m * x_line + b, color=col, linewidth=1.8, alpha=0.9)

    ax1.legend(facecolor=BG, edgecolor=SPINE, labelcolor=MUTED, fontsize=8)
    style_ax(ax1, xlabel="Surface habitable (m²)",
             ylabel="Prix/m² (€)",
             title="Prix/m² vs Surface habitable")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x/1000)}k"))

    types = ["Loft", "Studio", "T1", "T2", "T3", "T4", "Maison"]
    prices = [11200, 9800, 8500, 6200, 5100, 4300, 3800]
    n = len(types)
    palette = [mcolors.to_hex(
        np.array(mcolors.to_rgb(PRIMARY)) * (1 - i / (n - 1)) +
        np.array(mcolors.to_rgb(SECONDARY)) * (i / (n - 1))
    ) for i in range(n)]

    bars = ax2.barh(types, prices, color=palette, height=0.6, alpha=0.9)
    for bar, val in zip(bars, prices):
        ax2.text(bar.get_width() + 100, bar.get_y() + bar.get_height() / 2,
                 f"{val:,}€", va="center", color=MUTED, fontsize=8)
    style_ax(ax2, xlabel="€/m²", title="Prix médian/m² par type de bien")
    ax2.set_xlim(0, 14000)
    ax2.grid(axis="x", color=SPINE, alpha=0.4)
    ax2.grid(axis="y", alpha=0)

    fig.suptitle("Analyse DVF — 500 000 transactions immobilières",
                 color=TEXT, fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/immo-sql/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("3/8 Immo done")


# ─────────────────────────────────────────────────────────────────────────────
# 4. ACP + Clustering
# ─────────────────────────────────────────────────────────────────────────────
def make_acp():
    fig = plt.figure(figsize=(12, 6.5), facecolor=BG)
    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[11, 9], wspace=0.4)
    ax1 = fig.add_subplot(gs[0])

    cluster_params = [
        (PRIMARY,    (-2.5, 1.5), (1.0, 0.6),
         ["France", "Germany", "Italy", "Spain"]),
        (SECONDARY,  (2.0, 1.0),  (0.9, 0.7),
         ["Brazil", "Mexico", "Argentina"]),
        (TERTIARY,   (-1.0, -2.5), (1.1, 0.7),
         ["China", "India", "Japan"]),
        (QUATERNARY, (2.5, -1.5), (0.8, 0.6),
         ["USA", "Canada"]),
    ]

    for clr, (cx, cy), (sx, sy), labels in cluster_params:
        n = 15
        x = np.random.normal(cx, sx, n)
        y = np.random.normal(cy, sy, n)
        ax1.scatter(x, y, color=clr, alpha=0.75, s=40, edgecolors="none")
        ell = Ellipse((cx, cy), width=sx * 4, height=sy * 4,
                      facecolor=clr, alpha=0.12, edgecolor=clr,
                      linewidth=1, linestyle="--")
        ax1.add_patch(ell)
        for lbl in labels[:2]:
            xi = np.random.normal(cx, sx * 0.5)
            yi = np.random.normal(cy, sy * 0.5)
            ax1.annotate(lbl, (xi, yi), fontsize=7, color=clr,
                         fontweight="bold", alpha=0.9)

    style_ax(ax1, xlabel="PC1 (38% variance expliquée)",
             ylabel="PC2 (22% variance expliquée)",
             title="Projection ACP — PC1 vs PC2")
    ax1.grid(axis="both", color=SPINE, alpha=0.3)

    axes_labels = ["PIB/hab", "Disponibilité", "Population",
                   "Urbanisation", "Stabilité"]
    n_axes = len(axes_labels)
    angles = np.linspace(0, 2 * np.pi, n_axes, endpoint=False).tolist()
    angles += angles[:1]

    cluster_profiles = [
        [0.85, 0.70, 0.60, 0.80, 0.90],
        [0.45, 0.55, 0.85, 0.50, 0.40],
        [0.70, 0.80, 0.95, 0.75, 0.65],
        [0.90, 0.65, 0.55, 0.90, 0.85],
    ]
    cluster_colors = [PRIMARY, SECONDARY, TERTIARY, QUATERNARY]
    cluster_names = ["Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4"]

    ax2 = fig.add_subplot(gs[1], polar=True)
    ax2.set_facecolor(BG)
    ax2.spines["polar"].set_color(SPINE)
    ax2.tick_params(colors=MUTED, labelsize=7)
    ax2.grid(color=SPINE, alpha=0.5)

    for profile, clr, name in zip(cluster_profiles, cluster_colors, cluster_names):
        vals = profile + profile[:1]
        ax2.plot(angles, vals, color=clr, linewidth=1.8, label=name)
        ax2.fill(angles, vals, color=clr, alpha=0.1)

    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(axes_labels, fontsize=8, color=MUTED)
    ax2.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax2.set_yticklabels(["0.25", "0.5", "0.75", "1.0"], fontsize=6, color=MUTED)
    ax2.set_ylim(0, 1)
    ax2.set_title("Profil moyen par cluster", color=TEXT, fontsize=10,
                  fontweight="bold", pad=12)
    ax2.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1),
               facecolor=BG, edgecolor=SPINE, labelcolor=MUTED, fontsize=7)

    fig.suptitle("Expansion internationale — ACP & Clustering K-means",
                 color=TEXT, fontsize=14, fontweight="bold", y=1.01)
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/poulet-international/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("4/8 ACP done")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Power BI Dashboard Mockup
# ─────────────────────────────────────────────────────────────────────────────
def make_powerbi():
    fig = plt.figure(figsize=(12, 6.5), facecolor=BG)
    gs = gridspec.GridSpec(3, 4, figure=fig,
                           hspace=0.55, wspace=0.35,
                           height_ratios=[1.2, 2, 1.5])

    kpi_data = [
        ("1 247", "collaborateurs", PRIMARY),
        ("73%",   "satisfaction",   QUATERNARY),
        ("4.2j",  "absences moy.",  TERTIARY),
        ("3 840€","coût moyen",     SECONDARY),
    ]
    for i, (val, label, clr) in enumerate(kpi_data):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor(BG)
        ax.axis("off")
        rect = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                              boxstyle="round,pad=0.05",
                              facecolor=SPINE, edgecolor=clr,
                              linewidth=1.5, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(0.5, 0.62, val, ha="center", va="center",
                fontsize=18, fontweight="bold", color=clr,
                transform=ax.transAxes)
        ax.text(0.5, 0.28, label, ha="center", va="center",
                fontsize=8, color=MUTED, transform=ax.transAxes)

    ax_line = fig.add_subplot(gs[1, :])
    x = np.arange(12)
    months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun",
              "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]
    maladie = np.array([45, 52, 48, 61, 55, 43, 38, 42, 67, 71, 58, 63])
    accidents = np.array([8, 6, 9, 7, 10, 6, 5, 7, 11, 9, 8, 10])
    ax_line.plot(x, maladie, color=SECONDARY, linewidth=2,
                 marker="o", markersize=4, label="Maladie")
    ax_line.plot(x, accidents, color=TERTIARY, linewidth=2,
                 marker="s", markersize=4, label="Accidents")
    ax_line.set_xticks(x)
    ax_line.set_xticklabels(months, fontsize=8)
    ax_line.legend(facecolor=BG, edgecolor=SPINE, labelcolor=MUTED, fontsize=8)
    style_ax(ax_line, title="Évolution des absences mensuelles (2023)")

    ax_bar = fig.add_subplot(gs[2, :])
    depts = ["Production", "Logistique", "Ventes", "RH", "Finance", "IT"]
    values = [18.3, 14.7, 11.2, 9.8, 7.4, 6.1]
    bars = ax_bar.barh(depts, values, color=PRIMARY, height=0.5, alpha=0.9)
    for bar, val in zip(bars, values):
        ax_bar.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                    f"{val}j", va="center", color=MUTED, fontsize=8)
    style_ax(ax_bar, title="Absences par département (jours/an/personne)")
    ax_bar.grid(axis="x", color=SPINE, alpha=0.4)
    ax_bar.grid(axis="y", alpha=0)

    fig.suptitle("Dashboard RH — KPIs santé entreprise",
                 color=TEXT, fontsize=14, fontweight="bold", y=1.02)
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/powerbi-dashboard/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("5/8 PowerBI done")


# ─────────────────────────────────────────────────────────────────────────────
# 6. FAO Nutrition
# ─────────────────────────────────────────────────────────────────────────────
def make_sante():
    fig = plt.figure(figsize=(12, 6.5), facecolor=BG)
    gs = gridspec.GridSpec(2, 2, figure=fig, width_ratios=[2, 3],
                           hspace=0.5, wspace=0.4)
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])

    countries = ["Yemen", "Haïti", "Madagascar", "Mozambique", "Éthiopie",
                 "Niger", "RDC", "Tchad", "Zambie", "Rwanda",
                 "Tanzanie", "Uganda", "Malawi", "Angola", "Cameroun"]
    prevalences = [42.8, 39.1, 35.6, 33.2, 30.7, 28.4, 26.9, 25.3,
                   23.7, 21.4, 19.8, 17.6, 15.3, 13.9, 11.2]

    n = len(countries)
    bar_colors = [mcolors.to_hex(
        np.array(mcolors.to_rgb(QUATERNARY)) * (1 - i / (n - 1)) +
        np.array(mcolors.to_rgb(SECONDARY)) * (i / (n - 1))
    ) for i in range(n)]

    bars = ax1.barh(countries[::-1], prevalences[::-1],
                    color=bar_colors[::-1], height=0.65, alpha=0.9)
    for bar, val in zip(bars, prevalences[::-1]):
        ax1.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
                 f"{val}%", va="center", color=MUTED, fontsize=7)
    style_ax(ax1, xlabel="Prévalence (%)",
             title="Sous-nutrition — Top 15 pays")
    ax1.set_xlim(0, 52)
    ax1.grid(axis="x", color=SPINE, alpha=0.4)
    ax1.grid(axis="y", alpha=0)
    ax1.tick_params(axis="y", labelsize=7)

    years = np.arange(2000, 2023)
    afr = 28 + 2 * np.sin(np.linspace(0, 2.5, len(years))) + np.random.normal(0, 0.5, len(years))
    asia = 22 - np.linspace(0, 8, len(years)) + np.random.normal(0, 0.4, len(years))
    world = 15 - np.linspace(0, 5, len(years)) + np.random.normal(0, 0.3, len(years))
    ax2.plot(years, afr, color=SECONDARY, linewidth=2, label="Afrique subsaharienne")
    ax2.plot(years, asia, color=TERTIARY, linewidth=2, label="Asie du Sud")
    ax2.plot(years, world, color=PRIMARY, linewidth=2,
             linestyle="--", label="Monde")
    ax2.legend(facecolor=BG, edgecolor=SPINE, labelcolor=MUTED, fontsize=7)
    style_ax(ax2, ylabel="% sous-nutrition",
             title="Évolution mondiale 2000–2022")

    gdp = np.random.exponential(8000, 80)
    undernut = np.clip(35 - 0.002 * gdp + np.random.normal(0, 4, 80), 2, 45)
    pop = np.random.exponential(30, 80)
    regions = np.random.choice([PRIMARY, SECONDARY, TERTIARY, QUATERNARY], 80)
    ax3.scatter(gdp, undernut, s=pop * 0.8, color=regions, alpha=0.6,
                edgecolors="none")
    m, b = np.polyfit(gdp, undernut, 1)
    x_line = np.linspace(gdp.min(), gdp.max(), 100)
    ax3.plot(x_line, m * x_line + b, color=PRIMARY, linewidth=1.5, alpha=0.8)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x/1000)}k$"))
    style_ax(ax3, xlabel="PIB/hab", ylabel="Sous-nutrition",
             title="Corrélation PIB vs Sous-nutrition")

    fig.suptitle("Sous-nutrition mondiale — Analyse FAO",
                 color=TEXT, fontsize=14, fontweight="bold", y=1.01)
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/sante-publique/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("6/8 Santé done")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Socio-Demo dbt
# ─────────────────────────────────────────────────────────────────────────────
def make_sociodemo():
    fig = plt.figure(figsize=(12, 6.5), facecolor=BG)
    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[11, 9], wspace=0.4)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    age_groups = ["18-24", "25-29", "30-34", "35-39", "40-44", "45+"]
    oc_vals = [22, 31, 28, 12, 5, 2]
    market_vals = [14, 18, 19, 18, 16, 15]
    x = np.arange(len(age_groups))
    width = 0.35
    ax1.bar(x - width / 2, oc_vals, width, label="OC Apprenants",
            color=PRIMARY, alpha=0.9)
    ax1.bar(x + width / 2, market_vals, width, label="Marché national",
            color=TERTIARY, alpha=0.9)
    ax1.set_xticks(x)
    ax1.set_xticklabels(age_groups, fontsize=8)
    ax1.legend(facecolor=BG, edgecolor=SPINE, labelcolor=MUTED, fontsize=8)
    ax1.annotate("Surreprésentation\n25-34 ans",
                 xy=(1.5, 29.5), xytext=(3.2, 32),
                 fontsize=8, color=PRIMARY,
                 arrowprops=dict(arrowstyle="->", color=PRIMARY, lw=1.2))
    style_ax(ax1, ylabel="%",
             title="Profil apprenants OC vs Marché national")

    domains = ["Tech", "Data", "Design", "Marketing", "Gestion", "Autre"]
    oc_shares = [38, 22, 14, 12, 8, 6]
    nat_shares = [18, 10, 12, 18, 22, 20]
    colors_stacked = [PRIMARY, TERTIARY, QUATERNARY, ORANGE, SECONDARY, MUTED]

    oc_arr = np.array(oc_shares, dtype=float) / 100
    nat_arr = np.array(nat_shares, dtype=float) / 100

    lefts_oc = 0.0
    lefts_nat = 0.0
    for i, (oc_v, nat_v, clr) in enumerate(zip(oc_arr, nat_arr, colors_stacked)):
        ax2.barh([1], [oc_v], left=lefts_oc, color=clr, height=0.4, alpha=0.85,
                 label=domains[i])
        ax2.barh([0], [nat_v], left=lefts_nat, color=clr, height=0.4, alpha=0.85)
        lefts_oc += oc_v
        lefts_nat += nat_v

    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["National", "OC"], fontsize=9, color=MUTED)
    ax2.set_xlim(0, 1)
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x*100)}%"))
    ax2.legend(loc="upper right", facecolor=BG, edgecolor=SPINE,
               labelcolor=MUTED, fontsize=7, bbox_to_anchor=(1.0, -0.15),
               ncol=3)
    style_ax(ax2, title="Répartition par domaine — OC vs National")
    ax2.grid(axis="x", color=SPINE, alpha=0.4)
    ax2.grid(axis="y", alpha=0)

    fig.suptitle("Profils OC vs Marché du travail — Pipeline dbt",
                 color=TEXT, fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/socio-demo-dbt/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("7/8 Socio-demo done")


# ─────────────────────────────────────────────────────────────────────────────
# 8. SQL Wine Sales
# ─────────────────────────────────────────────────────────────────────────────
def make_sql_wine():
    fig = plt.figure(figsize=(12, 6.5), facecolor=BG)
    gs = gridspec.GridSpec(2, 2, figure=fig, width_ratios=[1, 1],
                           height_ratios=[11, 9], hspace=0.5, wspace=0.4)
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])

    regions = ["Bordeaux", "Bourgogne", "Champagne", "Rhône",
               "Loire", "Alsace", "Provence", "Languedoc"]
    ca_vals = [2850, 2420, 2180, 1760, 1340, 1120, 890, 650]
    n = len(regions)
    bar_colors = [mcolors.to_hex(
        np.array(mcolors.to_rgb(PRIMARY)) * (1 - i / (n - 1)) +
        np.array(mcolors.to_rgb(TERTIARY)) * (i / (n - 1))
    ) for i in range(n)]

    bars = ax1.bar(regions, ca_vals, color=bar_colors, alpha=0.9, width=0.6)
    for bar, val in zip(bars, ca_vals):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 30,
                 f"{val}k€", ha="center", color=MUTED, fontsize=7.5,
                 fontweight="bold")
    ax1.set_xticklabels(regions, rotation=35, ha="right", fontsize=7.5)
    style_ax(ax1, ylabel="CA (k€)", title="CA par région (€)")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}k"))

    dates = np.arange(36)
    trend = 800 + 200 * np.sin(dates * np.pi / 6) + dates * 15 + np.random.normal(0, 60, 36)
    ax2.plot(dates, trend, color=PRIMARY, linewidth=2)
    ax2.fill_between(dates, trend, alpha=0.2, color=PRIMARY)
    peak_idx = [int(np.argmax(trend[i * 12:(i + 1) * 12])) + i * 12 for i in range(3)]
    for pi in peak_idx:
        ax2.plot(dates[pi], trend[pi], "o", color=SECONDARY, markersize=6, zorder=5)
    ax2.set_xticks([0, 12, 24, 35])
    ax2.set_xticklabels(["Jan 2020", "Jan 2021", "Jan 2022", "Déc 2022"], fontsize=7.5)
    style_ax(ax2, title="Évolution CA mensuel 2020–2022")
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}k€"))

    donut_vals = [52, 28, 12, 8]
    donut_labels = ["Rouge", "Blanc", "Rosé", "Effervescent"]
    donut_colors = [PRIMARY, TERTIARY, QUATERNARY, SECONDARY]
    wedges, texts, autotexts = ax3.pie(
        donut_vals, labels=donut_labels, colors=donut_colors,
        autopct="%1.0f%%", startangle=90,
        wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
        textprops=dict(color=MUTED, fontsize=8),
    )
    for at in autotexts:
        at.set_color(TEXT)
        at.set_fontsize(8)
        at.set_fontweight("bold")
    ax3.set_facecolor(BG)
    ax3.set_title("Répartition CA par type", color=TEXT, fontsize=10,
                  fontweight="bold", pad=6)

    fig.suptitle("Analyse ventes — Requêtes SQL avancées",
                 color=TEXT, fontsize=14, fontweight="bold", y=1.01)
    plt.savefig("/home/elicesjo/GitHub/elicesjo.github.io/projets/sql-requetes/thumbnail.png",
                dpi=100, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("8/8 SQL Wine done")


if __name__ == "__main__":
    make_rfm()
    make_data_quality()
    make_immo()
    make_acp()
    make_powerbi()
    make_sante()
    make_sociodemo()
    make_sql_wine()

    paths = [
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/ecommerce-lapage/thumbnail.png",
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/ecommerce-python/thumbnail.png",
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/immo-sql/thumbnail.png",
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/poulet-international/thumbnail.png",
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/powerbi-dashboard/thumbnail.png",
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/sante-publique/thumbnail.png",
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/socio-demo-dbt/thumbnail.png",
        "/home/elicesjo/GitHub/elicesjo.github.io/projets/sql-requetes/thumbnail.png",
    ]
    print()
    for p in paths:
        size = os.path.getsize(p)
        print(f"{p.split('projets/')[1]:<50} {size/1024:>6.1f} KB")
