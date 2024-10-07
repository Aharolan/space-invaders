import pygame
import game_manager

play = game_manager.GameManager()
play.start_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    play.run_game()
