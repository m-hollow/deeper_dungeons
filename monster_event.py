from random import randint
from random import choice
import time

class Dice():
	
	def __init__(self):
		self.last_roll = None

	def roll(self, sides=6):
		roll = randint(1, sides)
		self.last_roll = roll # multipurpose function here...
		return roll           # it assigns roll to attribute last_roll,
							  # but also returns the roll for assignment elsewhere...
							  # is this OK ?
	def print_roll(self):
		text = 'ROLLING...'
		for c in text:
			print(c, end='', flush=True)
			time.sleep(.08)
		print(' {}'.format(self.last_roll))

class Monster():

	def __init__(self, difficulty):
		self.difficulty = difficulty
		self.dice = Dice() #ok that it's not passed as argument?
		self.hp = 10
		self.name = choice(['Bat','Ogre','Gargoyle','Wasp','Roach', 'Vampire'])

class Player():

	def __init__(self):
		self.name = 'Hero'
		self.hp = 10


dice = Dice()
player = Player()
monster = Monster(1)

def engagement(player, monster, dice):
	"""initial monster engagement"""
	print('You have encountered a {}!'.format(monster.name))
	print('Do you FIGHT or RUN?')
	print()
	
	active = True

	while active:

		msg = 'Enter command F/R: '
		choice = input(msg)

		possible_choices = ['f','r']

		if choice not in possible_choices:
			print('You did not enter a valid option, try again')
		else:
			if choice == 'r':
				if run_attempt(dice):
					print('You have succesfully run away!')
					active = False
				else:
					print('You failed to run away!, now you must fight!')
					battle(player, monster, dice)
					active = False

			elif choice == 'f':
				battle(player, monster, dice)
				active = False

def run_attempt(dice):
	"""player tries to run away"""

	must_beat = 10 		# add settings.difficulty to this number, making it harder

	z = input('Press enter to roll d20...')

	dice.roll(20)
	dice.print_roll()

	if dice.last_roll >= must_beat:
		return True
	else:
		return False

def battle(player, monster, dice):
	"""main function for the battle"""

engagement(player, monster, dice)

msg = 'ok'
wait = input(msg)
	

# Q: again, normal to pass an object that was already passed to a function to another function 
# called within the initial function? e.g. see calls to battle() above, which pass all
# three parameters that were initially passed to engagement()

