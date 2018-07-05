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

#rand = random.randint(1, 63)

rbpt = RandomBinaryProjectionTree('rbpt', 64, 3)

engine = Engine(DIM, lshashes=[rbpt], distance=CosineDistance())

with open(str(sys.argv[1])) as f:
	content = f.readlines()

content = [x.strip() for x in content]

rand_frame = None
rand_v1 = None
rand_v2 = None
rand_v3 = None

count = 0
for i in content:
	frame_name = str(i)[(str(i).index('\'') + 1) : str(i).index('\'', (str(i).index('\'') + 1))]	
	
	v1 = float(str(i)[(str(i).index('(') + 1) : str(i).index(',')])
	v2 = float(str(i)[(str(i).index(',') + 2) : str(i).index(',', (str(i).index(',') + 1))])
	v3 = float(str(i)[(str(i).index(',', (str(i).index(',') + 1)) + 2) : (str(i).index(')'))])
	cam = "Cam1"
	'''
	if (count == rand):
		rand_frame = frame_name
		rand_v1 = v1
		rand_v2 = v2
		rand_v3 = v3
	'''
	count += 1
	v = numpy.array([v1, v2, v3])
	new_id = re_id.Re_id(frame_name, cam, v)
	engine.store_vector(v, new_id)
	
	
start = time.time()

rand_v1 = 213.2353275841418 
rand_v2 = 218.21493592046951 
rand_v3 = 0.09112867808519982

rand_v = numpy.array([rand_v1, rand_v2, rand_v3])
rand_id = re_id.Re_id(rand_frame, "blue2", rand_v)
print("Query feature vector: " + str(rand_v))

'''
rand1 = random.random()
rand2 = random.random()
rand_v2 = None

rand_type = random.randint(1, 10)
if (rand_type < 3):
	rand_v2 = rand_v[0:3] + rand1 + rand2
elif (rand_type >= 3 and rand_type < 5):
	rand_v2 = rand_v[0:3] - rand1 - rand2
elif (rand_type >= 5 and rand_type < 8):
	rand_v2 = rand_v[0:3] - rand1 + rand2
elif (rand_type >= 8):
	rand_v2 = rand_v[0:3] + rand1 - rand2
'''

# print("Randomly modified fv to query: " + str(rand_v2))

results = engine.neighbours(rand_v)		

end = time.time()

data = results[0][1]
dist = results[0][2]

print("======================")
print("Data: " + str(data.frame_name) + ", " + str(data.camera_name) + ", " + str(data.id_time) + ", " + str(data.bucket_key))
print("Distance: " + str(dist))		
print(str(data.feature_vector))
print('Time to find: ' + str(end - start))



