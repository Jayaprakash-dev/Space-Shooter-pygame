import pygame


class SpaceShip(pygame.sprite.Sprite):
    """ Base Class for player ship and enemy ship """

    def __init__(self, game, ship_img, scale=None) -> None:

        super().__init__()
        self.game = game

        self.game_display = game.main_surface

        self.settings = game.settings

        self.surface_width = game.main_surface.get_width()
        self.surface_height = game.main_surface.get_height()

        self.display_rect = self.game_display.get_rect()

        self.image = pygame.image.load(ship_img)

        if scale is not None:
            self.image = pygame.transform.scale(self.image, scale)
            
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        self._moving_up = False
        self._moving_down = False
        self._moving_right = False
        self._moving_left = False

        self.shooter = None

    def span_ship(self):
        self.__draw()

    def __draw(self):
        # pygame.draw.rect(self.game_display, (0,0,255), self.ship_rect)
        self.game_display.blit(self.image, self.rect)

    def move_up(self, speed):
        if self._moving_up:
            self.rect.y -= int(speed)

    def move_down(self, speed):
        if self._moving_down:
            self.rect.y += int(speed)



