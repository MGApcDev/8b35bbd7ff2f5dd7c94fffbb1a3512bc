'''Imports'''
import sys
import timeit
import hashlib

import utils
from letterbranch import LetterBranch
from wordbranch import WordBranch
from hashprop import HashProp
# from guppy import hpy

'''Functions'''

def mark_branch(parent, child):
    if parent.valid_children == None:
        parent.valid_children = {}
    if not (child in parent.valid_children):
        parent.valid_children[id(child)] = child
    else:
        return False

    return True

def mark_path(word_branch):
    pointer = word_branch
    while pointer.origin != None:
        # Mark path of valid children
        if not mark_branch(pointer.origin, pointer):
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
    hash_obj = HashProp.get_hash_obj()
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
    elif hash_algo == 'plain':
        if (candidate in hash_obj.hashes):
            return True

    return False

def valid_candidates(candidate):
    '''Validate a candidate WordBranch leaf for matching hashes_file.
    Args
        candidate (WordBranch) The WordBranch leaf to check.
    Returns
        ([string]) The array of strings that gave valid hashes.
    '''
    candidates = get_candidates(candidate, "")
    solutions = []
    for candidate in candidates:
        if valid_candidate(candidate):
            solutions.append(candidate)

    return solutions

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
        # print('Found -->', str(word_branch), '{w. remain:', dict_str, "} - ", id(wb))
        if wb.references == None:
            wb.references = []
        wb.references.append(word_branch)
        # Search for previously calculated solutions.

        # print("Begin search ------------------")
        # print("comp - ", str(word_branch), " --- ", str(word_branch.letter_branch))
        val = (False, search_solved_anagrams(str(word_branch), wb, word_branch, []))
        # return False, search_solved_anagrams(str(word_branch), wb, word_branch, [])
        # print("End search ------------------")
        return val

    else:
        # print("Adding -->", str(word_branch), '{w. remain:', dict_str, "} - ", id(word_branch))
        hash_to_branch[dict_str] = word_branch
        return True, []

def search_solved_anagrams(anagram_str, wb_up, origin, visited_branches):
    anagrams = []

    if wb_up.valid_children == None:
        # print("building:", anagram_str, " child: 0, me: " , id(wb_up))
        return []
    # else:
        # print("building:", anagram_str, " child: ", len(wb_up.valid_children))

    for hashcode, word_branch in wb_up.valid_children.items():
        new_anagram_str = anagram_str + ' ' + str(word_branch.letter_branch)
        visited_branches.append(word_branch)
        if word_branch.remain_char == 0:
            # print("Trying to validate up") # DEBUGthis
            if valid_candidate(new_anagram_str):
                mark_path(origin)
                # print("Marking branches",visited_branches)

                # visited_branches.reverse()
                for index, visited_branch in enumerate(visited_branches):
                    if index == 0:
                        mark_branch(origin, visited_branch)
                        # print("mark origin..", len(visited_branches), "from: ", str(origin.letter_branch),"to: ", str(visited_branch.letter_branch))
                    else:
                        # print("mark ", len(visited_branches), "from: ", str(visited_branches[index - 1].letter_branch),"to: ", str(visited_branch.letter_branch))
                        mark_branch(visited_branches[index - 1], visited_branch)
                # print("---- LEAF SOLUTION ---")
                # print("Origin path: ", str(word_branch))
                print((hashlib.md5(new_anagram_str.encode())).hexdigest()," --> " , new_anagram_str)
                return [new_anagram_str]
        else:
            # visited_branches.append(word_branch)
            anagrams = anagrams + search_solved_anagrams(new_anagram_str, word_branch, origin, visited_branches)

    return anagrams

def construct_word_tree_start(word_branch):
    '''Starting level of WordBranch tree to construct tree.
    Args
        word_branch (WordBranch)   The root of WordBranch tree.
    '''
    anagrams = []

    count = 0
    for child in word_branch.children:
        # print('Working on --> ', str(child.letter_branch)) # DEBUGthis
        # if add_hash(child.letter_branch.remain_dict, child):

        anagrams = anagrams + construct_word_tree(child, child.letter_branch.remain_dict, 1)
        # break

    return anagrams

def construct_word_tree(word_branch, phrase_dict, level):
    '''Recursive function to construct WordBranch tree.
    Args
        word_branch (WordBranch)    The root of WordBranch tree.
        phrase_dict ({char => int}) The remaining letters of the phrase from this point in the tree.
        level       (int)           The level depth of WordBranch tree.
    '''

    temp = ''
    for index in range(level):
        temp += '--'
    print(level, temp + '-->', str(word_branch.letter_branch))
    anagrams = []

    if level > 10:
        return []

    copy_dict = dict(phrase_dict)
    state, stored_anagrams = add_hash(copy_dict, word_branch)
    anagrams = anagrams + stored_anagrams

    if state:
        letter_tree = LetterBranch.get_letter_tree()
        anagrams = anagrams + search_letter_tree(word_branch, letter_tree, copy_dict, word_branch.remain_char, level)
    # else:
    #     print('  ' + temp + '-->', level , '-', str(word_branch.letter_branch))

    return anagrams

def search_letter_tree(origin, letter_branch, remain_dict, remain_char, level):
    '''Recursive function to search for valid words from this point in the tree.
    Args
        origin        (WordBranch)    The origin WordBranch we're doing the recursive search from
        letter_branch (LetterBranch)  The current LetterBranch we're looking at.
        remain_dict   ({char => int}) The remaining letters of the phrase from this point in the search.
        remain_char   (int)           Count of the remaining letters in the remain_dict.
        level         (int)           The level depth of WordBranch tree.
    '''
    anagrams = []
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

        anagrams = anagrams + search_letter_tree(origin, letter_branch.children[char], remain_dict_copy, remain_char_copy, level)

    # Free up memory.
    remain_char_copy = None
    remain_dict_copy = None

    if letter_branch.is_word:
        leaf = WordBranch(letter_branch, origin, None, remain_char, None, None)
        if remain_char == 0:
            mark_path(leaf)
            solutions = valid_candidates(leaf)
            for solution in solutions:
                # print("----- ROOT SOLUTION --------")
                print((hashlib.md5(solution.encode())).hexdigest()," --> " , solution)

            anagrams = anagrams + solutions
        else:
            anagrams = anagrams + construct_word_tree(leaf, remain_dict, level + 1)

    return anagrams

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

        word_tree = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)

        LetterBranch.set_letter_tree(letter_tree)
        anagrams = construct_word_tree_start(word_tree)

        print("---")
        for anagram in anagrams:
            print(anagram)

        elapsed = timeit.default_timer() - start_time # Time
        print('time --> ', elapsed)
    else:
        print('Invalid arguments, expecting: "phrase" word_file "hash algo" hashes_file')