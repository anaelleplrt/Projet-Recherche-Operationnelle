# Projet de Recherche Opérationnelle

## Présentation

Ce projet vise à résoudre des problèmes de flots sur des graphes à l'aide de différents algorithmes :
- **Flot maximal** avec :
  - Ford-Fulkerson
  - Push-Relabel
- **Flot à coût minimal** utilisant Bellman-Ford sur graphe résiduel.
- **Mesures de performances** sur graphes aléatoires.


---

## Contenu du projet

| Fichier / Dossier         | Rôle |
|----------------------------|------|
| **main.py**                | Lancement du menu principal pour choisir un graphe, exécuter les algorithmes ou générer un graphe aléatoire. |
| **menu.py**                | Contient la logique du menu interactif utilisé dans `main.py`. |
| **fonctions.py**           | Implémente tous les algorithmes et fonctionnalités principales : Ford-Fulkerson, Push-Relabel, Flot à coût minimal, matrices, Bellman, génération de graphes, mesure de temps, etc. |
| **reader.py**              | Lit les graphes depuis les fichiers `.txt`. |
| **generer_traces.py**      | Génère automatiquement les fichiers de **traces d'exécution** pour les 10 graphes fournis (graphes-tests). |
| **tester_performance.py**  | Effectue **100 tests** sur un `n` donné, mesure les temps d'exécution des 3 algorithmes et stocke les résultats dans un fichier `.csv`. |
| **tracer_graphiques.py**   | Génère des **nuages de points** pour visualiser le temps d'exécution des algorithmes en fonction de la taille des graphes (`n`). |
| **graphes-tests/**         | Contient les 10 fichiers `.txt` représentant les graphes à analyser. |
| **traces-exécutions/**     | Dossier généré automatiquement contenant toutes les **traces d'exécution** pour les graphes 1 à 10. |
| **resultats_nX.csv**       | Fichiers générés lors des tests de performance pour différentes tailles `n`. |
| **nuage_FF.png / nuage_PR.png / nuage_MIN.png** | Graphiques générés à partir des résultats de performances. |

---

## Utilisation

### 1. Lancer le main.py

```bash
python main.py
```
- Choisissez un graphe (1-10) ou générez un graphe aléatoire.

- Exécutez l'algorithme choisi.

- Observez le flot maximal ou le coût minimal détaillé.

### 2. Générer les fichiers de traces pour les graphes 1 à 10
```bash
python generer_traces.py
```
- Génère automatiquement tous les fichiers de traces (FF, PR, MIN) dans traces-exécutions/.

### 3. Tester les performances (100 tests pour un n donné)
```bash
python tester_performance.py
```
- Entrez la taille n du graphe (ex : 10, 50, 100, etc.).
- Le script exécute les 3 algorithmes 100 fois et enregistre les résultats dans resultats_nX.csv.

### 4. Tracer les nuages de points
```bash
python tracer_graphiques.py
```
- Lit les fichiers .csv de performances.
- Génére des nuages de points pour Ford-Fulkerson, Push-Relabel et Flot à coût minimal (nuage_FF.png, nuage_PR.png, nuage_MIN.png).



### Auteurs
Projet réalisé par Anaëlle, Tristan, Diaby, Jérôme et Louise (Groupe G5)
Dans le cadre du cours de Recherche Opérationnelle.
