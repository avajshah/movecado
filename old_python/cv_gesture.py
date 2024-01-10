import cv2
import numpy as np

def detect(frame, model, hands, class_name):
    x, y, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(frame_rbg)

    class_name = ''

    #post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for hand_landmarks in result.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                lmx = int(landmark.x * x)
                lmy = int(landmark.y * x)
                landmarks.append([lmx, lmy])
            #predict gesture in hand gesture recognition model
            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = class_naes[classID]
            if class_name not in ['thumbs up', 'thumbs down']:
                classname = 'none'
            #show the prediction on the grame
            cv2.putText(frame, class_name, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            return frame, class_name 