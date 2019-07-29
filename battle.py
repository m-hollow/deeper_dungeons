from random import randint
from random import choice
import time

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

class Player():
	def __init__(self):
		self.name = 'Hero'
		self.hp = 10
		self.dice = Dice()
		self.armor = 10

class Monster():
	"""Generate a monster object for battle sequences, diff parameter determines difficulty"""

	def __init__(self, difficulty):
		self.difficulty = difficulty
		self.d_string = self.get_d_string()
		
		self.dice = Dice()	# constructs a die object by calling Dice class

		self.advantage = False	# determines who gets first attack, player or monster

		self.name = self.get_monster_name()	# gets random name on construction
		self.hp = self.get_hit_points()				# gets HP depending on difficulty
		self.weak_point = self.get_weak_point()

	def get_weak_point(self):
		"""called on instantiation to determine weak point of that object"""

		wp = randint(1, 3)

		if wp == 1:
			return 'h'
		if wp == 2:
			return 't'
		if wp == 3:
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
		print()

def press_enter():
	msg = '\n...'
	input(msg)

def slow_printer(word):
	for c in range(len(word)):
		print(c, end='', flush=True)
		time.sleep(0.06)

def engage_monster(settings, player, monster):
	
	#first attempt at scaling run difficulty based on monster difficulty

	print("\033[H\033[J")

	run_dc = int(randint(1,8) + (2 * monster.difficulty))

	print('You have encountered a {}!'.format(monster.name))
	print('Do you FIGHT or RUN? (Run Difficulty: {}):'.format(run_dc))
	print()

	active = True
	run_failed = False

	while active:

		msg = 'Enter command: '
		choice = input(msg)

		possible_choices = ['f','r']

		if choice not in possible_choices:
			print('You did not enter a valid option, try again.')
		else:
			if choice == 'r':

				if run_attempt(settings, player, run_dc):
					print('You have successfully run away!')
					active = False
				else:
					print('You failed to run away successfully!')
					print('Now you must fight the {}'.format(monster.name))
					monster.advantage = True
					run_failed = True
					press_enter()

			if choice == 'f' or run_failed == True:
				active = False
				battle(player, monster)

def get_player_input():
	msg = "\n> "
	player_input = input(msg)
	return player_input

def get_count_string(count):

	if count == 1:
		return 'first'
	elif count == 2:
		return 'second'
	elif count == 3:
		return 'third'
	elif count == 4:
		return 'fourth'
	elif count == 5:
		return 'fifth'
	elif count == 6:
		return 'sixth'
	elif count == 7:
		return 'seventh'
	elif count == 8:
		return 'eighth'
	elif count == 9:
		return 'ninth'
	elif count == 10:
		return 'tenth'
	elif count == 11:
		return 'eleventh'
	elif count == 12:
		return 'twelfth'

def battle(player, monster):
	"""battle between player and monster objects"""

	# how to use monster.advantage bool to determine who attacks first ???
	# what does the control flow look like? if you put it inside the while loop,
	# it gets re-assessed on every pass, which isn't necessary: you only need to
	# know at the very start. but maybe that doesn't matter?

	battle_on = True
	count = 1

	while battle_on:

		print("\033[H\033[J")

		print('*** BATTLE ***')
		print('')
		print('{}\'s HP: {}'.format(player.name.upper(), player.hp))
		print('ENEMY: {} \t HP: {}'.format(monster.name.title(), monster.hp))
		print()
		print('HEAD')
		print('TORSO')
		print('LEGS')

		continue_battle = True

		msg = 'Aim your {} attack: '.format(get_count_string(count))

		attack_choice = input(msg).lower()

		if attack_choice == monster.weak_point:
			print('You hit the {}\'s weak point!'.format(monster.name))
			msg = ('Enter to roll for damage...')
			input(msg)

			damage = roll_damage(player)
			player.dice.print_roll()
			
			monster.hp -= damage

			print('You did {} points of damage to the {}'.format(damage, monster.name.title()))
			print('The {} has {} hp remaining.'.format(monster.name.title(), monster.hp))
			press_enter()


			if monster.hp <= 0:
				print('The {} is defeated!'.format(monster.name))
				continue_battle = False   # for the branching path in the main while
				battle_on = False		# to end the main while as well

		else:
			print('The {} successfully BLOCKED your attack!'.format(monster.name))
			press_enter()


		# this should be its own function, I think. one for player vs monster, another
		# for monster vs. player

		if continue_battle:

			print('The {} is attacking you!'.format(monster.name))
			print('{}\'s armor rank: {}'.format(player.name, player.armor))
			attack = monster.dice.roll(20)
			monster.dice.print_roll()

			if attack > player.armor:
				print('The {} successfully hits you!'.format(monster.name))

				damage = monster.dice.roll(6)
				monster.dice.print_roll()

				print('You take {} damage.'.format(damage))

				player.hp -= damage

				if player.hp <= 0:
					print('{} has been vanquished!!!'.format(player.name))
					battle_on = False

			else:
				print('The {}\'s attack misses you, phew!'.format(monster.name))
				press_enter()


		count += 1

		print('Press enter for next round of combat...')
		press_enter()

		print("\033[H\033[J")

def roll_damage(player):
	"""damage roll after player successfully hits monster"""

	return player.dice.roll(6)

def run_attempt(settings, player, run_dc):
	
	roll = player.dice.roll(20)
	player.dice.print_roll()
	return (roll >= run_dc)

settings = Settings()
player = Player()
monster_one = Monster(settings.difficulty)


engage_monster(settings, player, monster_one)


# issue: if you fail to run, it says you must fight, but then you can choose to run again...







