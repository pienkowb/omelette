from PyQt4.QtCore import QRectF

class BaseType:
    NODE = 1
    EDGE = 2


class Drawable(object):
    """
    Base for other Drawable objects.
    Holds uml_object and list of anchors which are in slot relation with it.
    """

    def __init__(self, uml_object):
        self.uml_object = uml_object
        self.anchors = []
        self.base_type = 0
        
    def przytnij_linie(self, line):
        return line
    
    #TODO: See if PyQt provides such functionality
    def globalBoundingRect(self):
        global_rect = QRectF(self.boundingRect())
        global_rect.translate(self.pos())
        
        return global_rect
    
class DrawableEdge(Drawable):
    """Base class for edgy things (e.g. lines, relations)."""

    def __init__(self, uml_object):
        super(DrawableEdge, self).__init__(uml_object)
        self.base_type = BaseType.EDGE

        self.source_anchor = None
        self.target_anchor = None


class DrawableNode(Drawable):
    """Base class for node-like diagram elements (e.g. classes, use cases)."""

    def __init__(self, uml_object):
        super(DrawableNode, self).__init__(uml_object)
        self.base_type = BaseType.NODE


class Anchor(object):
    """
    Class representing connection between edge (connector) and something else
    (slot).
    """

    def __init__(self, connector, slot):
        self.connector = connector
        self.slot = slot
