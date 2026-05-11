import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
from pathlib import Path

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

BASE = Path("/home/elicesjo/GitHub/elicesjo.github.io/projets")
W, H = 8, 5


def save(fig, slug):
    out = BASE / slug / "thumbnail.png"
    fig.savefig(out, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  {out.name} → {slug}/")


# ── 1. SQL Requêtes ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(W, H), facecolor="#1A1A2E")
fig.subplots_adjust(wspace=0.35, left=0.08, right=0.97, top=0.88, bottom=0.12)
fig.suptitle("Analyse des ventes — Marchand de vin", color="white", fontsize=13, fontweight="bold")

vins = ["Bordeaux", "Bourgogne", "Alsace", "Rhône", "Loire"]
ventes = [42000, 35000, 28000, 51000, 19000]
colors = ["#E74C3C", "#8E44AD", "#2ECC71", "#E67E22", "#3498DB"]

ax = axes[0]
ax.set_facecolor("#16213E")
bars = ax.barh(vins, ventes, color=colors, height=0.6, edgecolor="none")
ax.set_xlabel("CA (€)", color="#AAAAAA", fontsize=9)
ax.tick_params(colors="#CCCCCC", labelsize=8)
ax.spines["bottom"].set_color("#444")
ax.spines["left"].set_color("#444")
for bar, val in zip(bars, ventes):
    ax.text(val + 800, bar.get_y() + bar.get_height() / 2,
            f"{val/1000:.0f}k€", va="center", color="white", fontsize=8)

ax2 = axes[1]
ax2.set_facecolor("#16213E")
mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun"]
ca = [18, 22, 31, 27, 35, 29]
ax2.plot(mois, ca, color="#E67E22", linewidth=2.5, marker="o", markersize=6, markerfacecolor="white")
ax2.fill_between(range(len(mois)), ca, alpha=0.15, color="#E67E22")
ax2.set_ylabel("CA (k€)", color="#AAAAAA", fontsize=9)
ax2.tick_params(colors="#CCCCCC", labelsize=8)
ax2.spines["bottom"].set_color("#444")
ax2.spines["left"].set_color("#444")
ax2.set_xticks(range(len(mois)))
ax2.set_xticklabels(mois)

save(fig, "sql-requetes")


# ── 2. Santé publique ────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(W, H), facecolor="#0D1B2A")
fig.subplots_adjust(wspace=0.4, left=0.08, right=0.97, top=0.88, bottom=0.15)
fig.suptitle("Sous-nutrition mondiale — Analyse FAO", color="white", fontsize=13, fontweight="bold")

regions = ["Afrique\nsub-sah.", "Asie du\nSud", "Asie de\nl'Est", "Am.\nLatine", "Océanie"]
taux = [23.4, 15.1, 8.3, 6.5, 4.2]
pop = [420, 320, 180, 95, 12]

ax = axes[0]
ax.set_facecolor("#0A1628")
scatter_colors = ["#E74C3C", "#E67E22", "#F1C40F", "#2ECC71", "#3498DB"]
sc = ax.scatter(taux, pop, s=[t * 40 for t in taux], c=scatter_colors, alpha=0.85, edgecolors="white", linewidth=0.5)
for i, r in enumerate(regions):
    ax.annotate(r, (taux[i], pop[i]), textcoords="offset points", xytext=(6, 4),
                color="#CCCCCC", fontsize=7.5)
ax.set_xlabel("Taux sous-nutrition (%)", color="#AAAAAA", fontsize=9)
ax.set_ylabel("Pop. touchée (M)", color="#AAAAAA", fontsize=9)
ax.tick_params(colors="#CCCCCC", labelsize=8)
ax.spines["bottom"].set_color("#444")
ax.spines["left"].set_color("#444")

ax2 = axes[1]
ax2.set_facecolor("#0A1628")
items = ["Céréales", "Légumineuses", "Fruits/Légumes", "Viande/Poisson", "Produits\nlaitiers"]
dispo = [2850, 890, 640, 310, 180]
besoins = [2100, 700, 800, 400, 250]
x = np.arange(len(items))
w = 0.35
ax2.bar(x - w/2, dispo, w, label="Disponible", color="#2ECC71", alpha=0.85)
ax2.bar(x + w/2, besoins, w, label="Besoin min.", color="#E74C3C", alpha=0.85)
ax2.set_xticks(x)
ax2.set_xticklabels(items, fontsize=7, color="#CCCCCC")
ax2.tick_params(colors="#CCCCCC", labelsize=8)
ax2.spines["bottom"].set_color("#444")
ax2.spines["left"].set_color("#444")
ax2.legend(fontsize=8, facecolor="#0A1628", labelcolor="white", framealpha=0.5)
ax2.set_ylabel("kcal/pers./jour", color="#AAAAAA", fontsize=9)

save(fig, "sante-publique")


# ── 3. BDD Immobilier ────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(W, H), facecolor="#1C1C1E")
fig.subplots_adjust(wspace=0.4, left=0.1, right=0.97, top=0.88, bottom=0.15)
fig.suptitle("Base de données immobilière — Marché DVF", color="white", fontsize=13, fontweight="bold")

villes = ["Paris", "Lyon", "Bordeaux", "Marseille", "Nantes"]
prix_m2 = [10200, 5100, 4800, 3600, 4200]

ax = axes[0]
ax.set_facecolor("#111111")
bar_colors = ["#E74C3C" if p > 6000 else "#E67E22" if p > 4500 else "#2ECC71" for p in prix_m2]
bars = ax.bar(villes, prix_m2, color=bar_colors, edgecolor="none", width=0.6)
ax.set_ylabel("Prix moyen (€/m²)", color="#AAAAAA", fontsize=9)
ax.tick_params(colors="#CCCCCC", labelsize=8)
ax.spines["bottom"].set_color("#444")
ax.spines["left"].set_color("#444")
for bar, val in zip(bars, prix_m2):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 100, f"{val:,}€",
            ha="center", color="white", fontsize=7.5, fontweight="bold")

ax2 = axes[1]
ax2.set_facecolor("#111111")
types = ["Appartement\nT1-T2", "Appartement\nT3-T4", "Maison\npetite", "Maison\ngrande"]
volumes = [38, 29, 21, 12]
colors_pie = ["#3498DB", "#2ECC71", "#E67E22", "#9B59B6"]
wedges, texts, autotexts = ax2.pie(volumes, labels=types, colors=colors_pie,
                                    autopct="%1.0f%%", startangle=90,
                                    textprops={"color": "#CCCCCC", "fontsize": 8},
                                    wedgeprops={"edgecolor": "#1C1C1E", "linewidth": 2})
for at in autotexts:
    at.set_color("white")
    at.set_fontweight("bold")

save(fig, "immo-sql")


# ── 4. E-commerce Python ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(W, H), facecolor="#0F2027")
fig.subplots_adjust(wspace=0.4, left=0.1, right=0.97, top=0.88, bottom=0.15)
fig.suptitle("Optimisation données e-commerce — Boutique vin", color="white", fontsize=13, fontweight="bold")

ax = axes[0]
ax.set_facecolor("#0A1628")
categories = ["Complet", "Manquant\npartiel", "Doublon", "Incohérent"]
avant = [1240, 380, 145, 92]
apres = [1724, 18, 0, 0]
x = np.arange(len(categories))
w = 0.35
ax.bar(x - w/2, avant, w, label="Avant", color="#E74C3C", alpha=0.85)
ax.bar(x + w/2, apres, w, label="Après", color="#2ECC71", alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8, color="#CCCCCC")
ax.tick_params(colors="#CCCCCC", labelsize=8)
ax.spines["bottom"].set_color("#444")
ax.spines["left"].set_color("#444")
ax.legend(fontsize=8, facecolor="#0A1628", labelcolor="white", framealpha=0.5)
ax.set_ylabel("Nb lignes", color="#AAAAAA", fontsize=9)
ax.set_title("Audit qualité données", color="#AAAAAA", fontsize=9)

ax2 = axes[1]
ax2.set_facecolor("#0A1628")
produits = ["Bordeaux\nRouge", "Champagne", "Sancerre\nBlanc", "Côtes\ndu Rhône", "Muscadet"]
ca_prod = [58, 43, 37, 29, 18]
colors_h = ["#E74C3C", "#F1C40F", "#3498DB", "#E67E22", "#2ECC71"]
bars = ax2.barh(produits, ca_prod, color=colors_h, height=0.55, edgecolor="none")
ax2.set_xlabel("CA (k€)", color="#AAAAAA", fontsize=9)
ax2.tick_params(colors="#CCCCCC", labelsize=8)
ax2.spines["bottom"].set_color("#444")
ax2.spines["left"].set_color("#444")
ax2.set_title("Top produits", color="#AAAAAA", fontsize=9)
for bar, val in zip(bars, ca_prod):
    ax2.text(val + 0.8, bar.get_y() + bar.get_height() / 2,
             f"{val}k€", va="center", color="white", fontsize=8)

save(fig, "ecommerce-python")


# ── 5. Power BI Dashboard ────────────────────────────────────────────────────
fig = plt.figure(figsize=(W, H), facecolor="#1E1E2E")
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35,
                       left=0.06, right=0.97, top=0.88, bottom=0.1)
fig.suptitle("Dashboard Power BI — Indicateurs Sanitoral", color="white", fontsize=13, fontweight="bold")

kpis = [
    ("Score moyen", "87.3", "/100", "#2ECC71"),
    ("Collaborateurs", "1 248", "actifs", "#3498DB"),
    ("Taux absentéisme", "3.2%", "↓ vs N-1", "#E67E22"),
]
for i, (label, val, sub, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor("#2A2A3E")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(mpatches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                          boxstyle="round,pad=0.05",
                                          facecolor=color, alpha=0.15, linewidth=0))
    ax.add_patch(mpatches.FancyBboxPatch((0.05, 0.78), 0.9, 0.17,
                                          boxstyle="round,pad=0.02",
                                          facecolor=color, alpha=0.6, linewidth=0))
    ax.text(0.5, 0.86, label, ha="center", va="center", color="white", fontsize=7.5, fontweight="bold")
    ax.text(0.5, 0.5, val, ha="center", va="center", color=color, fontsize=18, fontweight="bold")
    ax.text(0.5, 0.18, sub, ha="center", va="center", color="#AAAAAA", fontsize=8)

ax_bar = fig.add_subplot(gs[1, :2])
ax_bar.set_facecolor("#2A2A3E")
services = ["RH", "Finance", "IT", "Prod.", "Commercial", "Logistique"]
scores = [91, 85, 88, 79, 93, 82]
colors_b = ["#2ECC71" if s >= 88 else "#E67E22" if s >= 82 else "#E74C3C" for s in scores]
ax_bar.barh(services, scores, color=colors_b, height=0.55, edgecolor="none")
ax_bar.set_xlim(60, 100)
ax_bar.axvline(87.3, color="white", linestyle="--", linewidth=1, alpha=0.5)
ax_bar.tick_params(colors="#CCCCCC", labelsize=8)
ax_bar.spines["bottom"].set_color("#444")
ax_bar.spines["left"].set_color("#444")
ax_bar.set_xlabel("Score santé", color="#AAAAAA", fontsize=8)

ax_line = fig.add_subplot(gs[1, 2])
ax_line.set_facecolor("#2A2A3E")
mois = ["J", "F", "M", "A", "M", "J"]
evol = [85, 86, 84, 88, 87, 87.3]
ax_line.plot(mois, evol, color="#2ECC71", linewidth=2.5, marker="o", markersize=5)
ax_line.fill_between(range(len(mois)), evol, 80, alpha=0.15, color="#2ECC71")
ax_line.set_ylim(78, 95)
ax_line.tick_params(colors="#CCCCCC", labelsize=7)
ax_line.spines["bottom"].set_color("#444")
ax_line.spines["left"].set_color("#444")
ax_line.set_xticks(range(len(mois)))
ax_line.set_xticklabels(mois)

save(fig, "powerbi-dashboard")

print("Tous les thumbnails générés.")
