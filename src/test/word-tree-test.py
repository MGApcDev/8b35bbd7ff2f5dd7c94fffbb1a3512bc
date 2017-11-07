import utils
from letterbranch import LetterBranch
from wordbranch import WordBranch
from hashprop import HashProp
from lamasandgroves import *

# def test_search_tree():
#     phrase = "appleandlamas"
#     HashProp.set_hash_obj(HashProp("plain", "data/sample-to-find-3.txt"))
#     phrase_dict, phrase_len = utils.phrase_to_dict(phrase)
#     letter_tree, words = LetterBranch.parse_words(phrase_dict, "data/sample")
#     LetterBranch.set_letter_tree(letter_tree)
#
#     word_tree = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)
#
#     # Check I got the 'apple' word_branch.
#     word = word_tree.children[2]
#     assert str(word.letter_branch) == 'apple'


def test_anagram_solutions_3():
    HashProp.set_hash_obj(HashProp("plain", "data/sample-to-find-3.txt"))
    # phrase = "grovesandl amas"
    phrase = "and groves lamas"
    phrase_dict, phrase_len = utils.phrase_to_dict(phrase)
    letter_tree, words = LetterBranch.parse_words(phrase_dict, "data/sample")
    LetterBranch.set_letter_tree(letter_tree)

    word_tree = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)
    anagrams = construct_word_tree_start(word_tree)

    print(anagrams)
    ''' Should produce 6 solutions:
        and - groves - lamas
        and - lamas - groves
        groves - and - lamas
        groves - lamas - and
        lamas - and - groves
        lamas - groves - and
    '''
    # assert len(anagrams) == 6
    # assert len(anagrams) == 100

    # anagrams_search = []
    # for word in word_tree.children:
    #     anagrams_search = anagrams_search + search_solved_anagrams(str(word), word)
    #
    # for ana in anagrams_search:
    #     print(ana)
    #
    # assert len(anagrams_search) == 6

    level_anagram = search_solved_words(word_tree)
    print(len(level_anagram))
    assert len(level_anagram) == 6

def test_anagram_solutions_4():
    HashProp.set_hash_obj(HashProp("plain", "data/sample-to-find-4.txt"))
    phrase = "andapplegroveslamas"
    phrase_dict, phrase_len = utils.phrase_to_dict(phrase)
    print(phrase_dict)
    print(phrase_len)

    letter_tree, words = LetterBranch.parse_words(phrase_dict, "data/sample")
    LetterBranch.set_letter_tree(letter_tree)

    word_tree = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)
    anagrams = construct_word_tree_start(word_tree)

    print(anagrams)
    ''' Should produce 24 solutions:
    '''
    # print(len(anagrams))
    # assert len(anagrams) == 24
    print('Search')

    anagrams_search = []
    for word in word_tree.children:
        anagrams_search = anagrams_search + search_solved_anagrams(str(word), word)

    print(len(anagrams_search))

    for ana in anagrams_search:
        print(ana)

    assert len(anagrams_search) == 24

    level_anagram = search_solved_words(word_tree)
    print(len(level_anagram))
    assert len(level_anagram) == 24



def test_anagram_solutions_dup():
    HashProp.set_hash_obj(HashProp("plain", "data/sample-to-find-dup.txt"))
    phrase = "andapplegrovesgroves"
    phrase_dict, phrase_len = utils.phrase_to_dict(phrase)
    print(phrase_dict)
    print(phrase_len)

    letter_tree, words = LetterBranch.parse_words(phrase_dict, "data/sample")
    LetterBranch.set_letter_tree(letter_tree)

    word_tree = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)
    anagrams = construct_word_tree_start(word_tree)

    anagrams_search = []
    for word in word_tree.children:
        anagrams_search = anagrams_search + search_solved_anagrams(str(word), word)

    print(len(anagrams_search))

    for ana in anagrams_search:
        print(ana)

    assert len(anagrams_search) == 12

    level_anagram = search_solved_words(word_tree)
    print(len(level_anagram))
    assert len(level_anagram) == 12

def test_complex_branching_3():
    HashProp.set_hash_obj(HashProp("plain", "data/sample2-to-find-3.txt"))
    phrase = "andlamasgroves"
    phrase_dict, phrase_len = utils.phrase_to_dict(phrase)
    print(phrase_dict)
    print(phrase_len)

    letter_tree, words = LetterBranch.parse_words(phrase_dict, "data/sample2")
    LetterBranch.set_letter_tree(letter_tree)

    word_tree = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)
    anagrams = construct_word_tree_start(word_tree)

    anagrams_search = []
    for word in word_tree.children:
        anagrams_search = anagrams_search + search_solved_anagrams(str(word), word)

    print(len(anagrams_search))

    for ana in anagrams_search:
        print(ana)

    assert len(anagrams_search) == 7

    level_anagram = search_solved_words(word_tree)
    print(len(level_anagram))
    assert len(level_anagram) == 7

def test_complex_branching_4():
    HashProp.set_hash_obj(HashProp("plain", "data/sample2-to-find-4.txt"))
    phrase = "applean dlam asgroves"
    phrase_dict, phrase_len = utils.phrase_to_dict(phrase)
    print(phrase_dict)
    print(phrase_len)

    letter_tree, words = LetterBranch.parse_words(phrase_dict, "data/sample2")
    LetterBranch.set_letter_tree(letter_tree)

    word_tree = WordBranch.get_word_tree_root(phrase_len, phrase_dict, words)
    anagrams = construct_word_tree_start(word_tree)

    anagrams_search = []
    for word in word_tree.children:
        anagrams_search = anagrams_search + search_solved_anagrams(str(word), word)

    print(len(anagrams_search))

    for ana in anagrams_search:
        print(ana)

    assert len(anagrams_search) == 28

    level_anagram = search_solved_words(word_tree)
    print(len(level_anagram))
    assert len(level_anagram) == 28
