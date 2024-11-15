import pygame
import csv

class MenuController:
    def __init__(self, screen):
        # Initialisation des polices et de l'écran
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

    def display_menu(self):
        """Affiche le menu principal et gère les entrées utilisateur."""
        menu_running = True
        while menu_running:
            self.screen.fill((255, 255, 255))
            self.draw_text("Menu Principal", 270, 100)
            self.draw_text("1. Lancer le jeu", 270, 200)
            self.draw_text("2. Afficher les scores", 270, 250)
            self.draw_text("3. Quitter", 270, 300)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 'play'
                    elif event.key == pygame.K_2:
                        return 'scores'
                    elif event.key == pygame.K_3:
                        menu_running = False
                        return None

    def get_player_name(self):
        """Demande à l'utilisateur de saisir son pseudo."""
        name = ""
        input_active = True

        while input_active:
            self.screen.fill((255, 255, 255))
            self.draw_text("Entrez votre pseudo:", 270, 200)
            self.draw_text(name, 300, 250)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = False
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

    def display_scores(self):
        """Affiche les scores des joueurs à partir du fichier CSV."""
        self.screen.fill((255, 255, 255))
        self.draw_text("Scores des joueurs :", 280, 100)
        self.draw_text("(Echap : Menu)", 310, 125)

        y_offset = 200
        try:
            with open('assets/scores.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Ignorer l'en-tête
                scores = list(reader)

            for i, score in enumerate(scores):
                self.draw_text(f"{score[1]} - Score: {score[2]} - Difficulté: {score[3]}", 225, y_offset)
                y_offset += 30

        except FileNotFoundError:
            self.draw_text("Aucun score enregistré.", 300, 200)

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False

    def draw_text(self, text, x, y, color=(0, 0, 0)):
        """Dessine du texte sur l'écran."""
        text_surface = self.small_font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
