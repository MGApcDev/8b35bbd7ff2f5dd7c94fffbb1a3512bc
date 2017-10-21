'''Imports'''
import sys

'''Classes'''
class LetterBranch(object):
    """LetterBranch represents a single branch in the tree of all the words in the loaded dictionary.

    Attributes:
        letter      (string)             The letter for the place in the tree.
        is_word     (bool)               Whether there is a word ending in the LetterBranch object.
        origin      (LetterBranch)       The reference to the parent LetterBranch.
        remain_dict (Object.<char, int>) The remaining letters of the phrase from this point in the tree.
        used_dict   (Object.<char, int>) The used letters of the phrase for getting to this point in the tree.
    """
    def __init__(self,  letter, is_word, origin, remain_dict, children):
        self.letter = letter
        self.is_word = is_word
        self.origin = origin
        self.remain_dict = remain_dict
        self.children = children

class WordBranch(object):
    """WordBranch represents a single branch in the tree of all the valid word combinations.

    Attributes:
        letter_branch   (LetterBranch)       The reference to the LetterBranch that represents the word.
        cur_remain_dict (Object.<char, int>) The remaining letters of the phrase from this point in the tree.
    """
    def __init__(self,  letter_branch, cur_remain_dict):
        self.letter_branch = letter_branch
        self.cur_remain_dict = cur_remain_dict

'''Functions'''

def invalid_char(char):
    '''Check if character is invalid.

    Args
        char (string) The character to check.
    Returns
        (bool) The True if char should be ignored otherwise return False.
    '''
    if char == '\n' or char == ' ':
        return True

    return False

def append_word_to_tree(root, word, remain_dict_ref):
    '''Append word to abstract syntax tree.

    Args
        root            (LetterBranch)       The root of the syntax tree.
        word            (string)             The word to add.
        remain_dict_ref (Object.<char, int>) The dictionary of the remaining available characters.
    Returns
        (bool) Return True if word was added otherwise return False.
    '''
    remain_dict = dict(remain_dict_ref) # Make copy of dictionary without reference
    pointer = root
    last_char = None

    valid_word = True
    # Check the word matches the remaining characters.
    for char in word:
        if invalid_char(char): # Ignore newlines
            continue

        if not(char in remain_dict):
            valid_word = False
            break
        if remain_dict[char] <= 0:
            valid_word = False
            break
        remain_dict[char] -= 1

    if not(valid_word):
        return False

    # Append valid word to tree.
    for char in word:
        if invalid_char(char): # Ignore newlines
            continue
        last_char = char

        if not(char in pointer.children):
            pointer.children[char] = LetterBranch(char, False, pointer, {}, {})
        pointer = pointer.children[char]

    pointer.is_word = True
    pointer.remain_dict = remain_dict

    return True

def phrase_to_dict(phrase):
    '''Convert string phrase to dictionary <char, int>, mapping letters to a count of them found in a given phrase.

    Args
        phrase (string) The string phrase to convert.
    Returns
        (Object.<char, int>) Returns a dictionary of characters and a count of their appearances in the phrase.
    '''
    phrase_dict = {}
    for char in phrase:
        if char == " ": # ignore spaces
            continue
        if char in phrase_dict:
            phrase_dict[char] += 1
        else:
            phrase_dict[char] = 1
    return phrase_dict

def parse_words(phrase, filename):
    '''Parse file to abstract syntax tree.

    Args
        phrase   (string) The phrase to look for anagrams.
        filename (string) The filename of the list of available words.
    Returns
        (LetterBranch) The root of the abstract syntax tree.
    '''
    phrase_dict = phrase_to_dict(phrase)
    root = LetterBranch(None, False, None, phrase_dict, {})

    for line in open(filename):
        append_word_to_tree(root, line, phrase_dict)
        ###
        # Create first level of word-tree
        ###

    return root

def get_word(letter_branch):
    '''Trace word from leaf branch to root.

    Args
        letter_branch (LetterBranch) The leaf branch to trace for word.
    Returns
        (string) The full string of represented by the leaf.
    '''
    word_str = ''
    pointer = letter_branch
    while pointer.origin != None:
        word_str += pointer.letter
        pointer = pointer.origin

    return word_str[::-1] # Flip string

def append_to_solutions(branch_obj):
    pass

def construct_tree(phrase, letter_tree):
    pass

def find_solutions(candidates):
    pass

def output(solutions):
    pass

'''Run'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        phrase = args[1]
        wordlist_filename = args[2]

        letter_tree = parse_words(phrase, wordlist_filename)
        candidates = construct_tree(phrase, letter_tree)

        solutions = find_solutions(candidates)
        output(solutions)
    else:
        print('Invalid arguments, expecting: "<string>" filename')
