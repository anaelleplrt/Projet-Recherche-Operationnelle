def lire_graphe(path):
    with open(path, 'r') as f:
        lines = f.readlines()  #on lit toutes les lignes du fichier

    n = int(lines[0].strip())  #la première ligne contient le nombre de sommets
    lines = lines[1:]  #on enlève cette première ligne pour traiter le reste

    #on lit la matrice des capacités (n lignes suivantes)
    capacites = [list(map(int, lines[i].strip().split())) for i in range(n)]

    #on lit la matrice des coûts uniquement si elle existe (au moins 2n lignes en tout)
    couts = None
    if len(lines) >= 2 * n:
        couts = [list(map(int, lines[i].strip().split())) for i in range(n, 2 * n)]

    return n, capacites, couts  #on retourne le nombre de sommets, la matrice des capacités et éventuellement la matrice des coûts
