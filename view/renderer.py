import pygame
import random
from .spritesheet import Spritesheet

class Renderer:
    def __init__(self, screen, spritesheet_path):
        # Initialisation du rendu et des sprites
        self.screen = screen
        self.spritesheet = Spritesheet(spritesheet_path)
        self.player_sprites_normal = self.spritesheet.get_sprites(0, 0, 64, 64, num_sprites=4)
        self.player_sprites_qte_success = [
            self.spritesheet.get_sprites(0, 64, 64, 64, num_sprites=4),
            self.spritesheet.get_sprites(0, 128, 64, 64, num_sprites=4),
            self.spritesheet.get_sprites(0, 192, 64, 64, num_sprites=4)
        ]
        self.current_sprite_index = 0
        self.animation_speed = 0.1  # Vitesse d'animation
        self.time_since_last_frame = 0
        self.facing_right = True
        self.current_qte_success_sprites = None
        self.is_qte_success = False
        self.font = pygame.font.Font(None, 36)

    def update_animation(self, dt):
        """Mise à jour de l'animation en fonction du temps écoulé."""
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.get_current_sprites())

    def get_current_sprites(self):
        """Retourne les sprites actuels en fonction de l'état."""
        if self.is_qte_success and self.current_qte_success_sprites:
            return self.current_qte_success_sprites
        return self.player_sprites_normal

    def draw_player(self, x, y):
        """Dessine le joueur à la position spécifiée."""
        current_sprite = self.get_current_sprites()[self.current_sprite_index]
        if not self.facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)
        self.screen.blit(current_sprite, (x, y))

    def set_facing_direction(self, facing_right):
        """Change la direction du joueur."""
        self.facing_right = facing_right

    def set_qte_success_animation(self, status):
        """Définit l'animation de réussite du QTE."""
        self.is_qte_success = status
        if status:
            self.current_qte_success_sprites = random.choice(self.player_sprites_qte_success)

    def draw_text(self, text, x, y, color=(0, 0, 0)):
        """Dessine du texte sur l'écran."""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_qte(self, qte_event):
        """Affiche l'instruction du QTE."""
        if qte_event.is_active():
            self.draw_text(f"Press '{pygame.key.name(qte_event.key).upper()}'!", 330, 490)

    def draw_qte_warning(self):
        """Affiche un avertissement de QTE."""
        warning_surface = pygame.Surface((200, 50))
        warning_surface.fill((255, 0, 0))
        warning_surface.set_alpha(128)
        self.screen.blit(warning_surface, (290, 480))
        self.draw_text("Prepare!", 335, 490)

    def draw_difficulty_level(self, level):
        """Affiche le niveau de difficulté."""
        self.draw_text(f"Difficulty Level: {level}", 10, 10)

    def draw_score(self, score):
        """Affiche le score."""
        self.draw_text(f"Score: {score}", 680, 10)

    def draw_lives(self, lives):
        """Affiche le nombre de vies restantes."""
        self.draw_text(f"Lives: {lives}", 10, 50)

    def draw_defeat_message(self):
        """Affiche le message de défaite."""
        self.draw_text("Game Over! You lost!", 260, 300, color=(255, 0, 0))
