import os
import cv2
import base64
import numpy as np
from keras.models import load_model
from tensorflow.keras.utils import img_to_array

face_classifier = cv2.CascadeClassifier(
    os.path.join(os.getcwd(), 'haarcascade_frontalface_default.xml'))
classifier = load_model(os.path.join(os.getcwd(), 'model.h5'))

emotion_labels = ['angry', 'disgust', 'fear',
                  'happy', 'neutral', 'sad', 'surprised']


class Expression(object):
    def __init__(self, image_data):
        self.image_data = image_data

    def get_result(self):
        labels = []
        # decode base64 string into bytes
        image = base64.b64decode(self.image_data)
        # convert bytes to numpy array
        nparr = np.frombuffer(image, np.uint8)
        # decode image with OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48),
                                  interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)[0]
                label = emotion_labels[prediction.argmax()]
                labels.append(label)
            else:
                labels.append('No Faces')

        return labels
