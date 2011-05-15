from PyQt4 import QtGui, QtCore
from omelette.compiler.code import Code, Library
from omelette.compiler.compiler import Compiler
from omelette.fromage.ui import Ui_MainWindow
from omelette.fromage.layouter import Layouter
from omelette.fromage.diagram import Diagram
from PyQt4.QtGui import QImage, QPainter

class Actions(object):

    def __init__(self, window, parent=None):
        self.compiler = Compiler(Library.load_libraries())
        self.window = window

        self.filename = QtCore.QString()
        self.window.actionSave.setDisabled(True)
        self.window.actionSaveAs.setDisabled(True)

        self.window.actionCircular_Layout.setChecked(True)
        self.is_layout_spring = False

    def generate(self):
        self.compiler.clear()
        self.window.scene.clear()
        self.diagram = Diagram()
        code = Code(str(self.window.qsci.text()))
        uml_objects = self.compiler.compile(code)

        for uml_object in uml_objects.values():
            self.diagram.add(uml_object)

        # nodes must be updated before layouting
        for node in self.diagram.nodes.values():
            node.update()

        # needed to layout and draw edges
        self.diagram.set_anchors()

        if self.isLayoutSpring():
            Layouter.layout(self.diagram)
        else:
            Layouter.layout(self.diagram,0)

        # edges must be updated after nodes are updated and layouted
        for edge in self.diagram.edges.values():
            edge.update()

        # this actually paints things, so must be invoked when everything is
        # ready
        for drawable in self.diagram.elements():
            self.window.scene.addItem(drawable)
            drawable.resize_scene_rect()

    def enable_save(self):
        self.window.actionSave.setEnabled(True)
        self.window.actionSaveAs.setEnabled(True)

    def new_file(self):
        self.window.qsci.setText(QtCore.QString(""))
        self.window.actionSave.setDisabled(True)
        self.window.actionSaveAs.setDisabled(True)
        self.window.statusbar.showMessage('Created empty document', 2000)

    def open_file(self):
        fn = QtGui.QFileDialog.getOpenFileName(self.window, "Load file", QtCore.QString(), "UML Files (*.uml)")
        if fn.isEmpty():
            self.window.statusbar.showMessage('Loading aborted', 2000)
            return
        filename = str(fn)
        self.window.qsci.clear()

        try:
            f = open(filename, 'r')
        except:
            return

        for line in f:
            self.window.qsci.append(line)

        f.close()

        self.window.setWindowTitle(filename)
        self.window.statusbar.showMessage('Loaded document %s' % (filename), 2000)

        self.generate()

    def save_file(self):
        if self.filename.isEmpty():
            self.save_file_as()
            return
        try:
            f = open(str(self.filename), 'w+')
        except:
            self.window.statusbar.showMessage('Cannot write to %s' % (self.filename), 2000)
            return

        f.write(str(self.window.qsci.text()))
        f.close()

        self.window.qsci.setModified(0)
        self.window.setWindowTitle(self.filename)
        self.window.statusbar.showMessage('Document %s saved' % (self.filename), 2000)

    def save_file_as(self):
        fn = QtGui.QFileDialog.getSaveFileName(self.window, QtCore.QString(), QtCore.QString())
        if not fn.isEmpty():
            self.filename = fn
            self.save_file()
        else:
            self.window.statusbar.showMessage('Saving aborted', 2000)

    def cut(self):
        self.window.qsci.cut()

    def copy(self):
        self.window.qsci.copy()

    def paste(self):
        self.window.qsci.paste()

    def undo(self):
        self.window.qsci.undo()

    def redo(self):
        self.window.qsci.redo()

    def export(self):
        fn = QtGui.QFileDialog.getSaveFileName(self.window, "Save Image", QtCore.QString(), "Image Files (*.png)");
        if fn.isEmpty():
            self.window.statusbar.showMessage('Saving aborted', 2000)
            return

        img = QImage(self.window.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        painter = QPainter(img)
        painter.resetMatrix()
        self.window.scene.render(painter)
        painter.end()

        if(img.save(fn) == False):
            self.window.statusbar.showMessage('Saving failed', 2000)
            return

        self.window.statusbar.showMessage('Image %s saved' % (self.filename), 2000)

    def circular_layout(self):
        if self.window.actionSpring_Layout.isChecked:
            self.window.actionSpring_Layout.setChecked(False)

        if self.window.actionCircular_Layout.isChecked:
            self.is_layout_spring = False

    def spring_layout(self):
        if self.window.actionCircular_Layout.isChecked:
            self.window.actionCircular_Layout.setChecked(False)

        if self.window.actionSpring_Layout.isChecked:
            self.is_layout_spring = True

    def isLayoutSpring(self):
        return self.is_layout_spring