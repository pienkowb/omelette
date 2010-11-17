import sys

from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication ,QMainWindow, QWidget, QVBoxLayout, QIcon
from toolbar import *
from qscintilla import *

class MainWindow(QMainWindow):
    def __init__(self):
        ##Window
        QMainWindow.__init__(self)
        self.setWindowTitle('Example for UML syntax')
        self.setWindowIcon(QIcon.fromTheme('accessories-text-editor'))
        self.resize(600,400)

        ##Widget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        ##Layout
        self.layout = QVBoxLayout(self.widget)
        self.layout.setMargin(2)

        ##QScintilla editor
        self.editor = QSci(self)

        ##Toolbar
        self.toolbar = ToolBar(self, self.editor)

        
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.editor)


if __name__ == "__main__":
        app = QApplication(sys.argv)
        app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
        win = MainWindow()
        win.show()
sys.exit(app.exec_())