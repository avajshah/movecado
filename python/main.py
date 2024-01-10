from absl import app
from absl import flags
from tensorflow.keras.models import load_model
import cv2
import logging
import mediapipe as mp
import numpy as np
import tensorflow as tf

from cv_button import Button
from cv_keyboard import Keyboard
from cv_gesture import detect


FLAGS = flags.FLAGS
flags.DEFINE_boolean("keyboard", None, "Initialize keyboard.")
flags.DEFINE_boolean("slider", None, "Initialize slider.")
flags.DEFINE_boolean("updown", None, "Initialize up and down buttons.")
flags.DEFINE_boolean("leftright", None, "Initialize left and right buttons.")
flags.DEFINE_boolean("flappybird", None, "Initialize space button for flappybird")


def main(_):
    # Initialize the logger
    logger = logging.getLogger("movementum")
    logger.setLevel(logging.INFO)

    # Initialize Mediapipe Hand model
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    # Initialize the webcam and get the width and height
    cap = cv2.VideoCapture(0)
    _, img = cap.read()
    height, width, _ = img.shape

    # Initialize the input sources
    sources = []
    if FLAGS.keyboard:
        sources.append(Keyboard())
    if FLAGS.slider:
        # TODO
        ...
    if FLAGS.updown:
        up = Button(coords=(300, 50, width - 300, 200),
                    text="UP")
        down = Button(coords=(300, height - 200, width - 300, height - 50),
                      text="DOWN")
        sources.append(up)
        sources.append(down)
    if FLAGS.leftright:
        left = Button(coords=(50, 50, 300, height - 50),
                      text="LEFT")
        right = Button(coords=(width - 300, 50, width - 50, height - 50),
                       text="RIGHT")
        sources.append(left)
        sources.append(right)
    if FLAGS.flappybird:
        space = Button(coords=(width - 300, 50, width - 50, height - 50),
                        text="SPACE")
        sources.append(space)
    # Load the gesture recognizer model
    model = load_model('data/mp_hand_gesture')

    # Load class names
    with open('data/gesture.names', 'r') as f:
        classNames = f.read().split('\n')

    while True:
        # Read the image from the webcam
        success, img = cap.read()

        # Flip the image horizontally to create a mirror effect
        img = cv2.flip(img, 1)

        # Convert the image to RGB (MediaPipe requires RGB input)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the image
                for landmark in hand_landmarks.landmark:
                    h, w, _ = img.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(img, (x, y), 5, (0, 0, 0), -1)
                mp_drawing.draw_landmarks(img,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS)

                # Check if index finger tip is within the regions of the virtual keyboard
                x_index = int(hand_landmarks.landmark[8].x * w)
                y_index = int(hand_landmarks.landmark[8].y * h)

                # Update all of the sources
                for source in sources:
                    source.update((x_index, y_index))

        # Draw all of the sources
        for source in sources:
            img = source.draw(img)

        # Detect gestures
        img, gesture = detect(img, model, hands, classNames)
        logger.info(gesture)

        # Display the image with hand landmarks
        cv2.imshow("Hand Tracking", img)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Required flags
    flags.mark_flag_as_required("keyboard")
    flags.mark_flag_as_required("slider")
    flags.mark_flag_as_required("updown")
    flags.mark_flag_as_required("leftright")
    flags.mark_flag_as_required("flappybird")
    app.run(main)
