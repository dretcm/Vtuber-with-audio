import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMessageBox, QProgressBar, QSlider, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

from data.vt_interface import Vt
from data.dialogs import Dialogs


class Interface(QWidget):
        def __init__(self):
                QWidget.__init__(self)

                self.program = Vt()

                self.initUI()
                
                self.setWindowIcon(QIcon('data/images/yasu.ico'))
                self.setWindowTitle('Virtual Avatar Voice')
                
                self.setFixedSize(300, 200)
                self.move(800,150)
                
                self.show()

        def initUI(self):

                label = QLabel("Settings", self)
                label.setGeometry(10,15,80,30)
                label.setStyleSheet('''
                                text-decoration: underline;
                                font: 16pt "MS Shell Dlg 2"
                                ''')

                label = QLabel("Sensitivity:", self)
                label.setGeometry(10,64,70,20)
                label.setStyleSheet('font: 10pt "MS Shell Dlg 2"')

                label = QLabel("Microphone:", self)
                label.setGeometry(10,105,70,20)
                label.setStyleSheet('font: 10pt "MS Shell Dlg 2"')

                self.label = QLabel("2", self)
                self.label.setGeometry(270,64,70,20)
                label.setStyleSheet('font: 10pt "MS Shell Dlg 2"')

                cb = QCheckBox('Mute', self)
                cb.setGeometry(150,18,50,30)
                # cb.toggle()
                cb.stateChanged.connect(self.mute)
                
                self.slider = QSlider(Qt.Horizontal, self)
                self.slider.setGeometry(90,67,170,20)
                self.slider.setRange(0, 30)
                self.slider.setValue(2)
                
                self.start = QPushButton("Start", self)
                self.start.setGeometry(50,150,90,30)
                self.start.setStyleSheet('font: 11pt "Arial";')

                self.stop = QPushButton("Stop", self)
                self.stop.setGeometry(160,150,90,30)
                self.stop.setStyleSheet('font: 11pt "Arial";')
                
                self.bar = QProgressBar(self)
                self.bar.setGeometry(90,110,205,10)
                self.bar.setMaximum(30)
                self.bar.setMinimum(0)
                self.bar.setValue(0)

                self.timer = QtCore.QTimer(self)
                self.timer.timeout.connect(self.update_volume)
                
                self.slider.valueChanged[int].connect(self.setLabel)
                
                self.start.clicked.connect(self.start_process)
                self.stop.clicked.connect(self.stop_process)
                
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
                except Exception as e:
                        Dialogs.dialog(text=str(e))


        def setLabel(self, value):
                self.label.setText(str(value))
                self.program.set_sensivility(value)

        def start_process(self):
                try:
                        self.start.setEnabled(False)
                        self.timer.start()
                        
                        self.program.start()
                        
                except Exception as e:
                        Dialogs.dialog(text=str(e))
                        

        def stop_process(self):
                try:
                        self.start.setEnabled(True)
                        self.stop_timer()

                        self.program.stop()
                        
                except Exception as e:
                        Dialogs.dialog(text=str(e))                        

        def stop_timer(self):
                        self.timer.stop()
                        self.bar.setValue(0)
                        
if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Interface()
        sys.exit(app.exec_())
        
