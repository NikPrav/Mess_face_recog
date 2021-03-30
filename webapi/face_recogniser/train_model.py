# Linear Support Vector Machine model is trained using the embeddings
# in this code
# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

ap = argparse.ArgumentParser()
# ap.add_argument("-e", "--embeddings", required=True,
# 	help="path to serialized db of facial embeddings")
# ap.add_argument("-r", "--recognizer", required=True,
# 	help="path to output model trained to recognize faces")
# ap.add_argument("-l", "--le", required=True,
# 	help="path to output label encoder")
args = vars(ap.parse_args())

# Loading the embeddings
print('[INFO] Loading the face embeddings ...')
data = pickle.load(open("output/embeddings.pickle",'rb'))

# Encoding the labels
print('[INFO] encoding labels ...')
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# training the model 
# Here, we use Linear SVM to train our model
print("[INFO] training model")
recogniser = SVC(C=1.0,kernel='linear', probability=True)
recogniser.fit(data['embeddings'],labels)

# Writing the facial recognition model to disk
f = open("output/recognizer.pickle","wb")
f.write(pickle.dumps(recogniser))
f.close()

# Writing the label encoder
f = open('output/le.pickle','wb')
f.write(pickle.dumps(le))
f.close()

