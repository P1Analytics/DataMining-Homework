import hash

'''
 2. Implement a class, that given a collection of sets of objects (e.g., strings, or numbers), creates a minwise hashing based signature for each set.
'''

class SignatureMatrix(object):
    def __init__(self, n):
        '''
        n is the length of the signatre (number of hash functions)
        :param n:
        '''
        self.elements = {}
        self.row = []

        self.random_row_permutation = {}
        self.n_hash_functions = n

        self.signature_matrix = {}      # key doc_id, value: signature for that doc_id
        self.document_set = []


    def add_sets(self, sets):
        print "\nCHARACTERISTIC_MATRIX :: add_sets "
        cnt = 0
        percent = 0
        for set_id, set_elements in sets.iteritems():
            cnt+=1
            if cnt >= len(sets)/100.:
                print "\t\t", percent, "% ..."
                percent+=1
                cnt = 0
            self.add_set(set_id, set_elements)
        print "\n\n\tNumber of different elements:", len(self.row)
        print "CHARACTERISTIC_MATRIX :: add_sets --> DONE"

    def add_set(self, document_id, set_elements):
        print "CHARACTERISTIC_MATRIX :: add_set [ "+str(document_id)+" ]"
        self.document_set.append(document_id)
        for element in set_elements:
            try:
                self.elements[element]
            except KeyError:
                self.row.append(element)
                self.elements[element] = element

    def compute_h(self):
        print "\nCHARACTERISTIC_MATRIX :: compute_h"
        print "\tNumber hash functions:",self.n_hash_functions
        print "\tNumber element to hash:", len(self.row)
        print "\tTotal Number Hashes:", len(self.row)*self.n_hash_functions
        cnt = 0
        percent = 0
        t = len(self.row)*self.n_hash_functions/100.
        for i in range(self.n_hash_functions):
            h = hash.hashFamily(i)
            for r in self.row:
                cnt += 1
                if cnt >= t:
                    percent+=1
                    cnt = 0
                    print "\t\t",percent,"% ..."
                try:
                    self.random_row_permutation[r].append(h(str(r.encode("utf-8"))))
                except Exception:
                    self.random_row_permutation[r] = []
                    self.random_row_permutation[r].append(h(str(r.encode("utf-8"))))
        print "CHARACTERISTIC_MATRIX :: compute_h --> DONE"

    def create_signature_matrix(self, document_shingles_diz):
        '''

        :param n_row:
        :param n_columns:
        :return:
        '''

        self.compute_h()    # compute hash for every element of the set

        print "\nCHARACTERISTIC_MATRIX :: create_signature_matrix"
        cnt = 0
        percent = 0
        for document_id, shingles in document_shingles_diz.iteritems():
            cnt += 1
            if cnt >= len(document_shingles_diz) / 100.:
                percent += 1
                cnt = 0
                print "\t\t", percent, "% ..."
            print "\tElaborating document:",document_id
            self.signature_matrix[document_id] = [None for x in range(self.n_hash_functions)]
            for i in range(self.n_hash_functions):
                for r in shingles:
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