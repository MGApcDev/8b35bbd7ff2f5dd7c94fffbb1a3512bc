import utils
from letterbranch import LetterBranch

def test_phrase_to_dict_simple():
    phrase_dict, phrase_len = utils.phrase_to_dict("abc")
    assert len(phrase_dict.keys()) == 3
    assert phrase_dict['a'] == 1
    assert phrase_dict['c'] == 1
    assert ("d" in phrase_dict) == False

def test_phrase_to_dict_repeat_and_multiple_words_and_distinct_case():
    phrase_dict, phrase_len = utils.phrase_to_dict("apple of Eden")
    assert len(phrase_dict.keys()) == 9
    assert phrase_dict['a'] == 1
    assert phrase_dict['p'] == 2
    assert phrase_dict['e'] == 2
    assert phrase_dict['E'] == 1
    assert (" " in phrase_dict) == False # ignore spaces

def test_append_word_to_tree_single():
    phrase_dict, phrase_len = utils.phrase_to_dict("apple of Eden")
    root = LetterBranch(None, False, None, phrase_dict, {})
    LetterBranch.append_word_to_letter_tree(root, "pale\n", phrase_dict)

    assert root.children['p'] != None
    assert root.children['p'].children['a'] != None
    assert root.children['p'].children['a'].children['l'] != None
    assert root.children['p'].children['a'].children['l'].children['e'] != None

def test_append_word_to_tree_multiple():
    phrase_dict, phrase_len = utils.phrase_to_dict("apple of Edenmot kaes")
    root = LetterBranch(None, False, None, phrase_dict, {})

    remain_dict = phrase_dict

    ret = LetterBranch.append_word_to_letter_tree(root, "pale\n", remain_dict)
    assert ret != None # Check that word was added

    ret = LetterBranch.append_word_to_letter_tree(root, "pakes\n", remain_dict)
    assert ret != None

    ret = LetterBranch.append_word_to_letter_tree(root, "tom\n", remain_dict)
    assert ret != None

    ret = LetterBranch.append_word_to_letter_tree(root, "applew", remain_dict) # Invalid word
    assert ret == None

    # Check tree structure
    assert root.children['p'] != None
    assert root.children['p'].children['a'] != None
    assert root.children['p'].children['a'].children['l'] != None
    assert root.children['p'].children['a'].children['l'].children['e'] != None

    assert root.children['p'].children['a'].children['k'] != None
    assert root.children['p'].children['a'].children['k'].children['e'] != None
    assert root.children['p'].children['a'].children['k'].children['e'].children['s'] != None
    assert root.children['p'].children['a'].children['k'].children['e'].children['s'].is_word == True

    assert root.children['t'] != None
    assert root.children['t'].children['o'] != None
    assert root.children['t'].children['o'].children['m'] != None

    # Check is_word
    assert root.children['p'].children['a'].children['l'].is_word == False
    assert root.children['p'].children['a'].children['l'].children['e'].is_word == True

    # Check local remain_dict
    assert root.children['p'].children['a'].children['k'].children['e'].children['s'].remain_dict['a'] == 1
    assert root.children['p'].children['a'].children['k'].children['e'].children['s'].remain_dict['p'] == 1
    assert root.children['p'].children['a'].children['k'].children['e'].children['s'].remain_dict['k'] == 0
    assert root.children['p'].children['a'].children['k'].children['e'].children['s'].remain_dict['E'] == 1


def test_parse_word():
    phrase_dict, phrase_len = utils.phrase_to_dict("poultry outwits ants")

    tree, words = LetterBranch.parse_words(phrase_dict, "data/wordlist")
    # Exclude invalid words.
    assert ('z' in tree.children) == False
    tree.children['t'].children['a'].children['i'].children['l'].is_word == True

    for word in words:
        assert word.is_word == True

def test_returned_word():
    phrase_dict, phrase_len = utils.phrase_to_dict("apple of Edenmot kaes")
    root = LetterBranch(None, False, None, phrase_dict, {})

    remain_dict = phrase_dict

    ret = LetterBranch.append_word_to_letter_tree(root, "pale\n", remain_dict)
    assert ret != None # Check that word was added
    assert ret.is_word == True
    assert ret.letter == 'e'

    ret = LetterBranch.append_word_to_letter_tree(root, "pakes", remain_dict)
    assert ret != None
    assert ret.is_word == True
    assert ret.letter == 's'

    ret = LetterBranch.append_word_to_letter_tree(root, "tom\n", remain_dict)
    assert ret != None

    ret = LetterBranch.append_word_to_letter_tree(root, "applew", remain_dict) # Invalid word
    assert ret == None
