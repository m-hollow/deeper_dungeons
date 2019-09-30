# the point of this program is to show how to allow modification of an existing grid object
# ---as well as--- the creation of an *entirely new instance* of a grid object within the context
# of a running event loop.

# the key takeaway here is that the new object must be created inside the primary event loop, one way or another.

# the design of this program is built such that original object and new object are created with the exact same
# call to construction of class object, rather than separate calls to the class constructor.
# (in my attempts with separate calls, there was never a way (that I could find anyway) to get the *new* object
# into the original event loop). I created methods that called the class constructor and assigned it to a name, 
# but then had no way to pass that name (local to that function) back to the original running event loop.

# this design appears to solve that problem.

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

class TheGrid():
	"""the grid object"""

	grid_counter = 0

	def __init__(self, rowcol=5):
		self.rowcol = rowcol
		self.matrix = self.make_grid_listcomp()		# matrix is a list of lists
		
		self.marker = ' X '

		self.__class__.grid_counter += 1
		
		self.previous_row = None
		self.previous_col = None

		self.current_row = int(rowcol/2)
		self.current_col = int(rowcol/2)

		self.matrix[self.current_row][self.current_col] = ' X ' # print the starting position of the X on init

	def print_grid_counter(self):
		print('The value of self.__class__.grid_counter is currently {}'.format(self.__class__.grid_counter))
		print('The value of grid_counter (in class namespace) is currently {}'.format(TheGrid.grid_counter))

	def make_grid_listcomp(self):
		"""list comprehension for creating the matrix"""
		outer = [[' * ' for x in range(self.rowcol)] for y in range(self.rowcol)]
		return outer

	def print_grid(self):
		"""print it, ya dingus"""
		for row in self.matrix:
			for val in row:
				print(val, end='')
			print()
		print()

def outer_event():
	"""program menu loop. main functional event loop is not active, but software is running."""
	clear_screen()

	active = True
	possible_choices = ['1','2']

	while active:

		print('1. Start')
		print('2. Quit')

		response = input('\n>')

		if response not in possible_choices:
			print('You did not enter a valid command.')
		else:
			if response == '1':
				main_event()
			elif response == '2':
				print('Thanks for using this fine software.')
				active = False

def press_enter():
	prompt = '...'
	input(prompt)

def main_event():
	"""program event loop. the software is active."""

	active = True

	grid_state = {'no_grid': True, 'rows_and_cols': 5}	# dict object, stores info and flag for building new grid objects.

	grid = None		# just an explicit placeholder for the grid object

	possible_choices = ['1','2','3','4','5','6']

	while active:

		clear_screen()
		
		if grid_state['no_grid']:	# flag check: are we making a new grid or using current one?
			
			grid = TheGrid(grid_state['rows_and_cols'])

			print('A Grid object has been created\n')

			grid_state['no_grid'] = False # we want to keep using the grid we made until user chooses to create a new one.

		print('1. Print Current Grid')
		print('2. Modify Current Grid')
		print('3. Make New Grid')
		print('4. Print current grid id')
		print('5. Print grid_counter attribute.')
		print('6. Return to Main Menu')
		print()
		
		response = input('>')

		if response not in possible_choices:
			print('\nYou did not enter a valid option, try again.')

		else:

			if response == '6':
				print('Returning to Main Menu')
				active = False

			elif response == '1':
				grid.print_grid()
				
			elif response == '2':
				modify_grid(grid)

			elif response == '3':
				make_new_grid(grid_state)

			elif response == '4':
				print('The ID of the current grid is {}'.format(id(grid)))
				print()

			elif response == '5':
				grid.print_grid_counter()

		press_enter()

def modify_grid(grid):
	"""mutate the current grid object. id of grid will remain the same after mutation"""

	# store current coords to previous since they are about to be udpated

	grid.previous_row = grid.current_row
	grid.previous_col = grid.current_col

	print('Enter new Row coordinate')
	row = int(input('>'))
	row -= 1							# we're assuming the user isn't starting from 0
	print('Enter new Col coordinate')
	col = int(input('>'))
	col -= 1

	grid.current_row = row
	grid.current_col = col

	grid.matrix[grid.previous_row][grid.previous_col] = ' * '
	grid.matrix[grid.current_row][grid.current_col] = ' X '

def make_new_grid(grid_state):
	"""provide instructions for generation of new grid, which will have a new id, and will created in main_event loop"""

	print('How many columns and rows do you want the new grid to have?')
	response = input('>')


	rows_and_cols = int(response)

	# package this new info into grid_state dictionary so it gets used in main event loop (where grid is created).
	grid_state['rows_and_cols'] = rows_and_cols
	grid_state['no_grid'] = True	# flip to true so grid creation occurs in the main_event while loop

	print('Ok, a new grid will be created when the main event loop runs next.')
	print('It will have {} rows and cols'.format(rows_and_cols))
	
# run the program
outer_event()



