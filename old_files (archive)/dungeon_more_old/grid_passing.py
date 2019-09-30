import time
from random import randint, choice

class TheGrid():
	"""the grid object"""

	def __init__(self, rowcol=5):
		self.row = rowcol
		self.col = rowcol
		self.matrix = self.make_grid_lc()		# matrix is a list of lists
		
		self.marker = ' X '
		self.matrix[2][2] = self.marker
	
	def make_grid(self):
		"""non list-comp version of building the matrix, just for notes purposes"""

		outer = []						# create the main list object itself
		for x in range(self.row):		# create a list called inner. this will (eventually) happen five times (row = 5) 
			inner = []
			for y in range(self.col):	# but -each time- a list is created above, the following will also 
										# happen before the next list is created...
				inner.append(' * ')		# create a '*' character once for each value in range(col) - so, x5, and put them all in the current
										# inner list (the one that just got created above).
										# once those five * have been put in inner, we go -back- to the first for loop, create
										# the next inner list, and so on...
			outer.append(inner)			# once a single inner list is created and filled with 5 *'s, we put it in outer.

		return outer

	def make_grid_lc(self):
		"""list comprehension version of making the matrix. so much cleaner!"""
				    
				    # This is the 'inner' loop	  And this is the 'outer' loop.
                    #    |						   |
		outer = [[' * ' for x in range(self.col)] for y in range(self.row)]
		return outer

	def print_grid(self):
		for row in self.matrix:
			for val in row:
				print(val, end='')
			print()
		print()

def outer_event():
	"""game menu loop. gameplay is not active."""

	active = True
	possible_choices = [1, 2]   # input is converted to int at time of input, see below.

	while active:

		print('1. Start')
		print('2. Quit')
		print()

		response = int(input('>'))

		if response not in possible_choices:
			print('You did not enter a valid command.')
		else:
			if response == 1:
				main_event()
			elif response == 2:
				print('Thanks for using this fine software.')
				active = False

def main_event():
	"""gameplay event loop. gameplay is active."""

	active = True

	grid_state = {'no_grid': True, 'rows_and_cols': 5}

	grid = None		# just an explicit placeholder for the object, C style

	while active:

		if grid_state['no_grid']:
			
			grid = TheGrid(grid_state['rows_and_cols'])

			print('Grid has been created')
			grid_state['no_grid'] = False

		print('1. Print Current Grid')
		print('2. Modify Current Grid')
		print('3. Make New Grid')
		print('4. Print current grid id')
		print('5. Return to Main Menu')
		print()
		
		response = int(input('>'))

		if response == 5:
			print('Returning to Main Menu')
			active = False

		elif response == 1:
			grid.print_grid()
			
		elif response == 2:
			modify_grid(grid)

		elif response == 3:
			make_new_grid(grid_state)

		elif response == 4:
			print('The ID of the current grid is {}'.format(id(grid)))
			print()

def modify_grid(grid):

	print('Enter new Row coordinate')
	x = int(input('>'))
	x -= 1
	print('Enter new Col coordinate')
	y = int(input('>'))
	y -= 1

	grid.matrix[2][2] = ' * '
	grid.matrix[x][y] = ' X '

def make_new_grid(grid_state):

	print('How many columns and rows do you want the new grid to have?')
	rows_and_cols = int(input('>'))

	# package this new info so it gets used in main event loop where grid is created.
	grid_state['rows_and_cols'] = rows_and_cols
	grid_state['no_grid'] = True	# flip to true so grid creation occurs in the main_event while loop

	print('New grid will be created. It will have {} rows and cols'.format(rows_and_cols))
	



outer_event()


