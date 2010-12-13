import sys
from PyQt4 import QtGui, QtCore
from omelette.fromage.modules.qscintilla import QSci
from omelette.fromage.modules.fromage_ui import Ui_MainWindow

class FromageForm(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.horizontal_layout = QtGui.QHBoxLayout(self.centralwidget)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)


        self.qsci = QSci(self.splitter)
        #TODO change parameter splitter to DiagramScene
        self.graphics_view = QtGui.QGraphicsView(self.splitter)

        self.horizontal_layout.addWidget(self.splitter)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = FromageForm()
    form.show()
    sys.exit(app.exec_())