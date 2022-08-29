# Part 2 Simple Hand Controller using Mediapipe

In this part, to get familiar with the hand information, you will implement a small program that will read the hands information and control the threshold filter of the image.(see https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html )

The threshold function below, takes the pixels in the images and basically set their value to zeros if they are in the range of intensity between 50 and 120. 

```python
ret, thresh = cv2.threshold(annotated_image, 50, 120, cv2.THRESH_TOZERO)
```

Now what we want is to use hand gesture to tune this range in real-time. 

```python
ret, thresh = cv2.threshold(annotated_image, 50+125/100*int(eDistance), 120+125/100*int(eDistance), cv2.THRESH_TOZERO)
```

For that we will use the distance between the tip of the thumb and the index (eDistance)
Write the code to compute eDistance. 

```{note}
Note that we use a scaling factor (125/100) that might depend on the size of your image and the distance of your hands to the screen. Feel free to adjust it to have a nice and wide range of output image as you bring your thumb and index together or apart. 
```
