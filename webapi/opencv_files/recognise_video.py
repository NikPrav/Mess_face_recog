# Recognising faces from video
# Importing necessary stuff
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os

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

# Loading the face recognition module from disk
# along with the label encoder
print("[INFO] Face recogniser initialising" )
recogniser = pickle.load(open("output/recognizer.pickle","rb"))
le = pickle.load(open('output/le.pickle','rb'))

# Starting video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Starting the fps estimatior
fps = FPS().start()
# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
    frame = vs.read()
	# resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]
	# Constructing a blob from image
    # Does preprocessing
    # like mean subtraction, scaling, channel swapping etc.
    # here, we are doing mean subtraction on the image
    imageBlob = cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),1.0,(300,300),(104.0,177.0,123.0),swapRB=False,crop=False)

    # Now localising the faces using opencv's face detector

    detector.setInput(imageBlob)
    detections = detector.forward()

    # Looping through detections
    for i in range(detections.shape[2]):
        # i = np.argmax(detections[0,0,:,2])
        # extracting confidence associated with the prediction
        confidence = detections[0,0,i,2]

        if confidence > 0.5:
            # getting the (x,y) coordinates of the bounding box
            box = detections[0,0,i,3:7]*np.array([w,h,w,h])
            (startX,startY,endX,endY) = box.astype("int")

            # extracting the face ROI and grabbing its dimensions
            face = frame[startX:endY,startX:endX]
            (fH,fW) = face.shape[:2]

            # threshold for face width and height
            if fW < 20 or fH <20:
                continue
            
            # contructing the blob, and passing the blob through the embeder
            # to get 128-d quantification of the face

            faceBlob = cv2.dnn.blobFromImage(face,1.0/255,(96,96),(0,0,0),swapRB=True, crop = False)
            embeder.setInput(faceBlob)
            vec = embeder.forward()

            # performing classification for face recognition
            preds = recogniser.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]

            # draw the bounding box of the face along with the
			# associated probability
            text = "{}: {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
            cv2.putText(frame, text, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    
    # updating FPS counter
    fps.update()

    # showing the output frame
    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()