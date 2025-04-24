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

                    source = 0

                    _,_, etapes = bellman_ford(capacites, couts, source)
                    afficher_table_bellman_detaillee(noms, etapes)

                    sortie_s = sum(capacites[0])
                    entree_t = sum(capacites[i][n-1] for i in range(n))
                    valeur_max_possible = min(sortie_s, entree_t)

                    print(f"\nCapacité maximale sortante de s : {sortie_s}")
                    print(f"Capacité maximale entrante dans t : {entree_t}")
                    print(f"Vous pouvez envoyer au maximum : {valeur_max_possible}")

                    val_flot = int(input("\nChoisissez la valeur de flot à envoyer : "))

                    if val_flot <= 0:
                        print("❌ Valeur non valide. Elle doit être strictement positive.")
                    elif val_flot > valeur_max_possible:
                        print("❌ Valeur trop élevée. Elle dépasse ce que le réseau peut supporter.")
                    else:
                        executer_flot_min_cout(capacites, couts, noms, val_flot)
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
