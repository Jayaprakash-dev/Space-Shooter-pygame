import pygame


class ExplosionGroup(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image_files = []

        self.animation = False

        self.load_images()

        self.index = 0
        self.animation_speed = 0

        self.image = self.image_files[self.index]
        self.rect = self.image.get_rect()

        self.pos = None

    def load_images(self):
        path = f'./assets/images/PNG/explosion_sprites/img_'

        self.image_files = [pygame.image.load(path + str(i) + '.png') for i in range(35)]

    def update(self, surface):
        # update method should be added in main method

        if self.animation:

            if self.index >= len(self.image_files):
                self.animation = False
                self.animation_speed = 0
                self.index = 0

            if self.index < len(self.image_files):
                self.animation_speed += 1

            self.image = self.image_files[self.index]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

            self.index = int(self.animation_speed)

            self._draw(surface)

    def _draw(self, surface):
        surface.blit(self.image, self.rect.center)
