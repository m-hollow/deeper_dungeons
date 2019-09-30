import random
import time

# randint version (index the list with randint)

# def get_monster_name():

# 	filename = 'text_files/monsters.txt'

# 	with open(filename, encoding='utf-8') as file_object:
# 		monster_names = file_object.read().split()

# 	word_index = random.randint(0, len(monster_names) - 1)

# 	return monster_names[word_index]


# m1 = get_monster_name()

# print(m1)



# choice() version

def get_monster_choice():

	filename = 'text_files/monsters.txt'

	with open(filename, encoding='utf-8') as file_object:
		monster_names = file_object.read().split()

	return random.choice(monster_names)	


m = get_monster_choice()
print(m)



# NOTES...
# file is read into program as a STRING. 
# use .split() to turn that string into a LIST.

# option 1: generate a random number from 0 to the length of the list (number of strings in list)
# 	index = random.randint(0, len(monster_names) - 1)     # -1 because list starts from 0
# then, index the list of strings with that random number.
# x = monster_names[index]		or, return monster_names[index]





