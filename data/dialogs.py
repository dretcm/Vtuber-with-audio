import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication

class Dialogs(QWidget):
        def __init__(self):
                super().__init__()

        @staticmethod
        def dialog(title='Error!', text = 'There was a mistake.', icon=QMessageBox.Warning):
                msgBox = QMessageBox()
                msgBox.setIcon(icon)
                msgBox.setText(text)
                msgBox.setWindowTitle(title)
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
                
if __name__=='__main__':
        app = QApplication(sys.argv)
        Dialogs.dialog()
        sys.exit(app.exec_())
