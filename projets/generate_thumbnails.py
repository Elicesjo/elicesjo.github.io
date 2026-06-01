import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
import os

np.random.seed(42)

PURPLE  = '#7B6FD4'
SALMON  = '#E07070'
BLUE    = '#5B8ED4'
TEAL    = '#4DBFA8'
ORANGE  = '#E8933A'
LPURPLE = '#B0A8E8'

TITLE_COLOR = '#1A1A2E'
AXIS_COLOR  = '#444466'
SPINE_COLOR = '#CCCCDD'
GRID_COLOR  = '#EEEEEE'


def base_style(ax):
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_color(SPINE_COLOR)
    ax.spines['left'].set_color(SPINE_COLOR)
    ax.tick_params(colors=AXIS_COLOR, labelsize=9)
    ax.xaxis.label.set_color(AXIS_COLOR)
    ax.yaxis.label.set_color(AXIS_COLOR)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)


def make_fig():
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.patch.set_facecolor('white')
    return fig, ax1, ax2


def save(fig, path):
    fig.savefig(path, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    size = os.path.getsize(path)
    print(f"{path.split('projets/')[1]:<50} {size/1024:>6.1f} KB")


# ── IMAGE 1 ────────────────────────────────────────────────────────────────────
def image1():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Segmentation RFM — Lapage", color=TITLE_COLOR, fontsize=14,
                 fontweight='bold', y=1.02)

    segments = ['Champions', 'Loyaux', 'Prometteurs', 'À risque', 'Perdus']
    vals     = [22, 18, 25, 21, 14]
    colors   = [PURPLE, TEAL, BLUE, ORANGE, SALMON]

    wedges, _ = ax1.pie(vals, colors=colors, startangle=90,
                        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
    ax1.text(0, 0, '2 543\nclients', ha='center', va='center',
             fontsize=11, fontweight='bold', color=TITLE_COLOR)
    ax1.legend(wedges, [f'{s}  {v}%' for s, v in zip(segments, vals)],
               loc='lower center', bbox_to_anchor=(0.5, -0.12), ncol=2,
               fontsize=8, frameon=False)
    ax1.set_title('Répartition des segments clients', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold', pad=10)

    ca    = [4820, 3650, 1240, 890, 210]
    y_pos = range(len(segments))
    bars  = ax2.barh(y_pos, ca, color=colors, edgecolor='white', height=0.6)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(segments, fontsize=9, color=AXIS_COLOR)
    ax2.set_xlabel('CA moyen (€)', color=AXIS_COLOR, fontsize=9)
    ax2.set_title('CA moyen par segment (€)', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    base_style(ax2)
    ax2.spines['left'].set_visible(False)
    ax2.yaxis.grid(False)
    for bar, v in zip(bars, ca):
        ax2.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
                 f'€{v:,}', va='center', fontsize=8.5, color=AXIS_COLOR)
    ax2.set_xlim(0, max(ca)*1.22)

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/ecommerce-lapage/thumbnail.png')


# ── IMAGE 2 ────────────────────────────────────────────────────────────────────
def image2():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Audit qualité données — Bottleneck", color=TITLE_COLOR,
                 fontsize=14, fontweight='bold', y=1.02)

    cols    = ['product_id', 'price', 'category', 'stock',
               'description', 'supplier', 'weight']
    missing = [0, 2.1, 0, 18.3, 41.2, 7.8, 12.5]
    bar_colors = [TEAL if v < 5 else (ORANGE if v <= 20 else SALMON) for v in missing]

    bars = ax1.bar(range(len(cols)), missing, color=bar_colors, edgecolor='white', width=0.65)
    ax1.set_xticks(range(len(cols)))
    ax1.set_xticklabels(cols, rotation=30, ha='right', fontsize=8.5, color=AXIS_COLOR)
    ax1.set_ylabel('Valeurs manquantes (%)', color=AXIS_COLOR, fontsize=9)
    ax1.set_title('Valeurs manquantes par colonne (%)', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax1.axhline(20, color=SALMON, linestyle='--', linewidth=1.2, alpha=0.8, label='Seuil 20%')
    ax1.legend(fontsize=8, frameon=False)
    base_style(ax1)
    for bar, v in zip(bars, missing):
        if v > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.6,
                     f'{v}%', ha='center', fontsize=8, color=AXIS_COLOR)

    categories = ['Produits', 'Commandes', 'Clients']
    valides    = [72, 85, 91]
    corrigees  = [18, 10, 7]
    supprimees = [10, 5, 2]
    x = np.arange(len(categories))
    w = 0.5
    ax2.bar(x, valides,    w, label='Valides',    color=TEAL,   edgecolor='white')
    ax2.bar(x, corrigees,  w, bottom=valides,     label='Corrigées',  color=BLUE,   edgecolor='white')
    ax2.bar(x, supprimees, w,
            bottom=[v+c for v, c in zip(valides, corrigees)],
            label='Supprimées', color=SALMON, edgecolor='white')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, fontsize=9, color=AXIS_COLOR)
    ax2.set_ylabel('Proportion (%)', color=AXIS_COLOR, fontsize=9)
    ax2.set_title('Statut des lignes après nettoyage', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax2.legend(fontsize=8, frameon=False, loc='upper right')
    ax2.set_ylim(0, 115)
    base_style(ax2)

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/ecommerce-python/thumbnail.png')


# ── IMAGE 3 ────────────────────────────────────────────────────────────────────
def image3():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Base DVF — 500 000 transactions", color=TITLE_COLOR,
                 fontsize=14, fontweight='bold', y=1.02)

    types = ['Studio', 'T1', 'T2', 'T3', 'T4', 'Maison']
    data  = [
        np.random.normal(5800, 900, 120),
        np.random.normal(4900, 800, 120),
        np.random.normal(4200, 750, 120),
        np.random.normal(3600, 700, 120),
        np.random.normal(3100, 650, 120),
        np.random.normal(2400, 600, 120),
    ]
    ax1.boxplot(data, vert=False, patch_artist=True,
                medianprops=dict(color=ORANGE, linewidth=2),
                flierprops=dict(marker='o', markersize=3, alpha=0.4,
                                markerfacecolor=PURPLE, markeredgecolor='none'),
                whiskerprops=dict(color=SPINE_COLOR),
                capprops=dict(color=SPINE_COLOR),
                boxprops=dict(facecolor=PURPLE, alpha=0.6, edgecolor=SPINE_COLOR))
    ax1.set_yticks(range(1, len(types)+1))
    ax1.set_yticklabels(types, fontsize=9, color=AXIS_COLOR)
    ax1.set_xlabel('Prix/m² (€)', color=AXIS_COLOR, fontsize=9)
    ax1.set_title('Distribution prix/m² par type de bien', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    base_style(ax1)
    ax1.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax1.yaxis.grid(False)

    depts = ['75 Paris', '69 Rhône', '13 B-du-R.', '33 Gironde',
             '06 A-Mar.', '31 Haute-G.', '59 Nord', '67 Bas-Rhin']
    tx   = [48320, 31450, 27800, 22100, 19600, 17300, 15800, 13200]
    blues = [BLUE]*4 + [LPURPLE]*4
    bars  = ax2.barh(range(len(depts)), tx, color=blues, edgecolor='white', height=0.65)
    ax2.set_yticks(range(len(depts)))
    ax2.set_yticklabels(depts, fontsize=8.5, color=AXIS_COLOR)
    ax2.set_xlabel('Nombre de transactions', color=AXIS_COLOR, fontsize=9)
    ax2.set_title('Transactions par département (top 8)', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    base_style(ax2)
    ax2.spines['left'].set_visible(False)
    ax2.yaxis.grid(False)
    for bar, v in zip(bars, tx):
        ax2.text(bar.get_width() + 300, bar.get_y() + bar.get_height()/2,
                 f'{v:,}', va='center', fontsize=8, color=AXIS_COLOR)
    ax2.set_xlim(0, max(tx)*1.2)

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/immo-sql/thumbnail.png')


# ── IMAGE 4 ────────────────────────────────────────────────────────────────────
def image4():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Expansion internationale — Clustering pays", color=TITLE_COLOR,
                 fontsize=14, fontweight='bold', y=1.02)

    cluster_colors_map = {0: PURPLE, 1: SALMON, 2: BLUE, 3: TEAL}
    centers = [(0.8, 1.2), (-1.2, 0.8), (1.5, -0.9), (-0.9, -1.3)]
    counts  = [14, 15, 13, 13]

    pts_list = []
    labels_list = []
    for i, (cx, cy) in enumerate(centers):
        p = np.column_stack([
            np.random.normal(cx, 0.55, counts[i]),
            np.random.normal(cy, 0.55, counts[i]),
        ])
        pts_list.append(p)
        labels_list.extend([i]*counts[i])

    all_pts   = np.vstack(pts_list)
    colors_pts = [cluster_colors_map[c] for c in labels_list]

    ax1.scatter(all_pts[:, 0], all_pts[:, 1], c=colors_pts,
                s=60, alpha=0.85, edgecolors='white', linewidth=0.5, zorder=3)

    for i, (cx, cy) in enumerate(centers):
        ell = Ellipse((cx, cy), width=1.6, height=1.4, angle=20*i,
                      edgecolor=cluster_colors_map[i],
                      facecolor=cluster_colors_map[i], alpha=0.12, zorder=1)
        ax1.add_patch(ell)

    country_pts = {
        'France':    (0.6,  1.4),
        'Brésil':    (-1.0, 0.5),
        'Inde':      (1.3,  -0.6),
        'Allemagne': (0.9,  0.9),
        'Nigéria':   (-0.8, -1.5),
        'Chine':     (1.7,  -1.1),
    }
    for name, (x, y) in country_pts.items():
        ax1.annotate(name, (x, y), fontsize=7.5, color=TITLE_COLOR,
                     xytext=(x+0.18, y+0.18), ha='left')

    legend_handles = [mpatches.Patch(color=cluster_colors_map[i], label=f'Cluster {i+1}')
                      for i in range(4)]
    ax1.legend(handles=legend_handles, fontsize=8, frameon=False, loc='upper left')
    ax1.set_xlabel('PC1', color=AXIS_COLOR, fontsize=9)
    ax1.set_ylabel('PC2', color=AXIS_COLOR, fontsize=9)
    ax1.set_title('ACP — Projection des pays (PC1 vs PC2)', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    base_style(ax1)
    ax1.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)

    indicators = ['PIB', 'Nutrition', 'Population', 'Urbanisation', 'Stabilité']
    cluster_scores = np.array([
        [0.82, 0.78, 0.55, 0.88, 0.91],
        [0.45, 0.52, 0.80, 0.42, 0.38],
        [0.65, 0.60, 0.70, 0.65, 0.58],
        [0.30, 0.40, 0.90, 0.35, 0.25],
    ])
    x = np.arange(len(indicators))
    w = 0.18
    cluster_colors_list = [PURPLE, SALMON, BLUE, TEAL]
    for i in range(4):
        ax2.bar(x + i*w, cluster_scores[i], w, label=f'Cluster {i+1}',
                color=cluster_colors_list[i], edgecolor='white')
    ax2.set_xticks(x + w*1.5)
    ax2.set_xticklabels(indicators, fontsize=9, color=AXIS_COLOR)
    ax2.set_ylabel('Score moyen', color=AXIS_COLOR, fontsize=9)
    ax2.set_title('Score moyen par cluster — 5 indicateurs', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax2.legend(fontsize=8, frameon=False, ncol=2)
    ax2.set_ylim(0, 1.1)
    base_style(ax2)

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/poulet-international/thumbnail.png')


# ── IMAGE 5 ────────────────────────────────────────────────────────────────────
def image5():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Dashboard RH — KPIs Santé Entreprise", color=TITLE_COLOR,
                 fontsize=14, fontweight='bold', y=1.02)

    months  = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
               'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    maladie  = [42, 48, 38, 35, 29, 25, 31, 22, 33, 39, 45, 51]
    accidents= [8,  10,  7,  9,  6,  5,  7,  4,  8,  9, 11,  8]
    x = range(12)

    ax1.plot(x, maladie,   color=SALMON, linewidth=2.5, label='Maladie',   zorder=3)
    ax1.fill_between(x, maladie, alpha=0.15, color=SALMON)
    ax1.plot(x, accidents, color=BLUE,   linewidth=1.8, label='Accidents', zorder=3)

    min_m, max_m = int(np.argmin(maladie)), int(np.argmax(maladie))
    min_a, max_a = int(np.argmin(accidents)), int(np.argmax(accidents))
    ax1.plot(min_m, maladie[min_m],   'o', color=TEAL,   markersize=8, zorder=5)
    ax1.plot(max_m, maladie[max_m],   'o', color=ORANGE, markersize=8, zorder=5)
    ax1.plot(min_a, accidents[min_a], 'o', color=TEAL,   markersize=7, zorder=5)
    ax1.plot(max_a, accidents[max_a], 'o', color=ORANGE, markersize=7, zorder=5)

    ax1.set_xticks(range(12))
    ax1.set_xticklabels(months, fontsize=8.5, color=AXIS_COLOR)
    ax1.set_ylabel("Nombre d'absences", color=AXIS_COLOR, fontsize=9)
    ax1.set_title('Absences mensuelles 2023', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax1.legend(fontsize=8.5, frameon=False)
    base_style(ax1)
    ax1.xaxis.grid(False)

    depts = ['Production', 'Logistique', 'Commercial', 'Admin', 'IT', 'RH', 'Direction']
    taux  = [6.8, 5.9, 4.5, 3.8, 3.1, 2.7, 2.1]
    bars  = ax2.barh(range(len(depts)), taux, color=PURPLE, edgecolor='white', height=0.6)
    ax2.axvline(4.2, color=ORANGE, linestyle='--', linewidth=1.3,
                label='Moy. entreprise 4.2%')
    ax2.set_yticks(range(len(depts)))
    ax2.set_yticklabels(depts, fontsize=9, color=AXIS_COLOR)
    ax2.set_xlabel("Taux d'absentéisme (%)", color=AXIS_COLOR, fontsize=9)
    ax2.set_title("Taux d'absentéisme par département (%)", color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax2.legend(fontsize=8, frameon=False)
    base_style(ax2)
    ax2.spines['left'].set_visible(False)
    ax2.yaxis.grid(False)
    for bar, v in zip(bars, taux):
        ax2.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height()/2,
                 f'{v}%', va='center', fontsize=8.5, color=AXIS_COLOR)
    ax2.set_xlim(0, max(taux)*1.25)

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/powerbi-dashboard/thumbnail.png')


# ── IMAGE 6 ────────────────────────────────────────────────────────────────────
def image6():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Sous-nutrition mondiale — Analyse FAO", color=TITLE_COLOR,
                 fontsize=14, fontweight='bold', y=1.02)

    years   = np.arange(2000, 2023)
    afrique = 28 - np.linspace(0, 4, len(years)) + np.random.normal(0, 0.6, len(years))
    asie    = 22 - np.linspace(0, 10, len(years)) + np.random.normal(0, 0.5, len(years))
    amerique= 11 - np.linspace(0, 4, len(years)) + np.random.normal(0, 0.4, len(years))
    monde   = 15 - np.linspace(0, 5, len(years)) + np.random.normal(0, 0.3, len(years))

    ax1.plot(years, afrique,  color=SALMON,  linewidth=1.8, label='Afrique subsaharienne')
    ax1.plot(years, asie,     color=BLUE,    linewidth=1.8, label='Asie du Sud')
    ax1.plot(years, amerique, color=TEAL,    linewidth=1.8, label='Amérique latine')
    ax1.plot(years, monde,    color=PURPLE,  linewidth=2.4, linestyle='--', label='Monde')
    ax1.set_xlabel('Année', color=AXIS_COLOR, fontsize=9)
    ax1.set_ylabel('Prévalence (%)', color=AXIS_COLOR, fontsize=9)
    ax1.set_title('Évolution prévalence 2000–2022 (%)', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax1.legend(fontsize=8, frameon=False)
    base_style(ax1)
    ax1.xaxis.grid(False)

    regions    = ["Asie du Sud", "Afrique sub.", "Asie de l'Est",
                  "Afrique du N.", "Am. latine", "Proche-Orient"]
    sizes      = [38, 28, 14, 8, 7, 5]
    colors_pie = [BLUE, SALMON, PURPLE, TEAL, ORANGE, LPURPLE]
    explode    = [0.06, 0, 0, 0, 0, 0]

    wedges, texts, autotexts = ax2.pie(
        sizes, labels=regions, colors=colors_pie, autopct='%1.0f%%',
        startangle=140, explode=explode,
        textprops=dict(color=AXIS_COLOR, fontsize=8),
        wedgeprops=dict(edgecolor='white', linewidth=1.5))
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color(TITLE_COLOR)
    ax2.set_title('Population sous-alimentée par région', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/sante-publique/thumbnail.png')


# ── IMAGE 7 ────────────────────────────────────────────────────────────────────
def image7():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Profils OC vs Marché national — Pipeline dbt", color=TITLE_COLOR,
                 fontsize=14, fontweight='bold', y=1.02)

    age_groups = ['<18', '18-24', '25-34', '35-44', '45-54', '55+']
    oc         = [2, 18, 38, 22, 13, 7]
    national   = [5, 14, 22, 21, 20, 18]
    x = np.arange(len(age_groups))
    w = 0.35

    ax1.bar(x - w/2, oc,       w, label='OC',       color=PURPLE, edgecolor='white')
    ax1.bar(x + w/2, national, w, label='National',  color=BLUE,   edgecolor='white')
    ax1.set_xticks(x)
    ax1.set_xticklabels(age_groups, fontsize=9, color=AXIS_COLOR)
    ax1.set_ylabel('Proportion (%)', color=AXIS_COLOR, fontsize=9)
    ax1.set_title("Répartition par tranche d'âge (%)", color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax1.legend(fontsize=9, frameon=False)
    base_style(ax1)

    ax1.annotate('Surreprésentation',
                 xy=(x[2] - w/2, oc[2]),
                 xytext=(x[2] + 0.7, oc[2] + 8),
                 fontsize=7.5, color=SALMON,
                 arrowprops=dict(arrowstyle='->', color=SALMON, lw=1.2))

    domains = ['Tech & Data', 'Business', 'Design', 'Marketing',
               'Management', 'Langues', 'Autre']
    oc_d    = [32, 22, 15, 12, 8, 5, 6]
    nat_d   = [18, 25, 10, 15, 14, 9, 9]
    stacked_colors = [PURPLE, BLUE, TEAL, ORANGE, SALMON, LPURPLE, '#AAAACC']

    y_labels  = ['OC Apprenants', 'Marché']
    data_rows = [oc_d, nat_d]
    for row_idx, (label, vals) in enumerate(zip(y_labels, data_rows)):
        left = 0
        for col_idx, (v, color) in enumerate(zip(vals, stacked_colors)):
            ax2.barh(row_idx, v, left=left, color=color, edgecolor='white',
                     height=0.5,
                     label=domains[col_idx] if row_idx == 0 else '')
            if v > 5:
                ax2.text(left + v/2, row_idx, f'{v}%',
                         ha='center', va='center',
                         fontsize=7.5, color='white', fontweight='bold')
            left += v

    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(y_labels, fontsize=9, color=AXIS_COLOR)
    ax2.set_xlabel('Proportion (%)', color=AXIS_COLOR, fontsize=9)
    ax2.set_title('Domaines de formation (%)', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    ax2.legend(handles=[mpatches.Patch(color=stacked_colors[i], label=domains[i])
                        for i in range(len(domains))],
               fontsize=7, frameon=False, loc='lower center',
               bbox_to_anchor=(0.5, -0.38), ncol=4)
    base_style(ax2)
    ax2.spines['left'].set_visible(False)
    ax2.yaxis.grid(False)

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/socio-demo-dbt/thumbnail.png')


# ── IMAGE 8 ────────────────────────────────────────────────────────────────────
def image8():
    fig, ax1, ax2 = make_fig()
    fig.suptitle("Analyse ventes vins — Requêtes SQL", color=TITLE_COLOR,
                 fontsize=14, fontweight='bold', y=1.02)

    regions = ['Bordeaux', 'Bourgogne', 'Rhône', 'Champagne',
               'Alsace', 'Loire', 'Provence', 'Languedoc']
    ca      = [480, 390, 310, 275, 198, 165, 142, 118]
    purple_shades = ['#5A50B0', '#6A64C4', '#7B6FD4', '#8C80DC',
                     '#9D92E4', '#AEA4EC', '#BEB8F0', '#CECAF5']

    bars = ax1.bar(range(len(regions)), ca, color=purple_shades,
                   edgecolor='white', width=0.65)
    ax1.set_xticks(range(len(regions)))
    ax1.set_xticklabels(regions, rotation=30, ha='right', fontsize=8.5, color=AXIS_COLOR)
    ax1.set_ylabel('CA (k€)', color=AXIS_COLOR, fontsize=9)
    ax1.set_title('CA par région vinicole (k€)', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')
    base_style(ax1)
    for bar, v in zip(bars, ca):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'{v}', ha='center', fontsize=8.5, color=AXIS_COLOR, fontweight='bold')
    ax1.set_ylim(0, max(ca)*1.18)

    wine_types = ['Rouge', 'Blanc', 'Rosé', 'Effervescent']
    sizes      = [52, 28, 12, 8]
    colors_pie = [SALMON, BLUE, TEAL, ORANGE]
    wedges, _ = ax2.pie(sizes, colors=colors_pie, startangle=90,
                        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
    ax2.text(0, 0, '€2.4M', ha='center', va='center',
             fontsize=13, fontweight='bold', color=TITLE_COLOR)
    ax2.legend(wedges, [f'{t}  {s}%' for t, s in zip(wine_types, sizes)],
               loc='lower center', bbox_to_anchor=(0.5, -0.12), ncol=2,
               fontsize=8.5, frameon=False)
    ax2.set_title('Répartition CA par type de vin', color=TITLE_COLOR,
                  fontsize=13, fontweight='bold')

    fig.tight_layout()
    save(fig, '/home/elicesjo/GitHub/elicesjo.github.io/projets/sql-requetes/thumbnail.png')


if __name__ == '__main__':
    image1()
    image2()
    image3()
    image4()
    image5()
    image6()
    image7()
    image8()
    print("\nAll done.")
