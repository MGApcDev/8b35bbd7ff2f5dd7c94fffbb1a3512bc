from main import *

def test_get_word_simple():
    tree = parse_words("poultry outwits ants", "data/wordlist")
    a_leaf = tree.children['a']

    assert a_leaf.is_word == True
    a_str = get_word(a_leaf)
    assert a_str == 'a'

def test_get_word_long():
    tree = parse_words("poultry outwits ants", "data/wordlist")
    tail_leaf = tree.children['t'].children['a'].children['i'].children['l']

    assert tail_leaf.is_word == True
    tail_str = get_word(tail_leaf)
    assert tail_str == 'tail'
