import pygame


class Shooter(pygame.sprite.Sprite):

    def __init__(self, game) -> None:

        pygame.sprite.Sprite.__init__(self)

        self.missile_folder = "./assets/images/PNG/Missile/"
        self.image = None
        self.scale = None
        self.rect = None

        self.direction = "up"

        self.game = game

        self.game_display = game.main_surface

    def create_missile(self, ship_rect):
        self.rect.centerx = ship_rect.centerx
        self.rect.centery = ship_rect.centery

    def span(self):
        # pygame.draw.rect(self.game_display, (0,0,255), self.missile_rect)
        self.game_display.blit(self.image, self.rect)

    def update(self):

        if self.direction == "up":
            self.rect.y -= self.game.settings.player_bullet_speed

        elif self.direction == "down":
            self.rect.y += self.game.settings.enemy_bullet_speed

