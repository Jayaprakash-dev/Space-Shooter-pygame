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

clock = pygame.time.Clock()


class Game:

    def __init__(self) -> None:

        self.game_status = True

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

    def run(self):

        while self.game_status:

            self.events.check_events()
            self._update_display()

            clock.tick(self.settings.fps)

        self._restart_or_quit()
        pygame.quit()
        sys.exit()

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
        pass


if __name__ == "__main__":

    game = Game()

    while game.game_status:
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
 