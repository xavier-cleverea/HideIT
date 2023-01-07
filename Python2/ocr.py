
import cv2
        
import numpy as np
import argparse
import time
import PIL.Image
import PIL.ImageOps
from tesserocr import PyTessBaseAPI, image_to_text, RIL
#import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QScreen
from PyQt5 import QtCore

#from datetime import datetime
#import subprocess
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from  overlay import *

class OCR(QObject):
    
    end_update = pyqtSignal()
    
    def __init__(self, WID, App ):
        super().__init__()
        print("ocr init")
        self.app = App
        self.WID = WID
        
        
        

        
        #self.started.connect(self.ocr.update)
    def load_to_mem(self):
        self.api = PyTessBaseAPI(lang='eng', path='/usr/share/tesseract-ocr/5/tessdata')
        #The quick red fox jumps over the lazy dog.
        
        
        self.banned_words = []

        self.boxes_banned = []
    
    
    def update(self):
        time.sleep(5)
        self.load_to_mem()

        
        while True:
            
            self.banned_words = []
            
            banned_boxes = []
            f = open('banned_words.txt','r')
            for line in f:
                for w in line.split():
                    w = w.strip()
                    w = w.lower()
                    w = w.replace('i','t')
                    self.banned_words.append(w)
            
            #print("start ocr update")
            #pilla captura y pasa su formato a formato de imagen opencv
            pixmap = QScreen.grabWindow(self.app.primaryScreen(), self.WID)
            qimg = pixmap.toImage()
            qimg = qimg.convertToFormat(4)
            imgWidth = qimg.width()
            imgHeight = qimg.height()
            ptr = qimg.bits()
            ptr.setsize(qimg.byteCount())
            image = np.array(ptr).reshape(imgHeight, imgWidth, 4)
            image = image[:,:,:3]
            
            cv2.imwrite("tmp/test.png",image)

            self.api.SetImage(PIL.Image.fromarray(image))
            
            boxes = self.api.GetComponentImages(RIL.WORD,True)
            #print(boxes)
            #print('\n\n')

            word_list = []
            for (_, box, _, _) in boxes:
                #Y = vertical, X = horizontal
                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']
                #print(x,y,w,h)
                
                if w > (imgWidth/2): break #aveces pilla toda la pantalla como si fuera una sola palabra
                
                w += 5
                h += 5
                
                if (x+w) > imgWidth: w = imgWidth - x
                if (y+h) > imgHeight: h = imgHeight - y
                x -= 5
                y -= 5
                if x < 0: x = 0
                if y < 0: y = 0
                
                #print(x, end ='\n\n\n\n')
                
                self.api.SetRectangle(x,y,w,h)
                
                #crop_img = image[y:(y+h), x:(x+w)]
                #cv2.imwrite("tmp/" + str(y) + str(x) + str(h) + str(w) + ".png",crop_img)

                #print(x,y,w,h)
                word = self.api.GetUTF8Text()
                
                #conf = self.api.MeanTextConf()
                


                
                
                word = word.lower()
                word = word.strip()
                
                #word = ''.join(char for char in word if ord(char) < 128)
                #print(word)
                word = word.replace('i','t')
                word = word.replace("\n",'')
                word_list.append(word)
                #print(word)
                
                for banned_word in self.banned_words:
                    if banned_word in word:
                        #print("banned word : " + banned_word + " found.")
                        banned_boxes.append((x,y,x+w,y+h))
                        break
                    
                
                #cv2.imwrite("tmp/" + word + ".png",crop_img) #para testear que lee las palabras bien
            #end = time.time()
            #print(end-start)

            #print(banned_boxes)
            #self.OL.boxes = banned_boxes
            #self.OL.update()
            
            #print(self.OL.boxes)
            #print(word_list)
            self.boxes_banned = banned_boxes #esto no es confuso, solo hace falta no mirar
            #print("end ocr update")
            self.end_update.emit()
            #time.sleep(1)
            #time.sleep(2)
            #print("signal sent")



#print("Haz click en la ventana que quieras censurar")
#comand = ["xdotool", "selectwindow"]
#comand_result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


#result = comand_result.communicate()
#WID = int(result[0])


#ocr = OCR(WID)
#while(True):
    #ocr.update()
    #print("end iteration",end = '\n\n')
    ##time.sleep(1)
