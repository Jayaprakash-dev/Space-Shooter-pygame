from playershipshooter import PlayerShipShooter
from spaceship import SpaceShip


class PlayerShip(SpaceShip):
    __instance = None

    def __init__(self, game) -> None:
        self.player_ship_img = "./assets/images/PNG/SpaceShip/PlayerShip/Ship__1.png"

        super().__init__(game, self.player_ship_img)

        self.rect.x, self.rect.y = 550, 680

        if PlayerShip.__instance is None:
            PlayerShip.__instance = self

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def move(self):

        # moving in up & down direction condition
        if self.rect.midbottom[1] <= self.surface_height:
            super().move_down(self.game.settings.player_ship_speed)

        if self.rect.midtop[1] > 1:
            super().move_up(self.game.settings.player_ship_speed)

        # moving in left & right direction condition
        if self.rect.topright[0] < self.surface_width:
            if self._moving_right:
                self.rect.x += self.settings.player_ship_speed

        if self.rect.x > 0:
            if self._moving_left:
                self.rect.x -= self.settings.player_ship_speed

    def shoot(self, missile_type):
        self.shooter = PlayerShipShooter(self.game, missile_type)
        self.shooter.create_missile(self.rect)

        return self.shooter

    def set_spaceship(self):
        self.rect.x, self.rect.y = 550, 680
        self._moving_up = False
        self._moving_down = False
        self._moving_right = False
        self._moving_left = False


    def __str__(self):
        return "player_ship"
