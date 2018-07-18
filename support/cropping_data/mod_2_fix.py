# module 2 image transformation fixed
#
# deskripsi: modul ini untuk mengubah ubah bentuk, contrast, dan memperbaiki gambar dengan melakukan transformasi
#
#
# Version: Betav-1.0
# author: @kvkr

import numpy as np
import imutils
import cv2
import glob

img = cv2.imread("out0.png",0)
height, width = img.shape[:2]
res = cv2.resize(img,(3*width, 3*height), interpolation= cv2.INTER_LINEAR )

kernel = np.ones((2,2),np.float32)
ret,thresh1 = cv2.threshold(res,100,255,cv2.THRESH_BINARY)
img = cv2.bitwise_not(thresh1)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

cv2.imwrite("coba6.png",closing)
cv2.imshow("th3", closing)
cv2.waitKey(0)