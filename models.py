from os import listdir
from random import randrange
import pygame


class Player:
    def __init__(self, x_position, y_position, inventory, image):
        self.position = (Position(x_position, y_position))
        self.inventory = inventory
        self.isDead = False
        self.win = False
        self.image = pygame.transform.scale(pygame.image.load(
            r'images/characters/' + image + '.png'), (45, 45))
        self.key_map = {
            pygame.K_LEFT: 'left',
            ord('a'): 'left',
            pygame.K_RIGHT: 'right',
            ord('d'): 'right',
            pygame.K_UP: 'up',
            ord('w'): 'up',
            pygame.K_DOWN: 'down',
            ord('s'): 'down'}

    def move(self, direction, game, screen):
        directions = {
            'left': (
                self.position.x - 1,
                self.position.y),
            'right': (
                self.position.x + 1,
                self.position.y),
            'up': (
                self.position.x,
                self.position.y - 1),
            'down': (
                self.position.x,
                self.position.y + 1)}
        if game.map.available_position(
                directions[direction][0],
                directions[direction][1]):
            self.position.x, self.position.y = directions[direction][0], directions[direction][1]
            self.checkItems(game, screen.sound)
            self.checkExit(game, screen)

    def checkItems(self, game, sound):
        for item in enumerate(game.map.items):
            if item[1].position.x == self.position.x and item[1].position.y == self.position.y:
                self.inventory.append(item[1])
                game.map.items.pop(item[0])
                if sound:
                    pygame.mixer.Sound("sounds/collect_item.wav").play()

    def checkExit(self, game, screen):
        if game.map.check_position(self.position.x, self.position.y) == 'E':
            self.isDead = True
            if game.map.items == []:
                self.win = True
                screen.state = 'win'
            else:
                self.win = False
                screen.state = 'lose'


class Position:
    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position


class Game:
    def __init__(self, player, map):
        self.player = player
        self.map = map

    def initializeGame(mapFile):
        map = Map(mapFile)
        for row in enumerate(map.map_elements):
            for cell in enumerate(row[1]):
                if cell[1] == 'S':
                    player = Player(cell[0], row[0], [], '1')
        return Game(player, map)


class Item:
    def __init__(self, x_position, y_position, name, image):
        self.position = (Position(x_position, y_position))
        self.name = name
        self.image = image


class Map:
    def __init__(self, map_file):
        self.map_file = map_file
        self.background = pygame.image.load(
            r'images\Menus\game_background.png')
        self.floor_image = pygame.transform.scale(
            pygame.image.load(r'images\floor.png'), (45, 45))
        self.wall_image = pygame.transform.scale(
            pygame.image.load(r'images\wall.png'), (45, 45))
        self.exit_image = pygame.transform.scale(
            pygame.image.load(r'images\Gardien.png'), (45, 45))
        self.elements_ref = {
            '1': (
                False, self.wall_image), '0': (
                True, self.floor_image), 'S': (
                True, self.floor_image), 'E': (
                    True, self.exit_image)}

        def create_items(self):
            items_list = listdir('images/items')
            items_positions = []
            (lambda __y,
             __g: [(lambda __sentinel,
                    __after,
                    __items: __y(lambda __this: lambda: (lambda __i: [[[(lambda __after: __y(lambda __this: lambda: [[__this() for __g['y'] in [(randrange(0,
                                                                                                                                                           14))]][0] for __g['x'] in [(randrange(0,
                                                                                                                                                                                                 14))]][0] if (not self.elements_ref[self.check_position(x,
                                                                                                                                                                                                                                                         y)][0]) else __after())())(lambda: (items_positions.append((x,
                                                                                                                                                                                                                                                                                                                     y)),
                                                                                                                                                                                                                                                                                             __this())[1]) for __g['y'] in [(randrange(0,
                                                                                                                                                                                                                                                                                                                                       14))]][0] for __g['x'] in [(randrange(0,
                                                                                                                                                                                                                                                                                                                                                                             14))]][0] for __g['item'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    __sentinel)))())([],
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     lambda: None,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     iter(range(len(items_list)))) for __g['items_positions'] in [([])]][0])((lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))),
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             globals())
            items = []
            for item in range(len(items_positions)):
                position = items_positions.pop()
                selected_item = items_list.pop()
                items.append(Item(position[0], position[1], selected_item[:-4], pygame.transform.scale(
                    pygame.image.load(r'images/items/' + selected_item), (45, 45))))
            return items

        def formatTxt(file):
            mapTxt = open(file, 'r').readlines()
            for i in range(len(mapTxt) - 1):
                mapTxt[i] = mapTxt[i][:-1]
            mapTxt = list(filter(lambda x: x != '', mapTxt))
            for i in range(len(mapTxt)):
                mapTxt[i] = list(filter(lambda x: x != ' ', mapTxt[i]))
            return mapTxt

        self.map_elements = formatTxt(self.map_file)
        self.items = create_items(self)

    def check_position(self, x, y):
        return self.map_elements[y][x]

    def available_position(self, x, y,):
        if 0 <= x < len(self.map_elements) and 0 <= y < len(
                self.map_elements) and self.elements_ref[self.check_position(x, y)][0]:
            return True


class Screen:
    def __init__(self):
        self.height = 675
        self.width = 675
        self.element_ratio = self.width / 15
        self.main_menu_background = pygame.image.load(
            r'images\Menus\main_menu2.png')
        self.settings_menu_background = pygame.image.load(
            r'images\Menus\settings_menu.png')
        self.win_menu_background = pygame.image.load(r'images\Menus\win.png')
        self.lose_menu_background = pygame.image.load(r'images\Menus\lose.png')
        self.inventory_menu_background = pygame.image.load(
            r'images\Menus\inventory2.png')
        self.characters = [character[:-4]
                           for character in listdir('images/characters')]
        self.selected_character = '1'
        self.window = pygame.display.set_mode([self.width, self.height])
        self.state = 'main'
        self.sound = True

    def handleClick(self, cursor):
        if self.state == 'main':
            if 218 < cursor[0] < 456 and 207 < cursor[1] < 293:
                self.state = 'game'
                return 'game'
            if 218 < cursor[0] < 456 and 378 < cursor[1] < 464:
                self.state = 'settings'
                return 'settings'
        elif self.state == 'settings':
            if 400 < cursor[0] < 440 and 267 < cursor[1] < 295:
                if not self.characters.index(
                        self.selected_character) == len(
                        self.characters) - 1:
                    self.selected_character = self.characters[self.characters.index(
                        self.selected_character) + 1]
            if 230 < cursor[0] < 270 and 267 < cursor[1] < 295:
                if self.characters.index(self.selected_character) != 0:
                    self.selected_character = self.characters[self.characters.index(
                        self.selected_character) - 1]
            if 280 < cursor[0] < 390 and 559 < cursor[1] < 604:
                self.state = 'main'
                return 'main'
            if 305 < cursor[0] < 369 and 410 < cursor[1] < 470:
                if self.sound:
                    self.settings_menu_background = pygame.image.load(
                        r'images\Menus\settings_menu_no_sound.png')
                else:
                    self.settings_menu_background = pygame.image.load(
                        r'images\Menus\settings_menu.png')
                self.sound = not self.sound
        elif self.state == 'win':
            if 230 < cursor[0] < 443 and 369 < cursor[1] < 417:
                self.state = 'game'
                return 'game'
            if 230 < cursor[0] < 443 and 446 < cursor[1] < 492:
                self.state = 'main'
                return 'main'
        elif self.state == 'lose':
            if 230 < cursor[0] < 443 and 312 < cursor[1] < 362:
                self.state = 'game'
                return 'game'
            if 230 < cursor[0] < 443 and 388 < cursor[1] < 438:
                self.state = 'main'
                return 'main'

    def main_screen(self):
        self.window.blit(self.main_menu_background, (0, 0))

    def win_screen(self):
        self.window.blit(self.win_menu_background, (0, 0))

    def lose_screen(self):
        self.window.blit(self.lose_menu_background, (0, 0))

    def settings_screen(self):
        self.window.blit(self.settings_menu_background, (0, 0))
        self.window.blit(
            pygame.transform.scale(
                pygame.image.load(
                    r'images/characters/' +
                    self.selected_character +
                    '.png'),
                (45,
                 45)),
            (self.width /
             2 -
             self.element_ratio /
             2,
             263))

    def fade(self, window):
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 150):
            fade_surface.set_alpha(alpha)
            fading = window.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)

    def displayElement(self, x, y, map):

        self.window.blit(map.elements_ref[map.check_position(
            x, y)][1], (x * self.element_ratio, y * self.element_ratio))

    def displayPlayer(self, player):
        self.window.blit(
            pygame.transform.scale(
                pygame.image.load(
                    r'images/characters/' +
                    self.selected_character +
                    '.png'),
                (45,
                 45)),
            (player.position.x *
             self.element_ratio,
             player.position.y *
             self.element_ratio))

    def displayItem(self, item):
        self.window.blit(
            item.image,
            (item.position.x *
             self.element_ratio,
             item.position.y *
             self.element_ratio))

    def displayInventory(self, inventory):
        inventory_window_x = self.width / 2 - \
            self.inventory_menu_background.get_width() / 2
        inventory_window_y = self.height / 2 - \
            self.inventory_menu_background.get_height() / 2
        self.window.blit(self.inventory_menu_background,
                         (inventory_window_x, inventory_window_y))
        item_x = 34
        item_y = 83
        for item in enumerate(inventory):
            if item[0] > 0 and item[0] % 6 == 0:
                item_y += 64
                item_x = 34
            self.window.blit(
                pygame.transform.scale(
                    item[1].image,
                    (36,
                     35)),
                (inventory_window_x +
                 item_x,
                 inventory_window_y +
                 item_y))
            item_x += 65
