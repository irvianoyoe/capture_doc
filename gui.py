#!/usr/bin/python
 
import wx
import pytesseract
import cv2
import os

def writeNum(image):
    f = open("output.txt",'w')
    text = pytesseract.image_to_string(image,lang='ind')
    f.write(text)
    f.close()

def onButton(event):
    openFileDialog.ShowModal()
    image = cv2.imread(openFileDialog.GetPath())
    writeNum(image)
    wx.MessageBox('Done! Hasil di Output.txt', 'Info', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, 'win.py')
    frame.SetDimensions(0,0,300,100)

    panel = wx.Panel(frame, wx.ID_ANY)
    button = wx.Button(panel, wx.ID_ANY, 'FILE', (10, 10))
    button.Bind(wx.EVT_BUTTON, onButton)

    openFileDialog = wx.FileDialog(frame, "Open", "", "", 
                                          "Image file (*.png)|*.png", 
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    frame.Show()
    frame.Centre()
    app.MainLoop()