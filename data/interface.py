import sys, os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMessageBox, QProgressBar, QSlider, QCheckBox, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

from data.vt_interface import Vt
from data.dialogs import Dialogs


class Interface(QWidget):
        def __init__(self):
                QWidget.__init__(self)

                self.__path = "./data/images/"
                self.program = Vt()

                self.initUI()
                
                self.setWindowIcon(QIcon('data/images/yasu.ico'))
                self.setWindowTitle('Virtual Avatar Voice')
                
                self.setFixedSize(300, 250)  # size window
                self.move(800,250)  # pos in the window display
                
                self.show()

        def initUI(self):

                label = QLabel("Settings", self)
                label.setGeometry(10,17,80,30)
                label.setStyleSheet('''
                                text-decoration: underline;
                                font: 16pt "MS Shell Dlg 2"
                                ''')

                label = QLabel("Sensitivity:", self)
                label.setGeometry(10,114,70,20)
                label.setStyleSheet('font: 10pt "MS Shell Dlg 2"')

                label = QLabel("Microphone:", self)
                label.setGeometry(10,155,70,20)
                label.setStyleSheet('font: 10pt "MS Shell Dlg 2"')

                self.label = QLabel("2", self)
                self.label.setGeometry(270,114,70,20)
                label.setStyleSheet('font: 10pt "MS Shell Dlg 2"')

                
                cb = QCheckBox('Mute', self)
                cb.setGeometry(190,20,50,30)
                # cb.toggle()
                cb.stateChanged.connect(self.mute)
                
                self.slider = QSlider(Qt.Horizontal, self)
                self.slider.setGeometry(90,117,170,20)
                self.slider.setRange(0, 30)
                self.slider.setValue(2)
                
                self.start = QPushButton("Start", self)
                self.start.setGeometry(50,200,90,30)
                self.start.setStyleSheet('font: 11pt "Arial";')

                self.stop = QPushButton("Stop", self)
                self.stop.setGeometry(160,200,90,30)
                self.stop.setStyleSheet('font: 11pt "Arial";')
                
                self.bar = QProgressBar(self)
                self.bar.setGeometry(90,160,205,10)
                self.bar.setMaximum(30)
                self.bar.setMinimum(0)
                self.bar.setValue(0)

                self.timer = QtCore.QTimer(self)
                self.timer.timeout.connect(self.update_volume)

                self.cbox = QComboBox(self)
                self.cbox.setStyleSheet('font: 75 11pt "Arial";')
                self.cbox.setGeometry(10,67,150,30)
                for path in os.listdir(self.__path):
                        if not os.path.isfile(os.path.join(self.__path, path)):
                                self.cbox.addItem(path)
                

                self.refresh = QPushButton("Update", self)
                self.refresh.setGeometry(190,67,90,30)
                self.refresh.setStyleSheet('font: 11pt "Arial";')

                
                self.slider.valueChanged[int].connect(self.setLabel)

                self.refresh.clicked.connect(self.update_avatar)
                self.start.clicked.connect(self.start_process)
                self.stop.clicked.connect(self.stop_process)


        def update_avatar(self):
                try:
                        self.program.update_avatar(self.cbox.currentText())
                except Exception as e:
                        Dialogs.dialog(text=str(e))

        def mute(self, state):
                if state == Qt.Checked:
                        self.program.stream.stop()
                        self.program.current = self.program.normal
                        self.stop_timer()
                else:
                        self.program.stream.start()
                        self.timer.start()
                    
        def update_volume(self):
                try:
                        self.bar.setValue(min(30, int(self.program.volume)))
                        if self.program.state:
                                self.start.setEnabled(False)
                        else:
                                self.stop_process()
                except Exception as e:
                        Dialogs.dialog(text=str(e))


        def setLabel(self, value):
                self.label.setText(str(value))
                self.program.set_sensivility(value)

        def start_process(self):
                try:
                        self.timer.start()
                        self.program.start()
                        
                except Exception as e:
                        Dialogs.dialog(text=str(e))
                        

        def stop_process(self):
                try:
                        self.stop_timer()
                        self.program.stop()
                        self.start.setEnabled(True)
                        
                except Exception as e:
                        Dialogs.dialog(text=str(e))

        def stop_timer(self):
                        self.timer.stop()
                        self.bar.setValue(0)

        def closeEvent(self, event):
                self.program.stop()
                
                
if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Interface()
        sys.exit(app.exec_())
        
