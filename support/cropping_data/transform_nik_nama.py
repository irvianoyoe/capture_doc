import numpy as np
import imutils
import cv2
import glob

images = [cv2.imread(file,0) for file in glob.glob("out/*.png")]

#img = cv2.imread("out5.png",0)
counter = 0
for img in images:
	height, width = img.shape[:2]
	res = cv2.resize(img,(3*width, 3*height), interpolation= cv2.INTER_LINEAR )

	kernel = np.ones((2,2),np.float32)
	ret,thresh1 = cv2.threshold(res,100,255,cv2.THRESH_BINARY)
	img = cv2.bitwise_not(thresh1)
	closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

	nama = 'hasil%d' % (counter)
	counter += 1
	cv2.imwrite("out/ktp/transform/"+nama+".png",closing)
	cv2.imshow("th3", closing)
	cv2.waitKey(0)