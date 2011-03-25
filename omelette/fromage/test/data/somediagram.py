from omelette.fromage.common import *
from PyQt4.QtGui import *

class DrawableEdge(DrawableEdge, QGraphicsItem):
    def __init__(self, o):
        super(QGraphicsItem, self).__init__()
        super(DrawableEdge, self).__init__(o)

class DrawableNode(DrawableNode, QGraphicsItem):
    def __init__(self, o):
        super(QGraphicsItem, self).__init__()
        super(DrawableNode, self).__init__(o)
