import os
from contextlib import redirect_stdout
from fonctions import (
    lire_graphe,
    get_noms_sommets,
    afficher_matrice,
    executer_ford_fulkerson,
    executer_push_relabel,
    est_flot_a_cout_min,
    executer_flot_min_cout 
)

GROUPE = "G2"
DOSSIER_BASE = "traces-exécutions"
os.makedirs(DOSSIER_BASE, exist_ok=True)

def generer_trace(graphe_num):
    chemin = f"graphes-tests/graphe{graphe_num}.txt"
    n, capacites, couts = lire_graphe(chemin)
    noms = get_noms_sommets(n)

    dossier_graphe = os.path.join(DOSSIER_BASE, f"graphe{graphe_num}")
    os.makedirs(dossier_graphe, exist_ok=True)


    # === Flot à coût maximal (graphe 1 à 5)
    if not est_flot_a_cout_min(graphe_num):
        # === Ford-Fulkerson ===
        nom_fichier_ff = os.path.join(dossier_graphe, f"{GROUPE}-trace{graphe_num}-FF.txt")
        with open(nom_fichier_ff, "w", encoding="utf-8") as f:
            with redirect_stdout(f):
                print(f"🔁 Graphe {graphe_num} — Ford-Fulkerson")
                afficher_matrice("Matrice des capacités", capacites, noms)
                executer_ford_fulkerson(capacites, noms)

        # === Push-Relabel ===
        nom_fichier_pr = os.path.join(dossier_graphe, f"{GROUPE}-trace{graphe_num}-PR.txt")
        with open(nom_fichier_pr, "w", encoding="utf-8") as f:
            with redirect_stdout(f):
                print(f"🔁 Graphe {graphe_num} — Push-Relabel")
                afficher_matrice("Matrice des capacités", capacites, noms)
                executer_push_relabel(capacites, noms)

    # === Flot à coût minimal (graphe 6 à 10)
    if est_flot_a_cout_min(graphe_num):
        nom_fichier_min = os.path.join(dossier_graphe, f"{GROUPE}-trace{graphe_num}-MIN.txt")
        with open(nom_fichier_min, "w", encoding="utf-8") as f:
            with redirect_stdout(f):
                print(f"🔁 Graphe {graphe_num} — Flot à coût minimal")
                afficher_matrice("Matrice des capacités", capacites, noms)
                afficher_matrice("Matrice des coûts", couts, noms)

                source = 0
                puits = len(capacites) - 1
                sortie_s = sum(capacites[source])
                entree_t = sum(capacites[i][puits] for i in range(len(capacites)))
                val_flot = min(sortie_s, entree_t)

                print(f"\nCapacité maximale sortante de s : {sortie_s}")
                print(f"Capacité maximale entrante dans t : {entree_t}")
                print(f"✅ Choix automatique de la valeur de flot : {val_flot} (valeur maximale possible)")
                executer_flot_min_cout(capacites, couts, noms, val_flot)



def lancer_generation():
    print("\n 📦 Génération des fichiers de traces pour l’équipe", GROUPE)
    for i in range(1, 11):
        generer_trace(i)
    print(f"\n ✅ Traces enregistrées dans le dossier '{DOSSIER_BASE}'\n ")

if __name__ == "__main__":
    lancer_generation()
