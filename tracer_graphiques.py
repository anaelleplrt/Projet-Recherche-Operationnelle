import matplotlib.pyplot as plt
import pandas as pd
import os

valeurs_n = [10, 20, 40, 100, 400, 1000, 4000, 10000]

# Initialiser les structures pour chaque algo
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

# Tracer un graphe par algorithme
for code, d in donnees.items():
    plt.figure(figsize=(10, 5))
    plt.title(f"Nuage de points – {d['titre']} en fonction de n")
    plt.xlabel("n (taille du graphe)")
    plt.ylabel("Temps (secondes)")
    plt.xscale("log")
    plt.grid(True)

    plt.scatter(d["n"], d["temps"], color=d["couleur"], s=12, alpha=0.6)

    plt.tight_layout()
    plt.savefig(f"nuage_{code}.png", dpi=300)
    plt.close()
    print(f"✅ Graphe nuage_{code}.png sauvegardé")
