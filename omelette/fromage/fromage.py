import sys
sys.path.append('../../') 
from PyQt4 import QtGui, QtCore
from omelette.parser.parser import Parser
from omelette.fromage.ui import Ui_MainWindow
from omelette.fromage.qscintilla import QSci
from omelette.fromage.factory import _import
from omelette.parser.uml import UMLObject

from omelette.fromage.modules.notakeyword import DrawableRelation

__import__("omelette.fromage.modules.class", fromlist=["DrawableClass"])

"""
class Scene(QtGui.QGraphicsScene):
    def mousePressEvent(self, event):
        self.rel.setLine(QtCore.QLineF(self.rel.line().p1(), QtCore.QPointF(event.scenePos().x(), event.scenePos().y())))
        self.rel.update()
   """     

class FromageForm(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.filename = QtCore.QString()
        self.parser = Parser()
        self.setupUi(self)

        self.layout = QtGui.QHBoxLayout(self.centralwidget)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        self.qsci = QSci(self.splitter)
        self.scene = QtGui.QGraphicsScene(self.splitter)
        #self.scene = Scene(self.splitter)
        self.view = QtGui.QGraphicsView(self.splitter)
        self.view.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 500, 500))

        self.layout.addWidget(self.splitter)

        QtCore.QObject.connect(self.actionGenerate, QtCore.SIGNAL("triggered()"), self.generate)
        QtCore.QObject.connect(self.actionNew, QtCore.SIGNAL("triggered()"), self.new_file)
        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.open_file)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL("triggered()"), self.save_file)
        QtCore.QObject.connect(self.actionSaveAs, QtCore.SIGNAL("triggered()"), self.save_file_as)
        QtCore.QObject.connect(self.actionCut, QtCore.SIGNAL("triggered()"), self.cut)
        QtCore.QObject.connect(self.actionCopy, QtCore.SIGNAL("triggered()"), self.copy)
        QtCore.QObject.connect(self.actionPaste, QtCore.SIGNAL("triggered()"), self.paste)
        QtCore.QObject.connect(self.actionUndo, QtCore.SIGNAL("triggered()"), self.undo)
        QtCore.QObject.connect(self.actionRedo, QtCore.SIGNAL("triggered()"), self.redo)
        QtCore.QObject.connect(self.qsci, QtCore.SIGNAL("textChanged()"), self.enable_save)
    
        umlo = UMLObject()
        umlo['name'] = 'jogi'
        
        umlo2 = UMLObject()
        umlo2['name'] = 'jogi class'
        umlo2.add_attribute("- nie chce pracowac")
        umlo2.add_attribute("- focha sie po 2h pracy")
        umlo2.add_attribute("- wersjonuje na wrzucie")
        umlo2.add_attribute("+ napisal parser")
        
        umlo3 = UMLObject()
        umlo3['name'] = 'piotr class'
        umlo3.add_attribute("+ ma brode")
        umlo3.add_attribute("- nie napisal layoutera")
        
        module = _import("omelette.fromage.modules.class")

        name = "DrawableClass"
        drawable = getattr(module, name, None)
    
        dc1 = drawable(umlo2)
        dc2 = drawable(umlo3)
        
        for dc in [dc1, dc2]:
            dc.updateSize()
            dc.addToScene(self.scene)
    
        self.scene.rel = DrawableRelation(umlo)
        self.scene.rel.source = dc1
        self.scene.rel.target = dc2 
        self.scene.rel.update()
        
        
        self.scene.rel.addToScene(self.scene)

    def generate(self):
        self.scene.clear()
        self.__x = self.__y = self.__highest_y = 0
        code = "prototype base class\n" + self.qsci.text()
        uml_objects = self.parser.parse(code)

        for name, uml_object in uml_objects.items():
            if "name" not in uml_object.properties:
                uml_object["name"] = name

        for uml_object in uml_objects.values():
            if uml_object.is_prototype: continue
    
            drawable = DrawableFactory.create("class", uml_object)
            drawable.updateSize()
            self.__layout(drawable)
            self.scene.addItem(drawable)

    def __layout(self, drawable):
        drawable.moveBy(self.__x, self.__y)
        self.__x += 20 + drawable.boundingRect().size().width()
        if drawable.boundingRect().size().height() > self.__highest_y:
                self.__highest_y = drawable.boundingRect().size().height()
        if self.__x > 400:
            self.__x = 0
            self.__y += self.__highest_y + 20
            self.__highest_y = 0

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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = FromageForm()
    form.show()
    sys.exit(app.exec_())
