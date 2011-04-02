import inspect
from PyQt4 import QtGui
from common import BaseType, Anchor

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
        self.drawables = {}
        self.nodes = {}
        self.edges = {}

    def set_type(self, diagram_type):
        self.common_path = self.modules_path + ".notakeyword"
        self.diagram_path = self.modules_path + "." + diagram_type

    def clear(self):
        super(Diagram, self).clear()
        self.nodes.clear()
        self.edges.clear()

    def add(self, uml_objects):
        for o in uml_objects.values():
            self.__add_object(o)
            
        self.__resolve_all_refs()
        self.__update_all()

    def __add_object(self, uml_object):
        o = self.__create(uml_object) 
        self.addItem(o)

        name = uml_object.name
        self.drawables[name] = o
        if o.base_type == BaseType.NODE:
            self.nodes[name] = o
        elif o.base_type == BaseType.EDGE:
            self.edges[name] = o
        else:
            raise AttributeError("Tried to create object from a corrupt module")

    def __create(self, uml_object):
        modules = [_import(self.common_path), _import(self.diagram_path)]
        
        for module in modules:
            name = "Drawable" + uml_object.type
    
            # capitalize prohibited creating modules with uppercase letters in name
            # example: with 'DrawableExampleA' changed to 'DrawableExamplea' and
            # won't match
    
            matching = filter(lambda a: a.lower() == name.lower(), dir(module))
            if(len(matching) == 0):
                continue
            name = matching.pop()
            drawable = getattr(module, name, None)
    
            if inspect.isclass(drawable):
                return drawable(uml_object)
                
    def __resolve_refs(self, drawable):
        type = drawable.uml_object.type.lower()
        if(type == 'relation'):
            drawable.source = self.drawables[drawable.uml_object['source-object']]
            drawable.source.anchors.append(Anchor(drawable, drawable.source))
            
            drawable.target = self.drawables[drawable.uml_object['target-object']]
            drawable.target.anchors.append(Anchor(drawable, drawable.target))
    
    def __resolve_all_refs(self):
        for obj in self.drawables.itervalues():
            self.__resolve_refs(obj)
    
    def __update_all(self):
        for obj in self.drawables.itervalues():
            obj.update()
            
            
            