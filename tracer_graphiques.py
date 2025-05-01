import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from matplotlib.ticker import LogFormatter, ScalarFormatter

valeurs_n = [10, 20, 40, 100, 200, 400, 1000]

donnees = {
    "FF": {"n": [], "temps": [], "couleur": "blue", "titre": "Ford-Fulkerson"},
    "PR": {"n": [], "temps": [], "couleur": "orange", "titre": "Pousser-Reétiqueter"},
    "MIN": {"n": [], "temps": [], "couleur": "green", "titre": "Flot à coût min"}
}

temps_max = {"FF": [], "PR": [], "MIN": []}  # Pour stocker les enveloppes
ratios_ff_pr = []  # Pour stocker les ratios FF/PR

# Chargement des données et calcul des temps max
for n in valeurs_n:
    fichier = f"resultats_n{n}.csv"
    if not os.path.exists(fichier):
        print(f"⚠️ Fichier {fichier} introuvable.")
        continue

    df = pd.read_csv(fichier)

    ff_temps = list(df["t_ff"])
    pr_temps = list(df["t_pr"])
    min_temps = list(df["t_min"])

    donnees["FF"]["n"] += [n] * len(ff_temps)
    donnees["FF"]["temps"] += ff_temps
    donnees["PR"]["n"] += [n] * len(pr_temps)
    donnees["PR"]["temps"] += pr_temps
    donnees["MIN"]["n"] += [n] * len(min_temps)
    donnees["MIN"]["temps"] += min_temps

    # Enveloppes supérieures
    temps_max["FF"].append(max(ff_temps))
    temps_max["PR"].append(max(pr_temps))
    temps_max["MIN"].append(max(min_temps))

    # Ratio FF/PR
    try:
        ratio = max(ff_temps) / max(pr_temps)
    except ZeroDivisionError:
        ratio = float("inf")
    ratios_ff_pr.append(ratio)

# Nuages de points pour chaque algo
for code, d in donnees.items():
    plt.figure(figsize=(10, 6))
    plt.title(f"Nuage de points – {d['titre']} en fonction de n", fontsize=14)
    plt.xlabel("n (taille du graphe)", fontsize=12)
    plt.ylabel("Temps d'exécution (secondes)", fontsize=12)
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.xscale("log")
    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.xticks(valeurs_n, labels=[str(n) for n in valeurs_n])
    plt.scatter(d["n"], d["temps"], color=d["couleur"], s=14, alpha=0.6, edgecolors='k', linewidths=0.3)
    plt.tight_layout()
    plt.savefig(f"./graphiques/nuage_{code}.png", dpi=300)
    plt.close()
    print(f"✅ Graphe nuage_{code}.png sauvegardé")

# Graphes des enveloppes supérieures
for code in ["FF", "PR", "MIN"]:
    plt.figure(figsize=(10, 6))
    plt.xlabel("n (taille du graphe)", fontsize=12)
    plt.ylabel("Temps max (secondes)", fontsize=12)
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.xscale("log")
    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.xticks(valeurs_n, labels=[str(n) for n in valeurs_n])
    plt.title(f"Enveloppe supérieure – {donnees[code]['titre']}", fontsize=14)
    plt.plot(valeurs_n, temps_max[code], color=donnees[code]["couleur"], marker='o', linestyle='-')
    plt.tight_layout()
    plt.savefig(f"./graphiques/enveloppe_{code}.png", dpi=300)
    plt.close()
    print(f"✅ Graphe enveloppe_{code}.png sauvegardé")

# Graphe des ratios FF/PR
plt.figure(figsize=(10, 6))
plt.title("Ratio des temps max Ford-Fulkerson / Pousser-Réetiqueter", fontsize=14)
plt.plot(valeurs_n, ratios_ff_pr, marker='o', linestyle='-', color='purple')
plt.xscale("log")
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.xticks(valeurs_n, labels=[str(n) for n in valeurs_n])
plt.xlabel("n (taille du graphe)", fontsize=12)
plt.ylabel("Ratio temps max (FF / PR)", fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("./graphiques/ratio_ff_pr.png", dpi=300)
plt.close()
print(f"✅ Graphe ratio_ff_pr.png sauvegardé")


print(temps_max)