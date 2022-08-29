# 1.2 Recognizing and displaying the Hands

To get the hands information (number of hands, position and pose of the joints of the hands), we use mediapipe. 
Mediapipe is a set of pre-trained model that have been wrapped up some nice APIs available in different programming language.

The model of the hand in mediapipe


## 1.2.1 Loading the model

In a new Python file, run the below code.
Read the documentation the Hands class to understand its structure.

```python
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
help(mp_hands.Hands)
```

## 1.2.2 Running Medipipe Hands in your image 

Now modify your code that reads an image with opencv to display the hand’s information. You can use the code-snipped below. 

```python
# Run MediaPipe Hands.
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.7) as hands:
  
    # Convert the BGR image to RGB, flip the image around y-axis for correct 
    # handedness output and process it with MediaPipe Hands.
    results = hands.process(cv2.flip(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 1))

    # Print handedness (left v.s. right hand).
    print(results.multi_handedness)

    # Draw hand landmarks of each hand.
    image_hight, image_width, _ = image.shape
    annotated_image = cv2.flip(image.copy(), 1)
    for hand_landmarks in results.multi_hand_landmarks:
      # Print index finger tip coordinates.
      print(
          f'Index finger tip coordinate: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    resize_and_show(cv2.flip(annotated_image, 1))

```

Try the code with different images and observe the console output. What changes? What are the values outputted? 

