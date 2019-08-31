import time
from random import randint, choice
import copy

from ui_functions import *

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

	def reset_settings(self):
		"""called when player dies or active game is quit"""
		self.grid_size = 5
		self.starting_gold = 10
		self.difficulty = 1

	def print_settings(self):
		"""dev feature to confirm if settings are getting udpated"""
		clear_screen()
		print('Grid Size: {}'.format(self.grid_size))
		print('Starting Gold: {}'.format(self.starting_gold))
		print('Difficulty: {}'.format(self.difficulty))

class GameGrid():
	"""Creates a grid object for the game of variable size"""

	floor_level = 0		# class attribute 

	def __init__(self, settings, player):

		self.__class__.floor_level += 1	

		self.floor_chrono = self.__class__.floor_level # order floor was created among all floors, e.g. 1 = first, 2 = second, etc.
		self.settings = settings
		self.player = player

		self.row = self.settings.grid_size		# grid size based on current settings
		self.col = self.settings.grid_size

		self.floor_exited = False

		self.grid_matrix = self.make_grid()			# grid for graphics, containing strings '*'
		self.all_room_grid = self.generate_rooms()  # grid for room data, containing room dictionaries

		self.create_start() # same as below, adds start on construction
		self.create_exit()	# doesn't need to return anything, just adds the exit on construction
		self.create_mystic() # number of mystics = floor level, perhaps give it a +1 as well (after floor one)
		
		self.current_room_type = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Type'] 
		
		# this is a bool and is used to track if current inhabited room was previously visited or not
		# and yes, you could perform this check by checking the all_room_grid and looking at 'Visited' bool directly.
		self.room_status = self.all_room_grid[self.player.player_location[0]][self.player.player_location[1]]['Visited']

	def reset_floor_level(self):
		"""we need to call this on player death or game quit, otherwise grid instance on restart picks up from last point"""
		self.__class__.floor_level = 1

		# or, instead of calling this, simply add a line of code to set GameGrid.floor_level to 0 *before* instantiating 
		# a grid object.

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

		# this is as close as I initially got to a 'state' variable. the grid object constantly updates the 
		# 'room type' attribute and 'room status' attribute to reflect 'current state' of player location.
		# but it's all just based on the dictionary contents stored in the dictionary that resides at coordinates
		# where player is currently located.

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

		# create as many mystics as = the level of the dungeon

		# level one will always have one mystic
		if self.__class__.floor_level == 1:
			active = True

			while active:

				random_x = randint(0, self.row - 1)
				random_y = randint(0, self.col - 1)
				
				coords = [random_x, random_y]

				if coords != self.player.player_location and self.all_room_grid[random_x][random_y]['Type'] != 'Exit':
					self.all_room_grid[random_x][random_y]['Type'] = 'Mystic'
					self.all_room_grid[random_x][random_y]['Mystic_Closed'] = False # adds this key-val pair to grid dictionary
					active = False
				else:
					pass

		# floors beyond level 1 will have a quanity of mystics equal to floor level, + a random amount added.
		elif self.__class__.floor_level > 1:

			extra_mystics = randint(0, 2)

			for level in range(self.__class__.floor_level + extra_mystics):

				active = True

				while active:

					random_x = randint(0, self.row - 1)
					random_y = randint(0, self.col - 1)
					
					coords = [random_x, random_y]

					if coords != self.player.player_location and self.all_room_grid[random_x][random_y]['Type'] != 'Exit':
						self.all_room_grid[random_x][random_y]['Type'] = 'Mystic'
						self.all_room_grid[random_x][random_y]['Mystic_Closed'] = False # will add this key-val pair only to mystic rooms
						active = False
					else:
						pass

	def print_grid(self):
		"""print the visual game grid"""
		
		print('\nLV.{}'.format(self.floor_level))	# will find the class attribute floor_level after looking at instance attributes.

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
	def __init__(self, name, damage_roll, bonus=[]):
		self.name = name
		self.damage_roll = damage_roll
		self.icon = self.get_dam_icon()
		self.bonus = bonus

	def print_stats(self):
		print('*** WEAPON INFO ***')
		#print()
		print('TYPE{:.>15}'.format(self.name))
		print('DAMAGE{:.>13}'.format(self.damage))
		print()
		# add mods here

	def get_dam_icon(self):
		return '(1d' + str(self.damage_roll) + ')'

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
		self.escaping = False

		self.current_state = ''
		self.info = {'Name':'None', 'Race':''}
		self.potion_mods = {'player_attack': 0, 'player_damage': 0}

		# starting values for player game attributes
		self.name = self.info['Name']
		self.level = 1
		self.hp = 10		# current in game hp amount
		self.max_hp = 10	# current max hp for player level
		self.gold = 10
		self.exp = 0	# set on creation of player object
		self.next_level_at = self.get_level_up_val()  # determined on creation of player object

		self.dice = Dice()

		# player items
		self.elixirs = []
		self.items = ['Torch',]
		self.weapon = Weapon('Dagger', 4)
		self.armor = Armor('Warm Sweater', 9)

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
		print("Name{:.>17} ".format(self.info['Name']))		# FYI: the space after the {} appears to make no difference..?
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
		print("#      INVENTORY      #\n")   #23 spaces used here
		print("Weapon{:.>17}".format(self.weapon.name + self.weapon.icon))
		print("Armor{:.>18}".format(self.armor.name))
		print("Items{:.>18}".format(self.items[0])) # how to show all list items here ?
		print()
		print("#       ELIXIRS       #\n")
		
		if self.elixirs:
			count = 1
			for elixir in self.elixirs:
				print('{}{:.>22} '.format(count, elixir['Type'].title()))
				count += 1
			print()
		
		if self.elixirs:
			print()
			print('Use an item?   Yes | No')
			answer = get_input_valid(key='yes_no')

			if answer.startswith('n'):
				pass
			elif answer.startswith('y'):
				self.use_potion()
		else:
			press_enter()

	def reset_player(self):
		"""reset the player, triggered on exit of active game"""
		# this will probably need modification once saving and loading are introduced!
		
		self.player_location = [(self.settings.grid_size - 1), (int(self.settings.grid_size / 2) - 1)]
		self.previous_coords = [0,0]

		self.level = 1
		self.hp = 10
		self.max_hp = 10
		self.gold = 10
		self.exp = 0
		self.next_level_at = self.get_level_up_val()
		self.current_state = ''

		self.elixirs = []
		self.weapon = Weapon('Dagger', 4)
		self.armor = Armor('Leather', 10)
		self.potion_mods = {'player_attack': 0, 'player_damage': 0}
		self.dead = False
		self.escaping = False

	def use_potion(self):
		"""player uses a potion via the inventory screen"""

		response = ''
		current_max = len(self.elixirs)
		active = True

		while active:

			clear_screen()
			print('{}\'s ELIXIRS'.format(self.info['Name']))
			print()

			if self.elixirs:	# player has elixirs, following code is for printing and using one.

				# print the elixirs the player currently has
				count = 1
				for elixir in self.elixirs:
					print('{}{:.>22} '.format(count, elixir['Type'].title()))
					count += 1

				# create a flag for input validation
				potion_inventory_valid = False

				# input validation loop to avoid user selecting a potion # beyond their actual current items
				while not potion_inventory_valid:

					# get players choice: the number of a potion, or Q to quit this menu

					response = get_input_valid('\nEnter # of Elixir to use, or Q to quit.', 'battle_potion')

					#player chose a number higher than current inventory allows
					if response.lower() != 'q' and int(response) > current_max:
						print('You do not have an elixir stored at that number, try again.')
					
					# player entered either 'q' or a valid potion number, so we exit this validation loop
					else:
						potion_inventory_valid = True
				
				# now we check if what they entered was q, if it was, we quit by ending the main loop ('active')
				if response.lower() == 'q':
					print('Cool. Saving \'em for later. Smart!')	
					active = False

				# choice was not q, so it is string of an integer
				else: 
					# index the elixir list attribute of player, then index the Type key of that chosen dictionary

					response_int = int(response) - 1	# to account for player always entering 1 greater than actual index location

					#print('BTW, choice_int currently = {}'.format(choice_int))

					if self.elixirs[response_int]['Type'] == 'health':
						bonus = 5 * self.elixirs[response_int]['Strength']
						if self.hp + bonus > self.max_hp:
							self.hp = self.max_hp
						else:
							self.hp += bonus

						time.sleep(0.06)
						step_printer('DRINKING ELIXIR...')
						print('\nYou drank the HEALTH elixir and gained {} hit points!'.format(bonus))

						del self.elixirs[response_int]
						active = False

					elif self.elixirs[response_int]['Type'] == 'health max':
						self.hp = self.max_hp

						time.sleep(0.06)
						step_printer('DRINKING ELIXIR...')
						print('\nYou drank the HEALTH MAX elixir and regained all your HP!')

						del self.elixirs[response_int]
						active = False

					elif self.elixirs[response_int]['Type'] == 'berzerk':

						if self.current_state != 'battle':
							print('The Berzerk Elixir is for use during a battle!')

						elif self.current_state == 'battle':
				
							bonus = 4
							self.potion_mods['player_attack'] += bonus
							self.potion_mods['player_damage'] += bonus
							time.sleep(0.06)
							print('You used a BERZERK elixir!')
							time.sleep(0.5)
							print('+4 attack roll')
							time.sleep(0.5)
							print('+4 damage roll')

							del self.elixirs[response_int]

							active = False

					elif self.elixirs[response_int]['Type'] == 'escape':

						if self.current_state != 'battle':
							print('The Escape Elixir is for use during a battle!')

						elif self.current_state == 'battle':

							print('You used an ESCAPE elixir!')
							time.sleep(0.5)
							print('You immediately flee this battle...')
							time.sleep(0.5)
							print('And return to the previous room.')
							time.sleep(0.5)

							del self.elixirs[response_int]

							self.escaping = True

			else: # player pressed p for potions but has none in their inventory at this time
				print('You do not have any Elixirs to use at this time, try to find some!')
				active = False

			press_enter()

class Monster():
	"""Generate a monster object for battle sequences, diff parameter determines difficulty"""

	def __init__(self, difficulty):
		self.difficulty = difficulty 
		self.name = self.get_monster_name()	# NOTE: also determines actual level if diff is > 1
		
		self.diff_string = self.get_diff_string()
		
		self.actual_level = 1 # modified depending on result of 

		self.dice = Dice()	# constructs a die object by calling Dice class

		self.advantage = False	# determines who gets first attack, player or monster

		self.damage_roll = self.get_damage_roll()
		self.armor_class = self.get_armor_class()

		self.hp = self.get_hit_points()		# gets HP depending on difficulty
		
	def get_armor_class(self):
		if self.difficulty == 1:
			return randint(4, 8)
		if self.difficulty == 2:
			return randint(8, 11)
		if self.difficulty == 3:
			return randint(10, 15)
		if self.difficulty == 4:
			return randint(11, 17)

	def get_diff_string(self):
		"""gets appropriate string based on difficult level int"""
		if self.actual_level == 1:
			return 'EASY'
		if self.actual_level == 2:
			return 'MEDIUM'
		if self.actual_level == 3:
			return 'HARD'
		if self.actual_level > 3:
			return 'ELITE'

	def get_monster_name(self):
		"""import name file, grab a name at random, return it -- all based on difficulty level"""

		with open('text_files/easy_monsters.txt', encoding='utf-8') as file_object_1:
			easy_monsters = file_object_1.read().split()

		with open('text_files/medium_monsters.txt', encoding='utf-8') as file_object_2:
			medium_monsters = file_object_2.read().split()

		with open('text_files/hard_monsters.txt', encoding='utf-8') as file_object_3:
			hard_monsters = file_object_3.read().split()

		with open('text_files/elite_monsters.txt', encoding='utf-8') as file_object_4:
			elite_monsters = file_object_4.read().split()

		if self.difficulty == 1:
		
			index = randint(0, len(easy_monsters) - 1)
			self.actual_level = 1
			return easy_monsters[index]

		elif self.difficulty == 2:
			
			num = randint(1, 3)

			if num == 1:
				index = randint(0, len(easy_monsters) - 1)
				# need to actually change monster's difficulty level to match chosen monster type!
				self.actual_level = 1
				return easy_monsters[index]
			elif num > 1:
				index = randint(0, len(medium_monsters) -1)
				self.actual_level = 2
				return medium_monsters[index]

		elif self.difficulty == 3:

			num = randint(1, 6)

			if num == 1:
				index = randint(0, len(easy_monsters) - 1)
				self.actual_level = 1
				return easy_monsters[index]
			elif num > 1 and num < 4:
				index = randint(0, len(medium_monsters) -1)
				self.actual_level = 2
				return medium_monsters[index]
			elif num >= 4:
				index = randint(0, len(hard_monsters) -1)
				self.actual_level = 3
				return hard_monsters[index]

		elif self.difficulty > 3:

			num = randint(1, 9)

			if num == 1:
				index = randint(0, len(easy_monsters) - 1)
				self.actual_level = 1
				return easy_monsters[index]
			elif num > 1 and num < 4:
				index = randint(0, len(medium_monstes) -1)
				self.actual_level = 2
				return medium_monsters[index]
			elif num >= 4 and num < 7:
				index = randint(0, len(hard_monsters) -1)
				self.actual_level = 3
				return hard_monsters[index]
			elif num >= 7:
				index = randint(0, len(elite_monsters) -1)
				self.actual_level = 4
				return elite_monsters[index]

	def get_hit_points(self):
		if self.actual_level == 1:
			return self.dice.roll(4)
		elif self.actual_level == 2:
			return ((self.dice.roll(5)) + 2)
		elif self.actual_level == 3:
			return ((self.dice.roll(8)) + 4)
		elif self.actual_level > 3:
			return ((self.dice.roll(20)) + 9)

	def print_stats(self):
		print('# MONSTER STATS       #')     #23 chars
		print('NAME:{:.>18}'.format(self.name.title()))
		print('LEVEL:{:.>17}'.format(self.actual_level))
		print()
		print('HP:{:.>20}'.format(self.hp))
		print('AC:{:.>20}'.format(self.armor_class))
		print('DAMAGE:{:.>16}'.format(self.damage_roll))
		print()
		press_enter()

	def get_damage_roll(self):
		"""determine damage roll of monster via difficulty level"""
		if self.actual_level == 1:
			return 4
		if self.actual_level == 2:
			return 6
		if self.actual_level == 3:
			return 8
		if self.actual_level > 3:
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

		# do you really need to separate the exit text like this? You can show a 'visited' text for the Exit room,
		# the important thing is that the Exit event still gets triggered regardless of which room_book text is shown!

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