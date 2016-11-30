import hashlib
import struct

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
        '''
        Return an integer number of 64bit length, that is the hash of the shingle
        The hash function used is always the same!
        :param x:
        :return:
        '''
        return struct.unpack("Q", hashlib.sha1(x + salt).digest()[-resultSize:])[0]

    return hashMember