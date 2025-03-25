def lire_graphe(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    lines = lines[1:]

    capacites = [list(map(int, lines[i].strip().split())) for i in range(n)]

    # Lire la matrice des coûts uniquement si elle existe
    couts = None
    if len(lines) >= 2 * n:
        couts = [list(map(int, lines[i].strip().split())) for i in range(n, 2 * n)]

    return n, capacites, couts
