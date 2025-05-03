from fonctions import generer_graphe_aleatoire, get_noms_sommets, mesurer_temps_execution_algos
import csv
from tabulate import tabulate

def tester_n_valeurs(n):
    print(f"\n Lancement des 100 tests pour n = {n}")
    fichier_csv = f"resultats_n{n}.csv"

    with open(fichier_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "t_ff", "t_pr", "t_min"])

        for i in range(1, 101):
            print(f"→ Test {i}/100 en cours...")

            capacites, couts = generer_graphe_aleatoire(n)
            noms = get_noms_sommets(n)

            sortie_s = sum(capacites[0])
            entree_t = sum(capacites[i][n-1] for i in range(n))
            val_flot = min(sortie_s, entree_t) // 2

            t_ff, t_pr, t_min, _, _, _ = mesurer_temps_execution_algos(capacites, couts, noms, val_flot, afficher=False)
            writer.writerow([i, t_ff, t_pr, t_min])

    print(f"\n✅ Resultats enregistrés dans {fichier_csv}")


if __name__ == "__main__":
    try:
        n = int(input("Quelle taille de graphe veux-tu tester ? (ex: 10, 50, 100, ...) : "))
        if n < 2:
            print("❌ La taille doit être ≥ 2")
        else:
            tester_n_valeurs(n)
    except ValueError:
        print("❌ Veuillez entrer un nombre entier valide.")


