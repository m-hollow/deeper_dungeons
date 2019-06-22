
# new goals:
# 1. DONE instead of entering coordinates, user inputs N, S, E, W
# 2. DONE boundary checking to prevent out of range error
# 3. previously entered rooms revert to * instead of staying an X
# 4. compute exits per room

# you will need to make a list of visited rooms for part 3

# Q: right now update_grid is a method of the Grid class, and the Player class
# has the various functions for getting the directions. shoud there just be
# one big function to do this, separate from the classes?

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
	
		# this loop and the active variable are unneccessary,
		# because the return statement will exit the function.
		# note that you never actually set active to False in the loop!
		while active:
			
			possible_answers = ['N','S','E','W','Q']
			choice = input(msg).upper()

			if choice not in possible_answers:
				print('You did not enter a valid direction, try again.')
			
			else:
				return choice

	def compute_move_coords(self, direction_choice):
		"""modify player coords based on chosen movement direction"""

		# this needs to happen here (and not in update grid) because the
		# player coords get changed in the following code, so we need to grab
		# the old coords and store them first, before they change.
		self.previous_coords = self.player_coords.copy()  # the : is CRUCIAL!!! (copy not reference)

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
			return False
		 
		print('\n')
		return True

# this function is no longer used by I'm leaving it here because it's...elegant.
def play_again(): 
	msg = 'Do you want to move the player again? Y/N: '
	choice = input(msg)
	return choice.lower() == 'y'

player = Player()
grid = Grid(player)

game_active = True

# initial print of grid, doesn't take player choice
# how to avoid needing to do this here?
# without it, the order of operations doesn't work correctly; map is shown,
# player chooses dir, then is asked if they want to play again before map is
# redrawn to show players choice...

print("\033[H\033[J") #clear screen 
print('Welcome to the Dungeon!\n')

grid.grid[0][0] = ' X '
grid.print_grid()

while game_active:
	direction_choice = player.get_move_direction()
	if direction_choice == 'Q':
		#game_active = False	# not good, because rest of loop executes once...
		break
	print("\033[H\033[J")	# clear the screen
	# can you use 'continue' in here so that if computer_move_coords results in a boundary collision,
	# we return to the start of this while loop, and otherwise move on to update_grid, etc?
	# because currently if there's a boundary collision we still run the next two functions,
	# but we don't want to in case of a boundary collision
	if player.compute_move_coords(direction_choice) == True:
		grid.update_grid()
	grid.print_grid()

	#if not play_again():
	#	game_active = False


print('\nThanks for playing!')
print()




