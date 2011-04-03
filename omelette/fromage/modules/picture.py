from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *

class DrawableIcon(DrawableNode, QGraphicsPixmapItem):
    def __init__(self, uml_object):
        super(DrawableIcon, self).__init__(uml_object)
        QGraphicsPixmapItem.__init__(self)
        
    def update(self):
        pass