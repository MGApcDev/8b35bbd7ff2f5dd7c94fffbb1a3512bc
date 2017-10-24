from main import *

def test_search_tree():
    phrase_dict, phrase_len = phrase_to_dict("poultry outwits anpts delamgrovesaan")

    letter_tree, words = parse_words(phrase_dict, "data/sample")
    word_tree = get_word_tree_root(phrase_len, phrase_dict, words)

    # Check I got the 'apple' word_branch.
    word = word_tree.children[2]
    assert word.letter_branch.letter == 'e'

    apple_solutions = search_letter_tree(word, letter_tree, word.remain_dict, word.remain_char)

    assert len(apple_solutions) == 3 # valid: and, lamas, groves

    lama_solution = apple_solutions[0]
    lama_str = get_word_from_letter_branch(lama_solution.letter_branch)
    assert lama_str == 'lamas'

    lama_solutions = search_letter_tree(lama_solution, letter_tree, lama_solution.remain_dict, lama_solution.remain_char)

    assert len(lama_solutions) == 2 # valid: and, groves


def test_get_word_tree_root():
    phrase_dict, phrase_len = phrase_to_dict("poultry outwits anpts delamgrovesaan")

    letter_tree, words = parse_words(phrase_dict, "data/sample")
    word_tree = get_word_tree_root(phrase_len, phrase_dict, words)

    assert len(word_tree.children) == 5

    assert word_tree.origin == None
    assert word_tree.letter_branch == None
    assert word_tree.remain_dict == phrase_dict

    word = word_tree.children[2]
    assert word.letter_branch.letter == 'e' # We got the apple word_branch

    assert word.remain_dict['p'] == 0
    assert word.remain_dict['l'] == 1
    print(word.remain_char)
    assert word.remain_char == phrase_len - 5

def test_check_tree_permutations():
    phrase_dict, phrase_len = phrase_to_dict("and apple lamas")

    letter_tree, words = parse_words(phrase_dict, "data/sample")
    word_tree = get_word_tree_root(phrase_len, phrase_dict, words)

    assert len(word_tree.children) == 4 # 'app' will be in solutions, but will never complete a full anagram

    anagrams = construct_word_tree(word_tree, letter_tree)

    ''' Should produce 6 solutions:
        and - apple - lamas
        and - lamas - apple
        apple - and - lamas
        apple - lamas - and
        lamas - and - apple
        lamas - apple - and
    '''
    assert len(anagrams) == 6

    # Check permutation
    assert get_word_from_letter_branch(anagrams[0].origin.origin.letter_branch) == 'and'
    assert get_word_from_letter_branch(anagrams[0].origin.letter_branch) == 'apple'
    assert get_word_from_letter_branch(anagrams[0].letter_branch) == 'lamas'

    assert get_word_from_letter_branch(anagrams[1].origin.origin.letter_branch) == 'and'
    assert get_word_from_letter_branch(anagrams[1].origin.letter_branch) == 'lamas'
    assert get_word_from_letter_branch(anagrams[1].letter_branch) == 'apple'

    assert get_word_from_letter_branch(anagrams[4].origin.origin.letter_branch) == 'lamas'
    assert get_word_from_letter_branch(anagrams[4].origin.letter_branch) == 'and'
    assert get_word_from_letter_branch(anagrams[4].letter_branch) == 'apple'
