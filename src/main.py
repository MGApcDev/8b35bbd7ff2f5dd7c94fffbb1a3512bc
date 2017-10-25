'''Imports'''
import sys
import hashlib

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
        letter_branch (LetterBranch)  The reference to the LetterBranch that represents the word.
        origin        (WordBranch)    The reference to the parent WordBranch.
        children      ([WordBranch])  Array of children WordBranches.
        remain_dict   ({char => int}) The remaining letters of the phrase from this point in the tree.
        remain_char   (int)           Number of characters remaining in the remain_dict.
    """
    def __init__(self,  letter_branch, origin, children, remain_dict, remain_char):
        self.letter_branch = letter_branch
        self.origin = origin
        self.children = children
        self.remain_dict = remain_dict
        self.remain_char = remain_char

    def __str__(self):
        output_str = ''
        words = []
        pointer = self
        while pointer.origin != None:
            words.append(pointer)
            pointer = pointer.origin

        words.reverse()
        for word in words:
            output_str += get_word_from_letter_branch(word.letter_branch) + ' '
            # output_str += get_word_from_letter_branch(pointer.letter_branch)

        # Remove last char --> ' '
        return output_str[:-1]

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
        (LetterBranch, [LetterBranch]) The root of the abstract syntax tree and array of word leafs.
    '''

    words = []
    root = LetterBranch(None, False, None, phrase_dict, {})

    for line in open(filename):
        word_ref = append_word_to_letter_tree(root, line, phrase_dict)
        if word_ref != None:
            words.append(word_ref)

    return (root, words)

def parse_hashes(hash_filename):
    hashes = {}
    for line in open(hash_filename):
        hashes[line[:-1]] = True

    return hashes

def get_word_from_letter_branch(letter_branch):
    '''Trace word from leaf branch to root.

    Args
        letter_branch (LetterBranch) The leaf branch to trace for word.
    Returns
        (string) The full string of represented by the leaf.
    '''
    word_str = ''
    pointer = letter_branch
    while pointer != None:
        if pointer.letter == None:
            break
        word_str += pointer.letter
        pointer = pointer.origin

    return word_str[::-1] # Flip string

def valid_candidate(candidate, hash_algo, hashes):
    hash_algo = hash_algo.lower()
    candidate_str = str(candidate)
    if hash_algo == "md5":
        local_hash = (hashlib.md5(candidate_str.encode())).hexdigest()
        # print(local_hash)
        if (local_hash in hashes):
            print('Found hash')
            return True
    elif hash_algo == 'sha1':
        pass
    elif hash_algo == "sha256":
        pass
    elif hash_algo == 'sha512':
        pass

    return False

def construct_word_tree(word_branch, letter_tree, hash_algo, hashes):
    anagrams = []

    for child in word_branch.children:
        candidates = search_letter_tree(child, letter_tree, child.remain_dict, child.remain_char)
        if len(candidates) > 0:
            for candidate in candidates:
                if candidate.remain_char == 0:
                    if valid_candidate(candidate, hash_algo, hashes):
                        anagrams.append(candidate)
            child.children = candidates
            anagrams = anagrams + construct_word_tree(child, letter_tree, hash_algo, hashes)

    return anagrams

def search_letter_tree(origin, letter_branch, remain_dict, remain_char):
    rec_solutions = []
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

        rec_solutions = rec_solutions + search_letter_tree(origin, letter_branch.children[char], remain_dict_copy, remain_char_copy)
    if letter_branch.is_word:
        rec_solutions.append(WordBranch(letter_branch, origin, [], dict(remain_dict), remain_char))
        return rec_solutions

    return rec_solutions

def get_word_tree_root(phrase_len, phrase_dict, words):
    root_children = []
    root = WordBranch(None, None, [], phrase_dict, phrase_len)
    for word in words:
        # Note: optimize remain_char count
        root_children.append(WordBranch(word, root, [], dict(word.remain_dict), phrase_len - len(get_word_from_letter_branch(word))))

    root.children = root_children
    return root

def output(anagrams):
    for anagram in anagrams:
        print(str(anagram))

'''Run'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 5:
        phrase = args[1]
        wordlist_filename = args[2]
        hash_algo = args[3]
        hash_filename = args[4]

        phrase_dict, phrase_len = phrase_to_dict(phrase)
        hashes = parse_hashes(hash_filename)

        # print(hashes)

        letter_tree, words = parse_words(phrase_dict, wordlist_filename)
        word_tree = get_word_tree_root(phrase_len, phrase_dict, words)
        anagrams = construct_word_tree(word_tree, letter_tree, hash_algo, hashes)

        output(anagrams)
    else:
        print('Invalid arguments, expecting: "<string>" filename')
