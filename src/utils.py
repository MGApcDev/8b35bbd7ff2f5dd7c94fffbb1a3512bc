def invalid_char(char):
    '''Check if character is invalid in a word.
    Args
        char (string) The character to check.
    Returns
        (bool) The True if char should be ignored otherwise return False.
    '''
    if char == '\n' or char == ' ':
        return True

    return False

def phrase_to_dict(phrase):
    '''Convert string phrase to dictionary <char, int>, mapping letters to a count of them found in a given phrase.
    Args
        phrase (string) The string phrase to convert.
    Returns
        ({char => int}) Returns a dictionary of characters and a count of their appearances in the phrase.
        (int)           Returns the length of the phrase, not including invalid characters like spaces.
    '''
    phrase_dict = {}
    phrase_len = 0
    for char in phrase:
        if invalid_char(char): # ignore spaces
            continue
        if char in phrase_dict:
            phrase_dict[char] += 1
            phrase_len += 1
        else:
            phrase_dict[char] = 1
            phrase_len += 1

    return phrase_dict, phrase_len

def dict_to_str(remain_dict):
    '''Parse a dictionary to string representation, e.g. {p:1, f:0, t:3} => pttt.
       Note: Ordering the string doesn't matter.
    Args
        remain_dict ({char => int}) The remaining characters in dictionary.
    Returns
        (string) The string representation.
    '''
    dict_str = ""
    for key, value in remain_dict.items():
        for value in range(value):
            dict_str += key

    # return ''.join(sorted(dict_str))
    return dict_str
