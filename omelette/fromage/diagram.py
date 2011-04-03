import inspect
from PyQt4 import QtGui
from omelette.fromage.common import DrawableNode, DrawableEdge, Anchor

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

    def set_anchors(self):
        for edge in self.edges.values():
            source, target = self.__get_nodes(edge)
            source_anchor, target_anchor = self.__create_anchors(edge)

            edge.source_anchor = source_anchor
            edge.target_anchor = target_anchor

            source.anchors.append(source_anchor)
            target.anchors.append(target_anchor)

    def __create_anchors(self, edge):
        target_anchor = Anchor()
        source_anchor = Anchor()
        source, target = self.__get_nodes(edge)

        source_anchor.connector = target_anchor.connector = edge
        source_anchor.slot = source
        target_anchor.slot = target

        return source_anchor, target_anchor

    def __get_nodes(self, edge):
        source = self.nodes[edge.uml_object['source-object']]
        target = self.nodes[edge.uml_object['target-object']]
        return source, target


    def clear(self):
        super(Diagram, self).clear()

        self.nodes.clear()
        self.edges.clear()
