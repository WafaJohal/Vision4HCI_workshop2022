import cv2

image = cv2.imread("thumbup.jpeg")
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)  # normally unnecessary, but it fixes a bug on 
                    # MacOS where the window doesn't close view raw