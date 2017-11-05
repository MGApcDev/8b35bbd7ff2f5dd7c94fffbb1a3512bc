import utils

class LetterBranch(object):
    """LetterBranch represents a single branch in the tree of all the words in the loaded dictionary.

    Attributes:
        letter      (string)                 The letter for the place in the tree.
        is_word     (bool)                   Whether there is a word ending in the LetterBranch object.
        origin      (LetterBranch)           The reference to the parent LetterBranch.
        remain_dict ({char => int})          The remaining letters of the phrase from this point in the tree.
        children    ({char => LetterBranch}) Dictionary of characters to children LetterBranches.
    """
    def __init__(self,  letter, is_word, origin, remain_dict, children):
        self.letter = letter
        self.is_word = is_word
        self.origin = origin
        self.remain_dict = remain_dict
        self.children = children

    def __str__(self):
        '''Trace word from leaf branch to root.
        Args
            self (LetterBranch) The leaf branch to trace for word.
        Returns
            (string) The full string of represented by the leaf.
        '''
        word_str = ''
        pointer = self
        while pointer != None:
            if pointer.letter == None:
                break
            word_str += pointer.letter
            pointer = pointer.origin

        return word_str[::-1] # Flip string

    # Global letter tree root to use.
    letter_tree = None

    def set_letter_tree(letter_branch):
        global letter_tree
        letter_tree = letter_branch

    def get_letter_tree():
        global letter_tree
        return letter_tree

    def parse_words(phrase_dict, filename):
        '''Parse file to abstract syntax tree.
        Args
            phrase   (string) The phrase to look for anagrams.
            filename (string) The filename of the list of available words.
        Returns
            (LetterBranch)   The root of the abstract syntax tree.
            ([LetterBranch]) An array of word leafs representing the words available.
        '''
        words = []
        root = LetterBranch(None, False, None, phrase_dict, {})

        for line in open(filename):
            word_ref = LetterBranch.append_word_to_letter_tree(root, line, phrase_dict)
            if word_ref != None:
                words.append(word_ref)

        return root, words

    def append_word_to_letter_tree(root, word, remain_dict_ref):
        '''Append word to abstract syntax tree.
        Args
            root            (LetterBranch)       The root of the syntax tree.
            word            (string)             The word to add.
            remain_dict_ref ({char => int})      The dictionary of the remaining available characters.
        Returns
            (LetterBranch) Return the leaf branch of the word if word was added otherwise return None.
        '''
        remain_dict = dict(remain_dict_ref) # Make copy of dictionary without reference
        pointer = root
        last_char = None

        valid_word = True
        # Check the word matches the remaining characters.
        for char in word:
            if utils.invalid_char(char): # Ignore newlines
                continue

            if not(char in remain_dict):
                valid_word = False
                break
            if remain_dict[char] <= 0:
                valid_word = False
                break
            remain_dict[char] -= 1

        if not(valid_word):
            return None

        # Append valid word to tree.
        for char in word:
            if utils.invalid_char(char): # Ignore newlines
                continue
            last_char = char

            if not(char in pointer.children):
                pointer.children[char] = LetterBranch(char, False, pointer, {}, {})
            pointer = pointer.children[char]

        if pointer.is_word: # Word previously added
            return None
        pointer.is_word = True
        pointer.remain_dict = remain_dict

        return pointer
