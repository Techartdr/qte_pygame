import pygame
from .spritesheet import Spritesheet

class Renderer:
    def __init__(self, screen, spritesheet_path):
        self.screen = screen
        self.spritesheet = Spritesheet(spritesheet_path)
        self.player_sprites = self.spritesheet.get_sprites(0, 0, 64, 64, num_sprites=4)
        self.current_sprite_index = 0
        self.animation_speed = 0.1  # Vitesse de l'animation
        self.time_since_last_frame = 0
        self.facing_right = True  # Indique la direction actuelle du joueur

    def update_music(self, musictoplay):
        soundtoplay = pygame.mixer.Sound(musictoplay)
        canal_sound = pygame.mixer.Channel(1)
        canal_sound.play(soundtoplay)

    def update_animation(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.player_sprites)

    def draw_player(self, x, y):
        current_sprite = self.player_sprites[self.current_sprite_index]

        # Retourne le sprite si le personnage doit faire face à gauche
        if not self.facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        self.screen.blit(current_sprite, (x, y))

    def set_facing_direction(self, facing_right):
        self.facing_right = facing_right
