import random
import time
from abc import ABC

from enemyship import EnemyShip


class Level(ABC):
    ship_level = 1
    start = time.time()
    respan_time = 0
    interval = 20.0
    scale = (100, 100)

    @staticmethod
    def load_ship_count(game):
        current_time = float(str(time.time() - Easy.start)[:3])

        if current_time == (Easy.respan_time + Easy.interval):
            game.settings.enemy_ship_count += 1
            Easy.respan_time += Easy.interval

    @staticmethod
    def create_level(game):
        pass


class Easy(Level):

    @staticmethod
    def create_level(game):

        Level.load_ship_count(game)

        if 250 < game.playerUI.score <= 500:
            Level.scale = (90, 90)
            game.settings.player_missile_count = 5
            Easy.ship_level = 2

            game.settings.player_ship_speed = 6
            game.settings.enemy_ship_speed = 5

        elif 500 < game.playerUI.score <= 1000:
            Easy.interval = 25.0
            Level.scale = (110, 110)
            game.settings.player_missile_count = 7
            Easy.ship_level = 3

            game.settings.player_ship_speed = 4
            game.settings.enemy_ship_speed = 2

        elif game.playerUI.score > 1000:
            Easy.interval = 30.0
            Level.scale = (125, 125)
            game.settings.player_missile_count = 10
            Easy.ship_level = 4

            game.settings.player_ship_speed = 4
            game.settings.enemy_ship_speed = 1

        if len(game.enemy_ships) < game.settings.enemy_ship_count:
            game.enemy_ships.add(EnemyShip(game, Easy.ship_level, scale=Level.scale))


class Medium(Level):

    @staticmethod
    def create_level(game):

        ship_level_list__1 = [1, 2]
        ship_level_list__2 = [3, 4]

        Level.load_ship_count(game)

        if game.playerUI.score <= 300:
            Level.scale = (90, 90)
            game.settings.player_missile_count = 5
            Easy.ship_level = 1

            game.settings.player_ship_speed = 5
            game.settings.enemy_ship_speed = 4

        elif 300 < game.playerUI.score <= 1200:
            Easy.interval = 25.0
            Level.scale = (100, 100)
            game.settings.player_missile_count = 7
            Easy.ship_level = random.choice(ship_level_list__1)

            game.settings.player_ship_speed = 5
            game.settings.enemy_ship_speed = 5

        elif game.playerUI.score > 1200:
            Easy.interval = 30.0
            Level.scale = (120, 120)
            game.settings.player_missile_count = 10
            Easy.ship_level = random.choice(ship_level_list__2)

            game.settings.player_ship_speed = 4
            game.settings.enemy_ship_speed = 2

        if len(game.enemy_ships) < game.settings.enemy_ship_count:
            game.enemy_ships.add(EnemyShip(game, Easy.ship_level, scale=Level.scale))


class GameLayout:

    """ This class creates basic layout or pattern for the game """
    def __init__(self, game) -> None:
        self.game = game

    def set_level(self, level_type):

        """ sets the game level based on its level_type
        1. e - Easy Level
        2. m - Medium Level
        3. h - Hard Level """

        if level_type == 'e':
            Easy.create_level(self.game)

        elif level_type == 'm':
            Medium.create_level(self.game)
