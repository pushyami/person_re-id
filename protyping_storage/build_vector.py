from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.distances import CosineDistance
from nearpy.filters import NearestFilter
from nearpy.storage import MemoryStorage
import numpy
import time

dimension = 1024

rbp = RandomBinaryProjections('rbp', 10)

engine = Engine(dimension,
                lshashes=[rbp],
                distance=CosineDistance(),
                vector_filters=[NearestFilter(10)],
                storage = MemoryStorage())

i = 0

query = numpy.zeros(dimension)

f = open('input_vectors', 'r')
# Opening, reading from the file::
for next_read_line in f:
    next_read_line = next_read_line.rstrip()

    split_arr = next_read_line.split(",")
    split_arr = list(map(float, split_arr))

    vector = numpy.asarray(split_arr)
    
    if(i == 10):
        query = vector
    else:
        engine.store_vector(vector, tuple(vector))

    i += 1

# Get nearest neighbors:
N = engine.neighbours(query)

for x in N:
    print (x[1])
