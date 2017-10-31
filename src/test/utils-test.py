from main import *

def test_dict_to_str():
    dict1 = {'p':1, 't':4, 'a':0, 'i':2}

    dict_str = dict_to_str(dict1)
    assert dict_str == "pttttii"
