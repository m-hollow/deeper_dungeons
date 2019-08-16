import time
from random import randint, choice
import copy

# define main 'game in play' functions

def action_menu(game_log):
	"""print the game_log, the map, the command menu, take user input, and Return user choice"""

	clear_screen()
	game_log.print_log()	# this is THE print command of the game header -and- game map !! 
							# if you want to create loops that keep header active, you'll either need to figure out
							# how and where to move this, or call it more than once.
	
	possible_choices = ['c', 'n', 's', 'e', 'w', 'r', 'i', 'b', 'q', 'd']
	
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

def game_action(settings, player, grid, game_log, dice):

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

		elif command == 'c':
			"""show player the available game commands they can use"""
			command_menu(player)

		elif command == 'q':
			print('Returning to Main Menu...')
			time.sleep(0.5)
			player.reset_player()	#reset player so new game starts fresh, attributes back to initials
			#reset_grid()	# I think this is not needed; grid is constructed when menu action 2 is chosen, so will be new.
			#reset_log()	# same as grid
			active = False

		else:
			pass

		if check_player_status(settings, player): 	# if True, player is dead, end action event loop.
			active = False
			player.reset_player() # needs to be reset for new game start
			print('Returning to Main Menu...', flush=True)
			time.sleep(0.8)
		
		else:
			pass

		# need to perform checks here to see if player exited floor of dungeon on this turn.
		# if so, we need to udpate settings (difficulty, etc) and update grid to create the next level of the dungeon
		# Q: do we actually create a new dungeon object? or modify the existing one? which makes more sense?	

		# if active:		# in case anything else needs to happen here, but probably there shouldn't be.

def check_player_status(settings, player): # seems we don't actually need settings ? 
	"""check in every pass of game action event loop to see if player status has changed in a way that triggers event"""

	# check if player is alive
	if player.hp <= 0:
		player.dead = True
		print('\nOh damn! Looks like {} has been defeated!'.format(player.info['Name']))
		time.sleep(0.6)
		print('\nGAME',end='',flush=True)
		time.sleep(0.8)
		print(' OVER.')
		press_enter()
		
		return True

	# check if player has levelled up... surely this needs to be its own function, and probably a method of
	# the player class...

	if not player.dead:
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
			time.sleep(0.8)
			print('\nHP has been increased to {}'.format(player.hp))
			
			press_enter()

	return False

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
				grid = GameGrid(settings, player)
				game_log = GameLog(player, grid)
				# player entered 2, so we call game_action, which is the main 'game in play' function:
				game_action(settings, player, grid, game_log, dice) 
				# note all the locations the arguments in game_action() call are being drawn from... they're all over the place!
				# that's because of Python's weird scope rules.
				# you'd think, logically / organizationally, that this function (run_game) could only pass objects that had
				# already been passed to it. and yet....but read through it all again: dice is the only outlier!
			else:
				print('\nYou need to create a character first!')
				press_enter()

		elif user_action == 3 or user_action == 4:
			print('\nSorry, that part of the game is still being developed.')
			press_enter()

def movement_engine(settings, player, grid, selection):

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

	return True

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
	# look at the 'current_room_type' attribute of the grid, which is based on that same info anyway.

	move_text = ('Moving {}'.format(direction.title()))

	slow_print_elipsis(move_text, '', 4)

	if grid.current_room_type == 'Empty' and grid.room_status != True: # bypass print for already visited rooms.
		slow_print_elipsis('This room', 'is EMPTY.')
		time.sleep(0.8)
	elif grid.current_room_type == 'Treasure' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a TREASURE chest!')
		time.sleep(0.8)
		treasure_event(settings, player)
	elif grid.current_room_type == 'Exit' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a staircase going DOWN!')
		time.sleep(0.8)
		exit_event()
	elif grid.current_room_type == 'Mystic' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a MYSTIC!')
		time.sleep(0.8)
		mystic_event()
	elif grid.current_room_type == 'Monster' and grid.room_status != True:
		slow_print_elipsis('This room', 'has a MONSTER!')
		time.sleep(0.8)
		battle_event(settings, player, grid, game_log)
	else:
		slow_print_elipsis('This room', 'seems familiar.')
		time.sleep(0.8)	# this else will only occur if the room being entered has already been visited.

# define room event functions -- triggered on entering unvisited room.

def treasure_event(settings, player):

	if settings.difficulty == 1:
		treasure_roll = randint(1, 5)

	if settings.difficulty > 1 and settings.difficulty < 3:
		treasure_roll = (randint(1, 8) + 2)

	if settings.difficulty > 3:
		treasure_roll = (randint(1, 10) + 3)

	step_printer('OPENING CHEST...')
	print('You found {} Gold Pieces inside!'.format(treasure_roll))

	player.gold += treasure_roll

	time.sleep(0.6)
	print('{} GP +{}'.format(player.info['Name'], treasure_roll))
	press_enter()

def mystic_event():
	clear_screen()
	print('A an apparition is forming in the center of this room...')
	time.sleep(0.8)
	print('It takes on a ghostly human shape, and speaks to you!')
	time.sleep(0.8)
	print('WOULD YOU LIKE TO BUY A MAGIC ELIXIR...?')

	response = get_player_input()

	press_enter()

def exit_event():
	print('An exit event is now triggered!')
	press_enter()

def battle_event(settings, player, grid, game_log):
	# create a monster
	monster = Monster(settings.difficulty)
	encounter_monster(player, monster, grid, game_log)