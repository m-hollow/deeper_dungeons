def create_room_text(self):
		"""prints text describing current room, based on room type"""

		if self.room == 'Empty':
			self.room_text = 'There doesn\'t appear to be anything in this room. What a relief!'

		if self.room == 'Monster':
			self.room_text = 'I think I something is in here with me...oh drat, here it comes!!!'

		if self.room == 'Treasure':
			self.room_text = 'I see something in the center of the room -- a large, ornate chest!'