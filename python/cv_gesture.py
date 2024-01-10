import cv2
import numpy as np


def detect(frame, model, hands, classNames):
    x, y, _ = frame.shape

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Get hand landmark prediction
    result = hands.process(framergb)

    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])

            # Predict gesture in Hand Gesture Recognition project
            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]
            if className not in ["thumbs up", "thumbs down"]:
                className = "none"

    # show the prediction on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    return frame, className
