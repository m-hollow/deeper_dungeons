import time
import random

class RoomBook():
	"""loads room text and builds dictionary of all separated entries"""
	def __init__(self):
		self.all_entries = self.load_entries()

		self.room_dict = {
		'Start':self.all_entries[0],
		'Empty':self.all_entries[1],
		'Monster':self.all_entries[2],
		'itsMonst':self.all_entries[3],
		'Treasure':self.all_entries[4],
		'itsTreas':self.all_entries[5],
		'itsItem':self.all_entries[6],
		'Exit':self.all_entries[7],
		'Mystic':self.all_entries[8]
		}

	def load_entries(self):
		filename = 'text_files/room_book.txt'
		with open(filename, encoding='utf-8') as file_object:
			room_text = file_object.read().split('X')

		return room_text

book = RoomBook()

# read() returns a string; but then split() returns it as a list, separator 'X'
# print(type(book.all_entries))

# example of timed printing...build a function in GameLog class to do this.
# print(book.all_entries[2], end='')
# time.sleep(1)
# print(book.all_entries[3])

msg = book.room_dict['Mystic']
print(msg)

print(type(book.room_dict['Start']))  # confirms that each entry is a string

# it makes way more sense to index each text chunk by a key that is set to the room type, rather 
# than indexing by arbitrary int. So, you start with a list in which each entry is indexed by an int,
# but then you build a dictionary from the contents of that list so each can be indexed by room
# key.







