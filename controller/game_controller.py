import pygame
from model.player import Player
from view.renderer import Renderer

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.renderer = Renderer(self.screen, 'assets/images/spritesheet_player.png')
        self.player = Player("Hero", 100)
        self.running = True
        self.renderer.update_music('./assets/musics/champion_red_battle.mp3')

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000  # Delta time en secondes

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move("à gauche")
                        self.renderer.set_facing_direction(False)  # Regarde à gauche
                    elif event.key == pygame.K_RIGHT:
                        self.player.move("à droite")
                        self.renderer.set_facing_direction(True)  # Regarde à droite

            self.renderer.update_animation(dt)
            self.screen.fill((0, 0, 0))
            self.renderer.draw_player(100, 100)
            pygame.display.flip()

        pygame.quit()
