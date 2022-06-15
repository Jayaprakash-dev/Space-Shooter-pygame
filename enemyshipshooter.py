import pygame

from shooter import Shooter


class EnemyShipShooter(Shooter):

    def __init__(self, game) -> None:
        super().__init__(game)

        self.game = game
        self.color = None

        self.direction = "down"
        self.scale = (20, 27)

        self.image = pygame.image.load("./assets/images/PNG/Missile/Missile_02.png")
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()

