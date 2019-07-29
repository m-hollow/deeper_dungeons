import time

def load_texts():
	"""loads text from txt file and return it as list of entries"""

	filename = 'text_files/room_book.txt'
	with open(filename, encoding='utf-8') as file_object:
		room_text = file_object.read().split('X')

	return room_text

def play_timed_msg(message_one, message_two):
	"""prints two messages divided by a pause"""

	print(message_one, end='')		
	time.sleep(1.5)
	print(message_two)

all_messages = load_texts()

# play_timed_msg(all_messages[4], all_messages[5])

play_timed_msg(all_messages[2], all_messages[3])

# msg_one = "Oh no, it's a..."
# msg_two = "Monster!!!"			

# print(msg_one, end='')		
# time.sleep(1.5)
# print(msg_two)				

# print(all_messages[2], end='')
# time.sleep(1.5)
# print(all_messages[3])