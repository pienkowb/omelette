import sys

from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication ,QMainWindow, QWidget, QVBoxLayout, QIcon
from toolbar import *
from qscintilla import *

class MainWindow(QMainWindow):
    def __init__(self):
        ##Window
        QMainWindow.__init__(self)
        self.setWindowTitle('Lexer example for UML syntax')
        self.setWindowIcon(QIcon.fromTheme('accessories-text-editor'))
        self.resize(600,400)

        ##Widget
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        ##Layout
        self.layout = QVBoxLayout(self.widget)
        self.layout.setMargin(2)

        ##Toolbar
        actions_dict = {'action_new':("document-new", "New"),
                        'action_open':("document-open", "Open"),
                        'action_save':("document-save", "Save"),
                        'action_save_as':("document-save-as", "Save As"),
                        'action_cut':("edit-cut", "Cut"),
                        'action_copy':("edit-copy", "Copy"),
                        'action_paste':("edit-paste", "Paste"),
                        'action_undo':("edit-undo", "Undo"),
                        'action_redo':("edit-redo", "Redo"),
                        'action_execute':("edit-Execute", "Execute")}
        self.toolbar = ToolBar(self,actions_dict)

        ##QScintilla editor
        self.editor = QSci(self)


        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.editor)


if __name__ == "__main__":
        app = QApplication(sys.argv)
        app.connect(app, SIGNAL('lastWindowClosed()'), SLOT('quit()'))
        win = MainWindow()
        win.show()
sys.exit(app.exec_())