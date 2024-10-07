import pygame
from settings import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        self.direction = direction
        if self.direction == -1:
            self.image = pygame.image.load(settings.bullet_img)
        else:
            self.image = pygame.image.load(settings.enemy_bullet_img)
        self.rect = self.image.get_rect(midbottom=position)

    def update(self):
        if 0 < self.rect.y < settings.screen_height:
            self.rect.y += settings.bullet_speed * self.direction
        else:
            self.kill()
