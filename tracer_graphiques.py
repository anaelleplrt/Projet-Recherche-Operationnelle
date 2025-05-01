import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from matplotlib.ticker import LogFormatter, ScalarFormatter

valeurs_n = [10, 20, 40, 100, 200, 400, 1000, 4000, 10000]

donnees = {
    "FF": {"n": [], "temps": [], "couleur": "blue", "titre": "Ford-Fulkerson"},
    "PR": {"n": [], "temps": [], "couleur": "orange", "titre": "Push-Relabel"},
    "MIN": {"n": [], "temps": [], "couleur": "green", "titre": "Flot à coût min"}
}

for n in valeurs_n:
    fichier = f"resultats_n{n}.csv"
    if not os.path.exists(fichier):
        print(f"⚠️ Fichier {fichier} introuvable.")
        continue

    df = pd.read_csv(fichier)
    donnees["FF"]["n"] += [n] * len(df)
    donnees["FF"]["temps"] += list(df["t_ff"])

    donnees["PR"]["n"] += [n] * len(df)
    donnees["PR"]["temps"] += list(df["t_pr"])

    donnees["MIN"]["n"] += [n] * len(df)
    donnees["MIN"]["temps"] += list(df["t_min"])

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
    plt.savefig(f"nuage_{code}.png", dpi=300)
    plt.close()
    print(f"✅ Graphe nuage_{code}.png sauvegardé")
