from random import randint
from random import choice
import time

from ui_funcs import *

# all class objects for use in Deeper Dungeons

class Settings():
	def __init__(self):
		self.difficulty = 2

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


		possible_choices = ['h','t','l', 'head', 'torso', 'legs']
		active = True

		while active:

			choice = get_player_input('What area will you guard? (HEAD/TORSO/LEGS)')

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