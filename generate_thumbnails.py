import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
from pathlib import Path

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.alpha": 0.25,
    "grid.linewidth": 0.6,
    "figure.facecolor": "white",
    "axes.facecolor": "#F8F8FF",
})

BASE = Path("/home/elicesjo/GitHub/elicesjo.github.io/projets")

# Gradient bleu → violet sur 7 projets
PALETTE = [
    "#5B7DBF",  # 1 bleu
    "#6B85C4",  # 2
    "#7B8DCA",  # 3
    "#8B8ECF",  # 4
    "#9B90D4",  # 5
    "#A992D8",  # 6
    "#B794DC",  # 7 violet
]
LIGHT = "#E8E8F5"
GRAY  = "#7A7A9A"
WHITE = "white"


def save(fig, slug):
    out = BASE / slug / "thumbnail.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {slug}/thumbnail.png")


def bar_colors(n, base):
    """n barres : la première en base, les suivantes en LIGHT."""
    return [base if i == 0 else LIGHT for i in range(n)]


# ── 1. SQL Requêtes ──────────────────────────────────────────────────────────
C = PALETTE[0]
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.38, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Analyse des ventes — Marchand de vin", fontsize=12, fontweight="bold",
             color="#3A3A5C", x=0.5, y=0.97)

vins = ["Bordeaux", "Bourgogne", "Rhône", "Alsace", "Loire"]
ventes = [51000, 42000, 35000, 28000, 19000]
ax = axes[0]
bars = ax.barh(vins, ventes, color=bar_colors(len(vins), C), height=0.55, edgecolor="none")
ax.set_xlabel("CA (€)", color=GRAY, fontsize=9)
ax.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(LIGHT)
for bar, val in zip(bars, ventes):
    ax.text(val + 600, bar.get_y() + bar.get_height() / 2,
            f"{val/1000:.0f}k€", va="center", color="#3A3A5C", fontsize=8, fontweight="bold")
ax.set_title("CA par région", fontsize=10, color="#4A4A6A", pad=8)

ax2 = axes[1]
mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun"]
ca = [18, 22, 31, 27, 35, 29]
ax2.plot(mois, ca, color=C, linewidth=2.5, marker="o", markersize=7,
         markerfacecolor=WHITE, markeredgecolor=C, markeredgewidth=2)
ax2.fill_between(range(len(mois)), ca, alpha=0.1, color=C)
ax2.set_ylabel("CA (k€)", color=GRAY, fontsize=9)
ax2.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax2.set_xticks(range(len(mois)))
ax2.set_xticklabels(mois)
ax2.spines["left"].set_color(LIGHT)
ax2.spines["bottom"].set_color(LIGHT)
ax2.set_title("Évolution mensuelle", fontsize=10, color="#4A4A6A", pad=8)
save(fig, "sql-requetes")


# ── 2. Santé publique ────────────────────────────────────────────────────────
C = PALETTE[1]
C2 = PALETTE[3]
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Sous-nutrition mondiale — Analyse FAO", fontsize=12, fontweight="bold",
             color="#3A3A5C", y=0.97)

regions = ["Afrique\nsub-sah.", "Asie\ndu Sud", "Asie\nde l'Est", "Am.\nLatine", "Océanie"]
taux = [23.4, 15.1, 8.3, 6.5, 4.2]
grad5 = [PALETTE[0], PALETTE[1], PALETTE[3], PALETTE[5], PALETTE[6]]

ax = axes[0]
bars = ax.bar(regions, taux, color=grad5, edgecolor="none", width=0.6)
ax.set_ylabel("Taux (%)", color=GRAY, fontsize=9)
ax.tick_params(labelcolor="#4A4A6A", labelsize=8)
ax.spines["left"].set_color(LIGHT)
ax.spines["bottom"].set_color(LIGHT)
for bar, val in zip(bars, taux):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.4, f"{val}%",
            ha="center", color="#3A3A5C", fontsize=8, fontweight="bold")
ax.set_title("Taux de sous-nutrition par région", fontsize=10, color="#4A4A6A", pad=8)

ax2 = axes[1]
items = ["Céréales", "Légumineuses", "Fruits/Lég.", "Protéines", "Laitiers"]
dispo = [2850, 890, 640, 310, 180]
besoins = [2100, 700, 800, 400, 250]
x = np.arange(len(items))
w = 0.35
ax2.bar(x - w / 2, dispo, w, label="Disponible", color=C, alpha=0.9, edgecolor="none")
ax2.bar(x + w / 2, besoins, w, label="Besoin min.", color=LIGHT, alpha=0.9, edgecolor=C2, linewidth=0.8)
ax2.set_xticks(x)
ax2.set_xticklabels(items, fontsize=7.5, color="#4A4A6A")
ax2.tick_params(labelcolor="#4A4A6A", labelsize=8)
ax2.spines["left"].set_color(LIGHT)
ax2.spines["bottom"].set_color(LIGHT)
ax2.legend(fontsize=8, framealpha=0.8)
ax2.set_ylabel("kcal/pers./j", color=GRAY, fontsize=9)
ax2.set_title("Disponible vs Besoin", fontsize=10, color="#4A4A6A", pad=8)
save(fig, "sante-publique")


# ── 3. BDD Immobilier ────────────────────────────────────────────────────────
C = PALETTE[2]
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Base de données immobilière — DVF", fontsize=12, fontweight="bold",
             color="#3A3A5C", y=0.97)

villes = ["Paris", "Lyon", "Bordeaux", "Nantes", "Marseille"]
prix = [10200, 5100, 4800, 4200, 3600]
colors_v = [PALETTE[0], PALETTE[2], PALETTE[3], LIGHT, LIGHT]

ax = axes[0]
bars = ax.bar(villes, prix, color=colors_v, edgecolor="none", width=0.6)
ax.set_ylabel("Prix moyen (€/m²)", color=GRAY, fontsize=9)
ax.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax.spines["left"].set_color(LIGHT)
ax.spines["bottom"].set_color(LIGHT)
for bar, val in zip(bars, prix):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 120, f"{val:,}€",
            ha="center", color="#3A3A5C", fontsize=8, fontweight="bold")
ax.set_title("Prix moyen au m² par ville", fontsize=10, color="#4A4A6A", pad=8)

ax2 = axes[1]
types = ["Appart.\nT1-T2", "Appart.\nT3-T4", "Maison\npetite", "Maison\ngrande"]
parts = [38, 29, 21, 12]
colors_p = [PALETTE[0], PALETTE[2], PALETTE[4], LIGHT]
wedges, texts, autotexts = ax2.pie(
    parts, labels=types, colors=colors_p, autopct="%1.0f%%", startangle=90,
    textprops={"fontsize": 8, "color": "#4A4A6A"},
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
for at in autotexts:
    at.set_fontweight("bold")
    at.set_color("#3A3A5C")
ax2.set_title("Répartition par type de bien", fontsize=10, color="#4A4A6A", pad=8)
ax2.set_facecolor("white")
save(fig, "immo-sql")


# ── 4. E-commerce Python ─────────────────────────────────────────────────────
C = PALETTE[3]
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Optimisation données e-commerce — Boutique vin", fontsize=12,
             fontweight="bold", color="#3A3A5C", y=0.97)

ax = axes[0]
categories = ["Complets", "Manquants", "Doublons", "Incohérents"]
avant = [1240, 380, 145, 92]
apres = [1824, 18, 0, 0]
x = np.arange(len(categories))
w = 0.35
ax.bar(x - w / 2, avant, w, label="Avant audit", color=LIGHT, alpha=0.9, edgecolor=C, linewidth=0.8)
ax.bar(x + w / 2, apres, w, label="Après nettoyage", color=C, alpha=0.9, edgecolor="none")
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8.5, color="#4A4A6A")
ax.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax.spines["left"].set_color(LIGHT)
ax.spines["bottom"].set_color(LIGHT)
ax.legend(fontsize=8.5, framealpha=0.8)
ax.set_ylabel("Nb lignes", color=GRAY, fontsize=9)
ax.set_title("Audit qualité des données", fontsize=10, color="#4A4A6A", pad=8)

ax2 = axes[1]
produits = ["Bordeaux\nRouge", "Champagne", "Sancerre", "Côtes Rhône", "Muscadet"]
ca_p = [58, 43, 37, 29, 18]
bars = ax2.barh(produits, ca_p,
                color=[PALETTE[0], PALETTE[2], PALETTE[3], PALETTE[5], LIGHT],
                height=0.55, edgecolor="none")
ax2.set_xlabel("CA (k€)", color=GRAY, fontsize=9)
ax2.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_color(LIGHT)
ax2.set_title("Top 5 produits", fontsize=10, color="#4A4A6A", pad=8)
for bar, val in zip(bars, ca_p):
    ax2.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
             f"{val}k€", va="center", color="#3A3A5C", fontsize=8, fontweight="bold")
save(fig, "ecommerce-python")


# ── 5. Power BI Dashboard ────────────────────────────────────────────────────
C = PALETTE[4]
fig = plt.figure(figsize=(9, 5), facecolor="white")
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.38,
                       left=0.06, right=0.97, top=0.84, bottom=0.1)
fig.suptitle("Dashboard Power BI — Indicateurs Sanitoral", fontsize=12,
             fontweight="bold", color="#3A3A5C", y=0.97)

kpis = [
    ("Score santé", "87.3", "/ 100", PALETTE[2]),
    ("Collaborateurs", "1 248", "actifs", PALETTE[4]),
    ("Absentéisme", "3.2%", "↓ vs N-1", PALETTE[6]),
]
for i, (label, val, sub, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(mpatches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03",
                                          facecolor="white", edgecolor=color,
                                          linewidth=1.5, transform=ax.transAxes, clip_on=False))
    ax.add_patch(mpatches.FancyBboxPatch((0, 0.82), 1, 0.18,
                                          boxstyle="round,pad=0.02",
                                          facecolor=color, alpha=0.18, linewidth=0))
    ax.text(0.5, 0.9, label, ha="center", va="center", color=color,
            fontsize=8, fontweight="bold")
    ax.text(0.5, 0.52, val, ha="center", va="center", color="#3A3A5C",
            fontsize=20, fontweight="800")
    ax.text(0.5, 0.2, sub, ha="center", va="center", color=GRAY, fontsize=8.5)

ax_bar = fig.add_subplot(gs[1, :2])
services = ["Commercial", "RH", "IT", "Finance", "Prod.", "Logistique"]
scores = [93, 91, 88, 85, 82, 79]
colors_b = [PALETTE[1] if s >= 88 else PALETTE[4] if s >= 83 else LIGHT for s in scores]
ax_bar.barh(services, scores, color=colors_b, height=0.5, edgecolor="none")
ax_bar.set_xlim(65, 100)
ax_bar.axvline(87.3, color=PALETTE[6], linestyle="--", linewidth=1.2, alpha=0.7)
ax_bar.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax_bar.spines["left"].set_visible(False)
ax_bar.spines["bottom"].set_color(LIGHT)
ax_bar.set_xlabel("Score", color=GRAY, fontsize=9)

ax_line = fig.add_subplot(gs[1, 2])
mois = ["J", "F", "M", "A", "M", "J"]
evol = [85.0, 85.8, 84.2, 87.5, 86.9, 87.3]
ax_line.plot(mois, evol, color=C, linewidth=2.5, marker="o", markersize=6,
             markerfacecolor=WHITE, markeredgecolor=C, markeredgewidth=2)
ax_line.fill_between(range(len(mois)), evol, 82, alpha=0.1, color=C)
ax_line.set_ylim(80, 92)
ax_line.tick_params(labelcolor="#4A4A6A", labelsize=8)
ax_line.set_xticks(range(len(mois)))
ax_line.set_xticklabels(mois)
ax_line.spines["left"].set_color(LIGHT)
ax_line.spines["bottom"].set_color(LIGHT)
save(fig, "powerbi-dashboard")


# ── 6. Socio-démographie dbt ─────────────────────────────────────────────────
C = PALETTE[5]
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Analyse socio-démographique — OpenClassrooms", fontsize=12,
             fontweight="bold", color="#3A3A5C", y=0.97)

tranches = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
oc = [18, 35, 24, 14, 7, 2]
nat = [12, 18, 20, 22, 16, 12]
x = np.arange(len(tranches))
w = 0.35
ax = axes[0]
ax.bar(x - w / 2, oc, w, label="OpenClassrooms", color=C, alpha=0.9, edgecolor="none")
ax.bar(x + w / 2, nat, w, label="Marché national", color=LIGHT, alpha=0.9, edgecolor=C, linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(tranches, fontsize=8.5, color="#4A4A6A")
ax.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax.spines["left"].set_color(LIGHT)
ax.spines["bottom"].set_color(LIGHT)
ax.legend(fontsize=8, framealpha=0.8)
ax.set_ylabel("Part (%)", color=GRAY, fontsize=9)
ax.set_title("Pyramide des âges", fontsize=10, color="#4A4A6A", pad=8)

ax2 = axes[1]
niveaux = ["Bac", "Bac+2", "Bac+3", "Bac+5", "Doctorat"]
parts2 = [12, 22, 30, 28, 8]
colors_n = [PALETTE[1], PALETTE[2], C, PALETTE[5], PALETTE[6]]
wedges, texts, autotexts = ax2.pie(
    parts2, labels=niveaux, colors=colors_n, autopct="%1.0f%%", startangle=90,
    textprops={"fontsize": 8, "color": "#4A4A6A"},
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
for at in autotexts:
    at.set_fontweight("bold")
    at.set_color("#3A3A5C")
ax2.set_title("Niveau d'étude", fontsize=10, color="#4A4A6A", pad=8)
ax2.set_facecolor("white")
save(fig, "socio-demo-dbt")


# ── 7. E-commerce Lapage ─────────────────────────────────────────────────────
C = PALETTE[6]
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Analyse e-commerce Lapage — Segmentation clients", fontsize=12,
             fontweight="bold", color="#3A3A5C", y=0.97)

ax = axes[0]
segments = ["Champions", "Fidèles", "Potentiels", "À risque", "Inactifs"]
counts = [312, 548, 421, 287, 182]
colors_seg = [PALETTE[1], PALETTE[3], C, PALETTE[5], LIGHT]
bars = ax.barh(segments, counts, color=colors_seg, height=0.55, edgecolor="none")
ax.set_xlabel("Nb clients", color=GRAY, fontsize=9)
ax.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(LIGHT)
ax.set_title("Segmentation RFM", fontsize=10, color="#4A4A6A", pad=8)
for bar, val in zip(bars, counts):
    ax.text(val + 4, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", color="#3A3A5C", fontsize=8, fontweight="bold")

ax2 = axes[1]
mois2 = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû"]
ca2 = [42, 38, 51, 47, 63, 58, 71, 65]
ca2b = [39, 41, 44, 49, 52, 61, 58, 67]
ax2.plot(mois2, ca2, color=PALETTE[2], linewidth=2.2, marker="o", markersize=5,
         markerfacecolor=WHITE, markeredgecolor=PALETTE[2], markeredgewidth=1.8, label="2023")
ax2.plot(mois2, ca2b, color=C, linewidth=2.2, marker="s", markersize=5,
         markerfacecolor=WHITE, markeredgecolor=C, markeredgewidth=1.8, label="2024")
ax2.fill_between(range(len(mois2)), ca2, alpha=0.07, color=PALETTE[2])
ax2.fill_between(range(len(mois2)), ca2b, alpha=0.07, color=C)
ax2.set_xticks(range(len(mois2)))
ax2.set_xticklabels(mois2, fontsize=8)
ax2.tick_params(labelcolor="#4A4A6A", labelsize=8.5)
ax2.spines["left"].set_color(LIGHT)
ax2.spines["bottom"].set_color(LIGHT)
ax2.set_ylabel("CA (k€)", color=GRAY, fontsize=9)
ax2.legend(fontsize=8, framealpha=0.8)
ax2.set_title("Évolution du CA", fontsize=10, color="#4A4A6A", pad=8)
save(fig, "ecommerce-lapage")


print("\nTous les thumbnails générés.")
