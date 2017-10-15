'''Imports'''
import sys

class Branch(object):
    """docstring for Branch."""
    def __init__(self, arg):
        super(Branch, self).__init__()
        self.arg = arg

def count_phrase(phrase):
    pass

def parse_words(phrase, filename):
    phrase_dict = count_phrase(phrase)

def append_to_solutions(branch_obj):
    pass

def construct_tree(phrase, valid_words):
    pass

def find_solutions(candidates):
    pass

def output(solutions):
    pass

'''RUN CODE'''
if __name__ == "__main__":
    args = sys.argv
    phrase = args[0]
    wordlist_filename = args[1]

    valid_words = parse_words(phrase, wordlist_filename)
    candidates = construct_tree(phrase, valid_words)

    solutions = find_solutions(candidates)
    output(solutions)
