import inspect
from PyQt4 import QtGui
from omelette.fromage.common import DrawableNode, DrawableEdge

def _import(name):
    module = __import__(name)
    components = name.split(".")

    for component in components[1:]:
        module = getattr(module, component)

    return module


class Diagram(QtGui.QGraphicsScene):

    def __init__(self, parent=None, modules_path="omelette.fromage.modules"):
        super(Diagram, self).__init__(parent)
        self.modules_path = modules_path
        self.nodes = {}
        self.edges = {}

    def set_type(self, diagram_type):
        self.diagram_path = self.modules_path + "." + diagram_type

    def clear(self):
        super(Diagram, self).clear()

        self.nodes.clear()
        self.edges.clear()

    def add(self, uml_object):
        object = self.__create(uml_object)

        self.addItem(object)
        object.update()

        if isinstance(object, DrawableNode):
            self.nodes[uml_object.name] = object
        elif isinstance(object, DrawableEdge):
            self.edges[uml_object.name] = object
        else:
            raise AttributeError("Tried to create an object from a corrupted" +
                " module")

    def __create(self, uml_object):
        module = _import(self.diagram_path)
        name = "Drawable" + uml_object.type

        name = filter(lambda a: a.lower() == name.lower(), dir(module)).pop()
        drawable = getattr(module, name, None)

        if inspect.isclass(drawable):
            return drawable(uml_object)
