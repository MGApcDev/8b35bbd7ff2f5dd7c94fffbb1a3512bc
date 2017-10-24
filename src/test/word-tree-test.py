from main import *

def test_search_tree():
    phrase_dict = phrase_to_dict("poultry outwits anpts delamgrovesaan")

    letter_tree, words = parse_words(phrase_dict, "data/sample")
    word_tree = get_tree_root(phrase_dict, words)

    assert len(word_tree.children) == 5

    # Check I got the 'apple' letter_branch.
    word = word_tree.children[2]
    assert word.letter_branch.letter == 'e'

    apple_solutions = search_tree(word.remain_dict, letter_tree, word_tree)

    assert len(apple_solutions) == 3 # valid: and, lamas, groves

    lama_solution = apple_solutions[0]
    lama_str = get_word(lama_solution.letter_branch)
    assert lama_str == 'lamas'

    lama_solutions = search_tree(lama_solution.remain_dict, letter_tree, lama_solution)

    assert len(lama_solutions) == 2 # valid: and, groves
