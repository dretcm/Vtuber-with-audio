import sys
import sounddevice as sd
import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from data.dialogs import Dialogs

class Vt(QWidget):
        def __init__(self):
                QWidget.__init__(self)

                try:
                        self.stream = sd.Stream(callback = self.stream_sound)

                        self.sensivility = 2
                        self.limit = 15
                        self.volume = 0
                        
                        self.normal = QPixmap("./data/images/normal.png")
                        self.talk = QPixmap("./data/images/talk.png")
                        self.scream = QPixmap("./data/images/scream.png")
                        self.current = self.normal

                        
                        self.label = QLabel(self)
                        self.label.setPixmap(self.current)

                        vbox = QVBoxLayout()
                        vbox.addWidget(self.label)
                        
                        self.setLayout(vbox)

                        self.timer = QtCore.QTimer(self)
                        self.timer.timeout.connect(self.update_img)
                        
                        self.setWindowIcon(QIcon('data/images/yasu.ico'))
                        self.setWindowTitle('Avatar')

                        self.setFixedSize(self.sizeHint())
                        self.move(150,150)
                        
                except Exception as e:
                        Dialogs.dialog(text=str(e))

        def start(self):
                self.stream.start()
                self.timer.start()
                self.show()
                
        def update_img(self):
                self.label.setPixmap(self.current)
                        
        def stream_sound(self, indata, outdata, frames, time, status):  # sounddevices Stream's function.
                self.volume = np.linalg.norm(indata)  # use the Frobenius norm
                #print(self.volume)
                
                if self.volume > self.sensivility:
                        if self.volume > self.limit:
                                self.current = self.scream
                        else:
                                self.current = self.talk
                else:
                        self.current = self.normal
                
        def stop(self):
                self.stream.stop()
                self.volume = 0
                self.close()  # destroy the window
                self.timer.stop()

        def set_sensivility(self, value):
                self.sensivility = value


if __name__=='__main__':
        app = QApplication(sys.argv)
        vt = Vt()
        vt.start()
        sys.exit(app.exec_())


        
