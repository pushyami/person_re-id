import cv2
from matplotlib import pyplot as plt
import numpy as np
from scipy import spatial
import os

#this function cleans the directory 
#abit patchy so check the directory after running this function
#clean directory manunually if function fails
def cleanFile(file_path):
    file_list = os.listdir(first_path)
    
    for i in file_list:
        if len(i) > 6:
            try:
                os.remove(file_path + "/" + i)
            except:
                print("")

#resize and cuts the sides, top and bottom to reduce background
def cutStill(image_path,cut_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img,(100,150),cv2.INTER_AREA)
    crop_img = img[30:130, 30:75]
    cv2.imwrite(cut_path,crop_img)


#cut image to get just clothes(top) of person
def getTop(image_path,first_path):
    img = cv2.imread(image_path)
    w,h,c = img.shape
    mid_h = int(h/2)
    first_top = img[0:int(3*h/2),0:w]
    cv2.imwrite(first_path,first_top)
    
#calculate the different color values of RGB, HSV, YCRCB
#RGB not used in final code
def getHSV(image_path):    
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    
    (n_r, bins, patches) = plt.hist(np.ndarray.flatten(r), bins=16)
    
    
    (n_g, bins, patches) = plt.hist(np.ndarray.flatten(g), bins=16)
    
    (n_b, bins, patches) = plt.hist(np.ndarray.flatten(b), bins=16)
    
    hsv_image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hue, sat, val = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    (n_h, bins, patches) = plt.hist(np.ndarray.flatten(hue), bins=16)
    
    (n_s, bins, patches) = plt.hist(np.ndarray.flatten(sat), bins=16)
    
    (n_v, bins, patches) = plt.hist(np.ndarray.flatten(val), bins=16)
    
    imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    y, cr, cb = imgYCC[:,:,0], imgYCC[:,:,1], imgYCC[:,:,2]
    (n_y, bins, patches) = plt.hist(np.ndarray.flatten(y), bins=16)
    
    (n_cr, bins, patches) = plt.hist(np.ndarray.flatten(cr), bins=16)
    
    (n_cb, bins, patches) = plt.hist(np.ndarray.flatten(cb), bins=16)

    #final = n_r.tolist() + n_g.tolist() + n_b.tolist() + n_h.tolist() + n_s.tolist() + n_v.tolist() + n_y.tolist() + n_cr.tolist() + n_cb.tolist()
    final = n_h.tolist() + n_s.tolist() + n_v.tolist() + n_y.tolist() + n_cr.tolist() + n_cb.tolist()
  
    return final

#calculates cosine similarity between two feature vectors
def getCosineSimilarity(first,second):
    result = 1 - spatial.distance.cosine(first, second)
    return result


#-----GET COLOR VECTOR-----#

#get color vector of 1 * 96 
def getColorFeature(image_path):

    if(image_path[-3:] != "png"):
        return
    
    base = image_path
    img_p = base
    base = base[:-4]
    cut_img_p = base + "cut.png"
    top_first = base + "top1.png"
    cutStill(img_p,cut_img_p)
    getTop(cut_img_p,top_first)
    first = getHSV(top_first)
    
    return first

#INPUT - PATH TO IMAGE FILE
#OUTPUT - FEATURE VECTOR
result = getColorFeature("72/1.png")
print (len(result))

#----- ----- ----- ----- -----#
'''
The following are the examples of how to use the functions
'''


#EXAMPLE 1 - Compare two images
'''
base = "77/1"
img_p = base + ".png"
cut_img_p = base + "cut.png"
top_first = base + "top1.png"
cutStill(img_p,cut_img_p)
getTop(cut_img_p,top_first)
first = getHSV(top_first)

base = "77/5"
img_p = base + ".png"
cut_img_p = base + "cut.png"
top_first = base + "top1.png"
cutStill(img_p,cut_img_p)
getTop(cut_img_p,top_first)
second = getHSV(top_first)

print (getCosineSimilarity(first,second))

'''

#Example 2 - Get average cosine similarity of same identity
'''
first_path = "74"
first_file = os.listdir(first_path)

acc = 0;
count = 0;

feature_vectors = []

for i in range(len(first_file)):
    if(first_file[i][-3:] != "png"):
        continue
    
    base = first_path + "/" + first_file[i]
    base = base[:-4]
    img_p = base + ".png"
    cut_img_p = base + "cut.png"
    top_first = base + "top1.png"
    cutStill(img_p,cut_img_p)
    getTop(cut_img_p,top_first)
    first = getHSV(top_first)
    feature_vectors.append(first)
    
for i in range(len(feature_vectors)):
    
    first = feature_vectors[i]
    
    for j in range(i + 1,len(feature_vectors)):
        second = feature_vectors[j]
        acc += getCosineSimilarity(first,second)
        count += 1
        
print (acc/count)
'''


#Example 3 - Get average cosine similarity of different identities
'''           
first_path = "79"
cleanFile(first_path)
first_file = os.listdir(first_path)

feature_vectors_first = []

for i in range(len(first_file)):
    if(first_file[i][-3:] != "png"):
        continue
    
    base = first_path + "/" + first_file[i]
    base = base[:-4]
    img_p = base + ".png"
    cut_img_p = base + "cut.png"
    top_first = base + "top1.png"
    cutStill(img_p,cut_img_p)
    getTop(cut_img_p,top_first)
    first = getHSV(top_first)
    feature_vectors_first.append(first)

cleanFile(first_path)
    
second_path = "80"
cleanFile(second_path)
second_file = os.listdir(second_path)

feature_vectors_second = []

for i in range(len(second_file)):
    if(second_file[i][-3:] != "png"):
        continue
    
    base = second_path + "/" + second_file[i]
    base = base[:-4]
    img_p = base + ".png"
    cut_img_p = base + "cut.png"
    top_first = base + "top1.png"
    cutStill(img_p,cut_img_p)
    getTop(cut_img_p,top_first)
    first = getHSV(top_first)
    feature_vectors_second.append(first)    

cleanFile(second_path)
    
acc = 0;
count = 0;

for i in range(len(feature_vectors_first)):
    first = feature_vectors_first[i];
    for i in range(len(feature_vectors_second)):
        second = feature_vectors_second[i];
        acc += getCosineSimilarity(first,second)
        count += 1

print (acc/count)


cleanFile("79")
'''
