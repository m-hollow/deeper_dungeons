from random import randint

class Room():
	"""Generates a room of a specific type, semi-randomly"""

	def __init__(self, dice):
		self.dice = dice
		self.room_type = self.room_select()

	def room_select(self):
		room_type = ''
		roll = self.dice.rolldie()

		if roll >=  1 and roll <= 35:
			room_type = 'EMPTY_1'
		elif roll > 35 and roll <= 42:
			room_type = 'ITEM'
		elif roll > 42 and roll <= 65:
			room_type = 'MONSTER'
		elif roll > 65 and roll <= 75:
			room_type = 'TREASURE'
		elif roll > 75 and roll <= 82:
			room_type = 'STORY'
		elif roll > 82 and roll <= 100:
			room_type = 'EMPTY_2'

		return room_type

	def print_roomtype(self):
		print('This room was generated as type {}'.format(self.room_type))


class Dice():

	def __init__(self, sides=6):
		self.sides = sides

	def rolldie(self):
		roll = randint(1, self.sides)
		return roll

d100 = Dice(100)

room1 = Room(d100)

room1.print_roomtype()
