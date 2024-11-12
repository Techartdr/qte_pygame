import pygame

class Spritesheet:
    def __init__(self, file_path):
        self.spritesheet = pygame.image.load(file_path).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return sprite

    def get_sprites(self, start_x, start_y, width, height, num_sprites, spacing=0):
        sprites = []
        for i in range(num_sprites):
            sprite = self.get_sprite(start_y + i * (width + spacing), start_x, width, height)
            sprites.append(sprite)
        return sprites
