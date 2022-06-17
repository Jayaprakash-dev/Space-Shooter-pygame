import random
import time
from abc import ABC

from enemyship import EnemyShip


class Level(ABC):
    _ship_level = 1
    start = time.time()
    prev_time = 0
    interval = 0.0

    _scale = {
        "level_1_ship": (90, 90),
        "level_2_ship": (100, 100),
        "level_3_ship": (120, 120),
        "level_4_ship": (120, 120)
    }

    ship_level_list_1 = None
    ship_level_list_2 = None

    @staticmethod
    def _load_ship_count(game):
        current_time = float(str(time.time() - Level.start)[:3])

        if current_time == (Level.prev_time + Level.interval):
            game.settings.enemy_ship_count += 1
            Level.prev_time += Level.interval

    @staticmethod
    def _load_ship_pros(ship_level, ship_speed_limit, game):
        scale = Level._scale[f"level_{ship_level}_ship"]
        game.settings.player_ship_speed = ship_speed_limit[f"level_{ship_level}"][0]
        game.settings.enemy_ship_speed = ship_speed_limit[f"level_{ship_level}"][1]

        return scale

    @staticmethod
    def create_level(game, ship_creation_limit, ship_speed_limit):
        scale = 0

        Level._load_ship_count(game)

        # limit for level 1 ship creation
        if ship_creation_limit["level_1"][0] <= game.playerUI.score <= ship_creation_limit["level_1"][1]:
            game.settings.player_missile_count = 5

            Level._ship_level = 1

            scale = Level._load_ship_pros(1, ship_speed_limit, game)

        # limit for level 2 ship creation
        elif ship_creation_limit["level_2"][0] < game.playerUI.score <= ship_creation_limit["level_2"][1]:
            game.settings.player_missile_count = 7

            Level._ship_level = 2
            scale = Level._load_ship_pros(2, ship_speed_limit, game)

        # limit for level 3 ship creation
        elif ship_creation_limit["level_3"][0] < game.playerUI.score <= ship_creation_limit["level_3"][1]:

            game.settings.player_missile_count = 9

            if Level.ship_level_list_2 is not None:
                Level._ship_level = random.choice(Level.ship_level_list_1)
                scale = Level._load_ship_pros(Level._ship_level, ship_speed_limit, game)

            else:
                Level._ship_level = 3
                scale = Level._load_ship_pros(Level._ship_level, ship_speed_limit, game)

        # limit for level 4 ship creation
        elif ship_creation_limit["level_4"][0] < game.playerUI.score <= ship_creation_limit["level_4"][1]:

            if Level.ship_level_list_2 is not None:
                Level._ship_level = random.choice(Level.ship_level_list_2)
                scale = Level._load_ship_pros(Level._ship_level, ship_speed_limit, game)
            else:
                Level._ship_level = 4
                scale = Level._load_ship_pros(Level._ship_level, ship_speed_limit, game)

        elif game.playerUI.score > ship_creation_limit["last"]:

            Level._ship_level = random.randrange(1, 5)

            if Level._ship_level == 1:
                scale = Level._load_ship_pros(Level._ship_level, ship_speed_limit, game)
            elif Level._ship_level == 2:
                scale = Level._load_ship_pros(Level._ship_level, ship_speed_limit, game)
            elif Level._ship_level == 3 or Level._ship_level == 4:
                scale = Level._load_ship_pros(3, ship_speed_limit, game)

        if len(game.enemy_ships) < game.settings.enemy_ship_count:
            game.enemy_ships.add(EnemyShip(game, Level._ship_level, scale=scale))

    @staticmethod
    def reduce_score(game, limit_val, ship_count, score):
        symbol = '-'

        if game.playerUI.score > limit_val:
            if game.e_ship_passed_count > ship_count:
                game.playerUI.update_player_score(-score)
                game.e_ship_passed_count = 0
                game.ga_anim.set_anim(score, symbol)


class Easy(Level):

    @staticmethod
    def load_level(game):
        Level.interval = 26.0

        ship_creation_limit = {
            "level_1": (0, 400),
            "level_2": (400, 1000),
            "level_3": (800, 2000),
            "level_4": (2000, 3000),
            "last": 3000,
        }

        ship_speed_limit = {
            "level_1": (5, 5),
            "level_2": (6, 5),
            "level_3": (4, 3),
            "level_4": (4, 2),
        }

        Easy.create_level(game, ship_creation_limit, ship_speed_limit)


class Medium(Level):

    @staticmethod
    def load_level(game):
        Level.ship_level_list_1 = [1, 2]
        Level.ship_level_list_2 = [3, 4]

        Level.interval = 22.0

        ship_creation_limit = {
            "level_1": (0, 300),
            "level_2": (300, 800),
            "level_3": (800, 2000),
            "level_4": (2000, 3000),
            "last": 3000,
        }

        ship_speed_limit = {
            "level_1": (5, 5),
            "level_2": (6, 4),
            "level_3": (4, 3),
            "level_4": (4, 2),
        }

        Level.create_level(game, ship_creation_limit, ship_speed_limit)


class Hard(Medium):

    @staticmethod
    def load_level(game):
        Medium.load_level(game)


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
            Easy.load_level(self.game)

        elif level_type == 'm':
            Medium.load_level(self.game)
            Medium.reduce_score(self.game, 15, 6, 5)

        elif level_type == 'h':
            Hard.load_level(self.game)
            Hard.reduce_score(self.game, 10, 5, 10)
