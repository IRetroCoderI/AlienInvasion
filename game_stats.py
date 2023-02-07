class GameStats:
    """ Tracks statistics for Alien Invasion gameplay"""

    def __init__(self, ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        """Start game in active state"""
        self.game_active = False #game begins in a false state until the player presses the start button

        #High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        