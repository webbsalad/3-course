class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.0  # Уменьшил скорость корабля
        self.ship_limit = 3
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.alien_speed_factor = 0.3  # Уменьшил скорость инопланетян
        self.fleet_drop_speed = 5  # Уменьшил скорость спуска
        self.fleet_direction = 1
        self.alien_width = 40
        self.alien_height = 30
        self.alien_color = (0, 255, 0)
        self.ship_width = 50
        self.ship_height = 30
        self.ship_color = (0, 0, 255)
