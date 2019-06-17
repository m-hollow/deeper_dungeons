class RoomBook():
	"""An object that stores all the possible text strings for dungeon rooms"""
	def __init__(self):
		"""stores all the text strings for each room type"""

		self.start_text = '''I'm at the entrance of the dungeon. I have this tattered old map, but
		it does't show very much and frankly I'm not sure it's even accurate. But, it's something, and
		something is better than nothing! There's an Exit marked on the far Northern end of the dungeon.
		I'll get there, eventually...but right now, my goal is to find any and all Treasure hidden within
		these depths. And hopefully not encounter anything nasty along the way...'''

		self.empty_text = '''I'm standing in a dark, musty room. The air is stale and surprisingly humid. There's
		cobwebs all around the place, and various debris, some of which look like...bones. Everything is covered in
		a thick layer of dust. But, beyond that, there's nothing else here. This room is empty.'''

		self.monster_text = '''I'm standing in a large room with a high-ceiling. The air is warmer than the last room,
		and there's some noise coming from one of the far corners. Wait, it's getting louder. Oh dear, I think something
		is approaching me..it's a Monster!'''

		self.treasure_text = '''I'm standing in a room with a very high ceiling. It's very quiet in here, strangely so.
		There's some kind of alter at the center of the room, and something bright resting on top of it...it's treasure!'''

		self.exit_text = '''I'm standing in a long, narrow corridor. There's a large, engraded gate at the end of the passage.
		I think this must be the Exit of this dungeon!'''

		# all the text entries stored in one dictionary, indexed by room type
		
		self.room_book = {'Start':self.start_text, 'Empty':self.empty_text, 'Monster':self.monster_text, 'Treasure':
			self.treasure_text, 'Exit':self.exit_text}



# an instance of the RoomBook class is an object that contains attributes: indivdual text strings
# for each type of room, and one dictionary, room_book, which contains all those same strings.

