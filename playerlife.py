import pygame


class PlayerLife:

    def __init__(self, game, pos):

        self.game = game

        self.image = pygame.image.load("./assets/images/PNG/life.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.pos = pos

    def draw(self):
        self.game.main_surface.blit(self.image, self.pos)