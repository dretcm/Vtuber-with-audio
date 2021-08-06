import sys
from PyQt5.QtWidgets import QApplication
from data.interface import Interface
from data.dialogs import Dialogs

if __name__ == "__main__":
        try:
                app = QApplication(sys.argv)
                
                ex = Interface()
                sys.exit(app.exec_())
        except Exception as e:
                Dialogs.dialog(text=str(e))
                sys.exit(1)


