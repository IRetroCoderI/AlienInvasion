import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep

class AlienInvasion:
    """Overall class to manage the game assets and behavior"""

    def __init__(self):
        '''Initializes the game, and creates the game's resources'''
        self._check_events()#always checking for events
        

        pygame.init()#initializes pygame 
        self.settings = Settings()
        self.background = pygame.image.load('galaxy.jpg')
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        #create an instance of stats to store game statistics
        self.stats = GameStats(self)
      

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()



    def run_game(self):
        '''Starts the main loop for the game'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update() 
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
        

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

    def create_fleet(self):
        """Creates fleet of aliens"""
        #Create an alien and find then number of aliens in a row.
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2 *alien_width)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height)

        #Create full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)



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

        self._check_bullet_alien_collisions()
    

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.

        #checks for collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            #Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.create_fleet()


    def _update_screen(self):
        '''Update images on the screen, and flip to the new screen'''
        
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.background, (0,0))
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()  #always shows up at the end of update screen function
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_aliens(self):
        """Update the positions of all aliens in the field"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien and ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #look for aliens hittting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
            #Decrement ships_left.
            self.stats.ships_left -= 1

            #get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship.
            self.create_fleet()
            self.ship.center_ship()

            #pause
            sleep(.5)
        else:
            self.stats.game_active = False
    
    def _check_aliens_bottom(self):
        """Checks if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit
                self._ship_hit()
                break
            
        
if __name__ == '__main__':
    #Makes an instance of the game, and runs.
    pygame.init()
    ai = AlienInvasion()
    ai.run_game()