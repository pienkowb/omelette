from omelette.compiler.compiler import Compiler
from omelette.compiler.code import Code,Library
from omelette.fromage.ui import Ui_MainWindow
from omelette.fromage.layouter import Layouter
from omelette.fromage.diagram import Diagram
from PyQt4 import QtGui, QtCore
import sys, os

class Actions(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self, qsci, scene, actionSave, actionSaveAs, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.compiler = Compiler([self.__get_lib("basic.uml")])
        self.qsci = qsci
        self.scene = scene
        self.filename = QtCore.QString()
        self.setupUi(self)

        self.actionSave = actionSave
        self.actionSaveAs = actionSaveAs
        self.actionSave.setDisabled(True)
        self.actionSaveAs.setDisabled(True)

    def __get_lib(self, libname):
        cwd = os.path.dirname(os.path.realpath(__file__))
        libpath = os.path.normcase("../compiler/data/")
        lib = os.path.join(cwd, libpath , libname)

        return Library(lib)
                        
    def generate(self):
        self.scene.clear()
        self.diagram = Diagram()
        code = Code(str(self.qsci.text()))
        uml_objects = self.compiler.compile(code)

        for uml_object in uml_objects.values():
            self.diagram.add(uml_object)


        # nodes must be updated before layouting
        for node in self.diagram.nodes.values():
            node.update()

        # needed to layout and draw edges
        self.diagram.set_anchors()

        Layouter.layout(self.diagram)

        # edges must be updated after nodes are updated and layouted
        for edge in self.diagram.edges.values():
            edge.update()

        # this actually paints things, so must be invoked when everything is
        # ready
        for drawable in self.diagram.elements():
            self.scene.addItem(drawable)

    def enable_save(self):
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
            self.save_file_as()
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

    def save_file_as(self):
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
