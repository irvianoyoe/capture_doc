# module 3 image enhancement
#
# deskripsi: untuk enhance image menjadi terbaca dan bagus
# input : folder out hasil transformasi
# output: folder out di C: untuk menyesuaikan tessract OS windows
#
# author: @kvkr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from imutils import contours
import imutils
import glob

#u read folder
images = [cv2.imread(file,0) for file in glob.glob("out/ktp/transform/*.png")]
counter = 0

for img in images:

	#img = cv2.imread("out/test.png",0)

	equ = cv2.equalizeHist(img)
	res = np.hstack((img,equ))

	name = "hasil"+`counter`
	counter += 1
	cv2.imwrite("C:/test/out/"+name+".png", equ)

	#cv2.imwrite("C:/test/out/hasil.png", equ)
	#cv2.imshow("th3", res)
	cv2.waitKey(0)