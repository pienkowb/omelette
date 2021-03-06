#!/usr/bin/env python
import sys, os

script_path = os.path.dirname(os.path.realpath(__file__))
modules_path = os.path.normcase("../../")
modules_directory = os.path.join(script_path, modules_path)
sys.path.append(modules_directory)

from PyQt4 import QtGui, QtCore
from omelette.fromage.ui import Ui_MainWindow
#from omelette.fromage.fromage_editor import FromageEditor
from omelette.fromage.qscintilla import QSci
from omelette.fromage.actions import Actions
from omelette.fromage.scalable_view import ScalableView
from omelette.fromage.layouter import *

class QFromage(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        frect = self.frameGeometry()
        frect.moveCenter(QtGui.QDesktopWidget().availableGeometry().center())
        self.move(frect.topLeft())

        self.setupUi(self)

        self.hlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.vlayout = QtGui.QVBoxLayout(self.dockContents)

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        self.qsci = QSci(self.splitter)
        #self.qsci = FromageEditor(self.splitter)
        self.scene = QtGui.QGraphicsScene(self.splitter)
        self.scalable_view = ScalableView(self.splitter)
        self.scalable_view.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 500, 500))
        self.splitter.setSizes([1,1])

        self.msg_view = QtGui.QTableWidget()
        self.msg_view.setColumnCount(3)
        self.msg_view.setHorizontalHeaderLabels(["Marker", "Line number", "Message"])
        self.msg_view.horizontalHeader().setStretchLastSection(True)
        self.msg_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.msg_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        for i in range(3):
            self.msg_view.horizontalHeaderItem(i).setTextAlignment(0x0001)

        self.vlayout.addWidget(self.msg_view)
        self.hlayout.addWidget(self.splitter)

        layouts_names = LayoutFactory.layouts()

        for name in layouts_names:
            self.layout = QtGui.QAction(self)
            self.layout.setObjectName(QtCore.QString.fromUtf8(name))
            self.layout.setCheckable(True)
            self.layout.setText(name)
            self.menuLayout.addAction(self.layout)

        self.actions = Actions(self)

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
        QtCore.QObject.connect(self.actionExport, QtCore.SIGNAL("triggered()"), self.actions.export)
        QtCore.QObject.connect(self.menuLayout, QtCore.SIGNAL("triggered(QAction*)"), self.actions.get_layout_name)
        QtCore.QObject.connect(self.menuLayout, QtCore.SIGNAL("triggered(QAction*)"), self.actions.check_layout_item)
        QtCore.QObject.connect(self.msg_view, QtCore.SIGNAL("cellDoubleClicked(int,int)"), self.actions.jump_to_line)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = QFromage()

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            for line in f:
                form.qsci.append(line)
            form.actions.generate()
            form.show()
    else:
        form.show()

    sys.exit(app.exec_())
