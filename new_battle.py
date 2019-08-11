# load modules

from random import randint
from random import choice
import time

from classes import *
from ui_funcs import *

def encounter_monster(player, monster):
	"""monster is engaged and decision to fight or run is chosen by player"""
	clear_screen()

	# determine how difficult it is for player to run away successfully
	run_difficulty = int(randint(2,10) + (3 * monster.difficulty))

	active = True

	# step print encounter text	
	slow_print_elipsis('You have encountered a', monster.name.upper())
	print('Run Difficulty: {}'.format(run_difficulty))

	#this version of the encounter loop removes the run_failed bool and simply checks against 'active' to determine
	#if the battle happens (see last if: player presses 'f' -or- active == True)
	while active:

		command = get_player_input()

		possible_choices = ['fight', 'run', 'f', 'r']

		if command not in possible_choices:
			print('You did not enter a valid command, try again.')
		else:
			# this if has no else case
			if command.lower().startswith('r'):
				if run_attempt(player, run_difficulty):
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
	"""the main battle function in which player fights monster"""

	clear_screen()
	battle_on = True
	round_num = 1

	while battle_on:

		battle_header(player, monster, round_num)
		
		if not monster.advantage:
			if player_attack(player, monster, round_num):
				player_damage(player, monster)
				press_enter()

		monster.advantage = False
		
		# don't trigger monster attack if monster was already killed by first player attack
		if monster.hp > 0:
			player.choose_guard()	# player chooses defense position

			if monster_attack(player, monster, round_num):
				monster_damage(player, monster)
				press_enter()

		# see if either player or monster has been defeated
		if check_battle_status(player, monster):
			battle_on = False

		if battle_on:			#reusing the same check that runs the loop itself, to create a branch.
			monster.update_monster()

	print('\nThe battle is over! Thanks for playing!')

def battle_header(player, monster, round_num):
	clear_screen()
	print('ROUND: {}'.format(round_num))
	print('{} HP: {}'.format(player.name.upper(), player.hp))
	print('{} HP: {}'.format(monster.name, monster.hp))
	print()

def check_battle_status(player, monster):
	"""checks state of player and monster to determine if battle is over, or should continue"""
	
	#check player
	if player.hp <= 0:
		print('{} has been defeated by the {}!'.format(player.name, monster.name))
		return True
	elif monster.hp <= 0:
		print('You have destroyed the {}!'.format(monster.name))
		return True
	else:
		return False

def player_attack(player, monster, round_num):

	print('CHEAT: {} is currently guarding {}'.format(monster.name, monster.guarded_area))
	command = get_player_input('Where will you aim your attack?? (HEAD/TORSO/LEGS)'.format(round_num))

	if command == monster.guarded_area:
		print('The {} immediately deflected your attack!'.format(monster.name))
		press_enter()
		return False
	else:
		#print('Press enter to roll your attack dice')
		#press_enter()

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
	msg_two = ''
	attack = ''

	monster_aim = randint(1, 3)

	if monster_aim == 1:
		attack = 'h'
		msg_two = 'HEAD'
	if monster_aim == 2:
		attack = 't'
		msg_two = 'TORSO'
	if monster_aim == 3:
		attack = 'l'
		msg_two = 'LEGS'

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
	#press_enter()


settings = Settings()
player = Player()
monster = Monster(settings.difficulty)

encounter_monster(player, monster)