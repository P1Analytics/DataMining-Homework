import hash

'''
 2. Implement a class, that given a collection of sets of objects (e.g., strings, or numbers), creates a minwise hashing based signature for each set.
'''

class SignatureMatrix(object):
    def __init__(self, n):
        self.row = []
        self.random_row_permutation = {}
        self.n_hash_functions = n
        self.signature_matrix = {}      # key doc_id, value: signature for that doc_id
        self.document_set = []

    def add_sets(self, sets):
        print "\nCHARACTERISTIC_MATRIX :: add_sets "
        for set_id, set_elements in sets.iteritems():
            self.add_set(set_id, set_elements)
        print "\n\n\tNumber of different elements:", len(self.row)
        print "CHARACTERISTIC_MATRIX :: add_sets --> DONE"

    def add_set(self, document_id, set_elements):
        print "\nCHARACTERISTIC_MATRIX :: add_set [ "+document_id+" ]"
        self.document_set.append(document_id)
        for element in set_elements:
            if element not in self.row:
                self.row.append(element)

    def compute_h(self):
        print "\nCHARACTERISTIC_MATRIX :: compute_h"
        print "\tNumber hash functions:",self.n_hash_functions
        print "\tNumber element to hash:", len(self.row)
        cnt = 0
        percent = 0
        for r in self.row:
            if cnt > len(self.row)/10.:
                percent+=10
                cnt = 0
                print "\t\t",percent,"% ..."
            self.random_row_permutation[r] = []
            for i in range(self.n_hash_functions):
                h = hash.hashFamily(i)
                self.random_row_permutation[r].append(h(str(r.encode("utf-8"))))
            cnt+=1
        print "CHARACTERISTIC_MATRIX :: compute_h --> DONE"

    def create_signature_matrix(self, document_shingles_diz):
        '''

        :param n_row:
        :param n_columns:
        :return:
        '''

        self.compute_h()    # compute hash for every element of the set

        print "\nCHARACTERISTIC_MATRIX :: create_signature_matrix"
        for document_id, shingles in document_shingles_diz.iteritems():
            print "\tElaborating document:",document_id
            self.signature_matrix[document_id] = [None for x in range(self.n_hash_functions)]
            for r in self.row:
                if r in shingles:
                    for i in range(self.n_hash_functions):
                        h_i = self.random_row_permutation[r][i]
                        if self.signature_matrix[document_id][i] is None or self.signature_matrix[document_id][i]>h_i:
                            self.signature_matrix[document_id][i] = h_i

        print "CHARACTERISTIC_MATRIX :: DONE"

    def print_signatures(self):
        for document_id, signature in self.signature_matrix.iteritems():
            print "\nSignature for document:",document_id
            for i in range(self.n_hash_functions):
                print "\t",i,signature[i], self.decode(i, signature[i])

    def decode(self, i, signature):
        for r in self.row:
            if self.random_row_permutation[r][i] == signature:
                return r