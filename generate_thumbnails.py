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
    "grid.alpha": 0.3,
    "grid.linewidth": 0.6,
    "figure.facecolor": "white",
    "axes.facecolor": "#F8FAFC",
})

BASE = Path("/home/elicesjo/GitHub/elicesjo.github.io/projets")
ACCENT = "#4F46E5"
GRAY = "#64748B"
LIGHT = "#E2E8F0"


def save(fig, slug):
    out = BASE / slug / "thumbnail.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {slug}/thumbnail.png")


# ── 1. SQL Requêtes ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.38, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Analyse des ventes — Marchand de vin", fontsize=12, fontweight="bold",
             color="#0F172A", x=0.5, y=0.97)

vins = ["Bordeaux", "Bourgogne", "Rhône", "Alsace", "Loire"]
ventes = [51000, 42000, 35000, 28000, 19000]

ax = axes[0]
colors = [ACCENT if i == 0 else LIGHT for i in range(len(vins))]
bars = ax.barh(vins, ventes, color=colors, height=0.55, edgecolor="none")
ax.set_xlabel("CA (€)", color=GRAY, fontsize=9)
ax.tick_params(labelcolor="#334155", labelsize=8.5)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(LIGHT)
for bar, val in zip(bars, ventes):
    ax.text(val + 600, bar.get_y() + bar.get_height() / 2,
            f"{val/1000:.0f}k€", va="center", color="#0F172A", fontsize=8, fontweight="bold")
ax.set_title("CA par région", fontsize=10, color="#334155", pad=8)

ax2 = axes[1]
mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun"]
ca = [18, 22, 31, 27, 35, 29]
ax2.plot(mois, ca, color=ACCENT, linewidth=2.5, marker="o", markersize=7,
         markerfacecolor="white", markeredgecolor=ACCENT, markeredgewidth=2)
ax2.fill_between(range(len(mois)), ca, alpha=0.08, color=ACCENT)
ax2.set_ylabel("CA (k€)", color=GRAY, fontsize=9)
ax2.tick_params(labelcolor="#334155", labelsize=8.5)
ax2.set_xticks(range(len(mois)))
ax2.set_xticklabels(mois)
ax2.spines["left"].set_color(LIGHT)
ax2.spines["bottom"].set_color(LIGHT)
ax2.set_title("Évolution mensuelle", fontsize=10, color="#334155", pad=8)

save(fig, "sql-requetes")


# ── 2. Santé publique ────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Sous-nutrition mondiale — Analyse FAO", fontsize=12, fontweight="bold",
             color="#0F172A", y=0.97)

regions = ["Afrique\nsub-sah.", "Asie\ndu Sud", "Asie\nde l'Est", "Am.\nLatine", "Océanie"]
taux = [23.4, 15.1, 8.3, 6.5, 4.2]
colors_r = ["#EF4444", "#F97316", "#EAB308", "#22C55E", "#3B82F6"]

ax = axes[0]
bars = ax.bar(regions, taux, color=colors_r, edgecolor="none", width=0.6)
ax.set_ylabel("Taux (%)", color=GRAY, fontsize=9)
ax.tick_params(labelcolor="#334155", labelsize=8)
ax.spines["left"].set_color(LIGHT)
ax.spines["bottom"].set_color(LIGHT)
for bar, val in zip(bars, taux):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.4, f"{val}%",
            ha="center", color="#0F172A", fontsize=8, fontweight="bold")
ax.set_title("Taux de sous-nutrition par région", fontsize=10, color="#334155", pad=8)

ax2 = axes[1]
items = ["Céréales", "Légumineuses", "Fruits/Lég.", "Protéines", "Laitiers"]
dispo = [2850, 890, 640, 310, 180]
besoins = [2100, 700, 800, 400, 250]
x = np.arange(len(items))
w = 0.35
ax2.bar(x - w / 2, dispo, w, label="Disponible", color="#22C55E", alpha=0.85, edgecolor="none")
ax2.bar(x + w / 2, besoins, w, label="Besoin min.", color="#EF4444", alpha=0.85, edgecolor="none")
ax2.set_xticks(x)
ax2.set_xticklabels(items, fontsize=7.5, color="#334155")
ax2.tick_params(labelcolor="#334155", labelsize=8)
ax2.spines["left"].set_color(LIGHT)
ax2.spines["bottom"].set_color(LIGHT)
ax2.legend(fontsize=8, framealpha=0.8)
ax2.set_ylabel("kcal/pers./j", color=GRAY, fontsize=9)
ax2.set_title("Disponible vs Besoin", fontsize=10, color="#334155", pad=8)

save(fig, "sante-publique")


# ── 3. BDD Immobilier ────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Base de données immobilière — DVF", fontsize=12, fontweight="bold",
             color="#0F172A", y=0.97)

villes = ["Paris", "Lyon", "Bordeaux", "Nantes", "Marseille"]
prix = [10200, 5100, 4800, 4200, 3600]
colors_v = [ACCENT if p > 6000 else "#818CF8" if p > 4500 else LIGHT for p in prix]

ax = axes[0]
bars = ax.bar(villes, prix, color=colors_v, edgecolor="none", width=0.6)
ax.set_ylabel("Prix moyen (€/m²)", color=GRAY, fontsize=9)
ax.tick_params(labelcolor="#334155", labelsize=8.5)
ax.spines["left"].set_color(LIGHT)
ax.spines["bottom"].set_color(LIGHT)
for bar, val in zip(bars, prix):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 120, f"{val:,}€",
            ha="center", color="#0F172A", fontsize=8, fontweight="bold")
ax.set_title("Prix moyen au m² par ville", fontsize=10, color="#334155", pad=8)

ax2 = axes[1]
types = ["Appart.\nT1-T2", "Appart.\nT3-T4", "Maison\npetite", "Maison\ngrande"]
parts = [38, 29, 21, 12]
colors_p = [ACCENT, "#818CF8", "#A5B4FC", LIGHT]
wedges, texts, autotexts = ax2.pie(
    parts, labels=types, colors=colors_p, autopct="%1.0f%%", startangle=90,
    textprops={"fontsize": 8, "color": "#334155"},
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
for at in autotexts:
    at.set_fontweight("bold")
    at.set_color("#0F172A")
ax2.set_title("Répartition par type de bien", fontsize=10, color="#334155", pad=8)
ax2.set_facecolor("white")

save(fig, "immo-sql")


# ── 4. E-commerce Python ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9, 5), facecolor="white")
fig.subplots_adjust(wspace=0.42, left=0.1, right=0.96, top=0.84, bottom=0.14)
fig.suptitle("Optimisation données e-commerce — Boutique vin", fontsize=12,
             fontweight="bold", color="#0F172A", y=0.97)

ax = axes[0]
categories = ["Complets", "Manquants", "Doublons", "Incohérents"]
avant = [1240, 380, 145, 92]
apres = [1824, 18, 0, 0]
x = np.arange(len(categories))
w = 0.35
ax.bar(x - w / 2, avant, w, label="Avant audit", color="#EF4444", alpha=0.85, edgecolor="none")
ax.bar(x + w / 2, apres, w, label="Après nettoyage", color="#22C55E", alpha=0.85, edgecolor="none")
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8.5, color="#334155")
ax.tick_params(labelcolor="#334155", labelsize=8.5)
ax.spines["left"].set_color(LIGHT)
ax.spines["bottom"].set_color(LIGHT)
ax.legend(fontsize=8.5, framealpha=0.8)
ax.set_ylabel("Nb lignes", color=GRAY, fontsize=9)
ax.set_title("Audit qualité des données", fontsize=10, color="#334155", pad=8)

ax2 = axes[1]
produits = ["Bordeaux\nRouge", "Champagne", "Sancerre", "Côtes Rhône", "Muscadet"]
ca_p = [58, 43, 37, 29, 18]
bars = ax2.barh(produits, ca_p,
                color=[ACCENT, "#818CF8", "#A5B4FC", LIGHT, LIGHT],
                height=0.55, edgecolor="none")
ax2.set_xlabel("CA (k€)", color=GRAY, fontsize=9)
ax2.tick_params(labelcolor="#334155", labelsize=8.5)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_color(LIGHT)
ax2.set_title("Top 5 produits", fontsize=10, color="#334155", pad=8)
for bar, val in zip(bars, ca_p):
    ax2.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
             f"{val}k€", va="center", color="#0F172A", fontsize=8, fontweight="bold")

save(fig, "ecommerce-python")


# ── 5. Power BI Dashboard ────────────────────────────────────────────────────
fig = plt.figure(figsize=(9, 5), facecolor="white")
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.38,
                       left=0.06, right=0.97, top=0.84, bottom=0.1)
fig.suptitle("Dashboard Power BI — Indicateurs Sanitoral", fontsize=12,
             fontweight="bold", color="#0F172A", y=0.97)

kpis = [
    ("Score santé", "87.3", "/ 100", "#22C55E"),
    ("Collaborateurs", "1 248", "actifs", ACCENT),
    ("Absentéisme", "3.2%", "↓ vs N-1", "#F97316"),
]
for i, (label, val, sub, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(mpatches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03",
                                          facecolor="white", edgecolor=color,
                                          linewidth=1.5, transform=ax.transAxes,
                                          clip_on=False))
    ax.add_patch(mpatches.FancyBboxPatch((0, 0.82), 1, 0.18,
                                          boxstyle="round,pad=0.02",
                                          facecolor=color, alpha=0.15, linewidth=0))
    ax.text(0.5, 0.9, label, ha="center", va="center", color=color,
            fontsize=8, fontweight="bold")
    ax.text(0.5, 0.52, val, ha="center", va="center", color="#0F172A",
            fontsize=20, fontweight="800")
    ax.text(0.5, 0.2, sub, ha="center", va="center", color=GRAY, fontsize=8.5)

ax_bar = fig.add_subplot(gs[1, :2])
ax_bar.set_facecolor("#F8FAFC")
services = ["Commercial", "RH", "IT", "Finance", "Prod.", "Logistique"]
scores = [93, 91, 88, 85, 82, 79]
colors_b = [ACCENT if s >= 88 else "#818CF8" if s >= 83 else LIGHT for s in scores]
ax_bar.barh(services, scores, color=colors_b, height=0.5, edgecolor="none")
ax_bar.set_xlim(65, 100)
ax_bar.axvline(87.3, color="#EF4444", linestyle="--", linewidth=1.2, alpha=0.7)
ax_bar.tick_params(labelcolor="#334155", labelsize=8.5)
ax_bar.spines["left"].set_visible(False)
ax_bar.spines["bottom"].set_color(LIGHT)
ax_bar.set_xlabel("Score", color=GRAY, fontsize=9)

ax_line = fig.add_subplot(gs[1, 2])
ax_line.set_facecolor("#F8FAFC")
mois = ["J", "F", "M", "A", "M", "J"]
evol = [85.0, 85.8, 84.2, 87.5, 86.9, 87.3]
ax_line.plot(mois, evol, color="#22C55E", linewidth=2.5, marker="o", markersize=6,
             markerfacecolor="white", markeredgecolor="#22C55E", markeredgewidth=2)
ax_line.fill_between(range(len(mois)), evol, 82, alpha=0.1, color="#22C55E")
ax_line.set_ylim(80, 92)
ax_line.tick_params(labelcolor="#334155", labelsize=8)
ax_line.set_xticks(range(len(mois)))
ax_line.set_xticklabels(mois)
ax_line.spines["left"].set_color(LIGHT)
ax_line.spines["bottom"].set_color(LIGHT)

save(fig, "powerbi-dashboard")

print("\nTous les thumbnails générés.")
