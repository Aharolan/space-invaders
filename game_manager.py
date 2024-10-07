import pygame
from settings import settings
import player
import enemies
import random


class GameManager:

    def __init__(self):
        self.game_active = True
        self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
        self.background = pygame.image.load(settings.background_img)
        self.clock = pygame.time.Clock()
        self.player = player.Player()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.background_pos = settings.background_pos
        self.shooting = False

    def start_game(self):
        pygame.init()
        pygame.display.set_caption(settings.name)
        self.init_enemy_group()
        settings.background_sound.play()

    def run_game(self):
        if self.game_active:
            self.init_background()
            self.screen.blit(self.player.image, self.player.rect)
            self.display_score_level_and_live()
            self.check_live()
            self.check_keys()
            self.check_collision()
            self.change_direction()
            self.shoot()
            self.enemy_shoot()
            self.enemy_group.update()
            self.bullet_group.update()
            self.enemy_bullet_group.update()
            self.enemy_group.draw(self.screen)
            self.bullet_group.draw(self.screen)
            self.enemy_bullet_group.draw(self.screen)
            if settings.level < settings.sum_levels:
                self.level_up()
            if settings.level == settings.sum_levels and len(self.enemy_group) <= 0:
                self.display_won()
        else:
            self.screen.blit(pygame.image.load(settings.game_over), settings.screen_dest)
            settings.game_over_sound.play()
        pygame.display.update()
        self.clock.tick(settings.ticks)

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_l()
        if keys[pygame.K_RIGHT]:
            self.player.move_r()
        if keys[pygame.K_SPACE]:
            self.shooting = True

    def shoot(self):
        for event in pygame.event.get():
            if self.shooting and len(self.bullet_group) <= settings.stuck:
                self.shooting = False
                self.bullet_group.add(self.player.shoot())
                # pygame.time.delay(1000)

    def check_collision(self):
        pygame.sprite.groupcollide(self.bullet_group, self.enemy_bullet_group, True, True)
        if pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, True):
            self.player.score += 1
            settings.smash_sound.play()
        if pygame.sprite.spritecollide(self.player, self.enemy_bullet_group, True):
            self.player.live -= 1
            if self.player.live >= 1:
                settings.hit_sound.play()

        if pygame.sprite.spritecollide(self.player, self.enemy_group, True):
            self.player.live -= 1

    def init_background(self):
        self.screen.blit(self.background, (0, self.background_pos))
        if self.background_pos < 0:
            self.background_pos += settings.background_change
        else:
            self.background_pos = settings.background_pos

    def init_enemy_group(self):
        y = settings.enemy_y_pos
        for i in range(settings.enemy_rows):
            x = settings.enemy_width
            for j in range(settings.enemy_columns):
                enemy = enemies.Enemy()
                self.enemy_group.add(enemy)
                enemy.rect.left = x
                enemy.rect.bottom = y
                x += settings.enemy_width
            y += settings.enemy_height

    def change_direction(self):
        for enemy in self.enemy_group:
            if enemy.rect.left <= 0 or enemy.rect.right >= settings.screen_width:
                settings.direction *= -1
                for one_enemy in self.enemy_group:
                    one_enemy.rect.bottom += settings.enemy_down
                break

    def enemy_shoot(self):
        if len(self.enemy_group) > 0:
            if random.randint(0, settings.shoot_amount) == 1:
                random_enemy = random.choice(self.enemy_group.sprites())
                self.enemy_bullet_group.add(random_enemy.shoot())

    def check_live(self):
        if self.player.live == 0:
            self.game_active = False

    def display_score_level_and_live(self):
        my_font = pygame.font.Font(None, settings.font_size)
        live = my_font.render(f"live = {self.player.live}", False, "yellow")
        score = my_font.render(f"score = {self.player.score}", False, "GREEN")
        level = my_font.render(f"level {settings.level}", False, "orange")
        self.screen.blit(live, settings.live_dest)
        self.screen.blit(score, settings.score_dest)
        self.screen.blit(level, settings.level_dest)
        pygame.draw.line(self.screen, "red", settings.line_start_pos, settings.line_end_pos, settings.line_width)

    def display_won(self):
        my_font = pygame.font.Font(None, settings.won_font_size)
        won = my_font.render("you won", False, "purple")
        settings.success_sound.play()
        self.screen.blit(settings.confetti, (0, self.background_pos))
        self.screen.blit(won, settings.won_dest)

    def level_up(self):
        if len(self.enemy_group) <= 0:
            settings.level += 1
            settings.enemy_speed += settings.increase_enemy_speed
            settings.stuck -= 1
            settings.enemy_down += settings.increase_enemy_down
            settings.enemy_y_pos = settings.new_group_pos
            settings.shoot_amount -= settings.increase_shoot_amount
            settings.player_speed += settings.increase_player_speed
            self.init_enemy_group()
