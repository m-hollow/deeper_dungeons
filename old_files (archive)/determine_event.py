from random import randint
from random import choice
import time


def determine_event(current_room):
	"""look at current room type and determine event that results"""
	if current_room == 'Empty':
		pass
	if current_room == 'Monster':
		monster_event(settings, player)
	if current_room == 'Treasure':
		treasure_event(player)
	if current_room == 'Exit':
		exit_event()
	if current_room == 'Mystic':
		mystic_event(player)

def treasure_event(settings, player, dice):
	"""the harder the level is, the more gold added; this is to balance play"""
	# note: this mod system isn't very good, currently. the idea is to increase
	# how much gold a treasure room gives as the dungeon levels increase.
	gold_mod = None

	if settings.difficulty == 1:
		gold_mod = 0
	if settings.difficulty > 1 and settings.difficulty < 3
		gold_mod = dice.rolldie(3)
	if settings.difficulty > 3
		gold_mod = dice.roldie(5)

	base_gold = (dice.rolldie(10) + gold_mod)

	player.stats['GOLD'] += base_gold

	print('You found {} pieces of Gold!'.format(base_gold))

def mystic_event(settings, player):
	

