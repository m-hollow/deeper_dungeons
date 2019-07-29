from random import randint
from random import choice
import time


def user_input():
	msg = '> '
	choice = input(msg)
	return choice

def press_enter():
	msg = '...'
	input(msg)

def run_attempt():
	
	escape_num = 10 # this will be determined by mosnster difficulty in actual game
	
	print('Press enter to roll your Run attempt')
	press_enter()

	roll = randint(1,20)
	
	if roll > escape_num:
		print('You rolled {}. You have successfully run away!'.format(roll))
		return True
	else:
		print('You rolled {}. You failed to get away, now you must fight!'.format(roll))
		return False

def encounter():
	"""this works. it may be a bit janky. is there a way to divide into two functions?"""

	active = True
	run_failed = False

	# put a clear_screen() here

	print('You have encountered a MONSTER!')
	print('Will you fight or run?')

	while active:

		command = user_input()

		possible_choices = ['fight', 'run', 'f', 'r']

		if command not in possible_choices:
			print('You did not enter a valid command, try again.')

		else:
			if command == 'r' or command == 'run':

				if run_attempt():
					# successful run, needs to exit the entire while loop.
					# works because run_failed will still == False, so next if will not execute.
					active = False
				else:
					run_failed = True

			if (command == 'f' or command == 'fight') or run_failed == True:

				active = False
				battle()		# clarify proper order of operations here, set active then call function?
								# or the other way around ?


# some new function to check if battle is starting, and if so, calls battle, and if not, return to 'main' area
# of game? only purpose would be so that battle() is not called from within the encounter() function, but
# does it matter? isn't adding -more- code best avoided? 

def battle():
	print('The battle begins now!')


encounter()







