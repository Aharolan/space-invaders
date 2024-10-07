import pygame
from settings import settings
import bullet


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(settings.player_img)
        self.rect = self.image.get_rect(midtop=(settings.player_x_pos, settings.player_y_pos))
        self.live = settings.live
        self.score = 0

    def move_r(self):
        if self.rect.right < settings.screen_width:
            self.rect.x += settings.player_speed

    def move_l(self):
        if self.rect.left > 0:
            self.rect.x -= settings.player_speed

    def shoot(self):
        settings.shoot_sound.play()
        return bullet.Bullet(self.rect.midtop, -1)
