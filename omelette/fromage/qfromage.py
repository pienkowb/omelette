import sys
sys.path.append("../../")
from PyQt4 import QtGui, QtCore
from omelette.fromage.ui import Ui_MainWindow
from omelette.fromage.qscintilla import QSci
from omelette.fromage.actions import Actions

class QFromage(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.layout = QtGui.QHBoxLayout(self.centralwidget)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        self.qsci = QSci(self.splitter)
        self.scene = QtGui.QGraphicsScene(self.splitter)
        self.view = QtGui.QGraphicsView(self.splitter)
        self.view.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 500, 500))

        self.layout.addWidget(self.splitter)

        self.actions = Actions(self.qsci, self.scene, self.actionSave, self.actionSaveAs)

        QtCore.QObject.connect(self.actionGenerate, QtCore.SIGNAL("triggered()"), self.actions.generate)
        QtCore.QObject.connect(self.actionNew, QtCore.SIGNAL("triggered()"), self.actions.new_file)
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.actions.open_file)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL("triggered()"), self.actions.save_file)
        QtCore.QObject.connect(self.actionSaveAs, QtCore.SIGNAL("triggered()"), self.actions.save_file_as)
        QtCore.QObject.connect(self.actionCut, QtCore.SIGNAL("triggered()"), self.actions.cut)
        QtCore.QObject.connect(self.actionCopy, QtCore.SIGNAL("triggered()"), self.actions.copy)
        QtCore.QObject.connect(self.actionPaste, QtCore.SIGNAL("triggered()"), self.actions.paste)
        QtCore.QObject.connect(self.actionUndo, QtCore.SIGNAL("triggered()"), self.actions.undo)
        QtCore.QObject.connect(self.actionRedo, QtCore.SIGNAL("triggered()"), self.actions.redo)
        QtCore.QObject.connect(self.qsci, QtCore.SIGNAL("textChanged()"), self.actions.enable_save)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = QFromage()
    form.show()
    sys.exit(app.exec_())
