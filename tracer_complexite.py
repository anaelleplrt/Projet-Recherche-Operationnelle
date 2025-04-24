import matplotlib.pyplot as plt
import csv

def tracer_nuage_points(fichier_csv):
    n_values = []
    temps_ff = []
    temps_pr = []
    temps_min = []

    with open(fichier_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                n_values.append(int(row['n']))
                temps_ff.append(float(row['Temps_FF']))
                temps_pr.append(float(row['Temps_PR']))
                temps_min.append(float(row['Temps_MinCout']))
            except:
                continue

    plt.figure(figsize=(10, 6))
    plt.scatter(n_values, temps_ff, label='Ford-Fulkerson', marker='o')
    plt.scatter(n_values, temps_pr, label='Push-Relabel', marker='s')
    plt.scatter(n_values, temps_min, label='Flot Min-Cout', marker='^')

    plt.title("Temps d'exécution des algorithmes en fonction de n")
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps (secondes)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("nuage_de_points.png")
    plt.show()

if __name__ == "__main__":
    tracer_nuage_points("resultats_algorithmes.csv")
