from fonctions import (
    lire_graphe,
    afficher_matrice,
    est_flot_a_cout_min,
    executer_ford_fulkerson,
    executer_push_relabel,
    get_noms_sommets,
    executer_flot_min_cout
)

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
                n, capacites, couts = lire_graphe(chemin) # capacites et couts sont des matrices
                noms_sommets = get_noms_sommets(n)

                print(f"\n✔ Chargement du graphe {numero}")
                #print(noms_sommets, capacites,  couts)
                afficher_matrice("Matrice des capacités", capacites, noms_sommets)

                if est_flot_a_cout_min(numero):
                    afficher_matrice("Matrice des coûts", couts, noms_sommets)

                    lancer = input("\nVoulez-vous lancer la résolution du flot à coût minimal ? (o/n) : ").lower() # est ce qu'on pourrait pas aussi lancer flot max ?
                    if lancer == 'o':
                        executer_flot_min_cout(capacites, couts, noms_sommets)
                    else:
                        print("Résolution annulée.")
                else:
                    print("\nQuel algorithme souhaitez-vous utiliser ?")
                    print("1 - Ford-Fulkerson")
                    print("2 - Push-Relabel")
                    algo = input("Votre choix : ")

                    if algo == "1":
                        executer_ford_fulkerson(capacites, noms_sommets)
                    elif  algo == "2" : 
                        executer_push_relabel(capacites, noms_sommets)
                    else:
                        print("Choix invalide.")
            else:
                print("Numéro invalide. Choisissez entre 1 et 10.")
        except ValueError:
            print("Veuillez entrer un nombre ou 'q' pour quitter.")
