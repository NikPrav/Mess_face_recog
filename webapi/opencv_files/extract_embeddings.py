# Extracting the facial features from a picture, then preprocessing the image
# by cropping and rotating the place with the images. THen, it uses a deep learning
# feature extractor to generate the 128-D vector describing the face

# Importing the necessary stuff

import imutils
import numpy as np
import argparse
import cv2
import os
from imutils import paths
import pickle


# Argument parser which takes in the location of the dataset, the output folder, the detector
# , the caffe model, and the percentage of confidence required as cl arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--dataset", required=True,
# 	help="path to input directory of faces + images")
# ap.add_argument("-e", "--embeddings", required=True,
# 	help="path to output serialized db of facial embeddings")
# ap.add_argument("-d", "--detector", required=True,
# 	help="path to OpenCV's deep learning face detector")
# ap.add_argument("-m", "--embedding-model", required=True,
# 	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


# Loading the face detector
# Caffe based deep-learning face detector to localise faces in image
print("[INFO] Face detector initialising")
path_toprototxt = 'face_detection_model/deploy.prototxt'
path_tomodel = '/home/nik/Documents/lambda/face_detection/babi_steps/opencv_mine/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel'
# path_toprototxt = os.path.sep.join([args["detector"], "deploy.prototxt"])
detector = cv2.dnn.readNetFromCaffe(path_toprototxt,path_tomodel)

# Loading the model to recognise the face embeds
# Torch-based detector that extracts facial embeddings
print("[INFO] Face recogniser initialising")
embeder = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')

# Declaring input image path
path_toimages = list(paths.list_images("dataset"))

# Initialising the embeddings array
known_Embeddings = []
known_names = []
total = 0

# Loading images
for (i,path_toimage) in enumerate(path_toimages):
    # Getting the name 
    print(f'[INFO] processing image{i + 1}/{len(path_toimages)} ')

    # splitting ar the path sep(varies form os, so we use os.path.sep)
    name = path_toimage.split(os.path.sep)[-2]

    # Reading the images and resizing them to width 600 px
    image = cv2.imread(path_toimage)
    image = imutils.resize(image, width=600)
    (h,w) = image.shape[:2]

    # Constructing a blob from image
    # Does preprocessing
    # like mean subtraction, scaling, channel swapping etc.
    # here, we are doing mean subtraction on the image
    imageBlob = cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),1.0,(300,300),(104.0,177.0,123.0),swapRB=False,crop=False)

    # Now localising the faces using opencv's face detector

    detector.setInput(imageBlob)
    detections = detector.forward()

    # Looping through detections
    if(len(detections)>0):
        # Assuming only one face per image
        # Taking the bounding box with the largest probability
        i = np.argmax(detections[0,0,:,2])
        confidence = detections[0,0,i,2]

        if confidence > args["confidence"]:
            # getting the (x,y) coordinates of the bounding box
            box = detections[0,0,i,3:7]*np.array([w,h,w,h])
            (startX,startY,endX,endY) = box.astype("int")

            # extracting the face ROI and grabbing its dimensions
            face = image[startX:endY,startX:endX]
            (fH,fW) = face.shape[:2]

            # threshold for face width and height
            if fW < 20 or fH <20:
                continue

            # contructing the blob, and passing the blob through the embeder
            # to get 128-d quantification of the face

            faceBlob = cv2.dnn.blobFromImage(face,1.0/255,(96,96),(0,0,0),swapRB=True, crop = False)
            embeder.setInput(faceBlob)
            vec = embeder.forward()

            # appending the name to the face    
            known_names.append(name)
            known_Embeddings.append(vec.flatten())
            total += 1


print(f"[INFO] serializing {total} encodings")
data = {"embeddings":known_Embeddings,"names":known_names}
# dumping the data object onto a pickle file
# Stores the facial embeding data
f = open("output/embeddings.pickle","wb")
f.write(pickle.dumps(data))
f.close()






    
    

