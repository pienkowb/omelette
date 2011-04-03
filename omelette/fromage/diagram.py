import inspect
from omelette.fromage.common import DrawableNode, DrawableEdge, Anchor


class _DrawableFactory(object):
    def __init__(self, modules_path):
        self.drawables = {}
        self.modules_path = modules_path

    def create(self, uml_object):
        type_ = uml_object.type
        if not type_ in self.drawables:
            self.drawables[type_] = self.__get_drawable(type_)
        return self.drawables[type_](uml_object)

    def __get_drawable(self, type_):
        module = self.__import(self.modules_path + "." + type_.lower())
        name = "Drawable" + type_
        match = filter(lambda n: n.lower() == name.lower(), dir(module)).pop()
        drawable = getattr(module, match, None)

        if inspect.isclass(drawable):
            return drawable

    def __import(self, name):
        module = __import__(name)
        components = name.split(".")

        for component in components[1:]:
            module = getattr(module, component)

        return module


class Diagram(object):

    def __init__(self, parent=None, modules_path="omelette.fromage.modules"):
        self.factory = _DrawableFactory(modules_path)
        self.nodes = {}
        self.edges = {}

    def add(self, uml_object):
        drawable = self.factory.create(uml_object)
        drawable.update()

        if isinstance(drawable, DrawableNode):
            self.nodes[uml_object.name] = drawable
        elif isinstance(drawable, DrawableEdge):
            self.edges[uml_object.name] = drawable
        else:
            raise AttributeError("Tried to create an object from a corrupted " +
                "module")

    def elements(self):
        return self.nodes.values() + self.edges.values()

    def set_anchors(self):
        for edge in self.edges.values():
            source, target = self.__get_slots(edge)
            source_anchor, target_anchor = self.__create_anchors(edge)

            edge.source_anchor = source_anchor
            edge.target_anchor = target_anchor

            source.anchors.append(source_anchor)
            target.anchors.append(target_anchor)

    def __create_anchors(self, edge):
        target_anchor = Anchor()
        source_anchor = Anchor()
        source, target = self.__get_slots(edge)

        source_anchor.connector = target_anchor.connector = edge
        source_anchor.slot = source
        target_anchor.slot = target

        return source_anchor, target_anchor

    def __get_slots(self, edge):
        source = self.__get_object(edge, "source-object")
        target = self.__get_object(edge, "target-object")
        return source, target

    def __get_object(self, edge, key):
        try:
            return self.nodes[edge.uml_object[key]]
        except KeyError:
            return self.edges[edge.uml_object[key]]

    def clear(self):
        self.nodes.clear()
        self.edges.clear()
