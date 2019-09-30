class Grid():

	def __init__(self, player):
		self.row = 5
		self.col = 5
		self.grid = self.create_grid()
		self.player = player

	def create_grid(self):

		grid = [[' * ' for x in range (self.col)] for y in range(self.row)]
		return grid

	def update_grid(self):
		"""looks at player coords to update grid graphics accordingly"""
		self.grid[self.player.player_coords[0]][self.player.player_coords[1]] = ' X '
		self.grid[self.player.previous_coords[0]][self.player.previous_coords[1]] = ' * '

	def print_grid(self):
		"""simply prints the grid"""

		for row in self.grid:
			for col in row:
				print(col, end='')
			print()

class Player():

	def __init__(self):
		self.player_coords = [0,0]
		self.previous_coords = []

	def get_move_direction(self):

		msg = '\nEnter direction to move (N,S,E,W) or Q to Quit: '
		choice = input(msg).upper()
		return choice

	def compute_move_coords(self, direction_choice):
		"""modify player_coords attribute based on direction_choice"""
		self.previous_coords = self.player_coords.copy()

		possible_choices = ['N','S','E','W','Q']

		if direction_choice not in possible_choices:
			print('You did not enter a valid direction, try again.\n')
			return False

		elif direction_choice == 'N' and self.player_coords[0] > 0:
			self.player_coords[0] -= 1
		elif direction_choice == 'S' and self.player_coords[0] < 4:
			self.player_coords[0] += 1
		elif direction_choice == 'E' and self.player_coords[1] < 4:
			self.player_coords[1] += 1
		elif direction_choice == 'W' and self.player_coords[1] > 0:
			self.player_coords[1] -= 1
		else:
			print('Sorry, you\'ve hit a boundary and can\'t proceed that way!\n')
			return False # this is what was missing in this copy and why it was broken
						 # it MUST return false so update_grid DOES NOT occur in a 
						 # boundary collision scenario
		print('\n')
		return True

player = Player()
grid = Grid(player)

game_active = True

print("\033[H\033[J")
print('Welcome to the Dungeon!\n')

# initial grid print with initial player location
# once the while loop starts, screen is cleared, board and player are
# reprinted again and again

grid.grid[0][0] = ' X '
grid.print_grid()

while game_active:
	direction_choice = player.get_move_direction()
	if direction_choice == 'Q':
		break

	print("\033[H\033[J")	# clear the screen

	if player.compute_move_coords(direction_choice):
		grid.update_grid()

	grid.print_grid()

print('\nThanks for playing!')
print()



























