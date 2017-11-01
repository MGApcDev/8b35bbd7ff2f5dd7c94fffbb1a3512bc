from main import *

def test_get_word_simple():
    phrase_dict, phrase_len = phrase_to_dict("poultry outwits ants")

    tree, words = parse_words(phrase_dict, "data/wordlist")
    a_leaf = tree.children['a']

    assert a_leaf.is_word == True
    a_str = str(a_leaf)
    assert a_str == 'a'

def test_get_word_long():
    phrase_dict, phrase_len = phrase_to_dict("poultry outwits ants")

    tree, words = parse_words(phrase_dict, "data/wordlist")
    tail_leaf = tree.children['t'].children['a'].children['i'].children['l']

    assert tail_leaf.is_word == True
    tail_str = str(tail_leaf)
    assert tail_str == 'tail'


def test_returned_words():
    phrase_dict, phrase_len = phrase_to_dict("poultry outwits anpts delamgrovesa")
    tree, words = parse_words(phrase_dict, "data/sample")

    app_leaf = tree.children['a'].children['p'].children['p']
    assert app_leaf.is_word == True
    app_str = str(app_leaf)
    assert app_str == 'app'

    assert len(words) == 5
