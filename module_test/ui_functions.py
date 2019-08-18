import time
from random import randint, choice
import copy

from classes import *

# define game UI functions.

def you_are_dead(player, text=''):

	clear_screen()

	if text:
		print(text)

	step_printer('YOU ARE DEAD')
	
	time.sleep(0.8)
	print()
	print('\nSo passes {} the {} into the endless night.'.format(player.info['Name'], player.info['Race']))

	press_enter()

def step_printer(word, speed=0.06):
	"""call whenever you want to print a word in steps"""
	#not modifying the word, so no need to index it
	for c in word:
		print(c, end='', flush=True)
		time.sleep(speed)

	# old index version
	#for c in range(len(word)):
	#	print(word[c], end='', flush=True)
	#	time.sleep(speed)

def slow_print_two(word_one, word_two):
	"""call to print one word, pause, then the second word"""
	print(word_one, end='', flush=True)
	time.sleep(0.08)
	print(word_two)

def slow_print_elipsis(word_one, word_two, elip=6):
	"""prints word one, then step prints elipsis, then prints word two"""
	elipsis = ('.' * elip)
	
	print(word_one, end='', flush=True)
	
	for c in elipsis:
		print(c, end='', flush=True)
		time.sleep(0.06)
	
	print(word_two, flush=True)

def command_menu(player):
	"""prints the command menu for the player"""
	clear_screen()

	print('#{:^33}#'.format(player.info['Name'].upper() + '\'s COMMANDS'))
	print()
	print('MOVE: North  DO:  Rest   GAME: Save')
	print('      South       Item         Quit')
	print('      East        Bio')
	print('      West')
	print()
	print()
	print('Type the first letter of a command') 
	print('at the game prompt (>).')

	press_enter()

def main_menu(player):
	"""displays main program menu, takes user input choice and returns it"""

	clear_screen()

	print('#   DEEPER DUNGEONS   #\n')
	print('1. Build character')
	print('2. Start New Game')
	print('3. Load Game')
	print('4. Change Game Settings')
	print('5. Exit Game')

	print('\nCurrently Loaded Character: {}'.format(player.info['Name']))

	possible_choices = ['1','2','3','4','5']
	
	msg = '\nEnter your choice: '
	choice = input(msg)
	if choice in possible_choices:
		return int(choice)
	else:
		print('That\'s not one of the menu options!')
		press_enter()
		return None 			# no loop is necessary in this function because run_game's call to this func gets None,
								# therefore has no other action to perform, so it (run_game body loop) loops, calling 
								# this function again. 

def get_player_input(text=None):
	if text:
		print(text)
	msg = '\n> '
	player_input = input(msg)
	return player_input

def get_input_valid(text=None, key='standard'):
	"""a version of input function that also performs input validation"""
	# always put key=... in a call to this function

	if text:
		print(text)

	command = ''	# initialize command as empty string
					# not necessary, but clean...

	possible_choices = get_possible_choices(key)
	
	valid = False

	while not valid:

		command = input('\n> ').lower()		# this function always takes lower() right here,
											# so there's no need to call lower() elsewhere.

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
		possible_choices = ['strike','headshot','s','h','p','i','b']
		possible_choices += ['finesse','fin','flurry','flu', 'help']
	elif key == 'exit_room':
		possible_choices = ['yes','no','y','n']

	# add more as needed here

	# think of it like this: this place is the 'master set' of valid commands.
	# inside the actual game functions, you will parse the inputs to perform the
	# corresponding actions, *always knowing that a valid command has already been 
	# entered*.

	

	return possible_choices

def press_enter(text=None):
	if text:
		print(text)
	msg = '\n...'
	input(msg)

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")