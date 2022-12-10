from  overlay import Overlay
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
import sys

App = QApplication(sys.argv)                                                                                                                  
overlay = Overlay()
App.exec()
print("hola")
sys.exit()
