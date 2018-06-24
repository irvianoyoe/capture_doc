import cv2
import numpy as np
from matplotlib import pyplot as plt
from imutils import contours
import imutils

img = cv2.imread("hasil_rev.png",0)
img = cv2.medianBlur(img,3)
kernel = np.ones((2,2),np.uint8)

ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

img = cv2.bitwise_not(thresh1)
dilation = cv2.dilate(img,kernel,iterations = 1)
dilation2 = cv2.dilate(dilation,kernel,iterations = 1)
blur = cv2.GaussianBlur(dilation,(3,3),0)
med = cv2.medianBlur(img,3)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
erosion = cv2.erode(img,kernel,iterations = 1)

cv2.imwrite("C:/test/hasil_rev2.png", erosion)
cv2.imshow("th3", erosion)
cv2.waitKey(0)