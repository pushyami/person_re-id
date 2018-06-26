import time
import numpy
import scipy
import nearpy.utils.utils
import re_id
from nearpy import Engine
from nearpy.distances import CosineDistance
from nearpy.hashes import RandomBinaryProjectionTree

def print_results(results):
	print('	 Data \t| Distance')
	for r in results:
		data = r[1]
		print("Data: " + str(data.frame_name) + ", " + str(data.camera_name) + ", " + str(data.id_time))
		print("\t" + str(data.bucket_key))
		dist = r[2]
		print("Distance: " + str(dist))

DIM = 16

POINTS = 100 

rbpt = RandomBinaryProjectionTree('rbpt', 8, 3)

engine = Engine(DIM, lshashes=[rbpt], distance=CosineDistance())

matrix = numpy.zeros((POINTS, DIM))
for i in xrange(POINTS):
	v = numpy.random.randn(DIM)
	cam = "Cam1"
	frame = "Cam1_20"
	new_id = re_id.Re_id(frame, cam, v)
	matrix[i, :] = nearpy.utils.utils.unitvec(v)
	engine.store_vector(v, new_id)

print('Buckets = %d' % len(engine.storage.buckets['rbpt'].keys()))

query = numpy.random.randn(DIM)

start = time.time()

results = engine.neighbours(query)

end = time.time()

# print_results(results)
data = results[0][1]
dist = results[0][2]

print("Data: " + str(data.frame_name) + ", " + str(data.camera_name) + ", " + str(data.id_time) + ", " + str(data.bucket_key))
print("Distance: " + str(dist))		

print('Time to find: ' + str(end - start))
