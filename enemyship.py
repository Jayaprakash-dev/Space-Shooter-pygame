import random

from spaceship import SpaceShip
from enemyshipshooter import EnemyShipShooter


def random_pos_generator(max_value, step_value, min_value=0):
    x = random.randrange(min_value, max_value, (step_value + 5))
    return x


class EnemyShip(SpaceShip):

    def __init__(self, game, ship_num=1, scale=(100, 100)):

        self.main_folder = "./assets/images/PNG/SpaceShip/EnemyShip/"
        self.ship_level = ship_num

        self.health = 100

        self.enemy_ship_img = self.main_folder + \
            "ship_0" + str(self.ship_level) + ".png"

        SpaceShip.__init__(self, game, self.enemy_ship_img, scale)

        self.speed = self.game.settings.enemy_ship_speed

        self.rect.y = random_pos_generator(
            -250, self.rect.height, min_value=-(self.surface_height - 250))

        self.rect.x = random_pos_generator(
            (self.surface_width - 100), self.rect.width)

        self._moving_down = True

    def shoot(self):
        self.shooter = EnemyShipShooter(self.game)
        self.shooter.create_missile(self.rect)

        return self.shooter

    def move(self):

        if self.ship_level == 4:
            self.speed = 2

        return super().move_down(self.speed)

    def update_health(self, val=0):

        # updates enemy ship health based on the ship level
        if self.ship_level == 1:
            self.health -= (val * 4)

        elif self.ship_level == 2:
            self.health -= (val * 2)

        elif self.ship_level == 3:
            self.health -= (val * 1.34)

        elif self.ship_level == 4:
            self.health -= val

    def __str__(self):
        return "enemy_ship"
