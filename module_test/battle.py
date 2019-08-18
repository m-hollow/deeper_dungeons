# define all Battle functions

def encounter_monster(player, monster, grid, game_log):
	"""monster is engaged and decision to fight or run is chosen by player"""
	clear_screen()

	# determine how difficult it is for player to run away successfully
	run_difficulty = int(randint(2,10) + (3 * monster.difficulty))

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
				battle_main(player, monster, run_failed)
						
def run_attempt(player, run_difficulty):
	"""rolls player dice, prints out roll, returns True if roll beats run_dc, False otherwise"""
	roll = player.dice.roll(20)
	player.dice.print_roll()
	return (roll >= run_difficulty)		# returns a bool

def battle_main(player, monster, run_failed):

	turn = 0
	round_num = 1
	fight_mods = {'enemy_armor': 0, 'player_roll': 0, 'player_damage': 0}

	atype = {'attack': None}
	crits = {'crit': False}
	player_turn = True
	
	if run_failed:
		player_turn = False

	active = True

	while active:

		battle_header(player, monster, round_num)

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
		if check_battle_status(player, monster, crits):
			active = False	# player or monster is dead, so end the battle loop.

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
			atype['attack'] = None

		elif not active:					# shouldn't this be the same result as just 'else'? but it didn't work...
			print('The battle is over!')
			press_enter()	#  second of two calls to press_enter, for pause before ending battle sequence.
			# clear_screen()

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

def check_battle_status(player, monster, crits):
	"""checks state of player and monster to determine if battle is over, or should continue"""
	
	#check player
	if player.hp <= 0:
		print('\nYou have been defeated by the {}!'.format(monster.name))
		player.dead = True
		time.sleep(0.8)
		return True

	elif monster.hp <= 0:
		if not crits['crit']:
			print('\nYou have destroyed the {}!'.format(monster.name))
		else:
			print()	# this may not be necessary, need to playtest on critical hit success for line spacing.

		time.sleep(0.8)
		gain_exp(player, monster)
		time.sleep(0.8)
		return True
	
	else:
		# neither player nor monster has been defeated, fight will continue.
		return False

def player_attack(player, monster, fight_mods, round_num, crits, atype):
	"""runs all player attack functions and returns a bool to call in battle_main function"""

	command = attack_menu_input(player, monster, fight_mods, round_num)

	# if applicable, fight_mods will be updated by this call
	compute_attack_mods(player, monster, fight_mods, command, atype)

	# compute_potion_mods(player)

	# here is the actual attack die roll...
	roll = player.dice.roll(20)
	player.dice.print_roll()
	
	# check if roll is a critical hit
	if roll == 20:
		print('CRITICAL HIT!')
		print('The {} has been destroyed by your perfectly placed strike!'.format(monster.name))
		monster.hp = 0
		crits['crit'] = True # used as flag to skip damage roll after critical hit
		return True

	# check if there are fight mods to Player Roll to display on screen
	# note: headshot doesn't appear here because it mods Enemy AC, not the player roll!

	if atype['attack'] == 'flurry' and not crits['crit']: # don't show mods on a critical hit
		total = roll + fight_mods['player_roll']
		time.sleep(0.6)
		print('+{} ({})'.format(fight_mods['player_roll'], 'flurry bonus')) 
		time.sleep(0.6)
		print('= {}'.format(total))

	elif (atype['attack'] == 'finesse' or atype['attack'] == 'standard') and not crits['crit']:
		pass # no mods to Player Roll on a standard or finesse attack.

	# check if hit was successul or not
	if roll + fight_mods['player_roll'] >= monster.armor_class + fight_mods['enemy_armor']:
		print('You successfully hit the {} with your {}!'.format(monster.name, player.weapon.name))
		return True

	else:
		print('Your attack missed the {}, dang!'.format(monster.name))
		return False

def attack_menu_input(player, monster, fight_mods, round_num):
	"""gets player input for player attack in a battle"""

	command = ''	# again, just for C style initialization; not necessary

	active = True

	while active:

		battle_header(player, monster, round_num)	# called because menu calls will clear screen

		print('Actions:\t Strike | Headshot | Flurry | Finesse | Help')
		print()
		print('Choose your attack...')

		command = get_input_valid(key='battle')

		# accessing menus keeps the loop running; any other input exits loop and proceeds to attack

		if command == 'help':
			print_battle_commands()
		elif command == 'p':
			print('This is how you will use a potion, eventually.')
			press_enter()
		elif command == 'i':
			player.show_inventory()
		elif command == 'b':
			player.print_player_info()
		elif command == 'print':
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

	# non-headshot attack damage roll
	if atype['attack'] != 'headshot':
		damage = player.dice.roll(player.weapon.damage) + fight_mods['player_damage']

		# prevent negative damage from flurry + a low roll
		if damage <= 0:
			damage = 1

	# headshot damage roll (different because it's the only one with multiplication)
	else:
		damage = player.dice.roll(player.weapon.damage) * 2
	
	# print damage roll
	player.dice.print_roll()

	if atype['attack'] == 'headshot':
		time.sleep(0.6)
		print('x2 (headshot bonus)')
		time.sleep(0.6)
		print('= {}'.format(damage))

	elif atype['attack'] == 'flurry' and fight_mods['player_damage'] != 0:
		time.sleep(0.6)
		print('{} (flurry penalty)'.format(fight_mods['player_damage']))
		time.sleep(0.6)
		print('= {}'.format(damage))

	elif atype['attack'] == 'finesse':
		time.sleep(0.6)
		print('+{} (finesse bonus)'.format(fight_mods['player_damage']))
		time.sleep(0.6)
		print('= {}'.format(damage))
	else:
		pass # standard attack prints no modifiers

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

	exp = ((monster.difficulty * 10) + randint(0,10))
	player.exp += exp

	#any gain of exp always prints a message about the gain...might need to decouple the two.
	print('You gained {} experience points.'.format(exp))
	time.sleep(0.08)