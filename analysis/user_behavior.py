import pandas as pd
import matplotlib.pyplot as plt

# Lire le fichier CSV
df = pd.read_csv("assets/scores.csv")

# Extraire les colonnes nécessaires
first_col = df["id"]
second_col = df["Pseudo"]
third_col = df["Score"]
fourth_col = df["Difficulté"]
time_col = df["Temps"]

# Créer une colonne "index_unique" pour chaque score
df['index_unique'] = range(len(df))

# Fonction pour afficher les graphiques
def afficher_graphique(type_graphique, data_type):
    """
    Fonction générique pour afficher différents types de graphiques
    type_graphique : "barres", "plot", "points"
    data_type : "score" ou "temps"
    """
    # Créer les données pour l'axe X
    x = df['index_unique']  # Utiliser un index unique pour l'axe X
    labels = df['Pseudo']   # Utiliser les pseudos des joueurs pour l'axe X

    # Vérifier quel type de données (score ou temps)
    if data_type == "score":
        y = df['Score']  # Les scores des joueurs
        y_label = "Score"
        title = "Graphique des Scores des Joueurs"
    elif data_type == "temps":
        y = df['Temps']  # Temps de jeu
        y_label = "Temps de Jeu (secondes)"  # Ajout de l'unité "secondes"
        title = "Graphique des Temps de Jeu des Joueurs"
    else:
        print("Type de données invalide.")
        return

    # Création de la fenêtre du graphique
    plt.figure(figsize=(12, 6))  # Taille de la fenêtre du graphique

    # Choisir le type de graphique
    if type_graphique == "barres":
        plt.bar(x, y, color="green")
        plt.title(f"{title} (Barres)")
    elif type_graphique == "plot":
        plt.plot(x, y, color="green")
        plt.title(f"{title} (Lignes)")
    elif type_graphique == "scatter":
        plt.scatter(x, y, color="green")
        plt.title(f"{title} (Points)")
    else:
        print("Type de graphique invalide.")
        return

    # Personnaliser les axes
    plt.xlabel("Joueurs")
    plt.ylabel(y_label)
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Fonction pour traiter la commande de l'utilisateur
def traiter_commande(commande):
    """
    Traite la commande de l'utilisateur de type 'score 1' ou 'temps 2'
    """
    try:
        # Diviser la commande en deux parties : data_type et type_graphique
        data_type, type_graphique = commande.split()

        # Vérifier que le type de graphique est valide
        type_graphique_dict = {"1": "barres", "2": "plot", "3": "scatter"}
        if type_graphique not in type_graphique_dict:
            print("Type d'affichage invalide. Veuillez entrer 1, 2 ou 3.")
            return
        
        # Convertir type_graphique en une forme exploitable
        type_graphique = type_graphique_dict[type_graphique]

        # Vérifier que data_type est valide
        if data_type not in ["score", "temps"]:
            print("Type de données invalide. Veuillez entrer 'score' ou 'temps'.")
            return
        
        # Afficher le graphique en fonction de la commande
        afficher_graphique(type_graphique, data_type)
    
    except ValueError:
        print("Commande invalide. Format attendu : 'score 1', 'temps 2', etc.")
    
# Explications pour l'utilisateur
def afficher_instructions():
    print("\nInstructions pour saisir la commande :")
    print("Vous pouvez choisir d'afficher le graphique des scores ou des temps de jeu des joueurs.")
    print("Les commandes doivent être saisies sous la forme :")
    print("'score X'  : pour afficher un graphique basé sur les scores des joueurs.")
    print("'temps X'  : pour afficher un graphique basé sur les temps de jeu des joueurs.")
    print("Où 'X' est le type de graphique :")
    print("1. Barres")
    print("2. Lignes")
    print("3. Points")
    print("Ou entrez quit pour quitter.")

# Menu interactif
def menu():
    afficher_instructions()  # Afficher les instructions pour l'utilisateur

    while True:
        commande = input("\nEntrez une commande pour afficher le graphique (ex. 'score 1', 'temps 2') ou 'quit' pour quitter : ").strip().lower()
        
        if commande == "quit":
            print("A bientôt!")
            break  # Quitter la boucle et terminer le programme
        else:
            traiter_commande(commande)

# Lancer le programme
menu()