# module 3 image enhancement
#
# deskripsi: untuk enhance image menjadi terbaca dan bagus
# input: out hasil transformasi
# output: out di C: untuk menyesuaikan tessract OS windows
#
# author: @kvkr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from imutils import contours
import imutils

img = cv2.imread("out/test.png",0)

equ = cv2.equalizeHist(img)
res = np.hstack((img,equ))

cv2.imwrite("C:/test/out/hasil.png", equ)
cv2.imshow("th3", res)
cv2.waitKey(0)