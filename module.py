# module 1 image cropping
#
# deskripsi: untuk mengcrop image secara otomatis terhadap ktp folder src
# input : folder src gambar .jpg
# output: folder out hasil cropping
#
# author: @kvkr
# referensi: credit card ocr *basic: https://www.pyimagesearch.com/2017/07/17/credit-card-ocr-with-opencv-and-python/
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import glob

#referensi angka ocr-a ikut web
ref = cv2.imread("ref.jpg")
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]

refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}

for (i, c) in enumerate(refCnts):
	# compute the bounding box for the digit, extract it, and resize
	# it to a fixed size
	(x, y, w, h) = cv2.boundingRect(c)
	roi = ref[y:y + h, x:x + w]
	roi = cv2.resize(roi, (57, 88))
 
	# update the digits dictionary, mapping the digit name to the ROI
	digits[i] = roi

#set kernel
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 7))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

#u read folder
images = [cv2.imread(file) for file in glob.glob("src/*.jpg")]

counter = 0
for image in images:

	#ngambil image
	#image = cv2.imread("ktp1.jpg")
	#image = imutils.resize(image, width=300)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	inv = cv2.threshold(gray, 127, 250, cv2.THRESH_BINARY_INV)[1]

	tophat = cv2.morphologyEx(inv, cv2.MORPH_TOPHAT, rectKernel)

	gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
		ksize=-1)
	gradX = np.absolute(gradX)
	(minVal, maxVal) = (np.min(gradX), np.max(gradX))
	gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
	gradX = gradX.astype("uint8")

	gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
	thresh = cv2.threshold(gradX, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	 
	# apply a second closing operation to the binary image, again
	# to help close gaps between credit card number regions
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

	#contouring
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	locs = []
	rec = image

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
		if (w > 280 and w < 290) and (h > 15 and h < 45):
			# append the bounding box region of the digits group
			# to our locations list
			locs.append((x, y, w, h))
			#rec = cv2.rectangle(image,(x,y),(w+x,h+y),(0,255,0),3)
			#print("masuk_if")

	#potong
	#print(locs)
	(x,y,w,h) = locs[0]
	img = image[y:y+h,x:x+w]
	
	#img = imutils.resize(img, height=35, width=285)
	name = "out"+`counter`
	counter += 1
	cv2.imwrite("out/"+name+".png", img)
	#cv2.imshow("th3", rec)
	cv2.waitKey(0)