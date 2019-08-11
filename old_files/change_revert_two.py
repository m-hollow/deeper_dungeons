
class Grid():

	def __init__(self, player):
		self.row = 5
		self.col = 5
		self.grid = self.create_grid() #created on instantiation of object!
		self.player = player
		
	def create_grid(self):
		"""creates the grid, assigns it to grid attribute"""
		grid = [[' * ' for x in range(self.col)] for y in range(self.row)]
		return grid

	def update_grid(self):
		"""looks at user coords to update location of player"""
		self.grid[self.player.player_coords[0]][self.player.player_coords[1]] = ' X '
		self.grid[self.player.previous_coords[0]][self.player.previous_coords[1]] = ' * '

	def print_grid(self):
		"""prints the grid, that's it!"""
		for row in self.grid:
			for col in row:
				print(col, end='')
			print()

class Player():

	def __init__(self):
		self.player_coords = [0,0]
		self.previous_coords = []

	def get_move_direction(self):
		"""prompts user for direction to move and returns choice"""
		# input validatin actually occurs in the compute_move_coords function

		msg = '\nEnter direction to move (N,S,E,W) or Q to Quit: '
		choice = input(msg).upper()
		return choice

	def compute_move_coords(self, direction_choice):
		"""modify player coords based on chosen movement direction"""
		self.previous_coords = self.player_coords[:] 

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
			print('Sorry, you\'ve hit a boundary and cannot proceed that way!\n')
			return False

		print('\n')
		return True

player = Player()
grid = Grid(player)

game_active = True

print("\033[H\033[J") #clear screen 
print('Welcome to the Dungeon!\n')

grid.grid[0][0] = ' X '
grid.print_grid()

while game_active:
	direction_choice = player.get_move_direction()
	if direction_choice == 'Q':
		break

	print("\033[H\033[J")	# clear the screen

	if player.compute_move_coords(direction_choice): #this IS the call to compute_move_coords !!
		grid.update_grid()
	
	grid.print_grid()	# happens whether second if was true or false; if false, no change to grid,
						# but it is still printed again in loop pass.

print('\nThanks for playing!')
print()

# the thing to remember here is that computer_move_coords is really doing TWO things:
# it's modifying the grid coords of player loation, if applicable, AND returning a bool value

