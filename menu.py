from fonctions import *
from time import perf_counter

def menu_principal():
    print("=== Projet de Recherche Opérationnelle ===")

    while True:
        choix = input("\n→ Choisissez un numéro de graphe (1 à 10), 'test' pour un graphe aléatoire, ou 'q' pour quitter : ")
        
        if choix.lower() == 'q':
            print("Fin du programme.")
            break

        elif choix.lower() == 'test':
            try:
                n = int(input("→ Taille du graphe aléatoire (ex: 10, 50, 100) : "))
                if n < 2:
                    print("❌ Le graphe doit contenir au moins 2 sommets.")
                else:
                    capacites, couts = generer_graphe_aleatoire(n)
                    noms = get_noms_sommets(n)

                    print("\n✔ Graphe aléatoire généré.")
                    afficher_matrice("Matrice des capacités", capacites, noms)
                    afficher_matrice("Matrice des coûts", couts, noms)

                    sortie_s = sum(capacites[0])
                    entree_t = sum(capacites[i][n-1] for i in range(n))
                    val_flot = min(sortie_s, entree_t) // 2

                    t_ff, t_pr, t_min, flot_ff, flot_pr, flot_min = mesurer_temps_execution_algos(capacites, couts, noms, val_flot)

                    print(f"\n📦 Flot envoyé :")
                    print(f"Ford-Fulkerson   : {flot_ff}")
                    print(f"Push-Relabel     : {flot_pr}")
                    print(f"Flot à coût min  : {flot_min} (sur {val_flot} demandé)")

                    print(f"\n⏱️ Temps d’exécution :")
                    print(f"Ford-Fulkerson   : {t_ff:.4f} s")
                    print(f"Push-Relabel     : {t_pr:.4f} s")
                    print(f"Flot à coût min  : {t_min:.4f} s")


            except ValueError:
                print("❌ Veuillez entrer un entier valide.")

        else:
            try:
                numero = int(choix)
                if 1 <= numero <= 10:
                    traiter_graphe(numero)
                else:
                    print("Numéro invalide. Choisissez entre 1 et 10.")

            except ValueError:
                print("Veuillez entrer un nombre ou 'q' pour quitter.")
