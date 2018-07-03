# module 3 image enhancement
#
# deskripsi: untuk enhance image menjadi terbaca dan bagus dan membuat dataset tiap angka
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

	#contouring
	cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	locs = []
	rec = img
	counter2 = 0

	for (i, c) in enumerate(cnts):
		# compute the bounding box of the contour, then use the
		# bounding box coordinates to derive the aspect ratio
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)
	 	#print("masuk_loop")
		# since credit cards used a fixed size fonts with 4 groups
		# of 4 digits, we can prune potential contours based on the
		# aspect ratio
		#if ar > 2.5 and ar < 4.0:
			# contours can further be pruned on minimum/maximum width
			# and height
		if (w > 10 and w < 290) and (h > 15 and h < 45):
			# append the bounding box region of the digits group
			# to our locations list
			locs.append((x, y, w, h))
			#rec = cv2.rectangle(img,(x,y),(w+x,h+y),(0,255,0),3)
			#print("masuk_if")

	#print(len(locs))

	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

	
	for (x,y,w,h) in locs:
		maxw = 16
		maxh = 23
		#print(`w`+" "+`h`)
		counter2 = counter2 + 1
		imgg = img[y:y+h,x:x+w]
		equ = cv2.equalizeHist(imgg)
		name2 = "dataset"+`counter2`+"_pic"+`counter`
		cv2.imwrite("out/ktp/transform/dataset/"+name2+".png", equ)
		cv2.waitKey(0)

	equ = cv2.equalizeHist(img)
	res = np.hstack((img,equ))

	name = "hasil"+`counter`
	counter += 1
	cv2.imwrite("C:/test/out/"+name+".png", equ)

	#cv2.imwrite("C:/test/out/hasil.png", equ)
	#cv2.imshow("th3", img)
	cv2.waitKey(0)