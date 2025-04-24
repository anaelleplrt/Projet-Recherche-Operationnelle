from fonctions import *

def menu_principal():
    print("=== Projet de Recherche Opérationnelle ===")

    while True:
        choix = input("\n→ Choisissez un numéro de graphe (1 à 10) ou 'q' pour quitter : ")
        if choix.lower() == 'q':
            print("Fin du programme.")
            break

        try:
            numero = int(choix)
            if 1 <= numero <= 10:
                chemin = f"graphes-tests/graphe{numero}.txt"
                n, capacites, couts = lire_graphe(chemin)
                noms = get_noms_sommets(n)

                print(f"\n✔ Chargement du graphe {numero}")
                afficher_matrice("Matrice des capacités", capacites, noms)

                if est_flot_a_cout_min(numero):
                    afficher_matrice("Matrice des coûts", couts, noms)

                    # Construction du graphe résiduel initial = le graphe de base (aucun flot envoyé)
                    residuel = [row[:] for row in capacites]
                    couts_residuel = [row[:] for row in couts]

                    # Exécution de Bellman-Ford "statique" pour affichage de la table initiale
                    n = len(capacites)
                    distances = [float('inf')] * n
                    parents = [-1] * n
                    distances[0] = 0
                    etapes = []

                    for _ in range(n - 1):
                        new_distances = distances[:]
                        new_parents = parents[:]
                        for u in range(n):
                            for v in range(n):
                                if residuel[u][v] > 0:
                                    if distances[u] + couts_residuel[u][v] < new_distances[v]:
                                        new_distances[v] = distances[u] + couts_residuel[u][v]
                                        new_parents[v] = u
                        etapes.append((new_distances[:], new_parents[:]))
                        if new_distances == distances:
                            break
                        distances = new_distances
                        parents = new_parents

                    afficher_table_bellman_detaillee(noms, etapes)


                    source = 0
                    sortie_s = sum(capacites[source])
                    entree_t = sum(capacites[i][n-1] for i in range(n))
                    valeur_max_possible = min(sortie_s, entree_t)

                    print(f"\nCapacité maximale sortante de s : {sortie_s}")
                    print(f"Capacité maximale entrante dans t : {entree_t}")
                    print(f"Vous pouvez envoyer au maximum : {valeur_max_possible}")

                    while True:
                        try:
                            val_flot = int(input("\nChoisissez la valeur de flot à envoyer : "))
                            if val_flot <= 0:
                                print("❌ Valeur non valide. Elle doit être strictement positive.")
                            elif val_flot > valeur_max_possible:
                                print("❌ Valeur trop élevée. Elle dépasse ce que le réseau peut supporter.")
                            else:
                                executer_flot_min_cout(capacites, couts, noms, val_flot)
                                break
                        except ValueError:
                            print("❌ Veuillez entrer un nombre entier valide.")

                else:
                    print("\nQuel algorithme souhaitez-vous utiliser ?")
                    print("1 - Ford-Fulkerson")
                    print("2 - Push-Relabel")

                    algo = input("Votre choix : ")

                    if algo == "1":
                        executer_ford_fulkerson(capacites, noms)
                    elif  algo == "2" : 
                        executer_push_relabel(capacites, noms)
                    else:
                        print("Choix invalide.")
            else:
                print("Numéro invalide. Choisissez entre 1 et 10.")
        except ValueError:
            print("Veuillez entrer un nombre ou 'q' pour quitter.")
