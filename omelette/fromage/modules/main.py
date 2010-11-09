import sys

from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication ,QMainWindow
from qscintilla import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Lexer example for UML syntax')
        self.setGeometry(50,200,400,400)

        self.editor = QSci(self)
        self.setCentralWidget(self.editor)


if __name__ == "__main__":
        app = QApplication(sys.argv)
        app.connect(app, SIGNAL('lastWindowClosed()'), SLOT('quit()'))
        win = MainWindow()
        win.show()
sys.exit(app.exec_())