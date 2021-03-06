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
							 # perhaps that means I should use a __class__ attribute here? 

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
		"""updates the grid_matrix to show the X for the player coordinates (and change prev room back to a *)"""

		self.grid_matrix[self.player.previous_coords[0]][self.player.previous_coords[1]] = ' * '
		self.grid_matrix[self.player.player_location[0]][self.player.player_location[1]] = ' X '


	def update_current_roomtype(self):
		"""udpate the current_room_type attribute to reflect current player location"""

		self.current_room_type = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type']
		self.room_status = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Visited']

		# remember, all_room_grid is a list containing multiple lists, and each of THOSE lists contains a bunch of
		# dictionaries (the room dictionaries, with keys for Type and Visited, etc).
		# the above code indexes the all_room_grid with format [][][]
		# first [] - index list inside the main list, e.g. which list do we want inside the main list?
		# second [] - index that list, e.g. which dictionary do we want inside the list we've chosen?
		# third [] - index the dictionary by key, giving us the value stored for that key.

	def generate_rooms(self):
		"""create a room that corresponds to each coordinate in the grid matrix object"""
		all_room_grid = []	# will become a matrix (a list of lists) containing room dictionaries
		
		for r in self.grid_matrix:		# r is a list

			row = []

			for c in r:					# c is a string ('*'), num of loops will = num of * in list r
				room_type = self.get_room_type()
				room = {'Type':room_type, 'Visited':False, 'Post_Note': None} 
				row.append(room)

			all_room_grid.append(row)		# done once for each list (r) in the grid_matrix
			
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

	def build_next_dungeon_floor(self):
		"""updates dungeon grid to next floor when player exits previous floor"""

		# increment various things to make next dungeon more difficult.
		# update settings file accordingly so monster difficulty scales, etc.

class Dice():
	"""Create a variable sided die that can be rolled"""
	def __init__(self):
		self.last_roll = None
		self.dice_text = ''

	def roll(self, sides=6):
		roll = randint(1, sides)
		self.last_roll = roll
		return roll

	def print_roll(self, mods=None):	# mods is not actually being used at all
		text = 'ROLLING...'
		for c in text:
			print(c, end='', flush=True)
			time.sleep(0.06)	
		print(' {}'.format(self.last_roll)) # use lambda here to put 'if mods' inside line?
		if mods:
			print('+{}'.format(mods))

class Weapon():
	"""Generates a weapon object with type and damage"""
	def __init__(self, name, damage):
		self.name = name
		self.damage = damage
		self.icon = self.get_dam_icon()

	def modify_weapon(self, add_to_damage):
		self.name += '++'
		self.damage += add_to_damage

	def print_stats(self):
		print('*** WEAPON INFO ***')
		#print()
		print('TYPE{:.>15}'.format(self.name))
		print('DAMAGE{:.>13}'.format(self.damage))

	def get_dam_icon(self):
		return '(1d' + str(self.damage) + ')'

class Armor():
	"""only instantiated as an attribute of player class"""
	def __init__(self, name, armor_class):
		self.name = name
		self.armor_class = armor_class

	def modify_armor(self, add_to_ac):
		self.name += '++'
		self.armor_class += add_to_ac

	def print_stats(self):
		print('*** ARMOR INFO ***')
		print('TYPE{:.>14}'.format(self.name))
		print('AC{:.>16}'.format(self.ac))

class Player():
	"""Generates the user character"""

	def __init__(self, settings):
		self.settings = settings

		self.created = False
		self.dead = False

		self.info = {'Name':'None', 'Race':''}

		# starting values for player game attributes
		self.name = self.info['Name']
		self.level = 1
		self.hp = 10		# current in game hp amount
		self.max_hp = 10	# current max hp for player level
		self.gold = 10
		self.exp = 10	# set on creation of player object
		self.next_level_at = self.get_level_up_val()  # determined on creation of player object

		# checks will need to be done in game loop to see if player's current exp is > than level_up, and if so,
		# we need to call a level up function AND ALSO call a function to increase 'level_up' attribute to next
		# setting (so next level-up occurs at higher exp amount, etc).

		self.dice = Dice()

		# player items
		self.potions = []
		self.items = ['Torch',]
		self.weapon = Weapon('Dagger', 4)
		self.armor = Armor('Leather', 10)

		# player location on grid. continually updated during gameplay.
		self.player_location = [(self.settings.grid_size - 1), (int(self.settings.grid_size / 2) - 1)]
		self.previous_coords = [0,0]

	def get_level_up_val(self):
		if self.level == 1:
			return 100
		if self.level == 2:
			return 220
		if self.level == 3:
			return 350
		if self.level > 3:
			return (2 * self.exp)	# think through / clarify this math here. can you use it throughout?

	def build_player(self):
		clear_screen()

		a = input('What is the name of your character? ')
		b = input('What is the Race of your character? ')

		self.info['Name'] = a.title()
		self.info['Race'] = b.title()

		clear_screen()

		print('You have successfully created {} the {}.'.format(a.title(), b.title()))
		print('You will begin with {} Hit Points and {} Gold Pieces.'.format(self.hp, self.gold))
		print('\nYou are now ready to start the game!')

		press_enter()

	def print_player_info(self):
		"""display all player stats on the screen"""
		clear_screen()

		print("#    PLAYER INFO    #\n")
		print("Name{:.>17} ".format(self.info['Name']))
		print("Race{:.>17} ".format(self.info['Race']))
		print("Level{:.>16} ".format(self.level))
		print("Hit Points{:.>11} ".format(self.hp))
		print("Gold Pieces{:.>10} ".format(self.gold))
		print("Experience{:.>11} ".format(self.exp))
		print("Next Level{:.>11} ".format(self.next_level_at))

		press_enter()

	def show_inventory(self):
		"""Prints player inventory screen"""
		clear_screen()

		# you have this redundant usage of player items. You could just access weapon
		# and armor info directly from the objects themselves, but instead you're doing 'inventory'.
		print("#      INVENTORY      #\n")
		print("Weapon{:.>17} ".format(self.weapon.name + self.weapon.icon))
		print("Armor{:.>18} ".format(self.armor.name))
		print("Items{:.>18} ".format(self.items[0])) # how to show all list items here ?
		print()
		print("#       POTIONS       #\n")
		
		count = 1
		for potion in self.potions:
			print('#{}  {}'.format(count, potion))
			count += 1

		press_enter()

	def reset_player(self):
		"""reset the player, triggered on exit of active game"""
		# this will probably need modification once saving and loading are introduced!

		self.player_location = [(self.settings.grid_size - 1), (int(self.settings.grid_size / 2) - 1)]

		self.level = 1
		self.hp = 10
		self.max_hp = 10
		self.gold = 10
		self.exp = 0
		self.next_level_at = self.get_level_up_val()

		self.potions = []
		self.weapon = Weapon('Dagger', 4)
		self.armor = Armor('Leather', 10)

		self.dead = False

class Monster():
	"""Generate a monster object for battle sequences, diff parameter determines difficulty"""

	def __init__(self, difficulty):
		self.difficulty = difficulty # add some randomization of difficulty here
		self.diff_string = self.get_diff_string()
		
		self.dice = Dice()	# constructs a die object by calling Dice class

		self.advantage = False	# determines who gets first attack, player or monster

		self.damage_roll = self.get_damage_roll()
		self.armor_class = self.get_armor_class()

		self.name = self.get_monster_name()	# gets random name on construction
		self.hp = self.get_hit_points()		# gets HP depending on difficulty
		
	def get_armor_class(self):
		if self.difficulty == 1:
			return 7
		if self.difficulty == 2:
			return 11
		if self.difficulty == 3:
			return 14
		if self.difficulty == 4:
			return 16

	def get_diff_string(self):
		"""gets appropriate string based on difficult level int"""
		if self.difficulty == 1:
			return 'EASY'
		if self.difficulty == 2:
			return 'MEDIUM'
		if self.difficulty == 3:
			return 'HARD'
		if self.difficulty > 3:
			return 'ELITE'

	def get_monster_name(self):
		"""import name file, grab a name at random, return it -- all based on difficulty level"""

		if self.difficulty == 1:
			filename = 'text_files/easy_monsters.txt'

			with open(filename, encoding='utf-8') as file_object:
				monster_names = file_object.read().split()

			index = randint(0, len(monster_names) - 1)
			return monster_names[index]

		elif self.difficulty == 2:
			filename = 'text_files/medium_monsters.txt'

			with open(filename, encoding='utf-8') as file_object:
				monster_names = file_object.read().split()

			index = randint(0, len(monster_names) - 1)
			return monster_names[index]

		elif self.difficulty == 3:
			filename = 'text_files/hard_monsters.txt'

			with open(filename, encoding='utf-8') as file_object:
				monster_names = file_object.read().split()

			index = randint(0, len(monster_names) - 1)
			return monster_names[index]

		elif self.difficulty > 3:
			filename = 'text_files/elite_monsters.txt'

			with open(filename, encoding='utf-8') as file_object:
				monster_names = file_object.read().split()

			index = randint(0, len(monster_names) - 1)
			return monster_names[index]

	def get_hit_points(self):
		if self.difficulty == 1:
			return self.dice.roll(4)
		elif self.difficulty == 2:
			return ((self.dice.roll(6)) + 2)
		elif self.difficulty == 3:
			return ((self.dice.roll(10)) + 4)
		elif self.difficulty > 3:
			return ((self.dice.roll(20)) + 10)

	def print_stats(self):
		print('# MONSTER STATS       #')     #23 chars
		print('NAME:{:.>18}'.format(self.monster_name.upper()))
		print('DIFF LEVEL:{:.>12}'.format(self.diff_string))
		print('HP:{:.>20}'.format(self.hp))
		print('AC:{:.>20}'.format(self.ac))
		print()

	def get_damage_roll(self):
		"""determine damage roll of monster via difficulty level"""
		if self.difficulty == 1:
			return 4
		if self.difficulty == 2:
			return 6
		if self.difficulty == 3:
			return 8
		if self.difficulty > 3:
			return 10

class GameLog():
	"""an object that contains the game log and displays its contents as necessary"""
	def __init__(self, player, grid):
		self.player = player
		self.grid = grid
		self.room_book = self.make_room_book()
		self.room_book_visited = self.make_room_book_visited()
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
				self.current_message = self.room_book['Start']
			elif self.grid.current_room_type == 'Empty':
				self.current_message = self.room_book['Empty']
			elif self.grid.current_room_type == 'Monster':
				self.current_message = self.room_book['Monster']
			elif self.grid.current_room_type == 'Treasure':
				self.current_message = self.room_book['Treasure']
			elif self.grid.current_room_type == 'Mystic':
				self.current_message = self.room_book['Mystic']

		# do you really need to separate the exit text like this?

		elif self.grid.current_room_type == 'Exit':		# doesn't matter if Visited is True or False, Exit always presents the same.
				self.current_message = self.room_book['Exit']

		# room_status = True, room has already been visited: use the visited dictionary of texts.
		else:
			if self.grid.current_room_type == 'Start':
				self.current_message = self.room_book_visited['Start']
			elif self.grid.current_room_type == 'Empty':
				self.current_message = self.room_book_visited['Empty']
			elif self.grid.current_room_type == 'Monster':
				self.current_message = self.room_book_visited['Monster']
			elif self.grid.current_room_type == 'Treasure':
				self.current_message = self.room_book_visited['Treasure']
			elif self.grid.current_room_type == 'Mystic':
				self.current_message = self.room_book_visited['Mystic']

		return self.current_message	

	def print_log(self):
		"""prints the header, the current dungeon grid, and the current log text entry"""
		
		# print header stats
		print('{} the {} \t HP: {}  GOLD: {}  EXP: {}\t ROOM: {}'.format(self.player.info['Name'].upper(), self.player.info['Race'], \
			self.player.hp, self.player.gold, self.player.exp, self.current_room))

		# print game map
		self.grid.print_grid()

		# game log
		print(self.current_message)

	def make_room_book(self):
		"""assign a dictionary of room text to room_book attribute"""

		filename = 'text_files/room_book.txt'
		with open(filename, encoding='utf-8') as file_object:
			room_text = file_object.read().split('X')

		room_dict = {
		'Start':room_text[0],
		'Empty':room_text[1],
		'Monster':room_text[2],
		'Treasure':room_text[3],
		'Mystic':room_text[4],
		'Exit':room_text[5],
		}

		return room_dict

	def make_room_book_visited(self):
		"""make the dictionary object of room text for already visited rooms"""

		filename = 'text_files/room_book_visited.txt'
		with open(filename, encoding='utf-8') as file_object:
			room_text_b = file_object.read().split('X')

		room_dict_b = {
		'Start':room_text_b[0],
		'Empty':room_text_b[1],
		'Monster':room_text_b[2],
		'Treasure':room_text_b[3],
		'Mystic':room_text_b[4],
		'Exit':room_text_b[5],
		}

		return room_dict_b

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

# define game UI functions.

def you_are_dead(player, text=''):
	if text:
		print(text)

	print('YOU', end='', flush=True)
	time.sleep(0.5)
	print('\tARE', end='', flush=True)
	time.sleep(0.5)
	print('\tDEAD.', end='', flush=True)

	print('So passes {} the {} into the endless night.'.format(player.info['Name'], player.info['Race']))

	press_enter()

def step_printer(word, speed=0.06):
	"""call whenever you want to print a word in steps"""
	#not modifying the word, so no need to index it
	for c in word:
		print(c, end='', flush=True)
		time.sleep(speed)

	# old index version
	#for c in range(len(word)):
	#	print(word[c], end='', flush=True)
	#	time.sleep(speed)

def slow_print_two(word_one, word_two):
	"""call to print one word, pause, then the second word"""
	print(word_one, end='', flush=True)
	time.sleep(0.08)
	print(word_two)

def slow_print_elipsis(word_one, word_two, elip=6):
	"""prints word one, then step prints elipsis, then prints word two"""
	elipsis = ('.' * elip)
	
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
	print('Type the first letter of a command') 
	print('at the game prompt (>).')

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
		return None 			# no loop is necessary in this function because run_game's call to this func gets None,
								# therefore has no other action to perform, so it (run_game body loop) loops, calling 
								# this function again. 

def get_player_input():
	msg = '\n> '
	player_input = input(msg)
	return player_input

def get_input_valid(text=None, key='standard'):
	"""a version of input function that also performs input validation"""
	# always put key=... in a call to this function

	if text:
		print(text)

	command = ''	# initialize command as empty string
					# not necessary, but clean...

	possible_choices = get_possible_choices(key)
	
	valid = False

	while not valid:

		command = input('\n> ')

		if command not in possible_choices:
			print('You did not enter a valid command, try again.')
		else:
			valid = True

	return command

def get_possible_choices(key):

	#possible_choices = []

	if key == 'standard':
		possible_choices = ['n','s','e','w','i','b','c','d','q']
	elif key == 'battle':
		possible_choices = ['attack','standard','headshot','s','h','c','p','i','b']
		possible_choices += ['finesse','fin','flurry','flu']

		# you need to add the menu options for battle mode: commands, potions, items, etc.


		# think of it like this: this place is the 'master set' of valid commands.
		# inside the actual game functions, you will parse the inputs to perform the
		# corresponding actions, *always knowing that a valid command has already been 
		# entered*.

	# add more as needed here

	return possible_choices

def press_enter(text=None):
	if text:
		print(text)
	msg = '\n...'
	input(msg)

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

# define main 'game in play' functions

def action_menu(game_log):
	"""print the game_log, the map, the command menu, take user input, and Return user choice"""

	clear_screen()
	game_log.print_log()	# this is THE print command of the game header -and- game map !! 
							# if you want to create loops that keep header active, you'll either need to figure out
							# how and where to move this, or call it more than once.
	
	possible_choices = ['c', 'n', 's', 'e', 'w', 'r', 'i', 'b', 'q', 'd']
	
	command = get_player_input().lower()

	if command in possible_choices:
		return command
	else:
		print('\nYou have entered an invalid command, try again.')
		press_enter()
		return None

	# note: the input validation performed here doesn't need to be in a while loop, because the
	# function that calls this function, game_action, has a while loop that essentially handles that.
	# if player gets the else statement above for invalid input, we fall back to game_action, which
	# has nothing left to do (command == None), so it loops, and this function is called again.

def game_action(settings, player, grid, game_log, dice):

	grid.update_player_location() # needs to happen here initially so the X gets printed to board
	game_log.update_log() # same, needs to happen so its attributes are not in initial state 'None'

	active = True
	
	while active:
		# main game event loop for *game in state of play* (as opposed to game at main menu, not in play)

		command = action_menu(game_log)
		movement_choices = ['n','s', 'e', 'w']

		if command in movement_choices:
			if movement_engine(settings, player, grid, command):	# True response = player moved on board
				grid.update_player_location()
				grid.update_current_roomtype()
				game_log.update_log()

				# check if movement into new room triggers an event, and if so, trigger it.
				determine_next_event(settings, player, grid, game_log, command)

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
			"""show player the available game commands they can use"""
			command_menu(player)

		elif command == 'q':
			print('Returning to Main Menu...')
			time.sleep(0.5)
			player.reset_player()	#reset player so new game starts fresh, attributes back to initials
			#reset_grid()	# I think this is not needed; grid is constructed when menu action 2 is chosen, so will be new.
			#reset_log()	# same as grid
			active = False

		else:
			pass

		if check_player_status(settings, player): 	# if True, player is dead, end action event loop.
			active = False
			player.reset_player() # needs to be reset for new game start
			print('Returning to Main Menu...', flush=True)
			time.sleep(0.8)
		
		else:
			pass

		# need to perform checks here to see if player exited floor of dungeon on this turn.
		# if so, we need to udpate settings (difficulty, etc) and update grid to create the next level of the dungeon
		# Q: do we actually create a new dungeon object? or modify the existing one? which makes more sense?	

		# if active:		# in case anything else needs to happen here, but probably there shouldn't be.

def check_player_status(settings, player): # seems we don't actually need settings ? 
	"""check in every pass of game action event loop to see if player status has changed in a way that triggers event"""

	# check if player is alive
	if player.hp <= 0:
		player.dead = True
		print('\nOh damn! Looks like {} has been defeated!'.format(player.info['Name']))
		time.sleep(0.6)
		print('\nGAME',end='',flush=True)
		time.sleep(0.8)
		print(' OVER.')
		press_enter()
		
		return True

	# check if player has levelled up... surely this needs to be its own function, and probably a method of
	# the player class...

	if not player.dead:
		if player.exp >= player.next_level_at:
			player.level += 1
			player.next_level_at = player.get_level_up_val()

			clear_screen()
			text = '**** {} LEVELS UP! ****'.format(player.info['Name'].upper())
			step_printer(text, 0.04)
			time.sleep(0.8)
			print()
			print('\n{} is now Level {}. Awesome!'.format(player.info['Name'], player.level), flush=True)
			player.max_hp += 4  
			time.sleep(0.8)
			print('\nHP has been increased to {}'.format(player.hp))
			
			press_enter()

	return False

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
				# player entered 2, so we call game_action, which is the main 'game in play' function:
				game_action(settings, player, grid, game_log, dice) 
				# note all the locations the arguments in game_action() call are being drawn from... they're all over the place!
				# that's because of Python's weird scope rules.
				# you'd think, logically / organizationally, that this function (run_game) could only pass objects that had
				# already been passed to it. and yet....but read through it all again: dice is the only outlier!
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

	grid.all_room_grid[player.previous_coords[0]][player.previous_coords[1]]['Visited'] = True

	return True

def determine_next_event(settings, player, grid, game_log, command):
	"""determine event that should occur on entering Room, and trigger that event"""
	direction = ''

	if command.lower() == 'n':
		direction = 'North'
	elif command.lower() == 's':
		direction = 'South'
	elif command.lower() == 'w':
		direction = 'West'
	elif command.lower() == 'e':
		direction = 'East'

	# we could look directly at the room dictionary stored in the all_room_grid, but it's less code to simply
	# look at the 'current_room_type' attribute of the grid, which is based on that same info anyway.

	move_text = ('Moving {}'.format(direction.title()))

	slow_print_elipsis(move_text, '', 4)

	if grid.current_room_type == 'Empty' and grid.room_status != True: # bypass print for already visited rooms.
		slow_print_elipsis('This room', 'is EMPTY.')
		time.sleep(0.8)
	elif grid.current_room_type == 'Treasure' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a TREASURE chest!')
		time.sleep(0.8)
		treasure_event(settings, player)
	elif grid.current_room_type == 'Exit' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a staircase going DOWN!')
		time.sleep(0.8)
		exit_event()
	elif grid.current_room_type == 'Mystic' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a MYSTIC!')
		time.sleep(0.8)
		mystic_event()
	elif grid.current_room_type == 'Monster' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a MONSTER!')
		time.sleep(0.8)
		battle_event(settings, player, grid, game_log)
	else:
		slow_print_elipsis('This room', 'seems familiar.')
		time.sleep(0.8)	# this else will only occur if the room being entered has already been visited.


# define room event functions -- triggered on entering unvisited room.

def treasure_event(settings, player):

	if settings.difficulty == 1:
		treasure_roll = randint(1, 5)

	if settings.difficulty > 1 and settings.difficulty < 3:
		treasure_roll = (randint(1, 8) + 2)

	if settings.difficulty > 3:
		treasure_roll = (randint(1, 10) + 3)

	step_printer('OPENING CHEST...')
	print('You found {} Gold Pieces inside!'.format(treasure_roll))

	player.gold += treasure_roll

	time.sleep(0.6)
	print('{} GP +{}'.format(player.info['Name'], treasure_roll))
	press_enter()

def mystic_event():
	clear_screen()
	print('A an apparition is forming in the center of this room...')
	time.sleep(0.8)
	print('It takes on a ghostly human shape, and speaks to you!')
	time.sleep(0.8)
	print('WOULD YOU LIKE TO BUY A MAGIC ELIXIR...?')

	response = get_player_input()

	press_enter()

def exit_event():
	print('An exit event is now triggered!')
	press_enter()

def battle_event(settings, player, grid, game_log):
	# create a monster
	monster = Monster(settings.difficulty)
	encounter_monster(player, monster, grid, game_log)

# define all Battle functions

def encounter_monster(player, monster, grid, game_log):
	"""monster is engaged and decision to fight or run is chosen by player"""
	clear_screen()

	# determine how difficult it is for player to run away successfully
	run_difficulty = int(randint(2,10) + (3 * monster.difficulty))

	run_failed = False

	active = True
	
	# step print encounter text	
	slow_print_elipsis('You have encountered a', monster.name.upper())

	print('Run Difficulty: {}'.format(run_difficulty))

	while active:

		command = get_player_input()

		possible_choices = ['fight', 'run', 'f', 'r']

		if command not in possible_choices:
			print('You did not enter a valid command, try again.')
		else:
			# this if has no else case
			if command.lower().startswith('r'):
				if run_attempt(player, run_difficulty):
					# run was successful, exit encounter loop and do not start battle.
					active = False
					print('You successfully run away from the {}!'.format(monster.name))
					time.sleep(0.8)
					print('You will now return to the previous room.')
					press_enter()

					# make current room (one being run out of) grid icon change back to a *
					grid.grid_matrix[player.player_location[0]][player.player_location[1]] = ' * '
					# move player coords equal that of previously visited room
					player.player_location = player.previous_coords.copy()

					# update everything since room has reverted
					grid.update_player_location()
					grid.update_current_roomtype()
					game_log.update_log()


					# NOTE: Player never 'moved' (entered move command) to leave this room, we just
					# force them back in next lines. movement_engine() function is where previous room
					# gets set to Visited = True, but that will NOT have happened in this situation,
					# because they never 'moved' out of it. So, it should remain Visited = False, which
					# is actually what we want anyway.

				else:
					# will be used to have monster attack first
					run_failed = True
					print('You failed to run away from the {}!'.format(monster.name))
					print('Now you must fight!')
					press_enter()

			if command.lower().startswith('f') or active:
				# end the encounter loop and start the battle
				active = False
				battle_main(player, monster, run_failed)
						
def run_attempt(player, run_difficulty):
	"""rolls player dice, prints out roll, returns True if roll beats run_dc, False otherwise"""
	roll = player.dice.roll(20)
	player.dice.print_roll()
	return (roll >= run_difficulty)		# returns a bool

def battle_main(player, monster, run_failed):

	turn = 0
	round_num = 1
	fight_mods = {'enemy_armor': 0, 'player_roll': 0, 'player_damage': 0}

	atype = {'attack': None}
	crits = {'crit': False}
	player_turn = True
	
	if run_failed:
		player_turn = False

	active = True

	while active:

		battle_header(player, monster, round_num)

		# player attack 
		if player_turn:

			if player_attack(player, monster, fight_mods, round_num, crits, atype):
				if not crits['crit']:
					player_damage(player, monster, fight_mods, atype)
				else:
					pass

			player_turn = False

		# monster attack
		else: 

			if monster.hp > 0:
				if monster_attack(player, monster, round_num):
					monster_damage(player, monster)

			player_turn = True

		# status check on both player and monster
		if check_battle_status(player, monster, crits):
			active = False	# player or monster is dead, so end the battle loop.

		# run updates if the battle is still going
		if active:
			press_enter()		# first of two calls to press_enter, for pause between ongoing loops
			turn += 1
			if turn % 2 == 0:
				round_num += 1
			crits['crit'] = False 	# reset crit. kinda inefficient.

			# reset the fight mods and atype so each round of battle starts with empty mods.
			fight_mods['enemy_armor'] = 0
			fight_mods['player_roll'] = 0
			fight_mods['player_damage'] = 0
			atype['attack'] = None

		elif not active:					# shouldn't this be the same result as just 'else'? but it didn't work...
			print('The battle is over!')
			press_enter()	#  second of two calls to press_enter, for pause before ending battle sequence.
			# clear_screen()

def print_battle_commands():
	"""print a screen showing all possible commands in battle"""
	clear_screen()

	print('*****              ATTACK TYPES              *****') # 31 characters used
	print()
	print('STANDARD (S):')
	print('A normal attack. No mods to attack or damage rolls.')
	print()
	print('HEADSHOT (H):')
	print('Aim for the head! Enemy AC gets +4 but if you hit,')
	print('you deal double damage.')
	print()
	print('FLURRY  (FLU):')
	print('Run in mad and flailing! Easier to hit enemy (Roll +3),') 
	print('but you usually deal less damage: damage roll gets a')
	print('random 0 to 3 penalty.')
	print()
	print('FINESSE (FIN):')
	print('A deliberate attack, going for a weak point. Slightly')
	print('harder to hit (Enemy AC +2) but success means +2 to ')
	print('your damage roll.')
	print('\n')
	print('Type the name (or shortcut) of attack to enter command.')
	print()
	press_enter()

def battle_header(player, monster, round_num):
	clear_screen()
	print('ROUND: {}'.format(round_num))
	print('{: <12} \t HP: {: <3} AC: {: <3} \t WEP: {}{}'.format(player.info['Name'].upper(), player.hp, player.armor.armor_class, player.weapon.name, player.weapon.icon))
	print('{: <12} \t HP: {: <3} AC: {: <3}'.format(monster.name.upper(), monster.hp, monster.armor_class))
	print()

def check_battle_status(player, monster, crits):
	"""checks state of player and monster to determine if battle is over, or should continue"""
	
	#check player
	if player.hp <= 0:
		print('\nYou have been defeated by the {}!'.format(monster.name))
		player.dead = True
		time.sleep(0.8)
		return True

	elif monster.hp <= 0:
		if not crits['crit']:
			print('\nYou have destroyed the {}!'.format(monster.name))
		else:
			print()	# this may not be necessary, need to playtest on critical hit success for line spacing.

		time.sleep(0.8)
		gain_exp(player, monster)
		time.sleep(0.8)
		return True
	
	else:
		# neither player nor monster has been defeated, fight will continue.
		return False

def player_attack(player, monster, fight_mods, round_num, crits, atype):
	"""runs all player attack functions and returns a bool to call in battle_main function"""

	command = attack_menu_input(player, monster, fight_mods, round_num)

	# if applicable, fight_mods will be updated by this call
	compute_attack_mods(player, monster, fight_mods, command, atype)

	# compute_potion_mods(player)

	# here is the actual attack die roll...
	roll = player.dice.roll(20)
	player.dice.print_roll()
	
	# check if roll is a critical hit
	if roll == 20:
		print('CRITICAL HIT!')
		print('The {} has been destroyed by your perfectly placed strike!'.format(monster.name))
		monster.hp = 0
		crits['crit'] = True # used as flag to skip damage roll after critical hit
		return True

	# check if there are fight mods to Player Roll to display on screen
	# note: headshot doesn't appear here because it mods Enemy AC, not the player roll!

	if atype['attack'] == 'flurry' and not crits['crit']: # don't show mods on a critical hit
		total = roll + fight_mods['player_roll']
		time.sleep(0.6)
		print('+{} ({})'.format(fight_mods['player_roll'], 'flurry bonus')) 
		time.sleep(0.6)
		print('= {}'.format(total))

	elif (atype['attack'] == 'finesse' or atype['attack'] == 'standard') and not crits['crit']:
		pass # no mods to Player Roll on a standard or finesse attack.

	# check if hit was successul or not
	if roll + fight_mods['player_roll'] >= monster.armor_class + fight_mods['enemy_armor']:
		print('You successfully hit the {} with your {}!'.format(monster.name, player.weapon.name))
		return True

	else:
		print('Your attack missed the {}, dang!'.format(monster.name))
		return False

def attack_menu_input(player, monster, fight_mods, round_num):
	"""gets player input for player attack in a battle"""

	command = ''	# again, just for C style initialization; not necessary

	active = True

	while active:

		battle_header(player, monster, round_num)	# called because menu calls will clear screen

		print('Choose your attack...')

		command = get_input_valid(key='battle')

		# accessing menu keeps loop running; any other input exits loop and proceeds to attack

		if command == 'c':
			print_battle_commands()
		elif command == 'p':
			print('This is how you will use a potion, eventually.')
			press_enter()
		elif command == 'i':
			print('This would show player inventory.')
			press_enter()
		elif command == 'b':
			print('And this would show player bio....')
			press_enter()
		else:
			active = False	# non-menu command entered, exit loop so battle can proceed.

	return command

def compute_attack_mods(player, monster, fight_mods, command, atype):

	attack_words = ['standard','s','attack'] # all result in standard attack

	# headshot
	if command.lower() == 'headshot' or command.lower() == 'h':
		atype['attack'] = 'headshot'
		fight_mods['enemy_armor'] = 4
		fight_mods['player_damage'] = 5

		print('Headshot attempt!')
		time.sleep(0.6)
		print('The {}\'s AC is increased to {} on this attack!'.format(monster.name, monster.armor_class + fight_mods['enemy_armor']))
		time.sleep(0.6)
	
	elif command.lower() == 'finesse' or command.lower() == 'fin':
		atype['attack'] = 'finesse'
		fight_mods['enemy_armor'] = 2
		fight_mods['player_damage'] = 2

		print('Finesse attack!')
		time.sleep(0.6)
		print('The {}\'s AC is increased to {} on this attack.'.format(monster.name, monster.armor_class + fight_mods['enemy_armor']))
		time.sleep(0.6)

	elif command.lower() == 'flurry' or command.lower() == 'flu':
		atype['attack'] = 'flurry'
		damage_penalty = randint(0, 3)

		fight_mods['player_roll'] = 3
		fight_mods['player_damage'] = (-damage_penalty)

		print('Flurry attack!')
		time.sleep(0.6)
		print('Attack roll will get +{} but damage will get -{}'.format(fight_mods['player_roll'], damage_penalty))
		time.sleep(0.6)

	# normal attack; could use 'else' but I might add more possible choices later.
	elif command.lower() in attack_words:
		atype['attack'] = 'standard'
		#print('Standard attack')
		#time.sleep(0.6)

def player_damage(player, monster, fight_mods, atype):

	# non-headshot attack damage roll
	if atype['attack'] != 'headshot':
		damage = player.dice.roll(player.weapon.damage) + fight_mods['player_damage']

		# prevent negative damage from flurry + a low roll
		if damage <= 0:
			damage = 1

	# headshot damage roll (different because it's the only one with multiplication)
	else:
		damage = player.dice.roll(player.weapon.damage) * 2
	
	# print damage roll
	player.dice.print_roll()

	if atype['attack'] == 'headshot':
		time.sleep(0.6)
		print('x2 (headshot bonus)')
		time.sleep(0.6)
		print('= {}'.format(damage))

	elif atype['attack'] == 'flurry' and fight_mods['player_damage'] != 0:
		time.sleep(0.6)
		print('{} (flurry penalty)'.format(fight_mods['player_damage']))
		time.sleep(0.6)
		print('= {}'.format(damage))

	elif atype['attack'] == 'finesse':
		time.sleep(0.6)
		print('+{} (finesse bonus)'.format(fight_mods['player_damage']))
		time.sleep(0.6)
		print('= {}'.format(damage))
	else:
		pass # standard attack prints no modifiers

	print('You dealt {} points of damage to the {}'.format(damage, monster.name.upper()))

	monster.hp -= damage

	# this is here simply so the header doesn't show a negative number for monster hp
	# after monster is defeated.
	if monster.hp < 0:
		monster.hp = 0
		
def monster_attack(player, monster, round_num):

	# put here to be consistent with player attack
	battle_header(player, monster, round_num)

	print('The {} is attacking you!'.format(monster.name))

	# time.sleep() here ?

	roll = monster.dice.roll(20)
	monster.dice.print_roll()

	if roll == 20:
		print('CRITICAL HIT, OUCH!')
		print('Automatic 5 points of damage, plus normal damage roll.')
		player.hp -= 5
		return True

	if roll > player.armor.armor_class:
		print('The {}\'s attack hits you!'.format(monster.name))
		return True
	else:
		print('The {}\'s attack misses you, phew!'.format(monster.name))
		return False

def monster_damage(player, monster):

	damage = monster.dice.roll(monster.damage_roll)

	monster.dice.print_roll()

	print('You take {} points of damage!'.format(damage))

	player.hp -= damage

def gain_exp(player, monster):
	"""award experience to player for beating a monster"""

	exp = ((monster.difficulty * 10) + randint(0,10))
	player.exp += exp

	#any gain of exp always prints a message about the gain...might need to decouple the two.
	print('You gained {} experience points.'.format(exp))
	time.sleep(0.08)

# instantiate game objects

# how do I make these not be global variables? should I have a 'build start objects' function
# that is called before run_game? 

settings = GameSettings()
player = Player(settings)
dice = Dice()

# call the main run_game function loop
run_game(settings, player)



