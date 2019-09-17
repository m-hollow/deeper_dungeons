# define all Battle functions
import time
from random import randint, choice
import copy

from ui_functions import *
from classes import *

def encounter_monster(settings, player, monster, grid, game_log):
	"""monster is engaged and decision to fight or run is chosen by player"""
	clear_screen()

	# determine how difficult it is for player to run away successfully
	run_difficulty = int(randint(2,10) + (2 * monster.difficulty))

	if run_difficulty > 18:
		run_difficulty = 18

	run_failed = False

	active = True

	# step print encounter text
	slow_print_elipsis('You have encountered a', monster.name.upper())

	print('Run Difficulty: {}'.format(run_difficulty))
	print('\nActions:\t Fight | Run')

	while active:

		command = get_player_input()

		possible_choices = ['fight', 'run', 'f', 'r']

		if command not in possible_choices:
			print('You did not enter a valid command, try again.')
		else:
			# this if has no else case
			if command.lower().startswith('r'):
				if run_attempt(player, run_difficulty):
					# run was successful, exit encounter loop and do not start battle.
					active = False
					print('You successfully run away from the {}!'.format(monster.name))
					time.sleep(0.8)
					print('You will now return to the previous room.')
					press_enter()

					# make current room (one being run out of) grid icon change back to a *
					grid.grid_matrix[player.player_location[0]][player.player_location[1]] = ' * '
					# make player coords equal that of previously visited room
					player.player_location = player.previous_coords.copy()

					# update everything since room has reverted
					grid.update_player_location()
					grid.update_current_roomtype()
					game_log.update_log()


					# NOTE: Player never 'moved' (entered move command) to leave this room, we just
					# force them back in next lines. movement_engine() function is where previous room
					# gets set to Visited = True, but that will NOT have happened in this situation,
					# because they never 'moved' out of it. So, it should remain Visited = False, which
					# is actually what we want anyway.

				else:
					# will be used to have monster attack first
					run_failed = True
					print('You failed to run away from the {}!'.format(monster.name))
					print('Now you must fight!')
					press_enter()

			if command.lower().startswith('f') or active:
				# end the encounter loop and start the battle
				active = False
				battle_main(settings, player, monster, grid, game_log, run_failed)

def run_attempt(player, run_difficulty):
	"""rolls player dice, prints out roll, returns True if roll beats run_dc, False otherwise"""
	roll = player.dice.roll(20)
	player.dice.print_roll()
	return (roll >= run_difficulty)		# returns a bool

def battle_main(settings, player, monster, grid, game_log, run_failed):

	player.current_state = 'battle'

	turn = 0
	round_num = 1
	fight_mods = {'enemy_armor': 0, 'player_roll': 0, 'player_damage': 0}
	# potion_mods = {'player_attack': 0, 'player_damage': 0} # this is now stored as player class attribute
	atype = {'attack': None}
	crits = {'crit': False}
	player_turn = True

	if run_failed:
		player_turn = False

	active = True

	while active:

		battle_header(player, monster, round_num)	# there is another call to battle_header in attack_menu_input()

		# player attack
		if player_turn:

			if player_attack(player, monster, fight_mods, round_num, crits, atype):
				if not crits['crit']:
					player_damage(player, monster, fight_mods, atype)
				else:
					pass

			player_turn = False

		# monster attack
		else:

			if monster.hp > 0:
				if monster_attack(player, monster, round_num):
					monster_damage(player, monster)

			player_turn = True

		# status check on both player and monster
		if check_battle_status(settings, player, monster, grid, game_log, crits):
			active = False	# player or monster is dead, so end the battle loop.
			#potion_mods is a player class attribute, so we need to reset it after battle ends or player enters next
			# battle with the mods still in place!
			player.potion_mods['player_attack'] = 0
			player.potion_mods['player_damage'] = 0

		# run updates if the battle is still going
		if active:
			press_enter()		# first of two calls to press_enter, for pause between ongoing loops
			turn += 1
			if turn % 2 == 0:
				round_num += 1
			crits['crit'] = False 	# reset crit. kinda inefficient.

			# reset the fight mods and atype so each round of battle starts with empty mods.
			fight_mods['enemy_armor'] = 0
			fight_mods['player_roll'] = 0
			fight_mods['player_damage'] = 0
			player.potion_mods['player_attack'] = 0
			player.potion_mods['player_damage'] = 0
			atype['attack'] = None

		elif not active:	# shouldn't this be the same result as just 'else'? but it didn't work...
			press_enter()	#  second of two calls to press_enter, for pause before ending battle sequence.

def print_battle_commands():
	"""print a screen showing all possible commands in battle"""
	clear_screen()

	print('*****              ATTACK TYPES              *****') # 31 characters used
	print()
	print('STANDARD (S):')
	print('A normal attack. No mods to attack or damage rolls.')
	print()
	print('HEADSHOT (H):')
	print('Aim for the head! Enemy AC gets +4 but if you hit,')
	print('you deal double damage.')
	print()
	print('FLURRY  (FLU):')
	print('Run in mad and flailing! Easier to hit enemy (Roll +3),')
	print('but you usually deal less damage: damage roll gets a')
	print('random 0 to 3 penalty.')
	print()
	print('FINESSE (FIN):')
	print('A deliberate attack, going for a weak point. Slightly')
	print('harder to hit (Enemy AC +2) but success means +2 to ')
	print('your damage roll.')
	print()
	print('Type the name (or shortcut) of attack to enter command.')

	press_enter()

def battle_header(player, monster, round_num):
	clear_screen()
	print('ROUND: {}'.format(round_num))
	print('{: <12} \t HP: {: <3} AC: {: <3} \t WEP: {}{}'.format(player.info['Name'].upper(), player.hp, player.armor.armor_class, player.weapon.name, player.weapon.icon))
	print('{: <12} \t HP: {: <3} AC: {: <3}'.format(monster.name.upper(), monster.hp, monster.armor_class))
	print()

def check_battle_status(settings, player, monster, grid, game_log, crits):
	"""checks state of player and monster to determine if battle is over, or should continue"""

	# check if player used an escape elixir on this turn
	if player.escaping == True:

		# make current room (one being escaped from) grid icon change back to a *
		grid.grid_matrix[player.player_location[0]][player.player_location[1]] = ' * '
		# mark the room as not visited so it will still be a monster on next visit
		grid.all_room_grid[player.player_location[0]][player.player_location[1]]['Visited'] = False
		# make player coords equal that of previously visited room
		player.player_location = player.previous_coords.copy()

		# update everything since room has reverted to previous room
		grid.update_player_location()
		grid.update_current_roomtype()
		game_log.update_log()

		# reset player.escaping attribute
		player.escaping = False
		return True

	# check if player was killed on this turn
	elif player.hp <= 0:
		print('\nYou have been defeated by the {}!'.format(monster.name))
		player.dead = True
		time.sleep(0.8)
		return True

	# check if monster was killed on this turn
	elif monster.hp <= 0:
		if not crits['crit']:
			time.sleep(.5)
			print('\nYou destroyed the {}!'.format(monster.name))
		else:
			print()	# this may not be necessary, need to playtest on critical hit success for line spacing.

		press_enter()
		clear_screen()

		step_printer('** BATTLE ENDED **', 0.03)
		print('\n')

		gain_exp(player, monster)
		time.sleep(0.5)

		monster_leaves_item(settings, player, monster)	# called here so chance of item only happens when monster is defeated.

		# reset current state attribute of player so it's no longer 'battle' (relevant to potion usage)
		player.current_state = ''
		return True

	else:
		# neither player nor monster has been defeated, fight will continue.
		return False

def player_attack(player, monster, fight_mods, round_num, crits, atype):
	"""runs all player attack functions and returns a bool to call in battle_main function"""

	command = attack_menu_input(player, monster, fight_mods, round_num)

	# it seems not great that I have to add this entire conditional indent just to check against player.escaping,
	# which is hardly a common event (only applies to use of escape potion). but currently, doing so is the only
	# way to bypass an attack roll on player's turn and skip forward to check_battle_status, where the escape usage
	# will be processed. without this, player will use escape potion but then still have an attack roll occur
	# before it gets processed.

	if not player.escaping:
		# if applicable, fight_mods will be updated by this call
		compute_attack_mods(player, monster, fight_mods, command, atype)

		weapon_bonus = 0	# default to zero, will update below if applicable weapon is used

		# here is the actual attack die roll...
		roll = player.dice.roll(20)
		player.dice.print_roll()

		# check if roll is a critical hit
		if roll == 20:
			critical = 'CRITICAL HIT!'
			step_printer(critical)
			time.sleep(0.2)

			print('\nThe {} has been destroyed by your perfectly placed strike!'.format(monster.name))
			monster.hp = 0
			crits['crit'] = True # used as flag to skip damage roll after critical hit
			return True

		# check if the weapon used has any built-in bonuses
		if player.weapon.bonus:	# returns True if the list has any contents
			if player.weapon.bonus[0] == 'Attack':
				weapon_bonus = player.weapon.bonus[1]

		# FLURRY ATTACK - additional attack mod printouts
		if atype['attack'] == 'flurry' and not crits['crit']: # don't show mods on a critical hit
			total = roll + fight_mods['player_roll'] + player.potion_mods['player_attack'] + weapon_bonus

			# print weapon bonus, if applicable
			if weapon_bonus > 0:
				time.sleep(0.6)
				print('+{} ({} bonus)'.format(weapon_bonus, player.weapon.name))

			time.sleep(0.6)
			print('+{} ({})'.format(fight_mods['player_roll'], 'flurry bonus'))

			if player.potion_mods['player_attack'] > 0:
				time.sleep(0.6)
				print('+{} ({})'.format(player.potion_mods['player_attack'], 'berzerk bonus'))

			time.sleep(0.6)
			print('= {}'.format(total))

		# FINESSE, HEADSHOT -OR- STANDARD ATTACKS - additional mod printouts
		# in these cases, THERE IS NO PLAYER ATTACK MOD TO PRINT - the attack styles modified enemy AC, not player roll
		elif (atype['attack'] == 'finesse' or atype['attack'] == 'standard' or atype['attack'] == 'headshot') and not crits['crit']:
			total = roll + player.potion_mods['player_attack'] + weapon_bonus

			if weapon_bonus > 0:
				time.sleep(0.6)
				print('+{} ({} bonus)'.format(weapon_bonus, player.weapon.name))

			if player.potion_mods['player_attack'] > 0:
				time.sleep(0.6)
				print('+{} ({})'.format(player.potion_mods['player_attack'], 'berzerk bonus'))

			if weapon_bonus > 0 or player.potion_mods['player_attack'] > 0: # a non-modified roll doesn't need the '=' printout
				time.sleep(0.6)
				print('= {}'.format(total))

		# check if hit was successul or not
		if roll + fight_mods['player_roll'] + player.potion_mods['player_attack'] + weapon_bonus >= monster.armor_class + fight_mods['enemy_armor']:
			print('You successfully hit the {} with your {}!'.format(monster.name, player.weapon.name))
			return True

		else:
			print('Your attack missed the {}, dang!'.format(monster.name))
			return False
	else:
		pass

def attack_menu_input(player, monster, fight_mods, round_num):
	"""gets player input for player attack in a battle"""

	command = ''	# again, just for C style initialization; not necessary

	active = True

	while active:

		battle_header(player, monster, round_num)	# called because menu calls will clear screen, other header call
												    # is in main event loop, but we can't cycle that just for player
												    # accessing a menu!

		print('Actions:\t Strike | Headshot | Flurry | Finesse | Help')
		print()
		print('Choose your attack...')

		command = get_input_valid(key='battle')

		# accessing menus keeps the loop running; any other input exits loop and proceeds to attack

		if command == 'help':
			print_battle_commands()
		elif command == 'i':
			player.show_inventory()
			# if player used escape potion, we need to exit this loop now
			if player.escaping == True:
				active = False
		elif command == 'b':
			player.print_player_info()
		elif command == 'm' or command == 'monster':
			monster.print_stats()
		else:
			active = False	# non-menu command entered, exit loop so battle can proceed.

	return command

def compute_attack_mods(player, monster, fight_mods, command, atype):

	attack_words = ['standard','s','attack'] # all result in standard attack

	# headshot
	if command.lower() == 'headshot' or command.lower() == 'h':
		atype['attack'] = 'headshot'
		fight_mods['enemy_armor'] = 4
		fight_mods['player_damage'] = 5

		print('Headshot attempt!')
		time.sleep(0.6)
		print('The {}\'s AC is increased to {} on this attack!'.format(monster.name, monster.armor_class + fight_mods['enemy_armor']))
		time.sleep(0.6)

	elif command.lower() == 'finesse' or command.lower() == 'fin':
		atype['attack'] = 'finesse'
		fight_mods['enemy_armor'] = 2
		fight_mods['player_damage'] = 2

		print('Finesse attack!')
		time.sleep(0.6)
		print('The {}\'s AC is increased to {} on this attack.'.format(monster.name, monster.armor_class + fight_mods['enemy_armor']))
		time.sleep(0.6)

	elif command.lower() == 'flurry' or command.lower() == 'flu':
		atype['attack'] = 'flurry'
		damage_penalty = randint(0, 3)

		fight_mods['player_roll'] = 3
		fight_mods['player_damage'] = (-damage_penalty)

		print('Flurry attack!')
		time.sleep(0.6)
		print('Attack roll will get +{} but damage will get -{}'.format(fight_mods['player_roll'], damage_penalty))
		time.sleep(0.6)

	# normal attack; could use 'else' but I might add more possible choices later.
	elif command.lower() in attack_words:
		atype['attack'] = 'standard'
		#print('Standard attack')
		#time.sleep(0.6)

def player_damage(player, monster, fight_mods, atype):

	mods = True		# used so we only print the = total damage line when there have been mods printed.

	weapon_dam_bonus = 0

	if player.weapon.bonus:
		if player.weapon.bonus[0] == 'Damage':
			weapon_dam_bonus = player.weapon.bonus[1]

	# non-headshot attack damage roll
	if atype['attack'] != 'headshot':
		damage = player.dice.roll(player.weapon.damage_roll) + fight_mods['player_damage'] + player.potion_mods['player_damage'] + weapon_dam_bonus

		# prevent negative damage from flurry + a low roll
		if damage <= 0:
			damage = 1

	# headshot damage roll (different because it's the only one with multiplication)
	else:
		damage = (player.dice.roll(player.weapon.damage_roll) + player.potion_mods['player_damage'] + weapon_dam_bonus) * 2

	# print damage roll
	player.dice.print_roll()

	# check attack type mods for printout to screen
	if atype['attack'] == 'headshot':
		time.sleep(0.6)
		print('x2 (headshot bonus)')

	elif atype['attack'] == 'flurry' and fight_mods['player_damage'] != 0:
		time.sleep(0.6)
		print('{} (flurry penalty)'.format(fight_mods['player_damage']))

	elif atype['attack'] == 'finesse':
		time.sleep(0.6)
		print('+{} (finesse bonus)'.format(fight_mods['player_damage']))

	# check weapon bonus mods for printout
	if weapon_dam_bonus > 0:
		time.sleep(0.6)
		print('+{} ({} bonus)'.format(weapon_dam_bonus, player.weapon.name))

	# check potion mods for printout
	if player.potion_mods['player_damage'] > 0:
		time.sleep(0.6)
		print('+{} (berzerk bonus)'.format(player.potion_mods['player_damage']))

	# attack mods and potion mods have been printed, so now we can print the total damage

	# this should be the only scenario in which we DON'T want the = total to printout
	if atype['attack'] == 'standard' and weapon_dam_bonus == 0 and player.potion_mods['player_damage'] == 0:
		mods = False

	if mods:	# only show this if there have been any kind of mods added
		time.sleep(0.6)
		print('= {}'.format(damage))

	print('You dealt {} points of damage to the {}'.format(damage, monster.name.upper()))

	monster.hp -= damage

	# this is here simply so the header doesn't show a negative number for monster hp
	# after monster is defeated.
	if monster.hp < 0:
		monster.hp = 0

def monster_attack(player, monster, round_num):

	# put here to be consistent with player attack
	battle_header(player, monster, round_num)

	print('The {} is attacking you!'.format(monster.name))

	# time.sleep() here ?

	roll = monster.dice.roll(20)
	monster.dice.print_roll()

	# removing monster critical hit for now...

	# if roll == 20:
	# 	print('CRITICAL HIT, OUCH!')
	# 	print('Automatic 5 points of damage, plus normal damage roll.')
	# 	player.hp -= 5
	# 	return True

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

	exp = ((monster.actual_level * 10) + randint(0,10))
	player.exp += exp

	#any gain of exp always prints a message about the gain...might need to decouple the two.
	print('You gained {} experience points!'.format(exp))

def monster_leaves_item(settings, player, monster):

	# determine if monster leaves anything behind at all
	number = randint(1, 10)
	found = ''
	found_more = ''
	not_weapon = True

	item_level = monster.actual_level # used to determine quality level of item on call to weapon and armor constructors

	# no, nothing left behind
	if number < 6:
		print()
		word = 'LOOTING {} CORPSE...'.format(monster.name.upper())
		step_printer(word, 0.04)
		time.sleep(0.3)
		print('\n...but nothing was found.')

	# yes, something is left behind
	else:
		item_list = ['gold', 'gold', 'gold', 'potion', 'potion', 'weapon', 'weapon']  # repetitions for chance ratio when choice() is used
		item_type = choice(item_list)	# grab one type randomly from item_list

		if item_type == 'potion':

			elixir = battle_create_elixir(settings)
			player.elixirs.append(elixir)

			found = 'a {} Elixir!'.format(elixir['Type'].title())
			found_more = '+1 {} Elixir to {}\'s inventory.'.format(elixir['Type'].title(), player.info['Name'])

		if item_type == 'gold':

			if settings.difficulty == 1:
				treasure_roll = randint(3,7)

			elif settings.difficulty == 2 or settings.difficulty == 3:
				treasure_roll = (randint(4, 10))

			elif settings.difficulty > 3:
				treasure_roll = (randint(3, 12) + 2)

			found = '{} Gold Pieces!'.format(treasure_roll)
			found_more = '+{} gold.'.format(treasure_roll)

			player.gold += treasure_roll

		if item_type == 'weapon':

			a_num = randint(1, 3)	# 1 creates armor, 2 and 3 create a weapon

			if a_num > 1:

				not_weapon = False
				weapon = battle_create_weapon(settings, item_level)

				print()
				word = 'LOOTING {} CORPSE...'.format(monster.name.upper())
				step_printer(word, 0.04)
				time.sleep(0.4)

				if not weapon.bonus:
					print('\nYou found a {}! \nIt deals {} damage.'.format(weapon.name, weapon.damage_roll))
				elif weapon.bonus:
					print('\nYou found a {}! \nIt deals {} damage and gets +{} to {} rolls!'.format(weapon.name, weapon.damage_roll, weapon.bonus[1], weapon.bonus[0].title()))

				time.sleep(0.8)
				print('\nDo you want to drop your old {} and take the {}?'.format(player.weapon.name, weapon.name))

				response = get_input_valid(key='yes_no')

				if response == 'n' or response == 'no':
					print('Ok, you keep your trusty {}'.format(player.weapon.name))
				elif response == 'y' or response == 'yes':
					print('Great, you\'ve replaced your {} with the {}!'.format(player.weapon.name, weapon.name))

					player.weapon = weapon

			elif a_num == 1:

				not_weapon = False
				armor = battle_create_armor(settings, item_level)

				print()
				word = 'LOOTING {} CORPSE...'.format(monster.name.upper())
				step_printer(word, 0.04)
				time.sleep(0.4)

				# this is just so the grammar of the strings below prints correctly, yepppp
				names_one = ['Dirty Sweater', 'Gross T-Shirt', 'Clean Sweater', 'Magic Sweater']

				if armor.name in names_one:
					a_string = '\nYou found a {}! It has an AC of {}.'.format(armor.name, armor.armor_class)
				else:
					a_string = '\nYou found {} Armor! It has an AC of {}.'.format(armor.name, armor.armor_class)

				print(a_string)

				time.sleep(0.8)
				print('\nDo you want to drop your {} and take the {}?'.format(player.armor.name, armor.name))

				response_armor = get_input_valid(key='yes_no')

				if response_armor == 'n' or response_armor == 'no':
					print('\nOk...I guess your {} must feel pretty comfy by now, eh?'.format(player.armor.name))
				elif response_armor == 'y' or response_armor == 'yes':
					print('\nGreat, you\'ve replaced your {} with the {}!'.format(player.armor.name, armor.name))

					player.armor = armor #mutate the player object

		# print the result to screen, except weapon find, which is already handled above.
		if not_weapon:
			print()
			word = 'LOOTING {} CORPSE...'.format(monster.name.upper())
			step_printer(word, 0.04)
			time.sleep(0.4)
			print('\nYou found {}!'.format(found))

			if found_more:
				time.sleep(0.5)
				print(found_more)

def battle_create_elixir(settings):
	"""create an elixir if one is left behind by a monster. Scales with difficulty setting"""
	elixir = {}
	elixir_types = ['health', 'health', 'health', 'berzerk', 'berzerk', 'escape', 'health max'] # 3x health so that it's more likely a choice.

	chosen_elixir = choice(elixir_types)

	# establish strength of elixir based on settings > difficulty
	if settings.difficulty < 3:										# diff is 1 or 2
		elixir_strength = 1
	elif settings.difficulty >= 3 and settings.difficulty <= 5:		# diff is 3 to 5
		elixir_strength = 2
	elif settings.difficulty > 5:									# diff is > 5
		elixir_strength = 3

	# establish cost of elixir based on type
	if chosen_elixir == 'health':
		cost = (5 * elixir_strength)
	elif chosen_elixir == 'berzerk':
		cost = 10
	elif chosen_elixir == 'escape':
		cost = 15
	elif chosen_elixir == 'health max':
		cost = 15

	# build the elixir dictionary. remember, if indexed key doesn't exist in dicionary, it gets added to it!
	elixir['Type'] = chosen_elixir
	elixir['Strength'] = elixir_strength
	elixir['Cost'] = cost

	return elixir

def battle_create_weapon(settings, item_level):

	bonus_package = []

	difficulty_one = ['Club', 'Dagger', 'Hatchet', 'Whip']
	difficulty_two = ['Shortsword', 'Axe', 'Mace', 'Flail', 'Gauntlet']
	difficulty_three = ['Longsword', 'Morning Star', 'Broadsword', 'Poleaxe', 'Trident', 'Rapier', 'Warhammer']

	if item_level == 1:
		weapon_name = choice(difficulty_one)
		weapon_dam = choice([4,6])
		bonus = 0

	elif item_level == 2:
		x = randint(1, 5)
		if x == 1 or x == 2:
			weapon_name = choice(difficulty_one)
			weapon_dam = choice([4,6])
		elif x >= 3:
			weapon_name = choice(difficulty_two)
			weapon_dam = choice([6,8,10])

	elif item_level >= 3:
		x = randint(1, 9)
		if x == 1 or x == 2:
			weapon_name = choice(difficulty_one)
			weapon_dam = choice([4,6])
		elif x >= 3 and x < 6:
			weapon_name = choice(difficulty_two)
			weapon_dam = choice([6,8,10])
		elif x >= 6:
			weapon_name = choice(difficulty_three)
			weapon_dam = choice([12,20])

	bonus_chance = randint(1, 20)
	bonus_chance += item_level 	# make this more involved

	if bonus_chance >= 13:
		bonus_type = choice(['Attack', 'Damage'])
		bonus_amount = randint(1, 3)

		bonus_package = [bonus_type, bonus_amount]

	the_weapon = Weapon(weapon_name, weapon_dam, bonus_package)

	return the_weapon

def battle_create_armor(settings, item_level):

	diff_one = ['Leather', 'Old Sweater', 'Gross T-Shirt']
	diff_two = ['Studded Leather', 'Clean Sweater', 'Broken Plate']
	diff_three = ['Blood Leather', 'Magic Sweater', 'Plate Mail']

	if item_level == 1:
		armor_name = choice(diff_one)
		if armor_name != 'Gross T-Shirt':
			armor_ac = 8 + randint(0, 4)
		else:
			armor_ac = 1		# put an easter egg where player gets some bonus for wearing the gross t-shirt

	elif item_level == 2:

		z = randint(1, 3)

		if z == 1:
			armor_name = choice(diff_one)
			if armor_name != 'Gross T-Shirt':
				armor_ac = 8 + randint(0, 4)
			else:
				armor_ac = 1

		elif z > 1:
			armor_name = choice(diff_two)
			armor_ac = 10 + randint(0, 3)

	elif item_level >= 3:

		z = randint(1, 9)

		if z == 1 or z == 2:
			armor_name = choice(diff_one)
			if armor_name != 'Gross T-Shirt':
				armor_ac = 8 + randint(0, 4)
			else:
				armor_ac = 1

		elif z > 2 and z < 6:
			armor_name = choice(diff_two)
			armor_ac = 10 + randint(0, 3)

		elif z >= 6:
			armor_name = choice(diff_three)
			armor_ac = 11 + randint(0, 4)

	the_armor = Armor(armor_name, armor_ac)

	return the_armor



























