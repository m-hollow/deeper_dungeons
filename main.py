import time
from random import randint
import copy

# define game objects

class GameSettings():
	"""Define game settings"""

	def __init__(self):
		self.grid_size = 5
		self.starting_gold = 10
		self.difficulty = 1

	def user_settings_change(self):

		msg = 'Choose the size of the dungeon grid: '

		size_choice = int(input(msg))

		self.grid_size = size_choice

	def print_legend(self):

		print('-------MAP LEGEND-------')
		print('PLAYER LOCATION........X')
		print('UNEXPLORED ROOM....... *')
		print('TREASURE...............T')
		print('ENEMY ENCOUNTER........E')

class GameGrid():
	"""Creates a grid object for the game of variable size"""
	def __init__(self, settings, player):
		
		self.settings = settings
		self.player = player

		self.row = self.settings.grid_size
		self.col = self.settings.grid_size

		self.grid_matrix = self.make_grid()			# grid for graphics, containing strings '*'
		self.all_room_grid = self.generate_rooms()  # grid for room data, containing room dictionaries

		self.create_exit()	# doesnt need to return anything, just adds the exit on construction
		self.create_start() # same

		# is this used for anything? update_player_location func is using self.player.playerlocation to update grid_matrix
		self.current_room_coords = self.player.player_location #list of two ints representing x and y coords

		# this is accessed by the gamelog and used to determine which room message is printed.
		# perhaps also used as primary means to determine room type during movement ??
		self.current_room_type = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type'] 

	def make_grid(self):
		# list comprehension to create matrix of the game grid

		grid_matrix = [[' * ' for x in range(self.col)] for y in range(self.row)]

		return grid_matrix

	def update_player_location(self):
		"""updates the grid_matrix to show the X for the player coordinates"""

		self.grid_matrix[self.player.player_location[0]][self.player.player_location[1]] = ' X '

	def update_current_roomtype(self):
		"""udpate the current_room_type attribute to reflect current player location"""

		self.current_room_type = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type']

	def generate_rooms(self):
		"""create a room for each coordinate in the grid matrix"""
		all_room_grid = []	# will become a matrix (a list of lists) containing room dictionaries
		
		for r in self.grid_matrix:		# r is a list

			row = []

			for c in r:					# c is a string ('*'), num of loops will = num of * in list r
				room_type = self.get_room_type()
				room = {'Type':room_type, 'Visited':False} 
				row.append(room)

			all_room_grid.append(row)
			
		return all_room_grid

	def get_room_type(self):
		"""called by generate_rooms function to make one random room"""
		room_type = ''
		num = randint(1,8)

		if num >= 1 and num <= 4:
			room_type = 'Empty'
		elif num >= 5 and num <= 7:
			room_type = 'Monster'
		elif num == 8:
			room_type = 'Treasure'
		
		return room_type

	def create_exit(self):
		random_x = randint(0, self.row - 1)
		random_y = randint(0, self.col - 1 )

		self.all_room_grid[random_x][random_y]['Type'] = 'Exit' 

	def create_start(self):

		self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type'] = 'Start'

	def print_grid(self):
		"""print the visual game grid"""
		clear_screen() # this is actually interesting; a class object is calling a standard function

		print('# DUNGEON MAP #\n')

		for r in self.grid_matrix:
			for c in r:
				print(c, end='')
			print()						# use print('\n' to space out grid further)

		print('\n{} is located at X'.format(self.player.info['Name']))

		press_enter() # and same here, class object calls function that exists outside the object

	def dev_grid_showtypes(self):
		"""for dev testing, not gameplay: show current properties of all rooms"""
		
		clear_screen()

		r = 0

		#grid_matrix_copy = self.grid_matrix[:]	  # doesn't work, does a shallow copy

		grid_matrix_copy = copy.deepcopy(self.grid_matrix)

		for row in self.all_room_grid:
			c = 0
			for col in row:
				if col['Type'] == 'Empty':				 
					grid_matrix_copy[r][c] = ' E '		
				elif col['Type'] == 'Monster':			
					grid_matrix_copy[r][c] = ' M '
				elif col['Type'] == 'Treasure':
					grid_matrix_copy[r][c] = ' T '
				elif col['Type'] == 'Exit':
					grid_matrix_copy[r][c] = ' @ '

				c += 1
			r += 1

		# print the dev grid
		for row in grid_matrix_copy:
			for val in row:
				print(val, end = '')
			print()

		press_enter()

class Dice():
	"""Create a variable sided die that can be rolled"""

	def __init__(self, sides=6):
		self.sides = sides

	def rolldie(self):
		roll = randint(1, self.sides)
		return roll

class Player():
	"""Generates the user character"""

	def __init__(self, settings):
		self.settings = settings

		self.created = False
		self.info = {'Name':'', 'Race':''}
		self.stats = {'Level': 1, 'HP': 10, 'GOLD':self.settings.starting_gold}

		self.inventory = {'Weapon':'None', 'Clothing':'Old Shirt', 'Items':'Torch'} #make items value a list

		# start location, fixed value for every new grid created, same as initial player row and col vals
		self.player_start_location = [self.settings.grid_size - 1, (int(self.settings.grid_size / 2) - 1)]
		
		#list of current coordinates for player, will constantly be modified
		self.player_location = [(self.settings.grid_size - 1), (int(self.settings.grid_size / 2) - 1)] 

	def build_player(self):
		"""fill dictionary with user character choices"""
		
		clear_screen()

		a = input('What is the name of your character? ')
		b = input('What is the Race of your character? ')

		self.info['Name'] = a.title()
		self.info['Race'] = b.title()

		clear_screen()

		print('You have successfully created {} the {}.'.format(a.title(), b.title()))
		print('You will begin with {} Hit Points and {} Gold Pieces.'.format(self.stats['HP'], 
			self.stats['GOLD']))
		print('\nYou are now ready to start the game!')

		press_enter()

	def print_player_info(self):
		"""display all player stats on the screen"""
		clear_screen()

		print("#    PLAYER INFO    #\n")
		print("Name{:.>17} ".format(self.info['Name']))
		print("Race{:.>17} ".format(self.info['Race']))
		print("Level{:.>16} ".format(self.stats['Level']))
		print("Hit Points{:.>11} ".format(self.stats['HP']))
		print("Gold Pieces{:.>10} ".format(self.stats['GOLD']))
	
		press_enter()

	def show_inventory(self):
		"""Prints player inventory screen"""
		clear_screen()

		print("#    INVENTORY    #\n")
		print("Weapon{:.>15} ".format(self.inventory['Weapon']))
		print("Clothing{:.>13} ".format(self.inventory['Clothing']))
		print("Items{:.>16} ".format(self.inventory['Items']))

		press_enter()

class GameLog():
	"""an object that contains the game log and displays its contents as necessary"""
	def __init__(self, grid):
		self.grid = grid
		self.room_book = RoomBook()
		self.current_room = 'None'
	
	def get_current_message(self):
		if self.grid.current_room_type == 'Start':
			self.current_message = self.room_book.start_text
		if self.grid.current_room_type == 'Empty':
			self.current_message = self.room_book.empty_text
		if self.grid.current_room_type == 'Monster':
			self.current_message = self.room_book.monster_text
		if self.grid.current_room_type == 'Treasure':
			self.current_message = self.room_book.treasure_text
		if self.grid.current_room_type == 'Exit':
			self.current_message = self.room_book.exit_text

		return self.current_message

	def update_room_type(self):
		"""is this even necessary? doesn't the grid updating cover this behavior?"""
		# need to think this one through.. is it redundant, or necessary...think about construction
		self.current_room = self.grid.current_room_type #self.current_room doesn't even exist...

		# current conclusion:
		# this is necessary if you're defining the current_room attribute in __init__
		# what's fascinating is that previously, you *did not* define it there, but the run_game_log function
		# was nonetheless able to find it, HERE, in the method update_room_type, and get the value from there.
		# which seems actually BETTER, because it means you don't need to keep updating the attribute
		# (because if it IS defined as an attribute upon instantiation, you then need to update it...)

class RoomBook():
	"""An object that stores all the possible text strings for dungeon rooms"""
	def __init__(self): #  TODO: consider storing all text in an actual text file and reading from it. 
		"""stores all the text strings for each room type"""
		self.start_text = '''\nI'm at the entrance to the dungeon. I sure hope I find treasure inside, \nand not anything nasty!'''
		

		self.empty_text = '''\nI'm entering a large, dark room. Looking around, there appears to be nothing \ninside other than dust, debris and more dust. This room is empty.'''
		

		self.monster_text = '''\nI've entered a very dark room. Something is approaching...it's a Monster!'''
		

		self.treasure_text = '''\nI'm standing in a room with a very high ceiling. There's an alter at the \ncenter with something on top...it's treasure!'''
		

		self.exit_text = '''\nI'm standing in a long, narrow corridor. There's a large, engraved gate at the \nend of this passage. I think this must be the exit!'''

		# all the text entries stored in one dictionary, indexed by room type
		# this isn't currently used
		self.room_book = {'Start':self.start_text, 'Empty':self.empty_text, 'Monster':self.monster_text, 'Treasure':
			self.treasure_text, 'Exit':self.exit_text}

class MainMenu():
	"""Display menu and receive input for user choice"""

	def __init__(self):
		self.nothing = None

	def print_menu(self):

		clear_screen()

		print('#   DEEPER DUNGEONS   #\n')
		print('1. Start New Game')
		print('2. Load Game')
		print('3. Change Game Settings')
		print('4. Exit Game')

	def main_choice(self):
		
		possible_choices = ['1','2','3','4']
		active = True

		while active:
			msg = '\nEnter your choice: '
			choice = input(msg)
			if choice in possible_choices:
				active = False
				return int(choice) # is active = False redundant since the return will exit the loop and function?
			else:
				print('That\'s not one of the menu options!')

# define game functions.

def main_menu():
	"""displays main program menu, takes user input choice"""

	clear_screen()

	print('#   DEEPER DUNGEONS   #\n')
	print('1. Build Character')
	print('2. Start New Game')
	print('3. Load Game')
	print('4. Change Game Settings')
	print('5. Exit Game')

	possible_choices = ['1','2','3','4','5']
	active = True

	while active:
		msg = '\nEnter your choice: '
		choice = input(msg)
		if choice in possible_choices:
			active = False #unnecessary because return will exit loop and function?
			return int(choice)
		else:
			print('That\'s not one of the menu options!')

def press_enter():
	msg = '\nOK...'
	input(msg)

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

def run_game_log(player, game_log):	
	"""updates and prints the current gamelog"""

	game_log.update_room_type()		# seems like ideally this would happen elsewhere, specifically in an 'update' function, not here
	current_msg = game_log.get_current_message()

	print('HP: {} GOLD: {}'.format(player.stats['HP'], player.stats['GOLD']))
	print('CURRENT ROOM: {}\n'.format(game_log.current_room)) # why does this work ??!!?? 
	print("{}'s LOG: {}\n".format(player.info['Name'].upper(), current_msg))

def action_menu(player, game_log):
	"""print the game_log, and a menu of game actions, and take user input"""

	clear_screen()

	run_game_log(player, game_log)

	print('1. Move')
	print('2. Show Map')
	print('3. Show Player Inventory')
	print('4. Show Player Stats')
	print('5. Exit to Main Menu')
	print('6. (dev) show dev map')

	possible_choices = ['1','2','3','4','5','6']
	active = True

	while active:
		selection = input('\nNow I shall... ')
		if selection in possible_choices:
			active = False
			return int(selection)	# return always exits a function, right? so active = False is redundant?
		else:
			print('That\'s not one of the menu options!')

def game_action(settings, player, grid_one, game_log, d6, d20):

	active = True
	
	while active:
		# main game event loop for -game in state of play- (as opposed to game at main menu not in play)

		grid_one.update_player_location()

		# run_game_log(player, game_log)      # doesn't work here right now because action_menu call clears screen!

		selection = action_menu(player, game_log)	#right now this is what prints action menu...

		if selection == 1:
			"""this needs to launch the player movement function and update location"""
			# player location is stored in the player class
			print('\nI will move to the next room...')

			press_enter()

		elif selection == 2:
			"""Unfinished"""
			grid_one.print_grid()

		elif selection == 3:
			"""Show inventory screen"""
			player.show_inventory()

		elif selection == 4:
			"""Unfinished"""
			player.print_player_info()

		elif selection == 6:
			grid_one.dev_grid_showtypes()

		elif selection == 5:
			print('Returning to Main Menu...')
			active = False

		else:			# this else is redundant, the validation checking happens inside action_menu
			print('That is not one of the menu options!')
			press_enter()

def run_game():	
	"""prints Main Menu and takes user input"""

	active = True

	while active:

		user_action = main_menu()

		if user_action == 5:
			print('\nThanks for playing Deeper Dungeons!')
			print()
			active = False

		elif user_action == 1:

			player.build_player()
			player.created = True

		elif user_action == 2:

			if player.created:
				game_action(settings, player, grid_one, game_log, d6, d20)
			else:
				print('\nYou need to create a character first!')
				press_enter()

		else:
			print('\nSorry, that part of the game is still being developed.')
			press_enter()

# instantiate game objects

settings = GameSettings()
player = Player(settings)
grid_one = GameGrid(settings, player)
game_log = GameLog(grid_one)

d6 = Dice()
d10 = Dice(10)
d20 = Dice(20)

# call the main run_game function loop
run_game()



