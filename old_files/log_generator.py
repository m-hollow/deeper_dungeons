# log generator class and/or functions for use in deeper dungeons RPG game
from random import randint
import time

class GameLog():
	"""GameLog object always has one 'state', which reflects the current room player is in"""

	def __init__(self, player, grid):
		self.player = player
		self.grid = grid
		self.current_room_coords = self.player.player_location

		# dictionary of all possible room texts, indexed by room type

		self.room_texts = RoomBook()	# contains all the possible texts for each room
		
	def print_log(self):
		"""prints the current player log to the screen"""

		self.create_room_text()
		print("{}'s LOG:\n".format(self.player.info['Name'].upper()))
		print()
		print("{}\n".format(self.room_text))



class Player():
	def __init__(self, name):
		self.info = {'Name':name}
		self.player_location = [1,1]



player = Player('Bilbo')

test_room = GameLog('Empty', player)

test_room.print_log()

