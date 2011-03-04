class Drawable(object):
    """
    Base for other Drawable objects. It's made with UMLObject, and
    provides interface for accessing its attributes, properties and
    operations. Properties are accessible via [] operator.
    """

    def __init__(self, uml_object):
        self.uml_object = uml_object


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

