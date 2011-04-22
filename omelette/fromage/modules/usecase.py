import math

from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

class DrawableUseCase(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableUseCase, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)
        
    def boundingRect(self):
        return self.__boundingRect

    def paint(self, painter, style, widget):
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QBrush(QColor(255, 255, 255), Qt.SolidPattern))
        
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawEllipse(self.__boundingRect)
        painter.setRenderHint(QPainter.Antialiasing, False)
        
        painter.drawText(self.__text_rect, 0, self.uml_object['name'])
    
    def update(self):
        metrics = QFontMetrics(self.__font)
        # Start by finding size of class name block
        textHeight = metrics.height()

        # TODO: This doesn't belong here. Or does it?
        if "name" not in self.uml_object.properties:
            self.uml_object["name"] = self.uml_object.name

        textWidth = metrics.width(self.uml_object['name'])

        ratio = (float(textWidth) / textHeight) / 1.5
        
        drawableHeight = textHeight * 2
        drawableWidth = ratio * drawableHeight
        
        print "%f" % ratio
        
        if(ratio > 3.5):
            drawableHeight = drawableWidth / max(3.5, ratio/3)

        self.__text_rect = QRectF((drawableWidth - textWidth) / 2,
                                  (drawableHeight - textHeight) / 2,
                                  textWidth, textHeight)

        self.__boundingRect = QRectF(0, 0, drawableWidth, drawableHeight)

    def crop_line(self, line, line_point):
        global_rect = self.globalBoundingRect()
        
        vertexes = [global_rect.topLeft(), global_rect.topRight(),
                  global_rect.bottomRight(), global_rect.bottomLeft()]
        
        intersectionPoint = QPointF()
        
        # Iterate over pairs of vertexes that make rectangle edges
        for (a, b) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            bok = QLineF(vertexes[a], vertexes[b])
            itype = line.intersect(bok, intersectionPoint)
            if(itype == QLineF.BoundedIntersection):
                if(line_point == 0):
                    return QLineF(intersectionPoint, line.p2())
                else:
                    return QLineF(line.p1(), intersectionPoint)
        
        return line
        
    def find_anchor(self):
        return self.globalBoundingRect().center()

    def itemChange(self, change, value):
        if(change == QGraphicsItem.ItemPositionChange):
            for anchor in self.anchors:
                anchor.connector.update()
                
        return QGraphicsItem.itemChange(self, change, value)