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
