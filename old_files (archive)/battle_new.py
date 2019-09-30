from random import randint
from random import choice
import time

# object definitions

class Settings():
	def __init__(self):
		self.difficulty = 1

class Dice():
	def __init__(self):
		self.last_roll = None
		self.mod_val = 0
		self.current_mod = None

	def roll(self, sides=6):
		roll = randint(1, sides)
		self.last_roll = roll
		return roll

	def print_roll(self):
		text = 'ROLLING...'
		for c in text:
			print(c, end='', flush=True)
			time.sleep(0.06)
		print(' {}'.format(self.last_roll))

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
		self.ac = armor_class

	def modify_armor(self, add_to_ac):
		self.name += 'x1'
		self.ac += add_to_ac

	def print_stats(self):
		print('*** ARMOR INFO ***')
		print('TYPE{:.>14}'.format(self.name))
		print('AC{:.>16}'.format(self.ac))

class Player():
	def __init__(self):
		self.name = 'Hero'
		self.hp = 10
		self.dice = Dice()
		self.armor = Armor('Leather', 10)
		self.exp = 0
		self.weapon = Weapon('Dagger', 4)
		self.guarding = 'h'

	def choose_guard(self):

		choice = get_player_input('What area will you guard? (HEAD/TORSO/LEGS)')
		possible_choices = ['h','t','l', 'head', 'torso', 'legs']
		active = True

		while active:

			if choice not in possible_choices:
				print('You did not make a valid selection, try again.')
			else:
				if choice.startswith('h'):
					self.guarding = 'h'
				elif choice.startswith('t'):
					self.guarding = 't'
				elif choice.startswith('l'):
					self.guarding = 'l'

				active = False

class Monster():
	"""Generate a monster object for battle sequences, diff parameter determines difficulty"""

	def __init__(self, difficulty):
		self.difficulty = difficulty #add randomization of difficulty here
		self.d_string = self.get_d_string()
		
		self.dice = Dice()	# constructs a die object by calling Dice class

		self.advantage = False	# determines who gets first attack, player or monster

		self.damage_roll = self.get_damage_roll()

		self.name = self.get_monster_name()	# gets random name on construction
		self.hp = self.get_hit_points()				# gets HP depending on difficulty
		self.guarded_area = self.choose_guard()
		self.ac = self.get_armor_class()


	def get_armor_class(self):
		if self.difficulty == 1:
			return 8
		if self.difficulty == 2:
			return 11
		if self.difficulty == 3:
			return 14
		if self.difficulty == 4:
			return 16

	def choose_guard(self):
		"""called to determine where enemy is currently guarding"""

		g = randint(1, 3)

		if g == 1:
			return 'h'
		if g == 2:
			return 't'
		if g == 3:
			return 'l'

	def get_d_string(self):
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
		print('DIFF LEVEL:{:.>12}'.format(self.d_string))
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

	def update_monster(self):
		"""Each round of the battle, the monster guards one or more part of its body"""

		# if nothing else gets added to this (no other changes to update) you could delete
		# this function and simply call self.choose_guard() in its place
		self.guarded_area = self.choose_guard()

# function definitions - basic UI stuff

def press_enter(text=None):
	if text:
		print(text)
	msg = '...'
	input(msg)

def get_player_input(text=None):
	if text:
		print(text)
	msg = '\n> '
	player_input = input(msg)
	return player_input

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

	# print the first word
	print(word_one, end='', flush=True)
	
	# step print the elipsis string
	for c in elipsis_long:
		print(c, end='', flush=True)
		time.sleep(0.06)

	# print the second word
	print(word_two, flush=True)

# function definitions - gameplay

def encounter_monster(player, monster):
	"""monster is engaged and decision to fight or run is chosen by player"""
	clear_screen()

	# determine how difficult it is for player to run away successfully
	run_difficulty = int(randint(2,10) + (3 * monster.difficulty))

	active = True
	run_failed = False		# used for proper control flow in while loop, because
							# f = fight, r = maybe fight, maybe no fight. we need a flag
							# so we know which to proceed into. this variable is that flag.

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
					# run was successful, exit while loop and do not start battle (run_failed remains false)
					active = False
					print('You successfully run away from the {}!'.format(monster.name))
					press_enter()

				else:
					# run failed, switch run_failed flag so battle will start; 
					run_failed = True
					# will be used to have monster attack first
					monster.advantage = True
					print('You failed to run away from the {}!'.format(monster.name))
					print('Now you must fight!')
					press_enter()

			if command.lower().startswith('f') or run_failed == True:
				# end the encounter loop and start the battle
				active = False
				battle_main(player, monster)
						
def run_attempt(player, run_difficulty):
	"""rolls player dice, prints out roll, returns True if roll beats run_dc, False otherwise"""
	roll = player.dice.roll(20)
	player.dice.print_roll()
	return (roll > run_difficulty)		# returns a bool.

def battle_main(player, monster):
	"""the main battle function in which player fights monster"""

	clear_screen()
	battle_on = True
	#player.choose_guard()

	round_num = 1

	while battle_on:

		clear_screen()

		
		it_goes_on = True	# is this the best way to create branching paths inside a while loop?

		print('* ROUND: {} \t{}\'s HP: {} \tENEMY HP: {} *\n'.format(round_num, player.name.upper(), player.hp, monster.hp))

		if not monster.advantage:

			if player_attack(player, monster, round_num):
				player_damage(player, monster)

		monster.advantage = False
		player.choose_guard()
		
		if monster.hp > 0:

			if monster_attack(player, monster, round_num):
				monster_damage(player, monster)

		# check results to see if either player or monster is defeated

		if player.hp <= 0:
			print('{} has been defeated by the {}!'.format(player.name, monster.name))
			battle_on = False
			it_goes_on = False
			press_enter()

		if monster.hp <= 0:
			print('You have destroyed the {}!'.format(monster.name))
			gain_exp(player, monster)
			battle_on = False
			it_goes_on = False
			press_enter()

		# update objects, but only if battle will be continuing
		if it_goes_on:
			round_num += 1
			monster.update_monster()
			#player.choose_guard()

	# press_enter()
	print('\nThe battle is over! Thanks for playing!')

def player_attack(player, monster, round_num):

	command = get_player_input('Where will you aim your attack?? (HEAD/TORSO/LEGS)'.format(round_num))

	if command == monster.guarded_area:
		print('The {} immediately deflected your attack!'.format(monster.name))
		press_enter()
		return False
	else:
		print('Press enter to roll your attack dice')
		press_enter()

		roll = player.dice.roll(20)

		player.dice.print_roll()

		if roll > monster.ac:

			print('You successfully hit the {} with your {}!'.format(monster.name, player.weapon.name))
			return True

		else:
			print('Your attack missed the {}, dang!'.format(monster.name))
			return False

def player_damage(player, monster):

	damage = player.dice.roll(player.weapon.damage)

	player.dice.print_roll()

	print('You dealt {} points of damage to the {}'.format(damage, monster.name))

	monster.hp -= damage

	press_enter()

def monster_attack(player, monster, round_num):

	msg_one = 'The monster is attacking your'
	guarded = ''
	attack = ''

	if player.guarding == 'h':
		guarded = 'HEAD'
	if player.guarding == 't':
		guarded = 'TORSO'
	if player.guarding == 'l':
		guarded = 'LEGS'

	msg_two = guarded

	monster_aim = randint(1, 3)

	if monster_aim == 1:
		attack = 'h'
	if monster_aim == 2:
		attack = 't'
	if monster_aim == 3:
		attack = 'l'

	slow_print_elipsis(msg_one, msg_two)

	if attack == player.guarding:
		print('You immediately deflect the {}\'s attack!'.format(monster.name))
		press_enter()
		return False

	else:
		press_enter()

		roll = monster.dice.roll(20)
		monster.dice.print_roll()

		if roll > player.armor.ac:
			print('The {}\'s attack hits you!'.format(monster.name))
			press_enter()
			return True
		else:
			print('The {}\'s attack misses you, phew!'.format(monster.name))
			press_enter()
			return False

def monster_damage(player, monster):

	damage = monster.dice.roll(monster.damage_roll)

	monster.dice.print_roll()

	print('You take {} points of damage!'.format(damage))

	player.hp -= damage

	press_enter()


def gain_exp(player, monster):
	"""award experience to player for beating a monster"""

	exp = monster.difficulty * 10
	player.exp += exp
	#any gain of exp always prints a message about the gain...might need to decouple the two.
	print('You gained {} experience points!'.format(exp))
	press_enter()


settings = Settings()
player = Player()
monster = Monster(settings.difficulty)

encounter_monster(player, monster)














