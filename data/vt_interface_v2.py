import sys, os
import sounddevice as sd
import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from data.dialogs import Dialogs


class Vt(QWidget):
        def __init__(self):
                super().__init__()

                try:
                        self.width = 550
                        self.height = 425
                        self.window_size = QtCore.QSize(self.width, self.height)
                        self.state = False
                        
                        self.stream = sd.Stream(callback = self.stream_sound)

                        self.sensivility = 2
                        self.limit = 10
                        self.volume = 0

                        self.label = QLabel(self)
                        self.label.setGeometry(0,0,self.width,self.height)
                        
                        self.__path = "./data/images/"
                        #self.__photos = ["normal", "talk", "scream"]
                        self.__formats = [".png", ".jpg"]
                        self.frame = 0
                        self.update_avatar("Alexander")

                        self.timer = QtCore.QTimer(self)
                        self.timer.timeout.connect(self.update_img)
                        
                        self.setWindowIcon(QIcon('data/images/yasu.ico'))
                        self.setWindowTitle('Avatar')

                        self.setFixedSize(self.window_size) # (self.sizeHint())
                        self.move(150,150)
                        
                except Exception as e:
                        Dialogs.dialog(text=str(e))


        def start(self):
                self.stream.start()
                self.timer.start()
                self.show()
                self.state = True
                
        def update_img(self):
                if self.frame >= len(self.current):
                        self.frame = 0

                self.label.setPixmap(self.current[int(self.frame)])
                self.frame += 0.05
                
                        
        def stream_sound(self, indata, outdata, frames, time, status):  # sounddevices Stream's function.
                self.volume = np.linalg.norm(indata)  # use the Frobenius norm
                #print(self.volume)
                
                if self.volume > self.sensivility:
                        if self.volume > self.limit + self.sensivility:
                                self.current = self.scream
                        else:
                                self.current = self.talk
                else:
                        self.current = self.normal

                
        def stop(self):
                self.stream.stop()
                self.volume = 0
                self.timer.stop()
                self.state = False
                self.close()  # destroy the window

        def set_sensivility(self, value):
                self.sensivility = value
                self.limit = value + 10

        def verificate_folder(self, path):
                files = []
                for file in os.listdir(path):
                        name, extension = os.path.splitext(file)
                        name = name.lower()
                        if extension.lower() in self.__formats: # and name in self.__photos:
                                files.append(QPixmap(path+file))
                        else:
                                raise Exception("Error: any image dont be a file .png or .jpg format or the name is wrong.")
                images = []
                for file in files:
                        images.append(file.scaled(self.window_size))
                
                return images

        def update_avatar(self, folder):
                path = self.__path + folder + "/"
                
                self.normal = self.verificate_folder(path+"normal/")
                self.talk = self.verificate_folder(path+"talk/")
                self.scream = self.verificate_folder(path+"scream/")
                
                self.current = self.normal

        def closeEvent(self, event):
                self.stop()
                
if __name__=='__main__':
        app = QApplication(sys.argv)
        vt = Vt()
        vt.start()
        sys.exit(app.exec_())


        
