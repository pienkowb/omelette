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

    def __create(self, uml_object):
        module = _import(self.modules_path + "." + uml_object.type.lower())

        name = "Drawable" + uml_object.type
        match = filter(lambda n: n.lower() == name.lower(), dir(module)).pop()

        drawable = getattr(module, match, None)

        if inspect.isclass(drawable):
            return drawable(uml_object)

    def add(self, uml_object):
        drawable = self.__create(uml_object)

        self.addItem(drawable)
        drawable.update()

        if isinstance(drawable, DrawableNode):
            self.nodes[uml_object.name] = drawable
        elif isinstance(drawable, DrawableEdge):
            self.edges[uml_object.name] = drawable
        else:
            raise AttributeError("Tried to create an object from a corrupted " +
                "module")

    def clear(self):
        super(Diagram, self).clear()

        self.nodes.clear()
        self.edges.clear()
