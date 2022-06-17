import pygame


class PlayerUI:

    def __init__(self, game):

        self.game = game

        self.player_health = 100
        self.enemy_health = game.settings.enemy_health

        self.wrapper_rect_width = 200
        self.wrapper_rect_height = 25

        self.health_bar_height = 23

        self.health_bar_color = (0, 255, 0)

        self.wrapper_rect_pos = (860, 20)
        self.health_bar_pos = (860.8, 21)

        self.score = 0
        self.score_font = pygame.font.SysFont('arial', 20)

        self.count = 20

        font_file = "./assets/fonts/SpaceMission.otf"
        self.font_color = (255, 0, 0)
        self.font = pygame.font.Font(font_file, 25)
        self.anim_font = None
        self.x = 880
        self.y = 50

    def update_player_health(self, val=0):

        self.player_health -= val
        if self.player_health > 4:

            if self.player_health > 40:
                self.health_bar_color = (0, 255, 0)

            if 17 < self.player_health <= 40:
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

    def update_player_score(self, val):
        self.score += val

    def _draw(self):

        # wrapper rect for player health bar
        wrapper_bar_rect = pygame.Rect(
            self.wrapper_rect_pos, (self.wrapper_rect_width, self.wrapper_rect_height))

        pygame.draw.rect(self.game.main_surface, (255, 255, 255), wrapper_bar_rect, width=1)

        # player health bar
        health_bar_rect = pygame.Rect(self.health_bar_pos, ((self.player_health * 2), self.health_bar_height))

        pygame.draw.rect(self.game.main_surface, self.health_bar_color, health_bar_rect)

        # player score
        x = (self.game.main_surface.get_width() / 2) - 8
        self.s_font = self.score_font.render("score: " + str(self.score), True, (255, 255, 255))
        self.game.main_surface.blit(self.s_font, (x, 17))

    def set_anim(self, val):

        symbol = '- '

        self.anim_font = self.font.render(symbol + str(val), True, self.font_color)
        self.count = 0

    def animate_health_val(self):

        if self.count < 20:
            self.game.main_surface.blit(self.anim_font, (self.x, self.y))
            self.count += 1
