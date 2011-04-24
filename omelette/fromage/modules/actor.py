import math

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

from omelette.fromage.common import *
from omelette.fromage.diagramcommon import DrawableText

class DrawableActor(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableActor, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        self.__sectionMargin = 5
        self.__textMargin = 3

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)
        
        self.__actor_rectangle = QRectF(0, 0, 50, 100)
        
        self.__actor_name_text = DrawableText.create_drawable_text(self)

    def boundingRect(self):
        return self.__boundingRect

    def paint(self, painter, style, widget):
        metrics = QFontMetrics(self.__font)
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        painter.fillRect(QRectF(self.__boundingRect), QBrush(QColor(255, 255, 255), Qt.SolidPattern))

        # painter.drawRect(self.__actor_rectangle)

        # TODO: Make lines dependent on __actor_rectangle
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        painter.drawEllipse(10,0,30,30)
        
        painter.drawLine(0, 40, 50, 40)
        painter.drawLine(25, 30, 25, 70)
        
        painter.drawLine(25, 70, 0, 100)
        painter.drawLine(25, 70, 50, 100)
        
        painter.setRenderHint(QPainter.Antialiasing, False)
        

    def __sizeOfSection(self, metrics, list):
        count = 0
        maxWidth = 0
        for text in list:
            maxWidth = max(maxWidth, 2 * self.__textMargin + metrics.width(text))
            count += 1

        return (maxWidth, 2 * self.__sectionMargin + (count - 1) * self.__textMargin + count * metrics.height())

    def update(self):
        metrics = QFontMetrics(self.__font)
        
        self.__boundingRect = QRectF(self.__actor_rectangle)
        globalRect = self.globalBoundingRect()
        
        # TODO: This again
        if "name" not in self.uml_object.properties:
            self.uml_object["name"] = self.uml_object.name
            
            
        self.__actor_name_text.text = self.uml_object["name"]
        self.__actor_name_text.origin_pos = QPointF(globalRect.x() + globalRect.width() / 2, globalRect.y() + globalRect.height())
        if(not self.__actor_name_text.isVisible()):
            textpos = QPointF(self.__actor_name_text.origin_pos)
            textpos.setX(textpos.x() - metrics.width(self.uml_object["name"]) / 2) # Making text centered
            self.__actor_name_text.setPos(textpos)
            self.__actor_name_text.setVisible(True)
            
            

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
