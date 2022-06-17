import pygame


class GameHitsAnimation:

    def __init__(self, surface):

        self.surface = surface

        self.count = 10
        font_file = "./assets/fonts/SpaceMission.otf"
        self.font_color = None

        self.font = pygame.font.Font(font_file, 32)

        self.hits_font = None
        self.y = 400
        self.x = 0

        self.animation_speed = 0

    def set_anim(self, val, symbol):

        if symbol == '-':
            self.x = 50
            self.font_color = (255, 0, 0)

        elif symbol == '+':
            self.x = 950
            self.font_color = (51, 255, 51)

        hits_font = self.font.render(symbol + str(val), True, self.font_color)
        self.hits_font = pygame.transform.rotate(hits_font, 25)
        self.count = 0
        self.y = 400
        self.animation_speed = 0

    def animate(self):

        if self.count < 10:
            self.surface.blit(self.hits_font, (self.x, self.y))
            self.y -= 3
            self.animation_speed += 0.25
            self.count = int(self.animation_speed)
