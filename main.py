from controller.game_controller import GameController

def main():
    # Initialisation du contrôleur principal du jeu
    game = GameController()
    
    # Lancement de la boucle principale du jeu
    game.run()

if __name__ == "__main__":
    main()