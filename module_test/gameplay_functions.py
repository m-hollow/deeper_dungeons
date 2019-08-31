import time
from random import randint, choice
import copy

from ui_functions import *
from classes import *
from battle import *

# define main 'game in play' functions

def action_menu(game_log):
	"""print the game_log, the map, the command menu, take user input, and return user choice"""

	clear_screen()
	game_log.print_log()	# this is THE print command of the game header -and- game map !! 
							# if you want to create loops that keep header active, you'll either need to figure out
							# how and where to move this, or call it more than once.
	
	possible_choices = ['n', 's', 'e', 'w', 'r', 'i', 'b', 'q', 'd', 'settings', 'help', 'h', 'rest']
	
	command = get_player_input().lower()

	if command in possible_choices:
		return command
	else:
		print('\nYou have entered an invalid command, try again.')
		press_enter()
		return None

	# note: the input validation performed here doesn't need to be in a while loop, because the
	# function that calls this function, game_action, has a while loop that essentially handles that.
	# if player gets the else statement above for invalid input, we fall back to game_action, which
	# has nothing left to do (command == None), so it loops, and this function is called again.

	# when that happens (action_menu is called again) it hits the clear_screen() right away, then prints
	# the gamelog again, and calls get_player_input. This mean the "successive printing down screen" effect is
	# avoided, because the screen is being -cleared and reprinted- *after the invalid input* event happens.

def game_action(settings, player, grid, game_log):

	grid.update_player_location() # needs to happen here initially so the X gets printed to board
	game_log.update_log() # same, needs to happen so its attributes are not in initial state 'None'

	active = True
	
	while active:
		# main game event loop for *game in state of play* (as opposed to game at main menu, not in play)

		command = action_menu(game_log)
		movement_choices = ['n','s', 'e', 'w']

		if command in movement_choices:
			if movement_engine(settings, player, grid, command):	# True response = player moved on board
				grid.update_player_location()
				grid.update_current_roomtype()
				game_log.update_log()

				# check if movement into new room triggers an event, and if so, trigger it.
				determine_next_event(settings, player, grid, game_log, command)

		elif command == 'i':
			"""Show inventory screen"""
			player.show_inventory()

		elif command == 'b':
			"""Show player info screen"""
			player.print_player_info()

		elif command == 'd':
			"""show room types for each grid coordinate (dev only)"""
			grid.dev_grid_showtypes()

		elif command == 'h' or command == 'help':
			command_menu(player)

		elif command == 'r' or command == 'rest':
			print('You\'re kidding, right? This is a DUNGEON. Hardly the place for a nap!')
			press_enter()

		elif command == 'settings':
			"""show the current settings; this is purely for dev purposes"""
			settings.print_settings()

		elif command == 'q':
			print('Returning to Main Menu...')
			time.sleep(0.08)
			player.reset_player()	#reset player so new game starts fresh, attributes back to initials
			settings.reset_settings()
			active = False

		else:
			pass

		if active: # we don't want to call check_player_status if user chose 'q' to quit above, so we do a check on active.
			if check_player_status(settings, player): 	# if True, player is dead, end action event loop.
				active = False
				settings.reset_settings()
				player.reset_player() # *must* happen after the settings reset!
				
			if grid.floor_exited:	# flag for player finding exit and choosing to use it during this turn (in exit event)
				grid = make_next_floor(settings, player, game_log) # successfully updates the primary grid object, because this
																   # object created here is the one getting passed around for use!
				game_log = make_next_gamelog(game_log, grid, player)
				
				grid.update_player_location() # needs to happen here just like it does above before while loop
				game_log.update_log()
		
def make_next_floor(settings, player, game_log):
	"""updates gamestate to update settings and generate new grid and log"""
	
	# update settings
	settings.difficulty += 1	# whenever make_next_floor is called, difficulty goes up by 1.
								# this is the core of the 'too linear' game structure.
	settings.grid_size += 1		# 2 seemed a bit too drastic, so it's 1 for now....
	
	grid = GameGrid(settings, player)	# create the new grid and return it
	return grid

def reset_player_location(settings, player):
	"""call this when a new dungeon floor is created so player will be at start"""
	# should this simply be a method of the Player class?

	player.player_location = [(settings.grid_size - 1), (int(settings.grid_size / 2) - 1)]
	#player.previous_coords = [0,0]

	# bug: why is the X not appearing when the new grid is first printed ?

def make_next_gamelog(game_log, grid, player):
	"""call this when a new dungeon floor is created so gamelog updates to match new dungeon grid"""
	game_log = GameLog(player, grid)

	return game_log
	
def check_player_status(settings, player): # seems we don't actually need settings ? 
	"""check in every pass of game action event loop to see if player status has changed in a way that triggers event"""

	# check if player is alive
	if player.hp <= 0:
		player.dead = True
		
		#print('\nOh damn! Looks like {} has been defeated!'.format(player.info['Name']))
		#time.sleep(0.6)
		you_are_dead(player)

		return True

	# check if player has levelled up... surely this needs to be its own function, and probably a method of
	# the player class...

	if not player.dead:
		player_level_check(settings, player)
		
	return False

def player_level_check(settings, player):
	"""checks if player can level up at end of each turn, and performs level up when applicable"""
	if player.exp >= player.next_level_at:
		player.level += 1
		player.next_level_at = player.get_level_up_val()

		clear_screen()
		text = '**** {} LEVELS UP! ****'.format(player.info['Name'].upper())
		step_printer(text, 0.04)
		time.sleep(0.8)
		print()
		print('\n{} is now Level {}. Awesome!'.format(player.info['Name'], player.level), flush=True)
		player.max_hp += 4 
		player.hp = player.max_hp # any issues here ?
		time.sleep(0.8)
		print('\n{}\'s Maximum HP has been increased to {}'.format(player.info['Name'], player.max_hp))

		press_enter()

def run_game(settings, player):	
	"""prints Main Menu and takes user input"""

	active = True

	while active: #main event loop of program running (but game not in play)

		user_action = main_menu(player)

		if user_action == 5:
			print('\nThanks for playing Deeper Dungeons!')
			print()
			active = False

		elif user_action == 1:

			player.build_player()
			player.created = True

		elif user_action == 2:

			if player.created:
				# we create the game grid object here, so that it's a brand new grid whenever option 2 (start game) is chosen
				
				# reset GameGrid *class* attribute to zero before creating a grid, otherwise it will keep incrementing on each game start
				GameGrid.floor_level = 0

				grid = GameGrid(settings, player)
				game_log = GameLog(player, grid)

				# this call to game_action effectively starts the running gameplay loop:
				game_action(settings, player, grid, game_log) 

			else:
				print('\nYou need to create a character first!')
				press_enter()

		elif user_action == 3:
			print('\nSorry, that part of the game is still being developed.')
			press_enter()

		elif user_action == 4:
			settings.print_settings()
			press_enter()

def movement_engine(settings, player, grid, selection):

	# assign current coords to previous coords because immediatley after this we change/update current coords.
	player.previous_coords = player.player_location.copy()

	if selection == 'n' and player.player_location[0] > 0:
		player.player_location[0] -= 1
	elif selection == 's' and player.player_location[0] < settings.grid_size - 1:
		player.player_location[0] += 1
	elif selection == 'e' and player.player_location[1] < settings.grid_size - 1:
		player.player_location[1] += 1
	elif selection == 'w' and player.player_location[1] > 0:
		player.player_location[1] -= 1

	# remember, the whole reason for the boolean return from this function is to separate between a
	# successful move (return true, grid update) and a border collision (return false, no grid update)
	else:
		print('\nYou\'ve hit the boundary of the dungeon!')
		press_enter()
		return False # false returned, so grid will not be updated; function exited here.

	grid.all_room_grid[player.previous_coords[0]][player.previous_coords[1]]['Visited'] = True

	return True # happens after condition code for any above condition, except else as that has its own return.

def determine_next_event(settings, player, grid, game_log, command):
	"""determine event that should occur on entering Room, and trigger that event"""
	direction = ''

	if command.lower() == 'n':
		direction = 'North'
	elif command.lower() == 's':
		direction = 'South'
	elif command.lower() == 'w':
		direction = 'West'
	elif command.lower() == 'e':
		direction = 'East'

	# we could look directly at the room dictionary stored in the all_room_grid, but it's less code to simply
	# look at the 'current_room_type' attribute of the grid, which is based on that same info anyway. (same goes for
	# room_status)

	move_text = ('Moving {}'.format(direction.title()))

	slow_print_elipsis(move_text, '', 4)

	if grid.current_room_type == 'Empty' and grid.room_status != True: # bypass print for already visited rooms.
		slow_print_elipsis('This room', 'is EMPTY.')
		time.sleep(0.8)
	elif grid.current_room_type == 'Treasure' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a TREASURE chest!')
		time.sleep(0.8)
		treasure_event(settings, player)
	
	elif grid.current_room_type == 'Exit': # no check on room_status because entering Exit room always triggers exit event!
		slow_print_elipsis('This room', 'has a staircase going down!')
		time.sleep(0.8)
		exit_event(settings, player, grid, game_log) # useful at all to use an if exit_event() here and have it return bool ??

	elif grid.current_room_type == 'Mystic' and not grid.all_room_grid[player.player_location[0]][player.player_location[1]]['Mystic_Closed']:
		slow_print_elipsis('This room', 'feels spooky...')
		time.sleep(0.8)
		mystic_event(settings, player, grid)
	elif grid.current_room_type == 'Monster' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a MONSTER!')
		time.sleep(0.8)
		battle_event(settings, player, grid, game_log)
	else:
		slow_print_elipsis('This room', 'seems familiar.')
		time.sleep(0.8)	# this else will only occur if the room being entered has already been visited.

# define room event functions -- triggered on entering unvisited room.

def treasure_event(settings, player):

	# review if / where you need press_enter() calls...

	item_level = settings.difficulty	# used to determine quality of weapons / armor on call to their constructors

	treasures = ['gold', 'gold', 'gold', 'potion', 'potion', 'weapon', 'weapon']

	treasure_type = choice(treasures)

	step_printer('OPENING CHEST...')
	time.sleep(0.1)

	if treasure_type == 'gold':

		if settings.difficulty == 1:
			treasure_roll = randint(4, 8)

		elif settings.difficulty == 2 or settings.difficulty == 3:
			treasure_roll = (randint(3, 10) + 3)

		elif settings.difficulty > 3:
			treasure_roll = (randint(3, 12) + 5)

		print('\nYou found {} Gold Pieces inside!'.format(treasure_roll))

		player.gold += treasure_roll

		time.sleep(0.6)
		print('\n{} GP +{}'.format(player.info['Name'], treasure_roll))
		press_enter()

	if treasure_type == 'potion':

		elixir = battle_create_elixir(settings)
		player.elixirs.append(elixir)

		found = 'a {} Elixir!'.format(elixir['Type'])
		found_more = '\n+1 {} Elixir to {}\'s inventory.'.format(elixir['Type'], player.info['Name'])

		print('You found {}!'.format(found))
		print(found_more)
		press_enter()

	if treasure_type == 'weapon':

		wep_or_armor = randint(1,2)

		if wep_or_armor == 1:

			weapon = battle_create_weapon(settings, item_level)

			if not weapon.bonus:
				print('\nYou found a {}! It deals {} damage.'.format(weapon.name, weapon.damage_roll))
			elif weapon.bonus:
				print('\nYou found a {}! It deals {} damage and has a +{} bonus to {} rolls!'.format(weapon.name, weapon.damage_roll, weapon.bonus[1], weapon.bonus[0].title()))

			time.sleep(0.8)
			print('\nDo you want to drop your old {} and take the {}?'.format(player.weapon.name, weapon.name))

			response = get_input_valid(key='yes_no')

			if response == 'n':
				print('Ok, you keep your trusty {}'.format(player.weapon.name))
				press_enter()
			elif response == 'y':
				print('Great, you\'ve replaced your {} with the {}!'.format(player.weapon.name, weapon.name))

				player.weapon = weapon #mutate the player object 
				press_enter()

		elif wep_or_armor == 2:
			
			armor = battle_create_armor(settings, item_level)

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

			if response_armor == 'n':
				print('Ok...I guess your {} must feel pretty comfy by now, eh?'.format(player.armor.name))
				press_enter()
			elif response_armor == 'y':
				print('Great, you\'ve replaced your {} with the {}!'.format(player.armor.name, armor.name))

				player.armor = armor #mutate the player object

				press_enter()

def mystic_event(settings, player, grid):
	
	clear_screen()
	slow_print_elipsis('An apparition is forming', 'it\'s a Mystic Merchant!')
	time.sleep(0.8)

	elixir = create_random_elixir(settings)

	print('\nMYSTIC:\nCurrently I\'m selling {} Elixir for {} gold pieces.'.format(elixir['Type'].title(), elixir['Cost']))

	active = True
	possible_choices = ['yes', 'no', 'y', 'n']

	print('\nBuy the item?')

	while active:

		response = get_player_input()

		if response not in possible_choices:
			press_enter('You did not enter a valid command, try again')

		else:
			if response.startswith('y') and elixir['Cost'] <= player.gold:
				print('\nMYSTIC:\nAn excellent decision, wise {}.'.format(player.info['Name']))

				player.elixirs.append(elixir)
				player.gold -= elixir['Cost']

				time.sleep(0.6)
				print('\n{} Elixir has been added to your inventory!'.format(elixir['Type'].title()))
				time.sleep(0.6)
				print('{} gold pieces removed.'.format(elixir['Cost']))
				time.sleep(0.8)
				slow_print_elipsis('\nThe Mystic begins to shimmer', '\nand disappears before your eyes!')

				# close this mystic now that player has purchased something from him
				grid.all_room_grid[player.player_location[0]][player.player_location[1]]['Mystic_Closed'] = True

			elif response.startswith('y') and elixir['Cost'] > player.gold:
				print('\nMYSTIC:\nI\'m sorry, but you currently cannot afford my wares.')

			elif response.startswith('n'):
				print('\nMYSTIC:\nAlright, but I hope you know what you\'re doing out there!')

			# there is no further else, all possibilities are accounted for above

			active = False
			press_enter()

def exit_event(settings, player, grid, game_log):
	"""player chooses if they will descend to next level of the dungeon"""

	print('You found the exit to the next level of the dungeon!')
	time.sleep(0.8)
	print('\nDo you want to go down the stairs now?')

	response = get_input_valid(key='exit_room')

	if response.startswith('y'):
		grid.floor_exited = True
		step_printer('DESCENDING......')
		time.sleep(0.5)

		# return True

	else:
		print('Ok, maybe next time...')
		time.sleep(0.8)

		# return False

def battle_event(settings, player, grid, game_log):
	# create a monster
	monster = Monster(settings.difficulty)		# this is where the monster is created for battle. this is where we can call
												# a function that scales monster difficulty in a less linear manner.

	encounter_monster(settings, player, monster, grid, game_log)

# define item creation / usage functions

def create_random_elixir(settings):
	"""create an elixir at random for each visit to a Mystic room. Scales with difficulty setting"""

	elixir = {}	
	elixir_types = ['health', 'health', 'health', 'berzerk', 'escape'] # 3x health so that it's more likely a choice.
	
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

	# build the elixir dictionary. remember, if indexed key doesn't exist in dicionary, it gets added to it!
	elixir['Type'] = chosen_elixir
	elixir['Strength'] = elixir_strength
	elixir['Cost'] = cost

	return elixir

	# NOTE: currently strength only applies to a health elixir, but perhaps I can work out how it effects
	# berzerk as well, etc.



