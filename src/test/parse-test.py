from main import *

def test_phrase_to_dict_simple():
    phrase_dict = phrase_to_dict("abc")
    assert len(phrase_dict.keys()) == 3
    assert phrase_dict['a'] == 1
    assert phrase_dict['c'] == 1
    assert ("d" in phrase_dict) == False

def test_phrase_to_dict_repeat_and_multiple_words_and_distinct_case():
    phrase_dict = phrase_to_dict("apple of Eden")
    assert len(phrase_dict.keys()) == 9
    assert phrase_dict['a'] == 1
    assert phrase_dict['p'] == 2
    assert phrase_dict['e'] == 2
    assert phrase_dict['E'] == 1
    assert (" " in phrase_dict) == False # ignore spaces

def test_append_word_to_tree_single():
    phrase_dict = phrase_to_dict("apple of Eden")
    root = LetterBranch(None, False, None, phrase_dict, {})
    append_word_to_tree(root, "pale\n", phrase_dict)

    assert root.children['p'] != None
    assert root.children['p'].children['a'] != None
    assert root.children['p'].children['a'].children['l'] != None
    assert root.children['p'].children['a'].children['l'].children['e'] != None

def test_append_word_to_tree_multiple():
    phrase_dict = phrase_to_dict("apple of Edenmot kaes")
    root = LetterBranch(None, False, None, phrase_dict, {})

    remain_dict = phrase_dict

    ret = append_word_to_tree(root, "pale\n", remain_dict)
    assert ret == True # Check that word was added

    ret = append_word_to_tree(root, "pakes\n", remain_dict)
    assert ret == True

    ret = append_word_to_tree(root, "tom\n", remain_dict)
    assert ret == True

    ret = append_word_to_tree(root, "applew", remain_dict) # Invalid word
    assert ret == False

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
    tree = parse_words("poultry outwits ants", "data/wordlist")

    # Exclude invalid words.
    assert ('z' in tree.children) == False
    tree.children['t'].children['a'].children['i'].children['l'].is_word == True
