from random import randint

class Potion():
	"""Creates a Potion object to be used by player"""

	def __init__(self, p_type):
		self.p_type = p_type
		self.type = self.determine_type()

	def determine_type(self):
		"""used to determine type of potion object"""
		if self.p_type == 'h':
			return 'HEAL'
		elif self.p_type == 'ha':
			return 'HEAL ADV'
		elif self.p_type == 's':
			return 'STRENGTH'
		elif self.p_type == 'sa':
			return 'STRENGTH ADV'
		elif self.p_type == 'i':
			return 'INVISIBLE'
		elif self.p_type == 's':
			return 'SPEED'
		elif self.p_type == 'r':
			# add speed potion to this randomization
			num = randint(1,10)
			if num == 10:
				return 'INVISIBLE'
			if num == 9:
				return 'STRENGTH ADV'
			if num == 8:
				return 'HEAL ADV'
			if num <= 4:
				return 'HEAL'
			if num > 4 and num < 8:
				return 'STRENGTH'

	def use_potion(self):
		"""method for player to use the potion object"""

		# should this be a player class method ?

	def p_info(self):
		print('TYPE: {}'.format(self.type))


potion = Potion('r')
potion.p_info()		
