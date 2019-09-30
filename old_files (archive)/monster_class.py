import time
from random import randint
from random import choice

class Dice():
	"""dice object for rolling; provide number of sides to roll_die method!"""

	def __init__(self):
		self.nothing = None       # should I have anything here? OK? 
		self.last_roll = None

	def roll_die(self, sides=6):	#provide number of sides on call to roll_die
		roll = randint(1, sides)
		self.last_roll = roll
		return roll

	def print_roll_slow(self):
		text = 'ROLLING...'
		for c in text:
			print(c, end='', flush=True)
			time.sleep(0.08)
		print(' {}'.format(self.last_roll))

class Settings():
	"""game settings object"""

	def __init__(self):
		self.difficulty = 1		#current difficulty level of game (but in 'backend stuff')

class Monster():
	"""Generate a monster object for battle sequences, diff parameter determines difficulty"""

	def __init__(self, difficulty):
		self.difficulty = difficulty
		self.d_string = self.get_d_string()
		
		self.dice = Dice()	# constructs a die object by calling Dice class

		self.monster_name = self.get_monster_name()	# gets random name on construction
		self.hp = self.get_hit_points()				# gets HP depending on difficulty

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
			return self.dice.roll_die(4)
		elif self.difficulty == 2:
			return ((self.dice.roll_die(6)) + 2)
		elif self.difficulty == 3:
			return ((self.dice.roll_die(10)) + 4)
		elif self.difficulty > 3:
			return ((self.dice.roll_die(20)) + 10)

	def print_stats(self):
		print('# MONSTER STATS       #')     #23 chars
		print('NAME:{:.>18}'.format(self.monster_name.upper()))
		print('DIFF LEVEL:{:.>12}'.format(self.d_string))
		print('HP:{:.>20}'.format(self.hp))
		print()

settings = Settings()

e_easy = Monster(settings.difficulty)	# how it would work in the game
e_easy_two = Monster(1)
e_medium = Monster(2)					# entering different values just to show effect
e_medium_two = Monster(2)
e_hard = Monster(3)
e_hard_two = Monster(3)
e_elite_one = Monster(4)
e_elite_two = Monster(4)

# create a bunch of monsters in a loop, with an increment to make them progressively harder? ...why?

all_monsters = [e_easy, e_easy_two, e_medium, e_medium_two, e_hard, e_hard_two, e_elite_one, e_elite_two]

for monster in all_monsters:
	monster.print_stats()



# logic:
# when you construct a monster object, you provide an int for the monster's difficulty level
# (in game, this could be a settings attribute of current difficulty level of game / dungeon floor)

# on construction, that difficulty level argument is assigned to class attribute "difficulty"
# on consctruction, a 'dice' object is created as an attribute (one of monster's attributes is object 'dice')
# this means the monster class object has an attribute that is also a class object, dice.
# on construction, monster_name is created by calling method that loads text file and picks entry at random
# on construction, hit point attribute calls method get_hit_points to assign an int value to attribute HP
# this method looks at the difficulty level that was originally sent as an argument on construction,
# and depending on its value, will roll different sided dice.
# that is: difficulty level (arbitrary int values) are used to determine what sided die is rolled.
# if I build a monster of difficulty 1, the HP will be deteremined by rolling d4
# if I build a monster of difficulty 2 or 3, the HP will be determined by rolling d6
# if I build a monster of difficulty greater than 3, the HP will be determined by rolling d10




