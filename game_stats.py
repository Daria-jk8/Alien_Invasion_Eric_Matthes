class GameStats():
   # Track Stats for Alien Invasion
   def __init__(self, ai_game):
    self.settings = ai_game.settings
    self.resert_stats()
    self.ships_left = self.settings.ship_limit 

    # Game Flag : Starts the game in an inactive state 
    self.game_active = False

    # High Score (should never be reset)
    self.high_score = 0

   def resert_stats(self):
       # Initialize stats that can change during the game
       self.ships_left = self.settings.ship_limit 
       self.score = 0
       self.level = 0