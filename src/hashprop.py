class HashProp(object):
    """Hash object to keep information of the hashes to find.
    Attributes:
        hash_algo (string)           The hash algorithm to hash with.
        hashes    ({string => bool}) The hashes and their state of if they were found.
    """
    def __init__(self,  hash_algo, hash_filename):
        self.algo = hash_algo.lower() # Lowercase algorithm
        self.hashes = self.parse_hashes(hash_filename)

    def parse_hashes(self, hash_filename):
        hashes = {}
        for line in open(hash_filename):
            hashes[line[:-1]] = True

        print(hashes)

        return hashes

    # Global hash object to use.
    hash_obj = None

    def set_hash_obj(obj):
        global hash_obj
        hash_obj = obj

    def get_hash_obj():
        global hash_obj
        return hash_obj
