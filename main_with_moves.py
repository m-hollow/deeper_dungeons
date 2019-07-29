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

class GameGrid():
	"""Creates a grid object for the game of variable size"""
	def __init__(self, settings, player):
		
		self.settings = settings
		self.player = player

		self.row = self.settings.grid_size
		self.col = self.settings.grid_size

		# question: should floor_level be stored in settings?
		self.floor_level = 1 # objects constructed as levels advance will increase this number

		self.grid_matrix = self.make_grid()			# grid for graphics, containing strings '*'
		self.all_room_grid = self.generate_rooms()  # grid for room data, containing room dictionaries

		self.create_start() # same as below, adds start on construction
		self.create_exit()	# doesn't need to return anything, just adds the exit on construction
		self.create_mystic() # one mystic in every dungeon level
		
		self.current_room_type = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type'] 
		
		# this is a bool and is used to track if current inhabited room was previously visited or not
		# and yes, you could perform this check by checking the all_room_grid and looking at 'Visited' bool directly.
		self.room_status = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Visited']

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
		self.room_status = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Visited']

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
		"""creates an exit in the room grid and makes sure it doesn't overlap with player start position"""
		active = True

		while active:
			# should I just change the min random number, rather than the complex conditionals in the if below ??
			random_x = randint(0, self.row - 1)
			random_y = randint(0, self.col - 1 )

			coords = [random_x, random_y]
			# makes sure exit 1. does not overlap player 2. is not within 2 rows of the player (this logic needs some work...)
			if coords != self.player.player_location and abs(coords[0] - self.player.player_location[0]) \
			>= 2 and abs(coords[1] - self.player.player_location[1]) >= 1:
				self.all_room_grid[random_x][random_y]['Type'] = 'Exit'
				active = False
			else:
				pass

		# QUESTION: are you inverting your coordinates above? x is row, y is col... isn't that backwards? isn't a row the Y coord?

	def create_mystic(self):

		active = True

		while active:

			random_x = randint(0, self.row - 1)
			random_y = randint(0, self.col - 1)
			
			coords = [random_x, random_y]

			if coords != self.player.player_location and self.all_room_grid[random_x][random_y]['Type'] != 'Exit':
				self.all_room_grid[random_x][random_y]['Type'] = 'Mystic'
				active = False
			else:
				pass

	def print_grid(self):
		"""print the visual game grid"""
		
		print('\nLV.{}'.format(self.floor_level))

		for r in self.grid_matrix:
			for c in r:
				print(c, end='')
			print()						# use print('\n' to space out grid further)

		print()

		#print('\n{} is located at X'.format(self.player.info['Name']))

	def dev_grid_showtypes(self):
		"""for dev testing, not gameplay: show current properties of all rooms"""
		
		clear_screen()

		r = 0

		#grid_matrix_copy = self.grid_matrix[:]	  # doesn't work, does a shallow copy

		grid_matrix_copy = copy.deepcopy(self.grid_matrix)

		# modify chars in the deepcopy based on corresponding roomtype in original all_room_grid
		# incrementing variables r, c used to index (and thereby modify) contents of deepcopy grid
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
				elif col['Type'] == 'Mystic':
					grid_matrix_copy[r][c] = ' & '

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

	def __init__(self):
		self.last_roll = None
		self.roll_mod = 0

	def roll(self, sides=6):
		roll = randint(1, sides)
		self.last_roll = roll
		return roll

	def print_roll(self):
		"""stepped printing of roll"""
		text = 'ROLLING...'
		for c in text:
			print(c, end='', flush=True)
			time.sleep(0.06)
		print(' {}'.format(self.last_roll))

class Weapon():
	"""Generates a weapon object with type and damage"""
	def __init__(self, name, damage):
		self.name = name
		self.damage = damage

	def modify_weapon(self, add_to_damage):
		self.name += 'x1'
		self.damage += add_to_damage

	def print_stats(self):
		print('*** WEAPON INFO ***')
		print('TYPE{:.>15}'.format(self.name))
		print('DAMAGE{:.>13}'.format(self.damage))

class Player():
	"""Generates the user character"""

	def __init__(self, settings):
		self.settings = settings

		self.created = False
		self.info = {'Name':'None', 'Race':''}
		self.stats = {'LEVEL': 1, 'HP': 10, 'GOLD':self.settings.starting_gold}

		self.potions = []
		self.weapon = Weapon('Dagger', 4)

		self.inventory = {'Weapon':self.weapon.name, 'Clothing':'Old Shirt', 'Items':['Torch',]}
		
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
		print("Level{:.>16} ".format(self.stats['LEVEL']))
		print("Hit Points{:.>11} ".format(self.stats['HP']))
		print("Gold Pieces{:.>10} ".format(self.stats['GOLD']))
	
		press_enter()

	def show_inventory(self):
		"""Prints player inventory screen"""
		clear_screen()

		print("#     INVENTORY     #\n")
		print("Weapon{:.>15} ".format(self.inventory['Weapon']))
		print("Clothing{:.>13} ".format(self.inventory['Clothing']))
		print("Items{:.>16} ".format(self.inventory['Items'][0])) # need to show ALL items in list...loop?
		print()
		print("#      POTIONS      #\n")
		
		count = 1
		for potion in self.potions:
			print('#{}  {}'.format(count, potion))
			count += 1

		press_enter()

	def reset_player(self):
		"""reset the player, triggered on exit of active game"""
		# this will probably need modification once saving and loading are introduced!

		self.player_location = [(self.settings.grid_size - 1), (int(self.settings.grid_size / 2) - 1)]

		# do I need to index these to reset them, or can I just rebuild them like this?
		self.stats = {'LEVEL': 1, 'HP': 10, 'GOLD':self.settings.starting_gold}
		self.inventory = {'Weapon':self.weapon.name, 'Clothing':'Old Shirt', 'Items':['Torch',]}
		self.potions = []

		# by index, I mean resetting them like this (is there reason to do this instead of full reassignments above?)
		# self.stats['LEVEL'] = 1
		# self.stats['HP'] = 10
		# self.stats['GOLD'] = self.settings.starting_gold

		# the difference is that the current approach is creating an entirely new dictionary and 
		# assigning it to stats, inventory, etc. the other approach is keeping the original dictionary,
		# but assigning new values to each entry in it. I think for your current purposes, you can
		# use either approach, but it's important to recognize the differnet in how both work.

	def create_rand_potion(self):
		"""creates an object of the Potion class, random type, stored in attribute Potions list"""
		potion = Potion('r')
		self.potions.append(potion)

	def create_spec_potion(self, p_type):
		"""creates a specific type of potion, stores it in Potions attribute list"""
		potion = Potion(p_type)
		self.potions.append(potion)

class Potion():
	"""Creates a Potion object to be used by player"""

	def __init__(self, p_type):
		self.p_type = p_type
		self.type = self.determine_type()

	def determine_type(self):
		"""used to determine type of potion object"""
		if self.p_type == 'h':
			return 'HEAL'
		elif self.p_type == 'ha':
			return 'HEAL ADV'
		elif self.p_type == 's':
			return 'STRENGTH'
		elif self.p_type == 'sa':
			return 'STRENGTH ADV'
		elif self.p_type == 'i':
			return 'INVISIBLE'
		elif self.p_type == 'r':
			num = randint(1,10)
			if num == 10:
				return 'INVISIBLE'
			if num == 9:
				return 'STRENGTH ADV'
			if num == 8:
				return 'HEAL ADV'
			if num <= 4:
				return 'HEAL'
			if num > 4 and num < 8:
				return 'STRENGTH'

	def use_potion(self):
		"""method for player to use the potion object"""

		# should this be a player class method ?
		# I think it has to be, otherwise you'd have to pass
		# player object to potion object, which seems backwards.

	def p_info(self):
		print('TYPE: {}'.format(self.type))

class GameLog():
	"""an object that contains the game log and displays its contents as necessary"""
	def __init__(self, player, grid):
		self.player = player
		self.grid = grid
		self.room_book = RoomBook()
		self.current_room = 'None'   # used only to print room type in game header
		self.current_message = 'None'
	
	def update_log(self):
		"""update the game_log to get current room from updated grid"""
		self.current_room = self.grid.current_room_type #a bit redundant, you could access grid object to print header info.
		self.current_message = self.get_current_message()

	def get_current_message(self):
		"""looks at grid object to determine and return appropriate log entry"""


		# this is where you use the room_status attribute bool, you COULD simply check the all_room_grid bool 
		# 'Visited' here instead, it's the same info. You just thought having this extra var was cleaner.

		if self.grid.room_status == False and self.grid.current_room_type != 'Exit':

			if self.grid.current_room_type == 'Start':
				self.current_message = self.room_book.room_dict['Start']
			elif self.grid.current_room_type == 'Empty':
				self.current_message = self.room_book.room_dict['Empty']
			elif self.grid.current_room_type == 'Monster':
				self.current_message = self.room_book.room_dict['Monster']
			elif self.grid.current_room_type == 'Treasure':
				self.current_message = self.room_book.room_dict['Treasure']
			elif self.grid.current_room_type == 'Mystic':
				self.current_message = self.room_book.room_dict['Mystic']

		elif self.grid.current_room_type == 'Exit':		# doesn't matter if Visited is True or False, Exit always presents the same.
				self.current_message = self.room_book.room_dict['Exit']

		# room_status = True, room has already been visited.
		else:
			self.current_message = 'You have visited this room previously!'

		return self.current_message	

	def print_log(self):
		"""prints the header, the current dungeon grid, and the current log text entry"""
		
		# print header stats
		print('{} the {} \t HP: {}  GOLD: {}\t ROOM: {}'.format(self.player.info['Name'].upper(), self.player.info['Race'], \
			self.player.stats['HP'], self.player.stats['GOLD'], self.current_room))

		# print game map
		self.grid.print_grid()

		# game log
		
		print(self.current_message)


		# print('{}\'s LOG:\n{}'.format(self.player.info['Name'].upper(), self.current_message))
	
class RoomBook():
	"""loads room text and builds dictionary of all separated entries"""
	def __init__(self):
		self.all_entries = self.load_entries()

		self.room_dict = {
		'Start':self.all_entries[0],
		'Empty':self.all_entries[1],
		'Monster':self.all_entries[2],
		'Treasure':self.all_entries[3],
		'Mystic':self.all_entries[4],
		'Exit':self.all_entries[5],
		}

	def load_entries(self):
		"""loads the text file with all entries and splits it into a list"""
		filename = 'text_files/room_book.txt'
		with open(filename, encoding='utf-8') as file_object:
			room_text = file_object.read().split('X')

		return room_text

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

def step_printer(word):
	"""call whenever you want to print a word in steps"""
	for c in range(len(word)):
		print(c, end='', flush=True)
		time.sleep(0.06)

def slow_print_two(word_one, word_two):
	"""call to print one word, pause, then the second word"""
	print(word_one, end='', flush=True)
	time.sleep(0.08)
	print(word_two)

def slow_print_elipsis(word_one, word_two):
	"""prints word one, then step prints elipsis, then prints word two"""
	elipsis = '......'
	print(word_one, end='', flush=True)
	for c in elipsis:
		print(c, end='', flush=True)
		time.sleep(0.06)
	print(word_two, flush=True)

def command_menu(player):
	"""prints the command menu for the player"""
	clear_screen()

	print('#{:^33}#'.format(player.info['Name'].upper() + '\'s COMMANDS'))
	print()
	print('MOVE: North  DO:  Rest   GAME: Save')
	print('      South       Item         Quit')
	print('      East        Bio')
	print('      West')
	print()
	print()
	print('Type the first letter of any command at game prompt.')

	press_enter()

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
	
	msg = '\nEnter your choice: '
	choice = input(msg)
	if choice in possible_choices:
		return int(choice)
	else:
		print('That\'s not one of the menu options!')
		press_enter()
		return None

def get_player_input():
	msg = '\n> '
	player_input = input(msg)
	return player_input

def press_enter():
	msg = '\n...'
	input(msg)

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

def action_menu(game_log):
	"""print the game_log, the map, the command menu, take user input, and Return user choice"""

	clear_screen()
	game_log.print_log()
	
	possible_choices = ['c', 'n', 's', 'e', 'w', 'r', 'i', 'b', 'q', 'd']
	
	command = get_player_input().lower()

	if command in possible_choices:
		return command
	else:
		print('\nYou have entered an invalid command, try again.')
		press_enter()
		return None

def game_action(settings, player, grid, game_log, dice):

	grid.update_player_location() # needs to happen here initially so the X gets printed to board
	game_log.update_log() # same, needs to happen so its attributes are not in initial state 'None'

	active = True
	
	while active:
		# main game event loop for *game in state of play* (as opposed to game at main menu, not in play)

		command = action_menu(game_log)
		movement_choices = ['n','s', 'e', 'w']

		if command in movement_choices:
			if movement_engine(settings, player, grid, command):
				grid.update_player_location()
				grid.update_current_roomtype()
				game_log.update_log()

		elif command == 'i':
			"""Show inventory screen"""
			player.show_inventory()

		elif command == 'b':
			"""Show player info screen"""
			player.print_player_info()

		elif command == 'd':
			"""show room types for each grid coordinate (dev only)"""
			grid.dev_grid_showtypes()

		elif command == 'c':
			command_menu(player)

		elif command == 'q':
			print('Returning to Main Menu...') #this won't be seen unless you add a press_enter() all after it
			player.reset_player()	#reset player so new game starts fresh, attributes back to initials
			#reset_grid()	# I think this is not needed; grid is constructed when menu action 2 is chosen, so will be new...
			#reset_log()	# needed ?
			active = False

		else:
			pass

def run_game(settings, player):	
	"""prints Main Menu and takes user input"""

	active = True

	while active: #main event loop of program running (but game not in play)

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
				grid = GameGrid(settings, player)
				game_log = GameLog(player, grid)
				game_action(settings, player, grid, game_log, dice) #note all the locations these arguments are being drawn from...
			
			else:
				print('\nYou need to create a character first!')
				press_enter()

		elif user_action == 3 or user_action == 4:
			print('\nSorry, that part of the game is still being developed.')
			press_enter()

def movement_engine(settings, player, grid, selection):

	player.previous_coords = player.player_location.copy()

	if selection == 'n' and player.player_location[0] > 0:
		player.player_location[0] -= 1
	elif selection == 's' and player.player_location[0] < settings.grid_size - 1:
		player.player_location[0] += 1
	elif selection == 'e' and player.player_location[1] < settings.grid_size - 1:
		player.player_location[1] += 1
	elif selection == 'w' and player.player_location[1] > 0:
		player.player_location[1] -= 1

	# remember, the whole reason for the boolean return from this function is to separate between a
	# successful move (return true, grid update) and a border collision (return false, no grid update)
	else:
		print('\nYou\'ve hit the boundary of the dungeon!')
		press_enter()
		return False # false returned, so grid will not be updated; function exited here.

	print('\n')

	# change 'Visited' key of previous room to 'True'
	grid.all_room_grid[player.previous_coords[0]][player.previous_coords[1]]['Visited'] = True

	return True 	# things down here are triggered even if an if/elif/else is True above; after 
					# executing code block for the if / elif, program moves to next section of code in 
					# the function body, which is this area (unless a Return was hit, in which case the
					# function is exited at the Return statement. So the 'else' condition, if True, will
					# exit the function).

# instantiate game objects

# how do I make these not be global variables? should I have a 'build start objects' function
# that is called before run_game? but then how do I pass the objects that it builds to run_game?
# or can I simply move these three inside run_game ?

settings = GameSettings()
player = Player(settings)
dice = Dice()

# call the main run_game function loop
run_game(settings, player)



