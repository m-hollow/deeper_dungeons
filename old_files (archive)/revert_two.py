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
		
		msg = '\nEnter direction to move (N,S,E,W) or Q to Quit: '
		active = True 
	
		# is 'active' even needed here? the return statement will exit the loop (and the function)
		while active:
			
			possible_answers = ['N','S','E','W','Q']
			choice = input(msg).upper()

			if choice not in possible_answers:
				print('You did not enter a valid direction, try again.')
			
			else:
				return choice

	def compute_move_coords(self, direction_choice):
		"""modify player coords based on chosen movement direction"""

		active = True

		while active:

			self.previous_coords = self.player_coords[:]  

			if direction_choice == 'N' and self.player_coords[0] > 0:
				self.player_coords[0] -= 1
			elif direction_choice == 'S' and self.player_coords[0] < 4:
				self.player_coords[0] += 1
			elif direction_choice == 'E' and self.player_coords[1] < 4:
				self.player_coords[1] += 1
			elif direction_choice == 'W' and self.player_coords[1] > 0:
				self.player_coords[1] -= 1
			else:
				print('Sorry, you\'ve hit a boundary and cannot proceed that way!\n')

# this function is no longer used but I'm leaving it here because it's...elegant.
def play_again(): 
	msg = 'Do you want to move the player again? Y/N: '
	choice = input(msg)
	return choice.lower() == 'y'

player = Player()
grid = Grid(player)

game_active = True

print("\033[H\033[J") #clear screen 
print('\nWelcome to the Dungeon!\n')

grid.grid[0][0] = ' X '
grid.print_grid()

while game_active:
	direction_choice = player.get_move_direction()
	if direction_choice == 'Q':
		active = False
	else:
		print("\033[H\033[J")	# clear the screen
		player.compute_move_coords(direction_choice)
		grid.update_grid()
		grid.print_grid()

print('\nThanks for playing!')
print()
