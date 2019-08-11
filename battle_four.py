from random import randint
from random import choice
import time

# object definitions - put these in a module! 

class Settings():
	def __init__(self):
		self.difficulty = 2

class Dice():
	def __init__(self):
		self.last_roll = None
		#self.mod_val = 0
		#self.current_mod = None

	def roll(self, sides=6):
		roll = randint(1, sides)
		self.last_roll = roll
		return roll

	def print_roll(self, mods=0):
		text = 'ROLLING...'
		for c in text:
			print(c, end='', flush=True)
			time.sleep(0.06)	
		print(' {}'.format(self.last_roll)) # use lambda here to put 'if mods' inside line?

		if mods > 0:
			print(' +{}'.format(mods)) # or just print mods as totally separate function?

class Weapon():
	"""this class will only be instantiated as an attribute of the player class"""
	def __init__(self, name, damage):
		self.name = name
		self.damage = damage

	def modify_weapon(self, add_to_damage):
		self.name += 'x1'
		self.damage += add_to_damage

	def print_stats(self):
		print('*** WEAPON INFO ***')
		#print()
		print('TYPE{:.>15}'.format(self.name))
		print('DAMAGE{:.>13}'.format(self.damage))

class Armor():
	"""only instantiated as an attribute of player class"""
	def __init__(self, name, armor_class):
		self.name = name
		self.armor_class = armor_class

	def modify_armor(self, add_to_ac):
		self.name += 'x1'
		self.armor_class += add_to_ac

	def print_stats(self):
		print('*** ARMOR INFO ***')
		print('TYPE{:.>14}'.format(self.name))
		print('AC{:.>16}'.format(self.ac))

class Player():
	def __init__(self):
		self.name = 'Max'
		self.hp = 10
		self.dice = Dice()
		self.armor = Armor('Leather', 10)
		self.exp = 0
		self.weapon = Weapon('Dagger', 4)
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

# function definitions - basic UI stuff - put these all in a module!

def press_enter(text=None):
	"""input is not assigned to anything, this is only to have enter pressed by user"""
	if text:
		print(text)
	msg = '...'
	input(msg)

def get_player_input(text=None):
	if text:
		print(text)
	command = input('\n> ')
	return command

def get_input_valid(text=None, key='standard'):
	"""a version of input function that also performs input validation"""
	# always put key=... in a call to this function

	if text:
		print(text)

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
		possible_choices = ['strike head', 'strike torso', 'strike legs', 'use potion', 'p', 'c']
		possible_choices += ['h','t','l','i', 's h', 's t', 's l', 's']

	# add more as needed here

	return possible_choices

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

def step_printer(word):
	for c in range(len(word)):
		print(c, end='', flush=True)
		time.sleep(0.06)

def slow_print_two(word_one, word_two):
	print(word_one, end='', flush=True)
	time.sleep(0.08)
	print(word_two)

def slow_print_elipsis(word_one, word_two):
	"""prints first word, step prints elipsis, prints second word"""
	elipsis_long = '......'
	#elipsis = '.' * 6

	# print the first word
	print(word_one, end='', flush=True)
	
	# step print the elipsis string
	for c in elipsis_long:
		print(c, end='', flush=True)
		time.sleep(0.06)

	# print the second word
	print(word_two, flush=True)

# battle-specific function definitions

def encounter_monster(player, monster):
	"""monster is engaged and decision to fight or run is chosen by player"""
	clear_screen()

	# determine how difficult it is for player to run away successfully
	run_difficulty = int(randint(2,10) + (3 * monster.difficulty))

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
					# run was successful, exit while loop and do not start battle.
					active = False
					print('You successfully run away from the {}!'.format(monster.name))
					press_enter()

				else:
					# will be used to have monster attack first
					monster.advantage = True
					print('You failed to run away from the {}!'.format(monster.name))
					print('Now you must fight!')
					press_enter()

			if command.lower().startswith('f') or active:
				# end the encounter loop and start the battle
				active = False
				battle_main(player, monster)
						
def run_attempt(player, run_difficulty):
	"""rolls player dice, prints out roll, returns True if roll beats run_dc, False otherwise"""
	roll = player.dice.roll(20)
	player.dice.print_roll()
	return (roll > run_difficulty)		# returns a bool

def battle_main(player, monster):

	round_num = 1
	fight_mods = {'enemy_armor': 0, 'player_damage': 0} # should be an attribute of player!?

	crits = {'crit': False}

	active = True

	# main event loop for player and monster attacks, goes until fight is ended.
	while active:

		# clears screen and prints battle header
		battle_header(player, monster, round_num)

		if not monster.advantage:
			if player_attack(player, monster, fight_mods, round_num, crits):
				if not crits['crit']:
					player_damage(player, monster, fight_mods)
					press_enter()		# only one that I need of this function ??
			
		monster.advantage = False

		# remember, this will clear any commands previously printed to the screen as well
		# as re-print the header!
		battle_header(player, monster, round_num) # second call, so monster HP updates on screen.

		if monster.hp > 0:
			if monster_attack(player, monster):
				monster_damage(player, monster)
			
		if check_battle_status(player, monster):
			active = False

		if active:
			press_enter()
			round_num += 1
			crits['crit'] = False

			#reset the fight_mods
			fight_mods['enemy_armor'] = 0
			fight_mods['player_damage'] = 0

	print('\nThe battle is over! Thanks for playing!')

def print_battle_commands():
	"""print a screen showing all possible commands in battle"""
	clear_screen()

	print('**** BATTLE COMMANDS ****') # 25 characters used
	print()
	print('Strike...............HEAD')
	print('                    TORSO')
	print('             	    LEGS')
	print()
	print('Use................POTION')
	print('                     ITEM')
	print()

	press_enter()

def battle_header(player, monster, round_num):
	clear_screen()
	print('ROUND: {}'.format(round_num))
	print('{} HP: {} \t WEP: {}'.format(player.name.upper(), player.hp, player.weapon.name))
	print('{} HP: {}'.format(monster.name.upper(), monster.hp))
	print()

def check_battle_status(player, monster):
	"""checks state of player and monster to determine if battle is over, or should continue"""
	
	#check player
	if player.hp <= 0:
		print('\nYou have been defeated by the {}!'.format(monster.name))
		player.dead = True
		return True

	elif monster.hp <= 0:
		print('\nYou have destroyed the {}!'.format(monster.name))

		gain_exp(player, monster)

		return True
	
	else:
		# neither player nor monster has been defeated, fight will continue.
		return False

def player_attack(player, monster, fight_mods, round_num, crits):

	active = True

	# some possible menu commands need to loop back to command input (command, potion)
	# loops until a non-looping command is given
	while active:

		battle_header(player, monster, round_num)		# called again here because menu calls will clear screen (command, potion)

		print('Choose your attack...')

		command = get_input_valid(text=None, key='battle')

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
			active = False

	# out of loop, perform actual battle attacks

	# IMPLEMENT FUNCTION FOR CHOOSING STRIKE AREA HERE (BUILD AS SEPERATE FUNCTION, CALL HERE)

	roll = player.dice.roll(20)
	player.dice.print_roll()

	if roll == 20:
		print('CRITICAL HIT!')
		print('The {} has been destroyed by your perfectly placed strike!'.format(monster.name))
		monster.hp = 0
		crits['crit'] = True # used as flag to skip damage roll after critical hit
		return True

	elif roll > monster.armor_class + fight_mods['enemy_armor']:
		print('You successfully hit the {} with your {}!'.format(monster.name, player.weapon.name))
		return True

	else:
		print('Your attacked missed the {}, dang!'.format(monster.name))
		return False

def player_damage(player, monster, fight_mods):

	damage = player.dice.roll(player.weapon.damage) + fight_mods['player_damage']

	player.dice.print_roll(fight_mods['player_damage'])

	print('You dealt {} points of damage to the {}'.format(damage, monster.name))

	monster.hp -= damage

	# this is here simply so the header doesn't show a negative number for monster hp
	# after monster is defeated.
	if monster.hp < 0:
		monster.hp = 0
		
def monster_attack(player, monster):

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

	exp = monster.difficulty * 10
	player.exp += exp

	#any gain of exp always prints a message about the gain...might need to decouple the two.
	print('You gained {} experience points!'.format(exp))



settings = Settings()
player = Player()
monster = Monster(settings.difficulty)

encounter_monster(player, monster)














