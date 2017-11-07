import hashlib

class HashProp(object):
    """Hash object to keep information of the hashes to find.
    Attributes:
        hash_algo (string)           The hash algorithm to hash with.
        hashes    ({string => bool}) The hashes and their state of if they were found.
    """
    def __init__(self,  hash_algo, hash_filename):
        self.algo = hash_algo.lower() # Lowercase algorithm
        self.hashes, self.count = self.parse_hashes(hash_filename)

    def parse_hashes(self, hash_filename):
        hashes = {}
        hash_count = 0
        for line in open(hash_filename):
            line = line.rstrip()
            if len(line) == 0: # Skip empty lines
                continue
            if line in hashes: # Skip duplicate hashes
                continue
            hashes[line] = False
            hash_count += 1

        return hashes, hash_count

    def valid_candidate(candidate):
        hash_obj = HashProp.get_hash_obj()

        local_hash = HashProp.get_hash_str(candidate)
        if (local_hash in hash_obj.hashes):
            hash_obj.hashes[local_hash] = True
            hash_obj.count -= 1
            return True

        return False

    def get_hash_str(input_str):
        hash_obj = HashProp.get_hash_obj()

        if hash_obj.algo == "md5":
            return (hashlib.md5(input_str.encode())).hexdigest()
        elif hash_obj.algo == "sha1":
            return None
        elif hash_obj.algo == "sha256":
            return None
        elif hash_obj.algo == "sha512":
            return None
        elif hash_obj.algo == "plain":
            return input_str

        return None

    # Global hash object to use.
    hash_obj = None

    def set_hash_obj(obj):
        global hash_obj
        hash_obj = obj

    def get_hash_obj():
        global hash_obj
        return hash_obj
