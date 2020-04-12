import pygame
from models import *
pygame.init()
game_running = False
inventory_opened = False
screen = Screen()
running = True
# Main pygame loop
while running:
    # ---------------------------------------- MENUS ---------------------------------------- #
    try:
        if screen.state == 'main':
            screen.main_screen()
        # ------------------------- YOU WON MENU ------------------------ #
        elif screen.state == 'win':
            screen.win_screen()
        # ------------------------ YOU LOST MENU ------------------ ------ #
        elif screen.state == 'lose':
            screen.lose_screen()
        # ------------------------ SETTINGS MENU ------------------------ #
        elif screen.state == 'settings':
            screen.settings_screen()
    except BaseException:
        pass
    # Catching events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if screen.handle_click(pygame.mouse.get_pos()) == 'game':
                screen.fade(screen.window)
                game = Game.initialize_game('map.txt')
    try:
        while not game.player.isDead:
            # ------------------------- GAME WINDOW ------------------------- #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.player.isDead = True
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if inventory_opened:
                            inventory_opened = False
                        else:
                            inventory_opened = True
                    if event.key in game.player.key_map:
                        game.player.move(
                            game.player.key_map[event.key], game, screen)
            # DRAW ELEMENTS
            for row in enumerate(game.map.map_elements):
                for cell in enumerate(row[1]):
                    screen.display_element(cell[0], row[0], game.map)
            # Draw player
            screen.display_player(game.player)
            # Draw items
            for item in game.map.items:
                screen.display_item(item)
            # Display Inventory
            if inventory_opened:
                screen.display_inventory(game.player.inventory)
            pygame.display.flip()

    except (RuntimeError, TypeError, NameError):
        pass
    # Flip the display
    pygame.display.flip()

pygame.quit()
