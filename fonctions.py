from reader import lire_graphe
from collections import deque
import heapq
from tabulate import tabulate

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
        get_noms_sommets(nb_sommets)

    print(f"\n=== {nom} ===")
    print(tabulate(matrice, headers=noms_sommets, showindex=noms_sommets, tablefmt="fancy_grid"))



# Fonction principale de traitement du graphe

def traiter_graphe(numero):
    chemin = f"graphes-tests/graphe{numero}.txt"
    n, capacites, couts = lire_graphe(chemin)
    noms = get_noms_sommets(n)

    print(f"\n✔ Chargement du graphe {numero}")
    afficher_matrice("Matrice des capacités", capacites, noms)

    if est_flot_a_cout_min(numero):
        afficher_matrice("Matrice des coûts", couts, noms)
        #table = calculer_table_bellman(n)
        #afficher_matrice("Table de Bellman (simulation)", table, noms)
        #executer_flot_min_cout(capacites, couts, noms)
    

# ------------------------------
# Algorithme Ford-Fulkerson
# ------------------------------

#Parcours en largeur
def bfs(capacites, residuel, source, puits, parent, noms, iteration):
    n = len(capacites)
    visited = [False] * n
    queue = deque()
    queue.append(source)
    visited[source] = True

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
                        print("".join(ligne_sommets) + " ; " + " ; ".join(ligne_parents))
                        return True
        if ligne_sommets:
            print("".join(ligne_sommets) + " ; " + " ; ".join(ligne_parents))
        niveaux.append(next_level)
        level += 1

    return False

def ford_fulkerson(capacites, source, puits, noms):
    n = len(capacites)
    residuel = [row[:] for row in capacites]
    parent = [-1] * n
    flot_max = 0
    iteration = 1

    while bfs(capacites, residuel, source, puits, parent, noms, iteration):
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

        print(f"\nDétection d’une chaîne améliorante : {chemin_str} de flot {flot}")

        v = puits
        while v != source:
            u = parent[v]
            residuel[u][v] -= flot
            residuel[v][u] += flot
            v = u

        print("\nModifications sur le graphe résiduel :")
        afficher_matrice("Graphe résiduel", residuel, noms)

        flot_max += flot
        iteration += 1

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

def executer_ford_fulkerson(capacites, noms):
    source = 0
    puits = len(capacites) - 1
    print("\n🔧 Résolution avec Ford-Fulkerson :")
    ford_fulkerson(capacites, source, puits, noms)


# ------------------------------
# Algorithme Pousser-Réétiqueter
# ------------------------------

def push_relabel(capacites, noms):
    n = len(capacites)
    source = 0
    puits = n - 1

    hauteur = [0] * n
    exces = [0] * n
    residuel = [row[:] for row in capacites]

    # Initialisation
    hauteur[source] = n
    for v in range(n):
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
        print(f"🔄 Push : {noms[u]} → {noms[v]} (Δ = {delta})")

    def relabel(u):
        min_h = float('inf')
        for v in range(n):
            if residuel[u][v] > 0:
                min_h = min(min_h, hauteur[v])
        if min_h < float('inf'):
            print(f"⤴️ Relabel : {noms[u]} (hauteur {hauteur[u]} → {min_h + 1})")
            hauteur[u] = min_h + 1

    def afficher_etat(iteration):
        print(f"\n★ Itération {iteration} :")
        print("Hauteur :", {noms[i]: h for i, h in enumerate(hauteur)})
        print("Excès   :", {noms[i]: e for i, e in enumerate(exces)})
        afficher_matrice("Graphe résiduel", residuel, noms)

    def choisir_sommet_actif():
        candidats = [(hauteur[i], noms[i], i) for i in range(n) if i != source and i != puits and exces[i] > 0]
        if not candidats:
            return None
        return sorted(candidats, key=lambda x: (-x[0], x[1]))[0][2]  # par hauteur décroissante puis ordre alphabétique

    # Lancement
    print("\n🔧 Résolution avec Push-Relabel :")
    iteration = 1
    afficher_etat(iteration)

    while True:
        u = choisir_sommet_actif()
        if u is None:
            break

        pushed = False
        voisins = sorted([v for v in range(n) if residuel[u][v] > 0], key=lambda x: (noms[x] != noms[puits], noms[x]))
        for v in voisins:
            if residuel[u][v] > 0 and hauteur[u] == hauteur[v] + 1:
                push(u, v)
                afficher_etat(iteration)
                pushed = True
                break
        if not pushed:
            relabel(u)
            afficher_etat(iteration)

        iteration += 1

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



def executer_push_relabel(capacites, noms):
    push_relabel(capacites, noms)


# ------------------------------#
# Algorithme Bellman-Ford       #
# ------------------------------#


# ------------------------------#
# Fonction Bellman détaillée    #
# ------------------------------#

def afficher_table_bellman_detaillee(noms, etapes):
    print("\n📊 Table de Bellman complète :")
    table = []
    for k, (distances, parents) in enumerate(etapes):
        ligne = [str(k)]
        for i in range(len(noms)):
            if distances[i] == float('inf'):
                val = "+∞"
            else:
                parent = parents[i]
                if parent == -1:
                    val = str(distances[i])
                else:
                    val = f"{distances[i]}{noms[parent].lower()}"
            ligne.append(val)
        table.append(ligne)
    print(tabulate(table, headers=["k"] + noms, tablefmt="fancy_grid"))

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
# Flot à coût minimal           #
# ------------------------------#

def bellman_ford(capacite, couts, source):
    n = len(couts)
    min_cout = [float('inf')] * n
    parent = [-1] * n
    min_cout[source] = 0
    etapes = [(min_cout[:], parent[:])]

    for k in range(n - 1):
        changement = False
        for u in range(n):
            for v in range(n):
                if capacite[u][v] > 0 and min_cout[u] + couts[u][v] < min_cout[v]:
                    min_cout[v] = min_cout[u] + couts[u][v]
                    parent[v] = u
                    changement = True
        etapes.append((min_cout[:], parent[:]))
        if not changement:
            break

    return min_cout, parent, etapes

def flot_min_cout(capacites, couts, noms, source, puits, val_flot):
    n = len(couts)
    residuel = [row[:] for row in capacites]
    couts_residuel = [row[:] for row in couts]
    flot_total = 0
    cout_total = 0

    for u in range(n):
        for v in range(n):
            if capacites[u][v] > 0:
                couts_residuel[v][u] = -couts[u][v]

    iteration = 1
    while True:
        cout_min, parents, etapes = bellman_ford(residuel, couts_residuel, source)
        print(f"\n📘 Itération {iteration}")
        afficher_table_bellman_detaillee(noms, etapes)

        if cout_min[puits] == float('inf'):
            print("\n❌ Aucun chemin améliorant trouvé, arrêt.")
            break

        chemin = []
        v = puits
        flot = float('inf')
        while v != source:
            u = parents[v]
            chemin.append((u, v))
            flot = min(flot, residuel[u][v])
            v = u
        chemin.reverse()
        chemin_str = ''.join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])

        print(f"\n✔️ Chaîne améliorante détectée : {chemin_str} de flot {flot}")

        if val_flot is not None and flot_total + flot > val_flot:
            flot = val_flot - flot_total
            print(f"🎯 Ajustement du flot : nouveau flot = {flot}")

        v = puits
        while v != source:
            u = parents[v]
            residuel[u][v] -= flot
            residuel[v][u] += flot
            v = u

        afficher_graphe_residuel_pondere(residuel, couts_residuel, noms)

        flot_total += flot
        cout_total += flot * cout_min[puits]

        if val_flot is not None and flot_total >= val_flot:
            print(f"\n🎯 Valeur cible de flot {val_flot} atteinte.")
            break

        iteration += 1

    print(f"\n★ Flot total = {flot_total}, Coût total = {cout_total}")
    matrice_flot = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if capacites[u][v] > 0:
                matrice_flot[u][v] = f"{capacites[u][v] - residuel[u][v]}/{capacites[u][v]}"
            else:
                matrice_flot[u][v] = "0"

    afficher_matrice("Flot final", matrice_flot, noms)
    return flot_total, cout_total

def executer_flot_min_cout(capacites, couts, noms, val_flot):
    source = 0
    puits = len(capacites) - 1
    print("\n🔧 Résolution du flot à coût minimal :")
    flot_min_cout(capacites, couts, noms, source, puits, val_flot)
