# import the necessary packages
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--display", default="False",
	help="display image or not")
# ap.add_argument("-d", "--detector", required=True,
# 	help="path to OpenCV's deep learning face detector")
# ap.add_argument("-m", "--embedding-model", required=True,
# 	help="path to OpenCV's deep learning face embedding model")
# ap.add_argument("-r", "--recognizer", required=True,
# 	help="path to model trained to recognize faces")
# ap.add_argument("-l", "--le", required=True,
# 	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = 'face_detection_model/deploy.prototxt'
modelPath = 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel'
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
 
# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')
 
# load the actual face recognition model along with the label encoder
recognizer = pickle.load(open("output/recognizer.pickle","rb"))
le = pickle.load(open('output/le.pickle','rb'))

# load the image, resize it to have a width of 600 pixels (while
# maintaining the aspect ratio), and then grab the image dimensions
def detect_fromimage(img):
	names = list()
	probs = list()
	faces = []

	image = cv2.imread(img)
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]
	
	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(image, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)
	
	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]
	
		# filter out weak detections
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for the
			# face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
	
			# extract the face ROI
			face = image[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]
	
			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue

			# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
				(0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()
	
			# perform classification to recognize the face
			preds = recognizer.predict_proba(vec)[0]
			j = np.argmax(preds)
			proba = preds[j]
			name = le.classes_[j]
			names.append(name)
			probs.append(proba)
			faces.append((startX, startY, endX, endY))

	return names, probs, faces

		# draw the bounding box of the face along with the associated
		# probability
if args["display"] == "True": 
	print("heyo")
	name,proba,faces  = detect_fromimage(args["image"])
	image = cv2.imread(args["image"])
	image = imutils.resize(image, width=600)
	for i in range(len(name)):
		text = "{}: {:.2f}%".format(name[i], proba[i] * 100)
		y = faces[i][1] - 10 if faces[i][1] - 10 > 10 else faces[i][1] + 10
		cv2.rectangle(image, (faces[i][0], faces[i][1]), (faces[i][2], faces[i][3]),
			(0, 0, 255), 2)
		cv2.putText(image, text, (faces[i][0], y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		
	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)