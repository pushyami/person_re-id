import time
import numpy
import scipy
import nearpy.utils.utils
import re_id
import random
import sys
from nearpy import Engine
from nearpy.distances import CosineDistance, EuclideanDistance
from nearpy.hashes import RandomBinaryProjectionTree
import kdtree

def print_results(results):
	print('  Data \t| Distance')
	for r in results:
		data = r[1]
		dist = r[2]	
		print('  {} \t| {:.4f}'.format(data, dist))	

DIM = int(sys.argv[2])

POINTS = int(sys.argv[3]) 

rand = random.randint(1, POINTS)

rbpt = RandomBinaryProjectionTree('rbpt', 64, 3)

engine = Engine(DIM, lshashes=[rbpt], distance=CosineDistance())

with open(str(sys.argv[1])) as f:
	content = f.readlines()
with open(str("test_nn.txt")) as f:
	content2 = f.readlines()
rand_frame = None
rand_v1 = None
rand_v2 = None
rand_v3 = None

count = 0
for i in content:
	fv = i.split()
	frame_name = str(count)
	count += 1
	v = numpy.array(fv)
	v_float = v.astype(numpy.float)
	new_id = re_id.Re_id(frame_name, "test", v)
	engine.store_vector(v_float, new_id)
	
	
start = time.time()

fv2 = content2[0].split()
v2 = numpy.array(fv2)
v2_float = v2.astype(numpy.float)

results = engine.neighbours(v2_float)

end = time.time()
data = results[0][1]
dist = results[0][2]

print("Data: " + str(data.frame_name) + ", " + str(data.camera_name) + ", " + str(data.id_time) + ", " + str(data.bucket_key))
print("Distance: " + str(dist))		
print(str(data.feature_vector))
print('Time to find: ' + str(end - start))

