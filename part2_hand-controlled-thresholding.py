import matplotlib.pyplot as plt
import cv2
import numpy as np
import mediapipe as mp
import math


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


cap = cv2.VideoCapture(0)
cap.set(3,640) # adjust width
cap.set(4,480) # adjust height




while True:
    success, img = cap.read()
    # Run MediaPipe Hands.
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.7) as hands:
    
        # Convert the BGR image to RGB, flip the image around y-axis for correct 
        # handedness output and process it with MediaPipe Hands.
        results = hands.process(cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1))

        # Print handedness (left v.s. right hand).
        print(results.multi_handedness)

        if not results.multi_hand_landmarks:
            continue
    
        # Draw hand landmarks of each hand.
        image_hight, image_width, _ = img.shape
        annotated_image = cv2.flip(img.copy(), 1)
        for hand_landmarks in results.multi_hand_landmarks:
            # Print index finger tip coordinates.
            print(
                f'Index finger tip coordinate: (',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight})'
            )

            eDistance = math.dist([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight], [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_hight])

            print(eDistance)

            ret, thresh = cv2.threshold(annotated_image, 50+125/100*int(eDistance), 120+125/100*int(eDistance), cv2.THRESH_TOZERO)

            mp_drawing.draw_landmarks(
                thresh,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())


        cv2.imshow("Webcam", thresh) # This will open an independent window
        if cv2.waitKey(1) & 0xFF==ord('q'): # quit when 'q' is pressed
            cap.release()
            break
        
cv2.destroyAllWindows() 
cv2.waitKey(1) # normally unnecessary, but it fixes a bug on MacOS where the window doesn't close view raw