import time
import numpy
import scipy
import nearpy.utils.utils
import re_id
from nearpy import Engine
from nearpy.distances import CosineDistance
from nearpy.hashes import RandomBinaryProjectionTree
import kdtree

import kdtree

def print_results(results):
	print('  Data \t| Distance')
	for r in results:
		data = r[1]
<<<<<<< HEAD
		# print("Data: " + str(data.frame_name) + ", " + str(data.camera_name) + ", " + str(data.id_time))
		# print("\t" + str(data.bucket_key))
		dist = r[2]
		# print("Distance: " + str(dist))
		print('  {} \t| {:.4f}'.format(data, dist))
=======
		dist = r[2]	
		print('  {} \t| {:.4f}'.format(data, dist))	
>>>>>>> 5bbe9f7644b229c71935bf78f5e524a25e08ede0

DIM = 4096

<<<<<<< HEAD
POINTS = 200
=======
POINTS = 10000 
>>>>>>> 5bbe9f7644b229c71935bf78f5e524a25e08ede0

rbpt = RandomBinaryProjectionTree('rbpt', 64, 3)

engine = Engine(DIM, lshashes=[rbpt], distance=CosineDistance())

<<<<<<< HEAD
# matrix = numpy.zeros((POINTS, DIM))
vectors = []
vectors_k = []
for i in xrange(POINTS):
	cam = "Cam1"
	frame = "Cam1_20"
	v = numpy.random.randn(DIM)

	new_id = re_id.Re_id(frame, cam, v)
	vectors.append(new_id)

=======
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
>>>>>>> 5bbe9f7644b229c71935bf78f5e524a25e08ede0

	fff = [v.tolist(),[cam,frame]]
	vectors_k.append(fff)

<<<<<<< HEAD
start = time.time()
for i in vectors:
	# matrix[i, :] = nearpy.utils.utils.unitvec(v)
	engine.store_vector(i.feature_vector, i)
=======
results = engine.neighbours(query)		
>>>>>>> 5bbe9f7644b229c71935bf78f5e524a25e08ede0

end = time.time()

print('Total insert time: ' + str(end - start))

start1 = time.time()

tree = kdtree.create(vectors_k[0: len(vectors_k)/2])						
count = 0
for i in vectors_k[len(vectors_k)/2: ]:
	count = (count + 1)
	if(count % 10 == 0):
		if( not tree.is_balanced):
			#print("BOI is not balanced!")
			tree.rebalance()
	tree.add(i)

end1 = time.time()

print('Total insert time kd fug: ' + str(end1 - start1))
'''
# Testing accuracy now:
query = numpy.random.randn(DIM)
new_id_find = re_id.Re_id("Cam1, Cam1_21", query)
start2 = time.time()
results = engine.neighbours(new_id.feature_vector)
end2 = time.time()

#Printing nearest neighbors out for the lsh:
print(results)


#Nearest neighbors for the kd tree:
kdtree_results = tree.search_nn(query)


print(kdtree_results)
'''





# print('Buckets = %d' % len(engine.storage.buckets['rbpt'].keys()))

# query = numpy.random.randn(DIM)

# start = time.time()

# results = engine.neighbours(query)

#print_results(results)
#data = results[0][1]
#dist = results[0][2]

#print("Data: " + str(data.frame_name) + ", " + str(data.camera_name) + ", " + str(data.id_time) + ", " + str(data.bucket_key))
#print("Distance: " + str(dist))		


#print('Find time: ' + str(end2 - start2))
