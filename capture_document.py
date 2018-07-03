#!/usr/bin/python
# #
# A GUI for Capture Document #
# #
# version 1.0 #
# Created by kevin.kristian #
# #
import wx
import pytesseract
import cv2
import os
import glob
import imutils
import numpy as np
from imutils import contours

class MyForm(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None,wx.ID_ANY, 'Capture_Dokumen.py')
		self.SetDimensions(0,0,300,100)
		panel = wx.Panel(self, wx.ID_ANY)
		button = wx.Button(panel, wx.ID_ANY, 'Select Folder', (50, 10))
		button.Bind(wx.EVT_BUTTON, onButton_dir)
		w = button.GetDefaultSize().GetWidth()
		buttontwo = wx.Button(panel, wx.ID_ANY, 'Select File', (w+60, 10))
		buttontwo.Bind(wx.EVT_BUTTON, onButton_file)
#----------------------------------------------------------------------
def crop_ktp(image):
	rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 7))
	sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	inv = cv2.threshold(gray, 127, 250, cv2.THRESH_BINARY_INV)[1]
	tophat = cv2.morphologyEx(inv, cv2.MORPH_TOPHAT, rectKernel)
	gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,ksize=-1)
	gradX = np.absolute(gradX)
	(minVal, maxVal) = (np.min(gradX), np.max(gradX))
	gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
	gradX = gradX.astype("uint8")
	gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
	thresh = cv2.threshold(gradX, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	locs = []
	for (i, c) in enumerate(cnts):
		(x, y, w, h) = cv2.boundingRect(c)
		if (w > 280 and w < 290) and (h > 15 and h < 45):
			locs.append((x, y, w, h))
	(x,y,w,h) = locs[0]
	return image[y:y+h,x:x+w]

def reshape_transform_image(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.medianBlur(image,3)
	kernel = np.ones((2,2),np.uint8)
	ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
	image = cv2.bitwise_not(thresh1)
	erosion = cv2.erode(image,kernel,iterations = 1)
	dilation = cv2.dilate(erosion,kernel,iterations = 1)
	blur2 = cv2.GaussianBlur(dilation,(3,3),0)
	h = image.shape[0]
	w = image.shape[1]
	border = int((40-h)/2)
	if h<30:
		image = cv2.copyMakeBorder(blur2, border, border, 10, 10, cv2.BORDER_CONSTANT, None, 0)
	if h<40:
		image = cv2.copyMakeBorder(blur2, border, border, 10, 10, cv2.BORDER_CONSTANT, None, 0)
	else:
		image = cv2.copyMakeBorder(blur2, 0, 0, 10, 10, cv2.BORDER_CONSTANT, None, 0)
	return image

def writeNum(image):
    f = open("output.txt",'a')
    text = pytesseract.image_to_string(image,lang='ind')
    f.write(text+'\n')
    f.close()
    return text

def onButton_dir(event):
	dlg = wx.DirDialog (frame, "Choose input directory", "",
		                wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
	dlg.ShowModal()
	if dlg.GetPath() == '':
		wx.MessageBox('Folder not found', 'Error', wx.OK | wx.ICON_ERROR)
	else:
	    print("folder_path: "+ dlg.GetPath())
	    images = [cv2.imread(file) for file in glob.glob(dlg.GetPath()+"/*.jpg")]
	    print('NIK_reader: ')
	    for image in images:
	    	image = crop_ktp(image)
	    	show = image
	    	image = reshape_transform_image(image)
	    	t = writeNum(image)
	    	print(':-'+t)
	    	cv2.imshow('show',show)
	    	cv2.waitKey(0)
	    wx.MessageBox('Hasil di Output.txt', 'Done!', wx.OK | wx.ICON_INFORMATION)

def onButton_file(event):
	openFileDialog = wx.FileDialog(frame, "Open", "", "", 
		                                      "Image file (*.jpg; *.png)|*.jpg; *png", 
		                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	openFileDialog.ShowModal()
	if openFileDialog.GetPath() == '':
		wx.MessageBox('File not found', 'Error', wx.OK | wx.ICON_ERROR)
	else:
		print("file_path: "+ openFileDialog.GetPath())
		print('NIK_reader: ')
		image = cv2.imread(openFileDialog.GetPath())
		image = crop_ktp(image)
		show = image
		image = reshape_transform_image(image)
		t = writeNum(image)
		print(':-'+t)
		cv2.imshow('show',show)
		cv2.waitKey(0)
		wx.MessageBox('Hasil di Output.txt', 'Done!', wx.OK | wx.ICON_INFORMATION)

def rewrite_out():
	f = open('output.txt','w')
	f.write('')
	f.close


if __name__ == '__main__':
	rewrite_out()
	app = wx.App()
	frame = MyForm()
	frame.Show()
	frame.Centre()
	app.MainLoop()