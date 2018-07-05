import datetime
import numpy

class Re_id:
	frame_name = ""
	camera_name = ""
	id_time = None
	bucket_key = None	
	feature_vector = None

	def __init__(self, frame_name, camera_name, feature_vector):
		self.frame_name = frame_name
		self.camera_name = camera_name
		self.id_time = datetime.datetime.now()
		self.feature_vector = feature_vector

	def average_vectors(self, new_features):
		feature_vector = (np.array(feature_vector) + np.array(new_features)) / 2 

	def get_goldfish(self):
		#print ([self.feature_vector,[self.frame_name,self.camera_name,self.id_time]])
		return self.feature_vector.tolist(),[self.frame_name,self.camera_name,self.id_time]
