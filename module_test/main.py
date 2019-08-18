from classes import *
from ui_functions import *
from gameplay_functions import *
from battle import *

settings = GameSettings()
player = Player(settings)
dice = Dice()

# call the main run_game function loop

run_game(settings, player)



