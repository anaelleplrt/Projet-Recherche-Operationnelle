def calculer_table_bellman(n):
    # Exemple de simulation simple
    return [[float('inf') if i != 0 else 0 for _ in range(n)] for i in range(n)]
