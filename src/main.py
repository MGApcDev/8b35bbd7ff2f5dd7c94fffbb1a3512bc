'''Imports'''
import sys
import timeit
import hashlib
# from guppy import hpy

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

    def __str__(self):
        '''Trace word from leaf branch to root.
        Args
            self (LetterBranch) The leaf branch to trace for word.
        Returns
            (string) The full string of represented by the leaf.
        '''
        word_str = ''
        pointer = self
        while pointer != None:
            if pointer.letter == None:
                break
            word_str += pointer.letter
            pointer = pointer.origin

        return word_str[::-1] # Flip string

class WordBranch(object):
    """WordBranch represents a single branch in the tree of all the valid word combinations.

    Attributes:
        letter_branch (LetterBranch)  The reference to the LetterBranch that represents the word.
        origin        (WordBranch)    The reference to the parent WordBranch.
        children      ([WordBranch])  Array of children WordBranches.
        remain_char   (int)           Number of characters remaining in the remain_dict.
    """
    def __init__(self,  letter_branch, origin, children, remain_char, references, valid_children):
        self.letter_branch = letter_branch
        self.origin = origin
        self.children = children
        self.remain_char = remain_char
        self.references = references
        self.valid_children = valid_children

    def __str__(self):
        '''Trace words from leaf branch to root.
        Args
            self (WordBranch) The leaf branch to trace for word.
        Returns
            (string) The full string of represented by the leaf.
        '''
        output_str = ''
        words = []
        pointer = self
        while pointer.origin != None:
            words.append(pointer)
            pointer = pointer.origin

        words.reverse() # Put words in the right order
        for word in words:
            output_str += str(word.letter_branch) + ' '

        # Remove last char --> ' '
        return output_str[:-1]

class Hash(object):
    """Hash object to keep information of the hashes to find.
    Attributes:
        hash_algo (string)           The hash algorithm to hash with.
        hashes    ({string => bool}) The hashes and their state of if they were found.
    """
    def __init__(self,  hash_algo, hash_filename):
        self.algo = hash_algo.lower() # Lowercase algorithm
        self.hashes = self.parse_hashes(hash_filename)

    def parse_hashes(self, hash_filename):
        hashes = {}
        for line in open(hash_filename):
            hashes[line[:-1]] = True

        return hashes

hash_obj = None
def set_hash_obj(obj):
    global hash_obj
    hash_obj = obj

def get_hash_obj():
    global hash_obj
    return hash_obj

letter_tree = None
def set_letter_tree(letter_branch):
    global letter_tree
    letter_tree = letter_branch

def get_letter_tree():
    global letter_tree
    return letter_tree

'''Functions'''

def invalid_char(char):
    '''Check if character is invalid in a word.
    Args
        char (string) The character to check.
    Returns
        (bool) The True if char should be ignored otherwise return False.
    '''
    if char == '\n' or char == ' ':
        return True

    return False

def append_word_to_letter_tree(root, word, remain_dict_ref):
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
        (int)           Returns the length of the phrase, not including invalid characters like spaces.
    '''
    phrase_dict = {}
    phrase_len = 0
    for char in phrase:
        if invalid_char(char): # ignore spaces
            continue
        if char in phrase_dict:
            phrase_dict[char] += 1
            phrase_len += 1
        else:
            phrase_dict[char] = 1
            phrase_len += 1

    return phrase_dict, phrase_len

def parse_words(phrase_dict, filename):
    '''Parse file to abstract syntax tree.
    Args
        phrase   (string) The phrase to look for anagrams.
        filename (string) The filename of the list of available words.
    Returns
        (LetterBranch)   The root of the abstract syntax tree.
        ([LetterBranch]) An array of word leafs representing the words available.
    '''
    words = []
    root = LetterBranch(None, False, None, phrase_dict, {})

    for line in open(filename):
        word_ref = append_word_to_letter_tree(root, line, phrase_dict)
        if word_ref != None:
            words.append(word_ref)

    return root, words

def dict_to_str(remain_dict):
    '''Parse a dictionary to string representation, e.g. {p:1, f:0, t:3} => pttt.
       Note: Ordering the string doesn't matter.
    Args
        remain_dict ({char => int}) The remaining characters in dictionary.
    Returns
        (string) The string representation.
    '''
    dict_str = ""
    for key, value in remain_dict.items():
        for value in range(value):
            dict_str += key

    return dict_str

# ------------------------------------------------------------------------------------------------ \/

def mark_path(word_branch):
    pointer = word_branch
    while pointer.origin != None:
        # Mark path of valid children
        if pointer.origin.valid_children == None:
            pointer.origin.valid_children = {}
        if not (pointer in pointer.origin.valid_children):
            pointer.origin.valid_children[id(pointer)] = pointer
        else: # WB is already stored so we break
            break
        pointer = pointer.origin

def get_candidates(word_branch, word_str):
    '''Search down to root of WordBranch tree and considering the references for identical subproblems.
    Args
        word_branch (WordBranch) The WordBranch to search from.
        word_str    (string)     The building string of the candidate.
    Returns
        ([string]) The array of strings candidates.
    '''
    if word_branch.origin == None:
        return [word_str[:-1]]

    candidates = []
    word_str = str(word_branch.letter_branch) + ' ' + word_str
    if word_branch.references != None:
        for ref in word_branch.references:
            candidates = candidates + get_candidates(ref.origin, word_str)

    candidates = candidates + get_candidates(word_branch.origin, word_str)

    return candidates

def valid_candidate(candidate):
    hash_obj = get_hash_obj()
    hash_algo = hash_obj.algo

    if hash_algo == "md5":
        local_hash = (hashlib.md5(candidate.encode())).hexdigest()
        if (local_hash in hash_obj.hashes):
            return True
    elif hash_algo == 'sha1':
        pass
    elif hash_algo == "sha256":
        pass
    elif hash_algo == 'sha512':
        pass

    return False

def valid_candidates(candidate):
    '''Validate a candidate WordBranch leaf for matching hashes_file.
    Args
        candidate (WordBranch) The WordBranch leaf to check.
    Returns
        ([string]) The array of strings that gave valid hashes.
    '''
    candidates = get_candidates(candidate, "")
    # candidates = [str(candidate)]
    solutions = []
    for candidate in candidates:
        print("Trying to validate down") # DEBUGthis
        if valid_candidate(candidate):
            solutions.append(candidate)
        # candidate = candidate[::-1]
        # print('-', candidate, '-')

    return solutions

hash_to_branch = {}
def add_hash(remain_dict, word_branch):
    '''Get a unique representation of remain_dict and add reference WordBranch.
    Args
        remain_dict ({char => int}) The remaining letters of the phrase from this point in the tree.
        word_branch (WordBranch)    The WordBranch we're working on.
    Returns
        (bool) Return True if the remain_dict was a new entry in the dictionary.
    '''
    global hash_to_branch

    dict_str = dict_to_str(remain_dict)
    # print("--> ", dict_str)
    if dict_str in hash_to_branch:
        wb = hash_to_branch[dict_str]
        if wb.references == None:
            wb.references = []
        wb.references.append(word_branch)
        # Search for previously calculated solutions.
        search_solved_anagrams(str(word_branch), wb)

        # print("Appending <-- ", dict_str)
        return False
    else:
        hash_to_branch[dict_str] = word_branch
        return True

def search_solved_anagrams(anagram_str, wb_up):
    # print("down_str --> ", anagram_str)
    if wb_up.valid_children == None:
        return
    for hashcode, word_branch in wb_up.valid_children.items():
        new_anagram_str = anagram_str + ' ' + str(word_branch.letter_branch)
        if word_branch.remain_char == 0:
            print("Trying to validate up") # DEBUGthis
            if valid_candidate(new_anagram_str):
                print("Found solve from leaf searching")
                print((hashlib.md5(new_anagram_str.encode())).hexdigest()," --> " , new_anagram_str)
        else:
            search_solved_anagrams(new_anagram_str, word_branch)


def construct_word_tree_start(word_branch):
    '''Starting level of WordBranch tree to construct tree.
    Args
        word_branch (WordBranch)   The root of WordBranch tree.
    '''
    count = 0
    for child in word_branch.children:
        print('Working on --> ', str(child.letter_branch)) # DEBUGthis
        # if add_hash(child.letter_branch.remain_dict, child):

        construct_word_tree(child, child.letter_branch.remain_dict, 1)
        # break

def construct_word_tree(word_branch, phrase_dict, level):
    '''Recursive function to construct WordBranch tree.
    Args
        word_branch (WordBranch)    The root of WordBranch tree.
        phrase_dict ({char => int}) The remaining letters of the phrase from this point in the tree.
        level       (int)           The level depth of WordBranch tree.
    '''
    if level > 2:
        return []

    copy_dict = dict(phrase_dict)
    if add_hash(copy_dict, word_branch):
        letter_tree = get_letter_tree()
        search_letter_tree(word_branch, letter_tree, copy_dict, word_branch.remain_char, level)

def search_letter_tree(origin, letter_branch, remain_dict, remain_char, level):
    '''Recursive function to search for valid words from this point in the tree.
    Args
        origin        (WordBranch)    The origin WordBranch we're doing the recursive search from
        letter_branch (LetterBranch)  The current LetterBranch we're looking at.
        remain_dict   ({char => int}) The remaining letters of the phrase from this point in the search.
        remain_char   (int)           Count of the remaining letters in the remain_dict.
        level         (int)           The level depth of WordBranch tree.
    '''
    remain_char_copy = None
    remain_dict_copy = None

    for char, count in remain_dict.items():

        # print('looking at --> ', char, ' --- ', count)
        if count <= 0:
            continue
        if not char in letter_branch.children:
            continue

        # Decrement char in dict
        remain_char_copy = remain_char
        remain_char_copy -= 1

        remain_dict_copy = dict(remain_dict)
        remain_dict_copy[char] -= 1

        search_letter_tree(origin, letter_branch.children[char], remain_dict_copy, remain_char_copy, level)

    # Free up memory
    remain_char_copy = None
    remain_dict_copy = None

    if letter_branch.is_word:
        leaf = WordBranch(letter_branch, origin, None, remain_char, None, None)
        if remain_char == 0:
            mark_path(leaf)
            solutions = valid_candidates(leaf)
            for solution in solutions:
                print("Found solution from root searching")
                print((hashlib.md5(solution.encode())).hexdigest()," --> " , solution)

        construct_word_tree(leaf, remain_dict, level + 1)

def get_word_tree_root(phrase_len, phrase_dict, words):
    '''Construct the root object of the WordBranch tree.
    Args
        phrase_len  (int)            Count of valid characters in phrase.
        phrase_dict ({char => int})  The remaining letters of the phrase.
        words       ([LetterBranch]) Array of all the available words as LetterBranch.
    Returns
        (WordBranch) The root of WordBranch tree.
    '''
    root_children = []
    root = WordBranch(None, None, [], phrase_len, None, None)
    for word in words:
        # Note: optimize remain_char count
        root_children.append(WordBranch(word, root, [], phrase_len - len(str(word)), None, None))

    root.children = root_children
    return root

'''Run'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 5:
        start_time = timeit.default_timer() # Time
        phrase = args[1]
        wordlist_filename = args[2]
        hash_algo = args[3]
        hash_filename = args[4]

        phrase_dict, phrase_len = phrase_to_dict(phrase)
        hash_obj = Hash(hash_algo, hash_filename)
        set_hash_obj(hash_obj)


        letter_tree, words = parse_words(phrase_dict, wordlist_filename)

        word_tree = get_word_tree_root(phrase_len, phrase_dict, words)

        set_letter_tree(letter_tree)
        construct_word_tree_start(word_tree)

        elapsed = timeit.default_timer() - start_time # Time
        print('time --> ', elapsed)
    else:
        print('Invalid arguments, expecting: "phrase" word_file "hash algo" hashes_file')
