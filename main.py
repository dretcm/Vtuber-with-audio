import sys
from PyQt5.QtWidgets import QApplication
from data.interface import Interface

if __name__ == "__main__":
        try:
                app = QApplication(sys.argv)
                
                ex = Interface()
                sys.exit(app.exec_())
        except Exception as e:
                print(str(e))
                sys.exit(1)


