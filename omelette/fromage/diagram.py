import inspect
from PyQt4 import QtGui
from common import BaseType

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

    def add(self, uml_objects):
        for o in uml_objects.values():
            self.__add_object(o)

    def __add_object(self, uml_object):
        o = self.__create(uml_object) 
        self.addItem(o)
        o.update()

        name = uml_object.name
        if o.base_type == BaseType.NODE:
            self.nodes[name] = o
        elif o.base_type == BaseType.EDGE:
            self.edges[name] = o
        else:
            raise AttributeError("Tried to create object from a corrupt module")

    def __create(self, uml_object):
        module = _import(self.diagram_path)
        name = "Drawable" + uml_object.type

        # capitalize prohibited creating modules with uppercase letters in name
        # example: with 'DrawableExampleA' changed to 'DrawableExamplea' and
        # won't match

        name = filter(lambda a: a.lower() == name.lower(), dir(module)).pop()
        drawable = getattr(module, name, None)

        if inspect.isclass(drawable):
            return drawable(uml_object)
