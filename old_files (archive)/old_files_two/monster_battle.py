import time
import copy
from random import randint
from random import choice

class RandomMonster():
	"""create a monster object"""

	def __init__(self):
		self.hp = randint(1,5)
	

	def make_rand_monster(self):


# use choice() to randomly select a monster from list
possible_monsters = []


current_monster = possible_monsters.choice()

def battle_main(player, monster):
	"""the main outer function that executes a battle with a monster"""


class BackInfo():
	"""object to track game settings not accessible to player"""

	# a reference to game settings that get modified as the game progresses, resulting in other
	# changes such as monsters becoming more difficult, treasure being worth more, etc.

	def __init__(self):
		"""default values for various game settings that will update progressively"""
		self.floor_level = 1
		self.monster_difficulty = 1
		self.treasure_value = 3

	def monster_diff_increase(self):

	def treasture_val_increase(self):



