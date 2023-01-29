
class Settings:
    
    def __init__(self):
        '''Initializes the game's default settings'''
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (250,60,60)
        self.bullets_allowed = 3

        #Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #alien settings
        self.alien_speed = .7
        self.fleet_drop_speed = 10


        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
    

    

