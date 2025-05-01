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
    if matrice is None:
        print("Aucune donnée.")
        return

    nb_sommets = len(matrice)

    if noms_sommets is None:
        noms_sommets = get_noms_sommets(nb_sommets)


    print(f"\n=== {nom} ===")
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

        # Flot max autorisé
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
    n = len(capacites)
    visited = [False] * n
    queue = deque()
    queue.append(source)
    visited[source] = True

    if afficher:
        print(f"\n★ Itération {iteration} :")
        print("Le parcours en largeur :")
        print(noms[source])

    niveaux = [[source]]  # liste des sommets par niveau
    level = 0

    while niveaux[level]:
        next_level = []
        ligne_sommets = []
        ligne_parents = []
        for u in niveaux[level]:
            for v in range(n):
                if not visited[v] and residuel[u][v] > 0:
                    parent[v] = u
                    visited[v] = True
                    next_level.append(v)
                    ligne_sommets.append(noms[v])
                    ligne_parents.append(f"Π({noms[v]}) = {noms[u]}")
                    if v == puits:
                        niveaux.append(next_level)
                        if afficher:
                            print("".join(ligne_sommets) + " ; " + " ; ".join(ligne_parents))
                        return True
        if ligne_sommets and afficher:
            print("".join(ligne_sommets) + " ; " + " ; ".join(ligne_parents))
        niveaux.append(next_level)
        level += 1

    return False


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
        while v != source: # O(n)
            u = parent[v]
            chemin.append((u, v))
            flot = min(flot, residuel[u][v])
            v = u
        chemin.reverse() #O(n)
        chemin_str = ''.join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])

        if afficher:
            print(f"\nDétection d’une chaîne améliorante : {chemin_str} de flot {flot}")

        v = puits
        while v != source: #O(n)
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
        print("\n🔧 Résolution avec Ford-Fulkerson :")
    return ford_fulkerson(capacites, source, puits, noms, afficher=afficher)




# ------------------------------
# Algorithme Pousser-Réétiqueter
# ------------------------------

def push_relabel(capacites, noms, afficher=True):
    n = len(capacites)
    source = 0
    puits = n - 1

    hauteur = [0] * n # O(n)
    exces = [0] * n # O(n)
    residuel = [row[:] for row in capacites] #  O(n * n)

    # Initialisation
    hauteur[source] = n
    for v in range(n):      #O(n)
        if residuel[source][v] > 0:
            flot = residuel[source][v]
            residuel[source][v] -= flot
            residuel[v][source] += flot
            exces[v] += flot
            exces[source] -= flot

    def push(u, v):
        delta = min(exces[u], residuel[u][v])
        residuel[u][v] -= delta
        residuel[v][u] += delta
        exces[u] -= delta
        exces[v] += delta
        if afficher:
            print(f"🔄 Push : {noms[u]} → {noms[v]} (Δ = {delta})")

    def relabel(u):
        min_h = float('inf')
        for v in range(n): # O(n)
            if residuel[u][v] > 0:
                min_h = min(min_h, hauteur[v]) 
        if min_h < float('inf'):
            if afficher:
                print(f"⤴️ Relabel : {noms[u]} (hauteur {hauteur[u]} → {min_h + 1})")
            hauteur[u] = min_h + 1

    def afficher_etat(iteration):
        if afficher:
            print(f"\n★ Itération {iteration} :")
            print("Hauteur :", {noms[i]: h for i, h in enumerate(hauteur)})
            print("Excès   :", {noms[i]: e for i, e in enumerate(exces)})
            afficher_matrice("Graphe résiduel", residuel, noms)

    def choisir_sommet_actif():
        candidats = [(hauteur[i], noms[i], i) for i in range(n) if i != source and i != puits and exces[i] > 0] # O(n)
        if not candidats:
            return None
        return sorted(candidats, key=lambda x: (-x[0], x[1]))[0][2] # O(n) + O(nlog(n))

    if afficher:
        print("\n🔧 Résolution avec Push-Relabel :")
    iteration = 1
    afficher_etat(iteration)

    while True: #O(n)
        u = choisir_sommet_actif() # O(n) + O(n) + O(nlog(n))
        if u is None:
            break

        pushed = False
        voisins = sorted([v for v in range(n) if residuel[u][v] > 0], key=lambda x: (noms[x] != noms[puits], noms[x])) # O(n) + O(nlog(n))
        for v in voisins: #O(n)
            if residuel[u][v] > 0 and hauteur[u] == hauteur[v] + 1:
                push(u, v)
                afficher_etat(iteration)
                pushed = True
                break
        if not pushed:
            relabel(u) # O(n)
            afficher_etat(iteration)

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
        print(f"\n✅ Flot maximum total = {exces[puits]}")

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
    n = len(residuel)
    graphe_mixte = [["" for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if residuel[u][v] > 0:
                graphe_mixte[u][v] = f"{residuel[u][v]} ; {couts_residuel[u][v]}"
            else:
                graphe_mixte[u][v] = "0"
    afficher_matrice("Graphe résiduel pondéré (capacité ; coût)", graphe_mixte, noms)

# ------------------------------#
# Fonction Bellman détaillée    #
# ------------------------------#

def afficher_table_bellman_detaillee(noms, etapes):
    print("\n=== Table de Bellman complète ===")
    table = []

    n = len(noms)
    for k in range(len(etapes) + 1):
        ligne = [str(k)]
        if k == 0:
            # Affichage initial
            for i in range(n):
                if i == 0:
                    ligne.append("0")  # s
                else:
                    ligne.append("+∞")
        else:
            distances, parents = etapes[k - 1]
            for i in range(n):
                if distances[i] == float('inf'):
                    val = "+∞"
                elif parents[i] == -1:
                    val = str(distances[i])
                else:
                    val = f"{distances[i]}({noms[parents[i]]})"
                ligne.append(val)
        table.append(ligne)

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

    residuel = [row[:] for row in capacites] #O(n * n)
    couts_residuel = [row[:] for row in couts] # O ( n * n )

    iteration = 1
    if afficher:
        print("\n🚀 Démarrage de l'algorithme de flot à coût minimal...")

    while flot_total < val_flot: # o(F)
        distances = [float('inf')] * n # O(n)
        parents = [-1] * n # O(n)
        distances[source] = 0
        etapes = []

        for _ in range(n - 1): #O (n**3)
            new_distances = distances[:]
            new_parents = parents[:]
            for u in range(n):
                for v in range(n):
                    if residuel[u][v] > 0 and distances[u] + couts_residuel[u][v] < new_distances[v]:
                        new_distances[v] = distances[u] + couts_residuel[u][v]
                        new_parents[v] = u
            etapes.append((new_distances[:], new_parents[:]))
            if new_distances == distances:
                break
            distances = new_distances
            parents = new_parents

        if afficher:
            afficher_table_bellman_detaillee(noms, etapes)

        if distances[puits] == float('inf'):
            if afficher:
                print("\n❌ Aucun chemin de coût minimal disponible. Arrêt.")
            break

        chemin = []
        v = puits
        while v != source: #O(n)
            u = parents[v]
            chemin.append((u, v))
            v = u
        chemin.reverse() # O(n)

        if afficher:
            chemin_str = ''.join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])
            print(f"\n➡️ Chaîne améliorante de coût minimal trouvée : {chemin_str}")

        flot_augmentable = min(residuel[u][v] for u, v in chemin) # O(n)
        flot_envoye = min(flot_augmentable, val_flot - flot_total) # O(n)
        cout_chaine = sum(couts_residuel[u][v] for u, v in chemin) # O(n)

        if afficher:
            print(f" Flot envoyé dans cette chaîne : {flot_envoye}")
            print(f" Coût unitaire de la chaîne : {cout_chaine}")

        for u, v in chemin: # O(n)
            residuel[u][v] -= flot_envoye
            residuel[v][u] += flot_envoye
            couts_residuel[v][u] = -couts_residuel[u][v]

        flot_total += flot_envoye
        cout_total += flot_envoye * cout_chaine

        if afficher:
            print("\n --> Graphe résiduel pondéré mis à jour :")
            afficher_graphe_residuel_pondere(residuel, couts_residuel, noms)
            print(f"📦 Flot total envoyé : {flot_total} / {val_flot}")
            print(f"💸 Coût total accumulé : {cout_total}\n")

        iteration += 1

    if afficher:
        print("\n✅ Algorithme terminé.")
        print(f" Flot total envoyé : {flot_total}")
        print(f" Coût total du flot : {cout_total}")

    return flot_total

    


# ------------------------------#
# Complexité                    #
# ------------------------------#

def generer_graphe_aleatoire(n):
    capacites = [[0]*n for _ in range(n)]
    couts = [[0]*n for _ in range(n)]

    nb_valeurs_non_nulles = math.floor((n * n) / 2)

    # Génère E(n²/2) couples (i ≠ j)
    couples = [(i, j) for i in range(n) for j in range(n) if i != j]
    selection = random.sample(couples, nb_valeurs_non_nulles)

    for i, j in selection:
        capacites[i][j] = random.randint(1, 100)
        couts[i][j] = random.randint(1, 100)

    return capacites, couts




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

