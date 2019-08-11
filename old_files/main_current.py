import time
from random import randint
from random import choice
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

		self.create_start() # same as below, adds start on construction
		self.create_exit()	# doesn't need to return anything, just adds the exit on construction
		
		self.current_room_type = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type'] 

	def make_grid(self):
		# list comprehension to create matrix of the game grid graphics

		grid_matrix = [[' * ' for x in range(self.col)] for y in range(self.row)]

		return grid_matrix

	def update_player_location(self):
		"""updates the grid_matrix to show the X for the player coordinates"""

		self.grid_matrix[self.player.player_location[0]][self.player.player_location[1]] = ' X '
		self.grid_matrix[self.player.previous_coords[0]][self.player.previous_coords[1]] = ' * '


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

	def create_start(self):

		self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type'] = 'Start'	

	def create_exit(self):
		"""creates an exit in the room grid and makes sure this exit doesn't overlap with start position"""
		active = True

		while active:

			random_x = randint(0, self.row - 1)
			random_y = randint(0, self.col - 1 )

			coords = [random_x, random_y]

			if coords != self.player.player_location:
				self.all_room_grid[random_x][random_y]['Type'] = 'Exit' 
				active = False
			else:
				pass

	def print_grid(self):
		"""print the visual game grid"""
		clear_screen()

		print('# DUNGEON MAP #\n')

		for r in self.grid_matrix:
			for c in r:
				print(c, end='')
			print()						# use print('\n' to space out grid further)

		print('\n{} is located at X'.format(self.player.info['Name']))

		press_enter()

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
				elif col['Type'] == 'Start':
					grid_matrix_copy[r][c] = ' S '

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
		self.info = {'Name':'None', 'Race':''}
		self.stats = {'Level': 1, 'HP': 10, 'GOLD':self.settings.starting_gold}

		self.inventory = {'Weapon':'None', 'Clothing':'Old Shirt', 'Items':['Torch',]}
		
		self.player_location = [(self.settings.grid_size - 1), (int(self.settings.grid_size / 2) - 1)]
		self.previous_coords = [0,0]

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
		print("Items{:.>16} ".format(self.inventory['Items'][0])) # need to show ALL items in list...loop?

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

	def update_log(self):
		"""update the game_log to get current room from updated grid"""
		self.current_room = self.grid.current_room_type 

	# def print_log(self):

		
class RoomBook():
	"""An object that stores all the possible text strings for dungeon rooms"""
	def __init__(self): #  TODO: store all text in an actual text file and read from it here. 
		"""stores all the text strings for each room type"""
		self.start_text = '''\nI'm at the entrance to the dungeon. I sure hope I find treasure inside, \nand not anything nasty!'''
		

		self.empty_text = '''\nI'm entering a large, dark room. Looking around, there appears to be nothing \ninside other than dust, debris and more dust. This room is empty.'''
		

		self.monster_text = '''\nI've entered a very dark room. Something is approaching...it's a Monster!'''
		

		self.treasure_text = '''\nI'm standing in a room with a very high ceiling. There's an alter at the \ncenter with something on top...it's treasure!'''
		

		self.exit_text = '''\nI'm standing in a long, narrow corridor. There's a large, engraved gate at the \nend of this passage. I think this must be the exit!'''

		# all the text entries stored in one dictionary, indexed by room type
		# this isn't currently used in the game
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

def main_menu(player):
	"""displays main program menu, takes user input choice and returns it"""

	clear_screen()

	print('#   DEEPER DUNGEONS   #\n')
	print('1. Build character')
	print('2. Start New Game')
	print('3. Load Game')
	print('4. Change Game Settings')
	print('5. Exit Game')

	print('\nCurrently Loaded Character: {}'.format(player.info['Name']))

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
	# should this whole function be a method inside the game_log class ???

	game_log.update_log()		# should this be in the game_action event loop instead of here?
	current_msg = game_log.get_current_message() # shouldn't this be part of update_log ? 

	print('HP: {} GOLD: {}'.format(player.stats['HP'], player.stats['GOLD']))
	print('CURRENT ROOM: {}\n'.format(game_log.current_room))
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

	grid_one.update_player_location() # needs to happen here initially so the X gets printed to board

	active = True
	
	while active:
		# main game event loop for *game in state of play* (as opposed to game at main menu, not in play)

		selection = action_menu(player, game_log)

		if selection == 1:
			if movement_engine(settings, player, grid_one):
				grid_one.update_player_location()
				grid_one.update_current_roomtype()
				# game_log.update_log() # not used here because it gets called by run_game_log function

		elif selection == 2:
			"""show the map and current player location"""
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

		#else:			# this else is redundant, the validation checking happens inside action_menu
		#	print('That is not one of the menu options!')
		#	press_enter()

def run_game(settings, player):	
	"""prints Main Menu and takes user input"""

	active = True

	while active:

		user_action = main_menu(player)

		if user_action == 5:
			print('\nThanks for playing Deeper Dungeons!')
			print()
			active = False

		elif user_action == 1:

			player.build_player()
			player.created = True

		elif user_action == 2:

			if player.created:
				# we create the game grid object here, so that it's a brand new grid whenever option 2 (start game) is chosen
				grid_one = GameGrid(settings, player)
				game_log = GameLog(grid_one)
				game_action(settings, player, grid_one, game_log, d6, d20) #note all the locations these arguments are being drawn from...
			else:
				print('\nYou need to create a character first!')
				press_enter()

		else:
			print('\nSorry, that part of the game is still being developed.')
			press_enter()

def movement_engine(settings, player, grid):

	clear_screen()
	
	print('# DUNGEON MAP #\n')

	for r in grid.grid_matrix:
		for c in r:
			print(c, end='')
		print()

	print('\n{} is located at X'.format(player.info['Name']))

	player.previous_coords = player.player_location.copy()

	msg = '\nEnter direction to move (N,S,E,W) or Q for previous Menu: '
	choice = input(msg).upper()

	possible_choices = ['N', 'S', 'E', 'W', 'Q']

	# we actually need a while loop here for input validation, yes?
	# yes, invalid answer should repeat loop, NOT return False and exit function

	if choice not in possible_choices:
		print('You did not enter a valid direction, try again.\n')
		press_enter()
		return False

	elif choice == 'N' and player.player_location[0] > 0:
		player.player_location[0] -= 1
	elif choice == 'S' and player.player_location[0] < settings.grid_size - 1:
		player.player_location[0] += 1
	elif choice == 'E' and player.player_location[1] < settings.grid_size - 1:
		player.player_location[1] += 1
	elif choice == 'W' and player.player_location[1] > 0:
		player.player_location[1] -= 1
	elif choice == 'Q':
		print('Actually, I don\'t feel like moving right now...')
		press_enter()
		return False
	else:
		print('You\'ve hit a boundary and can\'t proceed that way!\n')
		press_enter()
		return False

	print('\n')
	return True

# instantiate game objects

settings = GameSettings()
player = Player(settings)
d6 = Dice()
d10 = Dice(10)
d20 = Dice(20)

# call the main run_game function loop
run_game(settings, player)



