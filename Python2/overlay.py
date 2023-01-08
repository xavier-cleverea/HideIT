from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import *
#from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import subprocess
import re
import string
import sys
import time
from  ocr import OCR


class Overlay(QMainWindow):
        
    #win_id = ""
    def __init__(self, App):
        super().__init__()
        
        
        
        #Setup de la GUI
        self.window = QWidget()
        self.window.setWindowTitle("HideIT")
        self.window.setStyleSheet("background-color: white;")
        self.window.closeEvent = self.exit
        #logo
        self.logo = QLabel(parent=self.window)
        self.logopix = QPixmap('logo50.png')
        self.logo.setPixmap(self.logopix)
        self.logo.move(20,5)
        
        
        #dimensión GUI
        self.window.setGeometry(300, 300, self.logopix.width() + 40, 480)
        self.window.setFixedSize(self.logopix.width() + 40, 480)
        
        
        #boundires checkbox
        self.boundries_check = QCheckBox("Highlight captured window", parent=self.window)
        self.boundries_check.setChecked(True)
        self.show_boundries = True
        self.boundries_check.stateChanged.connect(self.switch_boundries_bool)
        self.boundries_check.move(20, self.logopix.height() + 15)
        
        #pause censor checkbox
        self.censor_check = QCheckBox("Show censored words", parent=self.window)
        self.censor_check.setChecked(False)
        self.show_words = False
        self.censor_check.stateChanged.connect(self.switch_censor_bool)
        self.censor_check.move(20, self.logopix.height() + 45)
        
        #change window
        self.change_window_button = QPushButton("Change window", parent=self.window)
        self.change_window_button.move(20, self.logopix.height() + 75)
        self.change_window_button.clicked.connect(self.change_window)
        
        #text box
        self.text_box = QTextEdit(parent=self.window)
        self.text_box.verticalScrollBar().minimum()
        self.text_box.move(20, self.logopix.height() + 110)
        textfile = open('banned_words.txt','r')
        self.text_box.append(textfile.read())
        textfile.close()
        
        #apply changes button
        
        self.apply_changes_button = QPushButton("Apply Changes", parent=self.window)
        self.apply_changes_button.move(20, self.logopix.height() + 315)
        self.apply_changes_button.clicked.connect(self.apply_changes)
        
        #exit button
        
        self.apply_changes_button = QPushButton("Exit", parent=self.window)
        self.apply_changes_button.move(196, self.logopix.height() + 315)
        self.apply_changes_button.clicked.connect(self.exit)
        
        
        
        self.window.show()
        
        
        
        
        #Al iniciar el programa se ejecuta el comando xdotool el cual nos permite seleccionar una ventana haciendo clickpara obtener su id
        #esta será la ventana donde se creará el overlay, le pasamos el id a xwininfo para saber la posición y tamaño de la
        #ventana seleccionada
        
        #print("Haz click en la ventana que quieras censurar")
        comand = ["xwininfo", "-id", "$(xdotool selectwindow)"]
        comand_result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = comand_result.communicate()
        
        #pillamos los volres que nos interesan mediante regex, la id la guardamos en una variable de clase (win_id)
        self.win_id = re.findall("Window id: +([0-9a-z]+).*", str(result))
        self.x_pos = re.findall("Absolute upper-left X: +([0-9]+).*", str(result))
        self.y_pos = re.findall("Absolute upper-left Y: +([0-9]+).*", str(result)) 
        self.h_pos = re.findall("Height: +([0-9]+).*", str(result))
        self.w_pos = re.findall("Width: +([0-9]+).*", str(result))
        
        self.x_pos_old = self.x_pos
        self.y_pos_old = self.y_pos
        self.h_pos_old = self.h_pos
        self.w_pos_old = self.w_pos

        #Definimos la posición y el tamaño de la ventana
        self.setGeometry(int(self.x_pos[0]), int(self.y_pos[0]), int(self.w_pos[0]), int(self.h_pos[0]))
        self.setWindowTitle("hide-it")

        self.boxes = []


        #definir que el fondo sea transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #definir que se pueda clicar a traves de la ventana
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        #mantener la ventana delante y sin marco
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        
        #print(int(self.win_id[0],16))
        

        self.thread = QThread()
        self.ocr = OCR(int(self.win_id[0],16), App)
        self.ocr.moveToThread(self.thread)
        
        
        
        self.thread.started.connect(self.ocr.update)
        
        self.ocr.end_update.connect(self.updateCensoredAreas)
        
        #self.ocr.finished.connect(self.thread.quit)
        #self.ocr.finished.connect(self.ocr.end_run)
        #self.thread.finished.connect(self.thread.deleteLater)
        #self.ocr.progress.connect(self.reportProgress)
        #print("before thread start")
        self.thread.start()
        
        
        self.configureEvents()
        
        self.show()

    
    def switch_boundries_bool(self):
        self.show_boundries =  not self.show_boundries
        
    def switch_censor_bool(self):
        self.show_words =  not self.show_words
        
        
    def change_window(self):
        #print("Haz click en la ventana que quieras censurar")
        comand = ["xwininfo", "-id", "$(xdotool selectwindow)"]
        comand_result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = comand_result.communicate()
        
        #pillamos los volres que nos interesan mediante regex, la id la guardamos en una variable de clase (win_id)
        self.win_id = re.findall("Window id: +([0-9a-z]+).*", str(result))
        
        self.ocr.WID = int(self.win_id[0],16)
        
        self.x_pos = re.findall("Absolute upper-left X: +([0-9]+).*", str(result))
        self.y_pos = re.findall("Absolute upper-left Y: +([0-9]+).*", str(result)) 
        self.h_pos = re.findall("Height: +([0-9]+).*", str(result))
        self.w_pos = re.findall("Width: +([0-9]+).*", str(result))

        #Definimos la posición y el tamaño de la ventana
        self.setGeometry(int(self.x_pos[0]), int(self.y_pos[0]), int(self.w_pos[0]), int(self.h_pos[0]))
        
        self.showNormal()
        self.update()
        
        
    def apply_changes(self):
        
        textfile = open('banned_words.txt','w')
        textfile.write(self.text_box.toPlainText())
        textfile.close()
        
        
    def exit(self, event = None):
        sys.exit()
    
    def updateCensoredAreas(self):
        #print("test signal")
        self.boxes = self.ocr.boxes_banned
        

    def configureEvents(self):
        
        #Hacemos que updateWin se ejecute cada cierto tiempo con un timer
        timer = QTimer(self)
        timer.timeout.connect(self.updateOverlay)
        #Definir cada cuanto queremos que se ejecute el evento
        timer.start(1)
        self.show()
    
        
        
    def paintEvent(self, e):
        #print("paintEvent")
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))
        
        #print(int(self.x_pos[0]), int(self.y_pos[0]), int(self.w_pos[0]), int(self.h_pos[0]))
        if(self.show_boundries): painter.drawRect(0, 0, int(self.w_pos[0]), int(self.h_pos[0]))
        #painter.drawRect(50, 50, 100, 100)
        
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        if(not self.show_words):
            for (startX, startY, w, h) in self.boxes:
                #print(startY, end ='\n\n\n\n')
                offset = 1.005
                offset2 = 1.008
                painter.drawRect(int(startX*offset2), int(startY * offset), int((w - startX)*offset2), int((h-startY)*offset))
        
        ##pinta un rectangulo de color rojo
        #painter = QPainter(self)
        #painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        ##painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        ##painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))
        #painter.drawRect(100, 15, 400,200)
        
        
        


    
    def updateOverlay(self):
       
        #Se actualiza la posición de la ventana
        comand = ["xwininfo", "-id", self.win_id[0]]
        comand_result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = comand_result.communicate()
        self.x_pos = re.findall("Absolute upper-left X: +([0-9]+).*", str(result))
        self.y_pos = re.findall("Absolute upper-left Y: +([0-9]+).*", str(result)) 
        self.h_pos = re.findall("Height: +([0-9]+).*", str(result))
        self.w_pos = re.findall("Width: +([0-9]+).*", str(result))
        #if(self.x_pos_old != self)
        #para pillar el tamaño de la ventana, puede ser util si queremos evitar el error cuando se acerca a un margen de la pantalla
        #screen = App.primaryScreen()
        #size = screen.size()

        self.setGeometry(int(self.x_pos[0]), int(self.y_pos[0]), int(self.w_pos[0]), int(self.h_pos[0]))
        self.showNormal()
        self.update()



