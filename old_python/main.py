from absl import app
from absl import flags
from keras.models import load_model #pretain model and load it up
import cv2
import logging
import mediapipe as mp
import numpy as np
#import tensorflow as tf

from cv_gesture import detect


FLAGS = flags.FLAGS


def main(_):
    #initialize logger
    logger = logging.getLogger("movecado")
    logger.setLevel(logging.INFO)

    #initialize the mediapipe hands model
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7)

    #initialize the webcam and get the frame size
    cap = cv2.VideoCapture(0) #0 is actual visible camera
    _, img = cap.read()
    height, width, _ = img.shape

    #load the gesture regonixser model
    model = load_model('/Users/avashah/Downloads/data/mp_data_gesture')

    #load class names
    with open('data/gesture.names', 'r') as f:
        class_names = f.read().split('\n')
    logger.info('class names loaded')

    #commit a sin
    while True:
        #read the image from the webcam
        _, img = cap.read()

        #flip the image
        img = cv2.flip(img, 1)

        #convert image to RGB (media pipe requires RGB input)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   

        #process the image to detect the hands
        results = hands.process(img_rgb)     

        #display the image with hand landmarks
        cv2.imshow('Hand Tracking', img)

        #if hands are detected
        if results.multi_hand_landmarks:
            for hand_lamdmarks in results.multi_hand_landmarks:
                #draw the hand landmarks on teh image
                for landmark in hand_lamdmarks.landmark:
                    h, w, _ = img.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(img, (x,y), 5, (0,0,0), -1)
                mp_drawing.draw_landmakrs(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)



        #detect gestures
        img, gesture = detect(img, model, hands, class_names)
        logger.info(gesture)


        #edit when q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #release video capture and close all openCV windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    #require that flags are inputed
    app.run(main)