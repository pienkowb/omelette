from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

class DrawableClass(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableClass, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        self.__sectionMargin = 5
        self.__textMargin = 3

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)

    def boundingRect(self):
        return self.__boundingRect

    def paint(self, painter, style, widget):
        metrics = QFontMetrics(self.__font)
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))

        painter.fillRect(QRectF(self.__boundingRect), QBrush(QColor(255, 255, 255), Qt.SolidPattern))

        # Name of the class        
        currentHeight = self.__sectionMargin
        painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(self.uml_object['name']), metrics.height()), 0, self.uml_object['name'])
        currentHeight += self.__sectionMargin + metrics.height()
        
        # Attributes section
        painter.drawLine(0, currentHeight, self.__boundingRect.width(), currentHeight)
        currentHeight += self.__sectionMargin
        for attribute in map(str, self.uml_object.attributes()):
            painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(attribute), metrics.height()), 0, attribute)
            currentHeight += self.__textMargin + metrics.height()
        
        # Operations section
        painter.drawLine(0, currentHeight, self.__boundingRect.width(), currentHeight)
        
        currentHeight += self.__sectionMargin
        for operation in map(str, self.uml_object.operations()):
            painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(operation), metrics.height()), 0, operation)
            currentHeight += self.__textMargin + metrics.height()

        painter.drawRect(self.__boundingRect)

    def __sizeOfSection(self, metrics, list):
        count = 0
        maxWidth = 0
        for text in list:
            maxWidth = max(maxWidth, 2 * self.__textMargin + metrics.width(text))
            count += 1

        return (maxWidth, 2 * self.__sectionMargin + (count - 1) * self.__textMargin + count * metrics.height())

    def update(self):
        metrics = QFontMetrics(self.__font)
        # Start by finding size of class name block
        drawableHeight = 1 * self.__sectionMargin + metrics.height()
        drawableWidth = 2 * self.__textMargin + metrics.width(self.uml_object['name'])

        # Find sizes of each section and update width/height
        for section in [map(str, self.uml_object.operations()), map(str,
            self.uml_object.attributes())]:
            size = self.__sizeOfSection(metrics, section)
            drawableWidth = max(drawableWidth, size[0])
            drawableHeight += size[1]

        self.__boundingRect = QRectF(0, 0, 2 * self.__textMargin + drawableWidth, drawableHeight)

    def przytnij_linie(self, line, ktory_bok):
        global_rect = self.globalBoundingRect()
        
        punkty = [global_rect.topLeft(), global_rect.topRight(),
                  global_rect.bottomRight(), global_rect.bottomLeft()]
        
        intersectionPoint = QPointF()
        
        for (a, b) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            bok = QLineF(punkty[a], punkty[b])
            itype = line.intersect(bok, intersectionPoint)
            if(itype == QLineF.BoundedIntersection):
                if(ktory_bok == 0):
                    return QLineF(intersectionPoint, line.p2())
                else:
                    return QLineF(line.p1(), intersectionPoint)
        
        return line
        
    def znajdz_anchor(self):
        return self.globalBoundingRect().center()

    def itemChange(self, change, value):
        if(change == QGraphicsItem.ItemPositionChange):
            for anchor in self.anchors:
                anchor.connector.update()
                
        return QGraphicsItem.itemChange(self, change, value)

class DrawableRelation(DrawableEdge, QGraphicsLineItem):
    def __init__(self, uml_object):
        super(DrawableRelation, self).__init__(uml_object)
        QGraphicsLineItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        
    def boundingRect(self):
        return self.__boundingRect
    
    
