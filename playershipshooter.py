import pygame

from shooter import Shooter


class PlayerShipShooter(Shooter):

    def __init__(self, game, missile_type) -> None:

        super().__init__(game)

        if missile_type == "BasicMissile":
            self.img = "Missile_01.png"
            self.scale = (18, 25)

        elif missile_type == "MediumMissile":
            self.img = "Missile_02.png"
            self.scale = (20, 27)

        self.load_missile()

    def load_missile(self):
        missile_img = self.missile_folder + self.img

        self.image = pygame.image.load(missile_img)
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()
