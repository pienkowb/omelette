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
    
    def __init__(self, diagram, parent=None, modules_path="omelette.fromage.modules"):
        super(QtGui.QGraphicsScene, self).__init__(parent)
        self.diagram_path = modules_path + "." + diagram
        self.nodes = {}
        self.edges = {}

    def add(self, uml_object):
        name = uml_object.name
        o = self.__create(uml_object) 
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
