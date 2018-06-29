import time
import numpy
import scipy
import nearpy.utils.utils
import re_id
from nearpy import Engine
from nearpy.distances import CosineDistance
from nearpy.hashes import RandomBinaryProjectionTree
import kdtree

def print_results(results):
	print('  Data \t| Distance')
	for r in results:
		data = r[1]
		dist = r[2]	
		print('  {} \t| {:.4f}'.format(data, dist))	

DIM = 16

POINTS = 10000 

rbpt = RandomBinaryProjectionTree('rbpt', 64, 3)

engine = Engine(DIM, lshashes=[rbpt], distance=CosineDistance())

v_list = []

matrix = numpy.zeros((POINTS, DIM))
for i in xrange(POINTS):
	v = numpy.random.randn(DIM)
	cam = "Cam"
	frame = "Cam1_" + str(i)
	new_id = re_id.Re_id(frame, cam, v)
	matrix[i, :] = nearpy.utils.utils.unitvec(v)
	engine.store_vector(v, new_id)
			
	v_list.append(v)
	
start = time.time()

query = numpy.random.randn(DIM)

results = engine.neighbours(query)		

end = time.time()

# print_results(results)
data = results[0][1]
dist = results[0][2]

print("Data: " + str(data.frame_name) + ", " + str(data.camera_name) + ", " + str(data.id_time) + ", " + str(data.bucket_key))
print("Distance: " + str(dist))		

print('Time to find: ' + str(end - start))
