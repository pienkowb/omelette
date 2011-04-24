from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsItem

class Drawable(object):
    """
    Base for other Drawable objects.
    Holds uml_object and list of anchors which are in slot relation with it.
    """

    def __init__(self, uml_object):
        self.uml_object = uml_object
        self.anchors = []

    """
    Crops QLineF, used mainly in relation to properly draw line 
    from one object to another. line_point is 0 when line.p1() is inside
    of the drawable, everything else when line.p2() inside. 
    
    This method shall be overloaded in specific drawables.  
    """
    def crop_line(self, line, line_point):
        return line

    """
    Returns boundingRect in relation to the diagram. Doesn't work if
    Drawable doesn't derive from QGraphicsItem (no boundingRect()).
    """
    #TODO: See if PyQt provides such functionality
    def globalBoundingRect(self):
        global_rect = QRectF(self.boundingRect())
        global_rect.translate(self.pos())

        return global_rect
    
    def resize_scene_rect(self):
        # Check if we are QGraphicsItem and if we are on scene
        if(not callable(self.scene) or self.scene() == None): 
            return
        
        # TODO: A place for optimization?
        rect = QRectF(self.scene().sceneRect())
        self.scene().setSceneRect(rect.united(self.globalBoundingRect()))

class DrawableEdge(Drawable):
    """Base class for edgy things (e.g. lines, relations)."""

    def __init__(self, uml_object):
        super(DrawableEdge, self).__init__(uml_object)

        self.source_anchor = None
        self.target_anchor = None


class DrawableNode(Drawable):
    """Base class for node-like diagram elements (e.g. classes, use cases)."""

    def __init__(self, uml_object):
        super(DrawableNode, self).__init__(uml_object)


class Anchor(object):
    """
    Class representing connection between edge (connector) and something else
    (slot).
    """

    def __init__(self):
        self.connector = None
        self.slot = None
