def use_potion_battle(player, potion_mods): 
	"""player accesses potion inventory and uses one during a battle; adjusts HP or fight_mods accordingly"""
	
	response = ''
	current_max = len(player.elixirs)
	active = True

	while active:

		clear_screen()
		print('{}\'s ELIXIRS'.format(player.info['Name']))
		print()

		# I think the printout of elixirs and the actual usage of elixirs should be handled separately, not
		# in this one long nested-conditional chain below....fix it up / refactor this function.

		if player.elixirs:	# player has elixirs, following code is for printing and using one.

			# print the elixirs the player currently has
			count = 1
			for elixir in player.elixirs:
				print('{}{:.>22} '.format(count, elixir['Type'].title()))
				count += 1

			# create a flag for input validation
			potion_inventory_valid = False

			while not potion_inventory_valid:

				# get players choice: the number of a potion, or Q to quit this menu

				response = get_input_valid('\nEnter number of Elixir to use, or Q to quit.', 'battle_potion')

				#player chose a number higher than current inventory allows
				if response.lower() != 'q' and int(response) > current_max:
					print('You do not have an elixir stored at that number, try again.')
				
				# player entered either 'q' or a valid potion number, so we exit this validation loop
				else:
					potion_inventory_valid = True
			
			# now we check if what they entered was q, if it was, we quit by ending the main loop ('active')
			if response.lower() == 'q':
				print('Ok, save \'em for later, right? Right.')	
				#print('BTW, choice currently = {}'.format(response))
				#print(type(choice))
				active = False

			# choice was not q, so it is string of an integere
			else: 
				# index the elixir list attribute of player, then index the Type key of that chosen dictionary

				response_int = int(response) - 1	# to account for player always entering 1 greater than actual index location

				#print('BTW, choice_int currently = {}'.format(choice_int))

				if player.elixirs[response_int]['Type'] == 'health':
					bonus = 5 * player.elixirs[response_int]['Strength']
					if player.hp + bonus > player.max_hp:
						player.hp = player.max_hp
					else:
						player.hp += bonus

					time.sleep(0.06)
					step_printer('DRINKING ELIXIR...')
					print('\nYou drank the HEALTH elixir and gained {} hit points!'.format(bonus))

					del player.elixirs[response_int]
					active = False

				elif player.elixirs[response_int]['Type'] == 'berzerk':
					bonus = 4
					potion_mods['player_attack'] += bonus
					potion_mods['player_damage'] += bonus
					time.sleep(0.06)
					print('You used a BERZERK elixir. You will get +4 to Attack and Damage rolls this turn!')

					del player.elixirs[response_int]
					active = False

				elif player.elixirs[response_int]['Type'] == 'escape':

					print('You used an ESCAPE elixir! You immediately flee this battle!')
					time.sleep(0.5)
					print('You will return to the previous room...')
					time.sleep(0.5)
					del player.elixirs[response_int]
					player.escaping = True

		else: # player pressed p for potions but has none in their inventory at this time
			print('You do not have any Elixirs to use at this time, try to find some!')
			active = False

		press_enter()