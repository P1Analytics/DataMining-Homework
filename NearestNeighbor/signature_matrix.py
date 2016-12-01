import io
import os
import hash
import time

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

        # initialization of hash function
        self.n_hash_functions = n
        self.hash_functions = {}
        for i in range(self.n_hash_functions):
            self.hash_functions[i] = hash.hashFamily(i)

        self.signature_matrix = {}      # key doc_id, value: signature for that doc_id
        self.document_set = []

        self.offset = 0
        #self.offset = self.read_existing_data()

    def get_signature(self, set_id, n_band, n_component):
        '''

        :param set_id:
        :param n_band:
        :param n_component:
        :return:
        '''
        return self.signature_matrix[set_id][n_band*n_component:(n_band+1)*n_component]

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

    def add_set(self, set_id, set_elements):
        print "CHARACTERISTIC_MATRIX :: add_set [ "+str(set_id)+" ]"
        self.document_set.append(set_id)
        for element in set_elements:
            try:
                self.elements[element]
            except KeyError:
                self.row.append(element)
                self.elements[element] = element

    def compute_h(self):
        print "\nCHARACTERISTIC_MATRIX :: compute_h"
        print "\tNumber hash functions:",self.n_hash_functions
        print "\tNumber element to hash:", len(self.row)-self.offset
        print "\tTotal Number Hashes:", (len(self.row)-self.offset)*self.n_hash_functions

        n_row = len(self.row)

        cnt = 0
        percent = 0
        t = (len(self.row)-self.offset)*self.n_hash_functions/100.

        start = time.time()
        for r in range(self.offset, n_row):
            self.random_row_permutation[self.row[r]] = []
        #for r in self.row:
        #    self.random_row_permutation[r] = []
        print "\tInitialization random permutation in:", time.time() - start, "seconds"


        start = time.time()
        i = self.offset     # start computing the hashes only for new element
        while i < n_row-3:
            cnt += 3*self.n_hash_functions
            if cnt >= t:
                percent+=1
                cnt = 0
                print "\t\t",percent,"% ..."

            h_i = 0
            while h_i < self.n_hash_functions-3:
                hash_0 = self.hash_functions[h_i]
                hash_1 = self.hash_functions[h_i+1]
                hash_2 = self.hash_functions[h_i+2]
                h_i += 3

                r = self.row[i]
                self.random_row_permutation[r].append(hash_0(str(r.encode("utf-8"))))
                self.random_row_permutation[r].append(hash_1(str(r.encode("utf-8"))))
                self.random_row_permutation[r].append(hash_2(str(r.encode("utf-8"))))

                r = self.row[i+1]
                self.random_row_permutation[r].append(hash_0(str(r.encode("utf-8"))))
                self.random_row_permutation[r].append(hash_1(str(r.encode("utf-8"))))
                self.random_row_permutation[r].append(hash_2(str(r.encode("utf-8"))))

                r = self.row[i+2]
                self.random_row_permutation[r].append(hash_0(str(r.encode("utf-8"))))
                self.random_row_permutation[r].append(hash_1(str(r.encode("utf-8"))))
                self.random_row_permutation[r].append(hash_2(str(r.encode("utf-8"))))

            while h_i < self.n_hash_functions:
                r = self.row[i]
                self.random_row_permutation[r].append(self.hash_functions[h_i](str(r.encode("utf-8"))))
                r = self.row[i + 1]
                self.random_row_permutation[r].append(self.hash_functions[h_i](str(r.encode("utf-8"))))
                r = self.row[i + 2]
                self.random_row_permutation[r].append(self.hash_functions[h_i](str(r.encode("utf-8"))))

                h_i += 1

            i+=3

        while i<n_row:
            r = self.row[i]
            for h_i in range(self.n_hash_functions):
                self.random_row_permutation[r].append(self.hash_functions[h_i](str(r.encode("utf-8"))))
            i+=1
        print "\tRandom permutation computed in:", time.time() - start, "seconds"
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

    def read_existing_data(self):
        print "READ EXISTING HASHES..."

        print "\tread shingles..."
        start = time.time()
        shingles_file_path = os.path.dirname(os.path.abspath(__file__)) + "/data/shingles.tsv"
        try:
            shingles_file = io.FileIO(shingles_file_path, "r")
            for line in shingles_file.readlines():
                shingle = line[:-1].decode("utf8")
                self.elements[shingle] = shingle
                self.row.append(shingle)
                self.random_row_permutation[shingle]=[]
            shingles_file.close()
        except IOError:
            pass
        print "\t...Shingles read in",time.time()-start, "seconds"

        print "\tread shingle hashes of",len(self.row),"elements..."
        start = time.time()
        matrix_file_path = os.path.dirname(os.path.abspath(__file__)) + "/data/signature_matrix.tsv"
        try:
            matrix_signature_file = io.FileIO(matrix_file_path, "r")
            i = 0
            for line in matrix_signature_file.readlines():
                hashes = line[:-2].split("\t")
                for h in hashes:
                    self.random_row_permutation[self.row[i]].append(int("0x"+h, 0))
                i += 1
            matrix_signature_file.close()
        except IOError:
            pass
        print "\t...Hashes read in", time.time() - start, "seconds"

        print len(self.row),"element read form the disk"
        return len(self.row)

    def store(self):
        print "STORE NEW HASHES"
        matrix_file_path = os.path.dirname(os.path.abspath(__file__))+"/data/signature_matrix.tsv"
        matrix_signature_file = io.FileIO(matrix_file_path, "a")

        shingles_file_path = os.path.dirname(os.path.abspath(__file__)) + "/data/shingles.tsv"
        shingles_file = io.FileIO(shingles_file_path, "a")
        print "Storing",len(self.row)-self.offset,"new elements..."
        for i in range(self.offset, len(self.row)):
            line = ""
            shingle = self.row[i]
            for h in self.random_row_permutation[shingle]:
                line += str(hex(h))[2:]+"\t"
            matrix_signature_file.write(line+"\n")
            shingles_file.write(shingle.encode("utf8")+"\n")


        matrix_signature_file.flush()
        matrix_signature_file.close()
        shingles_file.flush()
        shingles_file.close()

