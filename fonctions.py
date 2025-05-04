from reader import lire_graphe
from collections import deque
import heapq
from tabulate import tabulate
import copy
import time
import random
import os
import csv
import math
from time import perf_counter



# Génère les noms de sommets : s, a, b, ..., t
def get_noms_sommets(n):
    if n == 1:
        return ['s']
    elif n == 2:
        return ['s', 't']
    return ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']

# Détermine si un graphe est à coût minimal
def est_flot_a_cout_min(numero):
    return numero >= 6

# ------------------------
# Affichage Matrice
# ------------------------

def afficher_matrice(nom, matrice, noms_sommets=None):
    #si la matrice est vide, on affiche un message et on arrête
    if matrice is None:
        print("Aucune donnée.")
        return

    #on récupère le nombre de sommets (taille de la matrice)
    nb_sommets = len(matrice)

    #si aucun nom n'est donné, on les génère automatiquement
    if noms_sommets is None:
        noms_sommets = get_noms_sommets(nb_sommets)

    print(f"\n=== {nom} ===")

    #on affiche la matrice proprement grace a tabulate
    print(tabulate(matrice, headers=noms_sommets, showindex=noms_sommets, tablefmt="fancy_grid"))



# Fonction principale de traitement du graphe appelée dans le menu

def traiter_graphe(numero):
    chemin = f"graphes-tests/graphe{numero}.txt"
    n, capacites, couts = lire_graphe(chemin)
    noms = get_noms_sommets(n)

    print(f"\n✔ Chargement du graphe {numero}")
    afficher_matrice("Matrice des capacités", capacites, noms)

    if est_flot_a_cout_min(numero):
        afficher_matrice("Matrice des coûts", couts, noms)

        # Table de Bellman initiale
        residuel = [row[:] for row in capacites]
        couts_residuel = [row[:] for row in couts]

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

        # indique au user le flot max autorisé
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
        elif algo == "2":
            executer_push_relabel(capacites, noms)
        else:
            print("Choix invalide.")


# ------------------------------
# Algorithme Ford-Fulkerson
# ------------------------------

#Parcours en largeur
def bfs(capacites, residuel, source, puits, parent, noms, iteration, afficher=True):
    n = len(capacites)  #nombre de sommets
    visited = [False] * n  #liste pour savoir si un sommet a été visité

    visited[source] = True  #on commence par marquer la source comme visitée

    if afficher:
        print(f"\n★ Itération {iteration} :")
        print("Le parcours en largeur :")
        print(noms[source])

    niveaux = [[source]]  #liste des niveaux (pour affichage) → niveau 0 = source
    level = 0  #niveau actuel

    while niveaux[level]:  #tant qu’il y a des sommets à ce niveau
        next_level = []  #liste des sommets du niveau suivant
        ligne_sommets = []  #pour afficher les noms des sommets explorés à ce niveau
        ligne_parents = []  #pour afficher les parents associés

        for u in niveaux[level]:  #pour chaque sommet du niveau actuel
            for v in range(n):  #on regarde ses voisins
                if not visited[v] and residuel[u][v] > 0:  #si voisin non visité et capacité > 0
                    parent[v] = u  #on enregistre le parent de v
                    visited[v] = True
                    next_level.append(v)  #on ajoute ce voisin au niveau suivant
                    ligne_sommets.append(noms[v])
                    ligne_parents.append(f"Π({noms[v]}) = {noms[u]}")  #notation π(v) = u

                    if v == puits:  #si on a atteint le puits, on peut s’arrêter
                        niveaux.append(next_level)
                        if afficher:
                            print("".join(ligne_sommets) + " ; " + " ; ".join(ligne_parents))
                        return True  #un chemin de s à t a été trouvé

        #affichage intermédiaire du niveau courant
        if ligne_sommets and afficher:
            print("".join(ligne_sommets) + " ; " + " ; ".join(ligne_parents))

        niveaux.append(next_level)  #on passe au niveau suivant
        level += 1

    return False  #aucun chemin trouvé de s à t



def ford_fulkerson(capacites, source, puits, noms, afficher=True):
    n = len(capacites)
    residuel = [row[:] for row in capacites]
    parent = [-1] * n
    flot_max = 0
    iteration = 1

    while bfs(capacites, residuel, source, puits, parent, noms, iteration, afficher=afficher): 
        chemin = []
        v = puits
        flot = float('inf')
        while v != source: 
            u = parent[v]
            chemin.append((u, v))
            flot = min(flot, residuel[u][v])
            v = u
        chemin.reverse() 
        chemin_str = ''.join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])

        if afficher:
            print(f"\nDétection d’une chaîne améliorante : {chemin_str} de flot {flot}")

        v = puits
        while v != source: 
            u = parent[v]
            residuel[u][v] -= flot
            residuel[v][u] += flot
            v = u

        if afficher:
            print("\nModifications sur le graphe résiduel :")
            afficher_matrice("Graphe résiduel", residuel, noms)

        flot_max += flot
        iteration += 1

    if afficher:
        print("\n★ Affichage du flot max :")
        matrice_flot = [[0]*n for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if capacites[u][v] > 0:
                    matrice_flot[u][v] = f"{capacites[u][v] - residuel[u][v]}/{capacites[u][v]}"
                else:
                    matrice_flot[u][v] = "0"
        afficher_matrice("Flot maximum", matrice_flot, noms)
        print(f"\nValeur du flot max = {flot_max}")

    return flot_max

def executer_ford_fulkerson(capacites, noms, afficher=True):
    source = 0
    puits = len(capacites) - 1
    if afficher:
        print("\n Résolution avec Ford-Fulkerson :")
    return ford_fulkerson(capacites, source, puits, noms, afficher=afficher)




# ------------------------------
# Algorithme Pousser-Réétiqueter
# ------------------------------

def push_relabel(capacites, noms, afficher=True):
    n = len(capacites)
    s = 0
    puits = n - 1

    hauteur = [0] * n  #table des hauteurs de chaque sommet
    exces = [0] * n    #table des excès de chaque sommet
    residuel = [row[:] for row in capacites]  #copie de la matrice de capacités (graphe résiduel)

    #initialisation : la source a une hauteur = n
    hauteur[s] = n

    #pour chaque voisins v de n, on sature 
    for v in range(n):      
        if residuel[s][v] > 0:
            flot = residuel[s][v]
            residuel[s][v] -= flot  
            residuel[v][s] += flot 
            exces[v] += flot            
            exces[s] -= flot       

    #fonction pour effectuer un push de u vers v
    def push(u, v):
        delta = min(exces[u], residuel[u][v])  #on pousse le minimum entre l’excès de u et ce qu’on peut encore envoyer vers v
        residuel[u][v] -= delta
        residuel[v][u] += delta
        exces[u] -= delta
        exces[v] += delta
        if afficher:
            print(f"--> Push : {noms[u]} → {noms[v]} (Δ = {delta})")

    #fonction pour augmenter la hauteur de u (relabel)
    def relabel(u):
        min_h = float('inf')  #on initialise min_h à l'infini pour trouver la plus petite hauteur accessible

        for v in range(n):  #on parcourt tous les voisins v de u
            if residuel[u][v] > 0:  #s'il reste de la capacité de u vers v
                min_h = min(min_h, hauteur[v])  #on garde la plus petite hauteur parmi les voisins accessibles

        if min_h < float('inf'):  #si u peut pousser vers au moins un voisin
            if afficher:
                print(f"⤴  Relabel : {noms[u]} (hauteur {hauteur[u]} → {min_h + 1})")
            hauteur[u] = min_h + 1  #on augmente la hauteur de u juste au-dessus de celle de v

    
    #affichage de l'état actuel : hauteur, excès et graphe résiduel
    def afficher_etat(iteration):
        if afficher:
            print(f"\n★ Itération {iteration} :")
            print("Hauteur :", {noms[i]: h for i, h in enumerate(hauteur)})
            print("Excès   :", {noms[i]: e for i, e in enumerate(exces)})
            afficher_matrice("Graphe résiduel", residuel, noms)

    #fonction pour choisir le prochain sommet actif à traiter
    def choisir_sommet_actif():
        #on prend les sommets (hors s et t) qui ont un excès > 0
        candidats = [(hauteur[i], noms[i], i) for i in range(n) if i != s and i != puits and exces[i] > 0]
        if not candidats:
            return None 
        #on prend celui qui a la plus grande hauteur (ordre alphabétique en cas d'égalité)
        return sorted(candidats, key=lambda x: (-x[0], x[1]))[0][2]
    

    #boucle principale de push-relabel 
    if afficher:
        print("\n Résolution avec Push-Relabel :")
    iteration = 1
    afficher_etat(iteration) #afficher état initiale

    
    while True:
        u = choisir_sommet_actif()  #choix du sommet actif à traiter
        if u is None:
            break  #plus aucun sommet actif → on a terminé

        pushed = False  #pour savoir si un push a été fait

        #on trie les voisins de u : on pousse vers t en priorité, puis par ordre alphabétique
        voisins = sorted([v for v in range(n) if residuel[u][v] > 0], key=lambda x: (noms[x] != noms[puits], noms[x])) 

        for v in voisins:  #on essaie de pousser vers un voisin valide
            if residuel[u][v] > 0 and hauteur[u] == hauteur[v] + 1:
                push(u, v)  #on pousse si la condition de hauteur est respectée
                afficher_etat(iteration)
                pushed = True
                break

        if not pushed: #si aucun push possible, on relabel u
            relabel(u) 
            afficher_etat(iteration)

        iteration += 1

    if afficher:
        print("\n★ Affichage du flot max :")

        #on crée une matrice vide pour afficher le flot final
        matrice_flot = [[0]*n for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if capacites[u][v] > 0:
                    #on calcule le flot envoyé sur l’arête u→v : capacité initiale - capacité résiduelle et on l’affiche sous forme "flot/capacité"
                    matrice_flot[u][v] = f"{capacites[u][v] - residuel[u][v]}/{capacites[u][v]}"
                else:
                    #s’il n’y avait pas d’arête à la base, on affiche 0
                    matrice_flot[u][v] = "0"
        
        #affiche la matrice de flot final avec les noms de sommets + le flot max tot
        afficher_matrice("Flot maximum", matrice_flot, noms)
        print(f"\n --> Flot maximum total = {exces[puits]}")

    return exces[puits]

def executer_push_relabel(capacites, noms, afficher=True):
    return push_relabel(capacites, noms, afficher=afficher)




# ------------------------------#
# Algorithme Bellman-Ford       #
# ------------------------------#


# ------------------------------#
# Graphe résiduel pondéré       #
# ------------------------------#

def afficher_graphe_residuel_pondere(residuel, couts_residuel, noms):
    n = len(residuel)  #nombre de sommets
    #on crée une matrice vide de chaînes de caractères pour mélanger capacité et coût
    graphe_mixte = [["" for _ in range(n)] for _ in range(n)]

    for u in range(n):
        for v in range(n):
            if residuel[u][v] > 0:
                #s’il reste de la capacité de u vers v, on affiche "capacité ; coût"
                graphe_mixte[u][v] = f"{residuel[u][v]} ; {couts_residuel[u][v]}"
            else:
                #sinon on met "0" pour dire qu’il n’y a pas d’arête résiduelle
                graphe_mixte[u][v] = "0"

    afficher_matrice("Graphe résiduel pondéré (capacité ; coût)", graphe_mixte, noms)


# ------------------------------#
# Fonction Bellman détaillée    #
# ------------------------------#

def afficher_table_bellman_detaillee(noms, etapes):
    print("\n=== Table de Bellman complète ===")
    table = []

    n = len(noms)  #nombre de sommets

    for k in range(len(etapes) + 1):  #pour chaque itération k (de 0 à n)
        ligne = [str(k)]  #on commence la ligne par le numéro d’itération

        if k == 0:
            #affichage initial (avant la première mise à jour)
            for i in range(n):
                if i == 0:
                    ligne.append("0")  #la source a une distance de 0
                else:
                    ligne.append("+∞")  #les autres sommets sont à l’infini au début
        else:
            distances, parents = etapes[k - 1]  #on récupère les valeurs de l’étape k-1
            for i in range(n):
                if distances[i] == float('inf'):
                    val = "+∞"  #si le sommet est toujours inaccessible
                elif parents[i] == -1:
                    val = str(distances[i])  #pas de parent connu, juste la distance
                else:
                    val = f"{distances[i]}({noms[parents[i]]})"  #on affiche la distance et le parent
                ligne.append(val)

        table.append(ligne)  #on ajoute la ligne à la table

    #affichage final de la table avec tabulate
    print(tabulate(table, headers=["k"] + noms, tablefmt="fancy_grid"))




# ------------------------------#
# Flot à coût minimal           #
# ------------------------------#

def executer_flot_min_cout(capacites, couts, noms, val_flot, afficher=True): 
    n = len(capacites)
    source = 0
    puits = n - 1
    flot_total = 0
    cout_total = 0

    residuel = [row[:] for row in capacites]  #copie du graphe pour le graphe résiduel
    couts_residuel = [row[:] for row in couts]  #copie des coûts pour suivre les inverses

    iteration = 1
    if afficher:
        print("\n Démarrage de l'algorithme de flot à coût minimal...")

    #tant qu’on n’a pas encore atteint le flot voulu
    while flot_total < val_flot:
        distances = [float('inf')] * n  #distances depuis la source
        parents = [-1] * n  #parents pour reconstruire le chemin
        distances[source] = 0
        etapes = []  #pour afficher les étapes de Bellman

        #algorithme de Bellman-Ford sur n-1 itérations
        for _ in range(n - 1):
            new_distances = distances[:]
            new_parents = parents[:]
            for u in range(n):
                for v in range(n):
                    if residuel[u][v] > 0 and distances[u] + couts_residuel[u][v] < new_distances[v]:
                        new_distances[v] = distances[u] + couts_residuel[u][v]
                        new_parents[v] = u
            etapes.append((new_distances[:], new_parents[:]))
            if new_distances == distances:
                break  #plus aucune mise à jour
            distances = new_distances
            parents = new_parents

        #affiche les étapes du Bellman si demandé
        if afficher:
            afficher_table_bellman_detaillee(noms, etapes)

        #si on ne peut pas atteindre le puits
        if distances[puits] == float('inf'):
            if afficher:
                print("\n --> Aucun chemin de coût minimal disponible. Arrêt.")
            break

        #on reconstruit le chemin trouvé
        chemin = []
        v = puits
        while v != source:
            u = parents[v]
            chemin.append((u, v))
            v = u
        chemin.reverse()

        if afficher:
            chemin_str = ''.join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])
            print(f"\n --> Chaîne améliorante de coût minimal trouvée : {chemin_str}")

        #calcul du flot qu’on peut envoyer dans le chemin trouvé
        flot_augmentable = min(residuel[u][v] for u, v in chemin)
        flot_envoye = min(flot_augmentable, val_flot - flot_total)
        cout_chaine = sum(couts_residuel[u][v] for u, v in chemin)

        if afficher:
            print(f" Flot envoyé dans cette chaîne : {flot_envoye}")
            print(f" Coût unitaire de la chaîne : {cout_chaine}")

        #mise à jour du graphe résiduel et des coûts
        for u, v in chemin:
            residuel[u][v] -= flot_envoye
            residuel[v][u] += flot_envoye
            couts_residuel[v][u] = -couts_residuel[u][v]  #inversion du coût sur l’arête retour

        flot_total += flot_envoye
        cout_total += flot_envoye * cout_chaine

        if afficher:
            print("\n --> Graphe résiduel pondéré mis à jour :")
            afficher_graphe_residuel_pondere(residuel, couts_residuel, noms)
            print(f"--> Flot total envoyé : {flot_total} / {val_flot}")
            print(f"--> Coût total accumulé : {cout_total}\n")

        iteration += 1

    if afficher:
        print("\n--> Algorithme terminé.")
        print(f" Flot total envoyé : {flot_total}")
        print(f" Coût total du flot : {cout_total}")

    return flot_total  #on retourne le flot réellement envoyé

    


# ------------------------------#
# Complexité                    #
# ------------------------------#

def generer_graphe_aleatoire(n):
    capacites = [[0]*n for _ in range(n)]  #matrice des capacités initialisée à 0
    couts = [[0]*n for _ in range(n)]      #matrice des coûts initialisée à 0

    nb_valeurs_non_nulles = math.floor((n * n) / 2)  #on veut remplir ~50% des cases

    #on génère tous les couples (i, j) avec i ≠ j (pas de boucle sur soi-même)
    couples = [(i, j) for i in range(n) for j in range(n) if i != j]

    #on sélectionne aléatoirement nb_valeurs_non_nulles arêtes parmi tous les couples possibles
    selection = random.sample(couples, nb_valeurs_non_nulles)

    for i, j in selection:
        capacites[i][j] = random.randint(1, 100)  #on donne une capacité aléatoire entre 1 et 100
        couts[i][j] = random.randint(1, 100)      #on donne un coût aléatoire entre 1 et 100

    return capacites, couts  #on retourne les deux matrices générées





def mesurer_temps_execution_algos(capacites, couts, noms, val_flot, afficher=True):
    #FF
    start = perf_counter()
    flot_ff = executer_ford_fulkerson([row[:] for row in capacites], noms, afficher=afficher)
    t_ff = perf_counter() - start

    #PR
    start = perf_counter()
    flot_pr = executer_push_relabel([row[:] for row in capacites], noms, afficher=afficher)
    t_pr = perf_counter() - start

    #MIN
    start = perf_counter()
    flot_min = executer_flot_min_cout([row[:] for row in capacites], couts, noms, val_flot, afficher=afficher)
    t_min = perf_counter() - start

    return t_ff, t_pr, t_min, flot_ff, flot_pr, flot_min

