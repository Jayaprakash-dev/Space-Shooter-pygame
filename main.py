import random
import sys

import pygame
from pygame.locals import *

from events import Events
from explosion import ExplosionGroup
from gamelayout import GameLayout
from playership import PlayerShip
from settings import Settings
from playerUI import PlayerUI
from mainUI import MainUI
from playerlife import PlayerLife
from gamehits_animation import GameHitsAnimation as ga

clock = pygame.time.Clock()

main_screen = True


class Game:

    def __init__(self) -> None:

        self.game_status = True
        self.quit = False

        # It stores how many enemy ships passed over the player ship
        self.e_ship_passed_count = 0

        self.settings = Settings(difficulty)

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

        self.life_list = []

        self._load_player_life(self.settings.player_lives)

        self.ga_anim = ga(self.main_surface)

    def run(self):

        while self.quit is not True:

            if self.game_status:
                self.events.check_events()
                self._update_display()

                clock.tick(self.settings.fps)

            else:
                self._restart_or_quit()

            pygame.display.update()

        pygame.quit()
        sys.exit()

    def _update_display(self):
        self.main_surface.fill((0, 0, 0))

        self.game_layout.set_level(difficulty)

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
                self.e_ship_passed_count += 1

        self.player_ship.span_ship()
        self.player_ship.move()

        self.expl_grp.update(self.main_surface)

        self.playerUI.update_player_health()

        for life in self.life_list:
            life.draw()

        self._check_player_life()

        self.ga_anim.animate()
        self.playerUI.animate_health_val()

    def load_shooter_of_player_ship(self):
        if len(self.player_ship_missiles) < self.settings.player_missile_count:
            self.player_ship_missiles.add(
                self.player_ship.shoot("BasicMissile"))

    def _load_enemy_ship_missiles(self, ship):
        interval = random.randrange(0, 120)

        if interval == 1:
            self.enemy_ship_missiles.add(ship.shoot())

    def _load_player_life(self, num):
        x = 20
        for i in range(num):
            x += 50
            self.life_list.append(PlayerLife(self, (x, 17)))

    def _check_player_life(self):

        if self.playerUI.player_health <= 0:
            self.life_list.pop()
            self.playerUI.player_health = 100

        if len(self.life_list) == 0:
            self.game_status = False

    # asking player to quit or play again, after losing all lives
    def _restart_or_quit(self):

        bg_img = pygame.image.load("./assets/images/PNG/main_screen_bg.jpg")
        bg_img = pygame.transform.scale(bg_img, (self.main_surface.get_width(), self.main_surface.get_height()))
        self.main_surface.blit(bg_img, (0, 0))

        color = (255, 255, 255)

        font_file = "./assets/fonts/SpaceMission.otf"
        font_color = (255, 255, 255)

        s_font = pygame.font.Font(font_file, 40)
        score_font = s_font.render("Game Score: " + str(self.playerUI.score), True, (0, 0, 0))

        menu_font = pygame.font.Font(font_file, 35)
        q_font = menu_font.render("Quit", True, font_color)

        width, height = 500, 300
        pos = (((self.main_surface.get_width() / 2) / 2) + 15, 250)

        main_rect = pygame.Rect(pos, (width, height))
        pygame.draw.rect(self.main_surface, color, main_rect, border_radius=10)
        p_rect = pygame.Rect((main_rect.left + 150, main_rect.top + 100), (215, 48))
        q_rect = pygame.Rect((main_rect.left + 150, p_rect.bottom + 50), (215, 48))

        pygame.draw.rect(self.main_surface, (0, 0, 0), p_rect, border_top_left_radius=12,
                         border_bottom_right_radius=12)
        pygame.draw.rect(self.main_surface, (0, 0, 0), q_rect, border_top_left_radius=12, border_bottom_right_radius=12)

        self.main_surface.blit(score_font, (main_rect.x + 85, main_rect.y + 30))

        if len(self.life_list) != 0:
            p_font = menu_font.render("Resume", True, font_color)
            self.main_surface.blit(p_font, (p_rect.x + 45, p_rect.y + 8))
        else:
            p_font = menu_font.render("Play Again", True, font_color)
            self.main_surface.blit(p_font, (p_rect.x + 10, p_rect.y + 8))

        self.main_surface.blit(q_font, ((q_rect.x + ((q_rect.width // 2) // 2)) + 16, q_rect.y + 8))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == MOUSEBUTTONDOWN:

                if p_rect.collidepoint(pygame.mouse.get_pos()) and len(self.life_list) != 0:
                    self.game_status = True

                elif p_rect.collidepoint(pygame.mouse.get_pos()):
                    self.player_ship.set_spaceship()
                    self.player_ship_missiles.empty()
                    self.expl.animation = False
                    self.enemy_ships.empty()
                    self.enemy_ship_missiles.empty()
                    self.playerUI.player_health = 100
                    self.playerUI.score = 0
                    self.player_ship_grp.add(self.player_ship)
                    self._load_player_life(self.settings.player_lives)

                    self.game_status = True

                elif q_rect.collidepoint(pygame.mouse.get_pos()):
                    self.quit = True


if __name__ == "__main__":

    pygame.init()

    surface = pygame.display.set_mode((1100, 800))
    pygame.display.set_caption("space  shooter")

    difficulty = 'e'

    while main_screen:
        MainUI.show_main_board(surface, difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if MainUI.start_event(event):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                main_screen = False
                Game().run()

            if MainUI.exit_event(event):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_e:
                    difficulty = 'e'

                elif event.key == K_m:
                    difficulty = 'm'

                elif event.key == K_h:
                    difficulty = 'h'

                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    main_screen = False
                    Game().run()

        pygame.display.update()
