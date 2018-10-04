from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.distances import CosineDistance
from nearpy.filters import NearestFilter
from nearpy.storage import MemoryStorage
import numpy

dimension = 1024

rbp = RandomBinaryProjections('rbp', 10)

engine = Engine(dimension,
                lshashes=[rbp],
                distance=CosineDistance(),
                vector_filters=[NearestFilter(10)],
                storage = MemoryStorage())

i = 0

query = numpy.zeros(dimension)

f = open('test.txt', 'r')
# Opening, reading from the file::
for next_read_line in f:
    next_read_line = next_read_line.rstrip()

    split_arr = next_read_line.split(" ")
    split_arr = list(map(float, split_arr))

    vector = numpy.asarray(split_arr)
    
    if(i == 10):
        query = vector
        print (query)
    else:
        vec_data = numpy.append(vector, i)
        engine.store_vector(vector, tuple(vec_data))

    i += 1

# Get nearest neighbors:
N = engine.neighbours(query)

# Number of nearest neighbors:
print(len(N))

for x in N:
    #Printing the id of the vector here as needed:
    print (x[1][dimension])
