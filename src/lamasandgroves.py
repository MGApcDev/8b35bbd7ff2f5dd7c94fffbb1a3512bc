'''Imports'''
import sys
import timeit
import hashlib
from collections import deque

import utils
from letterbranch import LetterBranch
from wordbranch import WordBranch
from hashprop import HashProp
# from guppy import hpy

'''Functions'''

def mark_branch(parent, child):
    '''Add a path from one WordBranch 'parent' to another WordBranch 'child'.
    Args
        parent (WordBranch) The branch to add reference to.
        child  (WordBranch) The branch to be added.
    Returns
        (bool) Return True if path was added, otherwise return False.
    '''
    if parent.valid_children == None:
        parent.valid_children = set()
    if not (child in parent.valid_children):
        parent.valid_children.add(child)
        return True

    return False

def mark_path(word_branch):
    '''Mark reference from parent to child from given branch to root.
    Args
        word_branch (WordBranch) The child branch to mark from.
    '''
    pointer = word_branch
    while pointer.origin != None:
        # Mark path of valid children
        if not mark_branch(pointer.origin, pointer):
            break # This path is already marked

        pointer = pointer.origin

def add_hash(remain_dict, word_branch):
    '''Get a unique representation of remain_dict and add reference WordBranch.
    Args
        remain_dict ({char => int}) The remaining letters of the phrase from this point in the tree.
        word_branch (WordBranch)    The WordBranch we're working on.
    Returns
        (bool) Return True if the remain_dict was a new entry in the dictionary.
    '''
    hash_to_branch = WordBranch.get_hash_to_branch()

    dict_str = utils.dict_to_str(remain_dict)
    if dict_str in hash_to_branch:
        wb = hash_to_branch[dict_str]
        if wb.valid_children != None and len(wb.valid_children) > 0:

            mark_path(word_branch)
            word_branch.valid_children = wb.valid_children

        return False
    else:
        hash_to_branch[dict_str] = word_branch
        return True

def construct_word_tree_start(word_tree_root, word_tree_children):
    '''Starting level of WordBranch tree to construct tree.
    Args
        word_branch (WordBranch) The root of WordBranch tree.
    '''
    for child in word_tree_children:
        construct_word_tree(child, child.letter_branch.remain_dict)

def construct_word_tree(word_branch, phrase_dict):
    '''Recursive function to construct WordBranch tree.
    Args
        word_branch (WordBranch)    The root of WordBranch tree.
        phrase_dict ({char => int}) The remaining letters of the phrase from this point in the tree.
    '''
    copy_dict = dict(phrase_dict)

    if add_hash(copy_dict, word_branch):
        letter_tree = LetterBranch.get_letter_tree()
        search_letter_tree(word_branch, letter_tree, copy_dict, word_branch.remain_char)

def search_letter_tree(origin, letter_branch, remain_dict, remain_char):
    '''Recursive function to search for valid words from this point in the tree.
    Args
        origin        (WordBranch)    The origin WordBranch we're doing the recursive search from
        letter_branch (LetterBranch)  The current LetterBranch we're looking at.
        remain_dict   ({char => int}) The remaining letters of the phrase from this point in the search.
        remain_char   (int)           Count of the remaining letters in the remain_dict.
    '''
    remain_char_copy = None
    remain_dict_copy = None

    for char, count in remain_dict.items():

        if count <= 0:
            continue
        if not char in letter_branch.children:
            continue

        # Decrement char in dict.
        remain_char_copy = remain_char
        remain_char_copy -= 1

        remain_dict_copy = dict(remain_dict)
        remain_dict_copy[char] -= 1

        search_letter_tree(origin, letter_branch.children[char], remain_dict_copy, remain_char_copy)

    # Free up memory.
    remain_char_copy = None
    remain_dict_copy = None

    if letter_branch.is_word:
        leaf = WordBranch(letter_branch, origin, remain_char, None)
        if remain_char == 0:
            mark_path(leaf)
        else:
            construct_word_tree(leaf, remain_dict)

def search_solved_anagrams_start(word_tree, words, max_level = 2):
    '''Do a depth first search from the root of tree.
    Args
        word_tree (WordBranch)   The tree root.
        words     ([WordBranch]) The children of the first level.
        max_level (int)          The max depth to search in the tree.
    Returns
        ([string]) Array of strings that matched the hash object.
    '''
    anagrams = []
    state = 1

    for word in words:
        new_anagrams, new_state = search_solved_anagrams(str(word), word, max_level)
        anagrams = anagrams + new_anagrams
        if new_state > state:
            state = new_state

        if state == 3: # Found all hashes
            break

    if state == 2: # Increase max_level to search one level further down
        anagrams = anagrams + search_solved_anagrams_start(word_tree, words, max_level + 1)

    return anagrams

def search_solved_anagrams(anagram_str, word_branch, max_level, level = 2):
    '''One level DFS in word tree.
    Args
        anagram_str (string)     The current build string.
        word_branch (WordBranch) The branch we're looking at in DFS.
        max_level (int)          The max depth to search in the tree.
        level       (int)        The level in the DFS / tree we're in.
    Returns
        ([string]) Array of strings that matched the hash object.
        (int)      State of program {1: continue, 2: continue with increased max_level, 3: done all hashes found}
    '''
    anagrams = []
    state = 1

    if word_branch.valid_children == None:
        return [], state

    if level > max_level:
        return [], 2

    for word_branch in word_branch.valid_children:
        new_anagram_str = anagram_str + ' ' + str(word_branch.letter_branch)
        if word_branch.remain_char == 0:
            if HashProp.valid_candidate(new_anagram_str):
                print(HashProp.get_hash_str(new_anagram_str)," --> " , new_anagram_str)
                anagrams.append(new_anagram_str)
                hash_obj = HashProp.get_hash_obj()
                if hash_obj.count == 0:
                    return anagrams, 3
        else:
            new_anagrams, new_state = search_solved_anagrams(new_anagram_str, word_branch, max_level, level + 1)
            anagrams = anagrams + new_anagrams
            if new_state > state:
                state = new_state

            if state == 3: # Terminate search
                return anagrams, state

    return anagrams, state

'''Run'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 5:
        start_time = timeit.default_timer() # Time

        phrase = args[1]
        wordlist_filename = args[2]
        hash_algo = args[3]
        hash_filename = args[4]

        phrase_dict, phrase_len = utils.phrase_to_dict(phrase)
        hash_obj = HashProp(hash_algo, hash_filename)
        HashProp.set_hash_obj(hash_obj)

        letter_tree, words = LetterBranch.parse_words(phrase_dict, wordlist_filename)
        LetterBranch.set_letter_tree(letter_tree)

        word_tree, word_tree_children = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)
        construct_word_tree_start(word_tree, word_tree_children)

        anagrams = search_solved_anagrams_start(word_tree, word_tree_children)

        elapsed = timeit.default_timer() - start_time # Time
        print('Time elapsed --> ', elapsed, 'seconds')
    else:
        print('Invalid arguments, expecting: "phrase" word_file "hash algo" hashes_file')
