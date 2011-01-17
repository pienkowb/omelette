import sys
from PyQt4 import QtGui, QtCore
from omelette.fromage.qscintilla import QSci
from omelette.fromage.fromage_ui import Ui_MainWindow

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

        self.filename = QtCore.QString()

        QtCore.QObject.connect(self.actionGenerate, QtCore.SIGNAL("triggered()"), self.qsci.get_lines)
        QtCore.QObject.connect(self.actionNew, QtCore.SIGNAL("triggered()"), self.new_file)
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open_file)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL("triggered()"), self.save_file)
        QtCore.QObject.connect(self.actionSaveAs, QtCore.SIGNAL("triggered()"), self.saveAs_file)
        QtCore.QObject.connect(self.actionCut, QtCore.SIGNAL("triggered()"), self.cut)
        QtCore.QObject.connect(self.actionCopy, QtCore.SIGNAL("triggered()"), self.copy)
        QtCore.QObject.connect(self.actionPaste, QtCore.SIGNAL("triggered()"), self.paste)
        QtCore.QObject.connect(self.actionUndo, QtCore.SIGNAL("triggered()"), self.undo)
        QtCore.QObject.connect(self.actionRedo, QtCore.SIGNAL("triggered()"), self.redo)
        QtCore.QObject.connect(self.qsci, QtCore.SIGNAL("textChanged()"), self.enable_saveBtn)


    def enable_saveBtn(self):
        self.actionSave.setEnabled(True)
        self.actionSaveAs.setEnabled(True)

    def new_file(self):
        self.qsci.setText(QtCore.QString(""))
        self.actionSave.setDisabled(True)
        self.actionSaveAs.setDisabled(True)
        self.statusbar.showMessage('Created empty document', 2000)

    def open_file(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, QtCore.QString(), QtCore.QString())
        if fn.isEmpty():
            self.statusbar.showMessage('Loading aborted', 2000)
            return
        filename = str(fn)
        self.qsci.clear()

        try:
            f = open(filename, 'r')
        except:
            return

        for line in f:
            self.qsci.append(line)

        f.close()

        self.setWindowTitle(filename)
        self.statusbar.showMessage('Loaded document %s' % (filename), 2000)

    def save_file(self):
        if self.filename.isEmpty():
            self.saveAs_file()
            return
        try:
            f = open(str(self.filename), 'w+')
        except:
            self.statusbar.showMessage('Cannot write to %s' % (self.filename), 2000)
            return

        f.write(str(self.qsci.text()))
        f.close()

        self.qsci.setModified(0)
        self.setWindowTitle(self.filename)
        self.statusbar.showMessage('Document %s saved' % (self.filename), 2000)

    def saveAs_file(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, QtCore.QString(), QtCore.QString())
        if not fn.isEmpty():
            self.filename = fn
            self.save_file()
        else:
            self.statusbar.showMessage('Saving aborted', 2000)

    def cut(self):
        self.qsci.cut()

    def copy(self):
        self.qsci.copy()

    def paste(self):
        self.qsci.paste()

    def undo(self):
        self.qsci.undo()

    def redo(self):
        self.qsci.redo()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = FromageForm()
    form.show()
    sys.exit(app.exec_())