import time
from random import randint

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
		print('ENEMY ENCOUTNER........E')

class GameGrid():
	"""Creates a grid object for the game of variable size"""
	def __init__(self, settings, player):
		
		self.settings = settings
		self.player = player

		self.row = self.settings.grid_size
		self.col = self.settings.grid_size

		self.grid_matrix = self.make_grid()
		self.all_rooms = self.generate_rooms()
		self.player_start = self.find_start_room(self.all_rooms, self.player.player_start_location)
		#self.exit_room = self.choose_exit_room()

		self.current_room_coords = self.player.player_location
		self.current_room_type = self.find_current_room(self.all_rooms, self.current_room_coords)

	def make_grid(self):
		# list comprehension to create matrix of the game grid

		grid_matrix = [[' * ' for x in range(self.col)] for y in range(self.row)]

		# update this to simply grab the info from the player_location list attribute
		# grid_matrix[self.player.player_location[0]][self.player.player_location[1]]

		grid_matrix[self.player.player_row][self.player.player_col] = ' X '

		return grid_matrix

	def generate_rooms(self):
		"""create a room for each cooridnate in the grid matrix"""
		all_rooms = []
		
		row_num = 0

		for r in self.grid_matrix:		# r is a list, but it's really just used as a range here

			col_num = 0
			
			for c in r:					# c is a string (literally a ' * ') but is also used as range here 
				room_type = self.get_room_type()
				room = {'Coords':[row_num, col_num], 'Type':room_type}
				all_rooms.append(room)
				col_num += 1

			row_num += 1

		return all_rooms

	def get_room_type(self):
		"""called by generate rooms function to make one random room"""
		room_type = ''
		num = randint(1,8)

		if num >= 1 and num <= 4:
			room_type = 'Empty'
		elif num >= 5 and num <= 7:
			room_type = 'Monster'
		elif num == 8:
			room_type = 'Treasure'
		
		return room_type

	def find_start_room(self, all_rooms, room_to_find):
		"""locate start room in grid based on player_start_location, label as such in room dictionary"""

		index = 1

		for room_dict in all_rooms:
			if room_dict['Coords'] == room_to_find:
				all_rooms[index-1]['Type'] = 'Start'
			else:
				pass

			index += 1

	def find_current_room(self, all_rooms, room_to_find):
		"""determine the type of the current room based on contrasting player coords and dungeon grid info"""

		index = 1
		current_room_type = ''

		for room_dict in all_rooms:
			if room_dict['Coords'] == room_to_find:
				current_room_type = room_dict['Type']

		return current_room_type

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

		self.info = {'Name':'', 'Race':''}
		self.stats = {'Level': 1, 'HP': 10, 'GOLD':self.settings.starting_gold}

		# the value for key Items needs to be a LIST. figure out how to implement / index
		self.inventory = {'Weapon':'None', 'Clothing':'Old Shirt', 'Items':'Torch'}

		# self.grid_max = self.settings.grid_size

		# below attributes are redundant, you could just type the code directly into player_location
		# BUT, if you do that, the grid class will need to be updated to get info from player_location
		# rather than these two attributes!
		# also raises a question of: if you update these in the movement() function, does the 
		# player location attribute update as well? I'm guessing -no-, it's only deteremined upon
		# instantation of the object instance, and must be updated manually after that.
		self.player_row = (self.settings.grid_size - 1)
		self.player_col = (int(self.settings.grid_size / 2) - 1 )

		# start location, fixed value for every new grid created, same as initial player row and col vals
		self.player_start_location = [self.settings.grid_size - 1, (int(self.settings.grid_size / 2) - 1)]
		#list of current coordinates for player, will constantly be modified
		self.player_location = [self.player_row, self.player_col]

	def build_player(self):
		"""fill dictionary with user character choices"""
		
		clear_screen()

		print("Let's build your character before starting.")
		
		press_enter()
		clear_screen()

		a = input('What is the name of your character? ')
		b = input('What is the Race of your character? ')

		self.info['Name'] = a.title()
		self.info['Race'] = b.title()

		clear_screen()

		print('You have successfully created {} the {}.'.format(a.title(), b.title()))
		print('You will begin with {} Hit Points and {} Gold Pieces.'.format(self.stats['HP'], 
			self.stats['GOLD']))
		print('\nIt\'s time to enter the dungeon!')

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


	def player_movement(self):
		"""function to move the players location on the grid"""

class GameLog():
	"""an object that contains the game log and displays its contents as necessary"""
	def __init__(self, grid):
		self.grid = grid
		self.room_book = RoomBook()
		self.current_room = self.grid.current_room_type
		# do we need self.current_message = '' ?
	
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
		"""This needs to be called continually to update room as current_room_type changes"""
		# otherwise gamelog room will just stay fixed at value obtained during construction
		self.current_room = self.grid.current_room_type

class RoomBook():
	"""An object that stores all the possible text strings for dungeon rooms"""
	def __init__(self): #  TODO: consider storing all text in an actual text file and reading from it. 
		"""stores all the text strings for each room type"""
		self.start_text = '''\nI'm at the entrance to the dungeon. I sure hope I find treasure inside, \nand not anything nasty!
		'''

		self.empty_text = '''\nI'm entering a large, dark room. Looking around, there appears to be nothing \ninside other than dust, debris and more dust. This room is empty.'''
		

		self.monster_text = '''\nI've entered a very dark room. Something is approaching...it's a Monster!
		'''

		self.treasure_text = '''\nI'm standing in a room with a very high ceiling. There's an alter at the \ncenter with something on top...it's treasure!'''
		

		self.exit_text = '''\nI'm standing in a long, narrow corridor. There's a large, engraded gate at the \nend of this passage. I think this must be the exit!'''

		# all the text entries stored in one dictionary, indexed by room type
		
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
				return int(choice)
			else:
				print('That\'s not one of the menu options!')

# define game functions.

def press_enter():
	msg = '\nOK...'
	input(msg)

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

#def player_moves():
#	"""receives player input for movement and updates class attributes accordingly"""

def run_game_log(player, game_log):	
	"""updates and prints the current gamelog"""

	game_log.update_room_type()
	current_msg = game_log.get_current_message()

	print('HP: {} GOLD: {}'.format(player.stats['HP'], player.stats['GOLD']))
	print('CURRENT ROOM: {}\n'.format(game_log.current_room))
	print("{}'s LOG: {}".format(player.info['Name'].upper(), current_msg))

def action_menu(player):
	"""print menu of game actions and take user input"""

	clear_screen()

	run_game_log(player, game_log)	# runs the run_game_log function which gets output from game_log class

	print('1. Move')
	print('2. Show Map')
	print('3. Show Player Inventory')
	print('4. Show Player Stats')
	print('5. Exit to Main Menu')

	possible_choices = ['1','2','3','4','5']
	active = True

	while active:
		selection = input('\nNow I shall... ')
		if selection in possible_choices:
			active = False
			return int(selection)	# return always exits a function, right? so active = False is redundant?
		else:
			print('That\'s not one of the menu options!')

def game_action(settings, player, grid_one, d6, d20):
	
	# need an if here in case the player is already built
	# that is, skip the call to build_player if saved game has been loaded
	player.build_player()

	active = True
	# Q: this game_action loop is running -within- the broader while loop of run_game
	# is that standard for game structure, a while loop that runs inside another running while loop?
	# is it efficient / are there any issues to consider?
	# what's more, you have a *third* while loop nested in this series, inside action_menu
	# while loop nesting:  run_game > game_action > action_menu
	while active:
		# main game action loop
		selection = action_menu(player)	#right now this is what prints action menu...

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

		elif selection == 5:
			print('Returning to Main Menu...')
			active = False

		else:
			print('That is not one of the menu options!')
			press_enter()

def run_game():	

	active = True

	while active:
		main_menu.print_menu()
		user_action = main_menu.main_choice()

		if user_action == 4:
			print('\nThanks for playing Deeper Dungeons!')
			active = False

		elif user_action == 1:
			game_action(settings, player, grid_one, d6, d20)

		else:
			print('\nSorry, that part of the game is still being developed.')
			press_enter()

# instantiate game objects

settings = GameSettings()

player = Player(settings)
grid_one = GameGrid(settings, player)
game_log = GameLog(grid_one)
main_menu = MainMenu()

d6 = Dice()
d10 = Dice(10)
d20 = Dice(20)
d100 = Dice(100)

# call the main run_game function loop
run_game()

# important... when does game 'check' the attribute states to see if player is dead, game_over, etc?
# you can regularly update those attribute values based on player actions, but how does the game check
# them regularly to determine overall game status?
# needs to happen in while loop, but how exactly? 


# you're going to need various update functions added. for example, a global sort of 'current room' tracker
# that will need to be updated in the main game loop, by looking at current player location, etc.

