import random
import sys

import pygame

from events import Events
from explosion import ExplosionGroup
from gamelayout import GameLayout
from playership import PlayerShip
from settings import Settings
from playerUI import PlayerUI
from mainUI import MainUI
from playerlife import PlayerLife

clock = pygame.time.Clock()


class Game:

    def __init__(self) -> None:

        self.main_screen = True
        self.game_status = False
        self.quit = False

        self.settings = Settings()

        pygame.init()
        self.main_surface = pygame.display.set_mode(self.settings.display_size)
        pygame.display.set_caption("SpaceShooter")

        self.player_ship = PlayerShip(self)
        self.player_ship_grp = pygame.sprite.GroupSingle()
        self.player_ship_grp.add(self.player_ship)

        self.player_ship_missiles = pygame.sprite.Group()

        self.enemy_ships = pygame.sprite.Group()
        self.enemy_ship_missiles = pygame.sprite.Group()

        self.playerUI = PlayerUI(self)

        self.events = Events(self)

        self.game_layout = GameLayout(self)

        self.expl = ExplosionGroup()
        self.expl_grp = pygame.sprite.Group()
        self.expl_grp.add(self.expl)

        self.mainUI = MainUI()

        # self.life_list = [PlayerLife(self, (20, 17)), PlayerLife(self, (70, 17)), PlayerLife(self, (120, 17))]
        self.life_list = [PlayerLife(self, (20, 17))]
    def run(self):

        while self.quit is not True:
            if self.game_status == True:
                self.events.check_events()
                self._update_display()

                clock.tick(self.settings.fps)

            else:
                self._restart_or_quit()

    def _update_display(self):
        self.main_surface.fill((0, 0, 0))

        self.game_layout.set_level('m')

        self.player_ship_missiles.update()
        self.enemy_ship_missiles.update()

        for missile in self.player_ship_missiles:
            missile.span()

            self.events.check_missile_collision(missile, self.enemy_ships, self.player_ship_missiles)

            if missile.rect.midbottom[1] < 0:
                self.player_ship_missiles.remove(missile)

        for missile in self.enemy_ship_missiles: 
            missile.span()

            self.events.check_missile_collision(missile, self.player_ship_grp, self.enemy_ship_missiles)

            if missile.rect.midtop[1] > self.main_surface.get_height():
                self.enemy_ship_missiles.remove(missile)

        for ship in self.enemy_ships:
            ship.span_ship()
            ship.move()
            self._load_enemy_ship_missiles(ship)

            self.events.check_ship_collision(ship, self.player_ship, self.enemy_ships)

            if ship.rect.midtop[1] > (self.main_surface.get_height() + 2):
                self.enemy_ships.remove(ship)

        self.player_ship.span_ship()
        self.player_ship.move()

        self.expl_grp.update(self.main_surface)

        self.playerUI.update_player_health()

        for life in self.life_list:
            life.draw()

        self._check_life_of_player()

        pygame.display.update()

    def load_shooter_of_player_ship(self):
        if len(self.player_ship_missiles) < self.settings.player_missile_count:
            self.player_ship_missiles.add(
                self.player_ship.shoot("BasicMissile"))

    def _load_enemy_ship_missiles(self, ship):
        interval = random.randrange(0, 120)

        if interval == 1:
            self.enemy_ship_missiles.add(ship.shoot())

    def _restart_or_quit(self):

        color = (255, 255, 255)

        font_file = "./assets/fonts/SpaceMission.otf"
        font_color = (255, 255, 255)

        s_font = pygame.font.Font(font_file, 35)
        score_font = s_font.render("Game Score: " + str(self.playerUI.score), True, (0, 0, 0))

        menu_font = pygame.font.Font(font_file, 35)
        pa_font = menu_font.render("Play Again", True, font_color)
        q_font = menu_font.render("Quit", True, font_color)

        width, height = 500, 300
        pos = (((self.main_surface.get_width() / 2) / 2) + 15, 320)
        main_rect = pygame.Rect(pos, (width, height))
        pa_rect = pygame.Rect((main_rect.left + 150, main_rect.top + 100), (215, 48))
        q_rect = pygame.Rect((main_rect.left + 150, pa_rect.bottom + 50), (215, 48))

        pygame.draw.rect(self.main_surface, color, main_rect, border_radius=10)
        pygame.draw.rect(self.main_surface, (0, 0, 0), pa_rect, border_top_left_radius=12, border_bottom_right_radius=12)
        pygame.draw.rect(self.main_surface, (0, 0, 0), q_rect, border_top_left_radius=12, border_bottom_right_radius=12)

        self.main_surface.blit(score_font, (main_rect.x + 130, main_rect.y + 30))
        self.main_surface.blit(pa_font, (pa_rect.x + 10, pa_rect.y + 8))
        self.main_surface.blit(q_font, ((q_rect.x + ((q_rect.width // 2) // 2)) + 16, q_rect.y + 8))

        pygame.display.update()

    def _check_life_of_player(self):

        if self.playerUI.player_health <= 0:
            self.life_list.pop()
            self.playerUI.player_health = 100

        if len(self.life_list) <= 0:
            self.game_status = False


if __name__ == "__main__":

    game = Game()

    while game.main_screen:
        MainUI.show_main_board(game.main_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_status = False

            if MainUI.start_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                game.run()

            if MainUI.exit_event(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()

    # game = Game()
    # game.run()
 