'''Imports'''
import sys

'''Classes'''
class LetterBranch(object):
    """LetterBranch represents a single branch in the tree of all the words in the loaded dictionary.

    Attributes:
        letter      string             The letter for the place in the tree
        is_word     bool               Whether there is a word ending in the LetterBranch object
        origin      LetterBranch       The reference to the parent LetterBranch
        remain_dict Object.<char, int> The remaining letters of the phrase from this point in the tree
        used_dict   Object.<char, int> The used letters of the phrase for getting to this point in the tree
    """
    def __init__(self,  letter, is_word, origin, remain_dict, used_dict):
        self.letter = letter
        self.is_word = is_word
        self.origin = origin
        self.remain_dict = remain_dict
        self.used_dict = used_dict

class WordBranch(object):
    """WordBranch represents a single branch in the tree of all the valid word combinations.

    Attributes:
        letter_branch   LetterBranch       The reference to the LetterBranch that represents the word
        cur_remain_dict Object.<char, int> The remaining letters of the phrase from this point in the tree
    """
    def __init__(self,  letter_branch, cur_remain_dict):
        self.letter_branch = letter_branch
        self.cur_remain_dict = cur_remain_dict

'''Functions'''
def phrase_to_dict(phrase):
    pass

def parse_words(phrase, filename):
    phrase_dict = phrase_to_dict(phrase)
    pass

def append_to_solutions(branch_obj):
    pass

def construct_tree(phrase, valid_words):
    pass

def find_solutions(candidates):
    pass

def output(solutions):
    pass

'''Run'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        phrase = args[0]
        wordlist_filename = args[1]

        valid_words = parse_words(phrase, wordlist_filename)
        candidates = construct_tree(phrase, valid_words)

        solutions = find_solutions(candidates)
        output(solutions)
    else:
        print('Invalid arguments, expecting: "<string>" filename')
