import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QScreen
from datetime import datetime
import subprocess

comand = ["xdotool", "selectwindow"]
comand_result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result = comand_result.communicate()
print(result[0])

date = datetime.now()
#filename = date.strftime('%Y-%m-%d_%H-%M-%S.jpg')
filename = "screenshot.jpg"
app = QApplication(sys.argv)
QScreen.grabWindow(app.primaryScreen(), int(result[0])).save(filename, 'png')