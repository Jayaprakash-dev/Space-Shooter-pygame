class Settings:

    def __init__(self, difficulty) -> None:

        self.display_size = (1100, 800)

        self.fps = 60

        self.difficulty = difficulty

        # player ship properties
        self.player_ship_speed = 5

        self.player_bullet_speed = 5

        self.player_missile_count = 4

        if difficulty == 'e' or difficulty == 'm':
            self.player_lives = 3

        elif difficulty == 'h':
            self.player_lives = 2

        self.score = 15

        # enemy ship properties
        self.enemy_health = 100

        self.enemy_ship_speed = 4

        self.enemy_bullet_speed = 7

        self.enemy_ship_count = 4
