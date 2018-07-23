import math
from math import sqrt
import random

from scipy import spatial

def getVector(featurevector):
	
	body = featurevector.split()

	result = []

	for i in body:
		result.append(float(i))

	return result


num1= open("first.txt","r")
num2= open("second.txt","r")

lines1 = num1.readlines()
lines2 = num2.readlines()



for i in range(len(lines1)):
	first = getVector(lines1[i])
	second = getVector(lines2[i])

	print (1 - spatial.distance.cosine(first, second))

