import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage the game assets and behavior"""

    def __init__(self):
        '''Initializes the game, and creates the game's resources'''
        

        self._check_events()
        

        pygame.init()
        self.settings = Settings()
        self.background = pygame.image.load('galaxy.jpg')
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
      

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()



    def run_game(self):
        '''Starts the main loop for the game'''
        while True:
            self._check_events()
            self.ship.update() 
            self.bullets.update()
            self._update_bullets()
           
            

        
            print(len(self.bullets))

            self._update_screen() #must always be at the end
            
    
    def _check_events(self):
        """Responds to keypresses and events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:#when keys are pressed down
                    self._check_keydown_events(event)    
                elif event.type == pygame.KEYUP:#when keys are released
                    self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            

    def _update_bullets(self):
        """Update positin of bullets and get rid of old bullets."""
        self.bullets.update()

        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        '''Update images on the screen, and flip to the new screen'''
        
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.background, (0,0))
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()  #always shows up at the end of update screen function

            
        
if __name__ == '__main__':
    #Makes an instance of the game, and runs.
    pygame.init()
    ai = AlienInvasion()
    ai.run_game()