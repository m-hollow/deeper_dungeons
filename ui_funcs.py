from random import randint
from random import choice
import time

from classes import *

# all UI functions for Deeper Dungeons

def press_enter(text=None):
	if text:
		print(text)
	msg = '...'
	input(msg)

def get_player_input(text=None):
	if text:
		print(text)
	msg = '\n> '
	player_input = input(msg)
	return player_input

def clear_screen():
	"""simple command to clear the game screen"""
	print("\033[H\033[J")

def step_printer(word):
	for c in range(len(word)):
		print(c, end='', flush=True)
		time.sleep(0.06)

def slow_print_two(word_one, word_two):
	print(word_one, end='', flush=True)
	time.sleep(0.08)
	print(word_two)

def slow_print_elipsis(word_one, word_two):
	"""prints first word, step prints elipsis, prints second word"""
	elipsis_long = '......'
	#elipsis = '.' * 6

	# print the first word
	print(word_one, end='', flush=True)
	
	# step print the elipsis string
	for c in elipsis_long:
		print(c, end='', flush=True)
		time.sleep(0.06)

	# print the second word
	print(word_two, flush=True)