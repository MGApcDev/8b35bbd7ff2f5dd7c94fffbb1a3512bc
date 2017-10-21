'''Imports'''
import sys

'''Classes'''
class LetterBranch(object):
    """LetterBranch represents a single branch in the tree of all the words in the loaded dictionary.

    Attributes:
        letter      (string)                 The letter for the place in the tree.
        is_word     (bool)                   Whether there is a word ending in the LetterBranch object.
        origin      (LetterBranch)           The reference to the parent LetterBranch.
        remain_dict ({char => int})          The remaining letters of the phrase from this point in the tree.
        children    ({char => LetterBranch}) Dictionary of characters to children LetterBranches.
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
        letter_branch   (LetterBranch)  The reference to the LetterBranch that represents the word.
        cur_remain_dict ({char => int}) The remaining letters of the phrase from this point in the tree.
        origin          (WordBranch)    The reference to the parent WordBranch.
        children        ([WordBranch])  Array of children WordBranches.
    """
    def __init__(self,  letter_branch, cur_remain_dict, origin, children):
        self.letter_branch = letter_branch
        self.cur_remain_dict = cur_remain_dict
        self.origin = origin
        self.children = children

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
        remain_dict_ref ({char => int})      The dictionary of the remaining available characters.
    Returns
        (LetterBranch) Return the leaf branch of the word if word was added otherwise return None.
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
        return None

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

    return pointer

def phrase_to_dict(phrase):
    '''Convert string phrase to dictionary <char, int>, mapping letters to a count of them found in a given phrase.

    Args
        phrase (string) The string phrase to convert.
    Returns
        ({char => int}) Returns a dictionary of characters and a count of their appearances in the phrase.
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

def parse_words(phrase_dict, filename):
    '''Parse file to abstract syntax tree.

    Args
        phrase   (string) The phrase to look for anagrams.
        filename (string) The filename of the list of available words.
    Returns
        (LetterBranch, [LetterBranch]) The root of the abstract syntax tree and array of word leafs.
    '''

    words = []
    root = LetterBranch(None, False, None, phrase_dict, {})

    for line in open(filename):
        word_ref = append_word_to_tree(root, line, phrase_dict)
        if word_ref != None:
            words.append(word_ref)

    return (root, words)

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


def rec_search(word_branch):
    pass

def construct_tree(root, letter_tree, words):
    for child in root.children:
        candidates = search_tree(child.remain_dict, letter_tree)

def find_solutions(candidates):
    pass

def search_tree(remain_dict, letter_branch):
    rec_solutions = []
    for char, count in remain_dict.items():
        if count <= 0:
            continue
        if !(char in letter_branch.children):
            continue
        remain_copy = dict(remain_dict)
        remain_copy[char] -= 1
        rec_solutions.concat(search_tree(remain_copy, letter_branch.children[char]))
    if letter_branch.is_word:
        return rec_solutions.append(letter_branch)
    else:
        return rec_solutions


def get_tree_root(phrase_dict, words):
    root_children = []
    root = WordBranch(None, phrase_dict, None, [])
    for word in words:
        root_children.append(WordBranch(word, dict(word.remain_dict), root, []))

    root.children = root_children
    return root

def output(solutions):
    pass

'''Run'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        phrase = args[1]
        wordlist_filename = args[2]

        phrase_dict = phrase_to_dict(phrase)

        letter_tree, words = parse_words(phrase_dict, wordlist_filename)
        tree_root = get_tree_root(phrase_dict, words)
        candidates = construct_tree(tree_root, letter_tree, words)

        solutions = find_solutions(candidates)
        output(solutions)
    else:
        print('Invalid arguments, expecting: "<string>" filename')
