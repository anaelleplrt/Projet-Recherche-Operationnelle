from reader import lire_graphe
from bellman import calculer_table_bellman
from collections import deque
import heapq

# Génère les noms de sommets : s, a, b, ..., t
def get_noms_sommets(n):
    if n == 1:
        return ['s']
    elif n == 2:
        return ['s', 't']
    return ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']

# Détermine si un graphe est à coût minimal
def est_flot_a_cout_min(numero):
    return numero >= 6     # pk ???

# ------------------------
# Affichage Matrice
# ------------------------

def afficher_matrice(nom, matrice, noms_sommets=None):
    print(f"\n=== {nom} ===")
    if matrice is None:
        print("Aucune donnée.")
        return

    n = len(matrice)
    largeur = max(len(str(e)) for row in matrice for e in row) + 1

    # Génère automatiquement : s, a, b, ..., t selon n
    if noms_sommets is None:
        if n == 1:
            noms_sommets = ['s']
        elif n == 2:
            noms_sommets = ['s', 't']
        else:
            noms_sommets = ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t']

    header = "    " + " ".join([f"{nom:>{largeur}}" for nom in noms_sommets])
    print(header)
    print("   " + "-" * len(header))

    for i, ligne in enumerate(matrice):
        ligne_str = " ".join([f"{val:>{largeur}}" for val in ligne])
        print(f"{noms_sommets[i]:>2} | {ligne_str}")


# Fonction principale de traitement du graphe

def traiter_graphe(numero):
    chemin = f"graphes-tests/graphe{numero}.txt"
    n, capacites, couts = lire_graphe(chemin)
    noms = get_noms_sommets(n)

    print(f"\n✔ Chargement du graphe {numero}")
    afficher_matrice("Matrice des capacités", capacites, noms)

    if est_flot_a_cout_min(numero):
        afficher_matrice("Matrice des coûts", couts, noms)
        table = calculer_table_bellman(n)
        afficher_matrice("Table de Bellman (simulation)", table, noms)
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

    print(f"\n✅ Flot maximum total = {exces[puits]}")
    return exces[puits]

def executer_push_relabel(capacites, noms):
    push_relabel(capacites, noms)


# ------------------------------
# Algorithme Bellman
# ------------------------------

def executer_flot_min_cout(capacites, couts, noms) : 
    