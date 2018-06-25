# module 2 image transformation
#
# deskripsi: modul ini untuk mengubah ubah bentuk, contrast, dan memperbaiki gambar
# input : folder src
# output: folder out hasil transformasi
#
# author: @kvkr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from imutils import contours
import imutils

img = cv2.imread("out/out0.png",0)
img = cv2.medianBlur(img,3)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel = np.ones((2,2),np.uint8)

ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

img = cv2.bitwise_not(thresh1)
dilation = cv2.dilate(img,kernel,iterations = 1)
dilation2 = cv2.dilate(dilation,kernel,iterations = 1)
blur = cv2.GaussianBlur(dilation,(3,3),0)
med = cv2.medianBlur(img,3)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

erosion = cv2.erode(img,kernel,iterations = 1)
dilation = cv2.dilate(erosion,kernel,iterations = 1)
blur2 = cv2.GaussianBlur(dilation,(3,3),0)

#blur3 = cv2.medianBlur(erosion,3)



cv2.imwrite("out/test.png", blur2)
cv2.imshow("th3", dst)
cv2.waitKey(0)