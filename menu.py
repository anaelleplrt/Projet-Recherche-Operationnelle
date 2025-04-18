from fonctions import (
    lire_graphe,
    afficher_matrice,
    est_flot_a_cout_min,
    executer_ford_fulkerson,
    executer_push_relabel,
    #executer_flot_min_cout
)

def get_noms_sommets(n):
    if n == 1:
        return ['s']
    elif n == 2:
        return ['s', 't']
    return ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']

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

                    lancer = input("\nVoulez-vous lancer la résolution du flot à coût minimal ? (o/n) : ").lower()
                    #if lancer == 'o':
                        #executer_flot_min_cout(capacites, couts, noms)
                    #else:
                        #print("Résolution annulée.")
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
