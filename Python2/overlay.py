from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
import subprocess
import re
import string
import sys
import time


class Overlay(QMainWindow):
        
    win_id = ""
    def __init__(self):
        super().__init__()
        #Al iniciar el programa se ejecuta el comando xdotool el cual nos permite seleccionar una ventana haciendo clickpara obtener su id
        #esta será la ventana donde se creará el overlay, le pasamos el id a xwininfo para saber la posición y tamaño de la
        #ventana seleccionada

        print("Haz click en la ventana que quieras censurar")
        comand = ["xwininfo", "-id", "$(xdotool selectwindow)"]
        comand_result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = comand_result.communicate()
        
        #pillamos los volres que nos interesan mediante regex, la id la guardamos en una variable de clase (win_id)
        self.win_id = re.findall("Window id: +([0-9a-z]+).*", str(result))
        x_pos = re.findall("Absolute upper-left X: +([0-9]+).*", str(result))
        y_pos = re.findall("Absolute upper-left Y: +([0-9]+).*", str(result)) 
        h_pos = re.findall("Height: +([0-9]+).*", str(result))
        w_pos = re.findall("Width: +([0-9]+).*", str(result))
       # print(x_pos[0], y_pos[0], h_pos[0], w_pos[0])


        #para pillar el tamaño de la ventana, puede ser util si queremos evitar el error cuando se acerca a un margen de la pantalla
        #screen = App.primaryScreen()
        #size = screen.size()

        #Definimos la posición y el tamaño de la ventana
        self.setGeometry(int(x_pos[0]), int(y_pos[0]), int(w_pos[0]), int(h_pos[0]))
        self.setWindowTitle("hide-it")

        #definir que el fondo sea transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #definir que se pueda clicar a traves de la ventana
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        
        #transparencia de la ventana (ya no hace falta)
        #self.setStyleSheet("background-color: red;")
        #self.setWindowOpacity(1)

        #mantener la ventana delante y sin marco
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        #self.showMaximized()

        #Hacemos que updateWin se ejecute cada cierto tiempo con un timer
        timer = QTimer(self)
        timer.timeout.connect(self.updateOverlay)
        #Definir cada cuanto queremos que se ejecute el evento
        timer.start(1)

        self.show()

    def paintEvent(self, e):
        #pinta un rectangulo de color rojo
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        #painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))

        painter.drawRect(100, 15, 400,200)

    def updateOverlay(self):
       
        #Se actualiza la posición de la ventana
        comand = ["xwininfo", "-id", self.win_id[0]]
        comand_result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = comand_result.communicate()
        x_pos = re.findall("Absolute upper-left X: +([0-9]+).*", str(result))
        y_pos = re.findall("Absolute upper-left Y: +([0-9]+).*", str(result)) 
        h_pos = re.findall("Height: +([0-9]+).*", str(result))
        w_pos = re.findall("Width: +([0-9]+).*", str(result))
        #print(x_pos[0], y_pos[0], h_pos[0], w_pos[0])

        self.setGeometry(int(x_pos[0]), int(y_pos[0]), int(w_pos[0]), int(h_pos[0]))
        self.showNormal()


App = QApplication(sys.argv)
overlay = Overlay()
sys.exit(App.exec())


