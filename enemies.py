import pygame
from settings import settings
import bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(settings.enemy_img)
        self.rect = self.image.get_rect(midtop=(settings.enemy_x_pos, settings.enemy_y_pos))

    def shoot(self):
        return bullet.Bullet(self.rect.midbottom, 1)

    def update(self):
        self.rect.x += settings.enemy_speed * settings.direction
