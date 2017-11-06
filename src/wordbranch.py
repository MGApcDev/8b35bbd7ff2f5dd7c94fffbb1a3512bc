class WordBranch(object):
    """WordBranch represents a single branch in the tree of all the valid word combinations.

    Attributes:
        letter_branch (LetterBranch)  The reference to the LetterBranch that represents the word.
        origin        (WordBranch)    The reference to the parent WordBranch.
        children      ([WordBranch])  Array of children WordBranches.
        remain_char   (int)           Number of characters remaining in the remain_dict.
    """
    def __init__(self,  letter_branch, origin, children, remain_char, references, valid_children):
        self.letter_branch = letter_branch
        self.origin = origin
        self.children = children
        self.remain_char = remain_char
        self.references = references
        self.valid_children = valid_children

    def __str__(self):
        '''Trace words from leaf branch to root.
        Args
            self (WordBranch) The leaf branch to trace for word.
        Returns
            (string) The full string of represented by the leaf.
        '''
        output_str = ''
        words = []
        pointer = self
        while pointer.origin != None:
            words.append(pointer)
            pointer = pointer.origin

        words.reverse() # Put words in the right order
        for word in words:
            output_str += str(word.letter_branch) + ' '

        # Remove last char --> ' '
        return output_str[:-1]

    hash_to_branch = {}
    def get_word_tree_root(phrase_len, phrase_dict, words):
        '''Construct the root object of the WordBranch tree.
        Args
            phrase_len  (int)            Count of valid characters in phrase.
            phrase_dict ({char => int})  The remaining letters of the phrase.
            words       ([LetterBranch]) Array of all the available words as LetterBranch.
        Returns
            (WordBranch) The root of WordBranch tree.
        '''
        global hash_to_branch
        hash_to_branch = {} # Reset hash to branch on new tree root

        root_children = []
        root = WordBranch(None, None, [], phrase_len, None, None)
        for word in words:
            root_children.append(WordBranch(word, root, [], phrase_len - len(str(word)), None, None))

        root.children = root_children
        return root

    def get_hash_to_branch():
        global hash_to_branch
        return hash_to_branch
