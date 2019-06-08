# log generator class and/or functions for use in deeper dungeons RPG game
from random import randint
import time


class GameLog():
	# state of GameLog will constantly update to reflect the current location on the game grid
	# and thereby represent the current room type
	# that is, game log has one 'state', and that state reflects the current room.

	def __init__(self, player, grid):
		self.room_text = ''
		self.player = player
		self.player_name = player.info['Name']	# should this access player parameter, or self.player attribute?
		self.grid = grid
		self.current_room = get_current_room()

	def get_current_room(self):
		# unfinished starting to figure this out...
		# player_coords = self.player.player_location
		# current_room = self.grid.all_rooms.
		
	def print_log(self):
		"""prints the current player log to the screen"""

		self.create_room_text()
		print("{}'s LOG:\n".format(self.player_name.upper()))
		print()
		print("{}\n".format(self.room_text))

	def create_room_text(self):
		"""prints text describing current room, based on room type"""

		if self.room == 'Empty':
			self.room_text = 'There doesn\'t appear to be anything in this room. What a relief!'

		if self.room == 'Monster':
			self.room_text = 'I think I something is in here with me...oh drat, here it comes!!!'

		if self.room == 'Treasure':
			self.room_text = 'I see something in the center of the room -- a large, ornate chest!'

player = 'Bilbo'

test_room = GameLog('Empty', player)

test_room.print_log()

