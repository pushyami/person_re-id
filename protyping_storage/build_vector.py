from nearpy import Engine
from nearpy.filters import NearestFilter
from nearpy.distances import CosineDistance
from nearpy.hashes import RandomBinaryProjections
from nearpy.hashes import HashPermutations
from nearpy.hashes import HashPermutationMapper
from nearpy.storage import MemoryStorage
import numpy

dimension = 1000

permutations = HashPermutations('permut')

# Create binary hash as child hash
rbp_perm = RandomBinaryProjections('rbp_perm', 14)
rbp_conf = {'num_permutation':50,'beam_size':10,'num_neighbour':100}

# Add rbp as child hash of permutations hash
permutations.add_child_hash(rbp_perm, rbp_conf)

engine = Engine(dimension,
                lshashes=[permutations],
                distance=CosineDistance(),
                vector_filters=[NearestFilter(5)],
                storage = MemoryStorage())

i = 0

query = numpy.zeros(dimension)

f = open('features2.txt', 'r')
# Opening, reading from the file::
for next_read_line in f:
    next_read_line = next_read_line.rstrip()

    split_arr = next_read_line.split(" ")
    split_arr = split_arr[1:]
    split_arr = list(map(float, split_arr))

    vector = numpy.asarray(split_arr)
    
    if(i == 639):
        query = vector
   #     print (query)
    else:
        vec_data = numpy.append(vector, i)
        engine.store_vector(vector, tuple(vec_data))

    i += 1

permutations.build_permuted_index()

# Get nearest neighbors:
N = engine.neighbours(query)

# Number of nearest neighbors:
print(len(N))

print("Nearest Neighbors")

for x in N:
    #Printing the id of the vector here as needed:
    # print (x[1][dimension])
    print(x[1][dimension])
