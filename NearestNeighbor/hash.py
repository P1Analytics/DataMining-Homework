import hashlib

def hashFamily(i=0):
    '''
    Implement a family of hash functions. It hashes strings and takes an # integer to define the member of the family.
    Return a hash function parametrized by i
    :param i:
    :return:
    '''
    resultSize = 8      # how many bytes we want back
    maxLen = 20         # how long can our i be (in decimal)
    salt = str(i).zfill(maxLen)[-maxLen:]
    def hashMember(x):
        return hashlib.sha1(x + salt).digest()[-resultSize:]
    return hashMember