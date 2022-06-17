import pygame

from playership import PlayerShip


class Events:

    def __init__(self, game):
        self.game = game
        self.player_ship = PlayerShip.get_instance()

        self.playerUI = game.playerUI

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.game_status = False

            if event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)

            if event.type == pygame.KEYUP:
                self._check_key_up_events(event)

    def _check_key_down_events(self, e):
        if e.key == pygame.K_UP:
            self.player_ship._moving_up = True

        elif e.key == pygame.K_DOWN:
            self.player_ship._moving_down = True

        elif e.key == pygame.K_LEFT:
            self.player_ship._moving_left = True

        elif e.key == pygame.K_RIGHT:
            self.player_ship._moving_right = True

        elif e.key == pygame.K_SPACE:
            self.game.load_shooter_of_player_ship()

    def _check_key_up_events(self, e):
        if e.key == pygame.K_UP:
            self.player_ship._moving_up = False

        elif e.key == pygame.K_DOWN:
            self.player_ship._moving_down = False

        elif e.key == pygame.K_LEFT:
            self.player_ship._moving_left = False

        elif e.key == pygame.K_RIGHT:
            self.player_ship._moving_right = False

    def check_ship_collision(self, enemy_ship, player_ship, sprites_grp):

        if enemy_ship.rect.colliderect(player_ship.rect):
            pos = pygame.sprite.collide_mask(enemy_ship, player_ship)

            if pos is not None:
                x, y = Events.calculate_pos(pos, player_ship.rect)
                self.game.expl.pos = (x, y)
                self.game.expl.animation = True
                sprites_grp.remove(enemy_ship)

                if enemy_ship.ship_level == 4:
                    self.playerUI.update_player_health(100)
                    self.playerUI.set_anim(100)
                elif enemy_ship.ship_level == 3:
                    self.playerUI.update_player_health(50)
                    self.playerUI.set_anim(50)
                elif enemy_ship.ship_level == 2 or enemy_ship.ship_level == 1:
                    self.playerUI.update_player_health(30)
                    self.playerUI.set_anim(30)

    def check_missile_collision(self, bullet, ship_sprites_grp, bullet_sprites_grp):

        for sprite in ship_sprites_grp:
            if bullet.rect.colliderect(sprite.rect):
                pos = pygame.sprite.collide_mask(bullet, sprite)

                if pos is not None:
                    x, y = Events.calculate_pos(pos, sprite.rect)
                    self.game.expl.pos = (x, y)
                    self.game.expl.animation = True
                    bullet_sprites_grp.remove(bullet)

                    if str(sprite) == "player_ship":

                        if self.game.settings.difficulty == 'h':
                            self.playerUI.update_player_health(20)
                            self.playerUI.set_anim(20)
                        else:
                            self.playerUI.update_player_health(15)
                            self.playerUI.set_anim(15)

                    elif str(sprite) == "enemy_ship":
                        sprite.update_health(25)

                        if sprite.health <= 0:
                            ship_sprites_grp.remove(sprite)

                        self.playerUI.update_player_score(self.game.settings.score)
                        self.game.ga_anim.set_anim(self.game.settings.score, '+')

    @staticmethod
    def calculate_pos(pos, rect):
        x = rect.x - pos[0]
        y = rect.y - pos[1]
        x += 20
        y += 40

        return x, y
