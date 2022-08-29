# 1.3 Using your Webcam with VideoCapture

Now, we want our game to work on real-time capture image. So we will now try to stream our video camera stream and displaying it using opencv.  Below is the code snippet that lets you read and stream your webcam images

```python
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640) # adjust width
cap.set(4,480) # adjust height

while True:
    success, img = cap.read()
    cv2.imshow("Webcam", img) # This will open an independent window
    if cv2.waitKey(1) & 0xFF==ord('q'): # quit when 'q' is pressed
        cap.release()
        break
cv2.destroyAllWindows() 
cv2.waitKey(1) 
```
