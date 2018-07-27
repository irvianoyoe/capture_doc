#!/usr/bin/python
# #
# Capture Document with GUI #
# #
# version 2.3 #
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

class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        button = wx.Button(self, wx.ID_ANY, 'Select Folder', (50, 10))
        button.Bind(wx.EVT_BUTTON, onButton_dir)
        w = button.GetDefaultSize().GetWidth()
        buttontwo = wx.Button(self, wx.ID_ANY, 'Select File', (w+60, 10))
        buttontwo.Bind(wx.EVT_BUTTON, onButton_file)

class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is the second tab", (20,20))

class MyForm(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None,wx.ID_ANY, 'Capture_Dokumen.py')
		self.SetDimensions(0,0,300,120)
		panel = wx.Panel(self, wx.ID_ANY)
		nb = wx.Notebook(panel)
		tab1 = TabOne(nb)
		tab2 = TabTwo(nb)
		nb.AddPage(tab1, "KTP")
		nb.AddPage(tab2, "Log")
		sizer = wx.BoxSizer()
		sizer.Add(nb, 1, wx.EXPAND)
		panel.SetSizer(sizer)
		
#----------------------------------------------------------------------
def crop_ktp(image):
	rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 4))
	sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	inv = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)[1]
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
		if (w > 100 and w < 400) and (h > 10 and h < 22) and (y > 100 and y < 135):
			locs.append((x, y, w, h))
		if (w > 280 and w < 300) and (h >= 20 and h < 31):
			locs.append((x, y, w, h))
	while(len(locs) > 2):
		locs.pop(0)
	(x,y,w,h) = locs[0]
	nama = image[y-5:y+h,x+5:x+w+3]
	(x,y,w,h) = locs[1]
	nik = image[y-5:y+h+5,x-3:x+w+3]
	return (nama,nik)

def reshape_transform_image(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	height, width = img.shape[:2]
	res = cv2.resize(img,(3*width, 3*height), interpolation= cv2.INTER_LINEAR )
	kernel = np.ones((2,2),np.float32)/10
	ret,thresh1 = cv2.threshold(res,100,255,cv2.THRESH_BINARY_INV)
	image = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
	#dst = cv2.filter2D(image,-1,kernel)
	opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
	return opening

def writeNum(image, flag):
    f = open("output.txt",'a')
    if (flag == 1):
    	bahasa = 'ind'
    elif (flag == 0):
    	bahasa = 'nama'
    else:
    	bahasa = 'eng'
    text = pytesseract.image_to_string(image,lang=bahasa)
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
	    print('NIK_reader: \n')
	    for image in images:
	    	(nama,nik) = crop_ktp(image)
	    	show = nik
	    	nama = reshape_transform_image(nama)
	    	nik = reshape_transform_image(nik)
	    	t_nama = writeNum(nama,0)
	    	t_nik = writeNum(nik,1)
	    	print('nik:-'+t_nik)
	    	print('a/n:-'+t_nama)
	    	print('\n')
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
		(nama,nik) = crop_ktp(image)
		show = nik
		nama = reshape_transform_image(nama)
		nik = reshape_transform_image(nik)
		t_nama = writeNum(nama,0)
		t_nik = writeNum(nik,1)
		print('nik:-'+t_nik)
		print('a/n: '+t_nama)
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