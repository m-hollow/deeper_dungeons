import time
from random import randint, choice
import copy

# define all classes used in game

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