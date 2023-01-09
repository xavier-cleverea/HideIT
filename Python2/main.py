from  overlay import Overlay
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
import sys



def main():
    App = QApplication(sys.argv)                                                                                                                  
    overlay = Overlay(App)
    App.exec()
    sys.exit()

if __name__ == "__main__":
    main()

