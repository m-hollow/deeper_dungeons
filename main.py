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

		self.grid = self.make_grid()

	def make_grid(self):
		# list comprehension to create matrix of the game grid

		matrix = [[' * ' for x in range(self.col)] for y in range(self.row)]

		matrix[self.player.player_row][self.player.player_col] = ' X '

		return matrix

	def print_grid(self):
		"""print the grid attribute"""
		msg = 'OK...'
		print("\033[H\033[J")

		print('# DUNGEGON MAP #\n')

		for r in self.grid:
			for c in r:
				print(c, end='')
			print()						# use print('\n' to space out grid further)

		print('\n')
		y = input(msg)

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

		# self.grid_max = self.settings.grid_size

		self.player_row = (self.settings.grid_size - 1)
		self.player_col = (int(self.settings.grid_size / 2) - 1 )

	def build_player(self):
		"""fill dictionary with user character choices"""
		msg = 'OK...'
		
		print("\033[H\033[J")

		print("\nLet's build your character before starting.")
		y = input(msg)

		a = input('What is the name of your character? ')
		b = input('What is the Race of your charcter? ')

		self.info['Name'] = a
		self.info['Race'] = b

		print('You have successfully created {} the {}'.format(a, b))

		y2 = input(msg)		# make a 'pause until enter keypress' function...

	def print_player_info(self):
		"""display all player stats on the screen"""
		msg = 'OK...'
		print("\033[H\033[J")

		print("#    PLAYER INFO    #\n")
		print("Name{:.>17} ".format(self.info['Name']))
		print("Race{:.>17} ".format(self.info['Race']))
		print("Level{:.>16} ".format(self.stats['Level']))
		print("Hit Points{:.>11} ".format(self.stats['HP']))
		print("Gold Pieces{:.>10} ".format(self.stats['GOLD']))
		print('\n')

		y = input(msg)

class MainMenu():
	"""Display menu and receive input for user choice"""

	def __init__(self):
		self.nothing = None

	def print_menu(self):

		print("\033[H\033[J")

		print('#   DEEPER DUNGEONS   #\n')
		print('1. Start New Game')
		print('2. Load Game')
		print('3. Change Game Settings')
		print('4. Exit Game')

	def main_choice(self):
		msg = '\nEnter your choice: '
		choice = int(input(msg))
		return choice

# define game functions. need to add a whole function for movement in grid.

def game_log(player):
	"""prints the current gamelog"""
	current_msg = 'I am standing in an empty room.' # create a class for printing updated msgs
	
	print("{}'s Log: {}".format(player.info['Name'], current_msg))

def action_menu(player):
	"""print menu of game actions and take user input"""

	print("\033[H\033[J")		# command to clear screen, terminal specific ?

	game_log(player)

	print('1. Move')
	print('2. Show Map')
	print('3. Show Player Stats')
	print('4. Exit to Main Menu\n')

	selection = int(input('Now I shall... '))
	return selection

def game_action(settings, player, grid_one, d6, d20):
	
	# need an if here in case the player is already built
	player.build_player()

	active = True

	while active:
		### main game loop goes here ###
		selection = action_menu(player)	#right now this is what prints action menu...

		if selection == 1:
			"""unfinished"""
			msg = 'OK...'
			print('\nI will move to the next room...')
			y = input(msg)

		elif selection == 2:
			"""Unfinished"""
			grid_one.print_grid()

		elif selection == 3:
			"""Unfinished"""
			player.print_player_info()

		elif selection == 4:
			print('Returning to Main Menu...')
			active = False

		else:
			msg = 'OK...'
			print('That is not one of the menu options!')
			y = input(msg)


# instantiate game objects

settings = GameSettings()

player = Player(settings)
grid_one = GameGrid(settings, player)
main_menu = MainMenu()

d6 = Dice()
d20 = Dice(20)

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
			msg = 'OK...'
			print('\nSorry, that part of the game is still being developed.')
			y = input(msg)


run_game()






