import re, os, sys, multiprocessing, glob, operator
from random import randint

re_letters_pattern = r"[^a-zA-Z]"
# Working directory
cur_dir = os.getcwd()
# Paths to directories storing files with words
path_to_final = cur_dir + "/final/*"
path_to_misc = cur_dir + "/misc/*"

# Here we'll store all the paths to files with words
path_to_files = []
for fname in glob.glob(path_to_final):
    path_to_files.append(fname)

for fname in glob.glob(path_to_misc):
    path_to_files.append(fname)

word_bank = []

# Here we go to each file and add the words line by line to word_bank
for file_path in path_to_files:
    f = open(file_path, encoding = "ISO-8859-1")
    for line in f:
        word_bank.append(re.sub(re_letters_pattern, '', line).lower())
    f.close()

# We'll probably blow up the world if we print the list, so let's print the length
print("\nSearching through: {} words\n".format(len(word_bank)))



# Function Definition Area

def doesNotContain(word, _list):
    for letter in word:
        for bad_letter in _list:
            if letter == bad_letter:
                return False
    return True

def isProperLength(word, length):
    return len(word) == length

def letters_match(word, letters):
    for i in range(0, len(letters)):
        if letters[i] != '_':
            if word[i] != letters[i]:
                return False
    return True
# Inspired by the example that if the known is as_, the word can't be ass because the second s would already be there
def as_test(word, known):
    known = known.replace('_', '')

    word_list = []
    known_list = []
    for letter in word:
        word_list.append(letter)
    for letter in known:
        known_list.append(letter)

    #print(word_list)
    #print(known_list)

    for letter in known_list:
        index = word_list.index(letter)
        del word_list[index]

    #print(word_list)
    #print(known_list)

    for letter in known_list:
        if letter in word_list:
            return False
    return True

def fits_rules(word, exclude_list, known):
    word_length = len(known)
    return isProperLength(word, word_length) and (letters_match(word, known) and (doesNotContain(word, exclude_list) and as_test(word, known)))

def get_letter_freq(possible_words, known):
    known = known.replace('_', '')
    return_dict = dict()
    
    for pos_word in possible_words:
        pos_word_list = []
        known_list = []
        for letter in pos_word:
            pos_word_list.append(letter)
        for letter in known:
            known_list.append(letter)
        for letter in known_list:
            index = pos_word_list.index(letter)
            del pos_word_list[index]
        for letter in pos_word_list:
            if letter in return_dict:
                return_dict[letter] = return_dict[letter] + 1
            else:
                return_dict[letter] = 1
    sorted_dict = sorted(return_dict.items(), key=operator.itemgetter(1))
    sorted_dict.reverse()
    return sorted_dict
    
def get_possible_word(exclude_list, known):
    word_length = len(known)
    possible_words = []
    for word in word_bank:
        if fits_rules(word, exclude_list, known):
            if word in possible_words:
                #print("\nCalculating...\n")
                pass
            else:                        
                possible_words.append(word) 

    exclude_string = ""
    for letter in exclude_list:
        exclude_string += "{}, ".format(letter)
    exclude_string += ":"
    if len(exclude_list) == 0:
        exclude_string = "no letters:"

    print("========================")

    print("Here are all the possible words for {} excluding {}\n".format(known, exclude_string))
    print(possible_words)

    print("\nThere are {} out of {} possible words\n".format(len(possible_words), len(word_bank)))

    print("\nPossible Word Frequencies\n")
    letter_freqs = get_letter_freq(possible_words, known)
    for arr in letter_freqs:
        print("{}: {}".format(arr[0], arr[1]))
    print("I suggest guessing {}".format(letter_freqs[0][0]))

def get_possible_word_comp(exclude_list, known):
    num = 1
    while len(known.replace('_', '')) == 0:
        guess = numToLet(num)
        while guess in exclude_list:
            num += 1
            guess = numToLet(num)
        return {
            'guess': guess
        }
    print(exclude_list)
    word_length = len(known)
    possible_words = []
    for word in word_bank:
        if fits_rules(word, exclude_list, known):
            if word in possible_words:
                pass
            else:                        
                possible_words.append(word) 

    letter_freqs = get_letter_freq(possible_words, known)
    # Prints the letter freqs
    for arr in letter_freqs:
        print("{}: {}".format(arr[0], arr[1]))
    # Filters the ltter freqs for suggestions
    i = 0
    guess = letter_freqs[i][0]
    print("I will guess {}".format(guess))
    print(exclude_list)
    print(guess)
    while in_list(exclude_list, guess):
        print("Oh wait it's in the exclusion list")
        i += 1
        guess = letter_freqs[i][0]
        print("I will not guess {}".format(guess))
    return {
        'guess': guess
    }

def numToLet(num):
    lets = {
        1: 'a',
        2: 'b',
        3: 'c',
        4: 'd',
        5: 'e',
        6: 'f',
        7: 'g',
        8: 'h',
        9: 'i',
        10: 'j',
        11: 'k',
        12: 'l',
        13: 'm',
        14: 'n',
        15: 'o',
        16: 'p',
        17: 'q',
        18: 'r',
        19: 's',
        20: 't',
        21: 'u',
        22: 'v',
        23: 'w',
        24: 'x',
        25: 'y',
        26: 'z'
    }
    return lets[num]
def in_list(_list, _thing):
    print(_list)
    for x in _list:
        if _thing == x:
            return True
    return False

def generate_random_word():
    random_word = word_bank[randint(0, len(word_bank) - 1)]
    word_to_pass = ""
    for i in random_word:
        word_to_pass += "_"
    return (random_word, word_to_pass)

def is_solved(word_to_guess, bot_input):
    return word_to_guess == bot_input

def input_guess(word_to_guess, ignore_list, guess, current_word):
    original_word = word_to_guess
    original_word = original_word.replace(guess, '&')
    re_occur_pattern = r"[^&]"
    occurances = len(re.sub(re_occur_pattern, '', original_word))
    if occurances == 0:
        ignore_list.append(guess)
    for loop in range(0, occurances):
        print("\nLoop\n")
        print("Original Word: {}".format(original_word))
        print("Word To Guess: {}".format(word_to_guess))
        print("Current Word: {}".format(current_word))
        index = original_word.index('&')
        print("Index: {}".format(index))
        original_word = str_to_list(original_word)
        current_word = str_to_list(current_word)
        print("Original Word: {}".format(original_word))
        print("Current Word: {}".format(current_word))
        
        original_word[index] = guess
        current_word[index] = guess
        
        original_word = list_to_str(original_word)
        current_word = list_to_str(current_word)
        print("Original Word: {}".format(original_word))
        print("Current Word: {}".format(current_word))
    print("")
    print(ignore_list, current_word)
    return (ignore_list, current_word)

def str_to_list(_str):
    _list = []
    for letter in _str:
        _list.append(letter)
    return _list

def list_to_str(_list):
    _str = ""
    for letter in _list:
        _str += letter
    return _str

#get_possible_word(['k'], '_o__')
def play_game():
    gen = generate_random_word()
    word_to_guess = gen[0]
    bot_input = gen[1]
    ignore_list = []

    print("Chosen word is {}".format(word_to_guess))
    bot_output = "a"
    
    while is_solved(word_to_guess, bot_input) is False:
        print("Passing on {} to bot".format(bot_input))
        bot_output = get_possible_word_comp(ignore_list, bot_input)
        print("Robot guessed {}".format(bot_output["guess"]))
        ig = input_guess(word_to_guess, ignore_list, bot_output["guess"], bot_input)
        ignore_list = ig[0]
        bot_input = ig[1]
    
#print(get_possible_word_comp(['i', 'o', 'r', 't', 'n'], 'apple'))
play_game()
