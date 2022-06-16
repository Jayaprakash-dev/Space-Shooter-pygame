import pygame


class PlayerUI:

    def __init__(self, game):
        self.game = game

        self.player_health = game.settings.player_health
        self.enemy_health = game.settings.enemy_health

        self.wrapper_rect_width = 200
        self.wrapper_rect_height = 25

        self.health_bar_height = 23

        self.health_bar_color = (0, 255, 0)

        self.wrapper_rect_pos = (860, 20)
        self.health_bar_pos = (860.6, 21)

        self.score = 0
        self.score_font = pygame.font.SysFont('arial', 20)

    def update_player_health(self, val=0):

        self.player_health -= val

        if self.player_health > 40:
            self.health_bar_color = (0, 255, 0)

        if self.player_health <= 40:
            self.health_bar_color = (255, 153, 51)

        if self.player_health <= 17:
            self.health_bar_color = (255, 0, 0)

        self._draw()

    def update_enemy_health(self, sprite, val=0):

        if sprite.ship_num == 1:
            self.enemy_health -= (val * 4)

        elif sprite.ship_num == 2:
            self.enemy_health -= (val * 2)

        elif sprite.ship_num == 3:
            self.enemy_health -= (val * 1.34)

        elif sprite.ship_num == 4:
            self.enemy_health -= val

    def update_player_score(self):
        self.score += 15

    def _draw(self):

        # wrapper rect for player health bar
        wrapper_bar_rect = pygame.Rect(
            self.wrapper_rect_pos, (self.wrapper_rect_width, self.wrapper_rect_height))

        pygame.draw.rect(self.game.main_surface, (255, 255, 255),
                         wrapper_bar_rect, width=1, border_radius=10)

        # player health bar
        health_bar_rect = pygame.Rect(self.health_bar_pos, ((
                                                                    self.player_health * 2), self.health_bar_height))

        pygame.draw.rect(self.game.main_surface, self.health_bar_color,
                         health_bar_rect, border_radius=10)

        # player score
        x = (self.game.main_surface.get_width() / 2) - 8
        self.s_font = self.score_font.render("score: " + str(self.score),
                                             True, (255, 255, 255))
        self.game.main_surface.blit(self.s_font, (x, 17))
