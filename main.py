import pygame
from controller.menu_controller import MenuController
from controller.game_controller import GameController

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jeu QTE")

    menu_controller = MenuController(screen)
    while True:
        choice = menu_controller.display_menu()

        if choice == 'play':
            player_name = menu_controller.get_player_name()
            if player_name:
                # Démarrer le jeu avec la prise en charge de l'ESP32, si disponible
                game = GameController(player_name, serial_port='COM6')
                result = game.run()
                if result == 'menu':
                    continue

        elif choice == 'scores':
            menu_controller.display_scores()

        else:
            break  # Quitter l'application

    pygame.quit()
