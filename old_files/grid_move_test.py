
# where does it make the most sense to always store the current location 
# variable, in the player class or the grid class ?

class Player():

	def __init__(self):

		self.player_row = 3
		self.player_col = 1

class Grid():

	def __init__(self, player):
		self.player = player
		self.col = 4
		self.row = 4
		self.grid = self.update_grid()

	def update_grid(self):

		grid = [[' * ' for x in range(self.col)] for y in range(self.row)]

		grid[self.player.player_row][self.player.player_col] = ' X '

		return grid

	def print_grid(self):

		for r in self.grid:
			for c in r:
				print(c, end='')
			print()

def player_moves(player, grid):

	# msg = 'Choose direction to move (N,S,E,W): '
	# choice = input(msg)

	choice = 'N'

	if choice.lower() == 'n':
		player.player_row -= 1


player = Player()
grid_one = Grid(player)

player.player_row = 0

# I think the problem is that self.grid is defined in instantation only...

# what needs to be updated, player location or grid info? which really matters?
# seems like only grid info matters, player location is just to get the appropriate value
# player location changes, yes, but grid needs a function to update itself
# based on the new value of player location... this can't be part of the 
# class object construction, which only happens on instantiation... needs to be a
# a separate function





