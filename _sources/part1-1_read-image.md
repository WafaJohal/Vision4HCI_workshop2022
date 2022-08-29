---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Part 1 Getting Familiar with OpenCV and MediaPipe

The first part is to get familiar with OpenCV and mediapipe.
In this part, you will learn how to read and display images and use mediapipe to detect hands on the images.

## 1.1 Loading an Image and Displaying it using OpenCV

Take a picture of yourself with a thumbup
We will be using this image to get familiar with the hand detection using mediapipe

Use the code below to read and display the image using OpenCV. 
OpenCV is a big library, and you can find documentation here: 
https://opencv.org/

 
```python
import cv2

image = cv2.imread("thumbup.jpeg")
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1) # normally unnecessary, but it fixes a bug on MacOS where the window doesn't close view

```
