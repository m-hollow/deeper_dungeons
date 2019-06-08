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

		for r in self.grid_matrix:

			col_num = 0
			
			for c in r:
				room_type = self.get_room_type()
				room = {'Coords':[row_num, col_num], 'Type':room_type}
				all_rooms.append(room)
				col_num += 1

			row_num += 1

		all_rooms[13]['Type'] = 'Player Start'

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
		self.player_row = (self.settings.grid_size - 1)
		self.player_col = (int(self.settings.grid_size / 2) - 1 )	# starts at room 13 (coord 3, 1)

		#tuple start location, fixed value for every new grid created
		self.player_start_location = (self.settings.grid_size - 1, (int(self.settings.grid_size / 2) - 1))
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
		# need to find quick way to make this correct bad user input
		msg = '\nEnter your choice: '
		choice = int(input(msg))
		return choice

# define game functions. need to add a whole function for movement in grid.

def press_enter():
	msg = '\nOK...'
	input(msg)

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

def game_log(player):
	"""prints the current gamelog"""
	current_msg = '\nI am standing in an empty room.' # create a class for printing updated msgs
	
	print("{}'s LOG:{}\n".format(player.info['Name'].upper(), current_msg))

def action_menu(player):
	"""print menu of game actions and take user input"""

	clear_screen()

	game_log(player)

	print('1. Move')
	print('2. Show Map')
	print('3. Show Player Inventory')
	print('4. Show Player Stats')
	print('5. Exit to Main Menu')

	selection = int(input('\nNow I shall... '))
	return selection

def game_action(settings, player, grid_one, d6, d20):
	
	# need an if here in case the player is already built
	player.build_player()

	active = True

	while active:
		### main game loop goes here ###
		selection = action_menu(player)	#right now this is what prints action menu...

		if selection == 1:
			"""this needs to launch the player movement function and update location"""
			# movement function could be a method in player class or independent function
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
# game_log = LogGenerator(player, grid_one)
main_menu = MainMenu()

d6 = Dice()
d10 = Dice(10)
d20 = Dice(20)
d100 = Dice(100)

# call the main run_game function loop
run_game()

# right now, game_log is just a function; should it be a class?... yeah, probably!





