import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

np.random.seed(42)

BG = '#0D0D0D'
TEXT = '#C8C8E0'
PRIMARY = '#9B9BD4'
SECONDARY = '#7B7BB8'
ACCENT = '#E89090'
FIGSIZE = (12, 6.5)
DPI = 100

def apply_dark_style(fig, ax_list):
    fig.patch.set_facecolor(BG)
    for ax in ax_list:
        ax.set_facecolor(BG)
        ax.tick_params(colors=TEXT, labelsize=11)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor(SECONDARY)

# 1. sql-requetes — vertical bar chart
def chart_sql():
    regions = ['Bordeaux', 'Bourgogne', 'Alsace', 'Rhône', 'Loire', 'Champagne', 'Languedoc', 'Provence']
    ca = [4.2, 3.8, 2.1, 2.9, 1.7, 3.3, 1.4, 1.9]

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    apply_dark_style(fig, [ax])

    bars = ax.bar(regions, ca, color=PRIMARY, width=0.6, zorder=2)
    ax.set_title("CA par région vinicole (top 8)", fontsize=16, fontweight='bold', pad=16, color=TEXT)
    ax.set_ylabel("CA (M€)", fontsize=12, color=TEXT)
    ax.set_xlabel("Région", fontsize=12, color=TEXT)
    ax.yaxis.grid(True, color=SECONDARY, alpha=0.3, linestyle='--', zorder=1)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, ca):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{val:.1f}M', ha='center', va='bottom', color=TEXT, fontsize=11, fontweight='bold')

    fig.tight_layout()
    out = '/home/elicesjo/GitHub/elicesjo.github.io/projets/sql-requetes/thumbnail.png'
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    return out

# 2. immo-sql — scatter plot
def chart_immo():
    n1, n2 = 100, 100
    # Paris: high price, small surface
    surface1 = np.random.normal(35, 8, n1).clip(15, 70)
    price1 = np.random.normal(10500, 1500, n1).clip(6000, 16000)
    # Province: lower price, larger surface
    surface2 = np.random.normal(90, 25, n2).clip(30, 180)
    price2 = np.random.normal(3200, 800, n2).clip(1200, 6000)

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    apply_dark_style(fig, [ax])

    ax.scatter(surface1, price1, color=PRIMARY, alpha=0.7, s=40, label='Paris', zorder=3)
    ax.scatter(surface2, price2, color=ACCENT, alpha=0.7, s=40, label='Province', zorder=3)

    ax.set_title("Prix/m² vs Surface — DVF", fontsize=16, fontweight='bold', pad=16, color=TEXT)
    ax.set_xlabel("Surface (m²)", fontsize=12, color=TEXT)
    ax.set_ylabel("Prix/m²  (€)", fontsize=12, color=TEXT)
    ax.yaxis.grid(True, color=SECONDARY, alpha=0.3, linestyle='--', zorder=1)
    ax.xaxis.grid(True, color=SECONDARY, alpha=0.3, linestyle='--', zorder=1)
    ax.set_axisbelow(True)

    legend = ax.legend(fontsize=11, facecolor='#1A1A2E', edgecolor=SECONDARY, labelcolor=TEXT)

    fig.tight_layout()
    out = '/home/elicesjo/GitHub/elicesjo.github.io/projets/immo-sql/thumbnail.png'
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    return out

# 3. sante-publique — horizontal bar chart
def chart_sante():
    regions = ['Afrique sub-sah.', 'Asie du Sud', 'Asie du SE', 'Amérique Lat.',
               'Afrique du Nord', 'Asie centrale', 'Moyen-Orient', 'Europe Est']
    prevalence = [22.4, 15.8, 11.2, 8.7, 6.3, 4.9, 3.8, 2.1]

    sorted_idx = np.argsort(prevalence)
    regions_s = [regions[i] for i in sorted_idx]
    prev_s = [prevalence[i] for i in sorted_idx]

    n = len(regions_s)
    colors = [PRIMARY if i < n // 2 else SECONDARY for i in range(n)]

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    apply_dark_style(fig, [ax])

    bars = ax.barh(regions_s, prev_s, color=colors, height=0.6, zorder=2)
    ax.set_title("Prévalence sous-nutrition par région (FAO)", fontsize=16, fontweight='bold', pad=16, color=TEXT)
    ax.set_xlabel("Prévalence (%)", fontsize=12, color=TEXT)
    ax.xaxis.grid(True, color=SECONDARY, alpha=0.3, linestyle='--', zorder=1)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, prev_s):
        ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}%', va='center', ha='left', color=TEXT, fontsize=11, fontweight='bold')

    ax.set_xlim(0, max(prev_s) * 1.18)
    fig.tight_layout()
    out = '/home/elicesjo/GitHub/elicesjo.github.io/projets/sante-publique/thumbnail.png'
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    return out

# 4. ecommerce-python — two subplots
def chart_ecommerce():
    cols = ['prix', 'quantite', 'categorie', 'date', 'client_id', 'remise']
    missing_pct = [12.3, 5.7, 8.1, 2.4, 15.6, 9.8]

    categories = ['prix', 'quantite', 'remise']
    before = [12.3, 5.7, 9.8]
    after = [0.0, 0.0, 0.0]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE, dpi=DPI)
    apply_dark_style(fig, [ax1, ax2])

    x1 = np.arange(len(cols))
    ax1.bar(x1, missing_pct, color=PRIMARY, width=0.6, zorder=2)
    ax1.set_title("Valeurs manquantes par colonne", fontsize=13, fontweight='bold', pad=12, color=TEXT)
    ax1.set_xticks(x1)
    ax1.set_xticklabels(cols, rotation=30, ha='right', fontsize=10)
    ax1.set_ylabel("% manquant", fontsize=11, color=TEXT)
    ax1.yaxis.grid(True, color=SECONDARY, alpha=0.3, linestyle='--', zorder=1)
    ax1.set_axisbelow(True)
    for xi, val in zip(x1, missing_pct):
        ax1.text(xi, val + 0.2, f'{val:.1f}%', ha='center', va='bottom', color=TEXT, fontsize=9, fontweight='bold')

    x2 = np.arange(len(categories))
    w = 0.35
    ax2.bar(x2 - w/2, before, width=w, color=PRIMARY, label='Avant', zorder=2)
    ax2.bar(x2 + w/2, after, width=w, color=ACCENT, label='Après', zorder=2)
    ax2.set_title("Avant / Après correction", fontsize=13, fontweight='bold', pad=12, color=TEXT)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(categories, fontsize=11)
    ax2.set_ylabel("% manquant", fontsize=11, color=TEXT)
    ax2.yaxis.grid(True, color=SECONDARY, alpha=0.3, linestyle='--', zorder=1)
    ax2.set_axisbelow(True)
    legend2 = ax2.legend(fontsize=11, facecolor='#1A1A2E', edgecolor=SECONDARY, labelcolor=TEXT)

    fig.tight_layout(pad=2.0)
    out = '/home/elicesjo/GitHub/elicesjo.github.io/projets/ecommerce-python/thumbnail.png'
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    return out

paths = [chart_sql(), chart_immo(), chart_sante(), chart_ecommerce()]
for p in paths:
    size = os.path.getsize(p)
    print(f"{p}  →  {size:,} bytes")
